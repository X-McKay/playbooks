"""Shared identifiers and policy ordering for playbook contracts."""

import re

EXECUTION_CLASSES = ("ephemeral", "durable", "human_governed")
EXECUTION_RANK = {name: rank for rank, name in enumerate(EXECUTION_CLASSES)}
EFFECT_MINIMUM = {
    "read": "ephemeral",
    "write_reversible": "durable",
    "write_consequential": "human_governed",
}
RETRY_SAFETY = {"safe", "idempotency_key_required", "unsafe"}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
REQUIRED_BUDGETS = {
    "max_requests",
    "max_input_tokens",
    "max_output_tokens",
    "max_tool_calls",
    "max_cost_usd",
}

PACKAGE_PATTERN = re.compile(r"^[a-z_][a-z0-9_]*$")
TIERS = ("low", "medium", "high", "critical")
TIER_RANK = {tier: rank for rank, tier in enumerate(TIERS)}

RISK_TIERS = set(TIERS)
