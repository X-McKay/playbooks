from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import date
from functools import lru_cache
from importlib.resources import files
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from agentctl.contracts import TIER_RANK
from agentctl.diagnostics import Diagnostic, relative_display
from agentctl.files import DataFileError, load_data
from agentctl.risk import matrix_tier


@lru_cache(maxsize=1)
def load_system_risk_schema() -> dict[str, Any]:
    schema = json.loads(
        files("agentctl")
        .joinpath("schemas/system-risk-assessment.schema.json")
        .read_text(encoding="utf-8")
    )
    Draft202012Validator.check_schema(schema)
    return schema


def validate_system_risk_file(path: Path, *, root: Path) -> list[Diagnostic]:
    path = path if path.is_absolute() else root / path
    shown = relative_display(path, root)
    try:
        payload = load_data(path)
    except DataFileError as exc:
        return [Diagnostic("SYSRISK002", str(exc), shown)]

    schema_errors = sorted(
        Draft202012Validator(load_system_risk_schema()).iter_errors(payload),
        key=lambda error: (error.json_path, error.message),
    )
    if schema_errors:
        return [
            Diagnostic("SYSRISK025", f"{error.json_path}: {error.message}", shown)
            for error in schema_errors
        ]

    diagnostics: list[Diagnostic] = []
    required_mappings = (
        "assessment",
        "scope",
        "classification",
        "regulatory_screen",
        "acceptance",
        "monitoring",
    )
    for field in required_mappings:
        if not isinstance(payload.get(field), Mapping):
            diagnostics.append(
                Diagnostic("SYSRISK003", f"{field} must be a mapping", shown)
            )
    for field in ("member_assessments", "scenarios"):
        if not isinstance(payload.get(field), list) or not payload[field]:
            diagnostics.append(
                Diagnostic("SYSRISK004", f"{field} must be a non-empty list", shown)
            )
    if diagnostics:
        return diagnostics

    assessment = payload["assessment"]
    classification = payload["classification"]
    regulatory = payload["regulatory_screen"]
    for field in (
        "system",
        "system_version",
        "assessment_version",
        "status",
        "assessed_at",
        "review_by",
        "prepared_by",
    ):
        if assessment.get(field) in (None, "", [], {}):
            diagnostics.append(
                Diagnostic("SYSRISK005", f"assessment.{field} is required", shown)
            )
    tiers = ("low", "medium", "high", "critical")
    for field in (
        "governance_tier",
        "maximum_member_tier",
        "maximum_inherent_tier",
        "maximum_residual_tier",
    ):
        if classification.get(field) not in tiers:
            diagnostics.append(
                Diagnostic(
                    "SYSRISK006",
                    f"classification.{field} must be low, medium, high, or critical",
                    shown,
                )
            )
    if classification.get("decision") not in {"go", "conditional_go", "no_go"}:
        diagnostics.append(
            Diagnostic("SYSRISK007", "classification.decision is invalid", shown)
        )

    member_ids: set[tuple[Any, Any]] = set()
    member_tiers: list[str] = []
    for member in payload["member_assessments"]:
        if not isinstance(member, Mapping):
            diagnostics.append(
                Diagnostic("SYSRISK008", "member assessment must be a mapping", shown)
            )
            continue
        identity = (member.get("agent"), member.get("agent_version"))
        if identity in member_ids:
            diagnostics.append(
                Diagnostic(
                    "SYSRISK009",
                    f"duplicate member assessment {identity[0]!r} {identity[1]!r}",
                    shown,
                )
            )
        member_ids.add(identity)
        tier = member.get("governance_tier")
        if tier in TIER_RANK:
            member_tiers.append(tier)
        else:
            diagnostics.append(
                Diagnostic(
                    "SYSRISK010",
                    f"member {identity[0]!r} has invalid governance tier",
                    shown,
                )
            )
        reference = member.get("assessment")
        if not isinstance(reference, str) or not (root / reference).is_file():
            diagnostics.append(
                Diagnostic(
                    "SYSRISK011",
                    f"member {identity[0]!r} assessment does not exist",
                    shown,
                )
            )

    scenario_ids: set[str] = set()
    inherent_tiers: list[str] = []
    residual_tiers: list[str] = []
    for scenario in payload["scenarios"]:
        if not isinstance(scenario, Mapping):
            diagnostics.append(
                Diagnostic("SYSRISK012", "scenario must be a mapping", shown)
            )
            continue
        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str) or not scenario_id:
            diagnostics.append(
                Diagnostic("SYSRISK013", "scenario id is required", shown)
            )
            continue
        if scenario_id in scenario_ids:
            diagnostics.append(
                Diagnostic(
                    "SYSRISK014", f"duplicate scenario id {scenario_id!r}", shown
                )
            )
        scenario_ids.add(scenario_id)
        for phase in ("inherent", "residual"):
            score = scenario.get(phase)
            if not isinstance(score, Mapping):
                diagnostics.append(
                    Diagnostic(
                        "SYSRISK015",
                        f"scenario {scenario_id} {phase} must be a mapping",
                        shown,
                    )
                )
                continue
            impact = score.get("impact")
            likelihood = score.get("likelihood")
            tier = score.get("tier")
            if impact not in {1, 2, 3, 4} or likelihood not in {1, 2, 3, 4}:
                diagnostics.append(
                    Diagnostic(
                        "SYSRISK016",
                        f"scenario {scenario_id} {phase} scores must be 1 through 4",
                        shown,
                    )
                )
            elif tier != matrix_tier(impact, likelihood):
                diagnostics.append(
                    Diagnostic(
                        "SYSRISK017",
                        f"scenario {scenario_id} {phase} tier does not match matrix",
                        shown,
                    )
                )
            if tier in TIER_RANK:
                (inherent_tiers if phase == "inherent" else residual_tiers).append(tier)
        inherent = scenario.get("inherent", {})
        residual = scenario.get("residual", {})
        if (
            inherent.get("tier") in TIER_RANK
            and residual.get("tier") in TIER_RANK
            and TIER_RANK[residual["tier"]] < TIER_RANK[inherent["tier"]]
        ):
            verified = any(
                isinstance(control, Mapping)
                and control.get("effectiveness") == "verified"
                and isinstance(control.get("evidence"), list)
                and bool(control["evidence"])
                for control in scenario.get("controls", [])
            )
            if not verified:
                diagnostics.append(
                    Diagnostic(
                        "SYSRISK018",
                        f"scenario {scenario_id} reduces risk without verified evidence",
                        shown,
                    )
                )

    diagnostics.extend(
        _system_risk_summary_diagnostics(
            classification=classification,
            regulatory=regulatory,
            member_tiers=member_tiers,
            inherent_tiers=inherent_tiers,
            residual_tiers=residual_tiers,
            shown=shown,
        )
    )
    if assessment.get("status") != "approved":
        diagnostics.append(
            Diagnostic(
                "SYSRISK101",
                "assessment is not approved and cannot satisfy production readiness",
                shown,
                severity="warning",
            )
        )
    open_questions = payload.get("open_questions")
    if isinstance(open_questions, list) and open_questions:
        diagnostics.append(
            Diagnostic(
                "SYSRISK102",
                f"assessment has {len(open_questions)} open question(s)",
                shown,
                severity="warning",
            )
        )
    review_by = assessment.get("review_by")
    try:
        if isinstance(review_by, str) and date.fromisoformat(review_by) < date.today():
            diagnostics.append(
                Diagnostic("SYSRISK019", "assessment review date has expired", shown)
            )
    except ValueError:
        diagnostics.append(
            Diagnostic("SYSRISK020", "assessment.review_by must be an ISO date", shown)
        )
    return diagnostics


