from __future__ import annotations

from pathlib import Path

from agent_trust_lab.copilot import ReviewOrchestrator, load_copilot_input
from agent_trust_lab.copilot.reports import render_copilot_markdown


def test_load_copilot_input_and_review() -> None:
    path = Path("examples/copilot_input_agent_failure.json")
    review_input = load_copilot_input(path)
    session = ReviewOrchestrator().review(review_input)

    assert session.selected_rulepack == "agent_tool_use"
    assert session.decision.recommendation == "escalate_for_manual_review"
    assert session.decision.trust_level == "medium"
    assert session.decision.risk_score == 55
    assert session.evidence.normalized_evidence
    assert any(item["type"] == "missing_escalation" for item in session.decision.findings)


def test_render_copilot_markdown_contains_key_sections() -> None:
    path = Path("examples/copilot_input_agent_failure.json")
    review_input = load_copilot_input(path)
    session = ReviewOrchestrator().review(review_input)
    report = render_copilot_markdown(session)

    assert "# Agent Review Copilot Report" in report
    assert "Rule pack" in report
    assert "Next Checks" in report
    assert "COPILOT-DEMO-001" in report


def test_load_raw_text_copilot_input_and_review() -> None:
    path = Path("examples/copilot_input_agent_failure.txt")
    review_input = load_copilot_input(path)
    session = ReviewOrchestrator().review(review_input)

    assert review_input.case_id == "COPILOT-RAW-001"
    assert review_input.domain == "agent_output_review"
    assert review_input.agent_output.metadata["expected_risk_level"] == "high"
    assert review_input.agent_output.tool_trace
    assert session.selected_rulepack == "agent_tool_use"
    assert session.decision.recommendation == "escalate_for_manual_review"
