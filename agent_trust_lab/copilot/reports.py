from __future__ import annotations

from .models import CopilotSession


def render_copilot_markdown(session: CopilotSession) -> str:
    findings = "\n".join(
        f"- `{item['type']}`: {item['message']}" for item in session.decision.findings
    ) or "- No major finding."
    next_checks = "\n".join(f"- {item}" for item in session.decision.next_checks) or "- No additional check."
    evidence = "\n".join(f"- {item}" for item in session.evidence.normalized_evidence) or "- No normalized evidence."
    return f"""# Agent Review Copilot Report

## Case

- Case ID: `{session.review_input.case_id}`
- Domain: `{session.review_input.domain}`
- Rule pack: `{session.selected_rulepack}`
- Recommendation: `{session.decision.recommendation}`
- Trust level: `{session.decision.trust_level}`
- Risk score: `{session.decision.risk_score}/100`

## User Request

{session.review_input.user_request}

## Final Agent Output

{session.review_input.agent_output.final_output}

## Findings

{findings}

## Normalized Evidence

{evidence}

## Next Checks

{next_checks}
"""