def _system_risk_summary_diagnostics(
    *,
    classification: Mapping[str, Any],
    regulatory: Mapping[str, Any],
    member_tiers: list[str],
    inherent_tiers: list[str],
    residual_tiers: list[str],
    shown: str,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    def maximum(tiers: list[str]) -> str | None:
        return max(tiers, key=TIER_RANK.__getitem__) if tiers else None

    expected_member = maximum(member_tiers)
    expected_inherent = maximum(inherent_tiers)
    expected_residual = maximum(residual_tiers)
    for field, expected in (
        ("maximum_member_tier", expected_member),
        ("maximum_inherent_tier", expected_inherent),
        ("maximum_residual_tier", expected_residual),
    ):
        if expected and classification.get(field) != expected:
            diagnostics.append(
                Diagnostic(
                    "SYSRISK021",
                    f"classification.{field} must summarize scenarios or members as {expected}",
                    shown,
                )
            )
    tier = classification.get("governance_tier")
    floor_candidates = [item for item in (expected_member, expected_inherent) if item]
    if tier in TIER_RANK and floor_candidates:
        floor = maximum(floor_candidates)
        if floor and TIER_RANK[tier] < TIER_RANK[floor]:
            diagnostics.append(
                Diagnostic(
                    "SYSRISK022",
                    f"governance tier cannot be below {floor}",
                    shown,
                )
            )
    decision = classification.get("decision")
    if regulatory.get("prohibited_use") is True and decision != "no_go":
        diagnostics.append(
            Diagnostic("SYSRISK023", "prohibited use requires no_go", shown)
        )
    if expected_residual == "critical" and decision != "no_go":
        diagnostics.append(
            Diagnostic("SYSRISK024", "critical residual risk requires no_go", shown)
        )
    return diagnostics
