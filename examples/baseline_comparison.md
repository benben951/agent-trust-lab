# Baseline Comparison

## Question

How often would a naive reviewer accept confident LLM outputs compared with the structured trust-report workflow?

## Summary

| Metric | Value |
|---|---:|
| Total cases | 52 |
| Naive accept cases | 38 |
| Naive accept rate | 73% |
| Naive false accept cases | 25 |
| Naive false accept rate | 48% |
| Trust workflow accept cases | 20 |
| Trust workflow accept rate | 38% |
| Trust workflow manual review cases | 32 |
| Trust workflow manual review rate | 62% |

## Interpretation

The naive baseline treats confident acceptance language as usable. Agent Trust Lab instead routes unsupported, overconfident, policy-mismatched, or escalation-missing outputs to human review. This comparison is synthetic and public-safe; it demonstrates evaluation mechanics rather than production business impact.
