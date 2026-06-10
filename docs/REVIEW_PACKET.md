# Agent Trust Lab Review Packet

This packet is the recruiter- and interviewer-facing entry point for Agent Trust Lab.

Agent Trust Lab is a public-safe prototype for reviewing LLM and agent outputs in risk-sensitive workflows. It turns an LLM output into a structured trust report with evidence checks, policy-signal checks, failure findings, risk scoring, and a human-review recommendation.

## 1. Three-Minute Summary

| Question | Answer |
|---|---|
| What problem does it solve? | Risk-sensitive LLM outputs can sound confident while missing evidence, policy signals, or required escalation. |
| What does the system produce? | Markdown and JSON trust reports for each reviewed case, plus aggregate evaluation metrics. |
| What workflow evidence is included? | A public-safe multi-role workflow trace with evidence, policy, risk, escalation, and final reviewer notes. |
| What domains are simulated? | AML, KYC, due diligence, trust and safety, customer support compliance, agent output review, AI data quality, sanctions screening, and low-risk control. |
| What is the decision boundary? | The system recommends accept, escalate, or reject/escalate. It does not automate high-risk approval decisions. |
| What data is used? | Synthetic public-safe cases only. No customer data, private policy, internal labels, secrets, or patent claim text. |

Live demo: [https://benben951.github.io/agent-trust-lab/](https://benben951.github.io/agent-trust-lab/)

Fast walkthrough: [CASE_WALKTHROUGH.md](CASE_WALKTHROUGH.md)

Three-minute demo path: [DEMO_WALKTHROUGH.md](DEMO_WALKTHROUGH.md)

Context engineering note: [CONTEXT_ENGINEERING.md](CONTEXT_ENGINEERING.md)

Human spot-check protocol: [HUMAN_SPOT_CHECK_PROTOCOL.md](HUMAN_SPOT_CHECK_PROTOCOL.md)

Human spot-check log: [HUMAN_SPOT_CHECK_LOG.md](HUMAN_SPOT_CHECK_LOG.md)

Error taxonomy: [ERROR_TAXONOMY.md](ERROR_TAXONOMY.md)

Reusable workflow recipes: [WORKFLOW_RECIPES.md](WORKFLOW_RECIPES.md)

## 2. Why This Is Relevant To LLM Evaluation Roles

| Hiring Signal | Project Evidence |
|---|---|
| LLM output evaluation | 52 synthetic cases with failure findings and trust levels. |
| Human-in-the-loop review | Medium/high-risk or uncertain cases are routed to manual review. |
| Risk and compliance judgment | Findings include unsafe certainty, unsupported claim, missing policy signal, missing escalation, and risk-label mismatch. |
| Evaluation artifacts | Each case generates a Markdown trust report and machine-readable JSON summary. |
| Agent workflow thinking | `workflow-review` decomposes one case into evidence, policy, risk, escalation, and final reviewer roles. |
| Reusable workflow design | `WORKFLOW_RECIPES.md` converts common review scenarios into repeatable recipes with triggers, inputs, roles, findings, artifacts, and human routes. |
| Context engineering | Docs, generated reports, CLI commands, tests, and browser checks make AI-assisted changes reviewable. |
| Metrics thinking | Batch metrics track manual-review rate, low-trust rate, risk-score distribution, recommendations, finding frequencies, and naive false-accept behavior. |
| Error analysis | Formal taxonomy maps raw findings into evidence grounding, policy alignment, calibration, human escalation, and risk routing. |
| Coverage analysis | Case-family metrics show routing behavior across AML/KYC/sanctions, trust and safety, data quality, due diligence, legal, financial, health-safety, and agent-reliability scenarios. |
| Human spot-check readiness | A public-safe protocol defines sampled manual review, route agreement, over-trigger checks, missed-finding checks, and release gates. |
| Quality loop | A 15-case author spot-check found a missing-escalation edge case, added a regression test, and regenerated reports. |
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

The public workflow trace intentionally shows role-level review notes without exposing private scoring formulas, dynamic weighting, or patent-facing orchestration details.

Reusable workflow recipes document how to apply the same review pattern across
AML false-pass, agent tool-failure, financial advice, health-safety escalation,
and low-risk control scenarios.

## 4. Case Library

The public case library currently contains 52 synthetic public-safe cases. The table below shows representative examples rather than every case.

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
| Total synthetic cases | 52 |
| Manual review cases | 32 |
| Manual review rate | 61.5% |
| Low-trust cases | 25 |
| Low-trust rate | 48.1% |
| Average risk score | 45.77 |
| Max risk score | 100 |
| Min risk score | 0 |

Trust distribution:

| Trust level | Count |
|---|---:|
| Low | 25 |
| Medium | 7 |
| High | 20 |

Recommendation distribution:

| Recommendation | Count |
|---|---:|
| `reject_or_escalate` | 25 |
| `escalate_for_manual_review` | 7 |
| `accept_with_notes` | 20 |

Finding distribution:

| Finding | Count |
|---|---:|
| `risk_label_mismatch` | 33 |
| `missing_policy_signal` | 30 |
| `missing_escalation` | 30 |
| `unsafe_certainty` | 23 |
| `unsupported_claim` | 9 |

Taxonomy category distribution:

| Category | Count |
|---|---:|
| `risk_routing` | 33 |
| `policy_alignment` | 30 |
| `human_escalation` | 30 |
| `calibration` | 23 |
| `evidence_grounding` | 9 |

Representative case-family metrics:

| Case family | Cases | Manual review rate | Low-trust rate |
|---|---:|---:|---:|
| `aml_kyc_sanctions` | 13 | 69.23% | 53.85% |
| `agent_reliability` | 7 | 71.43% | 71.43% |
| `trust_safety_support` | 7 | 57.14% | 28.57% |
| `data_quality_hr_education` | 6 | 83.33% | 50.00% |
| `due_diligence_legal` | 5 | 60.00% | 60.00% |
| `financial_risk` | 5 | 60.00% | 60.00% |
| `health_safety` | 5 | 60.00% | 40.00% |
| `low_risk_control` | 4 | 0.00% | 0.00% |

Naive baseline comparison:

| Metric | Value |
|---|---:|
| Naive accept cases | 38 |
| Naive false accept cases | 25 |
| Naive false accept rate | 48% |
| Trust workflow accept cases | 20 |
| Trust workflow manual review cases | 32 |

## 6. Example Reports

Representative generated reports:

| Report | What it shows |
|---|---|
| [`SYN-AML-001`](../examples/reports/SYN-AML-001.md) | Detects unsafe low-risk approval and unsupported risk claims in an AML onboarding-style case. |
| [`SYN-AGENT-001`](../examples/reports/SYN-AGENT-001.md) | Detects a final agent answer that ignores a failed lookup tool call. |
| [`Workflow trace: SYN-AGENT-001`](../examples/workflow_report_agent_tool_failure.md) | Shows evidence, policy, risk, escalation, and final reviewer role notes for an ignored tool failure. |
| [`Workflow recipes`](WORKFLOW_RECIPES.md) | Shows how one-off LLM review prompts become reusable, auditable review workflows. |
| [`Case walkthrough: SYN-AGENT-001`](CASE_WALKTHROUGH.md) | Explains the input, evidence package, role trace, final routing, and safety boundary in recruiter-friendly form. |
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

Generate the naive-baseline comparison:

```powershell
python -m agent_trust_lab.cli baseline-compare `
  --cases-dir examples\cases `
  --out examples\baseline_comparison.json `
  --markdown-out examples\baseline_comparison.md
```

Generate a multi-role workflow trace:

```powershell
python -m agent_trust_lab.cli workflow-review `
  --case examples\cases\agent_tool_failure.json `
  --out examples\workflow_report_agent_tool_failure.md `
  --json-out examples\workflow_report_agent_tool_failure.json
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

> I built Agent Trust Lab to evaluate whether LLM or agent outputs are safe enough to accept, escalate, or reject in risk-sensitive workflows. The prototype uses 52 synthetic AML, KYC, due-diligence, trust-and-safety, and agent-review cases. It generates trust reports, multi-role workflow traces, human-review routing decisions, naive-baseline comparisons, and evaluation metrics such as manual-review rate, low-trust rate, recommendation distribution, and recurring failure types.

Chinese version:

> 我做 Agent Trust Lab 的核心原因是：在风控、合规、Trust & Safety 和 Agent 输出复审场景里，模型回答流畅并不代表可以被信任。这个项目用 52 个公开安全的 synthetic cases，把 LLM 或 Agent 输出转成可审计的 trust report，检查证据支撑、规则信号、风险标签、升级处理和最终路由，并通过 naive baseline 对比说明“自信输出直接接受”会带来的 false-accept 风险。

## 9. Resume Bullets

- Built Agent Trust Lab, a public-safe LLM output review prototype for AML/KYC, due diligence, trust and safety, AI data-quality, and agent-output evaluation scenarios.
- Designed a 52-case synthetic evaluation library and generated structured Markdown/JSON trust reports with risk findings, trust levels, escalation recommendations, baseline comparison, and aggregate review-routing metrics.
- Added a formal error taxonomy and case-family metrics to analyze evidence grounding, policy alignment, calibration, human escalation, risk routing, and scenario coverage across risk-sensitive domains.
- Added a public-safe multi-role workflow trace covering evidence, policy, risk, escalation, and final reviewer notes for agent-output review.
- Published a recruiter-friendly case walkthrough for a synthetic tool-failure scenario, connecting the input evidence, policy rule, role-level failures, final routing, and safety boundary.
- Documented a Codex-first context-engineering workflow using explicit project memory, generated artifacts, CLI reproduction commands, tests, and browser-demo checks.
- Defined a public-safe human spot-check protocol for sampling synthetic cases, recording route agreement, identifying over-triggered findings, and tracking missed findings before public sharing.
- Ran a 15-case author spot-check, identified a denied-clinician-review escalation edge case, added a regression test, and regenerated trust reports and metrics.
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
