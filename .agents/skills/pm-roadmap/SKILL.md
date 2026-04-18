---
name: pm-roadmap
description: Use when building, refreshing, or auditing a product roadmap, opportunity solution tree, story map, or any other relational/spatial strategy artifact that benefits from visual review.
---

# Roadmaps & Visual Strategy Artifacts

## Overview

Miro is the canonical surface for roadmaps, opportunity solution trees (OSTs), story maps,
and journey maps — artifacts whose value is in showing relationships and flow, not in
sequential prose. Markdown is the synthesis layer: a one-page summary that captures the
decisions reached visually.

## When NOT to Use

- The user wants a release plan with specific dates and engineering owners — that is a delivery plan, not a roadmap. Use `spec-kit` instead.
- The artifact is a single-axis priority list — use `pm-prioritization`.
- The roadmap already exists and is current — refresh only if the strategic bets behind it have changed (verify with Ron via `pm-product-strategist`).
- Miro MCP is not configured — do not produce ASCII roadmaps as a workaround; ask the user to configure Miro first.

## Quick Reference

| Artifact | Miro pattern | Markdown synthesis |
|---|---|---|
| Roadmap (now / next / later) | 3-column frame with sticky notes per bet | `docs/product/strategy/roadmap.md` |
| Opportunity Solution Tree | Tree diagram (root = outcome) | `docs/product/strategy/opportunity-tree.md` |
| Story map | 2D grid: activities (x) × detail (y) | Optional — link from PRD |
| Journey map | Horizontal phases with emotion/touchpoint rows | `docs/product/relationships/users/<persona>-journey.md` |

## Required Inputs Before Drafting

1. **An active strategic bet** from `docs/product/strategy/strategic-bets.md`. No bet = no roadmap.
2. **A primary persona** from `docs/product/relationships/users/`. If missing, invoke `pm-personas` first.
3. **A measurable outcome** from `docs/product/strategy/kpis.md`. Roadmaps without an outcome are feature lists.

## Drafting Workflow (Miro-first)

1. **Confirm the Miro board URL** with the user. If none exists, ask before creating.
2. **Use `miro-mcp` `diagram_get_dsl`** to fetch the format spec for the diagram type (flowchart for OST, etc.).
3. **Render the artifact** with `diagram_create` for trees, `table_create` for now/next/later grids, or `doc_create` for narrative captions.
4. **Position on the board** — never default to `(0, 0)`. Allocate explicit `x`/`y` ranges so multiple artifacts do not overlap.
5. **Synthesize to Markdown** — write a one-page summary listing the bets, the ranked opportunities, the candidate solutions, and the outcomes each is measured by. Link the Miro board URL at the top.
6. **Hand off** — for each "now" item, ensure a PRD exists or is queued (via `pm-prd-builder`). For each "later" item, ensure a hypothesis exists (via `pm-hypothesis-builder`).

## Behaviour Rules

- Roadmaps show **bets and outcomes**, not features and dates. If the user asks for dates, push back — those belong in `spec-kit` task lists.
- Every roadmap item must link to a strategic bet ID. Items without a bet are flagged as misaligned.
- Time horizons are **now / next / later**, not Q1/Q2/Q3. Calendar quarters create false precision.
- The Markdown synthesis is the source of truth for what was decided. The Miro board is the source of truth for how it relates.

## Common Mistakes

- **Quarterly Gantt-style roadmaps** — promise dates the team cannot meet; create credibility loss.
- **Feature lists masquerading as roadmaps** — no outcome, no bet, no persona. Just a wishlist.
- **Skipping the Markdown synthesis** — Miro boards alone are not searchable, not version-controlled, and decay fast.
- **Drawing an OST without a measurable outcome at the root** — the tree has nothing to be ranked against.
- **Auto-mirroring every roadmap change to Markdown** — drift. Sync on cadence (after each strategy review), not continuously.

## Render to Miro

Always invoke `miro-mcp` for the rendering. Typical sequence:

1. `context_explore` — confirm the target board's existing structure.
2. `diagram_get_dsl` for the diagram type you need.
3. `diagram_create` (or `table_create` / `doc_create`) with explicit `x`/`y` coordinates.
4. `context_get` on the created item to confirm placement and capture the URL for the Markdown synthesis.
