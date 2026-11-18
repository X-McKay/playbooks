"""Offline producer/reviewer composition with deterministic admission checks."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_ai import Agent, models
from pydantic_ai.models.test import TestModel
from pydantic_ai.usage import RunUsage, UsageLimits


class Investigation(BaseModel):
    ticket_id: str
    evidence: str


class Review(BaseModel):
    ticket_id: str
    status: Literal["action_proposed", "escalated"]


def run_case(
    *,
    tenant: str,
    actor_tenant: str,
    review_ticket: str = "T-100",
    request_limit: int = 2,
) -> Review:
    if tenant != actor_tenant:
        raise PermissionError("Authenticated tenant does not own this case")
    if request_limit < 2:
        raise ValueError("The fixed two-agent graph needs two requests")
    usage = RunUsage()
    limits = UsageLimits(request_limit=request_limit)
    with models.override_allow_model_requests(False):
        investigator = Agent(
            TestModel(
                call_tools=[],
                custom_output_args={
                    "ticket_id": "T-100",
                    "evidence": "Two charges share the same invoice.",
                },
            ),
            output_type=Investigation,
        )
        reviewer = Agent(
            TestModel(
                call_tools=[],
                custom_output_args={
                    "ticket_id": review_ticket,
                    "status": "action_proposed",
                },
            ),
            output_type=Review,
        )
        investigation = investigator.run_sync(
            "Investigate ticket T-100.", usage=usage, usage_limits=limits
        ).output
        review = reviewer.run_sync(
            investigation.model_dump_json(), usage=usage, usage_limits=limits
        ).output
    if review.ticket_id != investigation.ticket_id:
        raise ValueError("Reviewer output does not match the investigated ticket")
    return review


def evaluate() -> dict:
    result = run_case(tenant="acme", actor_tenant="acme")
    gates = {
        "typed_proposal": result.ticket_id == "T-100"
        and result.status == "action_proposed"
    }
    for name, arguments, error in [
        (
            "cross_tenant_denied",
            {"tenant": "other", "actor_tenant": "acme"},
            PermissionError,
        ),
        (
            "mismatched_review_denied",
            {"tenant": "acme", "actor_tenant": "acme", "review_ticket": "T-999"},
            ValueError,
        ),
        (
            "budget_enforced",
            {"tenant": "acme", "actor_tenant": "acme", "request_limit": 1},
            ValueError,
        ),
    ]:
        gates[name] = False
        try:
            run_case(**arguments)
        except error:
            gates[name] = True
    return {
        "schema_version": 1,
        "subject": {"kind": "system", "name": "support-system"},
        "hard_gates": gates,
        "metrics": {"task_success_rate": float(all(gates.values()))},
        "provenance": {
            "dataset_versions": ["offline-support-v1"],
            "evaluator_versions": ["assertions-v1"],
            "model": "TestModel",
            "run_count": 1,
        },
    }


if __name__ == "__main__":
    report = evaluate()
    if destination := os.environ.get("AGENTCTL_REPORT_PATH"):
        Path(destination).write_text(json.dumps(report, indent=2) + "\n")
    else:
        print(json.dumps(report, indent=2))
    raise SystemExit(0 if all(report["hard_gates"].values()) else 1)
