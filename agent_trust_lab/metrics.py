from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .taxonomy import CASE_FAMILY_DESCRIPTIONS, ERROR_TAXONOMY, case_family_for_domain, finding_taxonomy


def load_batch_summary(path: str | Path) -> list[dict[str, Any]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def summarize_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    total_cases = len(results)
    if total_cases == 0:
        return {
            "total_cases": 0,
            "manual_review_cases": 0,
            "manual_review_rate": 0.0,
            "low_trust_cases": 0,
            "low_trust_rate": 0.0,
            "average_risk_score": 0.0,
            "trust_level_distribution": {},
            "recommendation_distribution": {},
            "finding_distribution": {},
            "domain_distribution": {},
            "taxonomy_category_distribution": {},
            "case_family_distribution": {},
            "case_family_metrics": {},
            "error_taxonomy": ERROR_TAXONOMY,
            "case_family_descriptions": CASE_FAMILY_DESCRIPTIONS,
        }

    manual_review_cases = sum(1 for item in results if item.get("human_review_required"))
    low_trust_cases = sum(1 for item in results if item.get("trust_level") == "low")
    risk_scores = [int(item.get("risk_score", 0)) for item in results]
    findings: Counter[str] = Counter()
    taxonomy_categories: Counter[str] = Counter()
    for item in results:
        item_findings = item.get("findings", [])
        findings.update(item_findings)
        taxonomy_categories.update(finding_taxonomy(finding)["category"] for finding in item_findings)

    return {
        "total_cases": total_cases,
        "manual_review_cases": manual_review_cases,
        "manual_review_rate": round(manual_review_cases / total_cases, 4),
        "low_trust_cases": low_trust_cases,
        "low_trust_rate": round(low_trust_cases / total_cases, 4),
        "average_risk_score": round(sum(risk_scores) / total_cases, 2),
        "max_risk_score": max(risk_scores),
        "min_risk_score": min(risk_scores),
        "trust_level_distribution": dict(Counter(item.get("trust_level") for item in results)),
        "recommendation_distribution": dict(Counter(item.get("recommendation") for item in results)),
        "finding_distribution": dict(findings),
        "domain_distribution": dict(Counter(item.get("domain") for item in results)),
        "taxonomy_category_distribution": dict(taxonomy_categories),
        "case_family_distribution": dict(
            Counter(case_family_for_domain(item.get("domain")) for item in results)
        ),
        "case_family_metrics": _summarize_case_families(results),
        "error_taxonomy": ERROR_TAXONOMY,
        "case_family_descriptions": CASE_FAMILY_DESCRIPTIONS,
    }


def _summarize_case_families(results: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in results:
        family = case_family_for_domain(item.get("domain"))
        grouped.setdefault(family, []).append(item)

    summary: dict[str, dict[str, Any]] = {}
    for family, items in sorted(grouped.items()):
        total_cases = len(items)
        manual_review_cases = sum(1 for item in items if item.get("human_review_required"))
        low_trust_cases = sum(1 for item in items if item.get("trust_level") == "low")
        risk_scores = [int(item.get("risk_score", 0)) for item in items]
        findings: Counter[str] = Counter()
        taxonomy_categories: Counter[str] = Counter()
        for item in items:
            item_findings = item.get("findings", [])
            findings.update(item_findings)
            taxonomy_categories.update(finding_taxonomy(finding)["category"] for finding in item_findings)

        summary[family] = {
            "description": CASE_FAMILY_DESCRIPTIONS.get(family, CASE_FAMILY_DESCRIPTIONS["other"]),
            "total_cases": total_cases,
            "manual_review_cases": manual_review_cases,
            "manual_review_rate": round(manual_review_cases / total_cases, 4),
            "low_trust_cases": low_trust_cases,
            "low_trust_rate": round(low_trust_cases / total_cases, 4),
            "average_risk_score": round(sum(risk_scores) / total_cases, 2),
            "trust_level_distribution": dict(Counter(item.get("trust_level") for item in items)),
            "recommendation_distribution": dict(Counter(item.get("recommendation") for item in items)),
            "finding_distribution": dict(findings),
            "taxonomy_category_distribution": dict(taxonomy_categories),
            "domain_distribution": dict(Counter(item.get("domain") for item in items)),
        }
    return summary
