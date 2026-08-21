from __future__ import annotations

import unittest

from apparatus.canonical import load_json
from apparatus.constants import MAXIMUM_MEASURED_CALLS, MAX_NEW_CALLS_PER_SEED, ROOT
from apparatus.runner import canonical_action_key, local_nonchurn_window, short_cycle_thrash


class OutcomeTests(unittest.TestCase):
    def test_frozen_horizon_and_forecast(self) -> None:
        schedule = load_json(ROOT / "EXECUTION_SCHEDULE.json")
        self.assertEqual(MAX_NEW_CALLS_PER_SEED, 12)
        self.assertEqual(MAXIMUM_MEASURED_CALLS, 24)
        self.assertEqual(sum(row["maximum_new_model_calls"] for row in schedule["order"]), 24)
        forecast = load_json(ROOT / "FORECAST.json")
        self.assertEqual(sum(row["probability_percent"] for row in forecast["mutually_exclusive_outcomes_in_precedence_order"]), 100)

    def test_short_cycle_thrash_is_mechanical(self) -> None:
        a = {"action": "read_region", "region_id": "R001"}
        b = {"action": "read_region", "region_id": "R002"}
        history = [
            {"action_key": canonical_action_key(action), "acquisition": True, "candidate_unchanged": True}
            for action in (a, b, a, b)
        ]
        self.assertTrue(short_cycle_thrash(history))
        history[-1]["candidate_unchanged"] = False
        self.assertFalse(short_cycle_thrash(history))

    def test_outcome_labels_do_not_claim_semantic_unnecessariness(self) -> None:
        outcomes = load_json(ROOT / "OUTCOME_CLASSIFICATION.json")
        self.assertIn("not evidence", outcomes["interpretation_limit"])
        self.assertEqual(outcomes["terminal_classes_in_precedence_order"][0], "apparatus_censored")

    def test_local_nonchurn_window_is_distinct_from_convergence_claim(self) -> None:
        actions = [{"action": "read_region", "region_id": f"R00{index}"} for index in range(1, 5)]
        history = [
            {"action_key": canonical_action_key(action), "acquisition": True, "candidate_unchanged": True, "receipt_reopen": False}
            for action in actions
        ]
        self.assertTrue(local_nonchurn_window(history))
        outcomes = load_json(ROOT / "OUTCOME_CLASSIFICATION.json")
        self.assertIn("not proof", outcomes["convergence_limit"])


if __name__ == "__main__":
    unittest.main()
