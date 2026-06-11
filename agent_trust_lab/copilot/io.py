from __future__ import annotations

import json
from pathlib import Path
import re

from .models import AgentOutputPackage, CopilotInput


def load_copilot_input(path: str | Path) -> CopilotInput:
    input_path = Path(path)
    text = input_path.read_text(encoding="utf-8")
    if input_path.suffix.lower() == ".json":
        return _load_json_input(text)
    return _load_raw_text_input(text)


def _load_json_input(text: str) -> CopilotInput:
    raw = json.loads(text)
    agent_output = raw["agent_output"]
    return CopilotInput(
        case_id=raw["case_id"],
        domain=raw["domain"],
        user_request=raw["user_request"],
        agent_output=AgentOutputPackage(
            final_output=agent_output["final_output"],
            tool_trace=agent_output.get("tool_trace", []),
            evidence_snippets=agent_output.get("evidence_snippets", []),
            metadata=agent_output.get("metadata", {}),
        ),
        reviewer_notes=raw.get("reviewer_notes", []),
    )


def _load_raw_text_input(text: str) -> CopilotInput:
    sections = _split_sections(text)
    case_id = sections.get("case id", "COPILOT-RAW-001").strip()
    domain = sections.get("domain", "agent_output_review").strip()
    user_request = sections.get("user request", "").strip()
    final_output = sections.get("final output", "").strip()
    tool_trace = _parse_bullets(sections.get("tool trace", ""))
    evidence_snippets = _parse_bullets(sections.get("evidence", ""))
    reviewer_notes = _parse_bullets(sections.get("reviewer notes", ""))
    expected_risk_level = sections.get("expected risk level", "medium").strip()
    required_terms = _parse_csv_or_bullets(sections.get("required terms", ""))

    return CopilotInput(
        case_id=case_id,
        domain=domain,
        user_request=user_request,
        agent_output=AgentOutputPackage(
            final_output=final_output,
            tool_trace=tool_trace,
            evidence_snippets=evidence_snippets,
            metadata={
                "expected_risk_level": expected_risk_level,
                "required_terms": required_terms,
            },
        ),
        reviewer_notes=reviewer_notes,
    )


def _split_sections(text: str) -> dict[str, str]:
    pattern = re.compile(r"(?mi)^([A-Za-z][A-Za-z _-]+):\s*$")
    matches = list(pattern.finditer(text))
    if not matches:
        return {}

    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        name = match.group(1).strip().lower()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections[name] = text[start:end].strip()
    return sections


def _parse_bullets(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    cleaned = [line[2:].strip() if line.startswith("- ") else line for line in lines]
    return [line for line in cleaned if line]


def _parse_csv_or_bullets(text: str) -> list[str]:
    bullets = _parse_bullets(text)
    if len(bullets) > 1:
        return bullets
    if len(bullets) == 1 and "," in bullets[0]:
        return [item.strip() for item in bullets[0].split(",") if item.strip()]
    return bullets
