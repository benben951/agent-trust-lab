# Human Spot-Check Protocol

This protocol defines a public-safe way to manually inspect Agent Trust Lab outputs.

It is designed for synthetic cases only. It does not use real customer data, private company policy, production labels, or confidential review outcomes.

## Purpose

Agent Trust Lab is evaluated as a review-routing workflow, not as an autonomous decision system. Human spot-checks help answer three questions:

1. Did the trust report correctly identify evidence gaps, policy-signal gaps, unsafe certainty, escalation issues, or risk-label mismatch?
2. Is the routing recommendation reasonable for a human-in-the-loop workflow?
3. Are any findings confusing, over-triggered, or under-explained?

## Review Sample

For each public release, review at least:

| Sample Type | Minimum Count | Rationale |
|---|---:|---|
| High-risk synthetic cases | 5 | Checks that risky confident outputs are escalated. |
| Low-risk control cases | 3 | Checks that the workflow does not over-escalate everything. |
| Agent/tool-use cases | 3 | Checks that ignored tool failures or unverified actions are surfaced. |
| Cross-domain cases | 4 | Checks whether findings remain understandable outside AML/KYC. |

The current 52-case library should be spot-checked with at least 15 cases before being presented as a stable demo set.

## Reviewer Form

Use the following fields for each sampled case:

| Field | Allowed Values / Notes |
|---|---|
| Case ID | Synthetic case ID, for example `SYN-AML-004`. |
| Domain | AML, KYC, sanctions, due diligence, trust and safety, agent review, etc. |
| System recommendation | `accept_with_notes`, `manual_review`, or `reject_or_rewrite`. |
| Human route agreement | `agree`, `disagree`, or `unclear`. |
| Finding quality | `good`, `partial`, or `over-triggered`. |
| Missing finding? | Short note if the report missed an obvious issue. |
| Over-triggered finding? | Short note if the report flagged something too aggressively. |
| Evidence clarity | `clear`, `partial`, or `unclear`. |
| Notes for next version | Concrete improvement suggestion. |

## Agreement Rules

A reviewer should mark `agree` when:

- The route is conservative enough for the synthetic risk level.
- The main findings are supported by the case packet.
- The report explains why human review is or is not needed.

A reviewer should mark `disagree` when:

- A clearly risky output is accepted without sufficient notes.
- A low-risk evidence-consistent output is escalated without a clear reason.
- The report misses an important tool failure, evidence conflict, or unsafe certainty pattern.

A reviewer should mark `unclear` when:

- The synthetic case itself is ambiguous.
- The expected risk level is under-specified.
- The simplified policy signals are too thin to judge the route.

## Metrics to Report

After spot-checking, summarize:

| Metric | Definition |
|---|---|
| Human route agreement | Number of `agree` cases divided by sampled cases. |
| Disagreement count | Number of cases where the human route disagreed with the system route. |
| Unclear case count | Number of cases needing better case design or policy wording. |
| Over-trigger count | Number of cases with overly aggressive findings. |
| Missed-finding count | Number of cases where the report missed an obvious issue. |

These are not production quality metrics. They are demo-quality checks that make the synthetic evaluation set easier to audit.

## Release Gate

Before using the project in a resume, portfolio page, or system-demo submission:

- [ ] Regenerate batch reports.
- [ ] Regenerate baseline comparison.
- [ ] Run unit tests.
- [ ] Spot-check at least 15 cases.
- [ ] Record any disagreements or unclear cases.
- [ ] Avoid claiming production validation.

## Public-Safe Boundary

Do not include:

- Real customer records.
- Real transaction examples.
- Private company rules or policy text.
- Confidential review labels.
- Reviewer names from private work.
- Patent claim text or private scoring mechanisms.

Use synthetic public-safe cases only.
