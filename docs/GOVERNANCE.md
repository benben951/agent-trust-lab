# Governance Checklist

Agent Trust Lab is designed as a human-review support system.

## Data Boundary

- Use synthetic or public-safe examples only.
- Do not include real customer data, transaction records, private policies, credentials, or internal labels.
- Keep patent claim drafts outside public repositories until filing guidance is clear.

## Decision Boundary

- The system does not approve high-risk financial, compliance, or user-impacting decisions.
- Medium and high-risk cases require manual review.
- The report is an evidence artifact, not a final business decision.

## Logs

Each review should preserve:

- case ID
- evidence IDs
- policy rule hits
- findings
- risk score
- recommendation
- report timestamp in future versions
- reviewer override in future versions

## Metrics

Minimum evaluation metrics:

- unsafe pass rate
- escalation recall
- unsupported-claim rate
- policy-signal coverage
- reviewer disagreement
- report latency

## Public Demo Safety

The public demo:

- uses fake case IDs
- uses synthetic evidence
- does not call external LLM APIs
- does not store secrets
- does not expose patent claim language

