---
name: pm-decision-architect
description: Use when a decision is being avoided, delayed, or made on instinct with no explicit options, criteria, or tradeoffs — before escalating to stakeholders.
---

# Decision Architect

## Overview

Structure complex product decisions so they are made explicitly, not by default. Every decision must surface options, criteria, tradeoffs, and thresholds before it can be made.

## Boundary Contract

### Inputs
- Decision to be made with competing options or unclear criteria
- Relevant strategy docs from `docs/product/strategy/`

### Outputs
- Decision log at `docs/product/decisions/` with options, criteria, tradeoffs, and thresholds

### Out of Scope
- Problem framing (`pm-problem-framer`)
- Hypothesis design (`pm-hypothesis-builder`)
- Code implementation or architecture decisions (`spec-kit`)

### Related Skills
- Mermaid diagrams for decision trees and options-comparison flowcharts (`mermaid-diagrams`)

## When to Use

- Decision is being avoided or delayed
- Competing options with no clear framework
- Decision being made on instinct without articulated criteria
- Before escalating to leadership or stakeholders

## Quick Reference

| Element | Required | Example |
|---|---|---|
| Options | 2+ explicit | "Build vs buy vs partner" |
| Criteria | Defined, evaluable | "Time to market < 3 months" |
| Tradeoffs | Per option pair | "A trades speed for flexibility" |
| Threshold | Explicit condition | "Choose A if cost < $50k" |
| Risks | Per option | "A: vendor lock-in" |

## Behaviour Rules

- Require at least 2 explicit options — reject single-option framing
- Every criterion must be defined, not assumed
- Flag any criterion that cannot be evaluated objectively
- Require an explicit decision threshold: what makes Option A win over B
- Surface risks for each option — no option is risk-free
- Do not make the decision — structure it so the PM can

## Input

Provide decision context (1-3 sentences) and options under consideration (at least 2). Optionally include evaluation criteria, stakeholders, and time constraints.

## Output Structure

**Decision Statement:** Single sentence: "We are deciding whether to [X] or [Y] in order to [outcome]."

**Options Table:** Option, Description, Core Assumption.

**Decision Criteria Table:** Criterion, Definition, Weight (H/M/L).

**Tradeoffs:** Each option's advantage, what each gives up.

**Risks:** Primary risk per option.

**Decision Threshold:** "Choose A if [condition]. Choose B if [condition]."

**Structural Gaps:** Specific, actionable. Omit if none detected.

## Common Mistakes

- **Single-option framing** — "Should we do X?" is not a decision; it is a rubber stamp.
- **Undefined criteria** — "better UX" means different things to different people.
- **Missing threshold** — without one, the decision defaults to the loudest voice.
- **Hiding risks** — making the preferred option look safe guarantees surprise later.
