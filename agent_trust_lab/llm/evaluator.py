from __future__ import annotations

from typing import Any

from ..reviewer import RISK_WEIGHTS, _collect_rule_hits, _recommendation, _trust_level
from ..schema import ReviewCase
from .client import LLMClient, LLMNotAvailableError, parse_evaluation_json
from .prompts import SYSTEM_PROMPT, build_user_prompt


class LLMEvaluator:
    def __init__(self, client: LLMClient | None = None):
        self._client = client

    def evaluate(self, case: ReviewCase) -> dict[str, Any]:
        client = self._client or LLMClient()
        user_prompt = build_user_prompt(case)
        raw = client.chat(SYSTEM_PROMPT, user_prompt)
        parsed = parse_evaluation_json(raw)

        if not parsed or "risk_score" not in parsed:
            return self._fallback(case, raw)

        findings = self._normalize_findings(parsed.get("findings", []))
        score = min(100, max(0, int(parsed.get("risk_score", 0))))
        trust = parsed.get("trust_level") or _trust_level(score)
        if trust not in ("low", "medium", "high"):
            trust = _trust_level(score)
        recommendation = parsed.get("recommendation") or _recommendation(score)
        rule_hits = parsed.get("rule_hits") or _collect_rule_hits(case, case.llm_output.lower())

        result: dict[str, Any] = {
            "case_id": case.case_id,
            "domain": case.domain,
            "risk_score": score,
            "trust_level": trust,
            "recommendation": recommendation,
            "rule_hits": rule_hits,
            "findings": findings,
            "human_review_required": recommendation != "accept_with_notes",
        }

        if parsed.get("analysis"):
            result["llm_analysis"] = parsed["analysis"]
        result["evaluator"] = "llm"
        result["model"] = client.model
        return result

    def _normalize_findings(self, raw_findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        valid_types = set(RISK_WEIGHTS.keys())
        cleaned: list[dict[str, Any]] = []
        for item in raw_findings:
            ftype = item.get("type", "").strip()
            if ftype not in valid_types:
                continue
            message = item.get("message", "").strip()
            if not message:
                continue
            entry: dict[str, Any] = {"type": ftype, "message": message}
            for key in ("terms", "expected_risk_level", "evidence_id", "rule_id"):
                if key in item:
                    entry[key] = item[key]
            cleaned.append(entry)
        return cleaned

    def _fallback(self, case: ReviewCase, raw_response: str) -> dict[str, Any]:
        from ..reviewer import evaluate_case

        result = evaluate_case(case)
        result["evaluator"] = "deterministic_fallback"
        result["llm_raw_response_preview"] = raw_response[:500]
        return result

    @staticmethod
    def is_available() -> bool:
        try:
            LLMClient()
            return True
        except LLMNotAvailableError:
            return False
