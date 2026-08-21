from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from apparatus.canonical import load_json, sha256_bytes
from apparatus.constants import CELLS, PREDECESSOR_ROOT


PARENT_TURNS = {"s42-s1": 12, "s314159-s1": 10}


def predecessor_cell_root(cell: str) -> Path:
    return PREDECESSOR_ROOT / "runs" / "2026-08-20-sealed-run-v0" / "cells" / CELLS[cell]["predecessor_cell"]


def predecessor_call(cell: str, ordinal: int) -> dict[str, Any]:
    root = predecessor_cell_root(cell)
    return {
        "request": load_json(root / "requests" / f"call-{ordinal:02d}.json"),
        "response": load_json(root / "responses" / f"call-{ordinal:02d}.json"),
        "action": load_json(root / "actions" / f"call-{ordinal:02d}.json"),
    }


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


def predecessor_assistant_message(cell: str) -> dict[str, str]:
    response = predecessor_call(cell, 2)["response"]
    content = response["choices"][0]["message"]["content"]
    if not isinstance(content, str):
        raise ValueError("predecessor response lacks string assistant content")
    parsed = json.loads(content)
    if parsed != CELLS[cell]["pending_action"]:
        raise ValueError(f"predecessor pending action mismatch for {cell}")
    return {"role": "assistant", "content": content}


def exact_backing_id(cell: str, result_index: int, result_message: dict[str, Any]) -> str:
    wanted = sha256_bytes(str(result_message.get("content") or "").encode("utf-8"))
    parent_messages = parent_boundary_objects(cell)["request"]["messages"]
    for index, message in enumerate(parent_messages):
        if sha256_bytes(str(message.get("content") or "").encode("utf-8")) == wanted:
            return f"parent:{cell}:request-message:{index:03d}"
    predecessor_messages = predecessor_call(cell, 2)["request"]["messages"]
    for index, message in enumerate(predecessor_messages):
        if sha256_bytes(str(message.get("content") or "").encode("utf-8")) == wanted:
            return f"predecessor:{cell}:call-02-message:{index:03d}"
    return f"recurrent:{cell}:sha256:{wanted}"
