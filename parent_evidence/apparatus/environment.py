from __future__ import annotations

import copy
import difflib
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from apparatus.canonical import compact_json, sha256_bytes
from apparatus.constants import CELLS, PREDECESSOR_ROOT, SOURCE_COMMIT, SOURCE_PATHS, TARGET
from apparatus.predecessor import parent_boundary_objects, parent_cell_root


MAX_READ_BYTES = 12_000
MAX_PATCH_BYTES = 180_000
RESULT_SCHEMA = "schema-action-result-v1"


class ActionRejected(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def _identity_bytes(value: Any) -> bytes:
    """Match the parent workbench identity serialization (no trailing newline)."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def snapshot_directory(root: Path) -> dict[str, Any]:
    root = root.resolve()
    if not root.is_dir():
        raise RuntimeError(f"candidate root is not a directory: {root}")
    directories: list[str] = []
    files: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise RuntimeError(f"candidate symlink is forbidden: {relative}")
        if path.is_dir():
            directories.append(relative)
        elif path.is_file():
            data = path.read_bytes()
            files.append(
                {
                    "path": relative,
                    "size_bytes": len(data),
                    "sha256": sha256_bytes(data),
                }
            )
        else:
            raise RuntimeError(f"unsupported candidate entry: {relative}")
    payload = {"schema_version": 1, "directories": directories, "files": files}
    return {**payload, "candidate_id": sha256_bytes(_identity_bytes(payload))}


@dataclass(frozen=True)
class Region:
    region_id: str
    heading_level: int
    heading_text: str
    part: int
    part_count: int
    start_line: int
    end_line: int
    content: str

    @property
    def raw(self) -> bytes:
        return self.content.encode("utf-8")


def build_regions(data: bytes) -> list[Region]:
    lines = data.decode("utf-8", errors="strict").splitlines(keepends=True)
    headings: list[tuple[int, int, str]] = []
    for number, line in enumerate(lines, start=1):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line.rstrip("\r\n"))
        if match:
            headings.append((number, len(match.group(1)), match.group(2)))
    if not headings or headings[0][0] != 1:
        raise RuntimeError("target must begin with an ATX heading")

    regions: list[Region] = []
    ordinal = 0
    for heading_index, (start, level, heading) in enumerate(headings):
        end = headings[heading_index + 1][0] - 1 if heading_index + 1 < len(headings) else len(lines)
        chunks: list[tuple[int, int]] = []
        chunk_start = start
        chunk_size = 0
        for number in range(start, end + 1):
            line_size = len(lines[number - 1].encode("utf-8"))
            if line_size > MAX_READ_BYTES:
                raise RuntimeError(f"one target line exceeds the transfer limit: {number}")
            if chunk_size and chunk_size + line_size > MAX_READ_BYTES:
                chunks.append((chunk_start, number - 1))
                chunk_start = number
                chunk_size = 0
            chunk_size += line_size
        chunks.append((chunk_start, end))
        for part, (chunk_start, chunk_end) in enumerate(chunks, start=1):
            ordinal += 1
            regions.append(
                Region(
                    region_id=f"R{ordinal:03d}",
                    heading_level=level,
                    heading_text=heading,
                    part=part,
                    part_count=len(chunks),
                    start_line=chunk_start,
                    end_line=chunk_end,
                    content="".join(lines[chunk_start - 1 : chunk_end]),
                )
            )
    if b"".join(region.raw for region in regions) != data:
        raise RuntimeError("region construction did not reassemble the target")
    return regions


def validate_action(cell: str, action: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(action, dict) or not isinstance(action.get("action"), str):
        raise ActionRejected("action_schema_violation", "action must be an object with an action string")
    schema = parent_boundary_objects(cell)["action_schema"]
    candidates = [
        item
        for item in schema.get("oneOf", [])
        if item.get("properties", {}).get("action", {}).get("const") == action["action"]
    ]
    if len(candidates) != 1:
        raise ActionRejected("unknown_action", f"undeclared action: {action['action']}")
    definition = candidates[0]
    required = set(definition.get("required", []))
    missing = sorted(required - set(action))
    if missing:
        raise ActionRejected("action_schema_violation", f"missing required fields: {missing}")
    properties = definition.get("properties", {})
    extras = sorted(set(action) - set(properties))
    if definition.get("additionalProperties") is False and extras:
        raise ActionRejected("action_schema_violation", f"undeclared fields: {extras}")
    for key, value in action.items():
        rule = properties.get(key, {})
        expected = rule.get("type")
        if expected == "string" and not isinstance(value, str):
            raise ActionRejected("action_schema_violation", f"{key} must be a string")
        if expected == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
            raise ActionRejected("action_schema_violation", f"{key} must be an integer")
        if isinstance(value, str) and int(rule.get("minLength", 0)) > len(value):
            raise ActionRejected("action_schema_violation", f"{key} is shorter than minLength")
        if isinstance(value, int) and "minimum" in rule and value < int(rule["minimum"]):
            raise ActionRejected("action_schema_violation", f"{key} is below minimum")
        if isinstance(value, str) and "pattern" in rule and re.fullmatch(str(rule["pattern"]), value) is None:
            raise ActionRejected("action_schema_violation", f"{key} does not match its pattern")
    return copy.deepcopy(action)


class ActionEnvironment:
    """Bounded continuation environment for recurrent pressure cycles.

    Historical results can be reopened exactly, target operations execute on a
    private candidate, and novel reads of the four frozen governing source
    documents use their standalone byte-exact materialization. A novel repo
    index/history request or a read outside that materialized source surface is
    an apparatus integrity endpoint rather than a fabricated partial result.
    """

    def __init__(self, cell: str, candidate_root: Path, submission_root: Path) -> None:
        if cell not in CELLS:
            raise ValueError(f"unknown cell: {cell}")
        self.cell = cell
        self.candidate_root = candidate_root.resolve()
        self.submission_root = submission_root.resolve()
        if self.candidate_root.exists():
            raise RuntimeError(f"candidate root already exists: {self.candidate_root}")
        fixture_candidate = parent_cell_root(cell) / "fixture" / "candidate"
        self.candidate_root.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(fixture_candidate, self.candidate_root)
        self.initial_snapshot = snapshot_directory(self.candidate_root)
        expected = parent_boundary_objects(cell)["run_summary"]["initial_candidate_id"]
        if self.initial_snapshot["candidate_id"] != expected:
            raise RuntimeError("materialized candidate identity does not match the parent")
        self.target_bytes = (self.candidate_root / TARGET).read_bytes()
        self.regions = {region.region_id: region for region in build_regions(self.target_bytes)}
        self.exact_reopens = self._build_reopen_map()
        self.source_records = self._build_source_records()
        self.cursors: dict[str, dict[str, Any]] = {}

    def snapshot(self) -> dict[str, Any]:
        return snapshot_directory(self.candidate_root)

    def _build_reopen_map(self) -> dict[str, dict[str, Any]]:
        parent = parent_boundary_objects(self.cell)
        messages = parent["request"]["messages"]
        results: dict[str, dict[str, Any]] = {}
        for result_index in range(3, len(messages), 2):
            action_message = messages[result_index - 1]
            result_message = messages[result_index]
            if action_message.get("role") != "assistant" or result_message.get("role") != "user":
                raise RuntimeError("parent chronology is not canonical")
            action = json.loads(action_message["content"])
            envelope = json.loads(result_message["content"])
            results[compact_json(action)] = copy.deepcopy(envelope["result"])
        historical_action = {"action": parent["action"]["tool_name"], **parent["action"]["arguments"]}
        results[compact_json(historical_action)] = copy.deepcopy(parent["tool_result"])
        return results

    def _build_source_records(self) -> dict[str, dict[str, Any]]:
        receipt_path = PREDECESSOR_ROOT / "provenance" / "MATERIALIZATION_RECEIPT.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        by_original = {row["original_path"]: row for row in receipt["files"]}
        records: dict[str, dict[str, Any]] = {}
        for source_path in SOURCE_PATHS:
            row = by_original[source_path]
            path = PREDECESSOR_ROOT / row["copied_path"]
            data = path.read_bytes()
            if sha256_bytes(data) != row["copied_sha256"]:
                raise RuntimeError(f"frozen source hash mismatch: {source_path}")
            records[source_path] = {**row, "path": path, "data": data}
        return records

    def _resolve(self, requested: str, *, allow_root: bool = False) -> tuple[Path, str]:
        if not isinstance(requested, str) or not requested or "\\" in requested or ":" in requested:
            raise ActionRejected("invalid_path", "path must be nonempty relative POSIX syntax")
        if requested == ".":
            if not allow_root:
                raise ActionRejected("invalid_path", "this action requires a file path")
            return self.candidate_root, "."
        pure = PurePosixPath(requested)
        if pure.is_absolute() or ".." in pure.parts or pure.as_posix() != requested:
            raise ActionRejected("invalid_path", "path must be canonical and stay inside the candidate")
        resolved = (self.candidate_root / Path(*pure.parts)).resolve()
        try:
            resolved.relative_to(self.candidate_root)
        except ValueError as exc:
            raise ActionRejected("path_escape", "path resolves outside the candidate") from exc
        return resolved, requested

    def _tree(self, action: dict[str, Any]) -> dict[str, Any]:
        path, canonical = self._resolve(action["path"], allow_root=True)
        if not path.is_dir():
            raise ActionRejected("not_a_directory", f"not a candidate directory: {canonical}")
        snapshot = self.snapshot()
        prefix = "" if canonical == "." else canonical.rstrip("/") + "/"
        entries: list[dict[str, Any]] = []
        for directory in snapshot["directories"]:
            if directory == canonical or directory.startswith(prefix):
                entries.append({"path": directory, "type": "directory"})
        for item in snapshot["files"]:
            if item["path"].startswith(prefix):
                entries.append({"type": "file", **item})
        entries.sort(key=lambda item: (item["path"], item["type"]))
        return {"accepted": True, "candidate_id": snapshot["candidate_id"], "entries": entries, "path": canonical, "tool": "tree"}

    def _read(self, action: dict[str, Any]) -> dict[str, Any]:
        path, canonical = self._resolve(action["path"])
        if not path.is_file():
            raise ActionRejected("not_a_file", f"not a candidate file: {canonical}")
        data = path.read_bytes()
        if len(data) > MAX_READ_BYTES:
            raise ActionRejected("read_limit", f"file is {len(data)} bytes; limit is {MAX_READ_BYTES}")
        return {
            "accepted": True,
            "candidate_id": self.snapshot()["candidate_id"],
            "content": data.decode("utf-8", errors="strict"),
            "file_sha256": sha256_bytes(data),
            "path": canonical,
            "size_bytes": len(data),
            "tool": "read",
        }

    def _read_lines(self, action: dict[str, Any]) -> dict[str, Any]:
        path, canonical = self._resolve(action["path"])
        if not path.is_file():
            raise ActionRejected("not_a_file", f"not a candidate file: {canonical}")
        data = path.read_bytes()
        text = data.decode("utf-8", errors="strict")
        lines = text.splitlines(keepends=True)
        requested_start = int(action["start_line"])
        requested_end = int(action["end_line"])
        if requested_start > requested_end or requested_start > len(lines):
            raise ActionRejected("invalid_line_range", "requested line range is outside the file")
        requested_end = min(requested_end, len(lines))
        end = requested_start - 1
        size = 0
        for number in range(requested_start, requested_end + 1):
            line_size = len(lines[number - 1].encode("utf-8"))
            if line_size > MAX_READ_BYTES:
                raise ActionRejected("line_too_large", f"line {number} exceeds the transfer limit")
            if size and size + line_size > MAX_READ_BYTES:
                break
            size += line_size
            end = number
        content = "".join(lines[requested_start - 1 : end])
        raw = content.encode("utf-8")
        complete = end == requested_end
        return {
            "accepted": True,
            "candidate_id": self.snapshot()["candidate_id"],
            "content": content,
            "continuation_cursor": None if complete else "standalone-terminal-cursor-not-used",
            "end_line": end,
            "file_sha256": sha256_bytes(data),
            "more_in_file": end < len(lines),
            "next_start_line": None if complete else end + 1,
            "pagination_schema": "exact-version-bound-line-cursor-v0",
            "path": canonical,
            "request_complete": complete,
            "requested_end_line": int(action["end_line"]),
            "requested_start_line": int(action["start_line"]),
            "size_bytes": len(data),
            "slice_sha256": sha256_bytes(raw),
            "slice_size_bytes": len(raw),
            "source_kind": "candidate",
            "start_line": requested_start,
            "tool": "read_lines",
            "total_lines": len(lines),
            "transfer_limit_bytes": MAX_READ_BYTES,
        }

    def _read_region(self, action: dict[str, Any]) -> dict[str, Any]:
        current = (self.candidate_root / TARGET).read_bytes()
        if sha256_bytes(current) != sha256_bytes(self.target_bytes):
            raise ActionRejected("stale_region_basis", "target no longer matches the frozen outline")
        region = self.regions.get(action["region_id"])
        if region is None:
            raise ActionRejected("unknown_region", "region_id is not in the frozen outline")
        raw = region.raw
        return {
            "accepted": True,
            "candidate_id": self.snapshot()["candidate_id"],
            "content": region.content,
            "end_line": region.end_line,
            "file_sha256": sha256_bytes(current),
            "heading_level": region.heading_level,
            "heading_text": region.heading_text,
            "line_count": region.end_line - region.start_line + 1,
            "locator": f"{TARGET}#L{region.start_line}-L{region.end_line}",
            "part": region.part,
            "part_count": region.part_count,
            "path": TARGET,
            "region_id": region.region_id,
            "semantic_relevance_supplied": False,
            "sha256": sha256_bytes(raw),
            "size_bytes": len(raw),
            "start_line": region.start_line,
            "tool": "read_region",
        }

    def _source_record(self, requested: str) -> dict[str, Any]:
        if not isinstance(requested, str) or not requested or "\\" in requested or ":" in requested:
            raise ActionRejected("invalid_repo_path", "repository path must be nonempty relative POSIX syntax")
        pure = PurePosixPath(requested)
        if pure.is_absolute() or ".." in pure.parts or pure.as_posix() != requested:
            raise ActionRejected("invalid_repo_path", "repository path must be canonical")
        record = self.source_records.get(requested)
        if record is None:
            raise ActionRejected(
                "source_surface_not_materialized",
                "novel repository access outside the four byte-exact governing documents is not qualified",
            )
        return record

    def _repo_read(self, action: dict[str, Any]) -> dict[str, Any]:
        record = self._source_record(action["path"])
        data = record["data"]
        if len(data) > MAX_READ_BYTES:
            raise ActionRejected("read_limit", f"file is {len(data)} bytes; limit is {MAX_READ_BYTES}")
        return {
            "accepted": True,
            "blob_sha": record["git_blob_sha"],
            "content": data.decode("utf-8", errors="strict"),
            "path": action["path"],
            "size_bytes": len(data),
            "source_commit": SOURCE_COMMIT,
            "tool": "repo_read",
        }

    def _repo_read_lines(self, action: dict[str, Any]) -> dict[str, Any]:
        record = self._source_record(action["path"])
        data = record["data"]
        text = data.decode("utf-8", errors="strict")
        lines = text.splitlines(keepends=True)
        requested_start = int(action["start_line"])
        requested_end_original = int(action["end_line"])
        if requested_start > requested_end_original or requested_start > len(lines):
            raise ActionRejected("invalid_line_range", "requested line range is outside the repository blob")
        requested_end = min(requested_end_original, len(lines))
        end = requested_start - 1
        size = 0
        for number in range(requested_start, requested_end + 1):
            line_size = len(lines[number - 1].encode("utf-8"))
            if line_size > MAX_READ_BYTES:
                raise ActionRejected("line_too_large", f"line {number} exceeds the transfer limit")
            if size and size + line_size > MAX_READ_BYTES:
                break
            size += line_size
            end = number
        content = "".join(lines[requested_start - 1 : end])
        raw = content.encode("utf-8")
        complete = end == requested_end
        cursor: str | None = None
        if not complete:
            binding = {
                "source_kind": "repository",
                "path": action["path"],
                "source_commit": SOURCE_COMMIT,
                "blob_sha": record["git_blob_sha"],
                "next_start_line": end + 1,
                "requested_end_line": requested_end_original,
            }
            cursor = "exact-line-v0:" + sha256_bytes(compact_json(binding).encode("utf-8"))
            self.cursors[cursor] = binding
        return {
            "accepted": True,
            "blob_sha": record["git_blob_sha"],
            "content": content,
            "continuation_cursor": cursor,
            "end_line": end,
            "more_in_file": end < len(lines),
            "next_start_line": None if complete else end + 1,
            "pagination_schema": "exact-version-bound-line-cursor-v0",
            "path": action["path"],
            "request_complete": complete,
            "requested_end_line": requested_end_original,
            "requested_start_line": requested_start,
            "size_bytes": len(data),
            "slice_sha256": sha256_bytes(raw),
            "slice_size_bytes": len(raw),
            "source_commit": SOURCE_COMMIT,
            "source_kind": "repository",
            "start_line": requested_start,
            "tool": "repo_read_lines",
            "total_lines": len(lines),
            "transfer_limit_bytes": MAX_READ_BYTES,
        }

    def _continue_lines(self, action: dict[str, Any]) -> dict[str, Any]:
        binding = self.cursors.get(action["cursor"])
        if binding is None:
            raise ActionRejected("invalid_or_stale_cursor", "cursor is unknown or no longer valid")
        if binding["source_kind"] != "repository":
            raise ActionRejected("unsupported_cursor_kind", "only locally issued repository cursors are continuable")
        return self._repo_read_lines(
            {
                "action": "repo_read_lines",
                "path": binding["path"],
                "start_line": binding["next_start_line"],
                "end_line": binding["requested_end_line"],
            }
        )

    def _search(self, action: dict[str, Any]) -> dict[str, Any]:
        path, canonical = self._resolve(action["path"], allow_root=True)
        if not path.exists():
            raise ActionRejected("not_found", f"candidate path does not exist: {canonical}")
        files = [path] if path.is_file() else sorted(item for item in path.rglob("*") if item.is_file())
        matches: list[dict[str, Any]] = []
        for file_path in files:
            text = file_path.read_text(encoding="utf-8")
            for number, line in enumerate(text.splitlines(), start=1):
                if action["query"] in line:
                    matches.append({"path": file_path.relative_to(self.candidate_root).as_posix(), "line": number, "text": line})
                    if len(matches) == 200:
                        return {"accepted": True, "candidate_id": self.snapshot()["candidate_id"], "matches": matches, "path": canonical, "query": action["query"], "skipped_binary": [], "tool": "search", "truncated": True}
        return {"accepted": True, "candidate_id": self.snapshot()["candidate_id"], "matches": matches, "path": canonical, "query": action["query"], "skipped_binary": [], "tool": "search", "truncated": False}

    def _patch(self, action: dict[str, Any]) -> dict[str, Any]:
        path, canonical = self._resolve(action["path"])
        if not path.is_file():
            raise ActionRejected("not_a_file", f"not a candidate file: {canonical}")
        before = path.read_bytes()
        before_sha = sha256_bytes(before)
        if action["expected_file_sha256"] != before_sha:
            raise ActionRejected("file_version_mismatch", f"expected {action['expected_file_sha256']}, current file is {before_sha}")
        old = action["old"]
        new = action["new"]
        text = before.decode("utf-8", errors="strict")
        if old == new:
            raise ActionRejected("no_op_patch", "old and new are identical")
        count = text.count(old)
        if count != 1:
            raise ActionRejected("patch_not_applicable", f"old text must occur exactly once; observed {count}")
        after_text = text.replace(old, new, 1)
        after = after_text.encode("utf-8")
        if len(after) > MAX_PATCH_BYTES:
            raise ActionRejected("patch_limit", "patched file exceeds the fixture limit")
        before_snapshot = self.snapshot()
        diff = "".join(
            difflib.unified_diff(
                text.splitlines(keepends=True),
                after_text.splitlines(keepends=True),
                fromfile=f"a/{canonical}",
                tofile=f"b/{canonical}",
            )
        )
        path.write_bytes(after)
        after_snapshot = self.snapshot()
        return {
            "accepted": True,
            "applied": True,
            "candidate_after": after_snapshot["candidate_id"],
            "candidate_before": before_snapshot["candidate_id"],
            "effective_diff": diff,
            "file_after_sha256": sha256_bytes(after),
            "file_before_sha256": before_sha,
            "path": canonical,
            "tool": "patch",
        }

    def _replace_file(self, action: dict[str, Any]) -> dict[str, Any]:
        path, canonical = self._resolve(action["path"])
        if not path.is_file():
            raise ActionRejected("not_a_file", f"not a candidate file: {canonical}")
        before = path.read_bytes()
        before_sha = sha256_bytes(before)
        if action["expected_file_sha256"] != before_sha:
            raise ActionRejected("file_version_mismatch", f"expected {action['expected_file_sha256']}, current file is {before_sha}")
        after = action["new_content"].encode("utf-8")
        if after == before:
            raise ActionRejected("no_op_replace", "new_content is byte-identical to the current file")
        if len(after) > MAX_PATCH_BYTES:
            raise ActionRejected("replace_limit", "replacement file exceeds the fixture limit")
        before_snapshot = self.snapshot()
        path.write_bytes(after)
        after_snapshot = self.snapshot()
        return {
            "accepted": True,
            "applied": True,
            "candidate_after": after_snapshot["candidate_id"],
            "candidate_before": before_snapshot["candidate_id"],
            "file_after_sha256": sha256_bytes(after),
            "file_before_sha256": before_sha,
            "path": canonical,
            "tool": "replace_file",
        }

    def _submit(self) -> dict[str, Any]:
        snapshot = self.snapshot()
        destination = self.submission_root / snapshot["candidate_id"] / "candidate"
        if destination.exists():
            raise ActionRejected("submission_exists", "submission destination already exists")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(self.candidate_root, destination)
        if snapshot_directory(destination)["candidate_id"] != snapshot["candidate_id"]:
            raise RuntimeError("submission materialization changed candidate identity")
        return {"accepted": True, "candidate_id": snapshot["candidate_id"], "submission_id": snapshot["candidate_id"], "tool": "submit"}

    def execute(self, action: dict[str, Any]) -> dict[str, Any]:
        validated = validate_action(self.cell, action)
        before = self.snapshot()
        key = compact_json(validated)
        try:
            if key in self.exact_reopens:
                result = copy.deepcopy(self.exact_reopens[key])
            elif validated["action"] == "tree":
                result = self._tree(validated)
            elif validated["action"] == "search":
                result = self._search(validated)
            elif validated["action"] == "read":
                result = self._read(validated)
            elif validated["action"] == "read_lines":
                result = self._read_lines(validated)
            elif validated["action"] == "read_region":
                result = self._read_region(validated)
            elif validated["action"] == "repo_read":
                result = self._repo_read(validated)
            elif validated["action"] == "repo_read_lines":
                result = self._repo_read_lines(validated)
            elif validated["action"] == "continue_lines":
                result = self._continue_lines(validated)
            elif validated["action"] == "patch":
                result = self._patch(validated)
            elif validated["action"] == "replace_file":
                result = self._replace_file(validated)
            elif validated["action"] == "submit":
                result = self._submit()
            elif validated["action"] in {"repo_list", "repo_catalog", "repo_search", "repo_history"}:
                raise ActionRejected(
                    "source_surface_not_materialized",
                    "novel repository index/search/history access is outside the frozen standalone source surface",
                )
            else:
                raise ActionRejected(
                    "unsupported_declared_action",
                    "declared action has no qualified standalone executor",
                )
        except ActionRejected as exc:
            after = self.snapshot()
            return {
                "accepted": False,
                "candidate_id": after["candidate_id"],
                "error": {"code": exc.code, "message": exc.message},
                "tool": validated["action"],
            }
        after = self.snapshot()
        if validated["action"] not in {"patch", "replace_file"} and before["candidate_id"] != after["candidate_id"]:
            raise RuntimeError("nonmutation action changed candidate identity")
        return result

    @staticmethod
    def result_message(action: dict[str, Any], action_id: str, result: dict[str, Any]) -> dict[str, str]:
        return {
            "role": "user",
            "content": compact_json(
                {
                    "action": action["action"],
                    "action_id": action_id,
                    "result": result,
                    "schema_version": RESULT_SCHEMA,
                }
            ),
        }


def make_environment(cell: str, root: Path) -> ActionEnvironment:
    return ActionEnvironment(cell, root / "candidate", root / "submissions")


__all__ = [
    "ActionEnvironment",
    "ActionRejected",
    "Region",
    "build_regions",
    "make_environment",
    "snapshot_directory",
    "validate_action",
]
