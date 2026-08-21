from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from apparatus.canonical import compact_json
from apparatus.constants import ROOT, TARGET_SHA256
from apparatus.runner import HttpRecord, run_cell


class _Count:
    def __init__(self, value: dict) -> None:
        self.value = value
        self.prompt_tokens = value["prompt_tokens"]

    def as_dict(self) -> dict:
        return dict(self.value)


class _StableTokenEndpoint:
    def __init__(self, capacity: dict) -> None:
        self.capacity = capacity
        self.chat_completion_calls = 0

    def count(self, messages: list[dict], kwargs: dict) -> _Count:
        return _Count(self.capacity)


def _response(action: dict) -> HttpRecord:
    payload = {
        "choices": [{"finish_reason": "stop", "message": {"role": "assistant", "content": compact_json(action)}}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2, "prompt_tokens_details": {"cached_tokens": 0}},
    }
    return HttpRecord(200, {}, json.dumps(payload, separators=(",", ":")).encode("utf-8"), 1, None)


class RunnerTests(unittest.TestCase):
    def test_mutation_does_not_stop_bounded_horizon(self) -> None:
        capacity_rows = json.loads((ROOT / "CAPACITY_PREFLIGHT.json").read_text(encoding="utf-8"))["cells"]
        capacity = next(row["horizon_start_after_pressure_policy"] for row in capacity_rows if row["cell"] == "s42-s1")
        actions = [
            {
                "action": "patch",
                "path": "QWEN_RELATION_ACTION_WORKING_MODEL.md",
                "old": "# Qwen relation-to-action working model",
                "new": "# Qwen relation-to-action working model (runner probe)",
                "expected_file_sha256": TARGET_SHA256,
            },
            {"action": "read_lines", "path": "QWEN_RELATION_ACTION_WORKING_MODEL.md", "start_line": 1, "end_line": 2},
            {"action": "read_region", "region_id": "R031"},
            {"action": "read_region", "region_id": "R032"},
        ]
        responses = [_response(action) for action in actions]
        with tempfile.TemporaryDirectory() as temporary, patch("apparatus.runner.MAX_NEW_CALLS_PER_SEED", 4), patch(
            "apparatus.runner.post_chat", side_effect=responses
        ):
            result = run_cell(
                "s42-s1",
                1,
                Path(temporary),
                "http://not-used.invalid",
                _StableTokenEndpoint(capacity),
            )
        self.assertEqual(result["model_calls"], 4)
        self.assertEqual(result["admitted_mutations"], 1)
        self.assertEqual(result["endpoint"], "model_call_limit_result_custodied_not_delivered")
        self.assertNotEqual(result["initial_candidate_id"], result["final_candidate_id"])


if __name__ == "__main__":
    unittest.main()
