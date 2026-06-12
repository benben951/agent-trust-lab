# Risk Review Copilot

This note packages the risk-control side of Agent Trust Lab for AML/KYC, sanctions, due diligence, payment-fraud, and compliance-QA interviews.

The project is an assistant-stage risk copilot. It does not approve high-risk cases. It reviews LLM or agent outputs, checks whether the conclusion is supported by evidence and policy signals, and routes questionable cases to human review.

## Business Problem

Risk-review teams increasingly receive AI-generated summaries, labels, or recommendations. A fluent answer can still create risk when it:

- approves a case while evidence is incomplete
- misses an AML/KYC or sanctions signal
- makes unsupported allegations
- sounds more certain than the evidence allows
- skips manual review for medium/high-risk cases

Agent Trust Lab turns those outputs into structured review artifacts so a human reviewer can decide faster and with a clearer audit trail.

## Data Schema

Each public-safe case uses synthetic data only.

| Field | Meaning |
|---|---|
| `case_id` | Stable review identifier |
| `domain` | Scenario type, such as `aml_monitoring`, `kyc_review`, or `sanctions_screening` |
| `user_question` | The review question or task |
| `expected_risk_level` | Public-safe expected route label |
| `llm_output` | Output under review |
| `evidence[]` | Evidence snippets with source and text |
| `policy_rules[]` | Required policy/rule signals represented as terms |
| `metadata` | Synthetic policy boundary and scenario notes |

## Decision Chain

```text
case package
  -> evidence extraction
  -> policy-signal check
  -> finding detection
  -> risk score
  -> trust level
  -> recommendation
  -> Markdown/JSON audit artifact
```

Recommendations:

| Recommendation | Meaning |
|---|---|
| `accept_with_notes` | Low-risk or sufficiently supported output |
| `escalate_for_manual_review` | Medium uncertainty or missing signals |
| `reject_or_escalate` | Unsafe, unsupported, or high-risk output |

## Metrics That Matter

The project reports risk-review metrics instead of only model accuracy.

| Metric | Why it matters |
|---|---|
| Manual review rate | How often the system routes cases to humans |
| Low-trust rate | How often outputs are unsafe or weakly supported |
| Finding distribution | Which failure types recur |
| Case-family metrics | Whether AML/KYC behaves differently from other scenarios |
| Naive false-accept rate | How often confident outputs would be wrongly accepted |
| Low-risk control rate | Whether safe cases avoid over-escalation |

## Current AML/KYC Evidence

The synthetic `aml_kyc_sanctions` family contains 13 public-safe cases across AML monitoring, onboarding, KYC review, KYC refresh, KYC screening, and sanctions screening.

Current family metrics:

| Metric | Value |
|---|---:|
| Cases | 13 |
| Manual review rate | 69.23% |
| Low-trust rate | 53.85% |
| Average risk score | 51.54 |

Typical failures:

- missing policy signals
- missing human escalation
- risk-label mismatch
- unsupported risk claims
- unsafe certainty in ambiguous cases

## Example Risk Patterns

| Pattern | Example case | Review route |
|---|---|---|
| Incomplete beneficial-owner evidence | `SYN-AML-001` | Reject or escalate |
| Transaction behavior mismatch | `SYN-AML-002` | Escalate |
| Near-threshold structuring signal | `SYN-AML-004` | Escalate with evidence |
| Sanctions false-positive handling | `SYN-SAN-001` | Reject or escalate |
| KYC address or identity conflict | `SYN-KYC-001` | Escalate |

## Human-In-The-Loop Boundary

The system is designed for reviewer support, not automated financial-crime decisions.

Hard boundaries:

- no real customer data in the public repo
- no internal policy text
- no hidden production labels
- no automatic high-risk approval
- no claim that synthetic metrics equal production performance
- no secrets, browser sessions, or private employer data

## Reproduce The Risk Review Slice

```powershell
python -m agent_trust_lab.cli batch-review `
  --cases-dir examples\cases `
  --out-dir examples\reports `
  --summary examples\batch_summary.json

python -m agent_trust_lab.cli summarize `
  --summary examples\batch_summary.json `
  --out examples\evaluation_metrics.json
```

Then inspect:

- `examples/evaluation_metrics.json`
- `examples/reports/SYN-AML-001.md`
- `examples/reports/SYN-SAN-001.md`
- `docs/REVIEW_PACKET.md`

## Resume Framing

Built a public-safe Risk Review Copilot prototype for AML/KYC, sanctions, due diligence, payment-fraud, and compliance-QA scenarios. Designed synthetic case schemas, evidence and policy-signal checks, finding taxonomy, risk scoring, human-review routing, Markdown/JSON audit reports, case-family metrics, and naive false-accept baseline comparison. The system supports reviewer judgment instead of automating high-risk approvals.
