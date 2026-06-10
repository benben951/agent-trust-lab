# Evaluation Metrics

Agent Trust Lab is designed as a public-safe evaluation prototype for risk-sensitive LLM and agent outputs. The goal is not to maximize automatic acceptance. The goal is to make unsafe confidence, missing evidence, policy mismatch, and weak escalation visible to a human reviewer.

## Evaluation Set

The current public demo uses a 40-case synthetic evaluation set:

| Domain | Case count | Purpose |
|---|---:|---|
| AML / KYC / sanctions | 13 | Detect unsafe low-risk approval, missing UBO review, structuring signals, and screening ambiguity. |
| Due diligence / legal / vendor review | 5 | Detect unsupported adverse claims, PEP links, litigation signals, and evidence gaps. |
| Trust and safety / customer support | 6 | Detect unsafe user-impacting decisions, policy-threshold gaps, and disputed context. |
| Agent output and coding-agent review | 4 | Detect ignored tool failures, unsupported test claims, and tool-result mismatch. |
| Data quality / HR / health / education / financial services | 11 | Detect sensitive-attribute misuse, unsafe certainty, label conflict, and financial false-pass risk. |
| Low-risk controls | 1 | Confirm the system can route safe cases without over-escalation. |

All cases are synthetic and public-safe. They do not contain real customer data, internal company policies, private labels, or credentials.

## Core Metrics

| Metric | Definition | Why it matters |
|---|---|---|
| Manual review rate | Share of cases routed to human review. | Measures whether the system escalates uncertain or high-risk outputs instead of blindly accepting them. |
| Low-trust rate | Share of cases assigned low trust. | Captures outputs that are unsafe to use without rejection or escalation. |
| Average risk score | Mean risk score across the synthetic case set. | Provides a quick overview of evaluation-set difficulty and review severity. |
| Trust-level distribution | Count of low, medium, and high trust cases. | Shows whether the system can separate risky, ambiguous, and acceptable outputs. |
| Recommendation distribution | Count of `reject_or_escalate`, `escalate_for_manual_review`, and `accept_with_notes`. | Converts model-output review into an operational routing decision. |
| Finding distribution | Frequency of failure types such as `unsafe_certainty` or `unsupported_claim`. | Helps identify recurring weaknesses in LLM or agent outputs. |
| Taxonomy category distribution | Frequency of higher-level review categories such as `risk_routing`, `human_escalation`, or `evidence_grounding`. | Makes error analysis easier to compare across case families. |
| Case-family metrics | Manual-review rate, low-trust rate, average risk score, and finding distribution by case family. | Shows where the evaluation set is strong, thin, or over-escalating. |
| Naive false accept rate | Share of cases where confident accept/approve wording would be accepted by a weak baseline even though the trust workflow requires review. | Highlights the risk of treating fluent LLM outputs as verified decisions. |

## v0.3 Demo Metrics

Generated from `examples/batch_summary.json`:

| Metric | Value |
|---|---:|
| Total synthetic cases | 40 |
| Manual review cases | 26 |
| Manual review rate | 65% |
| Low-trust cases | 19 |
| Low-trust rate | 47.5% |
| Average risk score | 47.62 |
| Max risk score | 100 |
| Min risk score | 0 |

Trust-level distribution:

| Trust level | Count |
|---|---:|
| Low | 19 |
| Medium | 7 |
| High | 14 |

Recommendation distribution:

| Recommendation | Count |
|---|---:|
| `reject_or_escalate` | 19 |
| `escalate_for_manual_review` | 7 |
| `accept_with_notes` | 14 |

Finding distribution:

| Finding | Count |
|---|---:|
| `risk_label_mismatch` | 27 |
| `missing_policy_signal` | 24 |
| `missing_escalation` | 24 |
| `unsafe_certainty` | 17 |
| `unsupported_claim` | 8 |

## Formal Error Taxonomy

The raw findings are mapped to higher-level review categories. See
`docs/ERROR_TAXONOMY.md` for reviewer questions and human-check guidance.

| Finding | Category | Severity |
|---|---|---|
| `unsupported_claim` | `evidence_grounding` | High |
| `missing_policy_signal` | `policy_alignment` | Medium |
| `unsafe_certainty` | `calibration` | Medium |
| `missing_escalation` | `human_escalation` | High |
| `risk_label_mismatch` | `risk_routing` | Medium |

Taxonomy category distribution:

| Category | Count |
|---|---:|
| `risk_routing` | 27 |
| `policy_alignment` | 24 |
| `human_escalation` | 24 |
| `calibration` | 17 |
| `evidence_grounding` | 8 |

## Case-Family Metrics

Generated from `examples/evaluation_metrics.json`:

| Case family | Cases | Manual review rate | Low-trust rate | Average risk score |
|---|---:|---:|---:|---:|
| `aml_kyc_sanctions` | 13 | 69.23% | 53.85% | 51.54 |
| `trust_safety_support` | 7 | 57.14% | 28.57% | 40.71 |
| `data_quality_hr_education` | 6 | 83.33% | 50.00% | 53.33 |
| `due_diligence_legal` | 5 | 60.00% | 60.00% | 55.00 |
| `agent_reliability` | 4 | 75.00% | 75.00% | 56.25 |
| `financial_risk` | 2 | 50.00% | 50.00% | 37.50 |
| `health_safety` | 2 | 50.00% | 0.00% | 27.50 |
| `low_risk_control` | 1 | 0.00% | 0.00% | 0.00 |

## Naive Baseline Comparison

Generated from `examples/baseline_comparison.json`:

| Metric | Value |
|---|---:|
| Total synthetic cases | 40 |
| Naive accept cases | 26 |
| Naive accept rate | 65% |
| Naive false accept cases | 19 |
| Naive false accept rate | 48% |
| Trust workflow accept cases | 14 |
| Trust workflow accept rate | 35% |
| Trust workflow manual review cases | 26 |
| Trust workflow manual review rate | 65% |

## How To Reproduce

Generate the batch trust reports:

```powershell
python -m agent_trust_lab.cli batch-review `
  --cases-dir examples\cases `
  --out-dir examples\reports `
  --summary examples\batch_summary.json
```

Generate the aggregate metric summary:

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

## How To Interpret The Metrics

For risk-sensitive workflows, a high manual-review rate is not necessarily a weakness. It can be a sign that the system is correctly refusing to auto-accept ambiguous, unsupported, or high-impact outputs.

The most important failure mode is the unsafe false pass: an LLM output that sounds confident, appears helpful, and recommends acceptance despite missing evidence or policy support. Agent Trust Lab treats escalation as a valid and often preferred system action.

## Current Limitations

- The evaluation set is synthetic and intentionally small compared with a production review queue.
- The public implementation uses deterministic checks for inspectability.
- The metrics are demo metrics, not production model-performance claims.
- The public repository does not include patent-facing claim details or private implementation ideas.

## Planned Extensions

- Add reviewer override tracking.
- Add disagreement metrics for multi-agent review workflows.
- Add drift checks across model versions or prompt variants.
- Add case difficulty labels and coverage buckets.
- Add latency and review-time-saved estimates after a real workflow simulation is available.
