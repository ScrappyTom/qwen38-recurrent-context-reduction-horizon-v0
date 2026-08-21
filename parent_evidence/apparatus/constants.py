from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STUDY_ID = "qwen38-recurrent-context-reduction-v0"
BRANCH = "codex/qwen38-recurrent-context-reduction-v0"

PREDECESSOR_REPOSITORY = "ScrappyTom/qwen38-context-reduction-pressure-boundary-v0"
PREDECESSOR_COMMIT = "ab0e21b201d04521a43f83c223a364bca35a7b86"
PREDECESSOR_RUN = "runs/2026-08-20-sealed-run-v0"
PARENT_REPOSITORY = "ScrappyTom/custody-cards-experimental-workbench"
PARENT_COMMIT = "40f9afdde9628e4fd5dbd8d18a6fcf85bdf9d820"
SOURCE_COMMIT = "f8c93e5ad33c8dd235c418df6561ba022d9077fb"

CONTEXT_TOKENS = 25_088
RESPONSE_RESERVE = 4_096
MAXIMUM_PROMPT_TOKENS = CONTEXT_TOKENS - RESPONSE_RESERVE
MAX_NEW_CALLS_PER_SEED = 3
MAXIMUM_MEASURED_CALLS = 6

TARGET = "QWEN_RELATION_ACTION_WORKING_MODEL.md"
TARGET_SHA256 = "899a37f188de42075d5559bcaf6ba4bea96713ba192517021dbcc533c9844387"

PREDECESSOR_ROOT = ROOT / "predecessor_evidence"

CELLS = {
    "s42-s1": {
        "seed": 42,
        "predecessor_cell": "01-s42-s1-oldest_fit_receipts_v0",
        "predecessor_prompt_tokens": 20_838,
        "predecessor_prompt_headroom": 154,
        "pending_action_id": "schema-action-013",
        "pending_action": {"action": "read_region", "region_id": "R030"},
        "pending_result_sha256": "ba4fe640c46f394b7cabaff0d09f96baf803c3e3a44f6853501553cf887502bb",
        "pending_result_size_bytes": 9_168,
        "raw_post_result_prompt_tokens": 23_353,
        "raw_post_result_headroom": -2_361,
        "raw_post_result_rendered_sha256": "be0dd0a032b61622b797b433d40d7d7c8b0af0a15c98312d4697fdc2398b36dc",
        "treated_post_result_prompt_tokens": 20_355,
        "treated_post_result_headroom": 637,
        "treated_post_result_rendered_sha256": "9dd6a867e6f743d80363502f8cabe5a25edf45d0f19405d13127fcb3b16f0e06",
        "expected_new_demoted_indices": [9, 11],
        "expected_new_token_savings": [1_750, 1_248],
    },
    "s314159-s1": {
        "seed": 314159,
        "predecessor_cell": "02-s314159-s1-oldest_fit_receipts_v0",
        "predecessor_prompt_tokens": 20_597,
        "predecessor_prompt_headroom": 395,
        "pending_action_id": "schema-action-011",
        "pending_action": {"action": "read_region", "region_id": "R032"},
        "pending_result_sha256": "12f35416365a0ec87c37c60ed4486112abb2daab604cf6ae51d39814234eb7bf",
        "pending_result_size_bytes": 2_979,
        "raw_post_result_prompt_tokens": 21_521,
        "raw_post_result_headroom": -529,
        "raw_post_result_rendered_sha256": "947dcf6e00fd23ab189fb80b3a4e11ea04b207e95857ec1616f7080c5301c54e",
        "treated_post_result_prompt_tokens": 19_775,
        "treated_post_result_headroom": 1_217,
        "treated_post_result_rendered_sha256": "fb49b32f9dba3bf582134c3417c833c8ef2bfe90947667e5f14124256acef34b",
        "expected_new_demoted_indices": [9],
        "expected_new_token_savings": [1_746],
    },
}

SOURCE_PATHS = (
    "experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md",
    "experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md",
    "experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md",
    "experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md",
)
