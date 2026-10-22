"""Regression coverage for the proposed Python profile's runnable local layout.

This fixture exercises a fresh source tree only.  It does not probe, configure, or
make claims about a native host, permissions, dependencies, or external effects.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


REPO = Path(__file__).resolve().parents[2]
PROFILE_PATH = REPO / "implementation-profiles/python/profile.json"
README_PATH = REPO / "implementation-profiles/python/README.md"
PACKAGE_NAME = "profile_fixture"
LAYERS = ("unit", "contract", "e2e", "security")
PROFILE_TOP_KEYS = {
    "id",
    "schema_version",
    "status",
    "language",
    "minimum_version",
    "required_artifacts",
    "checks",
    "forbidden_actions",
}
EXPECTED_CHECKS = [
    {
        "id": "compile",
        "argv": ["python3.11", "-m", "compileall", "-q", "src"],
        "timeout_seconds": 30,
    },
    {
        "id": "unit",
        "argv": ["python3.11", "-m", "unittest", "discover", "-s", "tests/unit", "-t", "."],
        "timeout_seconds": 60,
    },
    {
        "id": "contract",
        "argv": ["python3.11", "-m", "unittest", "discover", "-s", "tests/contract", "-t", "."],
        "timeout_seconds": 60,
    },
    {
        "id": "e2e",
        "argv": ["python3.11", "-m", "unittest", "discover", "-s", "tests/e2e", "-t", "."],
        "timeout_seconds": 120,
    },
    {
        "id": "security",
        "argv": ["python3.11", "-m", "unittest", "discover", "-s", "tests/security", "-t", "."],
        "timeout_seconds": 120,
    },
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class PythonProfileFeedbackTests(unittest.TestCase):
    """Keep source imports and test discovery reproducible without installation."""

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory(prefix="python-profile-feedback-")
        self.base = Path(self.temporary_directory.name)
        self.profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_documented_fixture(self, root: Path, *, package_markers: bool) -> None:
        """Create only the documented source-tree shape; do not install it."""
        write_text(
            root / "pyproject.toml",
            "[project]\n"
            'name = "profile-fixture"\n'
            'version = "0.0.0"\n'
            'requires-python = ">=3.11"\n',
        )
        write_text(root / "config.example.toml", "[fixture]\nmode = \"local\"\n")
        write_text(root / ".env.example", "PROFILE_FIXTURE_MODE=local\n")
        write_text(root / "src" / PACKAGE_NAME / "__init__.py", 'PACKAGE_NAME = "profile_fixture"\n')
        write_text(
            root / "src" / PACKAGE_NAME / "__main__.py",
            "import argparse\n"
            "import json\n"
            "from . import PACKAGE_NAME\n\n"
            "def main(argv=None):\n"
            "    parser = argparse.ArgumentParser(prog=PACKAGE_NAME)\n"
            "    parser.add_argument(\"--emit-json\", action=\"store_true\")\n"
            "    arguments = parser.parse_args(argv)\n"
            "    if arguments.emit_json:\n"
            "        print(json.dumps({\"event\": \"smoke\", \"package\": PACKAGE_NAME, \"schema_version\": \"1.0\", \"status\": \"ok\"}, sort_keys=True))\n"
            "    return 0\n\n"
            "if __name__ == \"__main__\":\n"
            "    raise SystemExit(main())\n",
        )
        tests = root / "tests"
        if package_markers:
            write_text(tests / "__init__.py", "")
        for layer in LAYERS:
            layer_root = tests / layer
            if package_markers:
                write_text(layer_root / "__init__.py", "")
            write_text(
                layer_root / f"test_{layer}.py",
                "import unittest\n"
                "from profile_fixture import PACKAGE_NAME\n\n"
                f"class {layer.title()}LayerTests(unittest.TestCase):\n"
                "    def test_source_package_is_importable(self):\n"
                "        self.assertEqual(PACKAGE_NAME, \"profile_fixture\")\n",
            )

    @staticmethod
    def runner_environment(root: Path) -> dict[str, str]:
        """The documented, intentionally minimal source-tree runner environment."""
        return {
            "PYTHONPATH": str(root / "src"),
            "PYTHONNOUSERSITE": "1",
        }

    def run_fixture(self, root: Path, argv: list[str], timeout_seconds: int) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            argv,
            cwd=root,
            env=self.runner_environment(root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout_seconds,
        )

    def test_profile_contract_and_documentation_preserve_runnable_literal_checks(self) -> None:
        self.assertEqual(set(self.profile), PROFILE_TOP_KEYS)
        self.assertEqual(self.profile["id"], "python-local")
        self.assertEqual(self.profile["status"], "proposed")
        self.assertEqual(self.profile["checks"], EXPECTED_CHECKS)

        readme = README_PATH.read_text(encoding="utf-8")
        self.assertIn("Status — proposed, non-normative implementation aid.", readme)
        self.assertIn('export PYTHONPATH="$PWD/src"', readme)
        self.assertIn("export PYTHONNOUSERSITE=1", readme)
        self.assertIn("tests/__init__.py", readme)
        for layer in LAYERS:
            self.assertIn(f"unittest discover -s tests/{layer} -t .", readme)

    def test_documented_layout_runs_cli_and_every_literal_profile_check(self) -> None:
        root = self.base / "documented-layout"
        self.write_documented_fixture(root, package_markers=True)

        # The current test environment is Python 3.12.  Keep profile.json's
        # literal python3.11 argv intact and substitute only this fixture runner.
        help_result = self.run_fixture(root, [sys.executable, "-m", PACKAGE_NAME, "--help"], 30)
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn("usage:", help_result.stdout)
        self.assertEqual(help_result.stderr, "")

        json_result = self.run_fixture(root, [sys.executable, "-m", PACKAGE_NAME, "--emit-json"], 30)
        self.assertEqual(json_result.returncode, 0, json_result.stderr)
        self.assertEqual(json_result.stderr, "")
        self.assertEqual(
            json.loads(json_result.stdout),
            {"event": "smoke", "package": PACKAGE_NAME, "schema_version": "1.0", "status": "ok"},
        )

        for check in self.profile["checks"]:
            with self.subTest(check=check["id"]):
                self.assertEqual(check["argv"][0], "python3.11")
                fixture_argv = [sys.executable, *check["argv"][1:]]
                deadline = check["timeout_seconds"]
                started = time.monotonic()
                completed = self.run_fixture(root, fixture_argv, deadline)
                elapsed = time.monotonic() - started
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
                self.assertLessEqual(elapsed, deadline, f"{check['id']} exceeded its profile deadline")
                if check["id"] != "compile":
                    self.assertIn("Ran 1 test", completed.stderr)
                    self.assertIn("OK", completed.stderr)

    def test_old_layout_without_package_markers_is_rejected_by_documented_discovery(self) -> None:
        root = self.base / "old-layout-without-markers"
        self.write_documented_fixture(root, package_markers=False)
        self.assertFalse((root / "tests" / "__init__.py").exists())
        for layer in LAYERS:
            self.assertFalse((root / "tests" / layer / "__init__.py").exists())

        result = self.run_fixture(
            root,
            [sys.executable, "-m", "unittest", "discover", "-s", "tests/unit", "-t", "."],
            30,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Start directory is not importable", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
