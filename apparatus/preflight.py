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
    DONOR_ROOT,
    MAXIMUM_MEASURED_CALLS,
    MAXIMUM_PROMPT_TOKENS,
    MAX_NEW_CALLS_PER_SEED,
    PARENT_COMMIT,
    PARENT_REPOSITORY,
    PREDECESSOR_COMMIT,
    PREDECESSOR_INFERENCE_COMMIT,
    PREDECESSOR_REPOSITORY,
    PREDECESSOR_ROOT,
    PREDECESSOR_RUN,
    RESPONSE_RESERVE,
    ROOT,
    SOURCE_COMMIT,
    SOURCE_PATHS,
    STUDY_ID,
)
from apparatus.environment import make_environment
from apparatus.modelio import ParentTokenEndpoint
from apparatus.predecessor import (
    donor_assistant_message,
    donor_call,
    donor_cell_root,
    donor_result_message,
    exact_backing_id,
    parent_boundary_objects,
)
from apparatus.receipts import POLICY_ID, pressure_projection, receipt_from_message
from apparatus.seal import verify_seal


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
    predecessor_verify = load_json(ROOT / "parent_evidence" / "POSTRUN_VERIFICATION.json")
    predecessor_replay = load_json(ROOT / "parent_evidence" / PREDECESSOR_RUN / "replay" / "REPLAY.json")
    predecessor_result = load_json(ROOT / "parent_evidence" / PREDECESSOR_RUN / "RUN_RESULT.json")
    predecessor_seal = verify_seal(ROOT / "parent_evidence" / PREDECESSOR_RUN)
    if predecessor_verify.get("passed") is not True:
        failures.append("imported predecessor verification was not passing")
    if predecessor_replay.get("passed") is not True:
        failures.append("imported predecessor replay was not passing")
    if predecessor_result.get("model_calls") != 6:
        failures.append("imported predecessor run does not declare six measured calls")
    if predecessor_seal.get("passed") is not True:
        failures.append("imported predecessor run seal did not verify")
    return {
        "passed": not failures,
        "checked_files": len(receipt["files"]),
        "checked_bytes": receipt["total_bytes"],
        "all_byte_equivalent": receipt["all_byte_equivalent"],
        "predecessor_postrun_verification_passed": predecessor_verify.get("passed") is True,
        "predecessor_measured_replay_passed": predecessor_replay.get("passed") is True,
        "predecessor_declared_model_calls": predecessor_replay.get("declared_model_calls"),
        "predecessor_result_model_calls": predecessor_result.get("model_calls"),
        "predecessor_seal_passed": predecessor_seal.get("passed") is True,
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
    sources: list[tuple[str, list[dict[str, Any]]]] = [
        ("underlying_parent_boundary_request", parent_boundary_objects(cell)["request"]["messages"]),
    ]
    for ordinal in (1, 2, 3):
        sources.append((f"direct_predecessor_call_{ordinal:02d}_request", donor_call(cell, ordinal)["request"]["messages"]))
        sources.append((f"direct_predecessor_call_{ordinal:02d}_result", [donor_result_message(cell) if ordinal == 3 else _donor_result_message(cell, ordinal)]))
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
        preferred = next((match for match in matches if match["source"] == "direct_predecessor_call_03_request"), matches[0])
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
    document = {"schema_version": "recurrent-horizon-exact-backing-index-v0", "cell": cell, "receipts": rows}
    write_json(path, document)
    return document


def _donor_result_message(cell: str, ordinal: int) -> dict[str, str]:
    row = donor_call(cell, ordinal)["result"]
    backing = donor_cell_root(cell) / row["exact_backing"]["path"]
    if not backing.is_file() or sha256_file(backing) != row["exact_backing"]["sha256"]:
        raise RuntimeError(f"direct predecessor result backing mismatch: {cell}/call-{ordinal:02d}")
    return {"role": "user", "content": backing.read_text(encoding="utf-8")}


def run_preflight(base_url: str, server_executable: Path, tokenizer_projection: Path) -> dict[str, Any]:
    custody = verify_materialization()
    if not custody["passed"]:
        raise RuntimeError("predecessor custody failed")
    predecessor_checkout = Path(r"E:\qwen38-recurrent-context-reduction-v0")
    predecessor_status = process(["git", "status", "--short", "--branch"], predecessor_checkout)
    predecessor_head = process(["git", "rev-parse", "HEAD"], predecessor_checkout)
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
        base = donor_call(cell, 3)["request"]
        base_messages = base["messages"]
        base_capacity = endpoint.count(base_messages, base["chat_template_kwargs"]).as_dict()
        if base_capacity["prompt_tokens"] != frozen["donor_prompt_tokens"]:
            raise RuntimeError(f"direct predecessor call-03 token mismatch for {cell}")
        if base_capacity["headroom_after_reserve"] != frozen["donor_prompt_headroom"]:
            raise RuntimeError(f"direct predecessor call-03 headroom mismatch for {cell}")
        with tempfile.TemporaryDirectory(prefix=f"recurrent-horizon-{cell}-") as temporary:
            env = make_environment(cell, Path(temporary))
            pending_action = frozen["pending_action"]
            pending_result = env.execute(pending_action)
            assistant = donor_assistant_message(cell)
            result_message = donor_result_message(cell)
            reconstructed = env.result_message(pending_action, frozen["pending_action_id"], pending_result)
            if reconstructed != result_message:
                raise RuntimeError(f"direct predecessor call-03 result cannot be reconstructed exactly for {cell}")
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
            repeated = pressure_projection(
                cell,
                base_messages,
                tail,
                maximum_prompt_tokens=MAXIMUM_PROMPT_TOKENS,
                token_count=lambda messages: endpoint.count(messages, base["chat_template_kwargs"]).prompt_tokens,
                backing_id=lambda index, message: exact_backing_id(cell, index, message),
            )
            if not projection.fits or canonical_json_bytes(projection.messages) != canonical_json_bytes(repeated.messages):
                raise RuntimeError(f"deterministic horizon-start projection failed for {cell}")

            packet_root = ROOT / "preflight" / "packets" / cell
            control_request = copy.deepcopy(base)
            control_request["messages"] = raw_messages
            treated_request = copy.deepcopy(base)
            treated_request["messages"] = projection.messages
            control_packet = write_packet(packet_root / "control-raw-post-result-request.json", control_request)
            treated_packet = write_packet(packet_root / "horizon-start-request.json", treated_request)
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
                    "deterministic_second_render_equal": True,
                },
            )
            packet_rows.append(packet_record(packet_root / "projection-receipt.json"))
            backing = exact_backing_index(cell, projection.messages, packet_root / "exact-backing-index.json")
            backing_rows.append({"cell": cell, "receipt_count": len(backing["receipts"]), "all_resolved": True})
            packet_rows.append(packet_record(packet_root / "exact-backing-index.json"))

            changed = {row["result_index"] for row in projection.changes}
            observed_changed = {index for index, (before, after) in enumerate(zip(raw_messages, projection.messages, strict=True)) if before != after}
            if changed != observed_changed:
                raise RuntimeError(f"declared/observed message delta mismatch for {cell}")
            boundary_rows.append(
                {
                    "cell": cell,
                    "seed": frozen["seed"],
                    "predecessor_cell": frozen["donor_cell"],
                    "predecessor_call": 3,
                    "predecessor_decision_action": pending_action,
                    "predecessor_decision_response_sha256": sha256_file(donor_cell_root(cell) / "responses" / "call-03.json"),
                    "pending_result": {
                        "result_message_sha256": frozen["pending_result_message_sha256"],
                        "result_message_size_bytes": frozen["pending_result_message_size_bytes"],
                        "assistant_message_sha256": sha256_bytes(assistant["content"].encode("utf-8")),
                    },
                    "candidate_id": env.initial_snapshot["candidate_id"],
                    "delivered_in_predecessor": False,
                    "first_horizon_model_call_sees_pending_result": True,
                    "full_structural_outline_remains_resident": True,
                }
            )
            capacity_rows.append(
                {
                    "cell": cell,
                    "direct_predecessor_call_03": base_capacity,
                    "raw_control_after_pending_result": raw_capacity,
                    "horizon_start_after_pressure_policy": treated_capacity,
                    "newly_demoted_result_indices": sorted(changed),
                    "newly_demoted_count": len(changed),
                    "tokens_recovered": raw_capacity["prompt_tokens"] - treated_capacity["prompt_tokens"],
                    "control_capacity_censored_before_call": not raw_capacity["fits"],
                    "horizon_start_feasible": treated_capacity["fits"],
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
            "schema_version": "recurrent-context-reduction-horizon-boundary-v0",
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
    write_json(ROOT / "CAPACITY_PREFLIGHT.json", {"schema_version": "recurrent-horizon-capacity-preflight-v0", "context_tokens": CONTEXT_TOKENS, "response_reserve_tokens": RESPONSE_RESERVE, "maximum_prompt_tokens": MAXIMUM_PROMPT_TOKENS, "cells": capacity_rows})
    write_json(
        ROOT / "SOURCE_SURFACE_QUALIFICATION.json",
        {
            "schema_version": "recurrent-horizon-source-surface-qualification-v0",
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
            "schema_version": "recurrent-context-reduction-horizon-schedule-v0",
            "order": [
                {"ordinal": 1, "cell": "s42-s1", "condition": "recurrent_oldest_fit_horizon_v0", "maximum_new_model_calls": MAX_NEW_CALLS_PER_SEED},
                {"ordinal": 2, "cell": "s314159-s1", "condition": "recurrent_oldest_fit_horizon_v0", "maximum_new_model_calls": MAX_NEW_CALLS_PER_SEED},
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
            "schema_version": "recurrent-context-reduction-horizon-forecast-v0",
            "frozen_before_measured_inference": True,
            "mutually_exclusive_outcomes_in_precedence_order": [
                {"probability_percent": 10, "outcome": "apparatus, capacity, provider, serialization, runtime, or source-surface integrity ends the study before both horizons"},
                {"probability_percent": 5, "outcome": "at least one seed produces an admitted submission"},
                {"probability_percent": 15, "outcome": "no submission, but at least one seed produces an admitted mutation"},
                {"probability_percent": 25, "outcome": "no mutation or submission, and both seeds exhibit at least one formal short-cycle thrash episode"},
                {"probability_percent": 25, "outcome": "no mutation or submission, and exactly one seed exhibits formal short-cycle thrash"},
                {"probability_percent": 20, "outcome": "no mutation, submission, or formal short-cycle thrash; acquisition continues to the endpoint"},
            ],
            "probability_sum": 100,
        },
    )
    write_json(
        ROOT / "OUTCOME_CLASSIFICATION.json",
        {
            "schema_version": "recurrent-context-reduction-horizon-outcomes-v0",
            "canonical_action_key": "canonical JSON of the admitted or rejected requested action",
            "construction_onset": "first admitted patch or replace_file action",
            "closure": "first admitted submit action",
            "repeat_within_four": "an acquisition action key equals one of the preceding three acquisition action keys and candidate identity is unchanged throughout that window",
            "short_cycle_thrash_episode": "four consecutive acquisition decisions, including the direct predecessor tail where available, with unchanged candidate identity, no more than two distinct canonical action keys, and at least one repeated key",
            "local_nonchurn_window": "four consecutive acquisition decisions on an unchanged candidate with four distinct canonical action keys and no exact-receipt reopen",
            "fault_in_churn": "an exact result is demoted to a receipt and its mechanically bound reopen_action is later requested; repeated fault-in is counted by action key",
            "novel_acquisition": "an acquisition action key absent from all earlier direct-predecessor and horizon decisions for that seed",
            "duplicate_acquisition": "an acquisition action key already issued on the unchanged candidate basis",
            "terminal_classes_in_precedence_order": [
                "apparatus_censored",
                "submission",
                "mutation_without_submission",
                "formal_thrash_without_mutation",
                "continued_acquisition_without_formal_thrash",
                "other",
            ],
            "interpretation_limit": "mechanical repetition is not evidence that the requested information was semantically unnecessary",
            "convergence_limit": "a local nonchurn window is evidence consistent with bounded noncycling continuation, not proof of asymptotic convergence or semantic sufficiency",
        },
    )
    inherited_profile_path = DONOR_ROOT / "provenance" / "MODEL_PROFILE_LOCK.json"
    inherited_profile = load_json(inherited_profile_path)
    write_json(
        ROOT / "provenance" / "MODEL_PROFILE_LOCK.json",
        {
            "schema_version": "recurrent-context-reduction-horizon-model-profile-lock-v0",
            "inherited_from": {"repository": PREDECESSOR_REPOSITORY, "commit": PREDECESSOR_COMMIT, "path": "provenance/MODEL_PROFILE_LOCK.json", "sha256": sha256_file(inherited_profile_path)},
            "held_common": inherited_profile["held_common"],
            "seed_specific": inherited_profile["seed_specific"],
            "maximum_new_calls_per_seed": MAX_NEW_CALLS_PER_SEED,
            "pre_call_offload_gate": "66/66 main-model layers",
        },
    )
    write_json(
        ROOT / "provenance" / "TOKENIZER_QUALIFICATION.json",
        {
            "schema_version": "recurrent-horizon-tokenizer-qualification-v0",
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
            "schema_version": "recurrent-horizon-predecessor-source-lock-v0",
            "predecessor_repository": PREDECESSOR_REPOSITORY,
            "predecessor_commit": PREDECESSOR_COMMIT,
            "predecessor_inference_commit": PREDECESSOR_INFERENCE_COMMIT,
            "predecessor_run": PREDECESSOR_RUN,
            "parent_repository": PARENT_REPOSITORY,
            "parent_commit": PARENT_COMMIT,
            "source_commit": SOURCE_COMMIT,
            "materialization_receipt_sha256": sha256_file(ROOT / "provenance" / "PREDECESSOR_MATERIALIZATION_RECEIPT.json"),
            "imported_predecessor_postrun_verification_sha256": sha256_file(DONOR_ROOT / "POSTRUN_VERIFICATION.json"),
            "imported_predecessor_replay_sha256": sha256_file(DONOR_ROOT / PREDECESSOR_RUN / "replay" / "REPLAY.json"),
            "imported_predecessor_run_result_sha256": sha256_file(DONOR_ROOT / PREDECESSOR_RUN / "RUN_RESULT.json"),
        },
    )
    write_json(
        ROOT / "DESIGN.json",
        {
            "schema_version": "recurrent-context-reduction-horizon-design-v0",
            "study_id": STUDY_ID,
            "question": "Beyond the predecessor's three-call window, does repeated minimum-necessary exact-receipt reduction converge to a stable productive working set, mechanically thrash, or eventually enable construction?",
            "continuation": {"starts_after_predecessor_call": 3, "maximum_additional_calls_per_seed": MAX_NEW_CALLS_PER_SEED, "maximum_combined_calls_from_predecessor_start": 3 + MAX_NEW_CALLS_PER_SEED},
            "conditions": {"raw_capacity_control": "exact predecessor call-03 request plus its exact accepted result; no model call when infeasible", "continuation_treatment": POLICY_ID},
            "primary_measures": ["admitted_mutation_before_endpoint", "admitted_submission_before_endpoint", "formal_short_cycle_thrash", "pressure_events_resolved", "exact_results_delivered_to_later_decisions"],
            "descriptive_behavior": ["novel acquisition", "duplicate acquisition", "exact reopen", "fault-in churn", "mutation", "submission", "candidate effect"],
            "causal_limit": "This is a descriptive continuation under one fixed policy, not a randomized policy comparison or a general context-manager validation.",
        },
    )
    write_json(
        ROOT / "TREATMENT_DELTA.json",
        {
            "schema_version": "recurrent-context-reduction-horizon-treatment-delta-v0",
            "held_fixed": ["task", "world", "candidate", "full structural outline", "model", "sampler", "seed", "reasoning off", "response reserve", "action schema", "chronology order", "exact pending result"],
            "changed": ["the already-frozen rule continues for up to twelve additional calls per seed starting from the sealed predecessor call-03 result-delivery boundary"],
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
            "OUTCOME_CLASSIFICATION.json",
            "POLICY_FREEZE.json",
            "SOURCE_SURFACE_QUALIFICATION.json",
            "TREATMENT_DELTA.json",
            "provenance/MODEL_PROFILE_LOCK.json",
            "provenance/PREDECESSOR_MATERIALIZATION_RECEIPT.json",
            "provenance/PREDECESSOR_SOURCE_LOCK.json",
            "provenance/TOKENIZER_QUALIFICATION.json",
            *[relative for relative in ("provenance/OFFLINE_RUNTIME_RELEASE.json", "provenance/RUNTIME_ASSET_AVAILABILITY.json") if (ROOT / relative).is_file()],
            *[relative for relative in ("README.md", "FREEZE.md", "TREATMENT_DELTA.md", "RESULTS.md", "DIRECT_TRANSCRIPT_AUDIT.md", "POSTRUN_APPARATUS_NOTE.md", "PARENT_PROJECT_IMPLICATIONS.md", "QWEN38_RECURRENT_CONTEXT_REDUCTION_HORIZON_HANDOFF.md", "provenance/BORROWING_LEDGER.md") if (ROOT / relative).is_file()],
        }
    )
    locked = {relative: sha256_file(ROOT / relative) for relative in lock_targets}
    source_lock = {
        "schema_version": "recurrent-context-reduction-horizon-source-lock-v0",
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
        "schema_version": "recurrent-context-reduction-horizon-offline-verification-v0",
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
