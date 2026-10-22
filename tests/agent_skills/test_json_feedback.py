"""Regression cases for PR #10's non-standard numeric-constant finding."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools/agent_skills/skillctl.py"


class JsonFeedbackTests(unittest.TestCase):
    def test_nonstandard_constants_are_rejected_but_quoted_strings_are_data(self):
        template = json.loads((ROOT / "development-skills/plan-agent-use/assets/packet-template.json").read_text())
        with tempfile.TemporaryDirectory(prefix="json-feedback-") as temporary:
            workspace = Path(temporary)
            packet = workspace / "packet.json"
            for token in ("NaN", "Infinity", "-Infinity"):
                with self.subTest(token=token):
                    template["inputs"] = {"temperature": "placeholder"}
                    packet.write_text(json.dumps(template).replace('"placeholder"', token) + "\n")
                    result = subprocess.run([sys.executable, str(TOOL), "check-packet", str(packet), "--workspace", temporary], capture_output=True, text=True, timeout=15)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertIn("non-standard JSON numeric constant", json.loads(result.stderr)["error"])
                    template["inputs"] = {"literal": token, "number": 0.5}
                    packet.write_text(json.dumps(template) + "\n")
                    valid = subprocess.run([sys.executable, str(TOOL), "check-packet", str(packet), "--workspace", temporary], capture_output=True, text=True, timeout=15)
                    self.assertEqual(valid.returncode, 0, valid.stderr)
                    self.assertTrue(json.loads(valid.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
