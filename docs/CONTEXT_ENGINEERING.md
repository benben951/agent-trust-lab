# Context Engineering For Agent Trust Lab

This document explains how Agent Trust Lab is maintained as a Codex-first AI evaluation project.

The point is not only to use AI coding tools. The point is to give AI agents the right context, boundaries, verification gates, and artifacts so they can help ship reliable work instead of producing plausible but unverified changes.

## 1. Operating Question

Agent Trust Lab asks:

> Can a human reviewer trust this LLM or agent output enough to use it, escalate it, or reject it?

The development workflow asks a parallel question:

> Can an AI coding assistant understand the project context, make a bounded change, verify it, and leave reviewable evidence?

## 2. Context Layers

| Layer | What It Contains | Why It Matters |
|---|---|---|
| Product context | README, review packet, case walkthrough, portfolio showcase | Keeps the project story consistent for recruiters and interviewers. |
| Domain context | AML/KYC, due diligence, trust and safety, AI data quality, agent-output review | Keeps examples tied to risk-sensitive workflows instead of generic chatbot demos. |
| Data context | Synthetic case schema, evidence items, policy rules, generated reports | Makes examples inspectable without exposing private data. |
| Evaluation context | Findings, trust levels, recommendations, batch metrics, workflow traces | Turns subjective AI output review into auditable artifacts. |
| Verification context | Tests, CLI reproduction commands, browser demo checks, generated Markdown/JSON | Prevents unsupported completion claims. |
| Governance context | Human-in-the-loop boundary, public-safe data boundary, no high-risk auto-approval | Keeps the portfolio aligned with Trust & Safety and risk-tech expectations. |

## 3. Repository Memory

The project keeps important decisions in public files rather than hidden chat history:

- `docs/REVIEW_PACKET.md`: recruiter-facing summary and reproduction path.
- `docs/CASE_WALKTHROUGH.md`: step-by-step case flow for a synthetic agent tool failure.
- `docs/EVALUATION_METRICS.md`: metric definitions and current demo values.
- `docs/GOVERNANCE.md`: data, decision, logging, and public demo boundaries.
- `examples/reports/*.md`: generated case-level trust reports.
- `examples/workflow_report_agent_tool_failure.md`: role-level workflow trace.

This lets a coding agent re-enter the project through files, not fragile memory.

## 4. Change Workflow

```text
goal
  -> inspect current repo state
  -> identify bounded change
  -> edit docs/code/demo
  -> regenerate reports when needed
  -> run tests and CLI checks
  -> inspect browser demo when UI changes
  -> commit with a narrow message
  -> update portfolio links when the public story changes
```

The workflow is intentionally boring. Boring is good for risk-sensitive systems.

## 5. Verification Gates

Before claiming a change is complete, at least one relevant gate must pass:

| Change Type | Verification Gate |
|---|---|
| Python review logic | `python -m pytest -q` |
| Single-case report | `python -m agent_trust_lab.cli review ...` |
| Multi-role workflow trace | `python -m agent_trust_lab.cli workflow-review ...` |
| Batch metrics | `batch-review` plus `summarize` |
| Documentation update | Keyword/link checks against updated files |
| Browser demo update | Local `http.server` plus Playwright snapshot or screenshot |

The project avoids "it should work" claims. Evidence comes first.

## 6. Agent-Friendly Boundaries

The repository is designed to be safe for AI-assisted development:

- Use synthetic data only.
- Keep patent-sensitive implementation details out of public docs.
- Do not include employer data, real customer data, private policies, credentials, or private labels.
- Prefer deterministic checks for public demos.
- Route uncertain or high-risk outputs to human review.
- Treat generated reports as review artifacts, not final business decisions.

## 7. How Codebase Graph Tools Fit

Codebase graph tools such as CodeGraph or Understand-Anything are useful as context accelerators.

They can help an AI coding assistant answer:

- Which files define the CLI entry points?
- Where are review findings created?
- Which docs should change when a new public artifact is added?
- What tests cover a workflow command?
- What files are affected by changing the case schema?

For this project, these tools are workflow accelerators rather than the core product. The core product remains trust reporting, review routing, and human-in-the-loop governance.

## 8. Interview Story

Short version:

> I use AI coding tools as part of a controlled engineering workflow. I keep project context in docs and generated artifacts, make bounded changes, run tests and reproduction commands, inspect the browser demo for UI changes, and avoid claiming completion without verification evidence.

Longer version:

> Agent Trust Lab is both a product and an example of how I work with AI agents. The product reviews LLM outputs in risk-sensitive cases. The workflow around it also follows risk-sensitive principles: context is explicit, changes are bounded, outputs are auditable, and tests or screenshots are required before claiming success.

Resume-safe phrasing:

> Built and maintained a Codex-first AI evaluation project using explicit context files, synthetic case artifacts, CLI reproduction commands, generated trust reports, browser-demo checks, and test gates to keep AI-assisted development auditable.

## 9. Next Improvements

- Add a lightweight codegraph index note after evaluating CodeGraph on this repository.
- Record before/after examples where context indexing reduces repo exploration work.
- Add a public-safe agent run log format for future workflow experiments.
- Link Agent Trust Lab context engineering with Agent Workflow Bench verifier artifacts.

