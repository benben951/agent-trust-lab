# Post Draft: Risk Review Copilot

## LinkedIn / GitHub Post

I built a small open-source project called Agent Trust Lab to explore a question
I keep running into when working with AI agents:

> A model can sound confident, but should a human reviewer trust the output?

This matters in risk-sensitive workflows such as AML/KYC-style review,
compliance QA, due diligence, Trust & Safety, and agent tool-use review.

In these settings, the key question is not only:

```text
Can the model produce an answer?
```

It is:

```text
Should this output be accepted, escalated, revised, or rejected?
```

So I built Agent Trust Lab as a public-safe prototype for second-pass review of
LLM and agent outputs.

What it does:

- converts LLM/agent outputs into Markdown and JSON trust reports
- checks evidence support, policy signals, unsafe certainty, risk-label
  mismatch, and missing escalation
- compares a naive "accept confident outputs" baseline against a structured
  trust-review workflow
- includes 52 synthetic review cases across 8 risk families
- includes realistic agent failure patterns, such as "a tool failed but the
  agent claimed success"
- keeps high-risk decisions human-in-the-loop

Current evidence:

- 52 synthetic cases
- 8 case families
- 48% naive false-accept rate on the synthetic benchmark
- 61.5% manual-review routing rate in the trust workflow
- CI, CLI reproduction steps, and a GitHub Pages demo

The project is not a production compliance engine. It intentionally uses
synthetic, public-safe cases. The goal is to make LLM review failures easier to
inspect, discuss, and reproduce.

Repo:
https://github.com/benben951/agent-trust-lab

Live demo:
https://benben951.github.io/agent-trust-lab/

I would appreciate feedback from people working on LLM evaluation, agent
reliability, Trust & Safety, compliance QA, or risk operations:

1. Are these error categories useful for second-pass review?
2. Which failure modes are missing?
3. What metrics would make this more credible?
4. What would you need before trusting a workflow like this in a real review
   process?

## Short Chinese Version

我做了一个开源小项目 Agent Trust Lab，想验证一个很实际的问题：

> AI Agent 的回答很流畅，但人到底能不能信？

在 AML/KYC、合规 QA、尽调、Trust & Safety、Agent 工具调用等风险敏感场景里，关键问题不是“模型能不能回答”，而是：

```text
这个输出应该被接受、升级人工复核、修改，还是拒绝？
```

所以这个项目做的是 LLM / Agent 输出的二次复审：

- 把模型输出转成 Markdown / JSON trust report
- 检查证据支撑、政策信号、过度自信、风险标签不一致、缺少人工升级等问题
- 用 52 个 synthetic cases 做基准
- 对比 naive baseline：只要模型自信就接受
- 加入真实常见的 Agent 失败模式，比如“工具失败了，但最终回答声称成功”
- 高风险决策始终保留 human-in-the-loop

当前证据：

- 52 个合成案例
- 8 类风险场景
- naive baseline 在合成集上有 48% false-accept rate
- trust workflow 有 61.5% manual-review routing rate
- 有 CI、CLI 复现步骤和 GitHub Pages demo

项目不是生产级合规引擎，也不使用真实客户/公司数据。它更像是一个公开安全的 AI 复审实验台，用来讨论：AI 输出到底怎样才算“可被信任”。

Repo:
https://github.com/benben951/agent-trust-lab

Live demo:
https://benben951.github.io/agent-trust-lab/

欢迎做 LLM evaluation、Agent reliability、风控、合规 QA、Trust & Safety 的朋友给我提建议。
