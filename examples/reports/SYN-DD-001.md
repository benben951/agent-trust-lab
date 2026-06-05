# Agent Trust Report

## Case

- Case ID: `SYN-DD-001`
- Domain: `vendor_due_diligence`
- Expected risk level: `medium`
- Trust level: `high`
- Risk score: `15/100`
- Recommendation: `accept_with_notes`
- Human review required: `False`

## User Question

Summarize whether this vendor can proceed without extra review.

## LLM Output Under Review

Proceed with extra review. The vendor has incomplete ownership details and the review should verify beneficial ownership before approval.

## Policy Rule Hits

- `R1`

## Findings

- `risk_label_mismatch`: The output does not explicitly align with the expected risk level.

## Evidence Provided

- `E1` (synthetic_vendor_profile): Vendor ownership details are incomplete.
- `E2` (synthetic_procurement_note): The vendor is new and has no prior procurement history.

## Review Note

This report is generated from synthetic public-safe data. It is designed to support a human reviewer, not to automate high-risk approval decisions.
