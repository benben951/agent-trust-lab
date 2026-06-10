# Agent Trust Lab Demo Script

Use this for a three-minute recruiter, portfolio, or EMNLP system-demo walkthrough.

## Setup

Run:

```powershell
python -m pytest -q
python -m agent_trust_lab.cli batch-review --cases-dir examples\cases --out-dir examples\reports --summary examples\batch_summary.json
python -m agent_trust_lab.cli summarize --summary examples\batch_summary.json --out examples\evaluation_metrics.json
python -m agent_trust_lab.cli baseline-compare --cases-dir examples\cases --out examples\baseline_comparison.json --markdown-out examples\baseline_comparison.md
python -m http.server 8765
```

Open:

```text
http://localhost:8765/web/
```

## Demo Narrative

### 0:00-0:20 Problem

Say:

> In risk-sensitive workflows, a fluent LLM answer is not enough. The question is whether a reviewer can trust the output enough to accept it, escalate it, reject it, or ask for revision.

Show:

- Browser console title.
- Status strip: 52 synthetic cases, representative web queue, human review first.

### 0:20-0:50 Case Queue

Say:

> Agent Trust Lab treats every model output as a case package with synthetic evidence, policy rules, expected risk level, and an output under review.

Show:

- Case queue.
- Domain filter.
- One low-trust AML or agent-output case.

### 0:50-1:30 Trust Report

Say:

> The system turns the output into a trust report. It checks evidence support, policy signals, unsafe certainty, escalation behavior, and risk-label alignment.

Show:

- Risk score.
- Recommendation.
- Human review flag.
- Finding badges.
- Trust report preview.

### 1:30-2:00 Baseline Comparison

Open:

```text
examples/baseline_comparison.md
```

Say:

> I also compare this against a deliberately weak baseline that treats confident accept or approve language as usable. On the 52-case synthetic set, the naive baseline accepts 38 cases and produces 25 false accepts under the trust-workflow criteria.

Show:

- Naive false accept cases: 25.
- Trust workflow manual review cases: 32.

### 2:00-2:35 Multi-Role Workflow Trace

Open:

```text
examples/workflow_report_agent_tool_failure.md
```

Say:

> For agent outputs, the demo can decompose the review into evidence, policy, risk, escalation, and final reviewer roles. This is useful when a tool call failed but the final agent answer sounds successful.

Show:

- Failed roles.
- Final routing.
- Public safety boundary.

### 2:35-3:00 Governance Boundary

Open:

```text
docs/GOVERNANCE.md
```

Say:

> The system supports human review. It does not approve high-risk financial, compliance, or user-impacting decisions automatically. The public demo uses only synthetic data and keeps patent-facing details outside the repository.

Show:

- Data boundary.
- Decision boundary.
- Logs and metrics section.

## Screenshot Checklist

Capture these for a paper or portfolio page:

| Screenshot | File suggestion | Purpose |
|---|---|---|
| Browser console overview | `assets/demo_console_overview.png` | Shows product surface. |
| Low-trust case selected | `assets/demo_low_trust_case.png` | Shows findings and routing. |
| Baseline comparison table | `assets/demo_baseline_comparison.png` | Shows naive false accepts. |
| Workflow report role trace | `assets/demo_workflow_trace.png` | Shows multi-role review. |
| Governance checklist | `assets/demo_governance_boundary.png` | Shows safety boundary. |

## Interview Version

Short pitch:

> I built Agent Trust Lab because LLM evaluation for risk-sensitive workflows cannot stop at answer quality. The system generates trust reports, baseline comparisons, and multi-role workflow traces from synthetic cases, so a human reviewer can inspect evidence support, policy signals, uncertainty, escalation, and final routing.

## Submission Version

System-demo pitch:

> Agent Trust Lab is an inspectable system demonstration for human-in-the-loop review of risk-sensitive LLM and agent outputs. It provides a CLI, static browser console, Markdown/JSON reports, a 52-case synthetic library, naive-baseline comparison, and governance documentation.
