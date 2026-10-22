#!/usr/bin/env python3
"""Regressions for source-identity exclusions without weakening referenced files."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import unittest


HELPER_PATH = Path(__file__).with_name("test_workflow_feedback.py")
HELPER_SPEC = importlib.util.spec_from_file_location("workflow_feedback", HELPER_PATH)
assert HELPER_SPEC is not None and HELPER_SPEC.loader is not None
workflow_feedback = importlib.util.module_from_spec(HELPER_SPEC)
HELPER_SPEC.loader.exec_module(workflow_feedback)


class ExcludedMetadataFeedbackTests(unittest.TestCase):
    """Keep ignored metadata out of identity traversal, not referenced validation."""

    def setUp(self) -> None:
        # Compose the existing fixture rather than inheriting its TestCase: inherited
        # test_* methods would be discovered again and inflate this module's count.
        self.workflow = workflow_feedback.WorkflowReceiptIdentityFeedbackTests()
        self.workflow.setUp()

    def tearDown(self) -> None:
        self.workflow.tearDown()

    def git(self, *arguments: str, cwd: Path | None = None) -> None:
        command = [
            "git",
            "-c",
            "user.name=local-fixture",
            "-c",
            "user.email=local-fixture@example.invalid",
        ]
        if cwd is not None:
            command.extend(("-C", str(cwd)))
        completed = subprocess.run(
            [*command, *arguments],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=20,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def local_clone(self, name: str) -> tuple[Path, Path]:
        """Create a local clone whose loose Git objects are genuine hardlinks."""
        source = self.workflow.base / f"{name}-source"
        workspace = self.workflow.base / name
        (source / "src").mkdir(parents=True)
        (source / "src" / "app.py").write_text("print('fixture')\n", encoding="utf-8")
        self.git("init", "-q", str(source))
        self.git("add", "src/app.py", cwd=source)
        self.git("commit", "-q", "-m", "fixture", cwd=source)
        self.git("clone", "--local", "-q", str(source), str(workspace))

        objects = [path for path in (workspace / ".git" / "objects").rglob("*") if path.is_file()]
        self.assertTrue(objects, "the fixture clone must contain loose Git objects")
        self.assertTrue(
            any(path.stat(follow_symlinks=False).st_nlink > 1 for path in objects),
            "git clone --local must produce a hardlinked object for this regression",
        )

        state = workspace / ".skillctl" / "state.json"
        state.parent.mkdir()
        self.workflow.run_cli("workflow", "init", "--output", str(state))
        return workspace, state

    def advance_through(self, state: Path, workspace: Path, events: tuple[str, ...]) -> None:
        for event in events:
            self.workflow.advance(
                state,
                workspace,
                event,
                root_receipt=event in {"plan", "retest", "package", "review_ready"},
                explicit_workspace=True,
            )

    def receipt(self, workspace: Path, event: str, artifact: Path, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "event": event,
                    "outcome": "pass",
                    "artifact": artifact.relative_to(workspace).as_posix(),
                    "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(),
                    "workspace": str(workspace),
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    def test_local_git_clone_hardlinked_metadata_completes_full_workflow(self) -> None:
        workspace, state = self.local_clone("full-git-clone")
        _, result = self.workflow.complete_candidate(
            state,
            workspace,
            explicit_workspace=True,
            root_events={"plan", "retest", "package", "review_ready"},
        )

        self.assertEqual(result["stage"], "review_ready")
        self.assertTrue((workspace / ".git").is_dir(), "the clone metadata must remain in place")
        saved = json.loads(state.read_text(encoding="utf-8"))
        self.assertEqual(
            saved["source_identity"]["files"],
            [{"artifact": "src/app.py", "sha256": workflow_feedback.sha256(workspace / "src" / "app.py")}],
        )

    def test_ignored_cache_symlink_and_special_metadata_do_not_block_identity(self) -> None:
        for kind in ("symlink", "fifo"):
            with self.subTest(kind=kind):
                workspace, state = self.local_clone(f"ignored-cache-{kind}")
                cache = workspace / ".pytest_cache"
                cache.mkdir()
                if kind == "symlink":
                    target = cache / "target.txt"
                    target.write_text("ignored target\n", encoding="utf-8")
                    os.symlink(target.name, cache / "metadata-link")
                else:
                    os.mkfifo(cache / "metadata-fifo")

                self.advance_through(
                    state,
                    workspace,
                    ("plan", "implement", "test", "cleanup", "retest", "package", "review_ready"),
                )
                saved = json.loads(state.read_text(encoding="utf-8"))
                self.assertEqual(
                    saved["source_identity"]["files"],
                    [{"artifact": "src/app.py", "sha256": workflow_feedback.sha256(workspace / "src" / "app.py")}],
                )

    def test_included_source_hardlinks_and_symlinks_are_rejected(self) -> None:
        for kind in ("hardlink", "symlink"):
            with self.subTest(kind=kind):
                workspace, state = self.local_clone(f"included-{kind}")
                alias = workspace / "src" / "alias.py"
                if kind == "hardlink":
                    os.link(workspace / "src" / "app.py", alias)
                else:
                    os.symlink("app.py", alias)

                self.advance_through(state, workspace, ("plan", "implement"))
                error, _ = self.workflow.advance(
                    state,
                    workspace,
                    "test",
                    root_receipt=False,
                    explicit_workspace=True,
                    ok=False,
                )
                expected = "symlinks are not allowed" if kind == "symlink" else "hardlinked files are not allowed"
                self.assertIn(expected, error["error"])

    def test_referenced_excluded_evidence_and_receipts_reject_links(self) -> None:
        for subject, kind in (
            ("artifact", "symlink"),
            ("artifact", "hardlink"),
            ("receipt", "symlink"),
            ("receipt", "hardlink"),
        ):
            with self.subTest(subject=subject, kind=kind):
                workspace, state = self.local_clone(f"referenced-{subject}-{kind}")
                evidence = workspace / "evidence"
                evidence.mkdir()
                artifact = evidence / "plan.txt"
                artifact.write_text("plan evidence\n", encoding="utf-8")

                if subject == "artifact":
                    target = evidence / "artifact-target.txt"
                    target.write_text("artifact target\n", encoding="utf-8")
                    artifact.unlink()
                    if kind == "symlink":
                        os.symlink(target.name, artifact)
                    else:
                        os.link(target, artifact)
                    receipt = evidence / "plan.receipt.json"
                    self.receipt(workspace, "plan", artifact, receipt)
                else:
                    receipt_target = evidence / "receipt-target.json"
                    self.receipt(workspace, "plan", artifact, receipt_target)
                    receipt = evidence / "plan.receipt.json"
                    if kind == "symlink":
                        os.symlink(receipt_target.name, receipt)
                    else:
                        os.link(receipt_target, receipt)

                error = self.workflow.run_cli(
                    "workflow",
                    "advance",
                    str(state),
                    "--event",
                    "plan",
                    "--evidence",
                    str(receipt),
                    ok=False,
                )
                expected = "symlinks are not allowed" if kind == "symlink" else "hardlinked files are not allowed"
                self.assertIn(expected, error["error"])


if __name__ == "__main__":
    unittest.main()
