"""Regression cases for conditional LIFECYCLE-03 and LIFECYCLE-06 applicability."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "development-skills/operate-agent-lifecycle"
TEMPLATE = SKILL / "assets/packet-template.json"
SCHEMA = ROOT / "development-skills/contracts/packet.schema.json"
TOOL = ROOT / "tools/agent_skills/skillctl.py"


class LifecycleFeedbackTests(unittest.TestCase):
    def load_template(self):
        return json.loads(TEMPLATE.read_text(encoding="utf-8"))

    def applicability_entry(self, entries, requirement_id):
        return next(entry for entry in entries if entry["requirement_id"] == requirement_id)

    def test_template_is_accepted_and_matches_shared_packet_schema(self):
        packet = self.load_template()
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(set(packet), set(schema["required"]))
        self.assertIn(packet["status"], schema["properties"]["status"]["enum"])
        self.assertEqual(packet["decision"]["authorized"], schema["properties"]["decision"]["properties"]["authorized"]["const"])
        entry_schema = schema["properties"]["applicability"]["items"]["properties"]
        for entry in packet["applicability"]:
            self.assertIn(entry["status"], entry_schema["status"]["enum"])
            self.assertTrue(entry["rationale"])
            self.assertIsInstance(entry["evidence_ids"], list)
        with tempfile.TemporaryDirectory(prefix="lifecycle-feedback-") as temporary:
            result = subprocess.run(
                [sys.executable, str(TOOL), "check-packet", str(TEMPLATE), "--workspace", temporary],
                capture_output=True,
                text=True,
                timeout=15,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)["ok"])

    def test_template_leaves_conditional_triggers_unresolved_without_claiming_absence(self):
        entries = self.load_template()["applicability"]
        for requirement_id, absent_claim in (
            ("LIFECYCLE-03", "no containment"),
            ("LIFECYCLE-06", "no deprecation"),
        ):
            with self.subTest(requirement_id=requirement_id):
                entry = self.applicability_entry(entries, requirement_id)
                rationale = entry["rationale"].lower()
                self.assertEqual(entry["status"], "unmet")
                self.assertIn("trigger is unresolved", rationale)
                self.assertIn("not_applicable", rationale)
                self.assertNotIn(absent_claim, rationale)

    def test_fictional_bounded_example_uses_reasoned_non_trigger_and_separate_preparedness(self):
        text = (SKILL / "references/examples.md").read_text(encoding="utf-8")
        section = text.split("## 7. Conditional recovery and retirement: bounded non-trigger", 1)[1]
        match = re.search(r"```json\n(.*?)\n```", section, re.DOTALL)
        self.assertIsNotNone(match)
        example = json.loads(match.group(1))
        entries = example["applicability"]
        lifecycle_01 = self.applicability_entry(entries, "LIFECYCLE-01")
        lifecycle_03 = self.applicability_entry(entries, "LIFECYCLE-03")
        lifecycle_06 = self.applicability_entry(entries, "LIFECYCLE-06")
        self.assertEqual(lifecycle_01["status"], "unmet")
        self.assertEqual(lifecycle_01["evidence_ids"], ["planned-lifecycle-preparedness"])
        self.assertEqual(lifecycle_03["status"], "not_applicable")
        self.assertIn("fictional bounded planning case", lifecycle_03["rationale"].lower())
        self.assertIn("pending resumption after containment", lifecycle_03["rationale"].lower())
        self.assertEqual(lifecycle_06["status"], "not_applicable")
        self.assertIn("fictional bounded planning case", lifecycle_06["rationale"].lower())
        self.assertIn("neither deprecated nor retired", lifecycle_06["rationale"].lower())
        preparedness = example["preparedness_assessment"]
        self.assertEqual(preparedness["support_ownership"]["requirement_id"], "LIFECYCLE-01")
        self.assertEqual(preparedness["recovery_runbook"]["status"], "planned")
        self.assertEqual(preparedness["retirement_handoff_runbook"]["status"], "planned")
        self.assertEqual(example["evidence"][0], {
            "id": "planned-lifecycle-preparedness",
            "kind": "planned",
            "status": "not_run",
            "artifact": "",
            "sha256": "",
        })
        self.assertEqual(example["decision"], {"recommendation": "not_assessed", "authorized": False})

    def test_trigger_present_but_pending_or_unverified_is_unmet(self):
        contract = (SKILL / "references/packet-contract.md").read_text(encoding="utf-8")
        self.assertIn("If the trigger exists, recovery or retirement work that is planned, pending, or unverified is `unmet`.", contract)
        self.assertIn("required recovery record is verified", contract)
        self.assertIn("every required handoff action is\n  verified", contract)


if __name__ == "__main__":
    unittest.main()
