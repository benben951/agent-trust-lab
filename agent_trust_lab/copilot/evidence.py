from __future__ import annotations

from .models import CopilotEvidence, CopilotInput


def extract_evidence(review_input: CopilotInput) -> CopilotEvidence:
    # The first version keeps extraction intentionally simple and deterministic.
    output = review_input.agent_output.final_output.strip()
    trace_summary = " ".join(item.strip() for item in review_input.agent_output.tool_trace if item.strip())
    normalized = [item.strip() for item in review_input.agent_output.evidence_snippets if item.strip()]
    claims = [output] if output else []
    actions = [line for line in review_input.agent_output.tool_trace if line.strip()]
    return CopilotEvidence(
        claims=claims,
        actions=actions,
        normalized_evidence=normalized,
        trace_summary=trace_summary,
    )
