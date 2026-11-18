"""Offline Markdown quality, local-link, and annotated contract checks."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from agentctl.risk import load_schema
from agentctl.system_risk import load_system_risk_schema
from agentctl.systems import load_system_schema
from agentctl.validation import load_agent_schema
from jsonschema import Draft202012Validator
from markdown_it import MarkdownIt

PARSER = MarkdownIt("commonmark").enable("table")


def tokens(path: Path):
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            text = "\n" * text[: end + 5].count("\n") + text[end + 5 :]
    return PARSER.parse(text)


def anchors(path: Path) -> set[str]:
    found = set()
    parsed = tokens(path)
    for index, token in enumerate(parsed):
        if token.type != "heading_open":
            continue
        children = parsed[index + 1].children or []
        title = "".join(
            child.content for child in children if child.type in {"text", "code_inline"}
        )
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        candidate, suffix = slug, 0
        while candidate in found:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        found.add(candidate)
    return found


def check_markdown(path: Path, root: Path) -> list[str]:
    errors = []
    shown = path.relative_to(root)
    parsed = tokens(path)
    previous_heading = 0
    for token in parsed:
        line = token.map[0] + 1 if token.map else 1
        prefix = f"{shown}:{line}"
        if token.type == "heading_open":
            level = int(token.tag[1:])
            if level > previous_heading + 1:
                errors.append(f"{prefix}: MD001 heading level skips a level")
            previous_heading = level
        if token.type == "fence":
            if not token.info.strip():
                errors.append(f"{prefix}: MD040 fenced code needs a language")
            parts = token.info.split()
            if len(parts) > 1 and parts[1] in {
                "agent-spec",
                "system-spec",
                "risk-assessment",
            }:
                loaders = {
                    "agent-spec": load_agent_schema,
                    "system-spec": load_system_schema,
                    "risk-assessment": load_schema,
                }
                try:
                    payload = yaml.safe_load(token.content)
                    for error in Draft202012Validator(loaders[parts[1]]()).iter_errors(
                        payload
                    ):
                        errors.append(f"{prefix}: {error.json_path}: {error.message}")
                except yaml.YAMLError as error:
                    errors.append(f"{prefix}: invalid YAML: {error}")
        for child in token.children or []:
            raw = (
                child.attrGet("href")
                if child.type == "link_open"
                else child.attrGet("src")
                if child.type == "image"
                else None
            )
            if not raw:
                continue
            target = urlsplit(raw)
            if target.scheme or target.netloc:
                continue
            destination = (
                (path.parent / unquote(target.path)).resolve()
                if target.path
                else path.resolve()
            )
            if not destination.is_relative_to(root.resolve()):
                errors.append(f"{prefix}: link escapes repository: {raw}")
            elif not destination.exists():
                errors.append(f"{prefix}: missing file: {raw}")
            elif (
                target.fragment
                and destination.suffix.lower() == ".md"
                and unquote(target.fragment) not in anchors(destination)
            ):
                errors.append(f"{prefix}: missing anchor: {raw}")
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if line.endswith((" ", "\t")) and not (
            line.endswith("  ") and not line.endswith("   ")
        ):
            errors.append(f"{shown}:{line_number}: MD009 trailing whitespace")
    return errors


def check_repository(root: Path) -> list[str]:
    paths = list(root.glob("*.md"))
    for directory in [
        "agent-playbook",
        "multi-agent-playbook",
        "skills",
        "docs",
        "examples",
        "tools",
    ]:
        paths.extend((root / directory).rglob("*.md"))
    errors = [error for path in sorted(paths) for error in check_markdown(path, root)]
    for relative, loader in [
        ("agent-playbook/templates/risk-assessment.yaml", load_schema),
        ("multi-agent-playbook/templates/system-spec.yaml", load_system_schema),
        (
            "multi-agent-playbook/templates/system-risk-assessment.yaml",
            load_system_risk_schema,
        ),
    ]:
        payload = yaml.safe_load((root / relative).read_text())
        errors.extend(
            f"{relative}: {error.json_path}: {error.message}"
            for error in Draft202012Validator(loader()).iter_errors(payload)
        )
    for manifest in sorted((root / "skills").glob("*/SKILL.md")):
        frontmatter = yaml.safe_load(manifest.read_text().split("---", 2)[1])
        metadata = frontmatter.get("metadata", {})
        for name in ["agent-playbook", "multi-agent-playbook"]:
            source_version = re.search(
                r"\*\*Version:\*\* (\S+)", (root / name / "README.md").read_text()
            )[1]
            if metadata.get(name) != source_version:
                errors.append(
                    f"{manifest.relative_to(root)}: metadata.{name} must track source version {source_version}"
                )
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = check_repository(root)
    if errors:
        print("\n".join(errors))
        return 1
    print("Markdown, local links, source versions, and contract examples passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
