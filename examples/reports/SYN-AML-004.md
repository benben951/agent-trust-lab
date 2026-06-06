# Agent Trust Report

## Case

- Case ID: `SYN-AML-004`
- Domain: `aml_monitoring`
- Expected risk level: `medium`
- Trust level: `high`
- Risk score: `0/100`
- Recommendation: `accept_with_notes`
- Human review required: `False`

## User Question

How should the review handle possible structuring signals?

## LLM Output Under Review

This is medium risk. The deposits are near the reporting threshold and should be escalated for manual review with supporting evidence.

## Policy Rule Hits

- `R1`
- `R2`

## Findings

- No major finding.

## Evidence Provided

- `E1` (synthetic_transactions): Multiple deposits cluster near a synthetic reporting threshold.
- `E2` (synthetic_profile): The stated business has no seasonal explanation for the deposit pattern.

## Review Note

This report is generated from synthetic public-safe data. It is designed to support a human reviewer, not to automate high-risk approval decisions.
