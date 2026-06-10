# Agent Trust Lab: Human-in-the-Loop Trust Reports for Risk-Sensitive LLM Outputs

Working EMNLP 2026 System Demonstration draft.

## Abstract

Large language models and agent workflows are increasingly used in risk-sensitive settings such as compliance review, due diligence, customer support, trust and safety, and AI data-quality calibration. In these settings, fluent answers are not enough: reviewers need to know whether an output is supported by evidence, aligned with policy signals, calibrated in uncertainty, and safe to route without bypassing human review. We present Agent Trust Lab, a public-safe system demonstration for generating structured trust reports for LLM and agent outputs. The prototype evaluates synthetic risk cases across AML, KYC, sanctions screening, due diligence, trust and safety, customer support, HR review, health-safety support, legal review, financial services, and agent tool-use scenarios. It produces Markdown and JSON trust reports, aggregate review-routing metrics, a formal error taxonomy, case-family metrics, a naive-baseline comparison, and public-safe multi-role workflow traces. On a 52-case synthetic case library, a naive confident-output baseline accepts 38 cases and produces 25 false accepts under the trust-workflow criteria, while Agent Trust Lab routes 32 cases to human review and accepts 20 with notes. The demo is designed to support human reviewers rather than automate high-risk decisions.

## 1. Introduction

LLM evaluation often focuses on answer quality, task success, or benchmark accuracy. Risk-sensitive workflows require an additional question: should this model output be trusted enough to use, escalate, reject, or revise?

Common failure modes include:

- unsupported risk claims
- missing evidence
- missing policy signals
- unsafe certainty
- missing escalation
- risk-label mismatch
- ignored tool failure in agent workflows

Agent Trust Lab turns these failure modes into structured review artifacts.

## 2. Related Work and Positioning

Agent Trust Lab sits between several active evaluation and deployment threads:

- **LLM evaluation and hallucination analysis.** Existing work often measures factuality, faithfulness, task success, or benchmark performance. Agent Trust Lab focuses on review-routing artifacts: what a human reviewer needs to inspect before trusting a model output.
- **RAG faithfulness and evidence grounding.** Retrieval-augmented systems require outputs to cite and preserve evidence. Agent Trust Lab generalizes this idea to risk-sensitive review packets where evidence, policy signals, and escalation behavior all matter.
- **Agent evaluation and tool-use reliability.** Tool-using agents can fail even when the final answer is fluent. Agent Trust Lab includes agent-output cases where tool failures, browser warnings, or missing test evidence are ignored by the final response.
- **Human-in-the-loop AI governance.** Many high-impact workflows should not be fully automated. The system treats escalation as a valid outcome and records review artifacts rather than replacing accountable human decisions.

The intended contribution is not a new foundation model or a production compliance system. The contribution is an inspectable system demonstration for turning LLM outputs into structured trust reports that can be reproduced, audited, and extended.

## 3. System Overview

The demo accepts a synthetic case package with:

- a user or analyst question
- an LLM output under review
- synthetic evidence
- simplified public-safe policy rules
- expected risk level
- non-sensitive metadata

The system returns:

- risk findings
- formal error taxonomy categories
- rule hits
- risk score
- trust level
- accept/escalate/reject recommendation
- Markdown and JSON trust reports
- batch metrics
- case-family metrics
- optional multi-role workflow trace

### 3.1 Case Schema

Each case contains a synthetic case ID, domain, user question, LLM output under review, expected risk level, evidence items, simplified policy rules, and public-safe metadata. Evidence items are represented with stable IDs so reports can cite the exact facts that support or contradict an output.

### 3.2 Review Pipeline

The public reviewer applies deterministic checks for:

| Component | Function |
|---|---|
| Evidence checker | Flags unsupported risk terms that do not appear in the evidence packet. |
| Policy-signal checker | Checks whether required policy terms appear in the output. |
| Certainty checker | Flags overconfident decision language such as "definitely", "approved", or "no risk". |
| Escalation checker | Flags decision-like outputs that do not mention escalation or human review. |
| Risk-label checker | Checks whether the output explicitly aligns with the expected risk level. |

The public implementation is deterministic by design. This makes the demo easy to inspect, test, and reproduce while leaving patent-facing or private orchestration details outside the repository.

### 3.3 Outputs

Each review produces:

