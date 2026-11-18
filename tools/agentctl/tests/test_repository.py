from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


class DocumentationChecksTests(unittest.TestCase):
    def checker(self):
        path = ROOT / "scripts/check_docs.py"
        self.assertTrue(path.is_file(), "repository documentation checker is missing")
        spec = importlib.util.spec_from_file_location("check_docs", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_links_and_anchors_ignore_code_examples(self):
        checker = self.checker()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "target.md").write_text(
                "# Target\n\n## Typed `Output`\n\n## Typed `Output`\n"
            )
            page = root / "README.md"
            page.write_text(
                "# Home\n\n[ok](target.md#typed-output-1)\n\n```text\n[example](missing.md)\n```\n"
            )
            self.assertEqual(checker.check_markdown(page, root), [])
            page.write_text(
                "# Home\n\n[bad](target.md#absent)\n\n[missing](missing.md)\n"
            )
            errors = checker.check_markdown(page, root)
            self.assertEqual(len(errors), 2)

    def test_markdown_quality_reports_heading_jumps_and_untyped_fences(self):
        checker = self.checker()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            page = root / "README.md"
            page.write_text("# Home\n\n### Skipped level\n\n```\nexample\n```\n")
            errors = checker.check_markdown(page, root)
            self.assertTrue(any("MD001" in error for error in errors))
            self.assertTrue(any("MD040" in error for error in errors))

    def test_nested_skill_reference_cannot_escape_package(self):
        import contextlib
        import io

        from agentctl.skills import validate_skills

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "check-agent"
            (package / "references").mkdir(parents=True)
            (root / "outside.md").write_text("# Outside\n")
            (package / "SKILL.md").write_text(
                "---\nname: check-agent\ndescription: Use when checking an agent.\n---\n\n# Check\n\n[Guide](references/guide.md)\n"
            )
            (package / "references/guide.md").write_text(
                "# Guide\n\n[Unavailable after installation](../../outside.md)\n"
            )
            with contextlib.redirect_stdout(io.StringIO()):
                result = validate_skills(root=root, paths=[package])
            self.assertEqual(result, 1)


class InstalledSkillTests(unittest.TestCase):
    def test_skill_packages_validate_outside_repository(self):
        import contextlib
        import io
        import shutil

        from agentctl.skills import validate_skills

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            packages = sorted((ROOT / "skills").glob("*/SKILL.md"))
            self.assertEqual(len(packages), 14)
            for manifest in packages:
                shutil.copytree(manifest.parent, root / manifest.parent.name)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(validate_skills(root=root, paths=[root]), 0)
