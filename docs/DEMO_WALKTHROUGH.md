# Agent Trust Lab Demo Walkthrough

This is the shortest recruiter- and interviewer-facing path through Agent Trust Lab. It is designed for a three-minute review, not a full technical audit.

Live demo: [https://benben951.github.io/agent-trust-lab/](https://benben951.github.io/agent-trust-lab/)

Screenshots: [DEMO_SCREENSHOTS.md](DEMO_SCREENSHOTS.md)

## 1. Thirty-Second Positioning

Agent Trust Lab reviews whether an LLM or agent output is safe enough to accept, escalate, or reject in a risk-sensitive workflow.

The project is not a chatbot demo. It is an evaluation and governance workflow with:

- a 40-case synthetic evaluation set
- Markdown and JSON trust reports
- naive-baseline comparison
- multi-role workflow traces
- human-in-the-loop routing
- public-safe governance boundaries

## 2. Three-Minute Review Path

| Time | Open | What to inspect | What it proves |
|---:|---|---|---|
| 0:00-0:30 | [Live demo](https://benben951.github.io/agent-trust-lab/) | Case queue, selected case, risk score, findings, and recommendation. | The project has a usable review surface, not only backend scripts. |
| 0:30-1:00 | [Review Packet](REVIEW_PACKET.md) | Three-minute summary, domains, metrics, and report links. | The system has a clear hiring-facing story and measurable outputs. |
| 1:00-1:30 | [Baseline Comparison](../examples/baseline_comparison.md) | Naive false accepts: 19; naive false accept rate: 48%. | A confident LLM output is not the same as a verified decision. |
| 1:30-2:15 | [Agent Tool-Failure Workflow](../examples/workflow_report_agent_tool_failure.md) | Evidence, policy, risk, escalation, and final reviewer notes. | The workflow can expose an agent that sounds successful after a tool failure. |
| 2:15-2:40 | [Evaluation Metrics](EVALUATION_METRICS.md) | Manual-review rate, low-trust rate, finding distribution, and limitations. | The project treats escalation and uncertainty as measurable system behavior. |
| 2:40-3:00 | [Governance](GOVERNANCE.md) | Data boundary, decision boundary, and human oversight. | The demo is public-safe and does not automate high-risk approvals. |

## 3. Best Case To Show First

Start with `SYN-AGENT-001`, the agent tool-failure case.

Why it works well in interviews:

- The failure is easy to understand: a lookup tool timed out.
- The final agent answer still says the lookup succeeded.
- The workflow catches the mismatch and routes it to human review.
- The example connects directly to modern agent evaluation work.

Open:

- [Case Walkthrough](CASE_WALKTHROUGH.md)
- [Workflow Report](../examples/workflow_report_agent_tool_failure.md)
- [JSON Workflow Report](../examples/workflow_report_agent_tool_failure.json)

## 4. Metrics To Quote

Use these numbers when introducing the project:

| Metric | Value |
|---|---:|
| Synthetic cases | 40 |
| Manual-review cases | 26 |
| Manual-review rate | 65% |
| Low-trust cases | 19 |
| Low-trust rate | 47.5% |
| Naive accept cases | 26 |
| Naive false accept cases | 19 |
| Naive false accept rate | 48% |
| Trust workflow accept cases | 14 |

Suggested wording:

> On a 40-case synthetic risk review set, a naive confident-output baseline accepts 26 cases and creates 19 false accepts under the trust-workflow criteria. Agent Trust Lab routes these risky or under-supported outputs into manual review instead of auto-accepting them.

## 5. Interview Pitch

English:

> I built Agent Trust Lab because LLM evaluation in risk-sensitive workflows cannot stop at answer fluency. The system turns model or agent outputs into trust reports with evidence checks, policy-signal checks, risk findings, baseline comparison, and human-review routing. It uses synthetic public-safe cases so the workflow can be inspected without exposing real customer data or private policies.

Chinese:

> 我做 Agent Trust Lab 的核心原因是：在风控、合规、Trust & Safety 或 Agent 输出复审场景里，模型回答得流畅不代表可以被信任。这个项目把 LLM 或 Agent 的输出转成可审计的 trust report，检查证据支撑、规则信号、风险标签、升级处理和最终路由，并用 40 个公开安全的 synthetic cases 做基线对比和指标汇总。

## 6. What Not To Claim

Do not describe the current public demo as production performance evidence.

Safe claims:

- public-safe prototype
- synthetic evaluation set
- inspectable trust-report workflow
- baseline comparison
- human-in-the-loop governance
- recruiter-facing portfolio artifact

Avoid:

- claiming real AML model accuracy
- claiming real customer-data validation
- exposing private employer process details
- exposing patent claim text
- saying high-risk decisions are automatically approved
