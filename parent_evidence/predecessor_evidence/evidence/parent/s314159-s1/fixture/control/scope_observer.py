from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

TARGET = 'QWEN_RELATION_ACTION_WORKING_MODEL.md'
INITIAL = '899a37f188de42075d5559bcaf6ba4bea96713ba192517021dbcc533c9844387'

def main() -> int:
    root = Path(sys.argv[1]).resolve()
    files = sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())
    target = root / TARGET
    exact_scope = files == [TARGET] and target.is_file()
    final_sha = hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else None
    report = {
        "scope_integrity": exact_scope,
        "files": files,
        "target_initial_sha256": INITIAL,
        "target_final_sha256": final_sha,
        "target_changed": final_sha is not None and final_sha != INITIAL,
        "semantic_grade": False,
        "task_complete": None,
        "note": "Mechanical custody/scope observation only; no semantic completion judgment.",
    }
    print(json.dumps(report, sort_keys=True))
    return 0 if exact_scope else 1

if __name__ == "__main__":
    raise SystemExit(main())
