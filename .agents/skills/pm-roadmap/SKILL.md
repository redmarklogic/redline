---
name: pm-roadmap
description: Use when building, refreshing, or auditing a product roadmap, opportunity solution tree, story map, or any other relational/spatial strategy artifact that benefits from visual review.
---

# Roadmaps & Visual Strategy Artifacts

## Overview

Miro is the canonical surface for roadmaps, opportunity solution trees, story maps, and journey maps — artifacts whose value is in relationships and flow, not sequential prose. Markdown is the synthesis layer: a one-page summary capturing the decisions reached visually.

## When NOT to Use

- User wants a release plan with dates and engineering owners — use `spec-kit`.
- Artifact is a single-axis priority list — use `pm-prioritization`.
- Roadmap exists and is current — refresh only if strategic bets have changed (verify via `pm-product-strategist`).
- Miro MCP not configured — do not produce ASCII roadmaps; ask user to configure Miro first.

## Quick Reference

| Artifact | Miro pattern | Markdown synthesis |
|---|---|---|
| Roadmap (now / next / later) | 3-column frame, sticky notes per bet | `docs/product/strategy/roadmap.md` |
| Opportunity Solution Tree | Tree diagram (root = outcome) | `docs/product/strategy/opportunity-tree.md` |
| Story map | 2D grid: activities (x) x detail (y) | Link from PRD |
| Journey map | Horizontal phases, emotion/touchpoint rows | `docs/product/relationships/users/<persona>-journey.md` |

## Required Inputs

1. **Active strategic bet** from `docs/product/strategy/strategic-bets.md`. No bet = no roadmap.
2. **Primary persona** from `docs/product/relationships/users/`. Missing: invoke `pm-personas`.
3. **Measurable outcome** from `docs/product/strategy/kpis.md`. Without one, it is a feature list.

## Drafting Workflow

1. **Confirm Miro board URL** — if none, ask before creating.
2. **Render** with `miro-mcp`: `diagram_create` for trees, `table_create` for grids. Use explicit `x`/`y` — never default `(0, 0)`.
3. **Synthesize to Markdown** — one page listing bets, ranked opportunities, candidate solutions, measured outcomes. Link Miro board at top.
4. **Hand off** — "now" items: ensure PRD exists (via `pm-prd-builder`). "Later" items: ensure hypothesis exists (via `pm-hypothesis-builder`).

## Behaviour Rules

- Roadmaps show **bets and outcomes**, not features and dates. Dates belong in `spec-kit`.
- Every item must link to a strategic bet ID. Unlinked items are flagged as misaligned.
- Time horizons are **now / next / later**, not Q1/Q2/Q3. Calendar quarters create false precision.
- Markdown is truth for what was decided. Miro is truth for how it relates.

## Common Mistakes

- **Quarterly Gantt roadmaps** — promise dates the team cannot meet; erode credibility.
- **Feature lists as roadmaps** — no outcome, no bet, no persona. Just a wishlist.
- **Skipping Markdown synthesis** — Miro boards are not searchable, not versioned, and decay.
- **OST without measurable root outcome** — tree has nothing to rank against.
- **Auto-mirroring every change** — sync on cadence (after strategy reviews), not continuously.
