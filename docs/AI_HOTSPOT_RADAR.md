# AI Hotspot Radar

Purpose: turn daily AI news into product, research, and career evidence for Agent Trust Lab. This file is not a news digest. Each entry must answer: what can we learn, what can we build, what should we avoid, and what evidence can we show publicly.

Last updated: 2026-06-14

## Operating Rule

Use this compact loop for every hotspot:

```text
Signal -> credible source -> project implication -> safe experiment -> public evidence
```

Do not chase hype. If a claim cannot be verified from a credible source, keep it as a weak signal and do not build public claims on it.

## Radar Table

| Date | Hotspot | Credible source | What it means for us | Reusable pattern | Risk / do not do | Next action |
|---|---|---|---|---|---|---|
| 2026-06-14 | DeepMind report: From AGI to ASI | arXiv 2606.12683 | Multi-agent scale, recursive improvement, and governance bottlenecks strengthen our core thesis: powerful agents need review, calibration, and trust reports. | Treat agent systems as socio-technical workflows, not single prompts. Evaluate handoffs, escalation, and failure modes. | Do not make speculative ASI claims in README. Use it as research motivation only. | Add a short "Why trust reports matter for multi-agent systems" paragraph to technical report or paper draft. |
| 2026-06-14 | AI browser / Tabbit 1.0: reusable browser-agent workflows | 36Kr English / Yicai reports | Browser agents are moving from chat to repeatable workflow automation. This matches our "review copilot" direction: users need saved review recipes, not one-off prompts. | Convert repeated review actions into reusable workflows: input capture -> risk checks -> evidence report -> human decision. | Do not promise automatic web actions for sensitive tasks without audit logs and human confirmation. | Add one demo recipe: "Review an agent claim against tool evidence." |
| 2026-06-14 | Fable 5 / leaked prompt claims | Unverified social/news chain; treat as weak signal | The useful lesson is not the leak. The lesson is that system prompts, tool permissions, and safety boundaries are product-critical. | Create "prompt and permission boundary" checklist for agent review. | Do not reproduce leaked system prompts, bypass commands, or permission-skipping flows. | Add a safety note: Agent Trust Lab evaluates failures; it does not teach bypasses. |
| 2026-06-14 | system-design-primer remains a high-signal learning repo | GitHub: donnemartin/system-design-primer | For foreign-company AI application roles, system design still matters. Our projects need architecture diagrams, data flow, queues, storage, observability, and failure handling. | Every public project should include an architecture page and one scalability/failure-mode section. | Do not only show prompt demos; they look shallow. | Use system-design framing to improve Agent Review Copilot architecture docs. |
| 2026-06-14 | The Book of Secret Knowledge | GitHub: trimstray/the-book-of-secret-knowledge | Useful as a tool index and engineering reference. It can improve our developer toolbox and interview breadth. | Maintain a curated "allowed tools" list for safe debugging, CLI, logs, docs, and observability. | Avoid security gray-zone usage, scraping abuse, credential handling, or offensive content. | Create a safe engineering toolbox section later if needed. |

## Product Implications For Agent Trust Lab

### 1. Agent systems need evidence, not just confident answers

The DeepMind report frames future AI progress partly through scaling, recursive improvement, and multi-agent collectives. For our project, the practical takeaway is simple: as agents become more autonomous and more numerous, the failure surface becomes larger. A trust report should record:

- the claim made by the agent
- the tool evidence it used
- missing or contradictory evidence
- risk category
- recommended human decision
- whether escalation is required

This is directly aligned with our AML / review / second-level review experience: the valuable skill is not blindly trusting outputs, but finding repeatable features of risky conclusions.

### 2. Browser-agent workflows make "review copilot" more realistic

AI browsers such as Tabbit suggest that users will increasingly save workflows instead of writing fresh prompts every time. Agent Trust Lab should therefore emphasize reusable review recipes:

- claim-vs-tool-evidence check
- hallucinated citation check
- failed-tool-but-confident-answer check
- policy-sensitive decision escalation
- customer / compliance / finance review summary

### 3. Safety boundary is part of the product value

The Fable 5 discussion is useful only as a cautionary signal. We should position Agent Trust Lab as a defensive evaluation and review framework:

- no leaked prompts
- no bypass reproduction
- no permission-skipping tutorials
- no credential or cookie handling
- no live financial or compliance decisions without human review

This is not a weakness. For risk-sensitive AI roles, this is exactly the mature engineering stance.

## Career Implications

This radar supports the user's target narrative:

```text
AML / review operations
-> pattern extraction and复审
-> LLM output review
-> agent workflow trust reports
-> AI application / risk data / LLM evaluation roles
```

The strongest resume angle is:

```text
Built an open-source Agent Trust Lab that converts agent outputs into evidence-backed trust reports, with synthetic risk cases, baseline comparison, CI, demo, and public feedback loop.
```

## Source Links

- DeepMind report: [From AGI to ASI, arXiv 2606.12683](https://arxiv.org/abs/2606.12683)
- Tabbit report: [36Kr English on Tabbit 1.0](https://eu.36kr.com/en/p/3845982766680581)
- Tabbit earlier report: [Yicai Global on Tabbit](https://www.yicaiglobal.com/news/meituan-unit-introduces-ai-powered-browser-tabbit)
- System design reference: [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer)
- Engineering reference index: [trimstray/the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge)

## Next Build Ideas

1. Add a `review recipe` concept to Agent Trust Lab docs.
2. Add one synthetic case family for "agent claimed success after tool failure."
3. Add a public-safe checklist for prompt, permission, and evidence boundaries.
4. Turn one radar entry per week into a LinkedIn/GitHub post with a concrete demo.
