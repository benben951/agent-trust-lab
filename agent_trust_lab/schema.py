from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    text: str
    source: str


@dataclass(frozen=True)
class PolicyRule:
    rule_id: str
    text: str
    required_terms: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ReviewCase:
    case_id: str
    domain: str
    user_question: str
    llm_output: str
    expected_risk_level: str
    evidence: list[EvidenceItem]
    policy_rules: list[PolicyRule]
    metadata: dict[str, Any] = field(default_factory=dict)

