from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from apparatus.seal import seal, verify_seal


class SealTests(unittest.TestCase):
    def test_seal_round_trip_and_detects_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "run"
            root.mkdir()
            item = root / "raw.json"
            item.write_bytes(b"{}\n")
            seal(root)
            self.assertTrue(verify_seal(root)["passed"])
            item.write_bytes(b'{"changed":true}\n')
            self.assertFalse(verify_seal(root)["passed"])


if __name__ == "__main__":
    unittest.main()
