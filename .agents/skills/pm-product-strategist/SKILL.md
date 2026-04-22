---
name: pm-product-strategist
description: Use when starting a new product, refreshing strategy after market shifts, or when the roadmap lacks a strategic thread or OKRs feel disconnected from real customer problems.
---

# Product Strategist

## Overview

Guide PMs through building a complete product strategy top-down: JTBD (the job), OST (the opportunity landscape), then OKR + Strategic Bets (the goals). Each layer must be grounded before moving to the next.

## Boundary Contract

### Inputs
- Market context and existing strategy docs in `docs/product/strategy/`
- Customer evidence and research from `docs/research/`

### Outputs
- `docs/product/strategy/jtbd.md`, `strategic-bets.md`, `kpis.md`, `opportunity-tree.md`

### Out of Scope
- Tactical product work (`pm-problem-framer`, `pm-prd-builder`)
- GTM execution and marketing (`marketing-*` skills)
- Code implementation

## When to Use

- Starting a new product or entering a new market
- Strategy refresh after market or competitive shift
- Roadmap feels like a feature list with no strategic thread
- OKRs feel disconnected from real customer problems

## Quick Reference

| Mode | Trigger | Output |
|---|---|---|
| 1: Job Definition (JTBD) | Strategy files empty or job unclear | `docs/product/strategy/jtbd.md` |
| 2: Opportunity Mapping (OST) | JTBD complete, need opportunity landscape | `docs/product/strategy/opportunity-tree.md` |
| 3: Strategy Synthesis (OKR) | JTBD + OST complete, need goals | `docs/product/strategy/strategic-bets.md` + `kpis.md` |

**Pre-read:** Check `vision.md`, `strategic-bets.md`, `kpis.md`, `jtbd.md` in `docs/product/strategy/`. If all empty, start Mode 1. If populated, start Mode 2 audit.

## Mode 1: Job Definition (JTBD)

1. Gather research signals — query `redline-research` or ask user for raw input.
2. Ground in a persona — invoke `pm-personas`.
3. Write JTBD: "When [situation], [persona] wants to [motivation], so they can [outcome]."
4. Validate against `vision.md` — aligned: proceed. Misaligned: flag gap.

## Mode 2: Opportunity Mapping (OST)

1. Confirm desired outcome from `kpis.md` — this becomes the OST root.
2. Build tree: outcome at root, opportunities as branches, solutions as leaves. Render via `pm-roadmap`.
3. Rank: 4+ opportunities, invoke `pm-prioritization`. Contested ranking, hand off to `pm-decision-architect`.
4. Audit active initiatives against the opportunity map — flag misaligned or missing.

## Mode 3: Strategy Synthesis (OKR + Bets)

1. Define OKRs per top opportunity — link to OST, measurable key result with threshold + time boundary.
2. Update strategic bets — one per selected opportunity, each names OKR + top candidate solutions.
3. Produce strategy brief — core job, ranked opportunities, bets table, gaps, next step.
4. Write to `docs/product/strategy/`.

## Behaviour Rules

- Do not run Mode 2 without a completed JTBD — an OST without a job anchor is a feature list.
- Do not set OKRs before the opportunity map is ranked.
- Every bet must link to an opportunity. A bet with no opportunity is a hope.
- If the PM cannot choose: surface criteria and hand off to `pm-decision-architect`.
- Flag active initiatives that do not map to the opportunity tree.
- Every bet should have a hypothesis (via `pm-hypothesis-builder`).

## Common Mistakes

- **Skipping JTBD** — jumping to OST produces a feature wishlist, not a strategy.
- **Setting OKRs on gut** — OKRs without opportunity backing will not survive the next review.
- **Orphan initiatives** — initiatives with no opportunity link are invisible misalignment.
- **Calendar quarters as time horizons** — now/next/later avoids false precision.
