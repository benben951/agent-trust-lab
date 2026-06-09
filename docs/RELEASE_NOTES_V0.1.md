# v0.1 Release Notes

Agent Trust Lab v0.1 packages a public-safe LLM and agent output review workflow for risk-sensitive settings.

## Highlights

- Markdown and JSON trust reports for synthetic LLM/agent outputs.
- 40-case synthetic evaluation library.
- Naive acceptance baseline comparison.
- Public-safe multi-role workflow trace: evidence, policy, risk, escalation, and final review.
- Static browser demo via GitHub Pages.
- CI-backed tests and recruiter/interviewer review packet.

## Good First Review Path

1. Open the live demo: https://benben951.github.io/agent-trust-lab/
2. Read `docs/REVIEW_PACKET.md`.
3. Inspect `examples/workflow_report_agent_tool_failure.md`.
4. Run `python -m pytest -q`.

## Boundary

The repo uses synthetic data only. It does not include employer data, customer data, real regulated cases, or patent-facing claim details.
