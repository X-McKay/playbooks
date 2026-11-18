from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import yaml
from agentctl.cli import main
from agentctl.systems import load_system_schema
from jsonschema import Draft202012Validator


class SystemContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self._scaffold_agent("planner-agent", "planner")
        self._scaffold_agent("worker-agent", "worker")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _scaffold_agent(self, name: str, purpose: str) -> None:
        result = main(
            [
                "scaffold",
                name,
                "--root",
                str(self.root),
                "--package",
                "sample_agents",
                "--owner",
                "agent-platform",
                "--execution-class",
                "durable",
                "--risk-tier",
                "medium",
            ]
        )
        self.assertEqual(result, 0)
        path = (
            self.root
            / "src"
            / "sample_agents"
            / "agents"
            / name.replace("-", "_")
            / "agent.yaml"
        )
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["description"] = f"Perform the bounded {purpose} role."
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    def _scaffold_system(self, *extra: str) -> Path:
        result = main(
            [
                "system",
                "scaffold",
                "research-system",
                "--root",
                str(self.root),
                "--package",
                "sample_agents",
                "--owner",
                "ai-platform",
                "--operational-owner",
                "research-operations",
                "--execution-class",
                "durable",
                "--risk-tier",
                "medium",
                "--member",
                "planner-agent:coordinator",
                "--member",
                "worker-agent:worker",
                *extra,
            ]
        )
        self.assertEqual(result, 0)
        path = self.root / "src/sample_agents/systems/research_system/system.yaml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["description"] = "Coordinate bounded planning and research work."
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        return path

    def test_schema_is_packaged_and_valid(self) -> None:
        Draft202012Validator.check_schema(load_system_schema())

    def test_scaffold_validate_graph_and_eval(self) -> None:
        path = self._scaffold_system()
        self.assertEqual(main(["system", "validate", "--root", str(self.root)]), 0)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(
                [
                    "system",
                    "graph",
                    str(path),
                    "--root",
                    str(self.root),
                    "--format",
                    "json",
                ]
            )
        self.assertEqual(result, 0)
        graph = json.loads(output.getvalue())
        self.assertEqual(graph["system"], "research-system")
        self.assertEqual(len(graph["members"]), 2)

        report = self.root / "artifacts/evals/research-system.json"
        self.assertEqual(
            main(
                [
                    "eval",
                    "run",
                    "research-system",
                    "--system",
                    "--root",
                    str(self.root),
                ]
            ),
            0,
        )
        payload = json.loads(report.read_text(encoding="utf-8"))
        self.assertEqual(
            payload["subject"], {"kind": "system", "name": "research-system"}
        )
        self.assertIn("git_commit", payload["provenance"])

    def test_validation_rejects_member_version_drift(self) -> None:
        path = self._scaffold_system()
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        payload["members"][0]["version"] = "9.9.9"
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        self.assertEqual(main(["system", "validate", "--root", str(self.root)]), 1)

    def test_dynamic_membership_scaffolds_admission_contracts(self) -> None:
        path = self._scaffold_system(
            "--dynamic-membership", "--topology", "dynamic_membership"
        )
        self.assertTrue((path.parent / "policies/registry.yaml").is_file())
        self.assertTrue((path.parent / "policies/admission.yaml").is_file())
        self.assertEqual(main(["system", "validate", "--root", str(self.root)]), 0)

    def test_system_rejection_matrix(self) -> None:
        path = self._scaffold_system()
        original = yaml.safe_load(path.read_text())
        cases = [
            (
                "execution floor",
                lambda p: p["metadata"].update(execution_class="ephemeral"),
                "SYSTEM022",
            ),
            (
                "governance floor",
                lambda p: p["metadata"].update(governance_tier="low"),
                "SYSTEM023",
            ),
            (
                "undeclared callee",
                lambda p: p["interactions"][0].update(to="unknown-agent"),
                "SYSTEM027",
            ),
            (
                "missing policy",
                lambda p: p["interactions"][0].update(policy="missing.yaml"),
                "SYSTEM029",
            ),
            ("malformed members", lambda p: p.update(members="invalid"), "SYSTEM003"),
            (
                "insufficient capacity",
                lambda p: p["limits"].update(max_agent_runs=1),
                "SYSTEM032",
            ),
        ]
        for label, mutate, code in cases:
            with self.subTest(case=label):
                payload = json.loads(json.dumps(original))
                mutate(payload)
                path.write_text(yaml.safe_dump(payload))
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    result = main(
                        [
                            "system",
                            "validate",
                            "--root",
                            str(self.root),
                            "--format",
                            "json",
                        ]
                    )
                self.assertEqual(result, 1)
                self.assertIn(
                    code,
                    {d["code"] for d in json.loads(output.getvalue())["diagnostics"]},
                )

    def test_malformed_system_risk_is_a_diagnostic(self) -> None:
        spec_path = self._scaffold_system()
        path = (
            self.root
            / yaml.safe_load(spec_path.read_text())["metadata"]["risk_assessment"]
        )
        original = yaml.safe_load(path.read_text())
        for field, value in [
            ("inherent", []),
            ("residual", {"impact": [], "likelihood": True, "tier": {}}),
            ("controls", {}),
        ]:
            with self.subTest(field=field):
                payload = json.loads(json.dumps(original))
                payload["scenarios"][0][field] = value
                path.write_text(yaml.safe_dump(payload))
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    result = main(
                        [
                            "system",
                            "validate",
                            "--root",
                            str(self.root),
                            "--format",
                            "json",
                        ]
                    )
                self.assertEqual(result, 1)
                self.assertIn(
                    "SYSRISK025",
                    {d["code"] for d in json.loads(output.getvalue())["diagnostics"]},
                )

    def test_invalid_member_metadata_stops_cross_member_checks(self) -> None:
        self._scaffold_system()
        path = self.root / "src/sample_agents/agents/planner_agent/agent.yaml"
        original = yaml.safe_load(path.read_text())
        for field, value in [
            ("execution_class", []),
            ("risk_tier", []),
            ("enabled_skills", [42]),
        ]:
            with self.subTest(field=field):
                payload = json.loads(json.dumps(original))
                payload["metadata"][field] = value
                path.write_text(yaml.safe_dump(payload))
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    result = main(
                        [
                            "system",
                            "validate",
                            "--root",
                            str(self.root),
                            "--format",
                            "json",
                        ]
                    )
                self.assertEqual(result, 1)
                self.assertIn(
                    "AGENT041",
                    {d["code"] for d in json.loads(output.getvalue())["diagnostics"]},
                )

    def test_integral_float_system_risk_scores_are_accepted(self) -> None:
        spec_path = self._scaffold_system()
        path = (
            self.root
            / yaml.safe_load(spec_path.read_text())["metadata"]["risk_assessment"]
        )
        risk = yaml.safe_load(path.read_text())
        for phase in ("inherent", "residual"):
            score = risk["scenarios"][0][phase]
            score["impact"] = float(score["impact"])
            score["likelihood"] = float(score["likelihood"])
        path.write_text(yaml.safe_dump(risk))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = main(
                ["system", "validate", "--root", str(self.root), "--format", "json"]
            )
        self.assertEqual(result, 0)
        self.assertTrue(json.loads(output.getvalue())["ok"])
