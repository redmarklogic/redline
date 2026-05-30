---
name: pm-product-strategist
description: Use when starting a new product, refreshing strategy after market shifts, or when the roadmap lacks a strategic thread or OKRs feel disconnected from real customer problems.
---

## Boundary Contract

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


See `procedures/pm-product-strategist.md` for detailed rules, examples, and extended reference.

## Common Mistakes

- **Skipping JTBD** — jumping to OST produces a feature wishlist, not a strategy.
- **Setting OKRs on gut** — OKRs without opportunity backing will not survive the next review.
- **Orphan initiatives** — initiatives with no opportunity link are invisible misalignment.
- **Calendar quarters as time horizons** — now/next/later avoids false precision.
