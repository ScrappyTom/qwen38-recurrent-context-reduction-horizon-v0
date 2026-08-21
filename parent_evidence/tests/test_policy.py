from __future__ import annotations

import json
import unittest

from apparatus.canonical import load_json, sha256_bytes
from apparatus.constants import CELLS, ROOT
from apparatus.receipts import receipt_from_message


class PolicyTests(unittest.TestCase):
    def test_treatment_changes_only_declared_old_result_bodies(self) -> None:
        capacity = load_json(ROOT / "CAPACITY_PREFLIGHT.json")
        for row in capacity["cells"]:
            cell = row["cell"]
            control = load_json(ROOT / "preflight" / "packets" / cell / "control-raw-post-result-request.json")
            treated = load_json(ROOT / "preflight" / "packets" / cell / "cycle-01-delivery-request.json")
            changed = {index for index, (before, after) in enumerate(zip(control["messages"], treated["messages"], strict=True)) if before != after}
            self.assertEqual(changed, set(CELLS[cell]["expected_new_demoted_indices"]))
            self.assertNotIn(len(control["messages"]) - 1, changed)
            for index in changed:
                receipt = receipt_from_message(treated["messages"][index])
                self.assertIsNotNone(receipt)
                assert receipt is not None
                self.assertEqual(receipt["exact_message_sha256"], sha256_bytes(control["messages"][index]["content"].encode("utf-8")))
                self.assertFalse({"content", "summary", "relevance", "semantic_status"} & set(receipt))

    def test_existing_receipts_remain_unchanged(self) -> None:
        for cell in CELLS:
            control = load_json(ROOT / "preflight" / "packets" / cell / "control-raw-post-result-request.json")
            treated = load_json(ROOT / "preflight" / "packets" / cell / "cycle-01-delivery-request.json")
            existing = [index for index, message in enumerate(control["messages"]) if receipt_from_message(message) is not None]
            self.assertGreaterEqual(len(existing), 2)
            for index in existing:
                self.assertEqual(control["messages"][index], treated["messages"][index])

    def test_projection_savings_are_exactly_frozen(self) -> None:
        for cell, frozen in CELLS.items():
            receipt = load_json(ROOT / "preflight" / "packets" / cell / "projection-receipt.json")
            self.assertEqual([row["token_savings"] for row in receipt["changes"]], frozen["expected_new_token_savings"])
            self.assertEqual(receipt["before_tokens"] - receipt["after_tokens"], sum(frozen["expected_new_token_savings"]))


if __name__ == "__main__":
    unittest.main()
