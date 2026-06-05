from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


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
        }

    manual_review_cases = sum(1 for item in results if item.get("human_review_required"))
    low_trust_cases = sum(1 for item in results if item.get("trust_level") == "low")
    risk_scores = [int(item.get("risk_score", 0)) for item in results]
    findings: Counter[str] = Counter()
    for item in results:
        findings.update(item.get("findings", []))

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
    }

