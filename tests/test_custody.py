from __future__ import annotations

import unittest

from apparatus.canonical import load_json, sha256_file
from apparatus.constants import DONOR_ROOT, PREDECESSOR_COMMIT, PREDECESSOR_RUN, ROOT


class CustodyTests(unittest.TestCase):
    def test_predecessor_materialization_is_exact(self) -> None:
        receipt = load_json(ROOT / "provenance" / "PREDECESSOR_MATERIALIZATION_RECEIPT.json")
        self.assertEqual(receipt["predecessor_commit"], PREDECESSOR_COMMIT)
        self.assertTrue(receipt["all_byte_equivalent"])
        self.assertEqual(receipt["file_count"], 255)
        for row in receipt["files"]:
            path = ROOT / row["copied_path"]
            self.assertTrue(path.is_file())
            self.assertEqual(path.stat().st_size, row["copied_size_bytes"])
            self.assertEqual(sha256_file(path), row["copied_sha256"])

    def test_imported_predecessor_verification_and_replay_passed(self) -> None:
        verification = load_json(DONOR_ROOT / "POSTRUN_VERIFICATION.json")
        replay = load_json(DONOR_ROOT / PREDECESSOR_RUN / "replay" / "REPLAY.json")
        self.assertTrue(verification["passed"])
        self.assertTrue(replay["passed"])
        self.assertEqual(replay["observed_model_calls"], 6)


if __name__ == "__main__":
    unittest.main()
