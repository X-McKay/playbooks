"""Exercise scaffold → validate → offline eval → passing/failing release gates."""

from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
from pathlib import Path

import yaml
from agentctl.cli import main

EXAMPLES = Path(__file__).resolve().parent


def verify(kind: str) -> None:
    with tempfile.TemporaryDirectory(prefix="playbooks-example-") as temporary:
        root = Path(temporary)
        members = (
            ["support-agent"]
            if kind == "agent"
            else ["investigator-agent", "reviewer-agent"]
        )
        for name in members:
            with contextlib.redirect_stdout(io.StringIO()):
                result = main(
                    [
                        "scaffold",
                        name,
                        "--root",
                        temporary,
                        "--owner",
                        "example-maintainer",
                    ]
                )
            if result != 0:
                raise RuntimeError("Agent scaffold failed")
            path = (
                root / "src/acme_agents/agents" / name.replace("-", "_") / "agent.yaml"
            )
            spec = yaml.safe_load(path.read_text())
            spec["description"] = "Propose a resolution for bounded support cases."
            path.write_text(yaml.safe_dump(spec))
        subject = "support-agent"
        if kind == "system":
            subject = "support-system"
            with contextlib.redirect_stdout(io.StringIO()):
                result = main(
                    [
                        "system",
                        "scaffold",
                        subject,
                        "--root",
                        temporary,
                        "--owner",
                        "example-maintainer",
                        "--operational-owner",
                        "example-maintainer",
                        "--execution-class",
                        "ephemeral",
                        "--risk-tier",
                        "low",
                        "--topology",
                        "producer_reviewer",
                        "--member",
                        "investigator-agent:producer",
                        "--member",
                        "reviewer-agent:reviewer",
                    ]
                )
            if result != 0:
                raise RuntimeError("System scaffold failed")
            path = root / "src/acme_agents/systems/support_system/system.yaml"
            spec = yaml.safe_load(path.read_text())
            spec["description"] = (
                "Investigate a case and review the proposed resolution."
            )
            path.write_text(yaml.safe_dump(spec))
        with contextlib.redirect_stdout(io.StringIO()):
            result = main(
                (["validate"] if kind == "agent" else ["system", "validate"])
                + ["--root", temporary]
            )
        if result != 0:
            raise RuntimeError("Example contract validation failed")
        script = (
            EXAMPLES
            / ("single-agent" if kind == "agent" else "multi-agent")
            / "main.py"
        )
        report = root / "report.json"
        arguments = [
            "eval",
            "run",
            subject,
            "--root",
            temporary,
            "--report",
            str(report),
        ]
        if kind == "system":
            arguments.append("--system")
        arguments += ["--command", sys.executable, str(script)]
        if main(arguments) != 0:
            raise RuntimeError("Offline example eval failed")
        policy = script.parent / "release-policy.yaml"
        release = ["release", "check", "--report", str(report), "--policy", str(policy)]
        if main(release) != 0:
            raise RuntimeError("Passing example was rejected")
        payload = json.loads(report.read_text())
        payload["hard_gates"]["typed_proposal"] = False
        report.write_text(json.dumps(payload))
        with contextlib.redirect_stdout(io.StringIO()):
            result = main(release)
        if result != 1:
            raise RuntimeError("Failed hard gate did not block release")
        print(
            f"{kind}: scaffold, validation, offline eval, release acceptance/rejection passed."
        )


if __name__ == "__main__":
    os.environ["PYDANTIC_AI_NO_BANNER"] = "1"
    verify("agent")
    verify("system")
