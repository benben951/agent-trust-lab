# Realistic Review Cases

Agent Review Copilot now includes public-safe cases adapted from common AI coding failure modes. They are not raw private transcripts. They preserve the review pattern while removing personal files, employer data, and local secrets.

## Why These Cases Matter

Synthetic benchmark cases are useful for coverage, but agent review tools become more convincing when they handle the kinds of mistakes that happen in real tool-using workflows:

- a tool call fails, but the agent still claims the task succeeded
- a browser check fails, but the agent still claims visual QA was completed
- the final answer lacks the verification evidence that the task required

## Included Cases

| Case | Pattern | Expected Route |
|---|---|---|
| `REALISTIC-CODEX-001` | Command failure followed by false success claim | Manual review |
| `REALISTIC-CODEX-002` | Browser verification failure followed by unsupported completion claim | Manual review |

## Safety Boundary

These examples are manually sanitized and rewritten. Do not publish raw local agent transcripts unless they have been reviewed for:

- personal data
- employer or client data
- file paths
- credentials or tokens
- private documents
- browser/session artifacts

## Reproduce

```powershell
python -m agent_trust_lab.cli copilot-review --input examples\realistic_cases\codex_tool_failure_false_success.txt --out examples\realistic_reports\REALISTIC-CODEX-001.md --json-out examples\realistic_reports\REALISTIC-CODEX-001.json
python -m agent_trust_lab.cli copilot-review --input examples\realistic_cases\codex_browser_claim_without_evidence.txt --out examples\realistic_reports\REALISTIC-CODEX-002.md --json-out examples\realistic_reports\REALISTIC-CODEX-002.json
```

The important test is not that the copilot catches every possible issue. The useful first milestone is that it consistently flags unsupported completion claims and routes them to human review with concrete next checks.
