"""Offline typed support agent: propose an action without executing it."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_ai import Agent, models
from pydantic_ai.models.test import TestModel
from pydantic_ai.usage import UsageLimits


class Resolution(BaseModel):
    ticket_id: str
    status: Literal["action_proposed", "answered"]
    explanation: str


def run_case(*, tenant: str, actor_tenant: str) -> Resolution:
    if tenant != actor_tenant:
        raise PermissionError("Authenticated tenant does not own this case")
    # No live provider calls are permitted in this example.
    with models.override_allow_model_requests(False):
        agent = Agent(
            TestModel(
                call_tools=[],
                custom_output_args={
                    "ticket_id": "T-100",
                    "status": "action_proposed",
                    "explanation": "Propose a refund for a duplicate charge; do not execute it.",
                },
            ),
            output_type=Resolution,
            instructions="Use verified ticket information and propose actions only.",
        )
        result = agent.run_sync(
            "Review duplicate-charge ticket T-100.",
            usage_limits=UsageLimits(request_limit=1),
        )
    return result.output


def evaluate() -> dict:
    result = run_case(tenant="acme", actor_tenant="acme")
    denied = False
    try:
        run_case(tenant="other", actor_tenant="acme")
    except PermissionError:
        denied = True
    passed = result.ticket_id == "T-100" and result.status == "action_proposed"
    return {
        "schema_version": 1,
        "agent": "support-agent",
        "hard_gates": {"typed_proposal": passed, "cross_tenant_denied": denied},
        "metrics": {"task_success_rate": float(passed)},
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
