import unittest
from pathlib import Path

from apparatus.analyze import analyze


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs" / "2026-08-20-sealed-run-v1"


@unittest.skipUnless(RUN.is_dir(), "measured run is not materialized")
class MeasuredAnalysisTests(unittest.TestCase):
    def test_measured_reducer_matches_raw_run(self) -> None:
        result = analyze(RUN)
        aggregate = result["aggregate"]
        self.assertEqual(aggregate["model_calls"], 6)
        self.assertEqual(aggregate["admitted_actions"], 6)
        self.assertEqual(aggregate["recurrent_pressure_events_resolved"], 4)
        self.assertEqual(aggregate["results_delivered_to_new_decisions_including_frozen_pending"], 6)
        self.assertEqual(aggregate["exact_reopens"], 4)
        self.assertEqual(aggregate["other_acquisitions"], 2)
        self.assertEqual(aggregate["mutations"], 0)
        self.assertEqual(aggregate["submissions"], 0)
        self.assertEqual(aggregate["candidate_changes"], 0)
        self.assertEqual(aggregate["recurrent_tokens_recovered"], 7853)
        self.assertEqual(aggregate["prompt_tokens"], 120030)
        self.assertEqual(aggregate["completion_tokens"], 221)


if __name__ == "__main__":
    unittest.main()
