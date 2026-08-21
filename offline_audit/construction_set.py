from __future__ import annotations

import argparse
import copy
import json
from collections import OrderedDict
from pathlib import Path
from typing import Any, Iterable

from apparatus.canonical import compact_json, load_json, sha256_bytes, sha256_file, write_json
from apparatus.constants import MAXIMUM_PROMPT_TOKENS, RESPONSE_RESERVE, ROOT
from apparatus.modelio import ParentTokenEndpoint, request_with_messages
from apparatus.receipts import make_receipt, pair_indices, receipt_from_message


AUDIT_ID = "qwen38-construction-set-counterfactual-audit-v0"
BASE_COMMIT = "f52642ec85efdc8f7196515503a0312af7c38d78"
RUN_ROOT = ROOT / "runs" / "2026-08-20-sealed-horizon-run-v0"

CELL_DIRS = OrderedDict(
    (
        ("s42-s1", "01-s42-s1-recurrent-oldest-fit-horizon-v0"),
        ("s314159-s1", "02-s314159-s1-recurrent-oldest-fit-horizon-v0"),
    )
)

GOVERNING_DOCUMENTS = OrderedDict(
    (
        (
            "source_navigation_results",
            "experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md",
        ),
        (
            "source_navigation_audit",
            "experiments/large-world-source-navigation-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md",
        ),
        (
            "navigation_continuity_results",
            "experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/RESULTS.md",
        ),
        (
            "navigation_continuity_audit",
            "experiments/large-world-navigation-continuity-v0/runs/2026-08-18-sealed-bank-v0/DIRECT_TRANSCRIPT_AUDIT.md",
        ),
    )
)

TARGET_GROUPS = OrderedDict(
    (
        ("governing_only", ()),
        ("plus_r030_operational_model", ("R030",)),
        ("plus_r031_phase_continuity", ("R031",)),
        ("plus_r032_design_consequences", ("R032",)),
        ("plus_r033_unknowns", ("R033",)),
        ("plus_r031_r033_tail", ("R031", "R032", "R033")),
        ("plus_r030_r033_top_level_tail", ("R030", "R031", "R032", "R033")),
    )
)

SURFACES = (
    "historical_restore_only",
    "receipt_floor_then_restore",
    "fresh_phase",
)


def action_from_message(message: dict[str, Any]) -> dict[str, Any]:
    value = json.loads(message["content"])
    if not isinstance(value, dict) or not isinstance(value.get("action"), str):
        raise ValueError("assistant message does not contain an action object")
    return value


def object_key(action: dict[str, Any]) -> str | None:
    if action.get("action") == "repo_read" and isinstance(action.get("path"), str):
        return f"repo_read:{action['path']}"
    if action.get("action") == "read_region" and isinstance(action.get("region_id"), str):
        return f"read_region:{action['region_id']}"
    return None


def governing_keys() -> tuple[str, ...]:
    return tuple(f"repo_read:{path}" for path in GOVERNING_DOCUMENTS.values())


def required_keys(target_regions: Iterable[str]) -> tuple[str, ...]:
    return governing_keys() + tuple(f"read_region:{region}" for region in target_regions)


