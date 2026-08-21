from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from apparatus.canonical import sha256_bytes, write_json
from apparatus.constants import PREDECESSOR_COMMIT, PREDECESSOR_REPOSITORY, PREDECESSOR_ROOT, ROOT


SELECTED_FILES = (
    "BOUNDARY_MANIFEST.json",
    "CAPACITY_PREFLIGHT.json",
    "DESIGN.json",
    "DIRECT_TRANSCRIPT_AUDIT.md",
    "FORECAST.json",
    "FREEZE.md",
    "PARENT_PROJECT_IMPLICATIONS.md",
    "POLICY_FREEZE.json",
    "POSTRUN_APPARATUS_NOTE.md",
    "POSTRUN_VERIFICATION.json",
    "RESULTS.md",
    "TREATMENT_DELTA.json",
    "provenance/MATERIALIZATION_RECEIPT.json",
    "provenance/MODEL_PROFILE_LOCK.json",
    "provenance/SOURCE_LOCK.json",
    "provenance/TOKENIZER_QUALIFICATION.json",
    "runs/2026-08-20-sealed-run-v0/RUN_RESULT.json",
    "runs/2026-08-20-sealed-run-v0/SEAL.json",
    "runs/2026-08-20-sealed-run-v0/analysis/AUDITED_ANALYSIS.json",
    "runs/2026-08-20-sealed-run-v0/analysis/DIRECT_TRANSCRIPT_AUDIT.md",
    "runs/2026-08-20-sealed-run-v0/analysis/FROZEN_PREFLIGHT_VERIFICATION.json",
    "runs/2026-08-20-sealed-run-v0/analysis/METRICS.json",
    "runs/2026-08-20-sealed-run-v0/analysis/RESULTS.md",
    "runs/2026-08-20-sealed-run-v0/model/runtime-custody.json",
    "runs/2026-08-20-sealed-run-v0/model/runtime-lifecycle.json",
    "runs/2026-08-20-sealed-run-v0/model/server-arguments.json",
    "runs/2026-08-20-sealed-run-v0/replay/REPLAY.json",
)

SELECTED_PREFIXES = (
    "evidence/",
    "runs/2026-08-20-sealed-run-v0/cells/01-s42-s1-oldest_fit_receipts_v0/",
    "runs/2026-08-20-sealed-run-v0/cells/02-s314159-s1-oldest_fit_receipts_v0/",
)


def git(donor: Path, *args: str) -> bytes:
    process = subprocess.run(
        ["git", "-C", str(donor), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode:
        raise RuntimeError(process.stderr.decode("utf-8", errors="replace"))
    return process.stdout


def selected_paths(donor: Path) -> list[str]:
    tracked = git(donor, "ls-tree", "-r", "--name-only", PREDECESSOR_COMMIT).decode("utf-8").splitlines()
    chosen = set(SELECTED_FILES)
    chosen.update(path for path in tracked if any(path.startswith(prefix) for prefix in SELECTED_PREFIXES))
    missing = sorted(set(SELECTED_FILES) - set(tracked))
    if missing:
        raise RuntimeError(f"selected predecessor files are absent at frozen commit: {missing}")
    return sorted(chosen)


def materialize(donor: Path) -> dict[str, Any]:
    observed = git(donor, "rev-parse", PREDECESSOR_COMMIT).decode().strip()
    if observed != PREDECESSOR_COMMIT:
        raise RuntimeError("predecessor commit did not resolve exactly")
    rows: list[dict[str, Any]] = []
    for original in selected_paths(donor):
        data = git(donor, "show", f"{PREDECESSOR_COMMIT}:{original}")
        blob = git(donor, "rev-parse", f"{PREDECESSOR_COMMIT}:{original}").decode().strip()
        destination = PREDECESSOR_ROOT / original
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        copied = destination.relative_to(ROOT).as_posix()
        copied_bytes = destination.read_bytes()
        rows.append(
            {
                "source_repository": PREDECESSOR_REPOSITORY,
                "source_commit": PREDECESSOR_COMMIT,
                "original_path": original,
                "git_blob_sha": blob,
                "original_sha256": sha256_bytes(data),
                "original_size_bytes": len(data),
                "copied_path": copied,
                "copied_sha256": sha256_bytes(copied_bytes),
                "copied_size_bytes": len(copied_bytes),
                "byte_equivalent": copied_bytes == data,
            }
        )
    receipt = {
        "schema_version": "recurrent-context-reduction-predecessor-materialization-v0",
        "predecessor_repository": PREDECESSOR_REPOSITORY,
        "predecessor_commit": PREDECESSOR_COMMIT,
        "file_count": len(rows),
        "total_bytes": sum(row["copied_size_bytes"] for row in rows),
        "all_byte_equivalent": all(row["byte_equivalent"] for row in rows),
        "files": rows,
    }
    write_json(ROOT / "provenance" / "PREDECESSOR_MATERIALIZATION_RECEIPT.json", receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predecessor", type=Path, default=Path(r"E:\qwen38-context-reduction-pressure-boundary-v0"))
    args = parser.parse_args()
    receipt = materialize(args.predecessor.resolve())
    print(json.dumps({key: receipt[key] for key in ("file_count", "total_bytes", "all_byte_equivalent")}, sort_keys=True))
    return 0 if receipt["all_byte_equivalent"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
