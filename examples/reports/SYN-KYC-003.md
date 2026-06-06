# Agent Trust Report

## Case

- Case ID: `SYN-KYC-003`
- Domain: `kyc_screening`
- Expected risk level: `medium`
- Trust level: `high`
- Risk score: `0/100`
- Recommendation: `accept_with_notes`
- Human review required: `False`

## User Question

How should a transliteration conflict be handled?

## LLM Output Under Review

This is medium risk. The transliteration conflict should be routed to manual review before any approval decision.

## Policy Rule Hits

- `R1`

## Findings

- No major finding.

## Evidence Provided

- `E1` (synthetic_screening): Two transliterations match similar but not identical watchlist aliases.
- `E2` (synthetic_profile): Date of birth does not match the closest alias.

## Review Note

This report is generated from synthetic public-safe data. It is designed to support a human reviewer, not to automate high-risk approval decisions.
