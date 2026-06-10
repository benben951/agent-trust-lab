# Paper Strategy

This project is best positioned as a system demonstration first, not as a
foundation-model research paper.

## Current Best Fit

Primary target:

- EMNLP 2026 System Demonstration track

Secondary targets:

- technical report or preprint
- workshop paper on LLM evaluation, agent reliability, governance, or
  human-in-the-loop review
- industry/application track only if the evaluation story becomes stronger

## Why System Demonstration Fits

Agent Trust Lab has:

- a working browser demo
- runnable CLI commands
- synthetic cases
- structured reports
- baseline comparison
- metrics summaries
- public-safe governance boundaries

This matches a system-demo contribution better than a pure modeling paper.

## Current 2026 Submission Window

As of 2026-06-10:

| Venue / Track | Status | Date |
|---|---|---|
| EMNLP 2026 main long/short papers | ARR submission deadline has passed | 2026-05-25 |
| EMNLP 2026 Industry Track | very close; possible only with a strong applied story | 2026-06-16 |
| EMNLP 2026 System Demonstrations | best near-term fit | 2026-07-10 |

Official pages to re-check before any submission:

- https://2026.emnlp.org/calls/main_conference_papers/
- https://2026.emnlp.org/calls/industry_track/
- https://2026.emnlp.org/calls/demos/

## Submission Readiness Checklist

Before submitting anywhere, the project should have:

- 50+ synthetic cases, or a clear explanation of why the current case count is
  enough for a demo paper.
- case-family metrics instead of only aggregate metrics.
- formal error taxonomy.
- reproducibility commands that work from a fresh clone.
- a concise demo script.
- screenshots or GIFs that show the system in use.
- limitations and ethics sections.
- no private employer data.
- no private Kaggle data.
- no unsupported production claims.

## Suggested Paper Claim

Strong:

> Agent Trust Lab demonstrates a public-safe workflow for converting
> risk-sensitive LLM and agent outputs into structured trust reports with
> evidence-grounded findings, baseline comparison, metrics summaries, and
> human-in-the-loop routing recommendations.

Weak:

> Agent Trust Lab solves LLM trust.

Avoid the weak claim.

## Paper Outline

1. Introduction
2. Motivation: fluent outputs are not sufficient in risk-sensitive workflows
3. System overview
4. Case schema and public-safe data design
5. Error taxonomy and trust-report generation
6. Baselines and metrics
7. Demo walkthrough
8. Limitations and governance boundaries
9. Conclusion

## Work Needed Next

Highest-value additions:

1. Formal error taxonomy.
2. Case-family metrics.
3. Error analysis table.
4. More clear comparison between naive acceptance and trust-report workflow.
5. Reproducibility appendix.

## Relationship To Patent Work

The public paper and repo should describe the demo-safe layer:

- case schema
- deterministic public checks
- report format
- evaluation methodology
- governance boundary

Potential patent-facing claims should stay outside the public repo until a filing
decision is made.
