---
name: pm-prioritization
description: Use when ranking features, initiatives, opportunities, or strategic bets at the portfolio level using RICE, MoSCoW, Value-Effort, or similar frameworks. Distinct from spec-kit's scenario-level RICE which ranks acceptance scenarios within a single spec.
---

# Portfolio Prioritization

## Overview

Rank **what to build next** across initiatives, bets, or opportunities at the portfolio level. Distinct from `spec-kit` RICE, which ranks scenarios inside a single spec. The two operate at different altitudes.

## Boundary Contract

### Inputs
- List of features, initiatives, or opportunities to rank
- Chosen framework ([RICE](../mental-models/strategic_decisions/rice.md), [MoSCoW](../mental-models/strategic_decisions/moscow.md), [Value-Effort](../mental-models/strategic_decisions/value-effort.md), or [Kano](../mental-models/strategic_decisions/kano.md))

### Outputs
- Ranked priority table with scores and rationale

### Out of Scope
- Scenario-level RICE within a single spec (`spec-kit`)
- Product strategy definition (`pm-product-strategist`)
- PRD writing (`pm-prd-builder`)

## When NOT to Use

- Ranking acceptance scenarios inside a spec — use `spec-kit`.
- Yes/no between two options, not a ranking — use `pm-decision-architect`.
- No strategic outcome to rank against — use `pm-product-strategist` first.
- Fewer than 4 items — just pick.

## Quick Reference

| Framework | Best for | Output |
|---|---|---|
| [**RICE**](../mental-models/strategic_decisions/rice.md) | 5-20 initiatives with rough quantitative inputs | Ranked table with score |
| **MoSCoW** (Must / Should / Could / Won't) | Scope-cutting a fixed-deadline release | Four buckets |
| **Value vs Effort** (2x2 matrix) | Visual stakeholder review of a small set | Miro 2x2 |
| **Kano** (Basic / Performance / Delight) | Differentiating must-have from delight | Three categories |

Choose ONE framework per session. Mixing produces incomparable scores.

> Framework definitions: `mental-models/strategic_decisions/rice.md`, `mental-models/strategic_decisions/moscow.md`, `mental-models/strategic_decisions/value-effort.md`, `mental-models/strategic_decisions/kano.md`.

## Required Inputs

1. Items to rank (initiatives, bets, opportunities — not features inside a spec).
2. Strategic outcome they are ranked against (from `docs/product/strategy/kpis.md`).
3. Constraint forcing the ranking (capacity, deadline, budget).

If any input is missing, stop and ask.

## Workflow

1. **Pick framework** using Quick Reference. Justify in one sentence.
2. **Score each item** — force evidence for each score (no gut numbers).
3. **Render on Miro** using `miro-mcp` — `table_create` for RICE/MoSCoW, `diagram_create` for Value-Effort 2x2.
4. **Write final ranking to Markdown** at `docs/product/strategy/prioritization-<date>.md`.
5. **Hand off** — top items to `pm-problem-framer` or `pm-prd-builder`. Bottom items to parking lot.

## Common Mistakes

- **Conflating with spec-kit RICE** — same name, different altitude. This ranks across the portfolio.
- **Mixing frameworks** — RICE scores and MoSCoW buckets cannot be cross-compared.
- **Hiding the "Won't" bucket** — produces shadow backlogs; commitments leak in.
- **Ranking without a constraint** — without capacity/deadline/budget, every item is "high priority."
- **Skipping the Miro review** — a sorted table flattens the spread between items that stakeholders need to see.
