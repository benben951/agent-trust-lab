# Evaluating Risk-Sensitive LLM Outputs With Trust Reports

Working technical report draft for Agent Trust Lab.

## Abstract

LLM and agent systems are increasingly used in workflows where incorrect confidence, missing evidence, or weak escalation behavior can create operational risk. This report introduces Agent Trust Lab, a public-safe evaluation prototype for reviewing LLM outputs in synthetic AML and compliance-style scenarios. The system generates structured trust reports that combine evidence checks, policy-signal checks, risk-language findings, and human-review recommendations.

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

## 4. Demo Result

In the sample synthetic AML case, the reviewed LLM output incorrectly treats an ambiguous onboarding case as no-risk and approval-ready. Agent Trust Lab assigns a low trust level, a high risk score, and recommends rejection or escalation.

See `examples/trust_report_sample.md`.

## 4.1 v0.1 Case Library

The v0.1 demo expands from one synthetic AML case to a 10-case library covering AML onboarding, AML transaction monitoring, KYC review, vendor due diligence, trust and safety, customer support compliance, agent output review, AI data quality, sanctions screening, and a low-risk control case.

The batch review command generates one Markdown trust report per case and a JSON summary for downstream dashboards or evaluation scripts.

## 4.2 v0.2 Static Review Console

The v0.2 demo adds a static browser review console under `web/`. The console presents aggregate risk metrics, a filterable synthetic case queue, trust levels, findings, recommendations, and a trust-report preview. It is intentionally static so it can be hosted easily while keeping patent-sensitive implementation details outside the public interface.

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

- Add more synthetic cases across AML, KYC, due diligence, and trust and safety.
- Add JSON report output examples.
- Add reviewer override tracking.
- Add benchmark tasks through `agent-workflow-bench`.
- Add interactive case upload after the patent filing strategy is settled.
