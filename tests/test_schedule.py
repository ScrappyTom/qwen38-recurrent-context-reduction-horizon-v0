from __future__ import annotations

import unittest

from apparatus.canonical import load_json
from apparatus.constants import MAXIMUM_MEASURED_CALLS, ROOT


class ScheduleTests(unittest.TestCase):
    def test_schedule_is_stable_and_bounded(self) -> None:
        schedule = load_json(ROOT / "EXECUTION_SCHEDULE.json")
        self.assertEqual([row["cell"] for row in schedule["order"]], ["s42-s1", "s314159-s1"])
        self.assertEqual(sum(row["maximum_new_model_calls"] for row in schedule["order"]), MAXIMUM_MEASURED_CALLS)
        self.assertEqual(schedule["retries"], 0)
        self.assertTrue(schedule["stop_whole_run_on_apparatus_invariant_failure"])


if __name__ == "__main__":
    unittest.main()