def _walk_messages(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        if value.get("role") == "user" and isinstance(value.get("content"), str):
            yield value
        for child in value.values():
            yield from _walk_messages(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_messages(child)


def _catalog_json_messages(path: Path, catalog: dict[str, dict[str, Any]]) -> None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return
    for message in _walk_messages(value):
        content = message["content"]
        digest = sha256_bytes(content.encode("utf-8"))
        existing = catalog.get(digest)
        if existing is not None and existing["content"] != content:
            raise ValueError(f"hash collision while cataloging {path}")
        catalog[digest] = {"role": "user", "content": content}


def build_backing_catalog(cell: str) -> dict[str, dict[str, Any]]:
    cell_dir = RUN_ROOT / "cells" / CELL_DIRS[cell]
    catalog: dict[str, dict[str, Any]] = {}
    sources = [
        cell_dir / "requests",
        cell_dir / "projections",
        ROOT / "preflight" / "packets" / cell,
        ROOT / "parent_evidence" / "predecessor_evidence" / "preflight" / "packets" / cell,
        ROOT / "parent_evidence" / "predecessor_evidence" / "evidence" / "parent" / cell,
    ]
    for source in sources:
        if source.is_dir():
            for path in sorted(source.rglob("*.json")):
                _catalog_json_messages(path, catalog)

    objects = cell_dir / "objects"
    if objects.is_dir():
        for path in sorted(objects.glob("*.json")):
            content = path.read_text(encoding="utf-8").rstrip("\n")
            digest = sha256_bytes(content.encode("utf-8"))
            if digest != path.stem:
                raise ValueError(f"object filename/content mismatch: {path}")
            catalog[digest] = {"role": "user", "content": content}
    return catalog


def restore_receipt(message: dict[str, Any], catalog: dict[str, dict[str, Any]]) -> dict[str, Any]:
    receipt = receipt_from_message(message)
    if receipt is None:
        return copy.deepcopy(message)
    digest = receipt["exact_message_sha256"]
    backing = catalog.get(digest)
    if backing is None:
        raise ValueError(f"exact backing unavailable for {digest}")
    raw = backing["content"].encode("utf-8")
    if len(raw) != receipt["exact_message_size_bytes"] or sha256_bytes(raw) != digest:
        raise ValueError(f"exact backing verification failed for {digest}")
    return copy.deepcopy(backing)


def pair_records(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for action_index, result_index in pair_indices(messages):
        action = action_from_message(messages[action_index])
        rows.append(
            {
                "action_index": action_index,
                "result_index": result_index,
                "action": action,
                "object_key": object_key(action),
                "resident": receipt_from_message(messages[result_index]) is None,
            }
        )
    return rows


def inventory(messages: list[dict[str, Any]], keys: Iterable[str]) -> dict[str, dict[str, int]]:
    wanted = tuple(keys)
    output = {key: {"resident_full_occurrences": 0, "receipt_occurrences": 0} for key in wanted}
    for row in pair_records(messages):
        key = row["object_key"]
        if key not in output:
            continue
        field = "resident_full_occurrences" if row["resident"] else "receipt_occurrences"
        output[key][field] += 1
    return output


def ensure_required_resident(
    messages: list[dict[str, Any]],
    keys: Iterable[str],
    catalog: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    projected = copy.deepcopy(messages)
    changes: list[dict[str, Any]] = []
    for key in keys:
        rows = [row for row in pair_records(projected) if row["object_key"] == key]
        if not rows:
            raise ValueError(f"required object absent from chronology: {key}")
        if any(row["resident"] for row in rows):
            continue
        chosen = rows[-1]
        before = projected[chosen["result_index"]]
        after = restore_receipt(before, catalog)
        projected[chosen["result_index"]] = after
        changes.append(
            {
                "object_key": key,
                "result_index": chosen["result_index"],
                "receipt_sha256": sha256_bytes(before["content"].encode("utf-8")),
                "restored_sha256": sha256_bytes(after["content"].encode("utf-8")),
                "restored_size_bytes": len(after["content"].encode("utf-8")),
            }
        )
    return projected, changes


def build_receipt_floor(
    cell: str,
    messages: list[dict[str, Any]],
    endpoint: ParentTokenEndpoint,
    kwargs: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    projected = copy.deepcopy(messages)
    current_tokens = endpoint.count(projected, kwargs).prompt_tokens
    changes: list[dict[str, Any]] = []
    for action_index, result_index in pair_indices(projected):
        before = projected[result_index]
        if receipt_from_message(before) is not None:
            continue
        digest = sha256_bytes(before["content"].encode("utf-8"))
        after = make_receipt(
            projected[action_index],
            before,
            backing_id=f"counterfactual:{cell}:message:{result_index}:sha256:{digest}",
        )
        candidate = copy.deepcopy(projected)
        candidate[result_index] = after
        candidate_tokens = endpoint.count(candidate, kwargs).prompt_tokens
        savings = current_tokens - candidate_tokens
        if savings <= 0:
            continue
        projected = candidate
        current_tokens = candidate_tokens
        changes.append(
            {
                "action_index": action_index,
                "result_index": result_index,
                "action": action_from_message(projected[action_index]),
                "original_content_sha256": digest,
                "receipt_content_sha256": sha256_bytes(after["content"].encode("utf-8")),
                "token_savings": savings,
            }
        )
    return projected, changes


def build_fresh_phase(
    base_messages: list[dict[str, Any]],
    keys: Iterable[str],
    catalog: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    chosen: list[dict[str, Any]] = []
    for key in keys:
        rows = [row for row in pair_records(base_messages) if row["object_key"] == key]
        if not rows:
            raise ValueError(f"required object absent from chronology: {key}")
        row = rows[-1]
        chosen.append(row)
    chosen.sort(key=lambda row: row["action_index"])
    messages = copy.deepcopy(base_messages[:2])
    manifest: list[dict[str, Any]] = []
    for row in chosen:
        action_message = copy.deepcopy(base_messages[row["action_index"]])
        result_message = restore_receipt(base_messages[row["result_index"]], catalog)
        messages.extend((action_message, result_message))
        manifest.append(
            {
                "object_key": row["object_key"],
                "source_action_index": row["action_index"],
                "source_result_index": row["result_index"],
                "result_sha256": sha256_bytes(result_message["content"].encode("utf-8")),
            }
        )
    return messages, manifest


def _scenario_row(
    *,
    cell: str,
    surface: str,
    target_group: str,
    keys: tuple[str, ...],
    messages: list[dict[str, Any]],
    base_request: dict[str, Any],
    endpoint: ParentTokenEndpoint,
    packet_root: Path,
    transformation: list[dict[str, Any]],
) -> dict[str, Any]:
    kwargs = base_request["chat_template_kwargs"]
    token = endpoint.count(messages, kwargs)
    state = inventory(messages, keys)
    missing = [key for key, row in state.items() if row["resident_full_occurrences"] < 1]
    if missing:
        raise ValueError(f"scenario missing required resident objects: {missing}")
    packet = request_with_messages(base_request, messages)
    relative = Path(cell) / f"{surface}--{target_group}.json"
    packet_path = packet_root / relative
    write_json(packet_path, packet)
    return {
        "cell": cell,
        "surface": surface,
        "target_group": target_group,
        "required_object_keys": list(keys),
        "required_inventory": state,
        "message_count": len(messages),
        "prompt_tokens": token.prompt_tokens,
        "response_reserve_tokens": RESPONSE_RESERVE,
        "maximum_prompt_tokens": MAXIMUM_PROMPT_TOKENS,
        "headroom_after_reserve": token.headroom_after_reserve,
        "fits": token.fits,
        "rendered_prompt_sha256": token.rendered_prompt_sha256,
        "rendered_prompt_size_bytes": token.rendered_prompt_size_bytes,
        "request_sha256": sha256_bytes(compact_json(packet).encode("utf-8")),
        "packet_path": packet_path.relative_to(ROOT).as_posix(),
        "packet_file_sha256": sha256_file(packet_path),
        "transformation": transformation,
    }


def _classification(rows: list[dict[str, Any]], cell: str) -> dict[str, Any]:
    def row(surface: str, group: str) -> dict[str, Any]:
        return next(
            item
            for item in rows
            if item["cell"] == cell and item["surface"] == surface and item["target_group"] == group
        )

    full_tail_fresh = row("fresh_phase", "plus_r030_r033_top_level_tail")
    full_tail_floor = row("receipt_floor_then_restore", "plus_r030_r033_top_level_tail")
    full_tail_historical = row("historical_restore_only", "plus_r030_r033_top_level_tail")
    single_rows = [
        row("receipt_floor_then_restore", name)
        for name in TARGET_GROUPS
        if name.startswith("plus_r0") and "r033_tail" not in name and "r030_r033" not in name
    ]
    if not full_tail_fresh["fits"]:
        disposition = "raw_full_tail_exceeds_envelope_even_in_fresh_phase"
    elif not full_tail_floor["fits"]:
        disposition = "raw_full_tail_fits_fresh_phase_but_not_receipt_bearing_chronology"
    elif not full_tail_historical["fits"]:
        disposition = "raw_full_tail_fits_after_additional_exact_receipt_reduction"
    else:
        disposition = "raw_full_tail_fits_in_actual_late_chronology"
    return {
        "cell": cell,
        "disposition": disposition,
        "all_single_target_sections_fit_on_receipt_floor": all(item["fits"] for item in single_rows),
        "governing_four_receipt_floor": row("receipt_floor_then_restore", "governing_only"),
        "full_tail_historical_restore": full_tail_historical,
        "full_tail_receipt_floor": full_tail_floor,
        "full_tail_fresh_phase": full_tail_fresh,
    }


def run_audit(endpoint_url: str, output: Path, packet_root: Path) -> dict[str, Any]:
    endpoint = ParentTokenEndpoint(endpoint_url)
    scenarios: list[dict[str, Any]] = []
    cells: list[dict[str, Any]] = []
    packet_root.mkdir(parents=True, exist_ok=True)

    for cell, directory in CELL_DIRS.items():
        cell_dir = RUN_ROOT / "cells" / directory
        base_path = cell_dir / "requests" / "call-12.json"
        response_path = cell_dir / "responses" / "call-12.json"
        base_request = load_json(base_path)
        base_messages = base_request["messages"]
        kwargs = base_request["chat_template_kwargs"]
        catalog = build_backing_catalog(cell)

        actual = endpoint.count(base_messages, kwargs)
        provider = load_json(response_path)["usage"]["prompt_tokens"]
        if actual.prompt_tokens != provider:
            raise ValueError(f"exact tokenizer mismatch for {cell}: {actual.prompt_tokens} != {provider}")

        floor, floor_changes = build_receipt_floor(cell, base_messages, endpoint, kwargs)
        floor_count = endpoint.count(floor, kwargs)
        cells.append(
            {
                "cell": cell,
                "base_request_path": base_path.relative_to(ROOT).as_posix(),
                "base_request_sha256": sha256_file(base_path),
                "base_response_path": response_path.relative_to(ROOT).as_posix(),
                "base_response_sha256": sha256_file(response_path),
                "actual_call_12_prompt_tokens": actual.prompt_tokens,
                "provider_prompt_tokens": provider,
                "exact_reproduction": actual.prompt_tokens == provider,
                "actual_call_12_headroom": actual.headroom_after_reserve,
                "receipt_floor_prompt_tokens": floor_count.prompt_tokens,
                "receipt_floor_headroom": floor_count.headroom_after_reserve,
                "receipt_floor_positive_savings_substitutions": floor_changes,
                "backing_catalog_objects": len(catalog),
            }
        )

        for target_group, target_regions in TARGET_GROUPS.items():
            keys = required_keys(target_regions)

            historical, restored = ensure_required_resident(base_messages, keys, catalog)
            scenarios.append(
                _scenario_row(
                    cell=cell,
                    surface="historical_restore_only",
                    target_group=target_group,
                    keys=keys,
                    messages=historical,
                    base_request=base_request,
                    endpoint=endpoint,
                    packet_root=packet_root,
                    transformation=restored,
                )
            )

            floor_restored, floor_restorations = ensure_required_resident(floor, keys, catalog)
            scenarios.append(
                _scenario_row(
                    cell=cell,
                    surface="receipt_floor_then_restore",
                    target_group=target_group,
                    keys=keys,
                    messages=floor_restored,
                    base_request=base_request,
                    endpoint=endpoint,
                    packet_root=packet_root,
                    transformation=floor_changes + floor_restorations,
                )
            )

            fresh, manifest = build_fresh_phase(base_messages, keys, catalog)
            scenarios.append(
                _scenario_row(
                    cell=cell,
                    surface="fresh_phase",
                    target_group=target_group,
                    keys=keys,
                    messages=fresh,
                    base_request=base_request,
                    endpoint=endpoint,
                    packet_root=packet_root,
                    transformation=manifest,
                )
            )

    result = {
        "schema_version": "qwen38-construction-set-counterfactual-audit-v0",
        "audit_id": AUDIT_ID,
        "base_commit": BASE_COMMIT,
        "measured_run": RUN_ROOT.relative_to(ROOT).as_posix(),
        "measured_run_seal_sha256": sha256_file(RUN_ROOT / "SEAL.json"),
        "mode": "offline_exact_tokenizer_counterfactual_no_inference",
        "model_calls": 0,
        "chat_completions_called": endpoint.chat_completion_calls > 0,
        "endpoint": endpoint_url,
        "context_tokens": MAXIMUM_PROMPT_TOKENS + RESPONSE_RESERVE,
        "response_reserve_tokens": RESPONSE_RESERVE,
        "maximum_prompt_tokens": MAXIMUM_PROMPT_TOKENS,
        "surfaces": list(SURFACES),
        "target_groups": {key: list(value) for key, value in TARGET_GROUPS.items()},
        "governing_documents": GOVERNING_DOCUMENTS,
        "cells": cells,
        "scenarios": scenarios,
        "classifications": [_classification(scenarios, cell) for cell in CELL_DIRS],
        "tokenizer_calls": {
            "apply_template": endpoint.apply_calls,
            "tokenize": endpoint.tokenize_calls,
            "chat_completions": endpoint.chat_completion_calls,
        },
        "interpretation_limits": [
            "Fit is a physical capacity result, not evidence that the selected set is semantically sufficient.",
            "Target groups are declared investigator counterfactuals, not host claims about the only valid edit surface.",
            "Fresh phase removes ordinary chronology and is a lower-bound capacity construction, not an observed model state.",
            "No model decision, mutation, evaluation, or GPU inference is performed.",
        ],
    }
    write_json(output, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the offline construction-set token counterfactual audit.")
    parser.add_argument("--endpoint", default="http://127.0.0.1:18081")
    parser.add_argument("--output", type=Path, default=ROOT / "CONSTRUCTION_SET_COUNTERFACTUAL_AUDIT.json")
    parser.add_argument("--packet-root", type=Path, default=ROOT / "counterfactual_packets")
    args = parser.parse_args()
    result = run_audit(args.endpoint, args.output.resolve(), args.packet_root.resolve())
    print(compact_json({"passed": True, "scenarios": len(result["scenarios"]), "model_calls": 0}))


if __name__ == "__main__":
    main()
