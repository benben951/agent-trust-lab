# Outreach Kit

Use this document when sharing Agent Trust Lab on GitHub, LinkedIn, portfolio
pages, project applications, or technical communities.

The rule: share a useful artifact, not a star request.

## One-Line Pitch

Agent Trust Lab turns risk-sensitive LLM and agent outputs into structured trust
reports with evidence checks, risk findings, baseline comparison, and
human-in-the-loop routing.

## Short Pitch

Most LLM demos optimize for fluent answers. Agent Trust Lab asks a different
question: should a risky output be accepted, revised, escalated, or rejected?

The project includes a browser demo, Python CLI, synthetic risk cases, Markdown
and JSON trust reports, reusable workflow recipes, baseline comparison, metrics
summaries, and public-safe multi-role workflow traces.

## Recruiter Pitch

I built Agent Trust Lab to connect my risk-review and AML background with LLM
evaluation. The system does not pretend to automate compliance decisions. It
generates reviewable trust reports, flags unsupported or overconfident outputs,
and routes risky cases to human review. The repo includes CI, a live demo,
synthetic cases, reusable review workflow recipes, baseline comparison, report
examples, and a system-demo draft.

## GitHub Repository Description

Risk-sensitive LLM output review and trust-report generation system.

## Suggested GitHub Topics

- `llm-evaluation`
- `agent-evaluation`
- `ai-safety`
- `trust-and-safety`
- `human-in-the-loop`
- `llmops`
- `aml`
- `compliance`
- `risk-management`
- `governance`

## LinkedIn Post Draft

I have been working on Agent Trust Lab, a small public-safe system for reviewing
risk-sensitive LLM and agent outputs.

Instead of asking only "is the answer fluent?", the project asks:

- Is the output supported by the provided evidence?
- Does it overstate certainty?
- Does it ignore policy or escalation signals?
- Should the case be accepted, revised, escalated, or rejected?

The repo includes a live demo, Python CLI, synthetic risk cases, Markdown/JSON
trust reports, reusable workflow recipes, baseline comparison, metrics
summaries, and a working system-demo paper draft.

This is part of my broader interest in LLM evaluation, agent workflow safety,
human-in-the-loop review, and risk-sensitive AI applications.

Repo:
https://github.com/benben951/agent-trust-lab

Live demo:
https://benben951.github.io/agent-trust-lab/

Feedback is welcome, especially from people working on LLM evaluation, Trust &
Safety, compliance QA, or agent reliability.

For a longer shareable post, see
[`POST_REUSABLE_TRUST_WORKFLOWS.md`](POST_REUSABLE_TRUST_WORKFLOWS.md).

## GitHub Discussion / Issue Prompt

Title:

```text
Feedback wanted: risk-sensitive LLM output review taxonomy
```

Body:

```text
I am building Agent Trust Lab, a public-safe prototype for converting risky LLM
and agent outputs into structured trust reports.

The current findings include unsupported claims, unsafe certainty, missing policy
signals, missing escalation, and risk-label mismatch.

I also added reusable workflow recipes for AML false-pass review, agent
tool-failure review, financial advice review, health-safety escalation review,
and low-risk control review.

I would appreciate feedback on:

1. Are these error categories useful for LLM evaluation or review QA?
2. Which risk-sensitive failure modes are missing?
3. What metrics would make this more credible?
4. Are the reusable workflow recipes concrete enough for another reviewer to run?
5. What would you need before trusting a system like this in a real workflow?

Repo: https://github.com/benben951/agent-trust-lab
Demo: https://benben951.github.io/agent-trust-lab/
```

## Communities To Consider

Use judgment and follow each community's rules.

- LinkedIn post from your own profile
- GitHub README and releases
- Kaggle discussion only if connected to evaluation or competition learning
- Hugging Face community post if a demo space is later created
- LLM evaluation / AI safety / agent engineering communities
- Chinese technical platforms only after the English README and demo are stable

## Anti-Spam Rules

- Do not post the same message everywhere.
- Do not ask for stars directly as the main call to action.
- Ask for feedback on one concrete artifact.
- Show a specific failure mode and how the report catches it.
- Be honest that the project uses synthetic public-safe cases.
- Do not claim production deployment or regulatory approval.

## Strong Call To Action

Best:

> I would appreciate feedback on the error taxonomy and case-family metrics.

Okay:

> If this is useful, stars and issue feedback help me prioritize the next release.

Avoid:

> Please star my repo.

## Outreach Log

Record public feedback actions in [`OUTREACH_LOG.md`](OUTREACH_LOG.md) so
feedback requests, responses, and follow-up work remain auditable.
