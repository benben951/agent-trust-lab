# Agent Trust Lab Review Packet

This packet is the recruiter- and interviewer-facing entry point for Agent Trust Lab.

Agent Trust Lab is a public-safe prototype for reviewing LLM and agent outputs in risk-sensitive workflows. It turns an LLM output into a structured trust report with evidence checks, policy-signal checks, failure findings, risk scoring, and a human-review recommendation.

## 1. Three-Minute Summary

| Question | Answer |
|---|---|
| What problem does it solve? | Risk-sensitive LLM outputs can sound confident while missing evidence, policy signals, or required escalation. |
| What does the system produce? | Markdown and JSON trust reports for each reviewed case, plus aggregate evaluation metrics. |
| What domains are simulated? | AML, KYC, due diligence, trust and safety, customer support compliance, agent output review, AI data quality, sanctions screening, and low-risk control. |
| What is the decision boundary? | The system recommends accept, escalate, or reject/escalate. It does not automate high-risk approval decisions. |
| What data is used? | Synthetic public-safe cases only. No customer data, private policy, internal labels, secrets, or patent claim text. |

Live demo: [https://benben951.github.io/agent-trust-lab/](https://benben951.github.io/agent-trust-lab/)

## 2. Why This Is Relevant To LLM Evaluation Roles

| Hiring Signal | Project Evidence |
|---|---|
| LLM output evaluation | 10 synthetic cases with failure findings and trust levels. |
| Human-in-the-loop review | Medium/high-risk or uncertain cases are routed to manual review. |
| Risk and compliance judgment | Findings include unsafe certainty, unsupported claim, missing policy signal, missing escalation, and risk-label mismatch. |
| Evaluation artifacts | Each case generates a Markdown trust report and machine-readable JSON summary. |
| Metrics thinking | Batch metrics track manual-review rate, low-trust rate, risk-score distribution, recommendations, and finding frequencies. |
| Governance awareness | The repository explicitly documents data, decision, logging, and public-demo boundaries. |

## 3. System Flow

```text
synthetic case + LLM output
        |
        v
evidence and policy checks
        |
        v
failure finding taxonomy
        |
        v
risk score + trust level
        |
        v
human-review recommendation
        |
        v
Markdown / JSON trust report
        |
        v
batch evaluation metrics
```

## 4. Case Library

| Case ID | Domain | Scenario | Trust Level | Recommendation |
|---|---|---|---|---|
| `SYN-AML-001` | AML onboarding | Unsafe false pass in incomplete onboarding evidence. | Low | Reject or escalate |
| `SYN-AML-002` | AML transaction monitoring | Transaction-behavior mismatch with weak escalation. | Medium | Escalate for manual review |
| `SYN-KYC-001` | KYC review | Conflicting identity/address evidence. | Medium | Escalate for manual review |
| `SYN-DD-001` | Vendor due diligence | Acceptable output with review notes. | High | Accept with notes |
| `SYN-TS-001` | Trust and safety | Unsupported fraud claim and unsafe user-impacting decision. | Low | Reject or escalate |
| `SYN-CS-001` | Customer support compliance | Unsupported compensation or policy guarantee. | Medium | Escalate for manual review |
| `SYN-AGENT-001` | Agent output review | Tool failure ignored by final agent conclusion. | Low | Reject or escalate |
| `SYN-DQ-001` | AI data quality | Label conflict and calibration risk. | Medium | Escalate for manual review |
| `SYN-SAN-001` | Sanctions screening | False-positive risk and overconfident match handling. | Low | Reject or escalate |
| `SYN-SAFE-001` | Low-risk control | Safe case that should not be over-escalated. | High | Accept with notes |

## 5. Current Metrics

Generated from `examples/batch_summary.json` and `examples/evaluation_metrics.json`.

| Metric | Value |
|---|---:|
| Total synthetic cases | 10 |
| Manual review cases | 8 |
| Manual review rate | 80% |
| Low-trust cases | 4 |
| Low-trust rate | 40% |
| Average risk score | 53.0 |
| Max risk score | 100 |
| Min risk score | 0 |

Trust distribution:

| Trust level | Count |
|---|---:|
| Low | 4 |
| Medium | 4 |
| High | 2 |

Recommendation distribution:

| Recommendation | Count |
|---|---:|
| `reject_or_escalate` | 4 |
| `escalate_for_manual_review` | 4 |
| `accept_with_notes` | 2 |

Finding distribution:

| Finding | Count |
|---|---:|
| `risk_label_mismatch` | 9 |
| `missing_policy_signal` | 7 |
| `missing_escalation` | 5 |
| `unsafe_certainty` | 4 |
| `unsupported_claim` | 3 |

## 6. Example Reports

Representative generated reports:

| Report | What it shows |
|---|---|
| [`SYN-AML-001`](../examples/reports/SYN-AML-001.md) | Detects unsafe low-risk approval and unsupported risk claims in an AML onboarding-style case. |
| [`SYN-AGENT-001`](../examples/reports/SYN-AGENT-001.md) | Detects a final agent answer that ignores a failed lookup tool call. |
| [`SYN-SAN-001`](../examples/reports/SYN-SAN-001.md) | Detects overconfident sanctions-screening handling and false-positive risk. |
| [`SYN-SAFE-001`](../examples/reports/SYN-SAFE-001.md) | Shows that the system can accept a low-risk control case with notes. |

## 7. Reproduce The Evaluation

Run tests:

```powershell
python -m pytest -q
```

Generate trust reports for the synthetic case library:

```powershell
python -m agent_trust_lab.cli batch-review `
  --cases-dir examples\cases `
  --out-dir examples\reports `
  --summary examples\batch_summary.json
```

Generate aggregate metrics:

```powershell
python -m agent_trust_lab.cli summarize `
  --summary examples\batch_summary.json `
  --out examples\evaluation_metrics.json
```

Run the local web demo:

```powershell
python -m http.server 8765
```

Then open:

```text
http://localhost:8765/web/
```

## 8. Interview Pitch

Short version:

> I built Agent Trust Lab to evaluate whether LLM or agent outputs are safe enough to accept, escalate, or reject in risk-sensitive workflows. The prototype uses synthetic AML, KYC, due-diligence, trust-and-safety, and agent-review cases. It generates trust reports, routes risky outputs to human review, and summarizes evaluation metrics such as manual-review rate, low-trust rate, recommendation distribution, and recurring failure types.

Chinese version:

> 我做的 Agent Trust Lab 是一个面向风险敏感场景的大模型输出复审与信任报告系统。它不是让模型直接替人做高风险决策，而是把模型输出拆成证据支持、政策信号、确定性控制、升级建议和风险标签一致性几个维度，生成可审计的 trust report，并把不确定或高风险输出路由给人工复审。

## 9. Resume Bullets

- Built Agent Trust Lab, a public-safe LLM output review prototype for AML/KYC, due diligence, trust and safety, AI data-quality, and agent-output evaluation scenarios.
- Designed a 10-case synthetic evaluation library and generated structured Markdown/JSON trust reports with risk findings, trust levels, escalation recommendations, and aggregate review-routing metrics.
- Implemented human-in-the-loop governance boundaries to avoid automated high-risk approval and make unsafe certainty, unsupported claims, missing policy signals, and missing escalation visible to reviewers.

## 10. Public-Safe Boundary

This repository intentionally avoids:

- real customer data
- internal company policy
- private annotation labels
- credentials or secrets
- patent claim text
- production approval automation for financial, compliance, or user-impacting decisions

The current metrics are demo metrics from a synthetic evaluation set. They are not production model-performance claims.