| Artifact | Purpose |
|---|---|
| Markdown trust report | Human-readable case review. |
| JSON review result | Machine-readable findings and routing. |
| Batch summary | Case-level metrics for all synthetic cases. |
| Evaluation metrics JSON | Aggregate review-routing metrics. |
| Baseline comparison | Naive confident-output acceptance versus trust workflow. |
| Multi-role workflow report | Public-safe evidence, policy, risk, escalation, and final reviewer notes. |

## 4. Demo Interface

The current public demo includes:

- CLI review command for one case
- batch-review command for a case directory
- summarize command for aggregate metrics
- baseline-compare command for naive baseline analysis
- workflow-review command for role-specific review notes
- static browser review console hosted on GitHub Pages

The demonstration flow is designed for a three-minute walkthrough:

1. Select a representative synthetic case from the browser console.
2. Inspect the LLM output and evidence packet.
3. Review risk score, trust level, findings, and routing recommendation.
4. Open the generated Markdown trust report.
5. Show the baseline comparison where confident language creates false accepts.
6. Open the multi-role workflow trace for an agent tool-failure case.

## 5. Case Library

The public evaluation set currently contains 52 synthetic cases. Domains include:

| Domain family | Example risks |
|---|---|
| AML / KYC / sanctions | Incomplete beneficial ownership, transaction mismatch, partial watchlist match, false-positive screening. |
| Due diligence / legal / vendor review | Unsupported adverse claims, PEP links, litigation signals, missing source evidence. |
| Trust and safety / customer support | Account takeover, harassment reports, refund-threshold policy gaps. |
| Agent output review | Ignored browser warnings, unsupported test claims, tool-result mismatch. |
| HR / health / education / financial services | Sensitive-attribute misuse, unsafe medical certainty, student support false pass, payment fraud signals. |
| Low-risk controls | Evidence-consistent cases that should not be over-escalated. |

All cases are synthetic and public-safe.

## 6. Evaluation

The current deterministic public prototype is evaluated as a review-routing system rather than as a production model.

| Metric | Value |
|---|---:|
| Total synthetic cases | 52 |
| Manual review cases | 32 |
| Manual review rate | 61.5% |
| Low-trust cases | 25 |
| Low-trust rate | 48.1% |
| Average risk score | 45.77 |

The most frequent findings are:

| Finding | Count |
|---|---:|
| `risk_label_mismatch` | 33 |
| `missing_policy_signal` | 30 |
| `missing_escalation` | 30 |
| `unsafe_certainty` | 23 |
| `unsupported_claim` | 9 |

The raw findings are also mapped into a compact error taxonomy for reviewer-facing analysis:

| Taxonomy category | Count |
|---|---:|
| `risk_routing` | 33 |
| `policy_alignment` | 30 |
| `human_escalation` | 30 |
| `calibration` | 23 |
| `evidence_grounding` | 9 |

This taxonomy separates low-level detector names from higher-level reviewer questions: whether the output is routed to the right risk level, whether it follows required policy signals, whether it preserves human escalation, whether it is calibrated in certainty, and whether claims are grounded in evidence.

### 6.1 Case-Family Metrics

The synthetic set is grouped into case families so coverage and routing behavior can be inspected by scenario type rather than only at the aggregate level.

| Case family | Cases | Manual review rate | Low-trust rate | Average risk score |
|---|---:|---:|---:|---:|
| `aml_kyc_sanctions` | 13 | 69.23% | 53.85% | 51.54 |
| `agent_reliability` | 7 | 71.43% | 71.43% | 53.57 |
| `trust_safety_support` | 7 | 57.14% | 28.57% | 40.71 |
| `data_quality_hr_education` | 6 | 83.33% | 50.00% | 53.33 |
| `due_diligence_legal` | 5 | 60.00% | 60.00% | 55.00 |
| `financial_risk` | 5 | 60.00% | 60.00% | 50.00 |
| `health_safety` | 5 | 60.00% | 40.00% | 41.00 |

This table is useful for demo review because it shows both project breadth and remaining limitations. For example, the `agent_reliability` family is deliberately small but high-risk, while `aml_kyc_sanctions` is the most developed family and anchors the portfolio story in risk review work.

### 6.2 Human Spot-Check Protocol

The repository includes a public-safe human spot-check protocol for auditing synthetic-case reports before public sharing or submission. The protocol samples at least 15 cases from the 52-case library, including high-risk synthetic cases, low-risk controls, agent/tool-use cases, and cross-domain cases.

For each sampled case, a reviewer records route agreement, finding quality, missed findings, over-triggered findings, evidence clarity, and notes for the next version. The planned summary metrics are human route agreement, disagreement count, unclear case count, over-trigger count, and missed-finding count.

