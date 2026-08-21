import unittest
from pathlib import Path

from apparatus.seal import verify_seal
from postrun.verify import audit_current_locked_paths, verify_frozen_commit_lock


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs" / "2026-08-20-sealed-horizon-run-v0"
FROZEN_COMMIT = "ca07e84cde79c7db147ba4cc43f06133fc6d353e"


class PostRunVerificationTests(unittest.TestCase):
    def test_frozen_commit_retains_exact_authorized_source_lock(self) -> None:
        self.assertTrue(verify_frozen_commit_lock(FROZEN_COMMIT)["passed"])

    @unittest.skipUnless((RUN / "SEAL.json").is_file(), "measured run has not been sealed")
    def test_measured_run_seal_verifies(self) -> None:
        self.assertTrue(verify_seal(RUN)["passed"])

    @unittest.skipUnless((ROOT / "POSTRUN_VERIFICATION.json").is_file(), "post-run reports are not finalized")
    def test_only_declared_frozen_paths_changed_after_inference(self) -> None:
        self.assertTrue(audit_current_locked_paths()["passed"])


if __name__ == "__main__":
    unittest.main()
