from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from apparatus.constants import CELLS
from apparatus.environment import make_environment
from apparatus.predecessor import donor_assistant_message, donor_call, donor_result_message


class BoundaryTests(unittest.TestCase):
    def test_direct_predecessor_third_actions_are_exact(self) -> None:
        for cell, frozen in CELLS.items():
            with self.subTest(cell=cell):
                call = donor_call(cell, 3)
                self.assertEqual(call["action"]["action"], frozen["pending_action"])
                self.assertEqual(donor_assistant_message(cell)["content"], call["response"]["choices"][0]["message"]["content"])

    def test_pending_results_reconstruct_exactly(self) -> None:
        for cell, frozen in CELLS.items():
            with self.subTest(cell=cell), tempfile.TemporaryDirectory() as temporary:
                environment = make_environment(cell, Path(temporary))
                result = environment.execute(frozen["pending_action"])
                self.assertTrue(result["accepted"])
                reconstructed = environment.result_message(frozen["pending_action"], frozen["pending_action_id"], result)
                self.assertEqual(reconstructed, donor_result_message(cell))

    def test_control_is_censored_and_treatment_fits(self) -> None:
        from apparatus.canonical import load_json
        from apparatus.constants import ROOT

        preflight = load_json(ROOT / "CAPACITY_PREFLIGHT.json")
        for row in preflight["cells"]:
            self.assertFalse(row["raw_control_after_pending_result"]["fits"])
            self.assertTrue(row["horizon_start_after_pressure_policy"]["fits"])
            self.assertEqual(row["direct_predecessor_call_03"]["prompt_tokens"], CELLS[row["cell"]]["donor_prompt_tokens"])
            self.assertEqual(row["raw_control_after_pending_result"]["prompt_tokens"], CELLS[row["cell"]]["raw_post_result_prompt_tokens"])


if __name__ == "__main__":
    unittest.main()
