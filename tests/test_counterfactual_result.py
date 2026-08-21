from __future__ import annotations

import unittest

from apparatus.canonical import load_json
from apparatus.constants import ROOT
from offline_audit.verify import verify


class CounterfactualResultTests(unittest.TestCase):
    def test_counterfactual_packets_and_run_custody_verify(self) -> None:
        receipt = verify(ROOT / "CONSTRUCTION_SET_COUNTERFACTUAL_AUDIT.json")
        self.assertTrue(receipt["passed"], receipt)
        self.assertEqual(receipt["scenario_count"], 42)
        self.assertEqual(receipt["packet_count"], 42)

    def test_key_capacity_dispositions_are_exact(self) -> None:
        result = load_json(ROOT / "CONSTRUCTION_SET_COUNTERFACTUAL_AUDIT.json")
        by_key = {
            (row["cell"], row["surface"], row["target_group"]): row
            for row in result["scenarios"]
        }
        for cell in ("s42-s1", "s314159-s1"):
            self.assertEqual(by_key[(cell, "fresh_phase", "governing_only")]["prompt_tokens"], 14173)
            self.assertEqual(
                by_key[(cell, "fresh_phase", "plus_r031_r033_tail")]["headroom_after_reserve"],
                2446,
            )
            self.assertEqual(
                by_key[(cell, "fresh_phase", "plus_r030_r033_top_level_tail")]["headroom_after_reserve"],
                -69,
            )
            self.assertFalse(by_key[(cell, "receipt_floor_then_restore", "governing_only")]["fits"])


if __name__ == "__main__":
    unittest.main()
