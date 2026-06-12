# Post Draft: Risk Review Copilot

Working title:

> I built a Risk Review Copilot for LLM outputs in AML/KYC-style workflows

Short version:

I have been thinking about a practical problem in AI adoption: in risk-sensitive workflows, a fluent LLM answer is not the same as a trustworthy answer.

For AML/KYC, sanctions screening, due diligence, payment-fraud review, compliance QA, and agent tool-use workflows, the question is usually not:

```text
Can the model answer?
```

It is:

```text
Can a human reviewer trust this output enough to accept it, escalate it, or reject it?
```

So I built Agent Trust Lab as a public-safe prototype for LLM and agent-output review.

What it does:

- turns LLM/agent outputs into Markdown and JSON trust reports
- checks evidence support, policy signals, risk-label alignment, unsafe certainty, and missing escalation
- compares a naive "accept confident outputs" baseline against a structured review workflow
- includes 52 synthetic cases across AML/KYC, sanctions, due diligence, financial risk, trust and safety, health-safety, data quality, and agent reliability
- adds realistic agent failure cases such as "tool failed but the agent claimed success"
- keeps high-risk decisions human-in-the-loop

Current evidence:

- 52-case synthetic evaluation set
- 8 case families
- 48% naive false-accept rate on the synthetic benchmark
- 61.5% manual-review routing rate in the trust workflow
- CI and GitHub Pages demo

The project is not a production compliance engine. It is a small, inspectable system for asking better evaluation questions:

- Is the conclusion supported by evidence?
- Did the model miss a required policy signal?
- Is the answer too certain?
- Should the case be escalated?
- What should the human reviewer check next?

Repo:

https://github.com/benben951/agent-trust-lab

Live demo:

https://benben951.github.io/agent-trust-lab/

I would be very interested in feedback from people working on LLM evaluation, risk operations, compliance QA, Trust & Safety, or agent reliability.
