from __future__ import annotations

import unittest

from apparatus.canonical import load_json
from apparatus.constants import ROOT
from offline_audit.construction_set import (
    CELL_DIRS,
    TARGET_GROUPS,
    build_backing_catalog,
    build_fresh_phase,
    ensure_required_resident,
    governing_keys,
    inventory,
    required_keys,
)
from apparatus.receipts import receipt_from_message


class CounterfactualAuditTests(unittest.TestCase):
    def _request(self, cell: str) -> dict:
        directory = CELL_DIRS[cell]
        return load_json(
            ROOT
            / "runs"
            / "2026-08-20-sealed-horizon-run-v0"
            / "cells"
            / directory
            / "requests"
            / "call-12.json"
        )

    def test_every_required_object_has_exact_backing(self) -> None:
        all_keys = required_keys(("R030", "R031", "R032", "R033"))
        for cell in CELL_DIRS:
            request = self._request(cell)
            catalog = build_backing_catalog(cell)
            projected, changes = ensure_required_resident(request["messages"], all_keys, catalog)
            state = inventory(projected, all_keys)
            self.assertTrue(changes)
            self.assertTrue(all(row["resident_full_occurrences"] >= 1 for row in state.values()))

    def test_fresh_phase_contains_only_fixed_frame_and_required_pairs(self) -> None:
        keys = required_keys(("R030", "R031", "R032", "R033"))
        for cell in CELL_DIRS:
            request = self._request(cell)
            messages, manifest = build_fresh_phase(request["messages"], keys, build_backing_catalog(cell))
            self.assertEqual(len(messages), 2 + 2 * len(keys))
            self.assertEqual({row["object_key"] for row in manifest}, set(keys))
            self.assertTrue(all(receipt_from_message(message) is None for message in messages[3::2]))

    def test_scenarios_are_mechanical_and_fixed(self) -> None:
        self.assertEqual(len(governing_keys()), 4)
        self.assertEqual(TARGET_GROUPS["governing_only"], ())
        self.assertEqual(TARGET_GROUPS["plus_r030_r033_top_level_tail"], ("R030", "R031", "R032", "R033"))
        self.assertEqual(len(TARGET_GROUPS), 7)


if __name__ == "__main__":
    unittest.main()
