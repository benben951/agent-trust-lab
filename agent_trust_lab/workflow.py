from __future__ import annotations

from typing import Any

from .reviewer import evaluate_case
from .schema import ReviewCase


def evaluate_workflow(case: ReviewCase) -> dict[str, Any]:
    """Create a public-safe multi-role review trace for one synthetic case.

    This demo decomposes the existing trust review into role-specific notes
    without exposing private scoring or patent-facing orchestration details.
    """
    base = evaluate_case(case)
    finding_types = {item["type"] for item in base["findings"]}
    role_reviews = [
        _role_review(
            "evidence_reviewer",
            "Checks whether output claims are grounded in provided evidence.",
            "fail" if "unsupported_claim" in finding_types else "pass",
            _evidence_notes(case, finding_types),
        ),
        _role_review(
            "policy_reviewer",
            "Checks whether the output references required policy signals.",
            "fail" if "missing_policy_signal" in finding_types else "pass",
            _policy_notes(base),
        ),
        _role_review(
            "risk_reviewer",
            "Checks risk-label alignment and unsafe certainty.",
            "fail" if {"unsafe_certainty", "risk_label_mismatch"} & finding_types else "pass",
            _risk_notes(case, finding_types),
        ),
        _role_review(
            "escalation_reviewer",
            "Checks whether uncertain or decision-like outputs are routed to humans.",
            "fail" if "missing_escalation" in finding_types else "pass",
            _escalation_notes(base, finding_types),
        ),
    ]
    role_reviews.append(
        _role_review(
            "final_reviewer",
            "Combines role findings into a human-in-the-loop recommendation.",
            "fail" if base["human_review_required"] else "pass",
            [
                f"Trust level: {base['trust_level']}.",
                f"Risk score: {base['risk_score']}/100.",
                f"Recommendation: {base['recommendation']}.",
                f"Human review required: {base['human_review_required']}.",
            ],
        )
    )

    failed_roles = [item["role"] for item in role_reviews if item["status"] == "fail"]
    return {
        "case_id": case.case_id,
        "domain": case.domain,
        "base_review": base,
        "role_reviews": role_reviews,
        "failed_roles": failed_roles,
        "workflow_status": "needs_human_review" if failed_roles else "review_passed",
        "public_safety_note": (
            "This workflow trace is generated from synthetic public-safe data and "
            "does not automate high-risk approval decisions."
        ),
    }


def render_workflow_markdown(case: ReviewCase, workflow: dict[str, Any]) -> str:
    base = workflow["base_review"]
    role_lines = "\n".join(_render_role(item) for item in workflow["role_reviews"])
    failed_roles = ", ".join(f"`{item}`" for item in workflow["failed_roles"]) or "None"
    finding_lines = "\n".join(
        f"- `{item['type']}`: {item['message']}" for item in base["findings"]
    ) or "- No major finding."

    return f"""# Multi-Role Agent Trust Workflow Report

## Case

- Case ID: `{case.case_id}`
- Domain: `{case.domain}`
- Expected risk level: `{case.expected_risk_level}`
- Workflow status: `{workflow['workflow_status']}`
- Failed roles: {failed_roles}

## Final Routing

- Trust level: `{base['trust_level']}`
- Risk score: `{base['risk_score']}/100`
- Recommendation: `{base['recommendation']}`
- Human review required: `{base['human_review_required']}`

## Role Trace

{role_lines}

## Findings

{finding_lines}

## Public Safety Boundary

{workflow['public_safety_note']}
"""


def _role_review(role: str, objective: str, status: str, notes: list[str]) -> dict[str, Any]:
    return {
        "role": role,
        "objective": objective,
        "status": status,
        "notes": notes,
    }


def _evidence_notes(case: ReviewCase, finding_types: set[str]) -> list[str]:
    notes = [f"Evidence items reviewed: {len(case.evidence)}."]
    if "unsupported_claim" in finding_types:
        notes.append("The output includes risk claims that are not grounded in the synthetic evidence.")
    else:
        notes.append("No unsupported risk claim was detected by the public demo checks.")
    return notes


def _policy_notes(base: dict[str, Any]) -> list[str]:
    if base["rule_hits"]:
        return [f"Policy rule hits: {', '.join(base['rule_hits'])}."]
    return ["No required policy signal was found in the output."]


def _risk_notes(case: ReviewCase, finding_types: set[str]) -> list[str]:
    notes = [f"Expected risk level: {case.expected_risk_level}."]
    if "unsafe_certainty" in finding_types:
        notes.append("The output uses high-certainty language in a risk-sensitive context.")
    if "risk_label_mismatch" in finding_types:
        notes.append("The output does not explicitly align with the expected risk level.")
    if len(notes) == 1:
        notes.append("Risk label and certainty checks passed in the public demo.")
    return notes


def _escalation_notes(base: dict[str, Any], finding_types: set[str]) -> list[str]:
    if "missing_escalation" in finding_types:
        return ["The output reaches a decision-like conclusion without human escalation."]
    if base["human_review_required"]:
        return ["Human review is required due to the aggregate trust review."]
    return ["The output can be accepted with notes under the public demo checks."]


def _render_role(item: dict[str, Any]) -> str:
    notes = "\n".join(f"  - {note}" for note in item["notes"])
    return f"""### `{item['role']}`: `{item['status']}`

Objective: {item['objective']}

Notes:
{notes}
"""
