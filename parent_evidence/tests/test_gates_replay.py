from __future__ import annotations

import json
import inspect
import unittest

from apparatus.canonical import canonical_json_bytes, load_json, sha256_file
from apparatus.constants import MAXIMUM_MEASURED_CALLS, ROOT, STUDY_ID
from apparatus.replay import replay_preflight
from apparatus.runner import HttpRecord, authorization_errors, parse_response, run_experiment


class GateReplayTests(unittest.TestCase):
    def test_authorization_requires_exact_scope(self) -> None:
        lock_sha = sha256_file(ROOT / "provenance" / "SOURCE_LOCK.json")
        good = {"schema_version": "measured-inference-authorization-v0", "study_id": STUDY_ID, "approved": True, "source_lock_sha256": lock_sha, "maximum_model_calls": MAXIMUM_MEASURED_CALLS, "retries": 0, "approval_statement": "authorized test"}
        self.assertEqual(authorization_errors(good, lock_sha), [])
        bad = dict(good, maximum_model_calls=MAXIMUM_MEASURED_CALLS + 1)
        self.assertTrue(authorization_errors(bad, lock_sha))

    def test_request_remains_unapproved(self) -> None:
        request = load_json(ROOT / "AUTHORIZATION_REQUEST.json")
        self.assertFalse(request["approved"])
        self.assertTrue(request["user_approval_required"])

    def test_provider_action_parser(self) -> None:
        payload = {"choices": [{"finish_reason": "stop", "message": {"role": "assistant", "content": '{"action":"read_region","region_id":"R033"}'}}], "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}}
        parsed = parse_response(HttpRecord(200, {}, canonical_json_bytes(payload), 1, None), "s42-s1")
        self.assertTrue(parsed["valid"])
        self.assertEqual(parsed["action"]["region_id"], "R033")

    def test_fresh_preflight_replay(self) -> None:
        receipt = replay_preflight()
        self.assertTrue(receipt["passed"], receipt)

    def test_clean_gate_precedes_run_tree_creation(self) -> None:
        source = inspect.getsource(run_experiment)
        self.assertLess(source.index("head = require_clean_head()"), source.index('(run_root / "model").mkdir'))


if __name__ == "__main__":
    unittest.main()
