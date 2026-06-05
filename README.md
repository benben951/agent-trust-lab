# Agent Trust Lab

[![CI](https://github.com/benben951/agent-trust-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/benben951/agent-trust-lab/actions/workflows/ci.yml)

Risk-sensitive LLM output review and trust-report generation system.

## Portfolio Snapshot

Agent Trust Lab is a public-safe portfolio project for evaluating LLM and agent outputs in risk-sensitive workflows such as AML review, compliance QA, due diligence, trust and safety, and AI data-quality calibration.

The project focuses on one practical question:

> Can a human reviewer trust this LLM or agent output enough to use it, escalate it, or reject it?

![Agent Trust Lab browser demo](assets/agent-trust-lab-v03.png)

## What It Demonstrates

- Multi-role review thinking: extractor, policy checker, evidence verifier, risk scorer, and final reviewer.
- Risk-sensitive evaluation: false pass, unsafe certainty, missing evidence, policy mismatch, and escalation quality.
- Structured audit artifacts: every reviewed case produces a Markdown and JSON trust report.
- Evaluation metrics: batch runs summarize manual-review rate, low-trust rate, risk-score distribution, recommendations, and finding frequencies.
- Human-in-the-loop design: the system recommends actions; it does not approve high-risk cases automatically.
- Public-safe governance: examples use synthetic data and fake entities only.

## Current Scope

This public repository intentionally exposes only the demo-safe layer:

- a synthetic case schema
- a deterministic trust-report generator
- sample LLM outputs and review reports
- a 10-case synthetic risk review library
- batch report generation
- a static browser review console
- public architecture and governance notes
- a technical-report draft

The patent-facing claim details are kept outside this repository until a filing decision is made.

## Quick Start

```powershell
python -m agent_trust_lab.cli review `
  --case examples/synthetic_aml_case.json `
  --out examples/generated_trust_report.md
```

Run tests:

```powershell
python -m pytest -q
```

Generate reports for the full synthetic case library:

```powershell
python -m agent_trust_lab.cli batch-review `
  --cases-dir examples\cases `
  --out-dir examples\reports `
  --summary examples\batch_summary.json
```

Summarize evaluation metrics:

```powershell
python -m agent_trust_lab.cli summarize `
  --summary examples\batch_summary.json `
  --out examples\evaluation_metrics.json
```

Open the browser demo:

```powershell
python -m http.server 8765
```

Then visit `http://localhost:8765/web/`.

## System Flow

```text
synthetic case + LLM output
        |
        v
evidence and policy checks
        |
        v
risk-sensitive scoring
        |
        v
human-review recommendation
        |
        v
Markdown / JSON trust report
        |
        v
batch metrics summary
```

## v0.2 Evaluation Snapshot

The 10-case synthetic evaluation set currently produces:

| Metric | Value |
|---|---:|
| Total cases | 10 |
| Manual review cases | 8 |
| Manual review rate | 80% |
| Low-trust cases | 4 |
| Low-trust rate | 40% |
| Average risk score | 53.0 |

The most frequent findings are `risk_label_mismatch`, `missing_policy_signal`, and `missing_escalation`. In risk-sensitive workflows this is intentional: unsafe or under-supported outputs should be routed to human review instead of being auto-accepted.

## Public Demo Case

The included synthetic case simulates an AML-style review where an LLM response must be checked for:

- unsupported claims
- missing evidence
- overconfident conclusions
- risk-label mismatch
- need for human escalation

See:

- [examples/synthetic_aml_case.json](examples/synthetic_aml_case.json)
- [examples/trust_report_sample.md](examples/trust_report_sample.md)
- [docs/PORTFOLIO_SHOWCASE.md](docs/PORTFOLIO_SHOWCASE.md)
- [docs/EVALUATION_METRICS.md](docs/EVALUATION_METRICS.md)
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- [examples/batch_summary.json](examples/batch_summary.json)
- [examples/evaluation_metrics.json](examples/evaluation_metrics.json)
- [web/index.html](web/index.html)

## Related Portfolio Projects

Agent Trust Lab is designed as the umbrella product layer for:

- `llm-proxy-auditor`: proxy and infrastructure trust checks
- `agent-workflow-bench`: planner-executor-reviewer workflow evaluation
- `gemma-aml-assistant`: AML and due-diligence RAG workflow

## Resume Angle

Built Agent Trust Lab, a risk-sensitive LLM output review system with a static browser review console, a 10-case synthetic AML/KYC/due-diligence/trust-and-safety library, batch trust-report generation, JSON summaries, escalation recommendations, and human-in-the-loop governance for AI evaluation workflows.

## Safety Boundary

This repository does not include:

- real customer data
- real company policies
- private review labels
- secrets or credentials
- patent claim text
- production approval automation for high-risk decisions
