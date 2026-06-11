from __future__ import annotations

from .models import CopilotDecision, CopilotEvidence, CopilotInput, CopilotSession


def build_session(
    review_input: CopilotInput,
    evidence: CopilotEvidence,
    decision: CopilotDecision,
    selected_rulepack: str,
) -> CopilotSession:
    return CopilotSession(
        review_input=review_input,
        evidence=evidence,
        decision=decision,
        selected_rulepack=selected_rulepack,
    )
