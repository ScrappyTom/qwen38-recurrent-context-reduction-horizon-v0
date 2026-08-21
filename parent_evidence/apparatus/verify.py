from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from apparatus.canonical import write_json
from apparatus.constants import PREDECESSOR_COMMIT, ROOT
from apparatus.replay import replay_preflight


PREDECESSOR = Path(r"E:\qwen38-context-reduction-pressure-boundary-v0")


def process(command: list[str], cwd: Path = ROOT) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, text=True)
    return {"command": command, "returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr, "passed": completed.returncode == 0}


def json_audit() -> dict[str, Any]:
    failures: list[str] = []
    files = sorted({*ROOT.glob("*.json"), *(ROOT / "provenance").glob("*.json"), *(ROOT / "preflight" / "packets").rglob("*.json")})
    for path in files:
        try:
            json.loads(path.read_bytes())
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT).as_posix()}: {type(exc).__name__}: {exc}")
    return {"file_count": len(files), "passed": not failures, "failures": failures}


def predecessor_status() -> dict[str, Any]:
    status = process(["git", "status", "--short", "--branch"], PREDECESSOR)
    head = process(["git", "rev-parse", "HEAD"], PREDECESSOR)
    clean = status["passed"] and not any(line and not line.startswith("##") for line in status["stdout"].splitlines())
    return {"path": str(PREDECESSOR), "status": status, "head": head, "clean": clean, "at_expected_commit": head["stdout"].strip() == PREDECESSOR_COMMIT}


def verify() -> dict[str, Any]:
    compile_result = process(["python", "-m", "compileall", "-q", "apparatus", "tests"])
    tests = process(["python", "-m", "unittest", "discover", "-s", "tests", "-v"])
    replay = replay_preflight()
    json_result = json_audit()
    donor = predecessor_status()
    passed = compile_result["passed"] and tests["passed"] and replay["passed"] and json_result["passed"] and donor["clean"] and donor["at_expected_commit"]
    return {
        "schema_version": "recurrent-context-reduction-verification-v0",
        "passed": passed,
        "compile": compile_result,
        "tests": tests,
        "replay": replay,
        "json_audit": json_result,
        "read_only_predecessor": donor,
        "measured_model_calls": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "VERIFICATION.json")
    args = parser.parse_args()
    receipt = verify()
    write_json(args.output.resolve(), receipt)
    print(json.dumps({"passed": receipt["passed"], "tests": receipt["tests"]["passed"], "replay": receipt["replay"]["passed"]}, sort_keys=True))
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
