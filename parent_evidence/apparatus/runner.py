from __future__ import annotations

import argparse
import copy
import json
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from apparatus.canonical import canonical_json_bytes, compact_json, load_json, sha256_bytes, sha256_file, write_json
from apparatus.constants import (
    CELLS,
    CONTEXT_TOKENS,
    MAXIMUM_MEASURED_CALLS,
    MAXIMUM_PROMPT_TOKENS,
    MAX_NEW_CALLS_PER_SEED,
    ROOT,
    STUDY_ID,
)
from apparatus.environment import ActionRejected, make_environment, validate_action
from apparatus.modelio import ParentTokenEndpoint
from apparatus.predecessor import exact_backing_id
from apparatus.receipts import pressure_projection, receipt_from_message


EXPECTED_SERVER_SHA256 = "5f1f831bc21dcbff4ca40e05cb59dbcbc0802d20b2046540bbbf3bd45cd61610"
EXPECTED_MODEL_SHA256 = "d416fa422c9035605c778f60d90a94b288c38b4f9ec2126b58ef938ce8d5f716"
EXPECTED_MODEL_SIZE = 11_141_912_032
MODEL_ALIAS = "qwen38-ad25q8-world-join"
INTEGRITY_REJECTION_CODES = {"source_surface_not_materialized", "unsupported_declared_action"}


@dataclass(frozen=True)
class HttpRecord:
    status_code: int
    headers: dict[str, str]
    body: bytes
    duration_ms: int
    transport_error: str | None

    @property
    def success(self) -> bool:
        return self.transport_error is None and 200 <= self.status_code < 300


def _http(request: urllib.request.Request, timeout_seconds: int = 900) -> HttpRecord:
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return HttpRecord(
                int(response.status),
                {key.lower(): value for key, value in response.headers.items()},
                response.read(),
                round((time.perf_counter() - started) * 1000),
                None,
            )
    except urllib.error.HTTPError as exc:
        return HttpRecord(
            int(exc.code),
            {key.lower(): value for key, value in exc.headers.items()} if exc.headers else {},
            exc.read(),
            round((time.perf_counter() - started) * 1000),
            None,
        )
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return HttpRecord(0, {}, b"", round((time.perf_counter() - started) * 1000), f"{type(exc).__name__}: {exc}")


def get_json(base_url: str, path: str) -> dict[str, Any]:
    response = _http(urllib.request.Request(base_url.rstrip("/") + path, method="GET"), 60)
    if not response.success:
        raise RuntimeError(f"GET {path} failed: status={response.status_code} error={response.transport_error}")
    value = json.loads(response.body)
    if not isinstance(value, dict):
        raise RuntimeError(f"GET {path} returned a non-object")
    return value


def post_chat(base_url: str, body: bytes) -> HttpRecord:
    return _http(
        urllib.request.Request(
            base_url.rstrip("/") + "/v1/chat/completions",
            data=body,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
    )


def current_head() -> str:
    process = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, text=True
    )
    if process.returncode:
        raise RuntimeError("standalone repository has no committed HEAD")
    return process.stdout.strip()


def require_clean_head() -> str:
    head = current_head()
    process = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=True,
    )
    if process.returncode or process.stdout.strip():
        raise RuntimeError("measured execution requires a clean committed standalone HEAD")
    return head


def verify_source_lock() -> tuple[dict[str, Any], str]:
    lock_path = ROOT / "provenance" / "SOURCE_LOCK.json"
    lock = load_json(lock_path)
    for relative, expected in lock["locked_artifacts"].items():
        path = ROOT / relative
        if not path.is_file() or sha256_file(path) != expected:
            raise RuntimeError(f"source-lock mismatch: {relative}")
    for packet in lock["packets"]:
        path = ROOT / packet["path"]
        if not path.is_file() or sha256_file(path) != packet["sha256"] or path.stat().st_size != packet["size_bytes"]:
            raise RuntimeError(f"frozen packet mismatch: {packet['path']}")
    return lock, sha256_file(lock_path)


def authorization_errors(authorization: dict[str, Any], lock_sha: str) -> list[str]:
    required = {
        "schema_version": "measured-inference-authorization-v0",
        "study_id": STUDY_ID,
        "approved": True,
        "source_lock_sha256": lock_sha,
        "maximum_model_calls": MAXIMUM_MEASURED_CALLS,
        "retries": 0,
    }
    errors = [f"field {key} must equal {expected!r}" for key, expected in required.items() if authorization.get(key) != expected]
    if not isinstance(authorization.get("approval_statement"), str) or not authorization["approval_statement"].strip():
        errors.append("approval_statement must be nonempty")
    return errors


def require_authorization() -> dict[str, Any]:
    request = load_json(ROOT / "AUTHORIZATION_REQUEST.json")
    lock, lock_sha = verify_source_lock()
    if request["source_lock_sha256"] != lock_sha:
        raise RuntimeError("authorization request does not bind the current source lock")
    path = ROOT / "execution" / "AUTHORIZATION.json"
    if not path.is_file():
        raise RuntimeError("measured inference is not authorized: execution/AUTHORIZATION.json is absent")
    authorization = load_json(path)
    errors = authorization_errors(authorization, lock_sha)
    if errors:
        raise RuntimeError("authorization mismatch: " + "; ".join(errors))
    return {"authorization": authorization, "source_lock": lock, "source_lock_sha256": lock_sha}


def verify_runtime_files(server_executable: Path, model: Path) -> dict[str, Any]:
    if not server_executable.is_file() or sha256_file(server_executable) != EXPECTED_SERVER_SHA256:
        raise RuntimeError("llama-server executable does not match the parent package")
    forbidden = model.name.endswith(".partial") or "tokenizer-projection" in model.name
    if forbidden or not model.is_file() or model.stat().st_size != EXPECTED_MODEL_SIZE:
        raise RuntimeError("full exact model file is unavailable or a tokenizer-only projection was supplied")
    if sha256_file(model) != EXPECTED_MODEL_SHA256:
        raise RuntimeError("model does not match the parent SHA-256")
    return {
        "server_executable": {"path": str(server_executable), "size_bytes": server_executable.stat().st_size, "sha256": EXPECTED_SERVER_SHA256},
        "model": {"path": str(model), "size_bytes": model.stat().st_size, "sha256": EXPECTED_MODEL_SHA256},
    }


def verify_endpoint(base_url: str, model: Path) -> dict[str, Any]:
    health = get_json(base_url, "/health")
    props = get_json(base_url, "/props")
    generation = props.get("default_generation_settings", {})
    errors: list[str] = []
    if health.get("status") != "ok":
        errors.append(f"health={health.get('status')!r}")
    if props.get("model_alias") != MODEL_ALIAS:
        errors.append(f"alias={props.get('model_alias')!r}")
    if props.get("build_info") != "b10434-7e4c0a968":
        errors.append(f"build_info={props.get('build_info')!r}")
    if generation.get("n_ctx") != CONTEXT_TOKENS:
        errors.append(f"n_ctx={generation.get('n_ctx')!r}")
    reported_model = props.get("model_path")
    if reported_model and Path(str(reported_model)).resolve() != model.resolve():
        errors.append(f"model_path={reported_model!r}")
    if errors:
        raise RuntimeError("model endpoint failed frozen identity checks: " + "; ".join(errors))
    return props


def parse_bare_action(content: str) -> dict[str, Any]:
    stripped = content.strip()
    decoder = json.JSONDecoder()
    value, end = decoder.raw_decode(stripped)
    if stripped[end:].strip():
        raise ValueError("assistant response contains trailing content")
    if not isinstance(value, dict):
        raise ValueError("assistant response is not a JSON object")
    return value


def parse_response(response: HttpRecord, cell: str) -> dict[str, Any]:
    if not response.success:
        return {"valid": False, "error": "provider_http_failure", "details": {"status_code": response.status_code, "transport_error": response.transport_error}}
    try:
        payload = json.loads(response.body)
    except Exception as exc:
        return {"valid": False, "error": "invalid_provider_json", "details": str(exc)}
    choices = payload.get("choices") if isinstance(payload, dict) else None
    if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
        return {"valid": False, "error": "invalid_choice_count", "details": None}
    choice = choices[0]
    message = choice.get("message")
    if choice.get("finish_reason") != "stop" or not isinstance(message, dict) or message.get("role") != "assistant":
        return {"valid": False, "error": "invalid_assistant_turn", "details": {"finish_reason": choice.get("finish_reason"), "message": message}}
    if message.get("reasoning_content") not in (None, "") or message.get("tool_calls") not in (None, []):
        return {"valid": False, "error": "unexpected_reasoning_or_native_tools", "details": message}
    content = message.get("content")
    if not isinstance(content, str):
        return {"valid": False, "error": "missing_action_content", "details": message}
    try:
        action = validate_action(cell, parse_bare_action(content))
    except (ValueError, json.JSONDecodeError, ActionRejected) as exc:
        return {"valid": False, "error": "invalid_schema_action", "details": f"{type(exc).__name__}: {exc}", "raw_content": content}
    return {"valid": True, "payload": payload, "assistant_message": {"role": "assistant", "content": content}, "action": action, "usage": payload.get("usage"), "finish_reason": "stop"}


def action_class(action: dict[str, Any], resident_messages: list[dict[str, Any]]) -> str:
    name = action.get("action")
    if name in {"patch", "replace_file"}:
        return "mutation"
    if name == "submit":
        return "submission"
    reopen_actions: list[dict[str, Any]] = []
    for message in resident_messages:
        receipt = receipt_from_message(message)
        if receipt is not None and isinstance(receipt.get("reopen_action"), dict):
            reopen_actions.append(receipt["reopen_action"])
    if any(compact_json(action) == compact_json(item) for item in reopen_actions):
        return "exact_reopen_of_demoted_result"
    if name in {"tree", "search", "read", "read_lines", "read_region", "repo_list", "repo_catalog", "repo_read_lines", "continue_lines", "repo_search", "repo_read", "repo_history"}:
        return "other_acquisition"
    return "other"


def _write_http(root: Path, ordinal: int, request_bytes: bytes, response: HttpRecord) -> None:
    (root / "requests").mkdir(parents=True, exist_ok=True)
    (root / "responses").mkdir(parents=True, exist_ok=True)
    (root / "raw").mkdir(parents=True, exist_ok=True)
    (root / "requests" / f"call-{ordinal:02d}.json").write_bytes(request_bytes)
    (root / "responses" / f"call-{ordinal:02d}.json").write_bytes(response.body)
    write_json(
        root / "raw" / f"call-{ordinal:02d}-http.json",
        {
            "request_sha256": sha256_bytes(request_bytes),
            "request_size_bytes": len(request_bytes),
            "response_sha256": sha256_bytes(response.body),
            "response_size_bytes": len(response.body),
            "status_code": response.status_code,
            "headers": response.headers,
            "duration_ms": response.duration_ms,
            "transport_error": response.transport_error,
        },
    )


def _packet_request(cell: str) -> dict[str, Any]:
    return load_json(ROOT / "preflight" / "packets" / cell / "cycle-01-delivery-request.json")


def _store_exact_result(root: Path, result_message: dict[str, str]) -> dict[str, Any]:
    raw = result_message["content"].encode("utf-8")
    digest = sha256_bytes(raw)
    path = root / "objects" / f"{digest}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != raw:
        raise RuntimeError("exact result object collision")
    path.write_bytes(raw)
    return {"path": path.relative_to(root).as_posix(), "sha256": digest, "size_bytes": len(raw)}


def run_cell(cell: str, ordinal: int, run_root: Path, base_url: str, token_endpoint: ParentTokenEndpoint) -> dict[str, Any]:
    frozen = CELLS[cell]
    cell_root = run_root / "cells" / f"{ordinal:02d}-{cell}-recurrent-oldest-fit-v1"
    for child in ("actions", "budget", "candidates", "objects", "projections", "raw", "requests", "responses", "results", "world"):
        (cell_root / child).mkdir(parents=True, exist_ok=True)
    environment = make_environment(cell, cell_root / "world")
    write_json(cell_root / "candidates" / "initial.json", environment.initial_snapshot)

    request = _packet_request(cell)
    messages = copy.deepcopy(request["messages"])
    kwargs = request["chat_template_kwargs"]
    initial_capacity = token_endpoint.count(messages, kwargs).as_dict()
    if initial_capacity["prompt_tokens"] != frozen["treated_post_result_prompt_tokens"] or not initial_capacity["fits"]:
        raise RuntimeError(f"frozen first recurrent packet mismatch for {cell}")

    base_action_number = int(str(frozen["pending_action_id"]).rsplit("-", 1)[1])
    endpoint = "model_call_limit"
    calls: list[dict[str, Any]] = []
    pressure_events: list[dict[str, Any]] = []
    delivered_result_count = 1
    apparatus_invariant_failure = False

    for call_ordinal in range(1, MAX_NEW_CALLS_PER_SEED + 1):
        capacity = token_endpoint.count(messages, kwargs).as_dict()
        if not capacity["fits"]:
            endpoint = "capacity_invariant_failed_before_call"
            apparatus_invariant_failure = True
            break
        call_request = copy.deepcopy(request)
        call_request["messages"] = copy.deepcopy(messages)
        request_bytes = canonical_json_bytes(call_request)
        response = post_chat(base_url, request_bytes)
        token_endpoint.chat_completion_calls += 1
        _write_http(cell_root, call_ordinal, request_bytes, response)
        parsed = parse_response(response, cell)
        if not parsed["valid"]:
            endpoint = "model_or_server_integrity_failure"
            write_json(cell_root / "actions" / f"call-{call_ordinal:02d}.json", parsed)
            apparatus_invariant_failure = True
            break

        action = parsed["action"]
        classification = action_class(action, messages)
        candidate_before = environment.snapshot()
        result = environment.execute(action)
        candidate_after = environment.snapshot()
        action_id = f"schema-action-{base_action_number + call_ordinal:03d}"
        result_message = environment.result_message(action, action_id, result)
        backing = _store_exact_result(cell_root, result_message)
        action_record = {
            "call": call_ordinal,
            "action": action,
            "classification": classification,
            "candidate_before": candidate_before["candidate_id"],
            "candidate_after": candidate_after["candidate_id"],
            "admitted": result.get("accepted") is True,
        }
        write_json(cell_root / "actions" / f"call-{call_ordinal:02d}.json", action_record)
        write_json(cell_root / "results" / f"call-{call_ordinal:02d}.json", {"action_id": action_id, "action": action, "result": result, "exact_backing": backing})

        call_record: dict[str, Any] = {
            **action_record,
            "request_capacity": capacity,
            "provider_usage": parsed["usage"],
            "http_duration_ms": response.duration_ms,
            "result_message_sha256": backing["sha256"],
            "result_message_size_bytes": backing["size_bytes"],
            "result_delivered_to_later_call": False,
        }
        calls.append(call_record)

        error_code = result.get("error", {}).get("code") if isinstance(result.get("error"), dict) else None
        if error_code in INTEGRITY_REJECTION_CODES:
            endpoint = "apparatus_source_surface_invariant_failure"
            apparatus_invariant_failure = True
            break
        if action["action"] == "submit" and result.get("accepted") is True:
            endpoint = "admitted_submission"
            break

        tail = [parsed["assistant_message"], result_message]
        raw_capacity = token_endpoint.count(messages + tail, kwargs).as_dict()
        cycle_record: dict[str, Any] = {
            "after_call": call_ordinal,
            "raw_post_result": raw_capacity,
            "pressure_triggered": not raw_capacity["fits"],
            "result_message_sha256": backing["sha256"],
            "result_message_size_bytes": backing["size_bytes"],
        }

        if call_ordinal == MAX_NEW_CALLS_PER_SEED:
            cycle_record["delivery_status"] = "not_attempted_due_to_frozen_call_limit"
            write_json(cell_root / "budget" / f"after-call-{call_ordinal:02d}.json", cycle_record)
            endpoint = "model_call_limit_result_custodied_not_delivered"
            break

        if raw_capacity["fits"]:
            messages = messages + tail
            cycle_record.update({"policy_applied": False, "post_policy": raw_capacity, "delivery_status": "delivered_to_next_call"})
        else:
            projection = pressure_projection(
                cell,
                messages,
                tail,
                maximum_prompt_tokens=MAXIMUM_PROMPT_TOKENS,
                token_count=lambda candidate: token_endpoint.count(candidate, kwargs).prompt_tokens,
                backing_id=lambda index, message: exact_backing_id(cell, index, message),
            )
            projection_request = copy.deepcopy(request)
            projection_request["messages"] = projection.messages
            write_json(
                cell_root / "projections" / f"after-call-{call_ordinal:02d}.json",
                {
                    "policy_id": projection.policy_id,
                    "before_tokens": projection.before_tokens,
                    "after_tokens": projection.after_tokens,
                    "fits": projection.fits,
                    "changes": projection.changes,
                    "selection_trace": projection.selection_trace,
                    "request": projection_request,
                },
            )
            cycle_record.update(
                {
                    "policy_applied": True,
                    "policy_id": projection.policy_id,
                    "changes": projection.changes,
                    "post_policy": token_endpoint.count(projection.messages, kwargs).as_dict(),
                    "delivery_status": "delivered_to_next_call" if projection.fits else "capacity_unrestored",
                }
            )
            pressure_events.append(cycle_record)
            if not projection.fits:
                endpoint = "capacity_unrestored_before_result_delivery"
                write_json(cell_root / "budget" / f"after-call-{call_ordinal:02d}.json", cycle_record)
                break
            messages = projection.messages

        calls[-1]["result_delivered_to_later_call"] = True
        delivered_result_count += 1
        write_json(cell_root / "budget" / f"after-call-{call_ordinal:02d}.json", cycle_record)

    terminal = environment.snapshot()
    write_json(cell_root / "candidates" / "terminal.json", terminal)
    result = {
        "cell": cell,
        "seed": frozen["seed"],
        "model_calls": len(calls),
        "maximum_model_calls": MAX_NEW_CALLS_PER_SEED,
        "endpoint": endpoint,
        "apparatus_invariant_failure": apparatus_invariant_failure,
        "initial_recurrent_packet_capacity": initial_capacity,
        "delivered_result_count_including_frozen_pending_result": delivered_result_count,
        "pressure_events_triggered_after_new_calls": sum(1 for item in pressure_events if item["pressure_triggered"]),
        "pressure_events_resolved_after_new_calls": sum(1 for item in pressure_events if item.get("delivery_status") == "delivered_to_next_call"),
        "calls": calls,
        "initial_candidate_id": environment.initial_snapshot["candidate_id"],
        "final_candidate_id": terminal["candidate_id"],
    }
    write_json(cell_root / "CELL_RESULT.json", result)
    return result


def run_experiment(run_id: str, base_url: str, runtime_custody: dict[str, Any]) -> dict[str, Any]:
    run_root = ROOT / "runs" / run_id
    if run_root.exists():
        raise RuntimeError(f"run directory already exists: {run_root}")
    head = require_clean_head()
    authorization = require_authorization()
    (run_root / "model").mkdir(parents=True)
    write_json(run_root / "model" / "AUTHORIZATION.json", authorization["authorization"])
    write_json(run_root / "model" / "runtime-custody.json", runtime_custody)
    token_endpoint = ParentTokenEndpoint(base_url)
    rows: list[dict[str, Any]] = []
    total_calls = 0
    for ordinal, cell in enumerate(("s42-s1", "s314159-s1"), start=1):
        row = run_cell(cell, ordinal, run_root, base_url, token_endpoint)
        rows.append(row)
        total_calls += row["model_calls"]
        if total_calls > MAXIMUM_MEASURED_CALLS:
            raise RuntimeError("measured call authorization exceeded")
        if row["apparatus_invariant_failure"]:
            break
    result = {
        "schema_version": "recurrent-context-reduction-run-result-v0",
        "study_id": STUDY_ID,
        "run_id": run_id,
        "standalone_commit": head,
        "source_lock_sha256": authorization["source_lock_sha256"],
        "cells": rows,
        "model_calls": total_calls,
        "maximum_authorized_model_calls": MAXIMUM_MEASURED_CALLS,
        "retries": 0,
        "token_endpoint_calls": {
            "apply_template": token_endpoint.apply_calls,
            "tokenize": token_endpoint.tokenize_calls,
            "chat_completions": token_endpoint.chat_completion_calls,
        },
    }
    write_json(run_root / "RUN_RESULT.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:18080")
    parser.add_argument("--runtime-custody", type=Path, required=True)
    args = parser.parse_args()
    result = run_experiment(args.run_id, args.base_url.rstrip("/"), load_json(args.runtime_custody.resolve()))
    print(json.dumps({"run_id": result["run_id"], "model_calls": result["model_calls"], "cells": len(result["cells"])}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
