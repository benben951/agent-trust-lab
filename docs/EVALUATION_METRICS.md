# Evaluation Metrics

Agent Trust Lab is designed as a public-safe evaluation prototype for risk-sensitive LLM and agent outputs. The goal is not to maximize automatic acceptance. The goal is to make unsafe confidence, missing evidence, policy mismatch, and weak escalation visible to a human reviewer.

## Evaluation Set

The current public demo uses a 10-case synthetic evaluation set:

| Domain | Case count | Purpose |
|---|---:|---|
| AML onboarding | 1 | Detect unsafe low-risk approval in incomplete onboarding evidence. |
| AML transaction monitoring | 1 | Detect missing escalation in transaction-behavior mismatch. |
| KYC review | 1 | Detect conflict handling problems in identity/address evidence. |
| Vendor due diligence | 1 | Check acceptable review with notes. |
| Trust and safety | 1 | Detect unsupported fraud claims and unsafe blocking. |
| Customer support compliance | 1 | Detect unsupported compensation or policy promises. |
| Agent output review | 1 | Detect tool failure ignored by final agent output. |
| AI data quality | 1 | Detect label conflict and calibration risk. |
| Sanctions screening | 1 | Detect false-positive risk and overconfident match handling. |
| Low-risk control | 1 | Confirm the system can route safe cases without over-escalation. |

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

## v0.2 Demo Metrics

Generated from `examples/batch_summary.json`:

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

Trust-level distribution:

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

## How To Interpret The Metrics

For risk-sensitive workflows, a high manual-review rate is not necessarily a weakness. It can be a sign that the system is correctly refusing to auto-accept ambiguous, unsupported, or high-impact outputs.

The most important failure mode is the unsafe false pass: an LLM output that sounds confident, appears helpful, and recommends acceptance despite missing evidence or policy support. Agent Trust Lab treats escalation as a valid and often preferred system action.

## Current Limitations

- The evaluation set is synthetic and intentionally small.
- The public implementation uses deterministic checks for inspectability.
- The metrics are demo metrics, not production model-performance claims.
- The public repository does not include patent-facing claim details or private implementation ideas.

## Planned Extensions

- Add reviewer override tracking.
- Add disagreement metrics for multi-agent review workflows.
- Add drift checks across model versions or prompt variants.
- Add case difficulty labels and coverage buckets.
- Add latency and review-time-saved estimates after a real workflow simulation is available.

