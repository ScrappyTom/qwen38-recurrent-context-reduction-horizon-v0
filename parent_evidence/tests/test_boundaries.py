from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from apparatus.constants import CELLS
from apparatus.environment import make_environment
from apparatus.predecessor import predecessor_assistant_message, predecessor_call


class BoundaryTests(unittest.TestCase):
    def test_predecessor_second_actions_are_exact(self) -> None:
        for cell, frozen in CELLS.items():
            with self.subTest(cell=cell):
                call = predecessor_call(cell, 2)
                self.assertEqual(call["action"]["action"], frozen["pending_action"])
                self.assertEqual(predecessor_assistant_message(cell)["content"], call["response"]["choices"][0]["message"]["content"])

    def test_pending_results_reconstruct_exactly(self) -> None:
        for cell, frozen in CELLS.items():
            with self.subTest(cell=cell), tempfile.TemporaryDirectory() as temporary:
                environment = make_environment(cell, Path(temporary))
                result = environment.execute(frozen["pending_action"])
                self.assertTrue(result["accepted"])
                self.assertEqual(result["sha256"], frozen["pending_result_sha256"])
                self.assertEqual(result["size_bytes"], frozen["pending_result_size_bytes"])

    def test_control_is_censored_and_treatment_fits(self) -> None:
        from apparatus.canonical import load_json
        from apparatus.constants import ROOT

        preflight = load_json(ROOT / "CAPACITY_PREFLIGHT.json")
        for row in preflight["cells"]:
            self.assertFalse(row["raw_control_after_pending_result"]["fits"])
            self.assertTrue(row["treatment_after_pending_result"]["fits"])
            self.assertEqual(row["treatment_after_pending_result"]["prompt_tokens"], CELLS[row["cell"]]["treated_post_result_prompt_tokens"])


if __name__ == "__main__":
    unittest.main()
