# Baseline Comparison

## Question

How often would a naive reviewer accept confident LLM outputs compared with the structured trust-report workflow?

## Summary

| Metric | Value |
|---|---:|
| Total cases | 40 |
| Naive accept cases | 26 |
| Naive accept rate | 65% |
| Naive false accept cases | 19 |
| Naive false accept rate | 48% |
| Trust workflow accept cases | 14 |
| Trust workflow accept rate | 35% |
| Trust workflow manual review cases | 26 |
| Trust workflow manual review rate | 65% |

## Interpretation

The naive baseline treats confident acceptance language as usable. Agent Trust Lab instead routes unsupported, overconfident, policy-mismatched, or escalation-missing outputs to human review. This comparison is synthetic and public-safe; it demonstrates evaluation mechanics rather than production business impact.
