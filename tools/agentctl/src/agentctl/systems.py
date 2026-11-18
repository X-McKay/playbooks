from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import asdict
from pathlib import Path
from typing import Any

from agentctl.diagnostics import emit_diagnostics, relative_display
from agentctl.files import load_data
from agentctl.system_risk import validate_system_risk_file as validate_system_risk_file
from agentctl.system_validation import load_system_schema as load_system_schema
from agentctl.system_validation import system_schema_path as system_schema_path
from agentctl.system_validation import validate_system_file
from agentctl.system_validation import validate_systems as validate_systems


def explain_system(*, root: Path, path: Path, output_format: str = "text") -> int:
    root = root.resolve()
    resolved = path if path.is_absolute() else root / path
    diagnostics = validate_system_file(resolved, root=root)
    if any(item.severity == "error" for item in diagnostics):
        return emit_diagnostics(
            diagnostics,
            output_format=output_format,
            heading="Multi-agent system contract",
        )
    payload = load_data(resolved)
    if output_format == "json":
        print(
            json.dumps(
                {
                    "ok": True,
                    "path": relative_display(resolved, root),
                    "system": payload,
                    "diagnostics": [asdict(item) for item in diagnostics],
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        metadata = payload["metadata"]
        topology = payload["topology"]
        print(f"System: {payload['name']} {metadata['version']}")
        print(f"Owner: {metadata['owner']}")
        print(
            f"Execution: {metadata['execution_class']} · "
            f"Governance: {metadata['governance_tier']}"
        )
        print(
            f"Topology: {topology['type']} · "
            f"Members: {len(payload['members'])} · "
            f"Interactions: {len(payload['interactions'])}"
        )
        print(f"Dynamic membership: {topology['dynamic_membership']}")
        print(f"Source: {relative_display(resolved, root)}")
        if diagnostics:
            emit_diagnostics(
                diagnostics,
                output_format="text",
                heading="System notices",
            )
    return 0


def graph_system(*, root: Path, path: Path, output_format: str = "text") -> int:
    root = root.resolve()
    resolved = path if path.is_absolute() else root / path
    diagnostics = validate_system_file(resolved, root=root)
    if any(item.severity == "error" for item in diagnostics):
        return emit_diagnostics(
            diagnostics,
            output_format="json" if output_format == "json" else "text",
            heading="Multi-agent system graph",
        )
    payload = load_data(resolved)
    graph = _graph_payload(payload)
    if output_format == "json":
        print(json.dumps(graph, indent=2, sort_keys=True))
    elif output_format == "dot":
        print(f'digraph "{payload["name"]}" {{')
        for member in graph["members"]:
            print(
                f'  "{member["agent"]}" [label="{member["agent"]}\\n{member["role"]}"];'
            )
        orchestrator = graph["orchestrator"]
        print(f'  "{orchestrator}" [shape=box, style=rounded];')
        for edge in graph["interactions"]:
            print(
                f'  "{edge["from"]}" -> "{edge["to"]}" '
                f'[label="{edge["id"]} ({edge["mode"]})"];'
            )
        print("}")
    else:
        print(f"{payload['name']} [{graph['topology']}]")
        print(f"  orchestrator: {graph['orchestrator']}")
        for member in graph["members"]:
            required = "required" if member["required"] else "optional"
            print(
                f"  member: {member['agent']} {member['version']} "
                f"as {member['role']} ({required})"
            )
        for edge in graph["interactions"]:
            print(
                f"  edge: {edge['from']} -> {edge['to']} [{edge['mode']}; {edge['id']}]"
            )
    return 0


def _graph_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "system": payload["name"],
        "version": payload["metadata"]["version"],
        "topology": payload["topology"]["type"],
        "dynamic_membership": payload["topology"]["dynamic_membership"],
        "orchestrator": payload["topology"]["orchestrator"],
        "members": [
            {
                "agent": item["agent"],
                "version": item["version"],
                "role": item["role"],
                "required": item["required"],
            }
            for item in payload["members"]
        ],
        "interactions": [
            {
                "id": item["id"],
                "from": item["from"],
                "to": item["to"],
                "mode": item["mode"],
                "input_schema": item["input_schema"],
                "output_schema": item["output_schema"],
            }
            for item in payload["interactions"]
        ],
    }
