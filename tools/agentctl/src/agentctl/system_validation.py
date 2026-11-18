from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from functools import lru_cache
from importlib.resources import files
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from agentctl.contracts import EXECUTION_RANK, TIER_RANK
from agentctl.diagnostics import Diagnostic, emit_diagnostics, relative_display
from agentctl.files import DataFileError, load_data
from agentctl.system_risk import validate_system_risk_file
from agentctl.validation import validate_agent_file

SUPPORTED_SUFFIXES = {".json", ".yaml", ".yml"}


def system_schema_path() -> Path:
    return Path(str(files("agentctl").joinpath("schemas/system-spec.schema.json")))


@lru_cache(maxsize=1)
def load_system_schema() -> dict[str, Any]:
    schema = json.loads(system_schema_path().read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def validate_systems(
    *, root: Path, paths: Sequence[Path], output_format: str = "text"
) -> int:
    root = root.resolve()
    targets = _resolve_system_targets(root, paths)
    diagnostics: list[Diagnostic] = []
    if not targets:
        diagnostics.append(
            Diagnostic(
                "SYSTEM001",
                "no System Specs found under src/<package>/systems/<system>/system.yaml",
                str(root),
            )
        )
    for path in targets:
        diagnostics.extend(validate_system_file(path, root=root))
    return emit_diagnostics(
        diagnostics,
        output_format=output_format,
        heading="Multi-agent system contract validation",
    )


def validate_system_file(path: Path, *, root: Path) -> list[Diagnostic]:
    path = path if path.is_absolute() else root / path
    shown = relative_display(path, root)
    try:
        payload = load_data(path)
    except DataFileError as exc:
        return [Diagnostic("SYSTEM002", str(exc), shown)]

    validator = Draft202012Validator(
        load_system_schema(), format_checker=FormatChecker()
    )
    schema_errors = sorted(validator.iter_errors(payload), key=_schema_error_key)
    if schema_errors:
        return [
            Diagnostic(
                "SYSTEM003",
                f"{_json_path(error.absolute_path)}: {error.message}",
                shown,
            )
            for error in schema_errors
        ]
    return _system_semantic_diagnostics(payload, path=path, root=root)


def _system_semantic_diagnostics(
    payload: Mapping[str, Any], *, path: Path, root: Path
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    def error(code: str, message: str, target: Path = path) -> None:
        diagnostics.append(Diagnostic(code, message, relative_display(target, root)))

    name = payload["name"]
    metadata = payload["metadata"]
    topology = payload["topology"]
    if name.replace("-", "_") != path.parent.name:
        error("SYSTEM004", "system directory must match the normalized system name")
    if "replace with" in payload["description"].lower():
        error("SYSTEM005", "replace the generated placeholder description")
    if (
        metadata["owner"] == "replace-me"
        or metadata["operational_owner"] == "replace-me"
    ):
        error("SYSTEM006", "metadata owners must name accountable owners")

    execution_class = metadata["execution_class"]
    if execution_class in {"durable", "human_governed"}:
        if metadata["temporal_enabled"] is not True:
            error("SYSTEM007", "durable execution requires temporal_enabled: true")
        package_dir = path.parents[2]
        for directory in (package_dir / "workflows", package_dir / "activities"):
            if not directory.is_dir():
                error(
                    "SYSTEM008", "durable execution requires this directory", directory
                )
    if execution_class == "human_governed":
        approval = metadata.get("approval_policy")
        if not isinstance(approval, str) or not (root / approval).is_file():
            error("SYSTEM009", "human-governed execution requires an approval policy")

    for field, code in (
        ("risk_assessment", "SYSTEM010"),
        ("threat_model", "SYSTEM011"),
        ("evaluation_policy", "SYSTEM012"),
    ):
        reference = metadata[field]
        if not (root / reference).is_file():
            error(code, f"metadata.{field} does not exist", root / reference)
    for reference, code, label in (
        (payload["state"]["artifact_policy"], "SYSTEM013", "artifact policy"),
        (payload["termination"]["policy"], "SYSTEM014", "termination policy"),
    ):
        target = _reference_path(root, path.parent, reference)
        if not target.is_file():
            error(code, f"{label} does not exist", target)
    if topology["dynamic_membership"]:
        for field, code in (
            ("registry", "SYSTEM015"),
            ("admission_policy", "SYSTEM016"),
        ):
            target = _reference_path(root, path.parent, topology[field])
            if not target.is_file():
                error(code, f"topology.{field} does not exist", target)

    members = payload["members"]
    member_names = [item["agent"] for item in members]
    if len(member_names) != len(set(member_names)):
        error("SYSTEM017", "members contain duplicate agent names")
    coordinator = topology.get("coordinator")
    if coordinator is not None and coordinator not in member_names:
        error("SYSTEM018", "topology.coordinator must name a declared member")

    resolved_members: dict[str, Mapping[str, Any]] = {}
    for member in members:
        candidates = sorted(root.glob("src/*/agents/*/agent.yaml"))
        matches: list[tuple[Path, Mapping[str, Any]]] = []
        for candidate in candidates:
            try:
                spec = load_data(candidate)
            except DataFileError:
                continue
            if spec.get("name") == member["agent"]:
                matches.append((candidate, spec))
        if not matches:
            error("SYSTEM019", f"member agent {member['agent']!r} was not found")
            continue
        if len(matches) > 1:
            error("SYSTEM020", f"member agent {member['agent']!r} is ambiguous")
            continue
        agent_path, spec = matches[0]
        member_diagnostics = validate_agent_file(agent_path, root)
        diagnostics.extend(member_diagnostics)
        if any(item.severity == "error" for item in member_diagnostics):
            continue
        agent_metadata = spec.get("metadata")
        if not isinstance(agent_metadata, Mapping):
            continue
        resolved_members[member["agent"]] = agent_metadata
        if agent_metadata.get("version") != member["version"]:
            error(
                "SYSTEM021",
                f"member {member['agent']!r} version does not match Agent Spec",
            )
        member_class = agent_metadata.get("execution_class")
        if (
            member_class in EXECUTION_RANK
            and EXECUTION_RANK[execution_class] < EXECUTION_RANK[member_class]
        ):
            error(
                "SYSTEM022",
                f"system execution class is below member {member['agent']!r}",
            )
        member_tier = agent_metadata.get("risk_tier")
        if (
            member_tier in TIER_RANK
            and TIER_RANK[metadata["governance_tier"]] < TIER_RANK[member_tier]
        ):
            error(
                "SYSTEM023",
                f"system governance tier is below member {member['agent']!r}",
            )
        restrictions = member.get("restrictions", {})
        for field, metadata_field in (
            ("skills", "enabled_skills"),
            ("toolsets", "enabled_toolsets"),
        ):
            selected = restrictions.get(field, {}).get("include", [])
            allowed = agent_metadata.get(metadata_field, [])
            undeclared = sorted(set(selected) - set(allowed))
            if undeclared:
                error(
                    "SYSTEM024",
                    f"member {member['agent']!r} restrictions expand {field}: {undeclared}",
                )

    interactions = payload["interactions"]
    interaction_ids = [item["id"] for item in interactions]
    if len(interaction_ids) != len(set(interaction_ids)):
        error("SYSTEM025", "interactions contain duplicate IDs")
    allowed_callers = set(member_names) | {topology["orchestrator"]}
    seen_edges: set[tuple[str, str, str]] = set()
    for interaction in interactions:
        if interaction["from"] not in allowed_callers:
            error(
                "SYSTEM026",
                f"interaction {interaction['id']!r} has an undeclared caller",
            )
        if interaction["to"] not in member_names:
            error(
                "SYSTEM027",
                f"interaction {interaction['id']!r} has an undeclared callee",
            )
        edge = (interaction["from"], interaction["to"], interaction["mode"])
        if edge in seen_edges:
            error("SYSTEM028", f"duplicate interaction edge {edge!r}")
        seen_edges.add(edge)
        policy_path = _reference_path(root, path.parent, interaction["policy"])
        if not policy_path.is_file():
            error(
                "SYSTEM029",
                f"interaction {interaction['id']!r} policy does not exist",
                policy_path,
            )
        else:
            try:
                policy = load_data(policy_path)
            except DataFileError as exc:
                error("SYSTEM030", str(exc), policy_path)
            else:
                policy_interactions = policy.get("interactions")
                if (
                    isinstance(policy_interactions, Mapping)
                    and interaction["id"] not in policy_interactions
                ):
                    error(
                        "SYSTEM031",
                        f"policy does not define interaction {interaction['id']!r}",
                        policy_path,
                    )

    limits = payload["limits"]
    required_members = sum(1 for member in members if member["required"])
    if limits["max_agent_runs"] < required_members:
        error("SYSTEM032", "max_agent_runs is below the required member count")
    if limits["max_parallel_agents"] > limits["max_agent_runs"]:
        error("SYSTEM033", "max_parallel_agents cannot exceed max_agent_runs")
    if topology["recursive_delegation"] and limits["max_delegation_depth"] < 1:
        error("SYSTEM034", "recursive delegation requires positive maximum depth")

    risk_reference = metadata["risk_assessment"]
    risk_path = root / risk_reference
    if risk_path.is_file():
        risk_diagnostics = validate_system_risk_file(risk_path, root=root)
        diagnostics.extend(risk_diagnostics)
        if not any(item.severity == "error" for item in risk_diagnostics):
            risk = load_data(risk_path)
            assessment = risk["assessment"]
            classification = risk["classification"]
            scope = risk["scope"]
            if assessment.get("system") != name:
                error("SYSTEM035", "risk assessment system does not match System Spec")
            if assessment.get("system_version") != metadata["version"]:
                error("SYSTEM036", "risk assessment version does not match System Spec")
            if scope.get("execution_class") != execution_class:
                error("SYSTEM037", "risk assessment execution class does not match")
            if classification.get("governance_tier") != metadata["governance_tier"]:
                error("SYSTEM038", "risk assessment governance tier does not match")
            risk_members = {
                (item.get("agent"), item.get("agent_version"))
                for item in risk["member_assessments"]
                if isinstance(item, Mapping)
            }
            spec_members = {(item["agent"], item["version"]) for item in members}
            if risk_members != spec_members:
                error(
                    "SYSTEM039", "risk assessment member set does not match System Spec"
                )
    return diagnostics


def _reference_path(root: Path, system_dir: Path, reference: str) -> Path:
    raw = reference.split("#", 1)[0]
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate
    local = system_dir / candidate
    return local if local.exists() else root / candidate


def _resolve_system_targets(root: Path, paths: Sequence[Path]) -> list[Path]:
    if paths:
        targets: set[Path] = set()
        for raw in paths:
            path = raw if raw.is_absolute() else root / raw
            if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
                targets.add(path.resolve())
            elif path.is_dir():
                targets.update(item.resolve() for item in path.rglob("system.yaml"))
            elif path.suffix.lower() in SUPPORTED_SUFFIXES:
                targets.add(path.resolve())
        return sorted(targets)
    return sorted(root.glob("src/*/systems/*/system.yaml"))


def _schema_error_key(error: Any) -> tuple[str, str]:
    return (_json_path(error.absolute_path), error.message)


def _json_path(parts: Sequence[Any]) -> str:
    rendered = "$"
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered
