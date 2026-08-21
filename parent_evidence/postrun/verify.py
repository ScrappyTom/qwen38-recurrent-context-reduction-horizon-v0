from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from apparatus.canonical import load_json, sha256_file, write_json
from apparatus.replay import replay_run, verify_materialization
from apparatus.seal import verify_seal


ROOT = Path(__file__).resolve().parents[1]
DECLARED_POSTRUN_MUTABLE = {
    "DIRECT_TRANSCRIPT_AUDIT.md",
    "PARENT_PROJECT_IMPLICATIONS.md",
    "POSTRUN_APPARATUS_NOTE.md",
    "README.md",
    "RESULTS.md",
}


def process(command: list[str]) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=True,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "passed": completed.returncode == 0,
    }


def git_blob(commit: str, relative: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(f"cannot read {relative} at {commit}: {completed.stderr.decode(errors='replace')}")
    return completed.stdout


def verify_frozen_commit_lock(commit: str) -> dict[str, Any]:
    lock_path = ROOT / "provenance" / "SOURCE_LOCK.json"
    lock = load_json(lock_path)
    failures: list[str] = []
    for relative, expected in lock["locked_artifacts"].items():
        try:
            actual = hashlib.sha256(git_blob(commit, relative)).hexdigest()
        except RuntimeError as exc:
            failures.append(str(exc))
            continue
        if actual != expected:
            failures.append(f"frozen commit hash mismatch: {relative}")
    for packet in lock["packets"]:
        try:
            data = git_blob(commit, packet["path"])
        except RuntimeError as exc:
            failures.append(str(exc))
            continue
        if hashlib.sha256(data).hexdigest() != packet["sha256"] or len(data) != packet["size_bytes"]:
            failures.append(f"frozen packet mismatch: {packet['path']}")
    return {
        "passed": not failures,
        "commit": commit,
        "source_lock_sha256": sha256_file(lock_path),
        "locked_artifact_count": len(lock["locked_artifacts"]),
        "packet_count": len(lock["packets"]),
        "failures": failures,
    }


def audit_current_locked_paths() -> dict[str, Any]:
    lock = load_json(ROOT / "provenance" / "SOURCE_LOCK.json")
    mismatches = sorted(
        relative
        for relative, expected in lock["locked_artifacts"].items()
        if not (ROOT / relative).is_file() or sha256_file(ROOT / relative) != expected
    )
    unexpected = sorted(set(mismatches) - DECLARED_POSTRUN_MUTABLE)
    missing_declared = sorted(DECLARED_POSTRUN_MUTABLE - set(mismatches))
    return {
        "passed": not unexpected and not missing_declared,
        "declared_postrun_mutable": sorted(DECLARED_POSTRUN_MUTABLE),
        "observed_mismatches": mismatches,
        "unexpected_mismatches": unexpected,
        "declared_but_unchanged": missing_declared,
    }


def json_audit(run_root: Path) -> dict[str, Any]:
    files = sorted(
        {
            *ROOT.glob("*.json"),
            *(ROOT / "provenance").glob("*.json"),
            *(ROOT / "preflight" / "packets").rglob("*.json"),
            *run_root.rglob("*.json"),
        }
    )
    failures: list[str] = []
    for path in files:
        try:
            json.loads(path.read_bytes())
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT).as_posix()}: {type(exc).__name__}: {exc}")
    return {"passed": not failures, "file_count": len(files), "failures": failures}


def verify(run_root: Path) -> dict[str, Any]:
    run_root = run_root.resolve()
    run = load_json(run_root / "RUN_RESULT.json")
    lifecycle = load_json(run_root / "model" / "runtime-lifecycle.json")
    authorization = load_json(run_root / "model" / "AUTHORIZATION.json")
    frozen_verifier = load_json(run_root / "analysis" / "FROZEN_PREFLIGHT_VERIFICATION.json")
    compile_result = process(["python", "-m", "compileall", "-q", "apparatus", "postrun", "tests"])
    analysis_tests = process(
        ["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_analysis.py", "-v"]
    )
    postrun_tests = process(
        ["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_postrun.py", "-v"]
    )
    frozen_lock = verify_frozen_commit_lock(run["standalone_commit"])
    current_paths = audit_current_locked_paths()
    materialization_failures = verify_materialization()
    measured_replay = replay_run(run_root)
    seal = verify_seal(run_root)
    json_result = json_audit(run_root)
    authorization_passed = (
        authorization.get("approved") is True
        and authorization.get("authorized_commit") == run["standalone_commit"]
        and authorization.get("source_lock_sha256") == run["source_lock_sha256"]
        and authorization.get("maximum_model_calls") == 6
        and authorization.get("retries") == 0
    )
    runtime_passed = (
        lifecycle.get("passed") is True
        and lifecycle.get("port_open_before") is False
        and lifecycle.get("port_open_after") is False
        and lifecycle.get("main_offloaded_layers_before_calls") == [66, 66]
        and lifecycle.get("main_offloaded_layers") == [66, 66]
        and lifecycle.get("llama_processes_after") == []
        and lifecycle.get("gpu_before", {}).get("stdout") == lifecycle.get("gpu_after_stop", {}).get("stdout")
    )
    run_bounds_passed = run.get("model_calls") == 6 and run.get("retries") == 0 and len(run.get("cells", [])) == 2
    passed = all(
        (
            compile_result["passed"],
            analysis_tests["passed"],
            postrun_tests["passed"],
            frozen_lock["passed"],
            current_paths["passed"],
            not materialization_failures,
            measured_replay["passed"],
            seal["passed"],
            json_result["passed"],
            frozen_verifier.get("passed") is True,
            authorization_passed,
            runtime_passed,
            run_bounds_passed,
        )
    )
    return {
        "schema_version": "recurrent-context-reduction-postrun-verification-v0",
        "passed": passed,
        "run_id": run["run_id"],
        "frozen_commit": run["standalone_commit"],
        "compile": compile_result,
        "analysis_tests": analysis_tests,
        "postrun_tests": postrun_tests,
        "frozen_commit_source_lock": frozen_lock,
        "current_locked_path_audit": current_paths,
        "materialization": {"passed": not materialization_failures, "failures": materialization_failures},
        "frozen_preflight_verifier": frozen_verifier,
        "measured_replay": measured_replay,
        "run_seal": seal,
        "json_audit": json_result,
        "authorization_passed": authorization_passed,
        "runtime_lifecycle_passed": runtime_passed,
        "run_bounds_passed": run_bounds_passed,
        "measured_model_calls": run["model_calls"],
        "retries": run["retries"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "POSTRUN_VERIFICATION.json")
    args = parser.parse_args()
    receipt = verify(args.run_root)
    write_json(args.output.resolve(), receipt)
    print(
        json.dumps(
            {
                "passed": receipt["passed"],
                "frozen_lock": receipt["frozen_commit_source_lock"]["passed"],
                "replay": receipt["measured_replay"]["passed"],
                "seal": receipt["run_seal"]["passed"],
                "tests": receipt["analysis_tests"]["passed"] and receipt["postrun_tests"]["passed"],
            },
            sort_keys=True,
        )
    )
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
