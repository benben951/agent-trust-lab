# Agent Review Copilot Architecture

This document describes how Agent Trust Lab should evolve from a synthetic
evaluation demo into a more useful Agent review copilot.

The goal is not to replace the current trust-report workflow. The goal is to
reuse the existing review logic, metrics, and public-safe artifacts as the base
layer of a system that can review agent outputs, extract evidence, apply rules,
and accumulate reusable cases over time.

## Product Direction

Agent Review Copilot should help a human reviewer answer:

> Is this agent output usable, questionable, or unsafe, and what evidence or
> rule pattern explains that judgment?

That means the next version should optimize for:

- reviewing real or semi-real agent outputs, not only synthetic benchmark cases
- extracting structured evidence from outputs, tool traces, and user context
- applying reusable rule packs by domain
- recommending a review route instead of pretending to automate final approval
- storing cases and review outcomes so the system becomes more useful over time

## Why Build On Agent Trust Lab

The current codebase already contains the right base primitives:

- `reviewer.py` provides deterministic finding logic and trust scoring
- `workflow.py` already decomposes review into role-based notes
- `metrics.py` and `baseline.py` already support measurable evaluation artifacts
- `cli.py` already exposes a simple workflow entry point
- `web/` already provides a public review surface

So the right move is not a full rewrite. The right move is:

```text
current trust-report engine
-> add evidence extraction and rule packs
-> add case memory and human review workflow
-> add domain-specific copilot modes
```

## Target Workflow

```text
agent output package
  -> evidence extraction
  -> rule-pack selection
  -> finding detection
  -> review strategy notes
  -> recommendation and human route
  -> case memory writeback
  -> reusable report artifact
```

In a more agentic version:

```text
orchestrator
  -> evidence agent
  -> rule / policy agent
  -> review agent
  -> report agent
  -> case memory
  -> human confirmation loop
```

## Proposed Roles

### 1. Orchestrator

Owns the review run.

Responsibilities:

- validate input package
- call evidence extraction
- select domain rule pack
- collect findings from existing reviewer logic
- build final recommendation
- write report and memory artifact

### 2. Evidence Extractor

Turns messy input into a reviewable bundle.

Inputs may include:

- final agent answer
- tool call results
- trace snippets
- user request
- optional metadata such as model, task, or reviewer tags

Output should be:

- normalized evidence items
- extracted claims
- extracted actions
- trace summary

### 3. Rule / Policy Layer

Encodes reusable checks by scenario.

Examples:

- financial review pack
- agent tool-use review pack
- support compliance review pack
- trust-and-safety review pack

This is where real product value will grow. Over time, repeated reviewer
patterns should be turned into explicit rule packs instead of living only in
prompts or memory.

### 4. Review Engine

Uses existing `evaluate_case`-style logic as the deterministic base layer.

Near term:

- reuse current finding taxonomy
- adapt current `ReviewCase` structure to accept richer input
- keep deterministic scoring as a trust anchor

Later:

- allow domain-specific weights
- allow evidence-quality scoring
- allow disagreement logging between reviewer and engine

### 5. Human Review Layer

Makes the system useful in a real workflow.

Needed outputs:

- why this case was escalated
- what evidence was missing
- what rule triggered
- what the reviewer should check next

The system should help a reviewer move faster, not claim to replace judgment.

### 6. Case Memory

Stores reusable learning.

Memory should be split into:

- review pattern memory
- rule-pack memory
- case outcome history
- reviewer disagreement notes

This matters because a useful copilot gets better from repeated cases, not just
from one-shot prompts.

## Proposed Directory Structure

```text
agent_trust_lab/
  copilot/
    __init__.py
    models.py
    orchestrator.py
    evidence.py
    rulepacks.py
    memory.py
    reports.py
    review_session.py
```

### File Responsibilities

`models.py`

- shared dataclasses for copilot input, evidence bundles, review decisions, and
  memory records

`orchestrator.py`

- top-level review flow controller

`evidence.py`

- converts raw agent output packages into normalized evidence bundles

`rulepacks.py`

- registers domain rule packs and selects them per case

`memory.py`

- stores case summaries, reviewer outcomes, and reusable patterns

`reports.py`

- renders recruiter-safe or operator-safe reports from one review session

`review_session.py`

- session object that links one review run, its artifacts, and final route

## Input Shape

The copilot should accept a richer input shape than the current synthetic case:

```text
task metadata
+ final agent answer
+ optional tool trace
+ optional evidence snippets
+ domain hint
+ reviewer notes
```

This is closer to how real review work happens.

The current scaffold supports both:

- structured JSON input
- lightweight raw text input with sections such as `Case ID:`, `Domain:`,
  `User Request:`, `Final Output:`, `Tool Trace:`, `Evidence:`, and
  `Reviewer Notes:`

## Migration Strategy

### Phase 1

Reuse current engine and add structure.

- keep current reviewer and workflow modules unchanged
- add copilot package skeleton
- define shared models
- add adapter layer from copilot input to existing `ReviewCase`

### Phase 2

Add real review workflow.

- build evidence extraction helpers
- add domain rule packs
- add session-level report rendering
- store case memory locally

### Phase 3

Make it genuinely useful.

- support reviewer feedback writeback
- log disagreement between engine and human
- rank repeated error patterns
- expose operator-oriented review queue views

## What Not To Do

- Do not pretend this is a production compliance engine yet.
- Do not mix too many domains into one fuzzy rule set.
- Do not replace deterministic checks with vague LLM-only scoring.
- Do not optimize for a flashy demo before case-memory and review flow exist.

## Real Value Test

The project becomes real when:

- you would use it to review your own agent-output examples
- it saves time on repeated review patterns
- reviewer feedback changes the rule packs or memory
- the same case history makes the next review better

Until then, it remains a strong prototype, not a proven product.
