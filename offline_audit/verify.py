from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from apparatus.canonical import compact_json, load_json, sha256_bytes, sha256_file, write_json
from apparatus.constants import MAXIMUM_PROMPT_TOKENS, ROOT
from apparatus.seal import verify_seal
from offline_audit.construction_set import CELL_DIRS, SURFACES, TARGET_GROUPS, inventory


def verify(result_path: Path) -> dict[str, Any]:
    result = load_json(result_path)
    failures: list[str] = []
    expected_scenarios = len(CELL_DIRS) * len(SURFACES) * len(TARGET_GROUPS)
    if len(result.get("scenarios", [])) != expected_scenarios:
        failures.append(f"scenario count mismatch: {len(result.get('scenarios', []))} != {expected_scenarios}")
    if result.get("model_calls") != 0 or result.get("chat_completions_called") is not False:
        failures.append("audit claims a model/chat-completion call")
    calls = result.get("tokenizer_calls", {})
    if calls.get("chat_completions") != 0:
        failures.append("tokenizer receipt records a chat-completion call")

    cell_rows = {row["cell"]: row for row in result.get("cells", [])}
    for cell in CELL_DIRS:
        row = cell_rows.get(cell)
        if row is None:
            failures.append(f"missing cell: {cell}")
        elif not row.get("exact_reproduction") or row.get("actual_call_12_prompt_tokens") != row.get("provider_prompt_tokens"):
            failures.append(f"call-12 tokenizer reproduction failed: {cell}")

    seen: set[tuple[str, str, str]] = set()
    for row in result.get("scenarios", []):
        identity = (row["cell"], row["surface"], row["target_group"])
        if identity in seen:
            failures.append(f"duplicate scenario: {identity}")
        seen.add(identity)
        if row["headroom_after_reserve"] != MAXIMUM_PROMPT_TOKENS - row["prompt_tokens"]:
            failures.append(f"headroom mismatch: {identity}")
        if row["fits"] != (row["prompt_tokens"] <= MAXIMUM_PROMPT_TOKENS):
            failures.append(f"fit predicate mismatch: {identity}")

        packet_path = ROOT / row["packet_path"]
        if not packet_path.is_file():
            failures.append(f"packet missing: {row['packet_path']}")
            continue
        if sha256_file(packet_path) != row["packet_file_sha256"]:
            failures.append(f"packet file hash mismatch: {row['packet_path']}")
            continue
        packet = load_json(packet_path)
        request_hash = sha256_bytes(compact_json(packet).encode("utf-8"))
        if request_hash != row["request_sha256"]:
            failures.append(f"packet request hash mismatch: {row['packet_path']}")
        observed = inventory(packet["messages"], row["required_object_keys"])
        if observed != row["required_inventory"]:
            failures.append(f"required inventory mismatch: {identity}")
        if any(value["resident_full_occurrences"] < 1 for value in observed.values()):
            failures.append(f"required object nonresident: {identity}")

    seal = verify_seal(ROOT / result["measured_run"])
    if not seal["passed"]:
        failures.extend(f"measured run {failure}" for failure in seal["failures"])
    expected_seal = result.get("measured_run_seal_sha256")
    observed_seal = sha256_file(ROOT / result["measured_run"] / "SEAL.json")
    if expected_seal != observed_seal:
        failures.append("measured run SEAL.json changed")

    return {
        "schema_version": "qwen38-construction-set-counterfactual-verification-v0",
        "passed": not failures,
        "failures": failures,
        "scenario_count": len(seen),
        "packet_count": sum(1 for _ in (ROOT / "counterfactual_packets").rglob("*.json")),
        "model_calls": 0,
        "chat_completions": 0,
        "measured_run_seal": seal,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, default=ROOT / "CONSTRUCTION_SET_COUNTERFACTUAL_AUDIT.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = verify(args.result.resolve())
    if args.output is not None:
        write_json(args.output.resolve(), receipt)
    print(compact_json(receipt))
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
