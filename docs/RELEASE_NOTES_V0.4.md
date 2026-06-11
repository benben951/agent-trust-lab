# v0.4 Release Notes

Agent Trust Lab v0.4 expands the public-safe evaluation library and upgrades
the project from a small review prototype into a stronger portfolio-facing
artifact with reusable workflows, refreshed demo proof, and a public feedback
entry point.

## Highlights

- Expanded the synthetic evaluation library from 40 to 52 public-safe cases.
- Added coverage for financial risk, health-safety, low-risk controls, and
  agent-reliability scenarios.
- Regenerated 52 Markdown trust reports, the batch summary, evaluation metrics,
  and naive-baseline comparison.
- Updated the browser demo metrics to show 52 cases, 32 manual-review routes,
  25 low-trust cases, and a 45.77 average risk score.
- Added reusable review workflow recipes for AML false-pass review, agent
  tool-failure review, financial advice review, health-safety escalation review,
  and low-risk control review.
- Refreshed the README and GitHub Pages demo proof path with metrics, workflow
  entry points, and updated screenshots.
- Opened a public GitHub feedback issue for the risk-sensitive taxonomy,
  workflow recipes, and evaluation-metric discussion.
- Synchronized README, review packet, demo walkthrough, technical report,
  EMNLP demo draft, taxonomy docs, and portfolio showcase with the new metrics.

## Release Links

- Live demo: https://benben951.github.io/agent-trust-lab/
- Review packet: https://github.com/benben951/agent-trust-lab/blob/main/docs/REVIEW_PACKET.md
- Workflow recipes: https://github.com/benben951/agent-trust-lab/blob/main/docs/WORKFLOW_RECIPES.md
- Feedback issue: https://github.com/benben951/agent-trust-lab/issues/2

## Current Snapshot

| Metric | Value |
|---|---:|
| Synthetic cases | 52 |
| Manual-review cases | 32 |
| Manual-review rate | 61.5% |
| Low-trust cases | 25 |
| Low-trust rate | 48.1% |
| Naive accept cases | 38 |
| Naive false accept cases | 25 |
| Trust workflow accept cases | 20 |

## Why This Release Matters

- It shows measurable AI review artifacts instead of a prompt-only demo.
- It demonstrates human-in-the-loop routing rather than automatic approval.
- It gives reviewers a fast path through metrics, workflow traces, and cases.
- It creates a public entry point for outside feedback and future iteration.

## Boundary

The release uses synthetic data only. It does not include employer data,
customer data, real regulated cases, credentials, private policy text, or
patent-facing claim details.
