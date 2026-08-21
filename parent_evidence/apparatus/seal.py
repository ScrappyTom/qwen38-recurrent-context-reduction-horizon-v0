from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from apparatus.canonical import canonical_json_bytes, load_json, sha256_bytes, sha256_file, write_json


def build_seal(run_root: Path) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    for path in sorted(run_root.rglob("*"), key=lambda item: item.relative_to(run_root).as_posix()):
        if not path.is_file() or path.name == "SEAL.json":
            continue
        files.append({"path": path.relative_to(run_root).as_posix(), "size_bytes": path.stat().st_size, "sha256": sha256_file(path)})
    return {
        "schema_version": "recurrent-context-reduction-run-seal-v0",
        "run_id": run_root.name,
        "file_count": len(files),
        "total_bytes": sum(row["size_bytes"] for row in files),
        "file_manifest_sha256": sha256_bytes(canonical_json_bytes(files)),
        "files": files,
    }


def seal(run_root: Path) -> dict[str, Any]:
    receipt = build_seal(run_root)
    write_json(run_root / "SEAL.json", receipt)
    return receipt


def verify_seal(run_root: Path) -> dict[str, Any]:
    expected = load_json(run_root / "SEAL.json")
    observed = build_seal(run_root)
    failures: list[str] = []
    for key in ("run_id", "file_count", "total_bytes", "file_manifest_sha256", "files"):
        if expected.get(key) != observed.get(key):
            failures.append(f"seal mismatch: {key}")
    return {"schema_version": "recurrent-context-reduction-run-seal-verification-v0", "run_id": run_root.name, "passed": not failures, "failures": failures, "file_manifest_sha256": observed["file_manifest_sha256"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_root", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    root = args.run_root.resolve()
    result = verify_seal(root) if args.verify else seal(root)
    print(json.dumps(result, sort_keys=True))
    return 0 if result.get("passed", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
