from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass
from typing import Any

from apparatus.canonical import compact_json, sha256_bytes
from apparatus.constants import CONTEXT_TOKENS, RESPONSE_RESERVE


def render_parent_template(messages: list[dict[str, Any]]) -> str:
    """Render the exact non-thinking parent template for string-only messages."""
    rendered: list[str] = []
    for index, message in enumerate(messages):
        role = message["role"]
        content = str(message.get("content") or "").strip()
        if role == "system" and index == 0:
            if content:
                rendered.append(f"<|im_start|>system\n{content}<|im_end|>\n")
        elif role in {"user", "assistant"}:
            rendered.append(f"<|im_start|>{role}\n{content}<|im_end|>\n")
        else:
            raise ValueError(f"unsupported parent message role at {index}: {role}")
    rendered.append("<|im_start|>assistant\n<think>\n\n</think>\n\n")
    return "".join(rendered)


@dataclass(frozen=True)
class TokenReceipt:
    prompt_tokens: int
    rendered_prompt_sha256: str
    rendered_prompt_size_bytes: int
    headroom_after_reserve: int
    fits: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "prompt_tokens": self.prompt_tokens,
            "rendered_prompt_sha256": self.rendered_prompt_sha256,
            "rendered_prompt_size_bytes": self.rendered_prompt_size_bytes,
            "context_tokens": CONTEXT_TOKENS,
            "response_reserve_tokens": RESPONSE_RESERVE,
            "headroom_after_reserve": self.headroom_after_reserve,
            "fits": self.fits,
        }


class ParentTokenEndpoint:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.apply_calls = 0
        self.tokenize_calls = 0
        self.chat_completion_calls = 0

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        raw = compact_json(payload).encode("utf-8")
        request = urllib.request.Request(
            self.base_url + path,
            data=raw,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            value = json.loads(response.read())
        if not isinstance(value, dict):
            raise ValueError(f"endpoint returned non-object for {path}")
        return value

    def count(self, messages: list[dict[str, Any]], kwargs: dict[str, Any]) -> TokenReceipt:
        applied = self._post(
            "/apply-template",
            {
                "messages": messages,
                "add_generation_prompt": True,
                "chat_template_kwargs": kwargs,
            },
        )
        self.apply_calls += 1
        prompt = applied.get("prompt")
        if not isinstance(prompt, str):
            raise ValueError("apply-template response lacks prompt")
        tokenized = self._post(
            "/tokenize",
            {"content": prompt, "add_special": False, "parse_special": True},
        )
        self.tokenize_calls += 1
        tokens = tokenized.get("tokens")
        if not isinstance(tokens, list):
            raise ValueError("tokenize response lacks token list")
        count = len(tokens)
        headroom = CONTEXT_TOKENS - RESPONSE_RESERVE - count
        raw = prompt.encode("utf-8")
        return TokenReceipt(count, sha256_bytes(raw), len(raw), headroom, headroom >= 0)


def request_with_messages(parent_request: dict[str, Any], messages: list[dict[str, Any]]) -> dict[str, Any]:
    request = json.loads(json.dumps(parent_request))
    request["messages"] = messages
    return request
