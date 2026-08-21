from __future__ import annotations

import argparse
import copy
import json
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

from apparatus.canonical import canonical_json_bytes, compact_json, load_json, sha256_bytes, sha256_file, write_json
from apparatus.constants import (
    BRANCH,
    CELLS,
    CONTEXT_TOKENS,
    MAXIMUM_MEASURED_CALLS,
    MAXIMUM_PROMPT_TOKENS,
    MAX_NEW_CALLS_PER_SEED,
    PARENT_COMMIT,
    PARENT_REPOSITORY,
    PREDECESSOR_COMMIT,
    PREDECESSOR_REPOSITORY,
    PREDECESSOR_ROOT,
    RESPONSE_RESERVE,
    ROOT,
    SOURCE_COMMIT,
    SOURCE_PATHS,
    STUDY_ID,
)
from apparatus.environment import make_environment
from apparatus.modelio import ParentTokenEndpoint
from apparatus.predecessor import exact_backing_id, parent_boundary_objects, predecessor_assistant_message, predecessor_call, predecessor_cell_root
from apparatus.receipts import POLICY_ID, pressure_projection, receipt_from_message


def process(command: list[str], cwd: Path = ROOT) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, text=True)
    return {"command": command, "returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr, "passed": completed.returncode == 0}


def endpoint_props(base_url: str) -> dict[str, Any]:
    with urllib.request.urlopen(base_url.rstrip("/") + "/props", timeout=60) as response:
        value = json.loads(response.read())
    if not isinstance(value, dict):
        raise RuntimeError("tokenizer endpoint props is not an object")
    return value


def verify_materialization() -> dict[str, Any]:
    receipt = load_json(ROOT / "provenance" / "PREDECESSOR_MATERIALIZATION_RECEIPT.json")
    failures: list[str] = []
    for row in receipt["files"]:
        path = ROOT / row["copied_path"]
        if not path.is_file():
            failures.append(f"missing: {row['copied_path']}")
        elif path.stat().st_size != row["copied_size_bytes"] or sha256_file(path) != row["copied_sha256"]:
            failures.append(f"mismatch: {row['copied_path']}")
    predecessor_verify = load_json(PREDECESSOR_ROOT / "POSTRUN_VERIFICATION.json")
    predecessor_replay = load_json(PREDECESSOR_ROOT / "runs" / "2026-08-20-sealed-run-v0" / "replay" / "REPLAY.json")
    if predecessor_verify.get("passed") is not True:
        failures.append("imported predecessor verification was not passing")
    if predecessor_replay.get("passed") is not True:
        failures.append("imported predecessor replay was not passing")
    return {
        "passed": not failures,
        "checked_files": len(receipt["files"]),
        "checked_bytes": receipt["total_bytes"],
        "all_byte_equivalent": receipt["all_byte_equivalent"],
        "predecessor_postrun_verification_passed": predecessor_verify.get("passed") is True,
        "predecessor_measured_replay_passed": predecessor_replay.get("passed") is True,
        "predecessor_declared_model_calls": predecessor_replay.get("declared_model_calls"),
        "failures": failures,
    }


def packet_record(path: Path) -> dict[str, Any]:
    return {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256_file(path), "size_bytes": path.stat().st_size}


def write_packet(path: Path, request: dict[str, Any]) -> dict[str, Any]:
    write_json(path, request)
    return packet_record(path)


def message_ledger(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, message in enumerate(messages):
        content = str(message.get("content") or "")
        receipt = receipt_from_message(message)
        action: dict[str, Any] | None = None
        if message.get("role") == "assistant" and index >= 2:
            try:
                parsed = json.loads(content)
                action = parsed if isinstance(parsed, dict) else None
            except json.JSONDecodeError:
                pass
        rows.append(
            {
                "index": index,
                "role": message.get("role"),
                "content_sha256": sha256_bytes(content.encode("utf-8")),
                "content_size_bytes": len(content.encode("utf-8")),
                "resident_form": "exact_receipt" if receipt is not None else "full",
                "reopen_action": receipt.get("reopen_action") if receipt is not None else action,
            }
        )
    return rows


def exact_backing_index(cell: str, treated_messages: list[dict[str, Any]], path: Path) -> dict[str, Any]:
    parent = parent_boundary_objects(cell)["request"]["messages"]
    predecessor = predecessor_call(cell, 2)["request"]["messages"]
    sources = [
        ("parent_boundary_request", parent),
        ("predecessor_call_02_request", predecessor),
    ]
    rows: list[dict[str, Any]] = []
    for index, message in enumerate(treated_messages):
        receipt = receipt_from_message(message)
        if receipt is None:
            continue
        wanted = receipt["exact_message_sha256"]
        matches: list[dict[str, Any]] = []
        for source_name, messages in sources:
            for source_index, candidate in enumerate(messages):
                if sha256_bytes(str(candidate.get("content") or "").encode("utf-8")) == wanted:
                    matches.append({"source": source_name, "message_index": source_index})
        if not matches:
            raise RuntimeError(f"receipt backing cannot be resolved for {cell} message {index}")
        preferred = next((match for match in matches if match["source"] == "predecessor_call_02_request"), matches[0])
        rows.append(
            {
                "resident_message_index": index,
                "receipt_sha256": sha256_bytes(message["content"].encode("utf-8")),
                "exact_message_sha256": wanted,
                "exact_message_size_bytes": receipt["exact_message_size_bytes"],
                "reopen_action": receipt["reopen_action"],
                "canonical_backing": preferred,
                "equivalent_backing_locations": matches,
            }
        )
    document = {"schema_version": "recurrent-exact-backing-index-v0", "cell": cell, "receipts": rows}
    write_json(path, document)
    return document


def run_preflight(base_url: str, server_executable: Path, tokenizer_projection: Path) -> dict[str, Any]:
    custody = verify_materialization()
    if not custody["passed"]:
        raise RuntimeError("predecessor custody failed")
    predecessor_status = process(["git", "status", "--short", "--branch"], Path(r"E:\qwen38-context-reduction-pressure-boundary-v0"))
    predecessor_head = process(["git", "rev-parse", "HEAD"], Path(r"E:\qwen38-context-reduction-pressure-boundary-v0"))
    if not predecessor_status["passed"] or any(line and not line.startswith("##") for line in predecessor_status["stdout"].splitlines()):
        raise RuntimeError("predecessor working tree is not clean")
    if predecessor_head["stdout"].strip() != PREDECESSOR_COMMIT:
        raise RuntimeError("predecessor working tree is not at the frozen result commit")

    props = endpoint_props(base_url)
    if props.get("model_alias") != "qwen38-tokenizer-projection" or props.get("build_info") != "b10434-7e4c0a968":
        raise RuntimeError("tokenizer endpoint identity mismatch")
    endpoint = ParentTokenEndpoint(base_url)

    boundary_rows: list[dict[str, Any]] = []
    capacity_rows: list[dict[str, Any]] = []
    packet_rows: list[dict[str, Any]] = []
    backing_rows: list[dict[str, Any]] = []
    source_surface_rows: list[dict[str, Any]] = []

    for cell, frozen in CELLS.items():
        base = predecessor_call(cell, 2)["request"]
        base_messages = base["messages"]
        base_capacity = endpoint.count(base_messages, base["chat_template_kwargs"]).as_dict()
        if base_capacity["prompt_tokens"] != frozen["predecessor_prompt_tokens"]:
            raise RuntimeError(f"predecessor call-02 token mismatch for {cell}")
        with tempfile.TemporaryDirectory(prefix=f"recurrent-{cell}-") as temporary:
            env = make_environment(cell, Path(temporary))
            pending_action = frozen["pending_action"]
            pending_result = env.execute(pending_action)
            if pending_result.get("sha256") != frozen["pending_result_sha256"] or pending_result.get("size_bytes") != frozen["pending_result_size_bytes"]:
                raise RuntimeError(f"pending exact result mismatch for {cell}")
            assistant = predecessor_assistant_message(cell)
            result_message = env.result_message(pending_action, frozen["pending_action_id"], pending_result)
            tail = [assistant, result_message]
            raw_messages = copy.deepcopy(base_messages) + tail
            raw_capacity = endpoint.count(raw_messages, base["chat_template_kwargs"]).as_dict()
            if raw_capacity["prompt_tokens"] != frozen["raw_post_result_prompt_tokens"] or raw_capacity["rendered_prompt_sha256"] != frozen["raw_post_result_rendered_sha256"]:
                raise RuntimeError(f"raw recurrent pressure mismatch for {cell}")
            projection = pressure_projection(
                cell,
                base_messages,
                tail,
                maximum_prompt_tokens=MAXIMUM_PROMPT_TOKENS,
                token_count=lambda messages: endpoint.count(messages, base["chat_template_kwargs"]).prompt_tokens,
                backing_id=lambda index, message: exact_backing_id(cell, index, message),
            )
            treated_capacity = endpoint.count(projection.messages, base["chat_template_kwargs"]).as_dict()
            if not projection.fits or treated_capacity["prompt_tokens"] != frozen["treated_post_result_prompt_tokens"] or treated_capacity["rendered_prompt_sha256"] != frozen["treated_post_result_rendered_sha256"]:
                raise RuntimeError(f"treated recurrent packet mismatch for {cell}")
            if [row["result_index"] for row in projection.changes] != frozen["expected_new_demoted_indices"]:
                raise RuntimeError(f"recurrent selection mismatch for {cell}")
            if [row["token_savings"] for row in projection.changes] != frozen["expected_new_token_savings"]:
                raise RuntimeError(f"recurrent token savings mismatch for {cell}")

            packet_root = ROOT / "preflight" / "packets" / cell
            control_request = copy.deepcopy(base)
            control_request["messages"] = raw_messages
            treated_request = copy.deepcopy(base)
            treated_request["messages"] = projection.messages
            control_packet = write_packet(packet_root / "control-raw-post-result-request.json", control_request)
            treated_packet = write_packet(packet_root / "cycle-01-delivery-request.json", treated_request)
            packet_rows.extend([control_packet, treated_packet])
            write_json(
                packet_root / "projection-receipt.json",
                {
                    "cell": cell,
                    "policy_id": POLICY_ID,
                    "before_tokens": projection.before_tokens,
                    "after_tokens": projection.after_tokens,
                    "changes": projection.changes,
                    "selection_trace": projection.selection_trace,
                    "raw_capacity": raw_capacity,
                    "treated_capacity": treated_capacity,
                    "control_packet": control_packet,
                    "treated_packet": treated_packet,
                },
            )
            packet_rows.append(packet_record(packet_root / "projection-receipt.json"))
            backing = exact_backing_index(cell, projection.messages, packet_root / "exact-backing-index.json")
            backing_rows.append({"cell": cell, "receipt_count": len(backing["receipts"]), "all_uniquely_resolved": True})
            packet_rows.append(packet_record(packet_root / "exact-backing-index.json"))

            changed = {row["result_index"] for row in projection.changes}
            observed_changed = {index for index, (before, after) in enumerate(zip(raw_messages, projection.messages, strict=True)) if before != after}
            if changed != observed_changed:
                raise RuntimeError(f"declared/observed message delta mismatch for {cell}")
            boundary_rows.append(
                {
                    "cell": cell,
                    "seed": frozen["seed"],
                    "predecessor_cell": frozen["predecessor_cell"],
                    "predecessor_decision_action": pending_action,
                    "predecessor_decision_response_sha256": sha256_file(predecessor_cell_root(cell) / "responses" / "call-02.json"),
                    "pending_result": {
                        "result_sha256": frozen["pending_result_sha256"],
                        "result_size_bytes": frozen["pending_result_size_bytes"],
                        "assistant_message_sha256": sha256_bytes(assistant["content"].encode("utf-8")),
                        "result_message_sha256": sha256_bytes(result_message["content"].encode("utf-8")),
                    },
                    "candidate_id": env.initial_snapshot["candidate_id"],
                    "model_visible_before_treatment": False,
                    "first_new_model_call_after_treatment_sees_pending_result": True,
                    "full_structural_outline_remains_resident": True,
                }
            )
            capacity_rows.append(
                {
                    "cell": cell,
                    "predecessor_call_02": base_capacity,
                    "raw_control_after_pending_result": raw_capacity,
                    "treatment_after_pending_result": treated_capacity,
                    "newly_demoted_result_indices": sorted(changed),
                    "newly_demoted_count": len(changed),
                    "tokens_recovered": raw_capacity["prompt_tokens"] - treated_capacity["prompt_tokens"],
                    "control_capacity_censored_before_call": not raw_capacity["fits"],
                    "treatment_feasible": treated_capacity["fits"],
                    "response_reserve_unchanged": True,
                    "message_ledger": message_ledger(projection.messages),
                }
            )
            source_probes = []
            for source_path in SOURCE_PATHS:
                probe = env.execute({"action": "repo_read", "path": source_path})
                source_probes.append({"path": source_path, "accepted": probe.get("accepted"), "sha256": sha256_bytes(probe["content"].encode("utf-8"))})
            outside = env.execute({"action": "repo_history", "path": SOURCE_PATHS[0]})
            source_surface_rows.append(
                {
                    "cell": cell,
                    "exact_governing_source_reads": source_probes,
                    "historical_exact_reopens_available": len(env.exact_reopens),
                    "novel_index_history_outside_materialization": outside,
                }
            )

    write_json(
        ROOT / "BOUNDARY_MANIFEST.json",
        {
            "schema_version": "recurrent-context-pressure-boundary-v0",
            "study_id": STUDY_ID,
            "predecessor_repository": PREDECESSOR_REPOSITORY,
            "predecessor_commit": PREDECESSOR_COMMIT,
            "boundaries": boundary_rows,
        },
    )
    write_json(
        ROOT / "POLICY_FREEZE.json",
        {
            "schema_version": "recurrent-pressure-policy-freeze-v1",
            "policy_id": POLICY_ID,
            "trigger": "prospective next request plus frozen response reserve exceeds context envelope",
            "eligible_objects": "resident user-role action-result bodies with exact backing and a preceding declared assistant action",
            "selection_order": "oldest result message first",
            "selection_filter": "accept only substitutions with positive exact tokenizer savings; skip existing receipts",
            "stop_rule": "stop as soon as prospective packet prompt_tokens <= 20992",
            "pending_result_protected_in_same_cycle": True,
            "semantic_scoring": False,
            "summarization": False,
            "continuous_background_rewriting": False,
            "maximum_new_calls_per_seed": MAX_NEW_CALLS_PER_SEED,
        },
    )
    write_json(ROOT / "CAPACITY_PREFLIGHT.json", {"schema_version": "recurrent-capacity-preflight-v0", "context_tokens": CONTEXT_TOKENS, "response_reserve_tokens": RESPONSE_RESERVE, "maximum_prompt_tokens": MAXIMUM_PROMPT_TOKENS, "cells": capacity_rows})
    write_json(
        ROOT / "SOURCE_SURFACE_QUALIFICATION.json",
        {
            "schema_version": "recurrent-source-surface-qualification-v0",
            "qualified": True,
            "qualified_surfaces": ["all historical exact reopen actions", "candidate tree/search/read/read_lines/read_region", "patch", "replace_file", "submit", "novel repo_read and repo_read_lines for four materialized governing documents"],
            "unqualified_surfaces": ["novel repo_list", "novel repo_catalog", "novel repo_search", "novel repo_history", "novel reads outside the four materialized governing documents"],
            "runtime_rule": "any unqualified request is an apparatus invariant endpoint for the whole measured run; it is not interpreted as model failure",
            "material_change_from_parent": True,
            "interpretive_effect": "a run that reaches the unqualified surface cannot answer recurrent operability beyond that point",
            "cells": source_surface_rows,
        },
    )
    write_json(
        ROOT / "EXECUTION_SCHEDULE.json",
        {
            "schema_version": "recurrent-context-reduction-schedule-v0",
            "order": [
                {"ordinal": 1, "cell": "s42-s1", "condition": "recurrent_oldest_fit_v1", "maximum_new_model_calls": 3},
                {"ordinal": 2, "cell": "s314159-s1", "condition": "recurrent_oldest_fit_v1", "maximum_new_model_calls": 3},
            ],
            "maximum_measured_model_calls": MAXIMUM_MEASURED_CALLS,
            "attempts_per_cell": 1,
            "retries": 0,
            "stop_whole_run_on_apparatus_invariant_failure": True,
        },
    )
    write_json(
        ROOT / "FORECAST.json",
        {
            "schema_version": "recurrent-context-reduction-frozen-forecast-v0",
            "frozen_before_measured_inference": True,
            "mutually_exclusive_outcomes_in_precedence_order": [
                {"probability_percent": 35, "outcome": "both seeds use all three new calls with no reopen, mutation, or submission; further acquisitions dominate"},
                {"probability_percent": 25, "outcome": "at least one seed exactly reopens a demoted result before any mutation, and neither seed mutates or submits"},
                {"probability_percent": 15, "outcome": "at least one seed produces an admitted mutation or submission"},
                {"probability_percent": 15, "outcome": "without a preceding mutation/reopen, at least one seed ends early because recurrent reduction cannot admit a result or an action is rejected"},
                {"probability_percent": 10, "outcome": "provider, serialization, runtime, or apparatus-source-surface integrity dominates"},
            ],
            "probability_sum": 100,
        },
    )
    inherited_profile = load_json(PREDECESSOR_ROOT / "provenance" / "MODEL_PROFILE_LOCK.json")
    write_json(
        ROOT / "provenance" / "MODEL_PROFILE_LOCK.json",
        {
            "schema_version": "recurrent-context-reduction-model-profile-lock-v0",
            "inherited_from": {"repository": PREDECESSOR_REPOSITORY, "commit": PREDECESSOR_COMMIT, "path": "provenance/MODEL_PROFILE_LOCK.json", "sha256": sha256_file(PREDECESSOR_ROOT / "provenance" / "MODEL_PROFILE_LOCK.json")},
            "held_common": inherited_profile["held_common"],
            "seed_specific": inherited_profile["seed_specific"],
            "maximum_new_calls_per_seed": MAX_NEW_CALLS_PER_SEED,
            "pre_call_offload_gate": "66/66 main-model layers",
        },
    )
    write_json(
        ROOT / "provenance" / "TOKENIZER_QUALIFICATION.json",
        {
            "schema_version": "recurrent-tokenizer-qualification-v0",
            "mode": "cpu_only_sparse_tokenizer_projection_no_inference",
            "endpoint": base_url,
            "props_model_alias": props.get("model_alias"),
            "props_context": props.get("default_generation_settings", {}).get("n_ctx"),
            "server_executable": {"path": str(server_executable), "size_bytes": server_executable.stat().st_size, "sha256": sha256_file(server_executable)},
            "tokenizer_projection": {"path": str(tokenizer_projection), "size_bytes": tokenizer_projection.stat().st_size, "sha256": sha256_file(tokenizer_projection)},
            "apply_template_calls": endpoint.apply_calls,
            "tokenize_calls": endpoint.tokenize_calls,
            "chat_completions_called": False,
            "exact_boundary_reproductions": len(capacity_rows),
            "qualification_scope": "rendering and token accounting only; projection forbidden for measured inference",
        },
    )
    write_json(
        ROOT / "provenance" / "PREDECESSOR_SOURCE_LOCK.json",
        {
            "schema_version": "recurrent-predecessor-source-lock-v0",
            "predecessor_repository": PREDECESSOR_REPOSITORY,
            "predecessor_commit": PREDECESSOR_COMMIT,
            "parent_repository": PARENT_REPOSITORY,
            "parent_commit": PARENT_COMMIT,
            "source_commit": SOURCE_COMMIT,
            "materialization_receipt_sha256": sha256_file(ROOT / "provenance" / "PREDECESSOR_MATERIALIZATION_RECEIPT.json"),
            "imported_predecessor_postrun_verification_sha256": sha256_file(PREDECESSOR_ROOT / "POSTRUN_VERIFICATION.json"),
            "imported_predecessor_replay_sha256": sha256_file(PREDECESSOR_ROOT / "runs" / "2026-08-20-sealed-run-v0" / "replay" / "REPLAY.json"),
        },
    )
    write_json(
        ROOT / "DESIGN.json",
        {
            "schema_version": "recurrent-context-reduction-design-v0",
            "study_id": STUDY_ID,
            "question": "Can the same pressure-triggered oldest-first positive-savings receipt rule repeatedly admit newly requested exact results while preserving a bounded continuation?",
            "conditions": {"control": "exact raw post-result packet; capacity preflight only when infeasible", "treatment": POLICY_ID},
            "primary_measures": ["initial_pending_result_delivered_to_new_decision", "successive_new_action_results_delivered_to_later_decisions", "recurrent_pressure_events_resolved"],
            "descriptive_behavior": ["acquisition", "exact reopen", "mutation", "submission", "candidate effect"],
            "causal_limit": "after the frozen first recurrent packet there is no matched untreated behavioral comparator; later behavior is descriptive",
        },
    )
    write_json(
        ROOT / "TREATMENT_DELTA.json",
        {
            "schema_version": "recurrent-context-reduction-treatment-delta-v0",
            "held_fixed": ["task", "world", "candidate", "full structural outline", "model", "sampler", "seed", "reasoning off", "response reserve", "action schema", "chronology order", "exact pending result"],
            "changed": ["at each actual pressure event, selected older exact-backed result bodies become exact reopenable receipts until fit"],
            "not_changed": ["no summaries", "no semantic relevance", "no fixed recent window", "no outline demotion", "no token filler", "no context increase", "no reserve reduction"],
            "apparatus_qualification": "novel repository surface is limited as declared in SOURCE_SURFACE_QUALIFICATION.json",
        },
    )

    lock_targets = sorted(
        {
            *[path.relative_to(ROOT).as_posix() for path in (ROOT / "apparatus").glob("*.py")],
            *[path.relative_to(ROOT).as_posix() for path in (ROOT / "tests").glob("*.py")],
            "BOUNDARY_MANIFEST.json",
            "CAPACITY_PREFLIGHT.json",
            "DESIGN.json",
            "EXECUTION_SCHEDULE.json",
            "FORECAST.json",
            "POLICY_FREEZE.json",
            "SOURCE_SURFACE_QUALIFICATION.json",
            "TREATMENT_DELTA.json",
            "provenance/MODEL_PROFILE_LOCK.json",
            "provenance/PREDECESSOR_MATERIALIZATION_RECEIPT.json",
            "provenance/PREDECESSOR_SOURCE_LOCK.json",
            "provenance/TOKENIZER_QUALIFICATION.json",
            *[relative for relative in ("provenance/OFFLINE_RUNTIME_RELEASE.json", "provenance/RUNTIME_ASSET_AVAILABILITY.json") if (ROOT / relative).is_file()],
            *[relative for relative in ("README.md", "FREEZE.md", "TREATMENT_DELTA.md", "BORROWING_LEDGER.md", "RESULTS.md", "DIRECT_TRANSCRIPT_AUDIT.md", "POSTRUN_APPARATUS_NOTE.md", "PARENT_PROJECT_IMPLICATIONS.md", "QWEN38_RECURRENT_CONTEXT_REDUCTION_HANDOFF.md") if (ROOT / relative).is_file()],
        }
    )
    locked = {relative: sha256_file(ROOT / relative) for relative in lock_targets}
    source_lock = {
        "schema_version": "recurrent-context-reduction-source-lock-v0",
        "study_id": STUDY_ID,
        "branch": BRANCH,
        "predecessor_repository": PREDECESSOR_REPOSITORY,
        "predecessor_commit": PREDECESSOR_COMMIT,
        "locked_artifacts": locked,
        "packets": sorted(packet_rows, key=lambda row: row["path"]),
    }
    write_json(ROOT / "provenance" / "SOURCE_LOCK.json", source_lock)
    write_json(
        ROOT / "AUTHORIZATION_REQUEST.json",
        {
            "schema_version": "measured-inference-authorization-request-v0",
            "study_id": STUDY_ID,
            "approved": False,
            "requested_scope": {"eligible_seeds": list(CELLS), "maximum_new_calls_per_seed": MAX_NEW_CALLS_PER_SEED, "maximum_model_calls": MAXIMUM_MEASURED_CALLS, "one_attempt_per_cell": True, "retries": 0, "control_model_calls": 0},
            "source_lock_sha256": sha256_file(ROOT / "provenance" / "SOURCE_LOCK.json"),
            "execution_requires_full_model_sha256": "d416fa422c9035605c778f60d90a94b288c38b4f9ec2126b58ef938ce8d5f716",
            "sparse_tokenizer_projection_forbidden_for_inference": True,
            "user_approval_required": True,
        },
    )
    summary = {
        "schema_version": "recurrent-context-reduction-offline-verification-v0",
        "study_id": STUDY_ID,
        "verification_passed": True,
        "materialization": custody,
        "boundaries_reconstructed": len(boundary_rows),
        "capacity_cells_qualified": len(capacity_rows),
        "packet_count": len(packet_rows),
        "exact_backing_cells": backing_rows,
        "maximum_measured_model_calls": MAXIMUM_MEASURED_CALLS,
        "network_model_calls": 0,
        "gpu_model_calls": 0,
        "chat_completions_called": False,
        "measured_execution_authorized": False,
        "predecessor_worktree_unchanged": True,
    }
    write_json(ROOT / "OFFLINE_PREFLIGHT.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", default="http://127.0.0.1:18081")
    parser.add_argument("--server-executable", type=Path, required=True)
    parser.add_argument("--tokenizer-projection", type=Path, required=True)
    args = parser.parse_args()
    result = run_preflight(args.endpoint, args.server_executable.resolve(), args.tokenizer_projection.resolve())
    print(json.dumps({"verification_passed": result["verification_passed"], "boundaries": result["boundaries_reconstructed"], "packets": result["packet_count"]}, sort_keys=True))
    return 0 if result["verification_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
