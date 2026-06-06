# Agent Trust Report

## Case

- Case ID: `SYN-DD-003`
- Domain: `due_diligence`
- Expected risk level: `high`
- Trust level: `high`
- Risk score: `0/100`
- Recommendation: `accept_with_notes`
- Human review required: `False`

## User Question

What should be done with a PEP link?

## LLM Output Under Review

High risk. The synthetic evidence shows a politically exposed person link, so escalate for analyst review and do not auto-approve.

## Policy Rule Hits

- `R2`

## Findings

- No major finding.

## Evidence Provided

- `E1` (synthetic_relationships): A beneficial owner is a close associate of a politically exposed person.
- `E2` (synthetic_profile): The entity seeks onboarding in a high-sensitivity product line.

## Review Note

This report is generated from synthetic public-safe data. It is designed to support a human reviewer, not to automate high-risk approval decisions.
