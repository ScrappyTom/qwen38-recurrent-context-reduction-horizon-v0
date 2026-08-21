from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from apparatus.canonical import sha256_bytes, write_json
from apparatus.constants import DONOR_ROOT, PREDECESSOR_COMMIT, PREDECESSOR_REPOSITORY, ROOT


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


def materialize(donor: Path) -> dict[str, Any]:
    observed = git(donor, "rev-parse", PREDECESSOR_COMMIT).decode().strip()
    if observed != PREDECESSOR_COMMIT:
        raise RuntimeError("predecessor result commit did not resolve exactly")
    if any(DONOR_ROOT.iterdir()):
        raise RuntimeError("parent_evidence must be empty before materialization")

    tracked = sorted(
        git(donor, "ls-tree", "-r", "--name-only", PREDECESSOR_COMMIT)
        .decode("utf-8")
        .splitlines()
    )
    rows: list[dict[str, Any]] = []
    for original in tracked:
        data = git(donor, "show", f"{PREDECESSOR_COMMIT}:{original}")
        blob = git(donor, "rev-parse", f"{PREDECESSOR_COMMIT}:{original}").decode().strip()
        destination = DONOR_ROOT / original
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
        "schema_version": "recurrent-horizon-predecessor-materialization-v0",
        "predecessor_repository": PREDECESSOR_REPOSITORY,
        "predecessor_commit": PREDECESSOR_COMMIT,
        "scope": "complete tracked direct-predecessor snapshot; no Custody Cards checkout",
        "file_count": len(rows),
        "total_bytes": sum(row["copied_size_bytes"] for row in rows),
        "all_byte_equivalent": all(row["byte_equivalent"] for row in rows),
        "files": rows,
    }
    write_json(ROOT / "provenance" / "PREDECESSOR_MATERIALIZATION_RECEIPT.json", receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--predecessor",
        type=Path,
        default=Path(r"E:\qwen38-recurrent-context-reduction-v0"),
    )
    args = parser.parse_args()
    receipt = materialize(args.predecessor.resolve())
    print(
        json.dumps(
            {key: receipt[key] for key in ("file_count", "total_bytes", "all_byte_equivalent")},
            sort_keys=True,
        )
    )
    return 0 if receipt["all_byte_equivalent"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
