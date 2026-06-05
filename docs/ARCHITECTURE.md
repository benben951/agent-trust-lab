# Architecture

Agent Trust Lab is a public-safe system design for LLM output review in risk-sensitive workflows.

## Public Architecture

```text
case input
  |
  v
synthetic evidence package
  |
  v
review pipeline
  |-- evidence checker
  |-- policy-signal checker
  |-- risk-language checker
  |-- escalation checker
  |
  v
trust scoring
  |
  v
Markdown / JSON report
  |
  v
human reviewer
```

## Review Roles

| Role | Responsibility | Public demo status |
|---|---|---|
| Extractor | Identify entities, evidence, risk signals, and policy references. | Represented by deterministic checks. |
| Policy checker | Compare output against provided policy rules. | Implemented with required-term rules. |
| Evidence verifier | Flag unsupported risk claims. | Implemented with synthetic evidence matching. |
| Risk scorer | Convert findings into a risk-sensitive score. | Implemented with transparent weights. |
| Reporter | Produce human-readable trust reports. | Implemented as Markdown output. |

## Design Boundary

The public implementation intentionally uses deterministic checks. This keeps the demo inspectable and avoids exposing patent-facing implementation details before a filing decision.

## Intended Extension

Future private or post-filing versions can add:

- model-based evidence extraction
- multi-agent disagreement analysis
- calibrated reviewer override tracking
- workflow-level evaluation with `agent-workflow-bench`
- proxy trust checks from `llm-proxy-auditor`
- AML RAG evidence from `gemma-aml-assistant`

