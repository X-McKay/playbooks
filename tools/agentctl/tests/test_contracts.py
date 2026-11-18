from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import yaml
from agentctl.cli import main


class AgentSchemaTests(unittest.TestCase):
    def test_packaged_schema_exists(self) -> None:
        from importlib.resources import files

        resource = files("agentctl").joinpath("schemas/agent-spec.schema.json")
        self.assertTrue(resource.is_file())

    def test_malformed_metadata_is_reported_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(
                    main(
                        [
                            "scaffold",
                            "test-agent",
                            "--root",
                            temporary,
                            "--owner",
                            "platform",
                        ]
                    ),
                    0,
                )
            path = root / "src/acme_agents/agents/test_agent/agent.yaml"
            original = yaml.safe_load(path.read_text())
            original["description"] = "Answer bounded questions."
            for field, value in [
                ("risk_tier", []),
                ("execution_class", {}),
                ("version", 1),
                ("budgets", []),
                ("enabled_skills", [42]),
            ]:
                with self.subTest(field=field):
                    payload = json.loads(json.dumps(original))
                    payload["metadata"][field] = value
                    path.write_text(yaml.safe_dump(payload))
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        result = main(
                            ["validate", "--root", temporary, "--format", "json"]
                        )
                    self.assertEqual(result, 1)
                    diagnostics = json.loads(output.getvalue())["diagnostics"]
                    self.assertTrue(any(d["code"] == "AGENT041" for d in diagnostics))

    def test_documented_agent_specs_match_schema(self) -> None:
        import re
        from importlib.resources import files

        from jsonschema import Draft202012Validator

        schema_file = files("agentctl").joinpath("schemas/agent-spec.schema.json")
        self.assertTrue(schema_file.is_file())
        schema = json.loads(schema_file.read_text())
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        root = Path(__file__).resolve().parents[3]
        for relative in [
            "agent-playbook/03-agent-contract.md",
            "skills/design-pydantic-agent/references/examples.md",
        ]:
            with self.subTest(document=relative):
                content = (root / relative).read_text()
                spec = yaml.safe_load(
                    re.search(r"```yaml(?: agent-spec)?\n(.*?)```", content, re.S)[1]
                )
                self.assertEqual(list(validator.iter_errors(spec)), [])
