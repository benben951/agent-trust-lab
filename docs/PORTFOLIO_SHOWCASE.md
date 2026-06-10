# Portfolio Showcase

Agent Trust Lab demonstrates a 52-case synthetic library, baseline comparison, and batch trust-report generation for risk-sensitive LLM output review.

![Agent Trust Lab browser demo](../assets/agent-trust-lab-v03.png)

## Demo Scope

| Capability | Status |
|---|---|
| Synthetic risk case schema | Implemented |
| Single-case trust report | Implemented |
| Batch trust reports | Implemented |
| Markdown report output | Implemented |
| JSON batch summary | Implemented |
| Evaluation metrics summary | Implemented |
| Naive-baseline comparison | Implemented |
| Multi-role workflow trace | Implemented |
| Reusable review workflow recipes | Implemented |
| Recruiter case walkthrough | Implemented |
| Context-engineering note | Implemented |
| Static browser demo | Implemented |
| Human-review recommendation | Implemented |
| Patent-sensitive implementation details | Kept private |

## Case Library

The full public-safe library contains 52 synthetic cases. The browser console shows a representative queue; the CLI generates reports and metrics for the full library.

| Representative Case ID | Domain | Scenario | Trust Level | Recommendation |
|---|---|---|---|---|
| `SYN-AML-001` | AML onboarding | Unsafe false pass | Low | Reject or escalate |
| `SYN-AML-002` | AML transaction monitoring | Missing escalation | Medium | Escalate for manual review |
| `SYN-KYC-001` | KYC review | Address conflict | Medium | Escalate for manual review |
| `SYN-DD-001` | Vendor due diligence | Acceptable escalation | High | Accept with notes |
| `SYN-TS-001` | Trust and safety | Unsupported fraud claim | Low | Reject or escalate |
| `SYN-CS-001` | Customer support compliance | Unsafe guarantee | Medium | Escalate for manual review |
| `SYN-AGENT-001` | Agent output review | Tool failure ignored | Low | Reject or escalate |
| `SYN-DQ-001` | AI data quality | Label conflict | Medium | Escalate for manual review |
| `SYN-SAN-001` | Sanctions screening | False-positive risk | Low | Reject or escalate |
| `SYN-SAFE-001` | Low-risk control | Safe accept | High | Accept with notes |

## Batch Command

```powershell
python -m agent_trust_lab.cli batch-review `
  --cases-dir examples\cases `
  --out-dir examples\reports `
  --summary examples\batch_summary.json
```

Outputs:

- `examples/reports/*.md`: one trust report per synthetic case
- `examples/batch_summary.json`: machine-readable summary for dashboards or evaluation scripts

## Baseline Comparison

```powershell
python -m agent_trust_lab.cli baseline-compare `
  --cases-dir examples\cases `
  --out examples\baseline_comparison.json `
  --markdown-out examples\baseline_comparison.md
```

Current synthetic comparison:

| Metric | Value |
|---|---:|
| Naive accept cases | 38 |
| Naive false accept cases | 25 |
| Naive false accept rate | 48% |
| Trust workflow accept cases | 20 |
| Trust workflow manual review cases | 32 |

## Multi-Role Workflow Trace

```powershell
python -m agent_trust_lab.cli workflow-review `
  --case examples\cases\agent_tool_failure.json `
  --out examples\workflow_report_agent_tool_failure.md `
  --json-out examples\workflow_report_agent_tool_failure.json
```

The public workflow trace decomposes a synthetic agent-output review into:

- evidence reviewer
- policy reviewer
- risk reviewer
- escalation reviewer
- final reviewer

See [`examples/workflow_report_agent_tool_failure.md`](../examples/workflow_report_agent_tool_failure.md).

## Reusable Workflow Recipes

See [`docs/WORKFLOW_RECIPES.md`](WORKFLOW_RECIPES.md) for public-safe recipes
that turn one-off LLM review prompts into repeatable review workflows.

Current recipes cover:

- AML false-pass review
- agent tool-failure review
- financial advice review
- health-safety escalation review
- low-risk control review

Each recipe defines its trigger, inputs, review roles, failure signals, output
artifact, and human route. This is the portfolio angle: the project is not only
a set of reports, but a reusable operating pattern for reviewing risky LLM and
agent outputs.

## Case Walkthrough

The fastest way to understand the product flow is:

1. Open [`docs/CASE_WALKTHROUGH.md`](CASE_WALKTHROUGH.md).
2. Compare the synthetic evidence package with the final LLM/agent output.
3. Inspect the role-level failures: policy, risk, escalation, and final review.
4. Confirm the system routes the case to human review rather than automatic approval.

This is the recruiter-facing story: input evidence becomes a trust report, workflow trace, and human-in-the-loop recommendation.

## Context Engineering

See [`docs/CONTEXT_ENGINEERING.md`](CONTEXT_ENGINEERING.md) for how the project is maintained with:

- explicit project memory in docs and generated artifacts
- bounded AI-assisted changes
- CLI reproduction commands
- tests and metrics checks
- browser-demo inspection when UI changes
- public-safe data and governance boundaries

## Evaluation Metrics

```powershell
python -m agent_trust_lab.cli summarize `
  --summary examples\batch_summary.json `
  --out examples\evaluation_metrics.json
```

Current v0.4 demo metrics:

| Metric | Value |
|---|---:|
| Total synthetic cases | 52 |
| Manual review cases | 32 |
| Manual review rate | 61.5% |
| Low-trust cases | 25 |
| Low-trust rate | 48.1% |
| Average risk score | 45.77 |

See [EVALUATION_METRICS.md](EVALUATION_METRICS.md) for definitions, interpretation, and limitations.

## Web Demo

Run locally:

```powershell
python -m http.server 8765
```

Then open:

```text
http://localhost:8765/web/
```

The demo presents:

- representative case queue
- manual-review count
- low-trust count
- average risk score
- filterable case queue
- selected case details
- finding badges
- trust-report preview

## Example Findings

The current demo can surface:

- `unsafe_certainty`
- `missing_policy_signal`
- `missing_escalation`
- `unsupported_claim`
- `risk_label_mismatch`

## Why This Helps The Resume

This project shows more than prompt use. It demonstrates a measurable AI review workflow:

- synthetic case design
- evidence and rule checks
- recruiter-readable case walkthrough
- context-engineering workflow
- structured failure taxonomy
- public-safe multi-role workflow trace
- reusable review workflow recipes
- human-review routing
- report generation
- governance boundary

Resume phrasing:

> Built Agent Trust Lab, a risk-sensitive LLM output review prototype with a static browser review console, 52 synthetic AML/KYC/due-diligence/trust-and-safety/agent-review cases, reusable review workflow recipes, batch trust-report generation, naive-baseline comparison, JSON summaries, and human-review recommendations for AI evaluation workflows.

## Public Safety Boundary

The demo uses synthetic data only. It does not include real customer data, company policy, internal labels, credentials, or patent claim text.
