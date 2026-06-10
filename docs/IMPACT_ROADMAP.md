# Impact Roadmap

This roadmap explains how Agent Trust Lab should grow from a portfolio demo into
a project that is easier for recruiters, maintainers, and researchers to trust.

The goal is not to chase vanity stars. The goal is to create public evidence
that the project is useful, reproducible, and positioned in a real problem
space.

## Current Position

Agent Trust Lab already has:

- a public browser demo
- a reproducible Python CLI
- CI
- a 40-case synthetic review library
- Markdown and JSON trust reports
- baseline comparison
- evaluation metrics
- a working system-demonstration draft
- public-safe governance and human-review boundaries

The current gap is external visibility:

- no stars yet
- no external users yet
- no paper acceptance yet
- no external benchmark adoption yet
- no public discussion thread yet

## Impact Funnel

```text
Credible artifact
-> clear review path
-> repeatable result
-> shareable story
-> external feedback
-> citation / stars / PRs / paper
```

Stars are the end of the funnel, not the start of the funnel.

## Priority 1: Make The Project Easier To Trust

Near-term work:

- Add a formal error taxonomy.
- Add case-family metrics.
- Add a baseline comparison table by case family.
- Add a short reproducibility appendix for the technical report.
- Add one "known limitations" table that makes the public-safe boundary obvious.

Why this matters:

- Recruiters can quickly understand the evidence.
- Researchers can see the evaluation frame.
- Maintainers can judge whether the project is serious.
- Interviewers can ask about trade-offs instead of only tooling.

## Priority 2: Make The Project Easier To Cite

Near-term work:

- Keep `CITATION.cff` updated.
- Keep the technical report and demo draft aligned with the README.
- Add stable release notes for each meaningful milestone.
- Avoid changing public claims unless the report, metrics, and examples support
  them.

Paper-facing target:

- System demonstration paper first.
- Technical report or preprint second.
- Industry/application track only if the evaluation story becomes stronger and
  less demo-only.

## Priority 3: Make The Project Easier To Share

Near-term work:

- Use the outreach kit in `docs/OUTREACH_KIT.md`.
- Share one concise LinkedIn/GitHub post after the taxonomy and case-family
  metrics land.
- Create a short GIF or screenshot thread showing one failure case and how the
  report catches it.
- Ask for feedback from LLM evaluation, AI safety, Trust & Safety, and AML/risk
  communities.

Good sharing angle:

> Many LLM demos show fluent answers. Agent Trust Lab asks a different question:
> should this output be trusted, escalated, revised, or rejected?

## Priority 4: Turn Feedback Into Public Proof

Good external proof types:

- GitHub issues with real feedback
- merged PRs from another contributor
- external stars from relevant users
- discussion thread with concrete critique
- workshop or demo submission
- Kaggle or competition evidence linked from the portfolio hub

Avoid:

- buying or begging for stars
- posting shallow "please star my repo" messages
- claiming production compliance use
- publishing private employer data
- overclaiming paper or patent status

## Six-Week Impact Plan

| Week | Main Outcome | Public Evidence |
|---|---|---|
| 1 | Error taxonomy and case-family metrics | README snapshot, metrics JSON, report appendix |
| 2 | 50+ case library and stronger baseline comparison | updated examples and evaluation table |
| 3 | Demo-paper draft v0.2 | demo draft and reproducibility appendix |
| 4 | Outreach post and feedback request | LinkedIn/GitHub post, discussion links |
| 5 | External contribution or issue feedback | merged PR, issue thread, or maintainer response |
| 6 | Resume-ready release | release notes, screenshots, final one-pager |

## Resume Positioning

Use this as the central proof project:

> Built Agent Trust Lab, a public-safe LLM output review system that converts
> risky model and agent outputs into structured trust reports with synthetic
> risk cases, baseline comparison, case-level findings, Markdown/JSON artifacts,
> and human-in-the-loop escalation recommendations.

Supporting projects should point back to this narrative instead of competing
with it for attention.
