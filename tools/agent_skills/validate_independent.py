#!/usr/bin/env python3
"""Independently validate static development-skill formats without executing skills."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

EXPECTED_SKILLS = (
    "plan-agent-use",
    "specify-agent-contract",
    "design-trust-boundaries",
    "build-agent-evidence",
    "review-agent-readiness",
    "operate-agent-lifecycle",
    "author-and-admit-agent-skills",
    "draft-agent-implementation",
)
PACKAGE_FILES = frozenset(
    {
        "SKILL.md",
        "references/owner-map.md",
        "references/packet-contract.md",
        "references/examples.md",
        "assets/packet-template.json",
        "assets/evaluation-cases.json",
    }
)
DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate object keys rather than silently keeping the last value."""
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key {key!r}")
        value[key] = item
    return value


def reject_constant(value: str) -> None:
    """Reject Python's non-standard JSON constants such as NaN and Infinity."""
    raise ValueError(f"non-standard JSON constant {value!r}")


def load_json(path: Path) -> Any:
    """Load strict JSON from a regular UTF-8 file; never execute its contents."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc


def resource_inventory(package: Path) -> tuple[set[str], list[str]]:
    """Return package files and filesystem-shape errors without following links."""
    paths: set[str] = set()
    errors: list[str] = []
    if not package.is_dir():
        return paths, [f"missing skill directory: {package}"]
    for entry in sorted(package.rglob("*"), key=lambda item: item.as_posix()):
        relative = entry.relative_to(package).as_posix()
        if entry.is_symlink():
            errors.append(f"symlink is not allowed: {relative}")
        elif entry.is_file():
            paths.add(relative)
        elif not entry.is_dir():
            errors.append(f"unsupported filesystem entry: {relative}")
    return paths, errors


def validate_schema(path: Path, label: str) -> tuple[Draft202012Validator | None, list[str]]:
    """Load one closed Draft 2020-12 schema with the library's strict JSON rules."""
    try:
        schema = load_json(path)
    except ValueError as exc:
        return None, [str(exc)]
    if not isinstance(schema, dict):
        return None, [f"{label} schema must be a JSON object"]
    errors: list[str] = []
    if schema.get("$schema") != DRAFT_2020_12:
        errors.append(f"{label} schema must declare {DRAFT_2020_12}")
    if schema.get("additionalProperties") is not False:
        errors.append(f"{label} schema root must set additionalProperties to false")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        errors.append(f"invalid {label} schema: {exc.message}")
    if errors:
        return None, errors
    return Draft202012Validator(schema), []


def format_schema_errors(validator: Draft202012Validator, value: Any) -> list[str]:
    """Render every violation deterministically so CI reports the complete fixture result."""
    errors = sorted(
        validator.iter_errors(value),
        key=lambda error: (tuple(str(item) for item in error.absolute_path), error.message),
    )
    rendered: list[str] = []
    for error in errors:
        location = "/".join(str(item) for item in error.absolute_path) or "<root>"
        rendered.append(f"{location}: {error.message}")
    return rendered


