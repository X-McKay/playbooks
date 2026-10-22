#!/usr/bin/env python3
"""End-to-end tests for the standalone skillctl CLI.

Fixtures are deliberately self-contained so this suite remains useful while other
contributors populate the shared skill-library files.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "tools/agent_skills/skillctl.py"
BASELINE = "151fca01fbc609c5550c563c902946db540c2f4c"
NAMES = (
    "plan-agent-use",
    "specify-agent-contract",
    "design-trust-boundaries",
    "build-agent-evidence",
    "review-agent-readiness",
    "operate-agent-lifecycle",
    "author-and-admit-agent-skills",
    "draft-agent-implementation",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packet_template(name: str) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "skill": name,
        "run_id": "example-run",
        "status": "draft",
        "source_commit": BASELINE,
        "inputs": {},
        "outputs": {"draft_packet": "[Draft: name the packet artifact and tailored output fields.]"},
        "assumptions": [],
        "blockers": [],
        "applicability": [],
        "evidence": [],
        "decision": {"recommendation": "not_assessed", "authorized": False},
    }


def cases(name: str) -> dict[str, object]:
    selections = ("select", "do_not_select", "clarify", "select", "do_not_select", "select")
    values = []
    for number, selection in enumerate(selections):
        values.append({
            "id": f"case-{number}",
            "split": "holdout" if number == 5 else "development",
            "prompt": f"Fixture prompt {number} for {name}",
            "expected_selection": selection,
            "required_outputs": ["packet"],
            "forbidden_behavior": ["invent approval"],
            "assertions": ["records a fixture assertion"],
        })
    return {"skill": name, "cases": values}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def create_profile(root: Path) -> None:
    profile = {
        "id": "python-local",
        "schema_version": "1.0",
        "status": "proposed",
        "language": "python",
        "minimum_version": "3.11",
        "required_artifacts": ["pyproject.toml", "src", "tests/unit"],
        "checks": [{"id": "compile", "argv": ["python3.11", "-m", "compileall", "src"], "timeout_seconds": 30}],
        "forbidden_actions": ["Do not use a permission bypass."],
    }
    write_json(root / "implementation-profiles/python/profile.json", profile)
    (root / "implementation-profiles/python/README.md").write_text("Profile fixture.\n", encoding="utf-8")


def create_library(root: Path, *, catalog: bool = True, profile: bool = True) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "requirement-index.md").write_text("# Index\n\n- **REQ-01** — MUST.\n", encoding="utf-8")
    packages = root / "development-skills"
    for name in NAMES:
        package = packages / name
        (package / "references").mkdir(parents=True)
        (package / "assets").mkdir()
        (package / "SKILL.md").write_text(
            "---\n"
            f"name: {name}\n"
            "description: Use for deterministic fixture validation and decline unrelated runtime actions.\n"
            "metadata:\n"
            "  version: '0.1.0'\n"
            "  playbook_version: '0.5.0-draft.2'\n"
            f"  source_commit: {BASELINE}\n"
            "---\n\n"
            "# Fixture Skill\n\n"
            "Read [the owner map](references/owner-map.md) before producing an output.\n",
            encoding="utf-8",
        )
        (package / "references/owner-map.md").write_text(
            "# Owner map\n\nREQ-01 belongs to "
            f"[the canonical chapter](https://github.com/X-McKay/playbooks/blob/{BASELINE}/requirement-index.md).\n",
            encoding="utf-8",
        )
        (package / "references/packet-contract.md").write_text("# Packet contract\n\nUse typed evidence.\n", encoding="utf-8")
        (package / "references/examples.md").write_text("# Examples\n\nThis is a fixture.\n", encoding="utf-8")
        write_json(package / "assets/packet-template.json", packet_template(name))
        write_json(package / "assets/evaluation-cases.json", cases(name))
    if catalog:
        entries = []
        for name in NAMES:
            entries.append({"id": f"org.example.{name}", "name": name, "path": f"development-skills/{name}", "dependencies": []})
        write_json(packages / "catalog.json", {
            "schema_version": "1.0",
            "library_version": "0.1.0",
            "playbook_version": "0.5.0-draft.2",
            "source_commit": BASELINE,
            "status": "proposed",
            "description": "Fixture catalog; not an authorization record.",
            "skills": entries,
        })
    contracts = root / "development-skills/contracts"
    write_json(contracts / "packet.schema.json", {
        "$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False,
        "required": ["schema_version", "skill", "run_id", "status", "source_commit", "inputs", "outputs", "assumptions", "blockers", "applicability", "evidence", "decision"],
        "properties": {
            "skill": {"pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$", "maxLength": 64},
            "status": {"enum": ["draft", "needs_information", "blocked", "candidate_evidenced"]},
            "decision": {"properties": {"authorized": {"const": False}}},
            "evidence": {"items": {"allOf": [{"if": {"properties": {"kind": {"const": "planned"}}}, "then": {"properties": {"status": {"const": "not_run"}}}}]}},
        },
    })
    write_json(contracts / "evaluation-cases.schema.json", {
        "$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "additionalProperties": False,
        "required": ["skill", "cases"],
        "properties": {"cases": {"items": {"additionalProperties": False, "properties": {"split": {"enum": ["development", "holdout"]}, "expected_selection": {"enum": ["select", "do_not_select", "clarify"]}}}}},
    })
    if profile:
        create_profile(root)


class SkillctlCliTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory(prefix="skillctl-test-")
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

    def library(self) -> Path:
        root = self.base / "library"
        create_library(root)
        return root

    def make_event(self, workspace: Path, event: str, outcome: str = "pass") -> Path:
        self.receipt_number += 1
        evidence = workspace / "evidence"
        evidence.mkdir(parents=True, exist_ok=True)
        artifact = evidence / f"{event}-{self.receipt_number}.{'zip' if event == 'package' else 'txt'}"
        if event == "package":
            with zipfile.ZipFile(artifact, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("receipt.txt", "package receipt only; no archive execution\n")
        else:
            artifact.write_text(f"{event}:{outcome}:{self.receipt_number}\n", encoding="utf-8")
        event_file = evidence / f"{event}-{self.receipt_number}.json"
        write_json(event_file, {"event": event, "outcome": outcome, "artifact": f"evidence/{artifact.name}", "sha256": digest(artifact), "workspace": str(workspace)})
        return event_file

    def advance(self, state: Path, workspace: Path, event: str, outcome: str = "pass", *, ok: bool = True) -> dict[str, object]:
        return self.run_cli("workflow", "advance", str(state), "--event", event, "--evidence", str(self.make_event(workspace, event, outcome)), ok=ok)

    def test_validate_inventory_and_reproducible_package_cover_all_eight(self) -> None:
        root = self.library()
        validated = self.run_cli("validate", "--root", str(root))
        self.assertEqual([item["name"] for item in validated["packages"]], list(NAMES))
        self.assertEqual(len(validated["packages"]), 8)
        self.assertEqual(len(validated["library_digest"]), 64)

        inventory_path = self.base / "inventory.json"
        reported = self.run_cli("inventory", "--root", str(root), "--output", str(inventory_path))
        self.assertEqual(reported["library_digest"], json.loads(inventory_path.read_text(encoding="utf-8"))["library_digest"])
        self.run_cli("inventory", "--root", str(root), "--output", str(inventory_path), ok=False)

        first = self.base / "first.zip"
        second = self.base / "second.zip"
        packaged = self.run_cli("package", "--root", str(root), "--output", str(first), "--profile", "python-local")
        self.run_cli("package", "--root", str(root), "--output", str(second), "--profile", "python-local")
        self.assertEqual(packaged["profile"], "python-local")
        self.assertEqual(len(packaged["profile_digest"]), 64)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.run_cli("package", "--root", str(root), "--output", str(first), ok=False)
        with zipfile.ZipFile(first) as archive:
            names = archive.namelist()
            manifest = json.loads(archive.read("manifest.json"))
        self.assertEqual(len(names), len(NAMES) * 6 + 1 + 2 + 2 + 1)
        self.assertIn("plan-agent-use/SKILL.md", names)
        self.assertIn("catalog.json", names)
        self.assertIn("contracts/packet.schema.json", names)
        self.assertIn("implementation-profiles/python/profile.json", names)
        self.assertEqual({item["path"] for item in manifest["archive_files"]}, set(names) - {"manifest.json"})
        self.assertEqual(manifest["profile"]["id"], "python-local")
        self.assertTrue(all(item.date_time == (1980, 1, 1, 0, 0, 0) for item in zipfile.ZipFile(first).infolist()))
        verified = self.run_cli("verify-package", str(first))
        self.assertEqual(verified["library_digest"], validated["library_digest"])

    def test_inventory_digest_changes_for_any_resource_tamper(self) -> None:
        root = self.library()
        before = self.run_cli("inventory", "--root", str(root))["library_digest"]
        target = root / "development-skills/build-agent-evidence/references/examples.md"
        target.write_text(target.read_text(encoding="utf-8") + "Changed fixture bytes.\n", encoding="utf-8")
        after = self.run_cli("inventory", "--root", str(root))["library_digest"]
        self.assertNotEqual(before, after)

    def test_manifest_required_resource_check_is_not_a_proper_subset_test(self) -> None:
        root = self.library()
        archive_path = self.base / "valid.zip"
        self.run_cli("package", "--root", str(root), "--output", str(archive_path))
        with zipfile.ZipFile(archive_path) as archive:
            members = {info.filename: (info, archive.read(info)) for info in archive.infolist()}
        manifest = json.loads(members["manifest.json"][1])
        package = manifest["packages"][0]
        package["files"] = [item for item in package["files"] if item["path"] != "references/owner-map.md"]
        package["files"].append({"path": "assets/extra.json", "sha256": "0" * 64, "bytes": 0})
        package["files"].sort(key=lambda item: item["path"])
        members["manifest.json"] = (members["manifest.json"][0], json.dumps(manifest).encode())
        malformed = self.base / "missing-resource.zip"
        with zipfile.ZipFile(malformed, "w") as archive:
            for info, content in members.values():
                archive.writestr(info, content)
        error = self.run_cli("verify-package", str(malformed), ok=False)
        self.assertIn("missing required resources", error["error"])

    def test_catalog_is_required_and_rejects_duplicate_json_ids_and_cycles(self) -> None:
        root = self.base / "missing-catalog"
        create_library(root, catalog=False)
        error = self.run_cli("validate", "--root", str(root), ok=False)
        self.assertIn("catalog.json", error["error"])

        root = self.library()
        catalog = root / "development-skills/catalog.json"
        catalog.write_text('{"schema_version":"1.0","schema_version":"1.0"}\n', encoding="utf-8")
        error = self.run_cli("validate", "--root", str(root), ok=False)
        self.assertIn("duplicate JSON key", error["error"])

        shutil.rmtree(root)
        create_library(root)
        data = json.loads(catalog.read_text(encoding="utf-8"))
        data["skills"][1]["id"] = data["skills"][0]["id"]
        write_json(catalog, data)
        error = self.run_cli("validate", "--root", str(root), ok=False)
        self.assertIn("duplicate catalog qualified id", error["error"])

        shutil.rmtree(root)
        create_library(root)
        data = json.loads(catalog.read_text(encoding="utf-8"))
        data["skills"][0]["dependencies"] = [NAMES[1]]
        data["skills"][1]["dependencies"] = [NAMES[0]]
        write_json(catalog, data)
        error = self.run_cli("validate", "--root", str(root), ok=False)
        self.assertIn("cycle", error["error"])

    def test_package_manifest_verification_rejects_content_manifest_and_zip_name_tampering(self) -> None:
        root = self.library()
        package = self.base / "library.zip"
        self.run_cli("package", "--root", str(root), "--output", str(package), "--profile", "python-local")

        content_tamper = self.base / "content-tamper.zip"
        with zipfile.ZipFile(package) as original, zipfile.ZipFile(content_tamper, "w", compression=zipfile.ZIP_DEFLATED) as altered:
            for info in original.infolist():
                content = original.read(info.filename)
                if info.filename == "catalog.json":
                    content = b"{}\n"
                altered.writestr(info, content)
        error = self.run_cli("verify-package", str(content_tamper), ok=False)
        self.assertIn("archive_files", error["error"])

        manifest_tamper = self.base / "manifest-tamper.zip"
        with zipfile.ZipFile(package) as original, zipfile.ZipFile(manifest_tamper, "w", compression=zipfile.ZIP_DEFLATED) as altered:
            for info in original.infolist():
                content = original.read(info.filename)
                if info.filename == "manifest.json":
                    manifest = json.loads(content)
                    manifest["archive_files"][0]["sha256"] = "0" * 64
                    content = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
                altered.writestr(info, content)
        error = self.run_cli("verify-package", str(manifest_tamper), ok=False)
        self.assertIn("archive_files", error["error"])

        duplicate_and_traversal = self.base / "unsafe.zip"
        shutil.copyfile(package, duplicate_and_traversal)
        with zipfile.ZipFile(duplicate_and_traversal, "a", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("catalog.json", b"duplicate")
        error = self.run_cli("verify-package", str(duplicate_and_traversal), ok=False)
        self.assertIn("duplicate entry", error["error"])
        traversal = self.base / "traversal.zip"
        with zipfile.ZipFile(traversal, "w") as archive:
            archive.writestr("../escape", b"no")
        error = self.run_cli("verify-package", str(traversal), ok=False)
        self.assertIn("escapes its root", error["error"])

    def test_package_profile_bytes_are_optional_but_bound_when_selected(self) -> None:
        root = self.library()
        with_profile = self.base / "with-profile.zip"
        without_profile = self.base / "without-profile.zip"
        self.run_cli("package", "--root", str(root), "--output", str(with_profile), "--profile", "python-local")
        self.run_cli("package", "--root", str(root), "--output", str(without_profile))
        self.assertNotEqual(with_profile.read_bytes(), without_profile.read_bytes())
        self.assertEqual(self.run_cli("verify-package", str(with_profile))["profile"], "python-local")
        self.assertIsNone(self.run_cli("verify-package", str(without_profile))["profile"])
        with zipfile.ZipFile(without_profile) as archive:
            self.assertFalse(any(name.startswith("implementation-profiles/") for name in archive.namelist()))

    def test_package_refuses_symlinks_traversal_and_duplicate_frontmatter(self) -> None:
        root = self.library()
        package = root / "development-skills/plan-agent-use"
        outside = self.base / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        (package / "references/escape.md").symlink_to(outside)
        error = self.run_cli("validate", "--root", str(root), ok=False)
        self.assertIn("symlinks are not allowed", error["error"])

        shutil.rmtree(root)
        create_library(root)
        skill = root / "development-skills/plan-agent-use/SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "[bad](../outside.md)\n", encoding="utf-8")
        error = self.run_cli("validate", "--root", str(root), ok=False)
        self.assertIn("escapes its root", error["error"])

        shutil.rmtree(root)
        create_library(root)
        skill = root / "development-skills/plan-agent-use/SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8").replace("description:", "description: duplicate\ndescription:", 1), encoding="utf-8")
        error = self.run_cli("validate", "--root", str(root), ok=False)
        self.assertIn("duplicate frontmatter", error["error"])

    def test_check_packet_validates_observed_hash_and_readiness_blockers(self) -> None:
        workspace = self.base / "workspace"
        artifact = workspace / "evidence/result.txt"
        artifact.parent.mkdir(parents=True)
        artifact.write_text("observed result\n", encoding="utf-8")
        valid = packet_template("plan-agent-use")
        valid.update({
            "run_id": "run-1",
            "status": "candidate_evidenced",
            "outputs": {"packet": "evidence/result.txt"},
            "applicability": [{"requirement_id": "REQ-01", "status": "met", "rationale": "Observed fixture pass.", "evidence_ids": ["ev-1"]}],
            "evidence": [{"id": "ev-1", "kind": "observed", "status": "pass", "artifact": "evidence/result.txt", "sha256": digest(artifact)}],
            "decision": {"recommendation": "go", "authorized": False},
        })
        packet_path = self.base / "packet.json"
        write_json(packet_path, valid)
        checked = self.run_cli("check-packet", str(packet_path), "--workspace", str(workspace))
        self.assertEqual(checked["recommendation"], "go")

        valid["blockers"] = ["A required dependency is unavailable."]
        write_json(packet_path, valid)
        error = self.run_cli("check-packet", str(packet_path), "--workspace", str(workspace), ok=False)
        self.assertIn("blocked", error["error"])

        valid["blockers"] = []
        valid["evidence"][0]["sha256"] = "0" * 64
        write_json(packet_path, valid)
        error = self.run_cli("check-packet", str(packet_path), "--workspace", str(workspace), ok=False)
        self.assertIn("hash does not match", error["error"])

    def test_packet_gate_rejects_planned_pass_empty_go_duplicates_invalid_enums_and_escape(self) -> None:
        workspace = self.base / "packet-workspace"
        artifact = workspace / "evidence/result.txt"
        artifact.parent.mkdir(parents=True)
        artifact.write_text("pass\n", encoding="utf-8")
        packet = packet_template("plan-agent-use")
        packet.update({
            "status": "candidate_evidenced",
            "applicability": [{"requirement_id": "REQ-01", "status": "met", "rationale": "observed", "evidence_ids": ["ok"]}],
            "evidence": [{"id": "ok", "kind": "observed", "status": "pass", "artifact": "evidence/result.txt", "sha256": digest(artifact)}],
            "decision": {"recommendation": "go", "authorized": False},
        })
        packet_path = self.base / "strict-packet.json"
        write_json(packet_path, packet)
        self.run_cli("check-packet", str(packet_path), "--workspace", str(workspace))

        packet["evidence"][0].update({"kind": "planned", "status": "pass", "artifact": "", "sha256": ""})
        write_json(packet_path, packet)
        error = self.run_cli("check-packet", str(packet_path), "--workspace", str(workspace), ok=False)
        self.assertIn("planned evidence", error["error"])

        packet["evidence"][0] = {"id": "ok", "kind": "observed", "status": "pass", "artifact": "evidence/result.txt", "sha256": digest(artifact)}
        packet["applicability"].append(dict(packet["applicability"][0]))
        write_json(packet_path, packet)
        error = self.run_cli("check-packet", str(packet_path), "--workspace", str(workspace), ok=False)
        self.assertIn("duplicate applicability", error["error"])

        packet["applicability"] = []
        packet["evidence"] = []
        write_json(packet_path, packet)
        error = self.run_cli("check-packet", str(packet_path), "--workspace", str(workspace), ok=False)
        self.assertIn("candidate_evidenced requires", error["error"])

        packet["applicability"] = [{"requirement_id": "REQ-01", "status": "not_applicable", "rationale": "not in scope", "evidence_ids": []}]
        packet["evidence"] = [{"id": "ok", "kind": "observed", "status": "pass", "artifact": "evidence/result.txt", "sha256": digest(artifact)}]
        write_json(packet_path, packet)
        error = self.run_cli("check-packet", str(packet_path), "--workspace", str(workspace), ok=False)
        self.assertIn("at least one met", error["error"])

        packet["status"] = []
        write_json(packet_path, packet)
        error = self.run_cli("check-packet", str(packet_path), "--workspace", str(workspace), ok=False)
        self.assertIn("status is invalid", error["error"])

        packet["status"] = "candidate_evidenced"
        packet["applicability"] = [{"requirement_id": "REQ-01", "status": "met", "rationale": "observed", "evidence_ids": ["ok"]}]
        packet["evidence"][0]["artifact"] = "../escape.txt"
        write_json(packet_path, packet)
        error = self.run_cli("check-packet", str(packet_path), "--workspace", str(workspace), ok=False)
        self.assertIn("escapes its root", error["error"])

    def test_workflow_exact_sequence_allows_cleanup_then_retest(self) -> None:
        workspace = self.base / "workflow"
        (workspace / "src").mkdir(parents=True)
        source = workspace / "src/app.txt"
        source.write_text("before cleanup\n", encoding="utf-8")
        state = workspace / ".skillctl/state.json"
        state.parent.mkdir()
        initialized = self.run_cli("workflow", "init", "--output", str(state), "--max-repairs", "1")
        self.assertEqual(initialized["stage"], "initialized")
        self.assertEqual(self.advance(state, workspace, "plan")["stage"], "planned")
        self.assertEqual(self.advance(state, workspace, "implement")["stage"], "implemented")
        self.assertEqual(self.advance(state, workspace, "test")["stage"], "tested")
        self.advance(state, workspace, "retest", ok=False)

        # Cleanup intentionally updates source identity; full retest binds the cleaned source.
        source.write_text("after cleanup\n", encoding="utf-8")
        self.assertEqual(self.advance(state, workspace, "cleanup")["stage"], "cleaned")
        self.assertEqual(self.advance(state, workspace, "retest")["stage"], "retested")
        self.assertEqual(self.advance(state, workspace, "package")["stage"], "packaged")
        self.assertEqual(self.advance(state, workspace, "review_ready")["stage"], "review_ready")

    def test_workflow_replay_rejects_manual_stage_edits_and_requires_actual_package_archive(self) -> None:
        workspace = self.base / "replay"
        (workspace / "src").mkdir(parents=True)
        (workspace / "src/app.txt").write_text("fixture\n", encoding="utf-8")
        state = workspace / ".skillctl/state.json"
        state.parent.mkdir()
        initialized = self.run_cli("workflow", "init", "--output", str(state))
        self.assertEqual(initialized["max_repairs"], 2)
        tampered = json.loads(state.read_text(encoding="utf-8"))
        tampered["stage"] = "review_ready"
        write_json(state, tampered)
        error = self.advance(state, workspace, "plan", ok=False)
        self.assertIn("event history", error["error"])

        self.run_cli("workflow", "init", "--output", str(state), "--force")
        for event in ("plan", "implement", "test", "cleanup", "retest"):
            self.advance(state, workspace, event)
        bad_artifact = workspace / "evidence/not-an-archive.zip"
        bad_artifact.write_text("not a zip\n", encoding="utf-8")
        bad_receipt = workspace / "evidence/bad-package.json"
        write_json(bad_receipt, {"event": "package", "outcome": "pass", "artifact": "evidence/not-an-archive.zip", "sha256": digest(bad_artifact), "workspace": str(workspace)})
        error = self.run_cli("workflow", "advance", str(state), "--event", "package", "--evidence", str(bad_receipt), ok=False)
        self.assertIn("actual .zip archive", error["error"])

    def test_workflow_source_mutation_after_retest_requires_repair_and_retained_evidence_cannot_change(self) -> None:
        workspace = self.base / "workflow"
        (workspace / "src").mkdir(parents=True)
        source = workspace / "src/app.txt"
        source.write_text("initial\n", encoding="utf-8")
        state = workspace / ".skillctl/state.json"
        state.parent.mkdir()
        self.run_cli("workflow", "init", "--output", str(state), "--max-repairs", "1")
        for event in ("plan", "implement", "test", "cleanup", "retest"):
            self.advance(state, workspace, event)
        source.write_text("changed after retest\n", encoding="utf-8")
        error = self.advance(state, workspace, "package", ok=False)
        self.assertIn("active source identity changed", error["error"])
        invalidated = json.loads(state.read_text(encoding="utf-8"))
        self.assertEqual(invalidated["stage"], "implemented")
        self.assertIsNotNone(invalidated["blocked"])
        self.assertEqual(self.advance(state, workspace, "repair")["repairs"], 1)

        # The repair returns to implementation; complete the mandatory test/cleanup/retest sequence.
        for event in ("test", "cleanup", "retest"):
            self.advance(state, workspace, event)
        plan_artifact = workspace / "evidence/plan-1.txt"
        plan_artifact.write_text("tampered retained evidence\n", encoding="utf-8")
        error = self.advance(state, workspace, "package", ok=False)
        self.assertIn("retained evidence changed", error["error"])
        self.assertEqual(json.loads(state.read_text(encoding="utf-8"))["stage"], "retested")

    def test_completed_package_can_be_invalidated_repaired_and_packaged_again(self) -> None:
        workspace = self.base / "late-repair"
        (workspace / "src").mkdir(parents=True)
        source = workspace / "src/app.txt"
        source.write_text("first candidate\n", encoding="utf-8")
        state = workspace / ".skillctl/state.json"
        state.parent.mkdir()
        self.run_cli("workflow", "init", "--output", str(state), "--max-repairs", "1")
        for event in ("plan", "implement", "test", "cleanup", "retest", "package", "review_ready"):
            self.advance(state, workspace, event)
        source.write_text("changed candidate\n", encoding="utf-8")
        self.advance(state, workspace, "review_ready", ok=False)
        self.assertEqual(self.advance(state, workspace, "repair")["repairs"], 1)
        for event in ("test", "cleanup", "retest", "package", "review_ready"):
            result = self.advance(state, workspace, event)
        self.assertEqual(result["stage"], "review_ready")
        self.assertTrue(any(row["event"] == "package" and not row["valid"] for row in result["evidence"]))

    def test_workflow_block_events_are_retained_and_repairs_are_bounded(self) -> None:
        workspace = self.base / "blocked"
        (workspace / "src").mkdir(parents=True)
        (workspace / "src/app.txt").write_text("fixture\n", encoding="utf-8")
        state = workspace / ".skillctl/state.json"
        state.parent.mkdir()
        self.run_cli("workflow", "init", "--output", str(state), "--max-repairs", "1")
        self.advance(state, workspace, "plan")
        blocked = self.advance(state, workspace, "block", "block")
        self.assertEqual(blocked["stage"], "planned")
        self.advance(state, workspace, "implement", ok=False)
        repaired = self.advance(state, workspace, "repair")
        self.assertEqual(repaired["stage"], "implemented")
        self.assertEqual(repaired["events"][-1]["event"], "repair")
        self.advance(state, workspace, "repair", ok=False)
        saved = json.loads(state.read_text(encoding="utf-8"))
        self.assertEqual(saved["repairs"], 1)
        self.assertTrue(any(item["event"] == "block" for item in saved["events"]))
        # The denied extra repair must not make an otherwise valid ledger unreadable.
        self.assertEqual(self.advance(state, workspace, "test")["stage"], "tested")


if __name__ == "__main__":
    unittest.main()
