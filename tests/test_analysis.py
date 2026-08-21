import unittest
from pathlib import Path

from apparatus.analyze import analyze


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs" / "2026-08-20-sealed-horizon-run-v0"


@unittest.skipUnless(RUN.is_dir(), "measured run is not materialized")
class MeasuredAnalysisTests(unittest.TestCase):
    def test_measured_reducer_matches_raw_run(self) -> None:
        result = analyze(RUN)
        aggregate = result["aggregate"]
        self.assertEqual(aggregate["model_calls"], 24)
        self.assertEqual(aggregate["admitted_actions"], 23)
        self.assertEqual(aggregate["recurrent_pressure_events_resolved"], 17)
        self.assertEqual(aggregate["results_delivered_to_new_decisions_including_frozen_pending"], 24)
        self.assertEqual(aggregate["exact_reopens"], 15)
        self.assertEqual(aggregate["other_acquisitions"], 9)
        self.assertEqual(aggregate["mutations"], 0)
        self.assertEqual(aggregate["submissions"], 0)
        self.assertEqual(aggregate["candidate_changes"], 0)
        self.assertEqual(aggregate["cells_with_formal_short_cycle_thrash"], 0)
        self.assertEqual(aggregate["cells_with_local_nonchurn_window"], 2)
        self.assertEqual(aggregate["recurrent_tokens_recovered"], 41339)
        self.assertEqual(aggregate["all_tokens_recovered_including_initial"], 44491)
        self.assertEqual(aggregate["prompt_tokens"], 477994)
        self.assertEqual(aggregate["completion_tokens"], 935)


if __name__ == "__main__":
    unittest.main()