def run_reference_validator(cli: Path, package: Path, root: Path) -> list[str]:
    """Run the pinned reference CLI on one directory; it receives no skill code to run."""
    try:
        completed = subprocess.run(
            [str(cli), "validate", str(package)],
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [f"could not run reference validator: {exc}"]
    if completed.returncode == 0:
        return []
    detail = (completed.stderr or completed.stdout).strip().replace("\n", " ")
    return [f"reference validator exited {completed.returncode}: {detail or 'no diagnostic'}"]


def add_inventory_errors(actual: set[str], errors: list[str]) -> None:
    """Require the proposed packages to retain their exact six-resource closure."""
    missing = sorted(PACKAGE_FILES - actual)
    unexpected = sorted(actual - PACKAGE_FILES)
    if missing:
        errors.append(f"missing package resources: {', '.join(missing)}")
    if unexpected:
        errors.append(f"unexpected package resources: {', '.join(unexpected)}")


def validate(root: Path, skills_ref: Path) -> dict[str, Any]:
    """Validate every expected skill and return a JSON-serializable complete report."""
    library = root / "development-skills"
    report: dict[str, Any] = {
        "ok": False,
        "root": str(root),
        "skills": [],
        "library_errors": [],
    }
    if not library.is_dir():
        report["library_errors"].append(f"missing proposed library: {library}")

    library_directories = {entry.name for entry in library.iterdir() if entry.is_dir()} if library.is_dir() else set()
    discovered = (
        {entry.name for entry in library.iterdir() if entry.is_dir() and (entry / "SKILL.md").is_file()}
        if library.is_dir()
        else set()
    )
    missing_skills = sorted(set(EXPECTED_SKILLS) - discovered)
    unexpected_skills = sorted(discovered - set(EXPECTED_SKILLS))
    if missing_skills:
        report["library_errors"].append(f"missing skill directories: {', '.join(missing_skills)}")
    if unexpected_skills:
        report["library_errors"].append(f"unexpected skill directories: {', '.join(unexpected_skills)}")
    unexpected_directories = sorted(library_directories - set(EXPECTED_SKILLS) - {"contracts", "evidence"})
    if unexpected_directories:
        report["library_errors"].append(
            f"unexpected top-level library directories: {', '.join(unexpected_directories)}"
        )

    packet_validator, packet_schema_errors = validate_schema(
        library / "contracts" / "packet.schema.json", "packet"
    )
    cases_validator, cases_schema_errors = validate_schema(
        library / "contracts" / "evaluation-cases.schema.json", "evaluation cases"
    )
    if packet_schema_errors:
        report["library_errors"].extend(packet_schema_errors)
    if cases_schema_errors:
        report["library_errors"].extend(cases_schema_errors)
    if not skills_ref.is_file():
        report["library_errors"].append(f"reference validator is not a file: {skills_ref}")

    for name in EXPECTED_SKILLS:
        package = library / name
        inventory, inventory_errors = resource_inventory(package)
        add_inventory_errors(inventory, inventory_errors)
        packet_errors: list[str] = []
        cases_errors: list[str] = []

        packet_path = package / "assets" / "packet-template.json"
        if packet_validator is None:
            packet_errors.append("packet schema is unavailable")
        elif not packet_path.is_file():
            packet_errors.append(f"missing packet fixture: {packet_path}")
        else:
            try:
                packet = load_json(packet_path)
            except ValueError as exc:
                packet_errors.append(str(exc))
            else:
                packet_errors.extend(format_schema_errors(packet_validator, packet))
                if isinstance(packet, dict) and packet.get("skill") != name:
                    packet_errors.append(f"skill must equal package directory name {name!r}")

        cases_path = package / "assets" / "evaluation-cases.json"
        if cases_validator is None:
            cases_errors.append("evaluation cases schema is unavailable")
        elif not cases_path.is_file():
            cases_errors.append(f"missing evaluation cases fixture: {cases_path}")
        else:
            try:
                cases = load_json(cases_path)
            except ValueError as exc:
                cases_errors.append(str(exc))
            else:
                cases_errors.extend(format_schema_errors(cases_validator, cases))
                if isinstance(cases, dict) and cases.get("skill") != name:
                    cases_errors.append(f"skill must equal package directory name {name!r}")

        reference_errors = (
            run_reference_validator(skills_ref, package, root) if skills_ref.is_file() else ["reference validator is unavailable"]
        )
        report["skills"].append(
            {
                "name": name,
                "inventory": {"ok": not inventory_errors, "errors": inventory_errors},
                "packet": {"ok": not packet_errors, "errors": packet_errors},
                "cases": {"ok": not cases_errors, "errors": cases_errors},
                "reference": {"ok": not reference_errors, "errors": reference_errors},
            }
        )

    report["ok"] = not report["library_errors"] and all(
        all(check["ok"] for check in skill.values() if isinstance(check, dict))
        for skill in report["skills"]
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument(
        "--skills-ref",
        type=Path,
        required=True,
        help="path to the pinned skills-ref CLI installed in the isolated development virtual environment",
    )
    arguments = parser.parse_args()
    report = validate(arguments.root.resolve(), arguments.skills_ref.resolve())
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
