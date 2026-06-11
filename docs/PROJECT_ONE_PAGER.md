# Agent Trust Lab One-Pager

Agent Trust Lab is a public-safe AI review prototype for one practical question:

> Should this LLM or agent output be trusted, revised, escalated, or rejected?

It is designed for risk-sensitive workflows where confident AI outputs can still
be unsafe because they miss evidence, ignore policy signals, or fail to trigger
human escalation.

## What It Does

- Reviews synthetic LLM and agent outputs with evidence, policy, risk, and
  escalation checks.
- Produces Markdown and JSON trust reports for each case.
- Routes cases to `accept_with_notes`, `escalate_for_manual_review`, or
  `reject_or_escalate`.
- Exposes reusable workflow recipes for common review scenarios.
- Provides a browser demo, reproducible CLI, metrics summaries, and baseline
  comparison.

## Why It Matters

Most AI demos optimize for fluent answers.

Agent Trust Lab focuses on reviewability:

- Is the output grounded in the available evidence?
- Does it overstate certainty?
- Does it ignore policy or escalation signals?
- Is the risk label calibrated to the case?
- Should a human reviewer step in?

This makes it more relevant to LLM evaluation, Trust & Safety, agent QA,
compliance review support, and human-in-the-loop AI systems.

## Current Proof

| Proof point | Evidence |
|---|---|
| Public demo | https://benben951.github.io/agent-trust-lab/ |
| Formal release | https://github.com/benben951/agent-trust-lab/releases/tag/v0.4.0 |
| Synthetic evaluation set | 52 public-safe cases |
| Manual-review routes | 32 cases |
| Low-trust cases | 25 cases |
| Average risk score | 45.77 |
| Naive false accepts | 25 |
| Public feedback thread | https://github.com/benben951/agent-trust-lab/issues/2 |

## Core Capabilities

| Capability | Evidence |
|---|---|
| Single-case review | `review` CLI command and report artifacts |
| Batch evaluation | `batch-review` and `summarize` outputs |
| Baseline comparison | `baseline-compare` output |
| Multi-role workflow trace | `workflow-review` output |
| Reusable review recipes | `WORKFLOW_RECIPES.md` |
| Browser review surface | GitHub Pages static demo |
| Public governance boundary | `GOVERNANCE.md` and release notes |

## Representative Scenarios

- AML false-pass review
- agent tool-failure review
- trust-and-safety moderation review
- financial advice review
- health-safety escalation review
- low-risk control review

## Technical Signals

- LLM evaluation artifacts, not just prompt output
- Human-in-the-loop routing
- Taxonomy-based failure analysis
- Case-family metrics and baseline comparison
- Reproducible CLI workflow
- Browser demo + screenshots
- Public release + feedback issue
- Clear synthetic-data governance boundary

## Boundary

This is not a production compliance system.

The repository uses synthetic public-safe data only. It does not include real
customer data, private policy, internal labels, credentials, or patent-facing
claim details.

## Fast Links

- Repo: https://github.com/benben951/agent-trust-lab
- Live demo: https://benben951.github.io/agent-trust-lab/
- Release: https://github.com/benben951/agent-trust-lab/releases/tag/v0.4.0
- Review packet: https://github.com/benben951/agent-trust-lab/blob/main/docs/REVIEW_PACKET.md
- Workflow recipes: https://github.com/benben951/agent-trust-lab/blob/main/docs/WORKFLOW_RECIPES.md
- Feedback issue: https://github.com/benben951/agent-trust-lab/issues/2

## Resume Version

> Built Agent Trust Lab, a public-safe LLM and agent output review prototype
> with a browser demo, 52 synthetic risk-review cases, Markdown/JSON trust
> reports, reusable workflow recipes, baseline comparison, and human-in-the-loop
> escalation recommendations for risk-sensitive AI evaluation workflows.

## Recruiter Version

> Agent Trust Lab is a small but concrete AI evaluation project that turns risky
> model outputs into structured review artifacts. It demonstrates error
> taxonomy, workflow thinking, measurable case coverage, and explicit human
> escalation boundaries rather than prompt-only demo behavior.
