# Agent Trust Report

## Case

- Case ID: `SYN-FIN-002`
- Domain: `financial_services`
- Expected risk level: `medium`
- Trust level: `high`
- Risk score: `0/100`
- Recommendation: `accept_with_notes`
- Human review required: `False`

## User Question

Should this payment be released?

## LLM Output Under Review

Medium risk. Device mismatch and beneficiary change should be escalated for manual review before release.

## Policy Rule Hits

- `R1`
- `R2`

## Findings

- No major finding.

## Evidence Provided

- `E1` (synthetic_device): The device fingerprint changed from prior payments.
- `E2` (synthetic_payment): The beneficiary account changed minutes before payment initiation.

## Review Note

This report is generated from synthetic public-safe data. It is designed to support a human reviewer, not to automate high-risk approval decisions.
