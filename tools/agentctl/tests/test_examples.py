from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


class OfflineExamplesTests(unittest.TestCase):
    def load_example(self, name):
        path = ROOT / "examples" / name / "main.py"
        self.assertTrue(path.is_file(), "runnable example is missing")
        spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    def test_single_agent_proposes_action_and_denies_cross_tenant_access(self):
        example = self.load_example("single-agent")
        result = example.run_case(tenant="acme", actor_tenant="acme")
        self.assertEqual(result.status, "action_proposed")
        self.assertEqual(result.ticket_id, "T-100")
        with self.assertRaises(PermissionError):
            example.run_case(tenant="other", actor_tenant="acme")

    def test_multi_agent_rejects_unsupported_review_and_bounds_requests(self):
        example = self.load_example("multi-agent")
        result = example.run_case(tenant="acme", actor_tenant="acme")
        self.assertEqual(result.status, "action_proposed")
        with self.assertRaises(PermissionError):
            example.run_case(tenant="other", actor_tenant="acme")
        with self.assertRaises(ValueError):
            example.run_case(tenant="acme", actor_tenant="acme", review_ticket="T-999")
        with self.assertRaises(ValueError):
            example.run_case(tenant="acme", actor_tenant="acme", request_limit=1)
