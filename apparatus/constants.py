from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STUDY_ID = "qwen38-recurrent-context-reduction-horizon-v0"
BRANCH = "codex/qwen38-recurrent-context-reduction-horizon-v0"

PREDECESSOR_REPOSITORY = "ScrappyTom/qwen38-recurrent-context-reduction-v0"
PREDECESSOR_COMMIT = "9a42b85b4d9fd25bd873d45c08a403c2ca1ff96e"
PREDECESSOR_INFERENCE_COMMIT = "50e72ba467388bd4c116a5f2b4e5b38f80e820d3"
PREDECESSOR_RUN = "runs/2026-08-20-sealed-run-v1"
PARENT_REPOSITORY = "ScrappyTom/custody-cards-experimental-workbench"
PARENT_COMMIT = "40f9afdde9628e4fd5dbd8d18a6fcf85bdf9d820"
SOURCE_COMMIT = "f8c93e5ad33c8dd235c418df6561ba022d9077fb"

CONTEXT_TOKENS = 25_088
RESPONSE_RESERVE = 4_096
MAXIMUM_PROMPT_TOKENS = CONTEXT_TOKENS - RESPONSE_RESERVE
MAX_NEW_CALLS_PER_SEED = 12
MAXIMUM_MEASURED_CALLS = 24

TARGET = "QWEN_RELATION_ACTION_WORKING_MODEL.md"
TARGET_SHA256 = "899a37f188de42075d5559bcaf6ba4bea96713ba192517021dbcc533c9844387"

DONOR_ROOT = ROOT / "parent_evidence"
PREDECESSOR_ROOT = DONOR_ROOT / "predecessor_evidence"

CELLS = {
    "s42-s1": {
        "seed": 42,
        "donor_cell": "01-s42-s1-recurrent-oldest-fit-v1",
        "donor_call": 3,
        "donor_prompt_tokens": 20_894,
        "donor_prompt_headroom": 98,
        "pending_action_id": "schema-action-016",
        "pending_action": {
            "action": "repo_read",
            "path": "experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md",
        },
        "pending_result_message_sha256": "8dc2a52b0145b8c4d317b6151ef8a892cf31253795e91d7c458469b9259c9df9",
        "pending_result_message_size_bytes": 5_836,
        "raw_post_result_prompt_tokens": 22_514,
        "raw_post_result_headroom": -1_522,
        "raw_post_result_rendered_sha256": "081e9d392412de91bb49830e6c68e08b584657530c57eaf0ae6eb06b9982bd89",
    },
    "s314159-s1": {
        "seed": 314159,
        "donor_cell": "02-s314159-s1-recurrent-oldest-fit-v1",
        "donor_call": 3,
        "donor_prompt_tokens": 19_086,
        "donor_prompt_headroom": 1_906,
        "pending_action_id": "schema-action-014",
        "pending_action": {
            "action": "repo_read",
            "path": "experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md",
        },
        "pending_result_message_sha256": "5b486bf2a0f9f72961b7090f556f6bfd606cc97df88c9b6183dbdf88f0bacdeb",
        "pending_result_message_size_bytes": 8_617,
        "raw_post_result_prompt_tokens": 21_193,
        "raw_post_result_headroom": -201,
        "raw_post_result_rendered_sha256": "22d30ca7985623c77f81d515d7be610b28916749171b88abda3f299ca7e51f8d",
    },
}

SOURCE_PATHS = (
    "experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md",
    "experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md",
    "experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md",
    "experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md",
)

INTEGRITY_REJECTION_CODES = {
    "source_surface_not_materialized",
    "historical_reopen_unavailable",
    "exact_backing_mismatch",
    "unsupported_declared_action",
}
