from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from typing import Any, Callable

from apparatus.canonical import compact_json, sha256_bytes


RECEIPT_SCHEMA = "exact-backed-result-receipt-v0"
POLICY_ID = "pressure_oldest_positive_savings_until_fit_v1"
IDENTITY_KEYS = (
    "candidate_id",
    "path",
    "region_id",
    "file_sha256",
    "blob_sha",
    "source_commit",
    "tree_sha",
    "slice_sha256",
    "sha256",
    "start_line",
    "end_line",
    "cursor",
    "continuation_cursor",
    "requested_start_line",
    "requested_end_line",
    "total_lines",
)


@dataclass
class Projection:
    policy_id: str
    messages: list[dict[str, Any]]
    changes: list[dict[str, Any]]
    selection_trace: list[dict[str, Any]]
    before_tokens: int
    after_tokens: int
    fits: bool


def pair_indices(messages: list[dict[str, Any]]) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for result_index in range(3, len(messages), 2):
        action_index = result_index - 1
        if messages[action_index].get("role") != "assistant" or messages[result_index].get("role") != "user":
            raise ValueError(f"noncanonical action/result pair at {action_index}/{result_index}")
        pairs.append((action_index, result_index))
    return pairs


def receipt_from_message(result_message: dict[str, Any]) -> dict[str, Any] | None:
    try:
        envelope = json.loads(result_message["content"])
        receipt = envelope["result"].get("context_receipt")
    except (KeyError, TypeError, json.JSONDecodeError):
        return None
    return receipt if isinstance(receipt, dict) and receipt.get("schema") == RECEIPT_SCHEMA else None


def make_receipt(action_message: dict[str, Any], result_message: dict[str, Any], *, backing_id: str) -> dict[str, Any]:
    if receipt_from_message(result_message) is not None:
        raise ValueError("cannot replace a receipt with another receipt")
    action = json.loads(action_message["content"])
    envelope = json.loads(result_message["content"])
    result = envelope["result"]
    binding = {key: result[key] for key in IDENTITY_KEYS if key in result}
    original = result_message["content"].encode("utf-8")
    context_receipt = {
        "schema": RECEIPT_SCHEMA,
        "residency": "nonresident",
        "previously_delivered": True,
        "exact_backing_available": True,
        "exact_backing_id": backing_id,
        "exact_message_sha256": sha256_bytes(original),
        "exact_message_size_bytes": len(original),
        "source_binding": binding,
        "reopen_action": action,
    }
    replacement = {
        "action": envelope["action"],
        "action_id": envelope["action_id"],
        "result": {"accepted": result.get("accepted") is True, "context_receipt": context_receipt},
    }
    return {"role": "user", "content": compact_json(replacement)}


TokenCount = Callable[[list[dict[str, Any]]], int]
BackingId = Callable[[int, dict[str, Any]], str]


def pressure_projection(
    cell: str,
    resident_messages: list[dict[str, Any]],
    pending_tail: list[dict[str, Any]],
    *,
    maximum_prompt_tokens: int,
    token_count: TokenCount,
    backing_id: BackingId | None = None,
) -> Projection:
    """Demote oldest positive-savings resident result bodies and stop when fit.

    The pending assistant/result pair is never eligible in the same pressure
    cycle. Existing receipts are skipped, and no transformation occurs when the
    prospective packet already fits.
    """
    projected = copy.deepcopy(resident_messages)
    before_tokens = token_count(projected + pending_tail)
    current = before_tokens
    changes: list[dict[str, Any]] = []
    trace: list[dict[str, Any]] = []
    if current <= maximum_prompt_tokens:
        return Projection(POLICY_ID, projected + copy.deepcopy(pending_tail), changes, trace, before_tokens, current, True)

    for action_index, result_index in pair_indices(projected):
        before = projected[result_index]
        existing = receipt_from_message(before)
        if existing is not None:
            trace.append(
                {
                    "result_index": result_index,
                    "action": json.loads(projected[action_index]["content"]),
                    "before_post_result_tokens": current,
                    "already_nonresident": True,
                    "accepted_positive_savings": False,
                }
            )
            continue
        after = make_receipt(
            projected[action_index],
            before,
            backing_id=(backing_id(result_index, before) if backing_id is not None else f"chronology:{cell}:sha256:{sha256_bytes(before['content'].encode('utf-8'))}"),
        )
        candidate = copy.deepcopy(projected)
        candidate[result_index] = after
        candidate_tokens = token_count(candidate + pending_tail)
        savings = current - candidate_tokens
        accepted = savings > 0
        trace.append(
            {
                "result_index": result_index,
                "action": json.loads(projected[action_index]["content"]),
                "before_post_result_tokens": current,
                "candidate_post_result_tokens": candidate_tokens,
                "token_savings": savings,
                "accepted_positive_savings": accepted,
            }
        )
        if accepted:
            record = {
                "action_index": action_index,
                "result_index": result_index,
                "action": json.loads(projected[action_index]["content"]),
                "original_content_sha256": sha256_bytes(before["content"].encode("utf-8")),
                "original_content_size_bytes": len(before["content"].encode("utf-8")),
                "receipt_content_sha256": sha256_bytes(after["content"].encode("utf-8")),
                "receipt_content_size_bytes": len(after["content"].encode("utf-8")),
                "token_savings": savings,
            }
            projected = candidate
            current = candidate_tokens
            changes.append(record)
        if current <= maximum_prompt_tokens:
            break
    return Projection(
        POLICY_ID,
        projected + copy.deepcopy(pending_tail),
        changes,
        trace,
        before_tokens,
        current,
        current <= maximum_prompt_tokens,
    )
