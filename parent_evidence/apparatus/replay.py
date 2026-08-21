from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from apparatus.canonical import canonical_json_bytes, load_json, sha256_bytes, sha256_file, write_json
from apparatus.constants import CELLS, ROOT
from apparatus.predecessor import predecessor_assistant_message, predecessor_call
from apparatus.receipts import receipt_from_message


def verify_materialization() -> list[str]:
    failures: list[str] = []
    receipt = load_json(ROOT / "provenance" / "PREDECESSOR_MATERIALIZATION_RECEIPT.json")
    for row in receipt["files"]:
        path = ROOT / row["copied_path"]
        if not path.is_file() or path.stat().st_size != row["copied_size_bytes"] or sha256_file(path) != row["copied_sha256"]:
            failures.append(f"materialization mismatch: {row['copied_path']}")
    if receipt.get("all_byte_equivalent") is not True:
        failures.append("materialization receipt is not all-byte-equivalent")
    return failures


def verify_lock() -> list[str]:
    failures: list[str] = []
    lock = load_json(ROOT / "provenance" / "SOURCE_LOCK.json")
    for relative, expected in lock["locked_artifacts"].items():
        path = ROOT / relative
        if not path.is_file() or sha256_file(path) != expected:
            failures.append(f"source-lock mismatch: {relative}")
    for row in lock["packets"]:
        path = ROOT / row["path"]
        if not path.is_file() or path.stat().st_size != row["size_bytes"] or sha256_file(path) != row["sha256"]:
            failures.append(f"packet lock mismatch: {row['path']}")
    return failures


def verify_packets() -> list[str]:
    failures: list[str] = []
    capacity = load_json(ROOT / "CAPACITY_PREFLIGHT.json")
    for row in capacity["cells"]:
        cell = row["cell"]
        root = ROOT / "preflight" / "packets" / cell
        control_path = root / "control-raw-post-result-request.json"
        treated_path = root / "cycle-01-delivery-request.json"
        control = json.loads(control_path.read_bytes())
        treated = json.loads(treated_path.read_bytes())
        if canonical_json_bytes(control) != control_path.read_bytes():
            failures.append(f"noncanonical control packet: {cell}")
        if canonical_json_bytes(treated) != treated_path.read_bytes():
            failures.append(f"noncanonical treatment packet: {cell}")
        base = predecessor_call(cell, 2)["request"]["messages"]
        expected_assistant = predecessor_assistant_message(cell)
        if control["messages"][: len(base)] != base or control["messages"][len(base)] != expected_assistant:
            failures.append(f"control prefix/tail mismatch: {cell}")
        if len(control["messages"]) != len(treated["messages"]):
            failures.append(f"message count changed: {cell}")
            continue
        observed = {index for index, (before, after) in enumerate(zip(control["messages"], treated["messages"], strict=True)) if before != after}
        declared = set(row["newly_demoted_result_indices"])
        if observed != declared:
            failures.append(f"treatment delta mismatch: {cell}")
        for index in observed:
            receipt = receipt_from_message(treated["messages"][index])
            if receipt is None:
                failures.append(f"changed message is not exact receipt: {cell}/{index}")
                continue
            original = control["messages"][index]["content"].encode("utf-8")
            if receipt.get("exact_message_sha256") != sha256_bytes(original):
                failures.append(f"receipt exact hash mismatch: {cell}/{index}")
            if {"content", "summary", "relevance", "semantic_status"} & set(receipt):
                failures.append(f"semantic or inline content in receipt: {cell}/{index}")
        backing = load_json(root / "exact-backing-index.json")
        for item in backing["receipts"]:
            index = item["resident_message_index"]
            receipt = receipt_from_message(treated["messages"][index])
            if receipt is None or receipt["exact_message_sha256"] != item["exact_message_sha256"]:
                failures.append(f"backing index mismatch: {cell}/{index}")
        if row["raw_control_after_pending_result"]["fits"] is not False or row["treatment_after_pending_result"]["fits"] is not True:
            failures.append(f"capacity disposition mismatch: {cell}")
        if row["treatment_after_pending_result"]["prompt_tokens"] != CELLS[cell]["treated_post_result_prompt_tokens"]:
            failures.append(f"frozen treatment token mismatch: {cell}")
    return failures


def replay_preflight() -> dict[str, Any]:
    categories = {"materialization": verify_materialization(), "source_lock": verify_lock(), "packets": verify_packets()}
    failures = [failure for rows in categories.values() for failure in rows]
    return {
        "schema_version": "recurrent-context-reduction-preflight-replay-v0",
        "passed": not failures,
        "categories": {key: {"passed": not value, "failures": value} for key, value in categories.items()},
        "failure_count": len(failures),
    }


def replay_run(run_root: Path) -> dict[str, Any]:
    failures: list[str] = []
    result = load_json(run_root / "RUN_RESULT.json")
    observed_calls = 0
    for cell in result["cells"]:
        roots = list((run_root / "cells").glob(f"*-{cell['cell']}-recurrent-oldest-fit-v1"))
        if len(roots) != 1:
            failures.append(f"cannot resolve cell directory: {cell['cell']}")
            continue
        root = roots[0]
        http_rows = sorted((root / "raw").glob("call-*-http.json"))
        observed_calls += len(http_rows)
        for receipt_path in http_rows:
            receipt = load_json(receipt_path)
            call = int(receipt_path.stem.split("-")[1])
            request = root / "requests" / f"call-{call:02d}.json"
            response = root / "responses" / f"call-{call:02d}.json"
            if not request.is_file() or sha256_file(request) != receipt["request_sha256"]:
                failures.append(f"request hash mismatch: {request.relative_to(run_root)}")
            if not response.is_file() or sha256_file(response) != receipt["response_sha256"]:
                failures.append(f"response hash mismatch: {response.relative_to(run_root)}")
        for result_path in sorted((root / "results").glob("call-*.json")):
            row = load_json(result_path)
            backing = root / row["exact_backing"]["path"]
            if not backing.is_file() or sha256_file(backing) != row["exact_backing"]["sha256"]:
                failures.append(f"exact backing mismatch: {result_path.relative_to(run_root)}")
        terminal = load_json(root / "candidates" / "terminal.json")
        if terminal["candidate_id"] != cell["final_candidate_id"]:
            failures.append(f"terminal candidate mismatch: {cell['cell']}")
    if observed_calls != result["model_calls"]:
        failures.append(f"model call count mismatch: observed={observed_calls} declared={result['model_calls']}")
    return {
        "schema_version": "recurrent-context-reduction-measured-replay-v0",
        "run_id": result["run_id"],
        "passed": not failures,
        "observed_model_calls": observed_calls,
        "declared_model_calls": result["model_calls"],
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = replay_run(args.run_root.resolve()) if args.run_root else replay_preflight()
    output = args.output.resolve() if args.output else ROOT / "PREFLIGHT_REPLAY.json"
    write_json(output, receipt)
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
