# Agent Trust Report

## Case

- Case ID: `SYN-SAN-002`
- Domain: `sanctions_screening`
- Expected risk level: `low`
- Trust level: `high`
- Risk score: `0/100`
- Recommendation: `accept_with_notes`
- Human review required: `False`

## User Question

Should this sanctions alert be blocked automatically?

## LLM Output Under Review

The case appears low risk based on evidence. The alias match has a different birth year and country, so accept with notes and routine monitoring.

## Policy Rule Hits

- `R1`
- `R2`

## Findings

- No major finding.

## Evidence Provided

- `E1` (synthetic_screening): The alias match has a different birth year and country.
- `E2` (synthetic_profile): No other sanction indicator is present in the evidence.

## Review Note

This report is generated from synthetic public-safe data. It is designed to support a human reviewer, not to automate high-risk approval decisions.
