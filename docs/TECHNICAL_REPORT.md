# Evaluating Risk-Sensitive LLM Outputs With Trust Reports

Working technical report draft for Agent Trust Lab.

## Abstract

LLM and agent systems are increasingly used in workflows where incorrect confidence, missing evidence, or weak escalation behavior can create operational risk. This report introduces Agent Trust Lab, a public-safe evaluation prototype for reviewing LLM outputs in synthetic AML and compliance-style scenarios. The system generates structured trust reports that combine evidence checks, policy-signal checks, risk-language findings, formal error-taxonomy categories, case-family metrics, and human-review recommendations.

## 1. Motivation

Generic answer quality is not enough for risk-sensitive AI systems. A useful review workflow must answer:

- Is the output supported by evidence?
- Does it follow the relevant policy signals?
- Does it overstate certainty?
- Does it escalate when the case is ambiguous or high-risk?
- Can a human reviewer audit the decision chain?

## 2. System Overview

Agent Trust Lab evaluates a case package containing:

- user question
- LLM output
- synthetic evidence
- policy rules
- expected risk level

The current public demo uses deterministic checks to produce a Markdown and JSON trust report.

## 3. Evaluation Dimensions

| Dimension | Example failure | Why it matters |
|---|---|---|
| Evidence support | Mentions sanctions without evidence. | Prevents hallucinated risk claims. |
| Policy signal | Ignores required beneficial-ownership review. | Preserves compliance process. |
| Certainty control | Says "definitely no risk". | Reduces unsafe false pass. |
| Escalation | Approves ambiguous case directly. | Keeps humans accountable. |
| Risk alignment | Fails to mention expected medium risk. | Improves reviewer calibration. |

The public finding names are intentionally simple. For analysis, they are mapped into higher-level review categories:

| Finding | Taxonomy category | Reviewer question |
|---|---|---|
| `unsupported_claim` | `evidence_grounding` | Is the claim supported by the evidence packet? |
| `missing_policy_signal` | `policy_alignment` | Did the output preserve required policy signals? |
| `unsafe_certainty` | `calibration` | Is the output overconfident for the available evidence? |
| `missing_escalation` | `human_escalation` | Did the output preserve human review for ambiguous or high-risk cases? |
| `risk_label_mismatch` | `risk_routing` | Does the output align with the expected risk route? |

## 4. Demo Result

In the sample synthetic AML case, the reviewed LLM output incorrectly treats an ambiguous onboarding case as no-risk and approval-ready. Agent Trust Lab assigns a low trust level, a high risk score, and recommends rejection or escalation.

See `examples/trust_report_sample.md`.

## 4.1 v0.4 Case Library

The current demo expands from one synthetic AML case to a 52-case library covering AML onboarding, AML transaction monitoring, KYC review, sanctions screening, vendor due diligence, trust and safety, customer support compliance, agent output review, coding-agent review, AI data quality, HR screening, health-safety support, legal review, education support, financial services, and low-risk control cases.

The batch review command generates one Markdown trust report per case and a JSON summary for downstream dashboards or evaluation scripts.

## 4.2 v0.2 Static Review Console

The v0.2 demo adds a static browser review console under `web/`. The console presents aggregate risk metrics, a filterable synthetic case queue, trust levels, findings, recommendations, and a trust-report preview. It is intentionally static so it can be hosted easily while keeping patent-sensitive implementation details outside the public interface.

## 4.3 Evaluation Metrics Summary

The public demo includes a reproducible metrics summary generated from the 52-case synthetic review library. The summary is intentionally focused on review-routing behavior rather than generic accuracy.

| Metric | Value |
|---|---:|
| Total synthetic cases | 52 |
| Manual review cases | 32 |
| Manual review rate | 61.5% |
| Low-trust cases | 25 |
| Low-trust rate | 48.1% |
| Average risk score | 45.77 |

The most frequent findings are `risk_label_mismatch`, `missing_policy_signal`, and `missing_escalation`. This reflects the central design principle of the prototype: in risk-sensitive AI workflows, escalation is a valid safety outcome when evidence, policy support, or uncertainty handling is weak.

See `docs/EVALUATION_METRICS.md` and `examples/evaluation_metrics.json`.

The same metrics file includes taxonomy category distribution and case-family metrics. On the current 52-case set, the largest taxonomy categories are `risk_routing` (33), `policy_alignment` (30), `human_escalation` (30), `calibration` (23), and `evidence_grounding` (9). The largest case family is `aml_kyc_sanctions` with 13 cases, followed by `agent_reliability` and `trust_safety_support` with 7 cases each.

These additions make the evaluation more useful for project iteration. Aggregate metrics show the overall review posture, taxonomy metrics show recurring error classes, and case-family metrics show which scenario groups need more examples or reviewer calibration.

## 4.4 Naive Baseline Comparison

Agent Trust Lab compares the structured trust workflow against a deliberately weak baseline that treats confident accept/approve language as usable. On the current 52-case synthetic set, the naive baseline accepts 38 cases and produces 25 false accepts under the trust-workflow review criteria. The trust workflow accepts 20 cases and routes 32 cases to manual review.

This is not a production accuracy claim. It is a public-safe demonstration of a common LLM risk: confident language can look operationally complete even when evidence, policy signals, or escalation behavior are missing.

See `examples/baseline_comparison.md` and `examples/baseline_comparison.json`.

## 5. Relationship To Portfolio Projects

- `llm-proxy-auditor` checks whether an LLM gateway can be trusted.
- `agent-workflow-bench` evaluates multi-agent workflow behavior.
- `gemma-aml-assistant` provides a regulated-domain RAG scenario.
- Agent Trust Lab combines these ideas into a product-facing trust report workflow.

## 6. Limitations

- Current examples are synthetic.
- Deterministic checks are intentionally simple.
- No production policy, customer data, or internal labels are used.
- Private patent-facing design details are excluded from the public report.

## 7. Next Steps

- Expand the synthetic case library toward 50 cases with explicit difficulty labels.
- Balance thin case families such as financial risk, health-safety, and low-risk controls.
- Add JSON report output examples.
- Add reviewer override tracking.
- Add benchmark tasks through `agent-workflow-bench`.
- Add interactive case upload after the patent filing strategy is settled.
