from __future__ import annotations

import json
from pathlib import Path

from .models import AgentOutputPackage, CopilotInput


def load_copilot_input(path: str | Path) -> CopilotInput:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
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
