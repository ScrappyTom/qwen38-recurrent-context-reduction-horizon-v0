from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apparatus.canonical import load_json, sha256_bytes, sha256_file
from apparatus.constants import CELLS, DONOR_ROOT, PREDECESSOR_ROOT


PARENT_TURNS = {"s42-s1": 12, "s314159-s1": 10}


def donor_cell_root(cell: str) -> Path:
    return DONOR_ROOT / "runs" / "2026-08-20-sealed-run-v1" / "cells" / CELLS[cell]["donor_cell"]


def donor_call(cell: str, ordinal: int = 3) -> dict[str, Any]:
    root = donor_cell_root(cell)
    return {
        "request": load_json(root / "requests" / f"call-{ordinal:02d}.json"),
        "response": load_json(root / "responses" / f"call-{ordinal:02d}.json"),
        "action": load_json(root / "actions" / f"call-{ordinal:02d}.json"),
        "result": load_json(root / "results" / f"call-{ordinal:02d}.json"),
    }


def donor_assistant_message(cell: str) -> dict[str, str]:
    response = donor_call(cell)["response"]
    content = response["choices"][0]["message"]["content"]
    parsed = json.loads(content)
    if parsed != CELLS[cell]["pending_action"]:
        raise RuntimeError(f"donor call-3 action mismatch: {cell}")
    return {"role": "assistant", "content": content}


def donor_result_message(cell: str) -> dict[str, str]:
    row = donor_call(cell)["result"]
    backing = donor_cell_root(cell) / row["exact_backing"]["path"]
    if not backing.is_file():
        raise RuntimeError(f"donor call-3 result backing is missing: {cell}")
    frozen = CELLS[cell]
    if (
        sha256_file(backing) != frozen["pending_result_message_sha256"]
        or backing.stat().st_size != frozen["pending_result_message_size_bytes"]
    ):
        raise RuntimeError(f"donor call-3 result backing mismatch: {cell}")
    return {"role": "user", "content": backing.read_text(encoding="utf-8")}


def donor_starting_tail(cell: str) -> list[dict[str, str]]:
    return [donor_assistant_message(cell), donor_result_message(cell)]


def donor_terminal_candidate(cell: str) -> dict[str, Any]:
    return load_json(donor_cell_root(cell) / "candidates" / "terminal.json")


def parent_cell_root(cell: str) -> Path:
    return PREDECESSOR_ROOT / "evidence" / "parent" / cell


def parent_data_root(cell: str) -> Path:
    return parent_cell_root(cell) / "data" / cell


def parent_boundary_objects(cell: str) -> dict[str, Any]:
    turn = PARENT_TURNS[cell]
    data = parent_data_root(cell)
    current = data / "turns" / f"turn-{turn:03d}"
    return {
        "request": load_json(current / "request.json"),
        "assistant_message": load_json(current / "assistant-message.json"),
        "action": load_json(current / "action.json"),
        "result_message": load_json(current / "result-message.json"),
        "tool_result": load_json(current / "tool-result.json"),
        "action_schema": load_json(data / "inputs" / "action-schema.json"),
        "run_summary": load_json(data / "run-summary.json"),
        "model_profile": load_json(data / "inputs" / "model-profile.json"),
        "tools": json.loads((data / "inputs" / "tools.json").read_text(encoding="utf-8")),
        "task": (data / "inputs" / "task.md").read_text(encoding="utf-8"),
    }


def exact_backing_id(cell: str, result_index: int, result_message: dict[str, Any]) -> str:
    digest = sha256_bytes(str(result_message.get("content") or "").encode("utf-8"))
    parent_messages = parent_boundary_objects(cell)["request"]["messages"]
    for index, message in enumerate(parent_messages):
        if sha256_bytes(str(message.get("content") or "").encode("utf-8")) == digest:
            return f"parent:{cell}:request-message:{index:03d}"
    for ordinal in (1, 2, 3):
        messages = donor_call(cell, ordinal)["request"]["messages"]
        for index, message in enumerate(messages):
            if sha256_bytes(str(message.get("content") or "").encode("utf-8")) == digest:
                return f"direct-predecessor:{cell}:call-{ordinal:02d}-message:{index:03d}"
        row = donor_call(cell, ordinal)["result"]
        if row["exact_backing"]["sha256"] == digest:
            return f"direct-predecessor:{cell}:call-{ordinal:02d}-result"
    return f"horizon:{cell}:sha256:{digest}"
