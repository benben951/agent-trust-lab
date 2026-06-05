# Agent Trust Report

## Case

- Case ID: `SYN-KYC-001`
- Domain: `kyc_review`
- Expected risk level: `medium`
- Trust level: `medium`
- Risk score: `35/100`
- Recommendation: `escalate_for_manual_review`
- Human review required: `True`

## User Question

Is the identity verification output acceptable?

## LLM Output Under Review

The identity verification is low risk and can be accepted. The address appears consistent.

## Policy Rule Hits

- No policy rule hit.

## Findings

- `missing_policy_signal`: The output does not reference any required policy signal.
- `risk_label_mismatch`: The output does not explicitly align with the expected risk level.

## Evidence Provided

- `E1` (synthetic_document_check): The identity document address differs from the submitted onboarding address.
- `E2` (synthetic_user_profile): The user updated the address twice during the onboarding flow.

## Review Note

This report is generated from synthetic public-safe data. It is designed to support a human reviewer, not to automate high-risk approval decisions.
