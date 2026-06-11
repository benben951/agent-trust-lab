from __future__ import annotations

DEFAULT_RULEPACKS = {
    "agent_output_review": "agent_tool_use",
    "aml_onboarding": "financial_risk",
    "aml_transaction_monitoring": "financial_risk",
    "kyc_review": "financial_risk",
    "trust_and_safety": "trust_safety",
    "customer_support_compliance": "support_compliance",
    "health_safety": "health_safety",
    "low_risk_control": "low_risk_control",
}


def select_rulepack(domain: str) -> str:
    return DEFAULT_RULEPACKS.get(domain, "general_review")
