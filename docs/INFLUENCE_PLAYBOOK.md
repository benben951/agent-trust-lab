# Influence Playbook

This playbook explains how Agent Trust Lab should earn real visibility without
buying followers, inflating stars, or publishing unsafe private data.

The goal is not vanity traffic. The goal is public evidence that the project is
useful, reproducible, and credible for LLM evaluation, agent reliability, and
risk-review AI roles.

## Positioning

Agent Trust Lab should be shared as:

> An open-source review copilot that checks whether risky LLM and agent outputs
> should be trusted, escalated, or rejected.

It should not be shared as:

- a production compliance engine
- an automated AML decision system
- a paper-accepted system before acceptance
- a private employer workflow
- a star-growth campaign

## Influence Strategy

```text
Useful failure case
-> inspectable trust report
-> reproducible demo
-> short technical post
-> targeted feedback request
-> public issue / PR / star / discussion
-> resume evidence
```

Stars are a byproduct of trust. They are not the strategy.

## What Not To Do

| Tactic | Decision | Reason |
|---|---|---|
| Buy followers | Do not do it | It weakens credibility and creates no technical evidence. |
| Sell risky cleanup EXEs as the main project | Avoid as main line | It creates security, support, and trust concerns. |
| Ask strangers to star without context | Avoid | It looks spammy and does not produce useful feedback. |
| Publish raw work records | Do not do it | Private data and employer context must stay private. |
| Overclaim production use | Do not do it | Current evidence is synthetic and public-safe. |

## Better Visibility Paths

### 1. Technical Posts

Publish one concrete artifact at a time.

Good topics:

- Why fluent LLM answers still need trust reports.
- A real agent failure pattern: tool failed, final answer claimed success.
- How to evaluate human-review routing instead of only accuracy.
- What AML review taught me about LLM output verification.
- Building a public-safe benchmark for risky AI outputs.

Each post should include:

- one failure case
- one screenshot or report link
- one metric
- one honest limitation
- one feedback question

### 2. Open Source Feedback

Ask for critique, not applause.

Good feedback targets:

- LLM evaluation maintainers
- agent framework maintainers
- Trust & Safety practitioners
- compliance QA practitioners
- AI safety and governance communities

Good ask:

> I would appreciate feedback on whether this taxonomy catches useful
> second-pass review failures.

Weak ask:

> Please star my repo.

### 3. External PRs

Use small, relevant PRs to build credible external proof.

Best PR types:

- documentation examples for LLM evaluation projects
- test cases for agent failure modes
- reproducibility fixes
- CI or quickstart improvements
- small benchmark or report examples

Resume value comes from merged, relevant contributions, not raw PR count.

### 4. Product-Like Demo

Keep the live demo easy to understand in under three minutes:

- what went wrong
- what the system detected
- why human review is required
- where the report artifact is
- how to reproduce it locally

## Four-Week Visibility Plan

| Week | Outcome | Evidence |
|---|---|---|
| 1 | Productized README and shareable post | README, post draft, live demo |
| 2 | One public feedback thread | GitHub issue, LinkedIn post, outreach log |
| 3 | One external PR or discussion | PR link, maintainer response, or issue comment |
| 4 | Resume-ready release | release notes, screenshots, metrics, one-pager |

## First Post Plan

Use [`POST_RISK_REVIEW_COPILOT.md`](POST_RISK_REVIEW_COPILOT.md).

Target platforms:

- LinkedIn first
- GitHub repository discussion or issue second
- Chinese note after the English version is stable

Call to action:

> Feedback is welcome on the error taxonomy and whether the workflow catches
> the right review failures.

## Resume Translation

Good resume bullet:

> Built Agent Trust Lab, an open-source LLM/agent output review copilot that
> converts risky outputs into Markdown/JSON trust reports, compares a naive
> confidence baseline against structured review routing, and evaluates 52
> synthetic cases across 8 risk families with CI and a live demo.

Avoid:

> Built a popular AI project.

Popularity should be proven by links, stars, feedback, issues, PRs, or usage.
