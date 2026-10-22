#!/usr/bin/env python3
"""Regression coverage for archive contract and resource-inventory closure."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from typing import Any, Callable


REPO = Path(__file__).resolve().parents[2]
TOOL = Path(os.environ.get("SKILLCTL_TOOL", REPO / "tools/agent_skills/skillctl.py"))
PACKAGE_NAME = "plan-agent-use"


def manifest_record(path: str, content: bytes) -> dict[str, Any]:
    return {
        "path": path,
        "sha256": hashlib.sha256(content).hexdigest(),
        "bytes": len(content),
    }


def package_digest(files: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for item in sorted(files, key=lambda record: record["path"]):
        digest.update(item["path"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(item["sha256"].encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def library_digest(packages: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for package in packages:
        digest.update(package["name"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(package["digest"].encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def deterministic_member(archive: zipfile.ZipFile, name: str, content: bytes) -> None:
    """Write a verifier-acceptable regular-file ZIP member with stable metadata."""
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.flag_bits = 0
    archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


class ArchiveClosureFeedbackTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory(prefix="archive-closure-")
        self.base = Path(self.tempdir.name)
        self.root = self.base / "library"
        shutil.copytree(REPO / "development-skills", self.root / "development-skills")
        shutil.copy2(REPO / "requirement-index.md", self.root / "requirement-index.md")
        # An optional, supported resource lets the manifest inventory omit one
        # archive member while declaring a different supported resource.
        (self.root / "development-skills" / PACKAGE_NAME / "references" / "optional.md").write_text(
            "# Optional fixture resource\n", encoding="utf-8"
        )
        self.valid = self.base / "valid.zip"
        self.run_cli("package", "--root", str(self.root), "--output", str(self.valid))

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_cli(self, *arguments: str, ok: bool = True) -> dict[str, Any]:
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

    def mutate(self, target: Path, mutate: Callable[[dict[str, bytes], dict[str, Any]], None]) -> None:
        with zipfile.ZipFile(self.valid) as archive:
            members = {info.filename: archive.read(info) for info in archive.infolist()}
        manifest = json.loads(members["manifest.json"])
        mutate(members, manifest)
        manifest["archive_files"] = sorted(
            (manifest_record(path, content) for path, content in members.items() if path != "manifest.json"),
            key=lambda item: item["path"],
        )
        members["manifest.json"] = (
            json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        )
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(members):
                deterministic_member(archive, path, members[path])

    def assert_rejected(self, name: str, mutate: Callable[[dict[str, bytes], dict[str, Any]], None], expected: str) -> None:
        target = self.base / f"{name}.zip"
        self.mutate(target, mutate)
        error = self.run_cli("verify-package", str(target), ok=False)
        self.assertIn(expected, error["error"])

    def test_valid_round_trip(self) -> None:
        verified = self.run_cli("verify-package", str(self.valid))
        self.assertEqual(len(verified["library_digest"]), 64)

    def test_source_packaging_requires_the_complete_contract_set(self) -> None:
        (self.root / "development-skills/contracts/packet.schema.json").unlink()
        error = self.run_cli(
            "package", "--root", str(self.root), "--output", str(self.base / "incomplete.zip"), ok=False
        )
        self.assertIn("contract resources", error["error"])

    def test_rejects_one_or_all_removed_mandatory_contracts(self) -> None:
        self.assert_rejected(
            "without-packet-contract",
            lambda members, manifest: members.pop("contracts/packet.schema.json"),
            "contracts",
        )
        self.assert_rejected(
            "without-contracts",
            lambda members, manifest: [members.pop(path) for path in list(members) if path.startswith("contracts/")],
            "contracts",
        )

    def test_rejects_empty_or_malformed_contract_content(self) -> None:
        def empty_schema(members: dict[str, bytes], manifest: dict[str, Any]) -> None:
            members["contracts/packet.schema.json"] = b"{}\n"

        def malformed_json(members: dict[str, bytes], manifest: dict[str, Any]) -> None:
            members["contracts/evaluation-cases.schema.json"] = b"{ not valid JSON\n"

        self.assert_rejected("empty-contract", empty_schema, "packet schema")
        self.assert_rejected("malformed-contract", malformed_json, "invalid JSON")

    def test_rejects_globally_inventoried_but_undeclared_resource_members(self) -> None:
        for relative, content in (
            ("references/uninventoried.md", b"# Not declared\n"),
            ("scripts/uninventoried.py", b"print('not declared')\n"),
        ):
            with self.subTest(resource=relative):
                self.assert_rejected(
                    relative.replace("/", "-"),
                    lambda members, manifest, relative=relative, content=content: members.__setitem__(
                        f"{PACKAGE_NAME}/{relative}", content
                    ),
                    "resource",
                )

    def test_rejects_unassigned_root_member(self) -> None:
        self.assert_rejected(
            "unassigned-root-member",
            lambda members, manifest: members.__setitem__("unassigned.txt", b"not assigned\n"),
            "unassigned",
        )

    def test_rejects_inventory_that_omits_one_member_and_substitutes_an_extra(self) -> None:
        def swap_descriptor_member(members: dict[str, bytes], manifest: dict[str, Any]) -> None:
            extra = f"{PACKAGE_NAME}/references/inventoried-extra.md"
            members[extra] = b"# Declared replacement\n"
            package = next(item for item in manifest["packages"] if item["name"] == PACKAGE_NAME)
            package["files"] = [
                item for item in package["files"] if item["path"] != "references/optional.md"
            ]
            package["files"].append(manifest_record("references/inventoried-extra.md", members[extra]))
            package["files"].sort(key=lambda item: item["path"])
            package["digest"] = package_digest(package["files"])
            manifest["library_digest"] = library_digest(manifest["packages"])

        self.assert_rejected("omitted-plus-extra", swap_descriptor_member, "exactly inventory")

    def test_rejects_catalog_metadata_that_does_not_match_catalog_json(self) -> None:
        def alter_catalog_metadata(members: dict[str, bytes], manifest: dict[str, Any]) -> None:
            manifest["catalog"]["library_version"] = "mismatched"

        self.assert_rejected("catalog-metadata-mismatch", alter_catalog_metadata, "catalog metadata")


if __name__ == "__main__":
    unittest.main()
