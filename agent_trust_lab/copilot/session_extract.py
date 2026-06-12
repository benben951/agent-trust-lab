from __future__ import annotations

import json
import re
from pathlib import Path


REDACTION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"[A-Za-z]:\\[^\s`\"']+"), "<WINDOWS_PATH>"),
    (re.compile(r"https?://\S+"), "<URL>"),
    (re.compile(r"\b\d{11}\b"), "<PHONE>"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "<EMAIL>"),
    (re.compile(r"\b(?:sk|gho|ghp|AIza|xoxb|xoxp)_[A-Za-z0-9_-]+\b"), "<TOKEN>"),
]


def codex_session_to_transcript(
    session_path: str | Path,
    *,
    case_id: str = "COPILOT-CODEX-SESSION-001",
    domain: str = "agent_output_review",
    expected_risk_level: str = "medium",
    required_terms: list[str] | None = None,
    max_tool_items: int = 8,
    max_output_chars: int = 400,
) -> str:
    lines = [
        f"SYSTEM: case_id={case_id}",
        f"SYSTEM: domain={domain}",
        f"SYSTEM: expected_risk_level={expected_risk_level}",
        f"SYSTEM: required_terms={','.join(required_terms or ['human review'])}",
        "",
    ]

    tool_items = 0
    for item in _iter_response_items(session_path):
        payload_type = item.get("type")
        role = item.get("role")
        if payload_type == "message" and role in {"user", "assistant"}:
            text = _extract_message_text(item)
            if not text:
                continue
            if _should_skip_message(text):
                continue
            label = "USER" if role == "user" else "AGENT"
            lines.append(f"{label}: {_redact_text(text)}")
            lines.append("")
            continue
        if payload_type == "function_call" and tool_items < max_tool_items:
            name = item.get("name", "unknown_tool")
            args = _redact_text(str(item.get("arguments", "")))
            lines.append(f"TOOL: call {name} args={_truncate(args, max_output_chars)}")
            lines.append("")
            tool_items += 1
            continue
        if payload_type == "function_call_output" and tool_items < max_tool_items:
            output = _redact_text(str(item.get("output", "")))
            lines.append(f"TOOL: output {_truncate(output, max_output_chars)}")
            lines.append("")
            tool_items += 1

    return "\n".join(lines).strip() + "\n"


def write_codex_session_transcript(
    session_path: str | Path,
    out_path: str | Path,
    **kwargs,
) -> Path:
    target = Path(out_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(codex_session_to_transcript(session_path, **kwargs), encoding="utf-8")
    return target


def _iter_response_items(session_path: str | Path) -> list[dict]:
    items: list[dict] = []
    for line in Path(session_path).read_text(encoding="utf-8").splitlines():
        obj = json.loads(line)
        if obj.get("type") != "response_item":
            continue
        payload = obj.get("payload", {})
        items.append(payload)
    return items


def _extract_message_text(payload: dict) -> str:
    content = payload.get("content")
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if item.get("type") in {"input_text", "output_text"}:
            text = item.get("text", "").strip()
            if text:
                parts.append(text)
    return "\n".join(parts).strip()


def _redact_text(text: str) -> str:
    result = text
    for pattern, replacement in REDACTION_PATTERNS:
        result = pattern.sub(replacement, result)
    return result


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _should_skip_message(text: str) -> bool:
    lowered = text.lower()
    boilerplate_markers = [
        "# agents.md instructions",
        "<environment_context>",
        "global codex memory entry",
        "do not read or expose secrets",
    ]
    return any(marker in lowered for marker in boilerplate_markers)
