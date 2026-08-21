from __future__ import annotations

import json
import unittest

from apparatus.canonical import compact_json, load_json, sha256_bytes
from apparatus.constants import CELLS, ROOT
from apparatus.receipts import receipt_from_message
from apparatus.runner import _catalog_exact_results, resolve_receipt_reopen


class PolicyTests(unittest.TestCase):
    def test_treatment_changes_only_declared_old_result_bodies(self) -> None:
        capacity = load_json(ROOT / "CAPACITY_PREFLIGHT.json")
        for row in capacity["cells"]:
            cell = row["cell"]
            control = load_json(ROOT / "preflight" / "packets" / cell / "control-raw-post-result-request.json")
            treated = load_json(ROOT / "preflight" / "packets" / cell / "horizon-start-request.json")
            changed = {index for index, (before, after) in enumerate(zip(control["messages"], treated["messages"], strict=True)) if before != after}
            row = next(item for item in capacity["cells"] if item["cell"] == cell)
            self.assertEqual(changed, set(row["newly_demoted_result_indices"]))
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
            treated = load_json(ROOT / "preflight" / "packets" / cell / "horizon-start-request.json")
            existing = [index for index, message in enumerate(control["messages"]) if receipt_from_message(message) is not None]
            self.assertGreaterEqual(len(existing), 2)
            for index in existing:
                self.assertEqual(control["messages"][index], treated["messages"][index])

    def test_projection_savings_are_exactly_frozen(self) -> None:
        for cell in CELLS:
            receipt = load_json(ROOT / "preflight" / "packets" / cell / "projection-receipt.json")
            savings = [row["token_savings"] for row in receipt["changes"]]
            self.assertTrue(all(value > 0 for value in savings))
            self.assertEqual(receipt["before_tokens"] - receipt["after_tokens"], sum(savings))
            self.assertTrue(receipt["deterministic_second_render_equal"])

    def test_every_start_receipt_has_exact_backing(self) -> None:
        for cell in CELLS:
            treated = load_json(ROOT / "preflight" / "packets" / cell / "horizon-start-request.json")
            index = load_json(ROOT / "preflight" / "packets" / cell / "exact-backing-index.json")
            by_action = {}
            for row in index["receipts"]:
                by_action.setdefault(compact_json(row["reopen_action"]), []).append(row)
            for key, rows in by_action.items():
                self.assertTrue(all(row["equivalent_backing_locations"] for row in rows), key)

    def test_every_start_reopen_action_resolves_exactly(self) -> None:
        catalog = _catalog_exact_results()
        for cell in CELLS:
            treated = load_json(ROOT / "preflight" / "packets" / cell / "horizon-start-request.json")
            actions = {
                compact_json(receipt["reopen_action"]): receipt["reopen_action"]
                for message in treated["messages"]
                if (receipt := receipt_from_message(message)) is not None
            }
            for key, action in actions.items():
                with self.subTest(cell=cell, action=key):
                    result = resolve_receipt_reopen(action, treated["messages"], catalog)
                    self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main()
