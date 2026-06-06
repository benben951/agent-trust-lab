from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .reviewer import evaluate_case
from .schema import ReviewCase


NAIVE_ACCEPT_MARKERS = (
    "accept",
    "approve",
    "approved",
    "no risk",
    "low risk",
    "routine monitoring",
)


def compare_naive_acceptance(cases: Iterable[ReviewCase]) -> dict[str, Any]:
    """Compare decision-like LLM wording with the trust-report workflow.

    The naive baseline intentionally models a weak reviewer that treats confident
    accept/approve language as usable. The trust workflow only accepts cases
    whose structured review does not require human review.
    """
    rows: list[dict[str, Any]] = []
    for case in cases:
        result = evaluate_case(case)
        naive_accept = _naive_accepts(case.llm_output)
        trust_accept = not result["human_review_required"]
        naive_false_accept = naive_accept and result["human_review_required"]
        rows.append(
            {
                "case_id": case.case_id,
                "domain": case.domain,
                "expected_risk_level": case.expected_risk_level,
                "naive_accept": naive_accept,
                "trust_workflow_accept": trust_accept,
                "naive_false_accept": naive_false_accept,
                "trust_workflow_manual_review": result["human_review_required"],
                "trust_level": result["trust_level"],
                "risk_score": result["risk_score"],
                "findings": [item["type"] for item in result["findings"]],
            }
        )

    total = len(rows)
    naive_accept_cases = sum(1 for row in rows if row["naive_accept"])
    trust_accept_cases = sum(1 for row in rows if row["trust_workflow_accept"])
    false_accept_cases = sum(1 for row in rows if row["naive_false_accept"])
    manual_review_cases = sum(1 for row in rows if row["trust_workflow_manual_review"])
    return {
        "total_cases": total,
        "naive_accept_cases": naive_accept_cases,
        "naive_accept_rate": _rate(naive_accept_cases, total),
        "naive_false_accept_cases": false_accept_cases,
        "naive_false_accept_rate": _rate(false_accept_cases, total),
        "trust_workflow_accept_cases": trust_accept_cases,
        "trust_workflow_accept_rate": _rate(trust_accept_cases, total),
        "trust_workflow_manual_review_cases": manual_review_cases,
        "trust_workflow_manual_review_rate": _rate(manual_review_cases, total),
        "rows": rows,
    }


def _naive_accepts(output: str) -> bool:
    output_lower = output.lower()
    return any(marker in output_lower for marker in NAIVE_ACCEPT_MARKERS)


def _rate(count: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round(count / total, 4)
