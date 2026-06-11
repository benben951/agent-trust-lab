from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentOutputPackage:
    final_output: str
    tool_trace: list[str] = field(default_factory=list)
    evidence_snippets: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CopilotInput:
    case_id: str
    domain: str
    user_request: str
    agent_output: AgentOutputPackage
    reviewer_notes: list[str] = field(default_factory=list)


@dataclass
class CopilotEvidence:
    claims: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    normalized_evidence: list[str] = field(default_factory=list)
    trace_summary: str = ""


@dataclass
class CopilotDecision:
    recommendation: str
    trust_level: str
    risk_score: int
    findings: list[dict[str, Any]] = field(default_factory=list)
    next_checks: list[str] = field(default_factory=list)


@dataclass
class CopilotSession:
    review_input: CopilotInput
    evidence: CopilotEvidence
    decision: CopilotDecision
    selected_rulepack: str
    memory_keys: list[str] = field(default_factory=list)
