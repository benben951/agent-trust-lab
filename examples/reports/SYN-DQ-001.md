# Agent Trust Report

## Case

- Case ID: `SYN-DQ-001`
- Domain: `ai_data_quality`
- Expected risk level: `medium`
- Trust level: `medium`
- Risk score: `35/100`
- Recommendation: `escalate_for_manual_review`
- Human review required: `True`

## User Question

Review whether the model label should be accepted.

## LLM Output Under Review

Accept the label as low risk. The annotator and model agree.

## Policy Rule Hits

- No policy rule hit.

## Findings

- `missing_policy_signal`: The output does not reference any required policy signal.
- `risk_label_mismatch`: The output does not explicitly align with the expected risk level.

## Evidence Provided

- `E1` (synthetic_annotation_log): Annotator A marked the sample as medium risk.
- `E2` (synthetic_model_output): The model predicted low risk without citing evidence.

## Review Note

This report is generated from synthetic public-safe data. It is designed to support a human reviewer, not to automate high-risk approval decisions.
