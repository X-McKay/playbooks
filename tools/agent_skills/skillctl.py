#!/usr/bin/env python3
"""Offline validation and evidence helpers for the playbook agent-skill library.

This tool deliberately validates static artifacts only.  It neither executes package
content nor grants authority, and a successful result is not an isolation, approval,
or behavioral-conformance claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
import unicodedata
import zipfile
from typing import Any

BASELINE = "151fca01fbc609c5550c563c902946db540c2f4c"
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
REQUIRED_FILES = {
    "SKILL.md",
    "references/owner-map.md",
    "references/packet-contract.md",
    "references/examples.md",
    "assets/packet-template.json",
    "assets/evaluation-cases.json",
}
CONTRACT_FILES = frozenset({"packet.schema.json", "evaluation-cases.schema.json"})
NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
SHA_RE = re.compile(r"[0-9a-f]{64}\Z")
COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
DRIVE_RE = re.compile(r"[A-Za-z]:")
REQ_RE = re.compile(r"\b([A-Z][A-Z0-9_]*-[0-9]{2})\b")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


class SkillctlError(Exception):
    """An expected, user-correctable validation failure."""


def fail(message: str) -> None:
    raise SkillctlError(message)


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def require_no_symlink_components(path: Path, *, require_exists: bool = True) -> Path:
    """Return an absolute lexical path after rejecting symlinks in every component."""
    absolute = Path(os.path.abspath(os.fspath(path)))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current = current / part
        try:
            mode = os.lstat(current).st_mode
        except FileNotFoundError:
            if require_exists:
                fail(f"path does not exist: {absolute}")
            break
        if os.path.islink(current):
            fail(f"symlinks are not allowed: {current}")
        # lstat succeeded; an inaccessible path is handled by its later operation.
        _ = mode
    return absolute


def require_directory(path: Path) -> Path:
    path = require_no_symlink_components(path)
    if not path.is_dir():
        fail(f"expected directory: {path}")
    return path


def require_regular_file(path: Path) -> Path:
    path = require_no_symlink_components(path)
    if not path.is_file():
        fail(f"expected regular file: {path}")
    if path.stat(follow_symlinks=False).st_nlink != 1:
        fail(f"hardlinked files are not allowed: {path}")
    return path


def normalized_relative(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        fail(f"{label} must be a non-empty relative path string")
    if "\\" in value or DRIVE_RE.match(value) or any(unicodedata.category(char).startswith("C") for char in value):
        fail(f"{label} must use a normalized POSIX relative path")
    candidate = PurePosixPath(value)
    if candidate.is_absolute() or any(part in ("", ".", "..") for part in candidate.parts):
        fail(f"{label} escapes its root: {value!r}")
    normalized = candidate.as_posix()
    if normalized != value:
        fail(f"{label} is not normalized: {value!r}")
    return normalized


def confined_file(root: Path, relative: str, label: str = "path") -> Path:
    root = require_directory(root)
    relative = normalized_relative(relative, label)
    candidate = root / relative
    require_no_symlink_components(candidate)
    resolved_root = root.resolve(strict=True)
    resolved_candidate = candidate.resolve(strict=True)
    if not is_within(resolved_candidate, resolved_root):
        fail(f"{label} escapes its root: {relative!r}")
    if not resolved_candidate.is_file():
        fail(f"{label} is not a regular file: {relative!r}")
    return require_regular_file(resolved_candidate)


def walk_regular_files(root: Path, *, excluded_components: frozenset[str] = frozenset(), excluded_paths: frozenset[Path] = frozenset()) -> list[Path]:
    """Enumerate included files strictly, pruning declared exclusions first."""
    root = require_directory(root)
    files: list[Path] = []
    for directory, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        current = Path(directory)
        dirnames[:] = [name for name in dirnames if name not in excluded_components and current / name not in excluded_paths]
        for name in list(dirnames):
            entry = current / name
            if entry.is_symlink():
                fail(f"symlinks are not allowed: {entry}")
            if not entry.is_dir():
                fail(f"unsupported directory entry: {entry}")
        for name in filenames:
            entry = current / name
            if name in excluded_components or entry in excluded_paths:
                continue
            if entry.is_symlink():
                fail(f"symlinks are not allowed: {entry}")
            metadata = entry.stat(follow_symlinks=False)
            if not stat.S_ISREG(metadata.st_mode):
                fail(f"unsupported non-regular file: {entry}")
            # Rejecting link-counts catches ordinary hardlinks.  It cannot prove
            # a filesystem has no aliasing or concurrent writer, so callers must
            # still treat this as a local development aid rather than tamper proof.
            if metadata.st_nlink != 1:
                fail(f"hardlinked files are not allowed: {entry}")
            files.append(entry)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def scalar(value: str, label: str) -> str:
    """Parse the intentionally tiny, safe YAML scalar subset used by SKILL.md."""
    if "\t" in value or "\x00" in value:
        fail(f"malformed {label}")
    value = value.strip()
    if not value:
        fail(f"missing scalar value for {label}")
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            fail(f"malformed quoted {label}: {exc.msg}")
        if not isinstance(parsed, str):
            fail(f"{label} must be a string")
        return parsed
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            fail(f"malformed quoted {label}")
        return value[1:-1].replace("''", "'")
    if value.startswith(("!", "&", "*", "|", ">", "[", "{")):
        fail(f"unsafe or unsupported YAML value for {label}")
    if value in ("null", "Null", "NULL", "true", "false", "True", "False", "~"):
        fail(f"{label} must be quoted when it could be a non-string YAML value")
    return value


def parse_frontmatter(skill_file: Path) -> dict[str, Any]:
    try:
        text = skill_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fail(f"SKILL.md is not UTF-8: {skill_file}")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        fail(f"SKILL.md must start with YAML frontmatter: {skill_file}")
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail(f"SKILL.md frontmatter is not closed: {skill_file}")
    body = lines[1:end]
    result: dict[str, Any] = {}
    metadata: dict[str, str] = {}
    top_re = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(.*)$")
    meta_re = re.compile(r"^  ([A-Za-z][A-Za-z0-9_-]*):(.*)$")
    mode = "top"
    for line in body:
        if not line.strip():
            continue
        if "\t" in line:
            fail(f"tabs are not allowed in frontmatter: {skill_file}")
        if line.startswith("  "):
            if mode != "metadata":
                fail(f"unexpected nested frontmatter field: {line!r}")
            match = meta_re.fullmatch(line)
            if not match:
                fail(f"malformed metadata field: {line!r}")
            key, raw = match.groups()
            if key in metadata:
                fail(f"duplicate metadata field {key!r}")
            metadata[key] = scalar(raw, f"metadata.{key}")
            continue
        match = top_re.fullmatch(line)
        if not match:
            fail(f"malformed frontmatter field: {line!r}")
        key, raw = match.groups()
        if key in result:
            fail(f"duplicate frontmatter field {key!r}")
        if key not in {"name", "description", "license", "compatibility", "allowed-tools", "metadata"}:
            fail(f"unknown frontmatter field {key!r}")
        if key == "metadata":
            if raw.strip():
                fail("metadata must be a mapping of string values")
            result[key] = metadata
            mode = "metadata"
        else:
            result[key] = scalar(raw, key)
            mode = "top"
    if not {"name", "description", "metadata"}.issubset(result):
        fail("frontmatter must contain name, description, and metadata")
    required_metadata = {"version": "0.1.0", "playbook_version": "0.5.0-draft.2", "source_commit": BASELINE}
    if metadata != required_metadata:
        fail("metadata must contain only the required version, playbook_version, and source_commit strings")
    return result


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def reject_nonstandard_json_constant(value: str) -> None:
    fail(f"non-standard JSON numeric constant: {value}")


def parse_json_text(text: str, label: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=reject_duplicate_json_keys, parse_constant=reject_nonstandard_json_constant)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {label}: {exc.msg}")


def parse_json(path: Path, label: str) -> Any:
    try:
        return parse_json_text(path.read_text(encoding="utf-8"), f"{label} ({path})")
    except UnicodeDecodeError:
        fail(f"{label} is not UTF-8: {path}")


def exact_object(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{label} must be an object")
    actual = set(value)
    if actual != fields:
        missing = sorted(fields - actual)
        extra = sorted(actual - fields)
        fail(f"{label} has wrong fields (missing={missing}, extra={extra})")
    return value


def string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        fail(f"{label} must be a list of strings")
    return value


def enum_string(value: Any, values: set[str], label: str) -> str:
    """Validate enums without allowing list/dict inputs to raise TypeError."""
    if not isinstance(value, str) or value not in values:
        fail(f"{label} is invalid")
    return value


def validate_evaluation_cases(data: Any, package_name: str) -> None:
    root = exact_object(data, {"skill", "cases"}, "evaluation cases")
    if root["skill"] != package_name:
        fail("evaluation cases skill does not match package directory")
    cases = root["cases"]
    if not isinstance(cases, list) or len(cases) < 6:
        fail("evaluation cases must contain at least six cases")
    identifiers: set[str] = set()
    selections: set[str] = set()
    splits: set[str] = set()
    for index, case in enumerate(cases):
        item = exact_object(case, {"id", "split", "prompt", "expected_selection", "required_outputs", "forbidden_behavior", "assertions"}, f"case {index}")
        identifier = item["id"]
        if not isinstance(identifier, str) or not identifier or identifier in identifiers:
            fail(f"case {index} id must be a unique non-empty string")
        identifiers.add(identifier)
        enum_string(item["split"], {"development", "holdout"}, f"case {identifier} split")
        splits.add(item["split"])
        enum_string(item["expected_selection"], {"select", "do_not_select", "clarify"}, f"case {identifier} expected_selection")
        selections.add(item["expected_selection"])
        if not isinstance(item["prompt"], str) or not item["prompt"].strip():
            fail(f"case {identifier} prompt must be non-empty")
        for field in ("required_outputs", "forbidden_behavior", "assertions"):
            values = string_list(item[field], f"case {identifier} {field}")
            if any(not value.strip() for value in values):
                fail(f"case {identifier} {field} cannot contain blank strings")
        if not item["assertions"]:
            fail(f"case {identifier} assertions must contain checkable statements")
    if selections != {"select", "do_not_select", "clarify"}:
        fail("evaluation cases must include select, do_not_select, and clarify examples")
    if splits != {"development", "holdout"}:
        fail("evaluation cases must include development and holdout examples")


def validate_packet_data(data: Any, workspace: Path | None, *, template: bool = False) -> dict[str, Any]:
    fields = {"schema_version", "skill", "run_id", "status", "source_commit", "inputs", "outputs", "assumptions", "blockers", "applicability", "evidence", "decision"}
    packet = exact_object(data, fields, "packet")
    if packet["schema_version"] != "1.0":
        fail("packet schema_version must be '1.0'")
    for field in ("skill", "run_id"):
        if not isinstance(packet[field], str) or not packet[field]:
            fail(f"packet {field} must be a non-empty string")
    if not NAME_RE.fullmatch(packet["skill"]) or len(packet["skill"]) > 64:
        fail("packet skill must be a safe name of at most 64 characters")
    enum_string(packet["status"], {"draft", "needs_information", "blocked", "candidate_evidenced"}, "packet status")
    if not isinstance(packet["source_commit"], str) or not COMMIT_RE.fullmatch(packet["source_commit"]):
        fail("packet source_commit must be a lowercase 40-character commit hash")
    if not isinstance(packet["inputs"], dict) or not isinstance(packet["outputs"], dict):
        fail("packet inputs and outputs must be objects")
    if template:
        if not packet["outputs"]:
            fail("packet template outputs must identify substantive draft output fields")
    for field in ("assumptions", "blockers"):
        values = string_list(packet[field], f"packet {field}")
        if any(not item.strip() for item in values):
            fail(f"packet {field} cannot contain blank strings")
    decision = exact_object(packet["decision"], {"recommendation", "authorized"}, "packet decision")
    enum_string(decision["recommendation"], {"not_assessed", "go", "conditional_go", "no_go"}, "packet decision recommendation")
    if decision["authorized"] is not False:
        fail("packet decision authorized must always be false; authorization is external")

    evidence_by_id: dict[str, dict[str, Any]] = {}
    if not isinstance(packet["evidence"], list):
        fail("packet evidence must be a list")
    for index, record in enumerate(packet["evidence"]):
        evidence = exact_object(record, {"id", "kind", "status", "artifact", "sha256"}, f"evidence {index}")
        identifier = evidence["id"]
        if not isinstance(identifier, str) or not identifier or identifier in evidence_by_id:
            fail("evidence ids must be unique non-empty strings")
        enum_string(evidence["kind"], {"planned", "observed"}, f"evidence {identifier} kind")
        enum_string(evidence["status"], {"pass", "fail", "invalid", "inconclusive", "not_run"}, f"evidence {identifier} status")
        if not isinstance(evidence["artifact"], str) or not isinstance(evidence["sha256"], str):
            fail(f"evidence {identifier} artifact and sha256 must be strings")
        if evidence["kind"] == "planned":
            if evidence["status"] != "not_run":
                fail(f"planned evidence {identifier} status must be not_run")
            if evidence["artifact"]:
                normalized_relative(evidence["artifact"], f"planned evidence {identifier} artifact")
            if evidence["sha256"] and not SHA_RE.fullmatch(evidence["sha256"]):
                fail(f"planned evidence {identifier} sha256 must be empty or lowercase 64-hex")
        else:
            if template:
                fail("packet templates cannot contain observed evidence")
            if workspace is None:
                fail("observed evidence requires a workspace")
            artifact = normalized_relative(evidence["artifact"], f"evidence {identifier} artifact")
            if not SHA_RE.fullmatch(evidence["sha256"]):
                fail(f"observed evidence {identifier} sha256 must be lowercase 64-hex")
            found = confined_file(workspace, artifact, f"evidence {identifier} artifact")
            if sha256_file(found) != evidence["sha256"]:
                fail(f"observed evidence {identifier} hash does not match artifact")
        evidence_by_id[identifier] = evidence

    if not isinstance(packet["applicability"], list):
        fail("packet applicability must be a list")
    app_statuses: list[str] = []
    requirement_ids: set[str] = set()
    for index, record in enumerate(packet["applicability"]):
        app = exact_object(record, {"requirement_id", "status", "rationale", "evidence_ids"}, f"applicability {index}")
        if not isinstance(app["requirement_id"], str) or not app["requirement_id"]:
            fail(f"applicability {index} requirement_id must be non-empty")
        if app["requirement_id"] in requirement_ids:
            fail(f"duplicate applicability requirement_id: {app['requirement_id']}")
        requirement_ids.add(app["requirement_id"])
        enum_string(app["status"], {"met", "not_applicable", "unmet", "exception_proposed"}, f"applicability {index} status")
        if not isinstance(app["rationale"], str) or not app["rationale"].strip():
            fail(f"applicability {index} rationale must be non-empty")
        evidence_ids = string_list(app["evidence_ids"], f"applicability {index} evidence_ids")
        if len(set(evidence_ids)) != len(evidence_ids) or any(item not in evidence_by_id for item in evidence_ids):
            fail(f"applicability {index} references missing or duplicate evidence ids")
        if app["status"] == "met":
            if not evidence_ids:
                fail(f"met applicability {index} requires observed passing evidence")
            linked = [evidence_by_id[item] for item in evidence_ids]
            if not all(item["kind"] == "observed" and item["status"] == "pass" for item in linked):
                fail(f"met applicability {index} requires observed passing evidence")
        app_statuses.append(app["status"])

    recommendation = decision["recommendation"]
    if packet["status"] == "candidate_evidenced" and (not packet["applicability"] or not packet["evidence"]):
        fail("candidate_evidenced requires non-empty applicability and evidence")
    if recommendation in {"go", "conditional_go"}:
        if packet["status"] != "candidate_evidenced":
            fail("go or conditional_go requires candidate_evidenced status")
        if not packet["applicability"] or not packet["evidence"]:
            fail("go or conditional_go requires non-empty applicability and evidence")
        if packet["blockers"]:
            fail("go or conditional_go is blocked while packet blockers are present")
        if any(status in {"unmet", "exception_proposed"} for status in app_statuses):
            fail("go or conditional_go is blocked by unmet applicability")
        if not any(status == "met" for status in app_statuses):
            fail("go or conditional_go requires at least one met applicability requirement")
        for evidence in evidence_by_id.values():
            if evidence["kind"] != "observed" or evidence["status"] != "pass":
                fail("go or conditional_go packet may contain only current observed pass evidence; retain prior failed attempts in a separate ledger")
    if template and packet["status"] != "draft":
        fail("packet template status must be draft")
    if template and recommendation != "not_assessed":
        fail("packet template recommendation must be not_assessed")
    return packet


def local_links(text: str) -> list[str]:
    paths: list[str] = []
    for raw in MARKDOWN_LINK_RE.findall(text):
        target = raw.strip().split(maxsplit=1)[0]
        if target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        if target:
            paths.append(target)
    return paths


def validate_owner_map(path: Path, requirement_ids: set[str]) -> None:
    text = path.read_text(encoding="utf-8")
    identifiers = set(REQ_RE.findall(text))
    if not identifiers:
        fail(f"owner map must identify canonical requirement IDs: {path}")
    unknown = sorted(identifiers - requirement_ids)
    if unknown:
        fail(f"owner map contains unknown requirement IDs: {', '.join(unknown)}")
    links = re.findall(r"https://github\.com/X-McKay/playbooks/blob/([^/]+)/[^\s)>]+", text)
    if not links:
        fail(f"owner map must include an immutable canonical GitHub link: {path}")
    if any(not COMMIT_RE.fullmatch(commit) for commit in links):
        fail(f"owner map GitHub links must use immutable 40-character commits: {path}")


def requirement_ids_from(root: Path) -> set[str]:
    index = require_regular_file(root / "requirement-index.md")
    return set(REQ_RE.findall(index.read_text(encoding="utf-8")))


def validate_profile_data(data: Any) -> dict[str, Any]:
    data = exact_object(data, {"id", "schema_version", "status", "language", "minimum_version", "required_artifacts", "checks", "forbidden_actions"}, "profile")
    exact = {"id": "python-local", "schema_version": "1.0", "status": "proposed", "language": "python", "minimum_version": "3.11"}
    for key, wanted in exact.items():
        if data[key] != wanted:
            fail(f"profile {key} must be {wanted!r}")
    artifacts = string_list(data["required_artifacts"], "profile required_artifacts")
    if not artifacts:
        fail("profile required_artifacts cannot be empty")
    for artifact in artifacts:
        normalized_relative(artifact, "profile required_artifacts item")
    if not isinstance(data["checks"], list) or not data["checks"]:
        fail("profile checks must be a non-empty list")
    check_ids: set[str] = set()
    for index, check in enumerate(data["checks"]):
        item = exact_object(check, {"id", "argv", "timeout_seconds"}, f"profile check {index}")
        if not isinstance(item["id"], str) or not item["id"] or item["id"] in check_ids:
            fail("profile check ids must be unique non-empty strings")
        check_ids.add(item["id"])
        argv = string_list(item["argv"], f"profile check {item['id']} argv")
        if not argv or any(not value or "\x00" in value for value in argv):
            fail(f"profile check {item['id']} argv contains an invalid argument")
        if any(value.startswith("/") or ".." in PurePosixPath(value).parts for value in argv if "/" in value):
            fail(f"profile check {item['id']} argv contains an unsafe path")
        if not isinstance(item["timeout_seconds"], int) or isinstance(item["timeout_seconds"], bool) or item["timeout_seconds"] <= 0:
            fail(f"profile check {item['id']} timeout_seconds must be a positive integer")
    forbidden = string_list(data["forbidden_actions"], "profile forbidden_actions")
    if not forbidden or any(not item.strip() for item in forbidden):
        fail("profile forbidden_actions must contain non-empty strings")
    return data


def validate_profile(root: Path, profile: str) -> str:
    if profile != "python-local":
        fail(f"unsupported implementation profile: {profile}")
    profile_file = require_regular_file(root / "implementation-profiles/python/profile.json")
    require_regular_file(root / "implementation-profiles/python/README.md")
    validate_profile_data(parse_json(profile_file, "profile"))
    digest = hashlib.sha256()
    for path in (root / "implementation-profiles/python/README.md", profile_file):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(path).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


CATALOG_FIELDS = {"schema_version", "library_version", "playbook_version", "source_commit", "status", "description", "skills"}


def validate_catalog_data(data: Any, names: set[str]) -> dict[str, Any]:
    data = exact_object(data, CATALOG_FIELDS, "catalog")
    if data["schema_version"] != "1.0":
        fail("catalog schema_version must be '1.0'")
    if data["playbook_version"] != "0.5.0-draft.2":
        fail("catalog playbook_version does not match the canonical baseline")
    if data["source_commit"] != BASELINE:
        fail("catalog source_commit does not match the canonical baseline")
    if not isinstance(data["library_version"], str) or not data["library_version"]:
        fail("catalog library_version must be a non-empty string")
    enum_string(data["status"], {"proposed"}, "catalog status")
    if not isinstance(data["description"], str) or not data["description"].strip():
        fail("catalog description must be a non-empty string")
    entries = data["skills"]
    if not isinstance(entries, list) or len(entries) != len(EXPECTED_SKILLS):
        fail("catalog skills must contain exactly the eight supported packages")
    catalog_names: set[str] = set()
    catalog_ids: set[str] = set()
    graph: dict[str, list[str]] = {}
    for index, entry in enumerate(entries):
        item = exact_object(entry, {"id", "name", "path", "dependencies"}, f"catalog skill {index}")
        identifier = item["id"]
        name = item["name"]
        if not isinstance(identifier, str) or not identifier or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", identifier):
            fail(f"catalog id must be a qualified safe non-empty string: skill {index}")
        if identifier in catalog_ids:
            fail(f"duplicate catalog qualified id: {identifier}")
        catalog_ids.add(identifier)
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            fail(f"catalog name must be a safe skill name: skill {index}")
        if name in catalog_names:
            fail(f"duplicate catalog skill name: {name}")
        catalog_names.add(name)
        if item["path"] != f"development-skills/{name}":
            fail(f"catalog path does not match skill name: {name}")
        dependencies = string_list(item["dependencies"], f"catalog dependencies for {name}")
        graph[name] = dependencies
    if catalog_names != names:
        fail("catalog skill names do not match the package inventory")
    for name, dependencies in graph.items():
        if len(set(dependencies)) != len(dependencies) or name in dependencies or any(item not in catalog_names for item in dependencies):
            fail(f"catalog dependencies are invalid for: {name}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visiting:
            fail(f"catalog dependencies contain a cycle at: {name}")
        if name in visited:
            return
        visiting.add(name)
        for dependency in graph.get(name, []):
            visit(dependency)
        visiting.remove(name)
        visited.add(name)

    for name in sorted(graph):
        visit(name)
    return data


def validate_catalog(root: Path, names: set[str]) -> dict[str, Any]:
    catalog = require_regular_file(root / "development-skills/catalog.json")
    return validate_catalog_data(parse_json(catalog, "catalog"), names)


def schema_property(schema: Any, name: str, label: str) -> dict[str, Any]:
    if not isinstance(schema, dict) or not isinstance(schema.get("properties"), dict) or not isinstance(schema["properties"].get(name), dict):
        fail(f"{label} is missing properties.{name}")
    return schema["properties"][name]


def validate_contract_schema_data(packet: Any, cases: Any) -> None:
    """Check the two shipped contracts cover this tool's strict constraints.

    This is deliberately not a complete JSON-Schema implementation; it catches
    obvious divergence in the independently shipped schema resources.
    """
    for schema, label in ((packet, "packet schema"), (cases, "evaluation-cases schema")):
        if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema" or schema.get("type") != "object" or schema.get("additionalProperties") is not False:
            fail(f"{label} must be a closed draft 2020-12 object schema")
    if set(packet.get("required", [])) != {"schema_version", "skill", "run_id", "status", "source_commit", "inputs", "outputs", "assumptions", "blockers", "applicability", "evidence", "decision"}:
        fail("packet schema required fields diverge from packet validation")
    skill = schema_property(packet, "skill", "packet schema")
    if skill.get("pattern") != "^[a-z0-9]+(?:-[a-z0-9]+)*$" or skill.get("maxLength") != 64:
        fail("packet schema skill constraint diverges from packet validation")
    if schema_property(packet, "status", "packet schema").get("enum") != ["draft", "needs_information", "blocked", "candidate_evidenced"]:
        fail("packet schema status enum diverges from packet validation")
    decision = schema_property(packet, "decision", "packet schema")
    if schema_property(decision, "authorized", "packet decision schema").get("const") is not False:
        fail("packet schema must keep authorization external")
    evidence = schema_property(packet, "evidence", "packet schema")
    evidence_items = evidence.get("items") if isinstance(evidence, dict) else None
    planned_rule = False
    if isinstance(evidence_items, dict) and isinstance(evidence_items.get("allOf"), list):
        for rule in evidence_items["allOf"]:
            if isinstance(rule, dict) and isinstance(rule.get("if"), dict) and schema_property(rule["if"], "kind", "packet planned-evidence if").get("const") == "planned" and isinstance(rule.get("then"), dict) and schema_property(rule["then"], "status", "packet planned-evidence then").get("const") == "not_run":
                planned_rule = True
    if not planned_rule:
        fail("packet schema must require planned evidence to be not_run")
    if set(cases.get("required", [])) != {"skill", "cases"}:
        fail("evaluation-cases schema required fields diverge from validation")
    case_items = schema_property(cases, "cases", "evaluation-cases schema").get("items")
    if not isinstance(case_items, dict) or case_items.get("additionalProperties") is not False or schema_property(case_items, "split", "evaluation case schema").get("enum") != ["development", "holdout"] or schema_property(case_items, "expected_selection", "evaluation case schema").get("enum") != ["select", "do_not_select", "clarify"]:
        fail("evaluation-cases schema enums diverge from validation")


def validate_contract_schemas(root: Path) -> None:
    contracts = require_directory(root / "development-skills/contracts")
    sources = {source.relative_to(contracts).as_posix(): source for source in walk_regular_files(contracts)}
    if set(sources) != CONTRACT_FILES:
        fail(f"contract resources must exactly be {sorted(CONTRACT_FILES)} (missing={sorted(CONTRACT_FILES - set(sources))}, extra={sorted(set(sources) - CONTRACT_FILES)})")
    packet = parse_json(sources["packet.schema.json"], "packet schema")
    cases = parse_json(sources["evaluation-cases.schema.json"], "evaluation-cases schema")
    validate_contract_schema_data(packet, cases)


def supported_package_resource(relative: str) -> bool:
    return relative == "SKILL.md" or (relative.startswith("references/") and relative.endswith(".md")) or (relative.startswith("assets/") and relative.endswith(".json"))


def validate_package(root: Path, package: Path, requirement_ids: set[str]) -> dict[str, Any]:
    package = require_directory(package)
    name = package.name
    if name not in EXPECTED_SKILLS:
        fail(f"unsupported package directory: {name}")
    files = walk_regular_files(package)
    rel_paths = {item.relative_to(package).as_posix() for item in files}
    missing = sorted(REQUIRED_FILES - rel_paths)
    if missing:
        fail(f"package {name} is missing required files: {', '.join(missing)}")
    for relative in rel_paths:
        if not supported_package_resource(relative):
            fail(f"unsupported package file: {name}/{relative}")
    frontmatter = parse_frontmatter(package / "SKILL.md")
    if frontmatter["name"] != name or not NAME_RE.fullmatch(name):
        fail(f"package name must match safe directory name: {name}")
    description = frontmatter["description"]
    if not description or len(description) > 1024:
        fail(f"package {name} description must be 1 to 1024 characters")
    for markdown in (item for item in files if item.suffix == ".md"):
        text = markdown.read_text(encoding="utf-8")
        markdown_parent = markdown.parent.relative_to(package).as_posix()
        for link in local_links(text):
            target = link if markdown_parent == "." else f"{markdown_parent}/{link}"
            confined_file(package, target, f"local reference in {markdown.relative_to(package)}")
    validate_owner_map(package / "references/owner-map.md", requirement_ids)
    template = parse_json(package / "assets/packet-template.json", "packet template")
    packet = validate_packet_data(template, None, template=True)
    if packet["skill"] != name:
        fail("packet template skill does not match package directory")
    if packet["source_commit"] != BASELINE:
        fail("packet template source_commit does not match the canonical baseline")
    validate_evaluation_cases(parse_json(package / "assets/evaluation-cases.json", "evaluation cases"), name)

    inventory_files = []
    digest = hashlib.sha256()
    for item in files:
        relative = item.relative_to(package).as_posix()
        file_hash = sha256_file(item)
        size = item.stat().st_size
        inventory_files.append({"path": relative, "sha256": file_hash, "bytes": size})
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        digest.update(b"\n")
    skill_bytes = (package / "SKILL.md").stat().st_size
    skill_words = len((package / "SKILL.md").read_text(encoding="utf-8").split())
    return {
        "name": name,
        "path": f"development-skills/{name}",
        "digest": digest.hexdigest(),
        "files": inventory_files,
        "skill_markdown": {"bytes": skill_bytes, "words": skill_words, "token_estimate": (skill_words * 4 + 2) // 3, "token_estimate_label": "heuristic"},
    }


def inventory(root_arg: str) -> dict[str, Any]:
    root = require_directory(Path(root_arg))
    base = require_directory(root / "development-skills")
    requirement_ids = requirement_ids_from(root)
    discovered = {entry.name: entry for entry in base.iterdir() if entry.is_dir() and (entry / "SKILL.md").exists()}
    if set(discovered) != set(EXPECTED_SKILLS):
        fail(f"skill package set must exactly match the eight supported packages (missing={sorted(set(EXPECTED_SKILLS) - set(discovered))}, extra={sorted(set(discovered) - set(EXPECTED_SKILLS))})")
    records = [validate_package(root, discovered[name], requirement_ids) for name in EXPECTED_SKILLS]
    validate_catalog(root, set(discovered))
    validate_contract_schemas(root)
    whole = hashlib.sha256()
    for record in records:
        whole.update(record["name"].encode("utf-8"))
        whole.update(b"\0")
        whole.update(record["digest"].encode("ascii"))
        whole.update(b"\n")
    return {"schema_version": "1.0", "tool": "skillctl", "packages": records, "library_digest": whole.hexdigest(), "limitations": "Static package checks only; this result is not runtime isolation, approval, or behavioral-conformance evidence."}


def atomic_bytes(path: Path, content: bytes, *, overwrite: bool) -> None:
    parent = require_directory(path.parent)
    target = Path(os.path.abspath(os.fspath(path)))
    require_no_symlink_components(target, require_exists=False)
    if target.exists():
        require_regular_file(target)
        if not overwrite:
            fail(f"refusing to overwrite existing file: {target}")
    fd, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if overwrite:
            os.replace(temporary, target)
        else:
            try:
                os.link(temporary, target)
            except FileExistsError:
                fail(f"refusing to overwrite existing file: {target}")
            temporary.unlink()
        directory_fd = os.open(parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_json(path: Path, value: Any, *, overwrite: bool) -> None:
    atomic_bytes(path, canonical_json(value), overwrite=overwrite)


MANIFEST_FIELDS = {
    "schema_version", "tool", "archive_layout", "manifest_exclusion", "library_digest",
    "catalog", "packages", "profile", "archive_files", "limitations",
}


def staged_file(source: Path, archive_path: str, label: str) -> dict[str, Any]:
    """Read one checked regular file once; archive and manifest use these exact bytes."""
    source = require_regular_file(source)
    archive_path = normalized_relative(archive_path, label)
    try:
        content = source.read_bytes()
    except OSError as exc:
        fail(f"cannot read {label}: {exc}")
    return {"path": archive_path, "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content), "content": content}


def package_digest(files: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for item in sorted(files, key=lambda record: record["path"]):
        digest.update(item["path"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(item["sha256"].encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def archive_file_record(staged: dict[str, Any]) -> dict[str, Any]:
    return {key: staged[key] for key in ("path", "sha256", "bytes")}


def deterministic_zip_write(archive: zipfile.ZipFile, path: str, content: bytes) -> None:
    info = zipfile.ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.flag_bits = 0
    archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def manifest_from_staged(report: dict[str, Any], staged: list[dict[str, Any]], catalog_data: dict[str, Any], profile: str | None, profile_digest: str | None) -> dict[str, Any]:
    by_path = {item["path"]: item for item in staged}
    packages: list[dict[str, Any]] = []
    for package in report["packages"]:
        name = package["name"]
        files = []
        for source_file in package["files"]:
            archive_path = f"{name}/{source_file['path']}"
            staged_item = by_path.get(archive_path)
            if staged_item is None or staged_item["sha256"] != source_file["sha256"] or staged_item["bytes"] != source_file["bytes"]:
                fail(f"source changed while staging package resource: {archive_path}")
            files.append({"path": source_file["path"], "sha256": staged_item["sha256"], "bytes": staged_item["bytes"]})
        skill_content = by_path[f"{name}/SKILL.md"]["content"]
        try:
            words = len(skill_content.decode("utf-8").split())
        except UnicodeDecodeError:
            fail(f"staged SKILL.md is not UTF-8: {name}")
        packages.append({
            "name": name,
            "path": name,
            "digest": package_digest(files),
            "files": files,
            "skill_markdown": {"bytes": len(skill_content), "words": words, "token_estimate": (words * 4 + 2) // 3, "token_estimate_label": "heuristic"},
        })
    whole = hashlib.sha256()
    for package in packages:
        whole.update(package["name"].encode("utf-8"))
        whole.update(b"\0")
        whole.update(package["digest"].encode("ascii"))
        whole.update(b"\n")
    catalog_file = by_path["catalog.json"]
    catalog = {
        "path": "catalog.json", "sha256": catalog_file["sha256"], "bytes": catalog_file["bytes"],
        "schema_version": catalog_data["schema_version"], "library_version": catalog_data["library_version"],
        "playbook_version": catalog_data["playbook_version"], "source_commit": catalog_data["source_commit"],
        "status": catalog_data["status"], "skill_ids": [item["id"] for item in catalog_data["skills"]],
    }
    profile_record: dict[str, Any] | None = None
    if profile is not None:
        profile_files = [item for item in staged if item["path"].startswith("implementation-profiles/python/")]
        if {item["path"] for item in profile_files} != {
            "implementation-profiles/python/README.md", "implementation-profiles/python/profile.json",
        }:
            fail("python-local profile staging is incomplete")
        actual_profile_digest = hashlib.sha256()
        for item in sorted(profile_files, key=lambda record: record["path"]):
            actual_profile_digest.update(item["path"].replace("implementation-profiles/python/", "implementation-profiles/python/").encode("utf-8"))
            actual_profile_digest.update(b"\0")
            actual_profile_digest.update(item["sha256"].encode("ascii"))
            actual_profile_digest.update(b"\n")
        if actual_profile_digest.hexdigest() != profile_digest:
            fail("source changed while staging implementation profile")
        profile_record = {"id": profile, "digest": profile_digest, "files": [archive_file_record(item) for item in sorted(profile_files, key=lambda record: record["path"])]}
    return {
        "schema_version": "1.0",
        "tool": "skillctl",
        "archive_layout": "flat-skills-v1",
        "manifest_exclusion": "manifest.json is intentionally excluded from archive_files to avoid a self-referential digest; every other archive member is listed.",
        "library_digest": whole.hexdigest(),
        "catalog": catalog,
        "packages": packages,
        "profile": profile_record,
        "archive_files": [archive_file_record(item) for item in sorted(staged, key=lambda record: record["path"])],
        "limitations": "Offline static archive verification only; hashes bind archive bytes but do not establish authorization, execution, isolation, runtime safety, or cryptographic tamper proof.",
    }


def package_library(root_arg: str, output_arg: str, profile: str | None, force: bool) -> dict[str, Any]:
    report = inventory(root_arg)
    root = require_directory(Path(root_arg))
    profile_digest = None
    if profile:
        profile_digest = validate_profile(root, profile)
    # Validate and then stage each file once.  The archive is written only from
    # these bytes, so a later source mutation cannot create a stale inventory in
    # the resulting ZIP (concurrent filesystem replacement is not tamper proof).
    staged: list[dict[str, Any]] = []
    for package in report["packages"]:
        base = root / package["path"]
        for item in package["files"]:
            staged.append(staged_file(confined_file(base, item["path"], "package resource"), f"{package['name']}/{item['path']}", "archive package resource"))
    catalog_source = require_regular_file(root / "development-skills/catalog.json")
    catalog_stage = staged_file(catalog_source, "catalog.json", "archive catalog")
    try:
        catalog_data = validate_catalog_data(parse_json_text(catalog_stage["content"].decode("utf-8"), "staged catalog"), set(EXPECTED_SKILLS))
    except UnicodeDecodeError:
        fail("catalog is not UTF-8")
    staged.append(catalog_stage)
    contracts = require_directory(root / "development-skills/contracts")
    contract_sources = {source.relative_to(contracts).as_posix(): source for source in walk_regular_files(contracts)}
    if set(contract_sources) != CONTRACT_FILES:
        fail(f"archive contracts must exactly be {sorted(CONTRACT_FILES)} (missing={sorted(CONTRACT_FILES - set(contract_sources))}, extra={sorted(set(contract_sources) - CONTRACT_FILES)})")
    staged_contracts: dict[str, Any] = {}
    for relative in sorted(CONTRACT_FILES):
        item = staged_file(contract_sources[relative], f"contracts/{relative}", "archive contract")
        try:
            staged_contracts[relative] = parse_json_text(item["content"].decode("utf-8"), f"contract {relative}")
        except UnicodeDecodeError:
            fail(f"contract {relative} is not UTF-8")
        staged.append(item)
    validate_contract_schema_data(staged_contracts["packet.schema.json"], staged_contracts["evaluation-cases.schema.json"])
    if profile:
        profile_json = staged_file(root / "implementation-profiles/python/profile.json", "implementation-profiles/python/profile.json", "archive profile")
        profile_readme = staged_file(root / "implementation-profiles/python/README.md", "implementation-profiles/python/README.md", "archive profile README")
        try:
            validate_profile_data(parse_json_text(profile_json["content"].decode("utf-8"), "staged profile"))
        except UnicodeDecodeError:
            fail("profile is not UTF-8")
        staged.extend((profile_json, profile_readme))
    if len({item["path"] for item in staged}) != len(staged):
        fail("duplicate archive paths while staging")
    manifest = manifest_from_staged(report, staged, catalog_data, profile, profile_digest)
    output = Path(output_arg)
    parent = require_directory(output.parent)
    target = Path(os.path.abspath(os.fspath(output)))
    require_no_symlink_components(target, require_exists=False)
    if target.exists() and not force:
        fail(f"refusing to overwrite existing package: {target}")
    if target.exists():
        require_regular_file(target)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=parent)
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, strict_timestamps=True) as archive:
            for item in sorted(staged, key=lambda record: record["path"]):
                deterministic_zip_write(archive, item["path"], item["content"])
            deterministic_zip_write(archive, "manifest.json", canonical_json(manifest))
        content = temporary.read_bytes()
        atomic_bytes(target, content, overwrite=force)
    finally:
        if temporary.exists():
            temporary.unlink()
    return {"schema_version": "1.0", "output": str(target), "sha256": sha256_file(target), "packages": [{"name": item["name"], "digest": item["digest"]} for item in manifest["packages"]], "profile": profile, "profile_digest": profile_digest, "manifest_sha256": hashlib.sha256(canonical_json(manifest)).hexdigest()}


def checked_manifest_files(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        fail("manifest archive_files must be a non-empty list")
    paths: set[str] = set()
    records: list[dict[str, Any]] = []
    for index, entry in enumerate(value):
        item = exact_object(entry, {"path", "sha256", "bytes"}, f"manifest archive file {index}")
        path = normalized_relative(item["path"], f"manifest archive file {index} path")
        if path == "manifest.json" or path in paths:
            fail("manifest archive_files contains a duplicate or self-referential path")
        if not isinstance(item["sha256"], str) or not SHA_RE.fullmatch(item["sha256"]):
            fail(f"manifest archive file {path} has invalid sha256")
        if not isinstance(item["bytes"], int) or isinstance(item["bytes"], bool) or item["bytes"] < 0:
            fail(f"manifest archive file {path} has invalid byte count")
        paths.add(path)
        records.append(item)
    if [item["path"] for item in records] != sorted(paths):
        fail("manifest archive_files must be sorted by normalized path")
    return records


def validate_manifest_data(manifest: Any, archive_files: list[dict[str, Any]]) -> dict[str, Any]:
    manifest = exact_object(manifest, MANIFEST_FIELDS, "manifest")
    if manifest["schema_version"] != "1.0" or manifest["tool"] != "skillctl" or manifest["archive_layout"] != "flat-skills-v1":
        fail("manifest schema_version, tool, or archive_layout is invalid")
    if not isinstance(manifest["manifest_exclusion"], str) or "manifest.json" not in manifest["manifest_exclusion"]:
        fail("manifest must document its manifest.json exclusion")
    if not isinstance(manifest["limitations"], str) or not manifest["limitations"].strip():
        fail("manifest limitations must be a non-empty string")
    expected_records = checked_manifest_files(manifest["archive_files"])
    if expected_records != archive_files:
        fail("manifest archive_files does not exactly describe archive members")
    expected_contracts = {f"contracts/{name}" for name in CONTRACT_FILES}
    archive_contracts = {item["path"] for item in archive_files if item["path"].startswith("contracts/")}
    if archive_contracts != expected_contracts:
        fail(f"archive contracts must exactly be {sorted(expected_contracts)} (missing={sorted(expected_contracts - archive_contracts)}, extra={sorted(archive_contracts - expected_contracts)})")
    package_prefixes = tuple(f"{name}/" for name in EXPECTED_SKILLS)
    for item in archive_files:
        path = item["path"]
        if path == "catalog.json" or path in expected_contracts or path.startswith(package_prefixes) or path.startswith("implementation-profiles/python/"):
            continue
        fail(f"manifest archive file is unassigned: {path}")
    catalog = exact_object(manifest["catalog"], {"path", "sha256", "bytes", "schema_version", "library_version", "playbook_version", "source_commit", "status", "skill_ids"}, "manifest catalog")
    if catalog["path"] != "catalog.json":
        fail("manifest catalog path must be catalog.json")
    matching = next((item for item in archive_files if item["path"] == "catalog.json"), None)
    if matching is None or any(catalog[field] != matching[field] for field in ("path", "sha256", "bytes")):
        fail("manifest catalog identity does not match catalog.json")
    if not isinstance(manifest["library_digest"], str) or not SHA_RE.fullmatch(manifest["library_digest"]):
        fail("manifest library_digest must be lowercase 64-hex")
    packages = manifest["packages"]
    if not isinstance(packages, list) or len(packages) != len(EXPECTED_SKILLS):
        fail("manifest packages must describe exactly eight skills")
    names: set[str] = set()
    whole = hashlib.sha256()
    for index, entry in enumerate(packages):
        package = exact_object(entry, {"name", "path", "digest", "files", "skill_markdown"}, f"manifest package {index}")
        name = package["name"]
        if not isinstance(name, str) or name not in EXPECTED_SKILLS or name in names or package["path"] != name:
            fail("manifest package names and flat paths must exactly match supported skills")
        names.add(name)
        if not isinstance(package["digest"], str) or not SHA_RE.fullmatch(package["digest"]):
            fail(f"manifest package {name} has invalid digest")
        files = checked_manifest_files(package["files"])
        declared_paths = {item["path"] for item in files}
        if not REQUIRED_FILES.issubset(declared_paths):
            fail(f"manifest package {name} is missing required resources")
        prefix = f"{name}/"
        archive_paths = {item["path"][len(prefix):] for item in archive_files if item["path"].startswith(prefix)}
        for relative in archive_paths:
            if not supported_package_resource(relative):
                fail(f"manifest package {name} has unsupported archive resource: {relative}")
        if archive_paths != declared_paths:
            fail(f"manifest package {name} resources do not exactly inventory archive members (missing={sorted(archive_paths - declared_paths)}, extra={sorted(declared_paths - archive_paths)})")
        for item in files:
            relative = item["path"]
            if not supported_package_resource(relative):
                fail(f"manifest package {name} has unsupported resource: {relative}")
            archive_record = next((record for record in archive_files if record["path"] == f"{name}/{relative}"), None)
            if archive_record is None or archive_record["sha256"] != item["sha256"] or archive_record["bytes"] != item["bytes"]:
                fail(f"manifest package {name} resource is absent or mismatched: {relative}")
        if package_digest(files) != package["digest"]:
            fail(f"manifest package {name} digest does not match its resources")
        markdown = exact_object(package["skill_markdown"], {"bytes", "words", "token_estimate", "token_estimate_label"}, f"manifest package {name} skill_markdown")
        skill = next((item for item in files if item["path"] == "SKILL.md"), None)
        if skill is None or markdown["bytes"] != skill["bytes"] or not isinstance(markdown["words"], int) or isinstance(markdown["words"], bool) or markdown["words"] < 0 or markdown["token_estimate"] != (markdown["words"] * 4 + 2) // 3 or markdown["token_estimate_label"] != "heuristic":
            fail(f"manifest package {name} has invalid SKILL.md descriptor")
        whole.update(name.encode("utf-8"))
        whole.update(b"\0")
        whole.update(package["digest"].encode("ascii"))
        whole.update(b"\n")
    if names != set(EXPECTED_SKILLS) or [item["name"] for item in packages] != list(EXPECTED_SKILLS):
        fail("manifest packages must be in the canonical eight-skill order")
    if whole.hexdigest() != manifest["library_digest"]:
        fail("manifest library_digest does not match package descriptors")
    profile = manifest["profile"]
    profile_paths = {item["path"] for item in archive_files if item["path"].startswith("implementation-profiles/python/")}
    if profile is None:
        if profile_paths:
            fail("manifest has profile files without a profile record")
    else:
        profile = exact_object(profile, {"id", "digest", "files"}, "manifest profile")
        if profile["id"] != "python-local" or not isinstance(profile["digest"], str) or not SHA_RE.fullmatch(profile["digest"]):
            fail("manifest profile identity is invalid")
        files = checked_manifest_files(profile["files"])
        expected = {"implementation-profiles/python/README.md", "implementation-profiles/python/profile.json"}
        if {item["path"] for item in files} != expected or profile_paths != expected:
            fail("manifest profile files are incomplete")
        digest = hashlib.sha256()
        for item in files:
            archive_item = next((record for record in archive_files if record["path"] == item["path"]), None)
            if archive_item is None or archive_item["sha256"] != item["sha256"] or archive_item["bytes"] != item["bytes"]:
                fail("manifest profile file is absent or mismatched")
            digest.update(item["path"].encode("utf-8"))
            digest.update(b"\0")
            digest.update(item["sha256"].encode("ascii"))
            digest.update(b"\n")
        if digest.hexdigest() != profile["digest"]:
            fail("manifest profile digest does not match its files")
    return manifest


def verify_package(package_arg: str) -> dict[str, Any]:
    package = require_regular_file(Path(package_arg))
    try:
        with zipfile.ZipFile(package, "r") as archive:
            infos = archive.infolist()
            if not infos:
                fail("package ZIP is empty")
            by_name: dict[str, zipfile.ZipInfo] = {}
            for info in infos:
                name = normalized_relative(info.filename, "ZIP entry")
                if name in by_name:
                    fail(f"package ZIP has duplicate entry: {name}")
                mode = (info.external_attr >> 16) & 0xFFFF
                if info.is_dir() or info.flag_bits & 0x1 or not stat.S_ISREG(mode):
                    fail(f"ZIP entry is not an unencrypted regular file: {name}")
                by_name[name] = info
            manifest_info = by_name.get("manifest.json")
            if manifest_info is None:
                fail("package ZIP is missing manifest.json")
            try:
                manifest = parse_json_text(archive.read(manifest_info).decode("utf-8"), "package manifest")
            except UnicodeDecodeError:
                fail("package manifest is not UTF-8")
            observed: list[dict[str, Any]] = []
            for name, info in sorted(by_name.items()):
                if name == "manifest.json":
                    continue
                content = archive.read(info)
                observed.append({"path": name, "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)})
            validated = validate_manifest_data(manifest, observed)
            catalog_content = archive.read(by_name["catalog.json"])
            try:
                catalog_data = parse_json_text(catalog_content.decode("utf-8"), "archived catalog")
            except UnicodeDecodeError:
                fail("archived catalog is not UTF-8")
            validate_catalog_data(catalog_data, set(EXPECTED_SKILLS))
            catalog = validated["catalog"]
            catalog_fields = ("schema_version", "library_version", "playbook_version", "source_commit", "status")
            if any(catalog[field] != catalog_data[field] for field in catalog_fields) or catalog["skill_ids"] != [item["id"] for item in catalog_data["skills"]]:
                fail("manifest catalog metadata does not match catalog.json")
            archived_contracts: dict[str, Any] = {}
            for name in sorted(CONTRACT_FILES):
                try:
                    archived_contracts[name] = parse_json_text(archive.read(by_name[f"contracts/{name}"]).decode("utf-8"), f"archived contracts/{name}")
                except UnicodeDecodeError:
                    fail(f"archived contracts/{name} is not UTF-8")
            validate_contract_schema_data(archived_contracts["packet.schema.json"], archived_contracts["evaluation-cases.schema.json"])
            if validated["profile"] is not None:
                try:
                    profile_data = parse_json_text(archive.read(by_name["implementation-profiles/python/profile.json"]).decode("utf-8"), "archived profile")
                except UnicodeDecodeError:
                    fail("archived profile is not UTF-8")
                validate_profile_data(profile_data)
    except zipfile.BadZipFile as exc:
        fail(f"invalid package ZIP: {exc}")
    return {"schema_version": "1.0", "package": str(package), "sha256": sha256_file(package), "library_digest": validated["library_digest"], "profile": None if validated["profile"] is None else validated["profile"]["id"], "limitations": "Offline static archive verification only; no extraction or execution was performed and no authorization or cryptographic tamper-proof claim is made."}


STAGES = ("initialized", "planned", "implemented", "tested", "cleaned", "retested", "packaged", "review_ready")
EVENT_TO_STAGE = {"plan": "planned", "implement": "implemented", "test": "tested", "cleanup": "cleaned", "retest": "retested", "package": "packaged", "review_ready": "review_ready"}
NEXT_EVENT = dict(zip(STAGES[:-1], EVENT_TO_STAGE))

# Source identity deliberately omits VCS metadata, the tool's ledger/evidence
# paths, generated output directories, and common test caches.  Retained
# evidence artifacts are checked separately and are never exempt from hashing.
IDENTITY_IGNORED_COMPONENTS = frozenset({
    ".git", ".skillctl", "evidence", "artifacts", "output", "outputs",
    "build", "dist", "coverage", "__pycache__", ".pytest_cache", ".mypy_cache",
})


def state_object(max_repairs: int) -> dict[str, Any]:
    return {"schema_version": "1.0", "stage": "initialized", "max_repairs": max_repairs, "repairs": 0, "workspace": None, "evidence": [], "events": [{"event": "init", "outcome": "pass"}], "blocked": None, "invalidations": [], "source_identity": None}


WORKFLOW_EVIDENCE_FIELDS = {"event", "stage", "artifact", "sha256", "evidence_file", "evidence_file_sha256", "valid", "outcome", "source_snapshot"}


def validate_snapshot(value: Any, label: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        fail(f"{label} must be a list")
    records: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, record in enumerate(value):
        item = exact_object(record, {"artifact", "sha256"}, f"{label} item {index}")
        artifact = normalized_relative(item["artifact"], f"{label} artifact")
        if artifact in seen or not isinstance(item["sha256"], str) or not SHA_RE.fullmatch(item["sha256"]):
            fail(f"{label} has duplicate or invalid file hashes")
        seen.add(artifact)
        records.append(item)
    if [record["artifact"] for record in records] != sorted(seen):
        fail(f"{label} must be sorted by normalized artifact")
    return records


def validate_state(data: Any) -> dict[str, Any]:
    state = exact_object(data, {"schema_version", "stage", "max_repairs", "repairs", "workspace", "evidence", "events", "blocked", "invalidations", "source_identity"}, "workflow state")
    if state["schema_version"] != "1.0" or not isinstance(state["stage"], str) or state["stage"] not in STAGES:
        fail("workflow state schema_version or stage is invalid")
    for field in ("max_repairs", "repairs"):
        if not isinstance(state[field], int) or isinstance(state[field], bool) or state[field] < 0:
            fail(f"workflow state {field} must be a non-negative integer")
    if state["repairs"] > state["max_repairs"]:
        fail("workflow state repairs exceeds max_repairs")
    if state["workspace"] is not None and (not isinstance(state["workspace"], str) or not os.path.isabs(state["workspace"])):
        fail("workflow state workspace must be null or an absolute path")
    if not isinstance(state["evidence"], list) or not isinstance(state["events"], list) or not isinstance(state["invalidations"], list):
        fail("workflow state evidence, events, and invalidations must be lists")
    if not state["events"]:
        fail("workflow state must retain its event history")
    if state["events"][0] != {"event": "init", "outcome": "pass"}:
        fail("workflow state must begin with the immutable init event")
    cursor = "initialized"
    active_block: str | None = None
    replay_repairs = 0
    evidence_events: list[dict[str, Any]] = []
    invalidation_events: list[dict[str, Any]] = []
    for index, event in enumerate(state["events"][1:], 1):
        if not isinstance(event, dict):
            fail(f"workflow event {index} must be an object")
        name = event.get("event")
        if not isinstance(name, str):
            fail(f"workflow event {index} has an invalid event name")
        if name in EVENT_TO_STAGE:
            expected = NEXT_EVENT.get(cursor)
            if active_block is not None or name != expected or event.keys() != {"event", "outcome", "artifact", "sha256"} or event["outcome"] != "pass":
                fail(f"workflow event history has an invalid stage transition at event {index}")
            normalized_relative(event["artifact"], f"workflow event {index} artifact")
            if not isinstance(event["sha256"], str) or not SHA_RE.fullmatch(event["sha256"]):
                fail(f"workflow event {index} has invalid evidence hash")
            cursor = EVENT_TO_STAGE[name]
            evidence_events.append(event)
        elif name in {"block", "fail"}:
            if active_block is not None or cursor == "initialized" or event.keys() != {"event", "outcome", "artifact", "sha256"} or event["outcome"] != name:
                fail(f"workflow event history has an invalid blocked replay at event {index}")
            normalized_relative(event["artifact"], f"workflow event {index} artifact")
            if not isinstance(event["sha256"], str) or not SHA_RE.fullmatch(event["sha256"]):
                fail(f"workflow event {index} has invalid evidence hash")
            active_block = name
            evidence_events.append(event)
        elif name == "repair":
            # A denied repair is an observation, not a successful transition.
            # Retain it without poisoning subsequent reads of the bounded ledger.
            if event == {"event": "repair", "outcome": "fail", "reason": "repair_limit_reached"}:
                if replay_repairs < state["max_repairs"]:
                    fail("workflow records a repair-cap denial before its limit")
                continue
            if active_block is None or cursor == "initialized" or replay_repairs >= state["max_repairs"] or event.keys() != {"event", "outcome", "artifact", "sha256"} or event["outcome"] != "pass":
                fail(f"workflow event history has an invalid bounded repair at event {index}")
            normalized_relative(event["artifact"], f"workflow event {index} artifact")
            if not isinstance(event["sha256"], str) or not SHA_RE.fullmatch(event["sha256"]):
                fail(f"workflow event {index} has invalid evidence hash")
            replay_repairs += 1
            cursor = "implemented"
            active_block = None
            evidence_events.append(event)
            invalidation_events.append({"reason": "repair"})
        elif name == "invalidate":
            if active_block is not None or cursor not in {"retested", "packaged", "review_ready"} or event.keys() != {"event", "outcome", "reason"} or event["outcome"] != "fail" or not isinstance(event["reason"], str) or not event["reason"].strip():
                fail(f"workflow event history has an invalid invalidation at event {index}")
            cursor = "implemented"
            active_block = "invalidate"
            invalidation_events.append({"reason": event["reason"]})
        else:
            fail(f"workflow event history has an unsupported event at event {index}")
    if state["stage"] != cursor or state["repairs"] != replay_repairs:
        fail("workflow state stage or repair count does not match its event history")
    if state["blocked"] is None:
        if active_block is not None:
            fail("workflow state omits its active block")
    else:
        blocked = exact_object(state["blocked"], {"event", "reason", "requires"}, "workflow state blocked")
        if active_block is None or blocked["event"] != active_block or not isinstance(blocked["reason"], str) or not blocked["reason"].strip() or blocked["requires"] != "repair":
            fail("workflow state blocked does not match its event history")
    if len(state["invalidations"]) != len(invalidation_events):
        fail("workflow state invalidation ledger does not match its event history")
    for index, record in enumerate(state["invalidations"]):
        item = exact_object(record, {"reason", "invalidated_events"}, f"workflow invalidation {index}")
        if not isinstance(item["reason"], str) or not item["reason"].strip() or not isinstance(item["invalidated_events"], list) or not all(isinstance(value, str) for value in item["invalidated_events"]):
            fail("workflow invalidation ledger is invalid")
        if item["reason"] != invalidation_events[index]["reason"]:
            fail("workflow invalidation ledger reason does not match event history")
    if len(state["evidence"]) != len(evidence_events):
        fail("workflow evidence ledger does not match its event history")
    last_snapshot: tuple[str, list[dict[str, str]]] | None = None
    package_snapshot: list[dict[str, str]] | None = None
    for index, (record, event) in enumerate(zip(state["evidence"], evidence_events)):
        item = exact_object(record, WORKFLOW_EVIDENCE_FIELDS, f"workflow evidence {index}")
        if item["event"] != event["event"] or item["artifact"] != event["artifact"] or item["sha256"] != event["sha256"] or item["outcome"] != event["outcome"]:
            fail("workflow evidence ledger does not match its event receipt")
        if item["stage"] not in STAGES or not isinstance(item["evidence_file"], str) or not os.path.isabs(item["evidence_file"]) or not isinstance(item["evidence_file_sha256"], str) or not SHA_RE.fullmatch(item["evidence_file_sha256"]) or not isinstance(item["valid"], bool):
            fail("workflow evidence ledger has invalid receipt metadata")
        if item["event"] in {"test", "cleanup", "retest"}:
            snapshot = validate_snapshot(item["source_snapshot"], "workflow evidence source_snapshot")
            last_snapshot = (item["stage"], snapshot)
        elif item["event"] == "package":
            historical_snapshot = validate_snapshot(item["source_snapshot"], "workflow package candidate snapshot")
            if item["valid"]:
                package_snapshot = historical_snapshot
        elif item["source_snapshot"] is not None:
            fail("workflow evidence source_snapshot is allowed only for test, cleanup, retest, or package")
    identity = state["source_identity"]
    if identity is not None:
        identity = exact_object(identity, {"stage", "files"}, "workflow source_identity")
        if identity["stage"] not in {"tested", "cleaned", "retested"}:
            fail("workflow source_identity is invalid")
        files = validate_snapshot(identity["files"], "workflow source_identity")
        if last_snapshot is None or (identity["stage"], files) != last_snapshot:
            fail("workflow source_identity does not match its latest testing receipt")
        if package_snapshot is not None and package_snapshot != files:
            fail("workflow package receipt is not bound to the current retested source identity")
    elif cursor in {"tested", "cleaned", "retested", "packaged", "review_ready"} and active_block is None:
        fail("workflow state after testing must retain a source identity")
    return state


def read_state(path: Path) -> dict[str, Any]:
    return validate_state(parse_json(require_regular_file(path), "workflow state"))


def evidence_workspace(evidence_path: Path, evidence: dict[str, Any]) -> Path:
    candidate = evidence.get("workspace")
    if candidate is None:
        return require_directory(evidence_path.parent)
    if not isinstance(candidate, str) or not os.path.isabs(candidate):
        fail("workflow evidence workspace must be an absolute path when supplied")
    return require_directory(Path(candidate))


def load_evidence(evidence_path: Path, event: str, *, allow_failure: bool) -> tuple[dict[str, Any], Path, str, str]:
    evidence_path = require_regular_file(evidence_path)
    content_hash = sha256_file(evidence_path)
    raw = parse_json(evidence_path, "workflow evidence")
    if not isinstance(raw, dict):
        fail("workflow evidence must be an object")
    if set(raw) not in ({"event", "outcome", "artifact", "sha256"}, {"event", "outcome", "artifact", "sha256", "workspace"}):
        fail("workflow evidence must contain only event, outcome, artifact, sha256, and optional workspace")
    if raw["event"] != event:
        fail("workflow evidence event does not match --event")
    expected_outcome = {"pass"} if not allow_failure else {event}
    if not isinstance(raw["outcome"], str) or raw["outcome"] not in expected_outcome:
        fail("workflow evidence outcome is invalid for the requested event")
    workspace = evidence_workspace(evidence_path, raw)
    if not isinstance(raw["artifact"], str) or not isinstance(raw["sha256"], str):
        fail("workflow evidence artifact and sha256 must be strings")
    artifact = normalized_relative(raw["artifact"], "workflow evidence artifact")
    if not SHA_RE.fullmatch(raw["sha256"]):
        fail("workflow evidence sha256 must be lowercase 64-hex")
    artifact_file = confined_file(workspace, artifact, "workflow evidence artifact")
    if sha256_file(artifact_file) != raw["sha256"]:
        fail("workflow evidence hash does not match artifact")
    return raw, workspace, str(evidence_path), content_hash


def is_identity_excluded(relative: str) -> bool:
    return any(part in IDENTITY_IGNORED_COMPONENTS for part in PurePosixPath(relative).parts)


def workflow_identity_ignored(state: dict[str, Any], state_path: Path, incoming_receipt: Path) -> set[Path]:
    """Return ledger-owned metadata paths excluded from source identity only."""
    ignored = {state_path.resolve(strict=True), incoming_receipt.resolve(strict=True)}
    # All retained receipt files are metadata rather than active source.  They
    # remain separately hash-validated by prior_evidence_is_valid(), including
    # receipts from invalidated attempts.
    for record in state["evidence"]:
        receipt = record.get("evidence_file")
        if isinstance(receipt, str):
            ignored.add(Path(receipt).resolve(strict=False))
    return ignored


def snapshot_workspace(workspace: Path, ignored: set[Path]) -> list[dict[str, str]]:
    """Hash the active source identity under the documented narrow exclusion scope."""
    records: list[dict[str, str]] = []
    root = require_directory(workspace)
    for item in walk_regular_files(root, excluded_components=IDENTITY_IGNORED_COMPONENTS, excluded_paths=frozenset(ignored)):
        resolved = item.resolve(strict=True)
        relative = item.relative_to(root).as_posix()
        if resolved in ignored or is_identity_excluded(relative):
            continue
        records.append({"artifact": relative, "sha256": sha256_file(item)})
    return records


def invalidate(state: dict[str, Any], reason: str) -> None:
    invalid = []
    for record in state["evidence"]:
        if record.get("stage") in {"tested", "cleaned", "retested", "packaged", "review_ready"} and record.get("valid", True):
            record["valid"] = False
            invalid.append(record.get("event", "unknown"))
    state["stage"] = "implemented"
    state["blocked"] = {"event": "invalidate", "reason": reason, "requires": "repair"}
    state["source_identity"] = None
    state["invalidations"].append({"reason": reason, "invalidated_events": invalid})
    state["events"].append({"event": "invalidate", "outcome": "fail", "reason": reason})


def prior_evidence_is_valid(state: dict[str, Any], workspace: Path, *, check_source_identity: bool, ignored: set[Path]) -> tuple[str, str] | None:
    for record in state["evidence"]:
        artifact = record.get("artifact")
        expected = record.get("sha256")
        if not isinstance(artifact, str) or not isinstance(expected, str):
            return "evidence", "workflow state contains malformed evidence"
        try:
            found = confined_file(workspace, artifact, "retained evidence artifact")
        except SkillctlError as exc:
            return "evidence", str(exc)
        if sha256_file(found) != expected:
            return "evidence", f"retained evidence changed: {artifact}"
        evidence_file = record.get("evidence_file")
        evidence_file_sha = record.get("evidence_file_sha256")
        if isinstance(evidence_file, str) and isinstance(evidence_file_sha, str):
            try:
                if sha256_file(require_regular_file(Path(evidence_file))) != evidence_file_sha:
                    return "evidence", f"workflow evidence record changed: {evidence_file}"
            except SkillctlError as exc:
                return "evidence", str(exc)
    identity = state["source_identity"]
    if check_source_identity and identity is not None:
        current = snapshot_workspace(workspace, ignored)
        if current != identity["files"]:
            return "source", "active source identity changed after retest; repair and full retest are required"
    return None


def advance_workflow(state_path: Path, event: str, evidence_path: Path | None) -> dict[str, Any]:
    state_path = require_regular_file(state_path)
    state = read_state(state_path)
    if not isinstance(event, str) or event not in set(EVENT_TO_STAGE) | {"block", "fail", "repair"}:
        fail(f"unsupported workflow event: {event}")
    if evidence_path is None:
        fail("workflow advance requires --evidence")
    raw, workspace, source_evidence_path, source_evidence_hash = load_evidence(evidence_path, event, allow_failure=event in {"block", "fail"})
    if state["workspace"] is None:
        state["workspace"] = str(workspace)
    elif state["workspace"] != str(workspace):
        fail("workflow evidence workspace does not match the initialized workflow workspace")

    ignored = workflow_identity_ignored(state, state_path, Path(source_evidence_path))
    identity_is_bound = state["source_identity"] is not None and state["source_identity"]["stage"] == "retested"
    integrity_problem = prior_evidence_is_valid(
        state,
        workspace,
        check_source_identity=identity_is_bound and event not in {"repair", "cleanup", "retest"},
        ignored=ignored,
    )
    if integrity_problem:
        kind, message = integrity_problem
        if kind == "source" and state["stage"] in {"retested", "packaged", "review_ready"}:
            invalidate(state, message)
            atomic_json(state_path, state, overwrite=True)
        fail(f"workflow cannot advance: {message}")

    if event in {"block", "fail"}:
        if state["stage"] == "initialized":
            fail("workflow block or fail requires a planned or later workflow")
        if state["blocked"] is not None:
            fail("workflow is already blocked; use a bounded repair before recording another block")
        state["blocked"] = {"event": event, "reason": f"{event} evidence was recorded", "requires": "repair"}
        state["events"].append({"event": event, "outcome": raw["outcome"], "artifact": raw["artifact"], "sha256": raw["sha256"]})
        state["evidence"].append({"event": event, "stage": state["stage"], "artifact": raw["artifact"], "sha256": raw["sha256"], "evidence_file": source_evidence_path, "evidence_file_sha256": source_evidence_hash, "valid": True, "outcome": raw["outcome"], "source_snapshot": None})
        atomic_json(state_path, state, overwrite=True)
        return state

    if event == "repair":
        if state["repairs"] >= state["max_repairs"]:
            state["events"].append({"event": "repair", "outcome": "fail", "reason": "repair_limit_reached"})
            atomic_json(state_path, state, overwrite=True)
            fail("workflow repair limit reached")
        if state["stage"] == "initialized":
            fail("workflow repair requires a planned or later workflow")
        if state["blocked"] is None:
            fail("workflow repair requires a retained block or invalidation")
        for record in state["evidence"]:
            if record.get("stage") in {"tested", "cleaned", "retested", "packaged", "review_ready"}:
                record["valid"] = False
        state["repairs"] += 1
        state["stage"] = "implemented"
        state["blocked"] = None
        state["source_identity"] = None
        state["invalidations"].append({"reason": "repair", "invalidated_events": [record.get("event") for record in state["evidence"] if not record.get("valid", True)]})
        state["events"].append({"event": "repair", "outcome": "pass", "artifact": raw["artifact"], "sha256": raw["sha256"]})
        state["evidence"].append({"event": "repair", "stage": "implemented", "artifact": raw["artifact"], "sha256": raw["sha256"], "evidence_file": source_evidence_path, "evidence_file_sha256": source_evidence_hash, "valid": True, "outcome": raw["outcome"], "source_snapshot": None})
        atomic_json(state_path, state, overwrite=True)
        return state

    if state["blocked"] is not None:
        fail("workflow is blocked; use a bounded repair before continuing")
    expected = NEXT_EVENT.get(state["stage"])
    if event != expected:
        fail(f"workflow requires event {expected!r} from stage {state['stage']!r}, not {event!r}")
    target_stage = EVENT_TO_STAGE[event]
    record: dict[str, Any] = {"event": event, "stage": target_stage, "artifact": raw["artifact"], "sha256": raw["sha256"], "evidence_file": source_evidence_path, "evidence_file_sha256": source_evidence_hash, "valid": True, "outcome": raw["outcome"], "source_snapshot": None}
    if event in {"test", "cleanup", "retest"}:
        record["source_snapshot"] = snapshot_workspace(workspace, ignored)
        state["source_identity"] = {"stage": target_stage, "files": record["source_snapshot"]}
    if event == "package":
        if not raw["artifact"].endswith(".zip") or not zipfile.is_zipfile(confined_file(workspace, raw["artifact"], "workflow package archive")):
            fail("workflow package evidence must hash an actual .zip archive")
        if state["source_identity"] is None or state["source_identity"]["stage"] != "retested":
            fail("workflow package requires a current retested source identity")
        record["source_snapshot"] = state["source_identity"]["files"]
    state["evidence"].append(record)
    state["events"].append({"event": event, "outcome": "pass", "artifact": raw["artifact"], "sha256": raw["sha256"]})
    state["stage"] = target_stage
    atomic_json(state_path, state, overwrite=True)
    return state


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise SkillctlError(f"argument error: {message}")


def cli_parser() -> argparse.ArgumentParser:
    parser = JsonArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "inventory"):
        command = commands.add_parser(name)
        command.add_argument("--root", required=True)
        if name == "inventory":
            command.add_argument("--output")
            command.add_argument("--force", action="store_true")
    package = commands.add_parser("package")
    package.add_argument("--root", required=True)
    package.add_argument("--output", required=True)
    package.add_argument("--profile")
    package.add_argument("--force", action="store_true")
    verify = commands.add_parser("verify-package")
    verify.add_argument("package")
    check = commands.add_parser("check-packet")
    check.add_argument("packet")
    check.add_argument("--workspace", required=True)
    workflow = commands.add_parser("workflow")
    workflow_commands = workflow.add_subparsers(dest="workflow_command", required=True)
    init = workflow_commands.add_parser("init")
    init.add_argument("--output", required=True)
    init.add_argument("--max-repairs", type=int, default=2)
    init.add_argument("--force", action="store_true")
    advance = workflow_commands.add_parser("advance")
    advance.add_argument("state")
    advance.add_argument("--event", required=True)
    advance.add_argument("--evidence")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = cli_parser().parse_args(argv)
        if args.command == "validate":
            result = inventory(args.root)
        elif args.command == "inventory":
            result = inventory(args.root)
            if args.output:
                atomic_json(Path(args.output), result, overwrite=args.force)
        elif args.command == "package":
            result = package_library(args.root, args.output, args.profile, args.force)
        elif args.command == "verify-package":
            result = verify_package(args.package)
        elif args.command == "check-packet":
            packet_path = require_regular_file(Path(args.packet))
            workspace = require_directory(Path(args.workspace))
            packet = validate_packet_data(parse_json(packet_path, "packet"), workspace)
            result = {"ok": True, "skill": packet["skill"], "status": packet["status"], "recommendation": packet["decision"]["recommendation"], "limitations": "Static packet checks only; no authorization, execution, isolation, or behavioral conformance is established."}
        elif args.workflow_command == "init":
            if args.max_repairs < 0:
                fail("--max-repairs must be non-negative")
            state_path = Path(args.output)
            atomic_json(state_path, state_object(args.max_repairs), overwrite=args.force)
            result = read_state(state_path)
        else:
            result = advance_workflow(Path(args.state), args.event, Path(args.evidence) if args.evidence else None)
        print(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
        return 0
    except (SkillctlError, OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True, separators=(",", ":")), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
