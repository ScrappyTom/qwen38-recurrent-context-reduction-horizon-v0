from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from apparatus.canonical import compact_json, sha256_bytes
from apparatus.constants import SOURCE_PATHS
from apparatus.environment import make_environment
from apparatus.predecessor import parent_boundary_objects


class EnvironmentTests(unittest.TestCase):
    def test_historical_reopen_returns_exact_result(self) -> None:
        cell = "s42-s1"
        parent = parent_boundary_objects(cell)
        action = json.loads(parent["request"]["messages"][8]["content"])
        expected = json.loads(parent["request"]["messages"][9]["content"])["result"]
        with tempfile.TemporaryDirectory() as temporary:
            environment = make_environment(cell, Path(temporary))
            self.assertEqual(compact_json(environment.execute(action)), compact_json(expected))

    def test_four_governing_documents_are_novel_readable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            environment = make_environment("s314159-s1", Path(temporary))
            for path in SOURCE_PATHS:
                result = environment.execute({"action": "repo_read", "path": path})
                self.assertTrue(result["accepted"])
                self.assertEqual(result["source_commit"], "f8c93e5ad33c8dd235c418df6561ba022d9077fb")
                self.assertEqual(sha256_bytes(result["content"].encode("utf-8")), environment.source_records[path]["copied_sha256"])

    def test_unmaterialized_repo_surface_is_integrity_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            environment = make_environment("s42-s1", Path(temporary))
            result = environment.execute({"action": "repo_history", "path": SOURCE_PATHS[0]})
            self.assertFalse(result["accepted"])
            self.assertEqual(result["error"]["code"], "source_surface_not_materialized")

    def test_mutation_and_submission_bind_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            environment = make_environment("s42-s1", Path(temporary))
            read = environment.execute({"action": "read_lines", "path": "QWEN_RELATION_ACTION_WORKING_MODEL.md", "start_line": 1, "end_line": 6})
            mutation = environment.execute({"action": "patch", "path": "QWEN_RELATION_ACTION_WORKING_MODEL.md", "old": "# Qwen relation-to-action working model", "new": "# Qwen relation-to-action working model (probe)", "expected_file_sha256": read["file_sha256"]})
            self.assertTrue(mutation["accepted"])
            self.assertNotEqual(mutation["candidate_before"], mutation["candidate_after"])
            submission = environment.execute({"action": "submit"})
            self.assertTrue(submission["accepted"])
            self.assertEqual(submission["candidate_id"], mutation["candidate_after"])


if __name__ == "__main__":
    unittest.main()
