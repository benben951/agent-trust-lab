from __future__ import annotations

from typing import Any


ERROR_TAXONOMY: dict[str, dict[str, Any]] = {
    "unsupported_claim": {
        "category": "evidence_grounding",
        "severity": "high",
        "review_question": "Does the output make a risk claim that is not supported by the provided evidence?",
        "human_check": "Ask the reviewer to trace each risk claim back to a cited evidence item.",
    },
    "missing_policy_signal": {
        "category": "policy_alignment",
        "severity": "medium",
        "review_question": "Does the output ignore required policy or rule signals?",
        "human_check": "Check whether required policy terms or rule IDs are represented in the output.",
    },
    "unsafe_certainty": {
        "category": "calibration",
        "severity": "medium",
        "review_question": "Does the output sound more certain than the evidence supports?",
        "human_check": "Look for approval-like or absolute language in ambiguous or high-impact cases.",
    },
    "missing_escalation": {
        "category": "human_escalation",
        "severity": "high",
        "review_question": "Does the output reach a decision-like conclusion without routing to human review?",
        "human_check": "Confirm whether high-impact, uncertain, or policy-sensitive cases are escalated.",
    },
    "risk_label_mismatch": {
        "category": "risk_routing",
        "severity": "medium",
        "review_question": "Does the output align with the expected risk level and routing decision?",
        "human_check": "Compare the output's stated risk label with the case's expected risk level.",
    },
}


CASE_FAMILY_BY_DOMAIN: dict[str, str] = {
    "agent_coding": "agent_reliability",
    "agent_output_review": "agent_reliability",
    "agent_tool_use": "agent_reliability",
    "ai_data_quality": "data_quality_hr_education",
    "aml_monitoring": "aml_kyc_sanctions",
    "aml_onboarding": "aml_kyc_sanctions",
    "aml_transaction_monitoring": "aml_kyc_sanctions",
    "customer_support_compliance": "trust_safety_support",
    "customer_support_policy": "trust_safety_support",
    "data_quality_review": "data_quality_hr_education",
    "due_diligence": "due_diligence_legal",
    "education_ai_review": "data_quality_hr_education",
    "financial_services": "financial_risk",
    "health_safety": "health_safety",
    "hr_ai_review": "data_quality_hr_education",
    "kyc_onboarding": "aml_kyc_sanctions",
    "kyc_refresh": "aml_kyc_sanctions",
    "kyc_review": "aml_kyc_sanctions",
    "kyc_screening": "aml_kyc_sanctions",
    "legal_ai_review": "due_diligence_legal",
    "low_risk_control": "low_risk_control",
    "payment_fraud": "financial_risk",
    "sanctions_screening": "aml_kyc_sanctions",
    "trust_and_safety": "trust_safety_support",
    "trust_safety": "trust_safety_support",
    "vendor_due_diligence": "due_diligence_legal",
}


CASE_FAMILY_DESCRIPTIONS: dict[str, str] = {
    "agent_reliability": "Tool-use, coding-agent, browser-agent, and final-answer reliability cases.",
    "aml_kyc_sanctions": "AML, KYC, sanctions, onboarding, refresh, and screening review cases.",
    "data_quality_hr_education": "Data-quality, HR, and education AI review cases with sensitive or label-quality risks.",
    "due_diligence_legal": "Due diligence, vendor review, PEP, litigation, and legal-summary review cases.",
    "financial_risk": "Financial-services and payment-fraud review cases.",
    "health_safety": "Health or safety-support cases where unsafe certainty can cause harm.",
    "low_risk_control": "Low-risk control cases used to check over-escalation behavior.",
    "trust_safety_support": "Trust and safety plus customer-support policy cases.",
    "other": "Cases that do not yet map to a named family.",
}


def finding_taxonomy(finding_type: str) -> dict[str, Any]:
    return ERROR_TAXONOMY.get(
        finding_type,
        {
            "category": "unknown",
            "severity": "unknown",
            "review_question": "This finding type is not mapped in the public taxonomy.",
            "human_check": "Review the finding manually and update the taxonomy if it becomes recurring.",
        },
    )


def case_family_for_domain(domain: str | None) -> str:
    if not domain:
        return "other"
    return CASE_FAMILY_BY_DOMAIN.get(domain, "other")