This protocol is intended to make the synthetic evaluation set easier to audit. It is not a claim of production validation or real-world reviewer agreement.

An initial 15-case author spot-check draft has been recorded for release readiness. The spot-check found one boundary issue: an output denying clinician review should be treated as a missing-escalation pattern even when it contains the phrase "clinician review." The reviewer rule was updated, a regression test was added, and reports were regenerated. This illustrates the intended quality loop: sampled review, error-pattern discovery, rule update, regression test, and metric refresh.

## 7. Naive Baseline

The naive baseline treats confident acceptance language such as "approve", "accepted", "no risk", or "routine monitoring" as usable. This approximates a weak review process that mistakes fluent confidence for verification.

| Metric | Value |
|---|---:|
| Naive accept cases | 38 |
| Naive false accept cases | 25 |
| Naive false accept rate | 48% |
| Trust workflow accept cases | 20 |
| Trust workflow manual review cases | 32 |

This comparison illustrates why a trust-report workflow is useful: it surfaces evidence gaps and escalation failures that can be hidden behind confident LLM wording.

## 8. Multi-Role Workflow Trace

For agent-style review, Agent Trust Lab can decompose a case into public-safe role notes:

```text
case package
  -> evidence reviewer
  -> policy reviewer
  -> risk reviewer
  -> escalation reviewer
  -> final reviewer
  -> human-in-the-loop routing
```

This role trace is designed for auditability and interviewability, not autonomous approval.

## 9. Demo Plan

The live demo can be run entirely offline after cloning the repository:

```powershell
python -m pytest -q
python -m http.server 8765
```

The presenter then opens `http://localhost:8765/web/` and walks through:

| Step | Screen / Artifact | Message |
|---|---|---|
| 1 | Browser review console | The project is a review console, not a chatbot. |
| 2 | Case queue | Risk-sensitive outputs are reviewed as cases with evidence and routing. |
| 3 | Selected case details | Findings expose missing evidence, policy mismatch, unsafe certainty, and escalation gaps. |
| 4 | `examples/baseline_comparison.md` | A naive baseline can falsely accept confident outputs. |
| 5 | `examples/workflow_report_agent_tool_failure.md` | Agent failures can be decomposed into evidence, policy, risk, escalation, and final-review roles. |
| 6 | `docs/GOVERNANCE.md` | The system supports human review and does not automate high-risk approval. |

## 10. Ethical and Safety Boundary

The public demo does not include:

- real customer data
- real company policies
- private labels
- secrets or credentials
- patent claim text
- automated approval for high-risk decisions

The system recommends human routing. It does not replace accountable human review.

## 11. Limitations

- The current case library is synthetic.
- The public reviewer is deterministic and intentionally inspectable.
- The baseline is deliberately weak and should not be interpreted as a production benchmark.
- The system has not yet been evaluated with real human reviewer agreement; the current spot-check protocol is a public-safe synthetic review audit.
- Patent-facing implementation details are intentionally excluded from public artifacts.

## 12. Reproducibility

```powershell
python -m pytest -q
python -m agent_trust_lab.cli batch-review --cases-dir examples\cases --out-dir examples\reports --summary examples\batch_summary.json
python -m agent_trust_lab.cli summarize --summary examples\batch_summary.json --out examples\evaluation_metrics.json
python -m agent_trust_lab.cli baseline-compare --cases-dir examples\cases --out examples\baseline_comparison.json --markdown-out examples\baseline_comparison.md
python -m agent_trust_lab.cli workflow-review --case examples\cases\agent_tool_failure.json --out examples\workflow_report_agent_tool_failure.md --json-out examples\workflow_report_agent_tool_failure.json
```

## 13. Planned Evaluation Extensions

Before submission, the next evaluation additions are:

| Extension | Why it matters |
|---|---|
| Difficulty labels | Separates low-risk controls from high-risk false-pass cases. |
| Larger case families | Expands thin families such as financial risk, health-safety, and low-risk controls. |
| Independent spot-check execution | Applies the documented protocol with an additional reviewer and records disagreements. |
| Single-output baseline | Compares raw LLM answers with trust-report review artifacts. |
| Reviewer override field | Records when a human reviewer disagrees with the system route. |
| Demo screenshots | Makes the system demonstration concrete for reviewers. |

## 14. Next Draft Work

- Add related work.
- Add screenshots from the browser console.
- Add a short demo script.
- Add an independent reviewer pass for the human spot-check protocol.
- Add table comparing single-output review, trust report, and multi-role workflow trace.
