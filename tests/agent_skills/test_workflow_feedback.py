#!/usr/bin/env python3
"""Regression tests for workflow receipt identity feedback."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "tools/agent_skills/skillctl.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


class WorkflowReceiptIdentityFeedbackTests(unittest.TestCase):
    """Exercise receipt exclusions without weakening independent hash checks."""

    maxDiff = None

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory(prefix="workflow-receipt-feedback-")
        self.base = Path(self.tempdir.name)
        self.receipt_number = 0

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_cli(self, *arguments: str, ok: bool = True) -> dict[str, object]:
        completed = subprocess.run(
            [sys.executable, str(TOOL), *arguments],
            cwd=REPO,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=20,
        )
        if ok:
            self.assertEqual(completed.returncode, 0, completed.stderr)
            return json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
        error = json.loads(completed.stderr)
        self.assertFalse(error["ok"])
        return error

    def make_receipt(
        self,
        workspace: Path,
        event: str,
        *,
        root_receipt: bool,
        explicit_workspace: bool,
    ) -> Path:
        """Make unique, retained receipts while keeping artifacts out of source."""
        self.receipt_number += 1
        evidence = workspace / "evidence"
        evidence.mkdir(parents=True, exist_ok=True)
        suffix = "zip" if event == "package" else "txt"
        artifact = evidence / f"{event}-{self.receipt_number}.{suffix}"
        if event == "package":
            with zipfile.ZipFile(artifact, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("receipt.txt", "fixture package; static only\n")
        else:
            artifact.write_text(f"{event}:{self.receipt_number}\n", encoding="utf-8")
        receipt = (workspace if root_receipt else evidence) / f"{event}-{self.receipt_number}.receipt.json"
        data: dict[str, object] = {
            "event": event,
            "outcome": "pass",
            "artifact": f"evidence/{artifact.name}",
            "sha256": sha256(artifact),
        }
        if explicit_workspace:
            data["workspace"] = str(workspace)
        write_json(receipt, data)
        return receipt

    def advance(
        self,
        state: Path,
        workspace: Path,
        event: str,
        *,
        root_receipt: bool,
        explicit_workspace: bool,
        ok: bool = True,
    ) -> tuple[dict[str, object], Path]:
        receipt = self.make_receipt(
            workspace,
            event,
            root_receipt=root_receipt,
            explicit_workspace=explicit_workspace,
        )
        result = self.run_cli(
            "workflow",
            "advance",
            str(state),
            "--event",
            event,
            "--evidence",
            str(receipt),
            ok=ok,
        )
        return result, receipt

    def initialize(self, name: str, *, max_repairs: int = 2) -> tuple[Path, Path]:
        workspace = self.base / name
        (workspace / "src").mkdir(parents=True)
        (workspace / "src/app.py").write_text("print('fixture')\n", encoding="utf-8")
        state = workspace / ".skillctl/state.json"
        state.parent.mkdir()
        self.run_cli("workflow", "init", "--output", str(state), "--max-repairs", str(max_repairs))
        return workspace, state

    def complete_candidate(
        self,
        state: Path,
        workspace: Path,
        *,
        explicit_workspace: bool,
        root_events: set[str],
    ) -> tuple[dict[str, Path], dict[str, object]]:
        receipts: dict[str, Path] = {}
        result: dict[str, object] = {}
        for event in ("plan", "implement", "test", "cleanup", "retest", "package", "review_ready"):
            result, receipts[event] = self.advance(
                state,
                workspace,
                event,
                root_receipt=event in root_events,
                explicit_workspace=explicit_workspace,
            )
        return receipts, result

    def test_mixed_root_and_excluded_receipts_complete_full_sequence_with_workspace(self) -> None:
        workspace, state = self.initialize("explicit-workspace")
        receipts, result = self.complete_candidate(
            state,
            workspace,
            explicit_workspace=True,
            root_events={"plan", "retest", "package", "review_ready"},
        )
        self.assertEqual(result["stage"], "review_ready")
        saved = json.loads(state.read_text(encoding="utf-8"))
        self.assertEqual(saved["workspace"], str(workspace))
        snapshot = saved["source_identity"]["files"]
        self.assertEqual(snapshot, [{"artifact": "src/app.py", "sha256": sha256(workspace / "src/app.py")}])
        for event in ("plan", "retest", "package", "review_ready"):
            self.assertEqual(receipts[event].parent, workspace)
            self.assertNotIn(receipts[event].name, {item["artifact"] for item in snapshot})

    def test_root_receipts_default_workspace_to_their_parent(self) -> None:
        workspace, state = self.initialize("implicit-workspace")
        receipts, result = self.complete_candidate(
            state,
            workspace,
            explicit_workspace=False,
            root_events={"plan", "implement", "test", "cleanup", "retest", "package", "review_ready"},
        )
        self.assertEqual(result["stage"], "review_ready")
        saved = json.loads(state.read_text(encoding="utf-8"))
        self.assertEqual(saved["workspace"], str(workspace))
        self.assertTrue(all(path.parent == workspace for path in receipts.values()))
        self.assertEqual(
            saved["source_identity"]["files"],
            [{"artifact": "src/app.py", "sha256": sha256(workspace / "src/app.py")}],
        )

    def test_late_repair_still_detects_added_root_code_and_tampered_invalidated_receipt(self) -> None:
        workspace, state = self.initialize("late-repair", max_repairs=1)
        receipts, result = self.complete_candidate(
            state,
            workspace,
            explicit_workspace=True,
            root_events={"plan", "retest", "package", "review_ready"},
        )
        self.assertEqual(result["stage"], "review_ready")

        # This is active code at the workspace root, not a retained receipt.
        (workspace / "new_root_module.py").write_text("VALUE = 1\n", encoding="utf-8")
        error, _ = self.advance(
            state,
            workspace,
            "review_ready",
            root_receipt=True,
            explicit_workspace=True,
            ok=False,
        )
        self.assertIn("active source identity changed after retest", error["error"])
        invalidated = json.loads(state.read_text(encoding="utf-8"))
        self.assertEqual(invalidated["stage"], "implemented")
        self.assertTrue(next(item for item in invalidated["evidence"] if item["event"] == "retest")["valid"] is False)

        repaired, _ = self.advance(
            state,
            workspace,
            "repair",
            root_receipt=False,
            explicit_workspace=True,
        )
        self.assertEqual(repaired["stage"], "implemented")
        for event in ("test", "cleanup", "retest"):
            self.advance(
                state,
                workspace,
                event,
                root_receipt=event == "retest",
                explicit_workspace=True,
            )

        # The root retest receipt was invalidated by the late source change, but its
        # independently recorded hash must remain protected.
        receipts["retest"].write_text(receipts["retest"].read_text(encoding="utf-8") + "tampered\n", encoding="utf-8")
        error, _ = self.advance(
            state,
            workspace,
            "package",
            root_receipt=True,
            explicit_workspace=True,
            ok=False,
        )
        self.assertIn("workflow evidence record changed", error["error"])
        self.assertEqual(json.loads(state.read_text(encoding="utf-8"))["stage"], "retested")


if __name__ == "__main__":
    unittest.main()
