from __future__ import annotations

from .evidence import extract_evidence
from .models import AgentOutputPackage, CopilotDecision, CopilotInput
from .review_session import build_session
from .rulepacks import select_rulepack
from ..reviewer import evaluate_case
from ..schema import EvidenceItem, PolicyRule, ReviewCase


class ReviewOrchestrator:
    """Thin first-pass orchestrator that adapts copilot input to the current engine."""

    def review(self, review_input: CopilotInput):
        evidence = extract_evidence(review_input)
        selected_rulepack = select_rulepack(review_input.domain)
        case = self._to_review_case(review_input)
        base = evaluate_case(case)
        decision = CopilotDecision(
            recommendation=base["recommendation"],
            trust_level=base["trust_level"],
            risk_score=base["risk_score"],
            findings=base["findings"],
            next_checks=self._build_next_checks(base),
        )
        return build_session(review_input, evidence, decision, selected_rulepack)

    def _to_review_case(self, review_input: CopilotInput) -> ReviewCase:
        evidence_items = [
            EvidenceItem(
                evidence_id=f"snippet_{idx + 1}",
                source="copilot_input",
                text=text,
            )
            for idx, text in enumerate(review_input.agent_output.evidence_snippets)
        ]
        return ReviewCase(
            case_id=review_input.case_id,
            domain=review_input.domain,
            user_question=review_input.user_request,
            llm_output=review_input.agent_output.final_output,
            expected_risk_level=review_input.agent_output.metadata.get("expected_risk_level", "medium"),
            evidence=evidence_items,
            policy_rules=[
                PolicyRule(
                    rule_id="copilot_default_review",
                    text="Placeholder rule pack bridge for the copilot scaffold.",
                    required_terms=review_input.agent_output.metadata.get("required_terms", []),
                )
            ],
            metadata=review_input.agent_output.metadata,
        )

    def _build_next_checks(self, base_result: dict) -> list[str]:
        checks: list[str] = []
        finding_types = {item["type"] for item in base_result["findings"]}
        if "unsupported_claim" in finding_types:
            checks.append("Verify whether the final answer cites evidence that actually appears in the trace or evidence bundle.")
        if "missing_policy_signal" in finding_types:
            checks.append("Check whether required domain rules or escalation terms are missing from the answer.")
        if "missing_escalation" in finding_types:
            checks.append("Confirm whether a human reviewer should intervene before the answer is used.")
        if "risk_label_mismatch" in finding_types:
            checks.append("Compare the final answer with the expected risk label or reviewer expectation.")
        if not checks:
            checks.append("Spot-check one accepted case to verify the copilot is not over-escalating.")
        return checks
