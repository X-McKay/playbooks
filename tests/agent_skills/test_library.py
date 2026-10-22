"""Offline content-contract tests; these do not measure model or host behavior."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LIBRARY = ROOT / "development-skills"
COMMIT = "151fca01fbc609c5550c563c902946db540c2f4c"
NAMES = {
    "plan-agent-use", "specify-agent-contract", "design-trust-boundaries",
    "build-agent-evidence", "review-agent-readiness", "operate-agent-lifecycle",
    "author-and-admit-agent-skills", "draft-agent-implementation",
}
PACKET_FIELDS = {
    "schema_version", "skill", "run_id", "status", "source_commit", "inputs",
    "outputs", "assumptions", "blockers", "applicability", "evidence", "decision",
}
CASE_FIELDS = {
    "id", "split", "prompt", "expected_selection", "required_outputs",
    "forbidden_behavior", "assertions",
}


class LibraryTests(unittest.TestCase):
    def test_catalog_has_exact_unique_closure(self):
        catalog = json.loads((LIBRARY / "catalog.json").read_text())
        self.assertEqual(catalog["status"], "proposed")
        self.assertEqual(catalog["source_commit"], COMMIT)
        rows = catalog["skills"]
        self.assertEqual({row["name"] for row in rows}, NAMES)
        self.assertEqual(len(rows), len(NAMES))
        self.assertEqual(len({row["id"] for row in rows}), len(rows))
        for row in rows:
            self.assertEqual(row["path"], f"development-skills/{row['name']}")
            self.assertLessEqual(set(row["dependencies"]), NAMES - {row["name"]})
        workflow = next(row for row in rows if row["name"] == "draft-agent-implementation")
        self.assertEqual(set(workflow["dependencies"]), NAMES - {workflow["name"]})

    def test_all_packages_are_complete_and_shallow(self):
        files = {
            "SKILL.md", "references/owner-map.md", "references/packet-contract.md",
            "references/examples.md", "assets/packet-template.json",
            "assets/evaluation-cases.json",
        }
        for name in sorted(NAMES):
            with self.subTest(skill=name):
                package = LIBRARY / name
                for relative in files:
                    path = package / relative
                    self.assertTrue(path.is_file(), str(path))
                    data = path.read_text()
                    self.assertTrue(data.strip())
                    self.assertTrue(data.endswith("\n"), str(path))
                    self.assertNotIn("[TODO", data)
                body = (package / "SKILL.md").read_text()
                self.assertIn(f"name: {name}\n", body)
                self.assertLess(len(body.splitlines()), 500)
                self.assertIn("references/owner-map.md", body)
                self.assertIn("references/packet-contract.md", body)
                self.assertIn("references/examples.md", body)
                self.assertIn("assets/packet-template.json", body)
                self.assertFalse((package / "scripts").exists())
                self.assertFalse((package / "agents").exists())

    def test_draft_templates_never_fabricate_observations_or_authority(self):
        for name in sorted(NAMES):
            with self.subTest(skill=name):
                packet = json.loads((LIBRARY / name / "assets/packet-template.json").read_text())
                self.assertEqual(set(packet), PACKET_FIELDS)
                self.assertEqual(packet["schema_version"], "1.0")
                self.assertEqual(packet["skill"], name)
                self.assertEqual(packet["source_commit"], COMMIT)
                self.assertEqual(packet["status"], "draft")
                self.assertEqual(packet["decision"], {"recommendation": "not_assessed", "authorized": False})
                self.assertIsInstance(packet["inputs"], dict)
                self.assertIsInstance(packet["outputs"], dict)
                self.assertTrue(packet["outputs"], "Template must specify substantive output fields")
                for record in packet["evidence"]:
                    self.assertEqual(record["kind"], "planned")
                    self.assertEqual(record["status"], "not_run")
                for record in packet["applicability"]:
                    self.assertNotEqual(record["status"], "met")

    def test_case_fixtures_include_selection_safety_and_holdout(self):
        for name in sorted(NAMES):
            with self.subTest(skill=name):
                data = json.loads((LIBRARY / name / "assets/evaluation-cases.json").read_text())
                self.assertEqual(set(data), {"skill", "cases"})
                self.assertEqual(data["skill"], name)
                cases = data["cases"]
                self.assertGreaterEqual(len(cases), 6)
                self.assertEqual(len({c["id"] for c in cases}), len(cases))
                self.assertTrue(any(c["split"] == "holdout" for c in cases))
                self.assertEqual({c["expected_selection"] for c in cases}, {"select", "do_not_select", "clarify"})
                self.assertTrue(any(c["forbidden_behavior"] for c in cases))
                for case in cases:
                    self.assertEqual(set(case), CASE_FIELDS)
                    self.assertIn(case["split"], {"development", "holdout"})
                    self.assertTrue(case["prompt"].strip())
                    self.assertTrue(case["assertions"])

    def test_owner_links_are_pinned_not_legacy(self):
        for name in sorted(NAMES):
            with self.subTest(skill=name):
                data = (LIBRARY / name / "references/owner-map.md").read_text()
                self.assertIn(COMMIT, data)
                urls = re.findall(r"https://github\.com/X-McKay/playbooks/[^\s)]+", data)
                self.assertTrue(urls)
                for url in urls:
                    self.assertRegex(url, rf"/(?:blob|tree)/{COMMIT}(?:/|$)")
                    self.assertNotIn("/agent-playbook/", url)
                    self.assertNotIn("/multi-agent-playbook/", url)
                    self.assertNotIn("/core/", url)

    def test_schema_contract_matches_template_contract(self):
        schema = json.loads((LIBRARY / "contracts/packet.schema.json").read_text())
        self.assertEqual(set(schema["required"]), PACKET_FIELDS)
        self.assertFalse(schema["additionalProperties"])
        self.assertIs(schema["properties"]["decision"]["properties"]["authorized"]["const"], False)
        cases = json.loads((LIBRARY / "contracts/evaluation-cases.schema.json").read_text())
        self.assertEqual(set(cases["properties"]["cases"]["items"]["required"]), CASE_FIELDS)

    def test_profile_is_separate_and_has_no_permission_bypass(self):
        directory = ROOT / "implementation-profiles/python"
        profile = json.loads((directory / "profile.json").read_text())
        self.assertEqual(profile["id"], "python-local")
        self.assertEqual(profile["status"], "proposed")
        self.assertTrue(profile["required_artifacts"])
        self.assertTrue(profile["checks"])
        for check in profile["checks"]:
            self.assertIsInstance(check["argv"], list)
            self.assertGreater(check["timeout_seconds"], 0)
            self.assertTrue(all(isinstance(arg, str) for arg in check["argv"]))
            self.assertNotIn("--yolo", check["argv"])
            self.assertNotIn("--dangerously-skip-permissions", check["argv"])


if __name__ == "__main__":
    unittest.main()
