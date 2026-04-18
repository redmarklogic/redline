---
name: pm-prioritization
description: Use when ranking features, initiatives, opportunities, or strategic bets at the portfolio level using RICE, MoSCoW, Value-Effort, or similar frameworks. Distinct from spec-kit's scenario-level RICE which ranks acceptance scenarios within a single spec.
---

# Portfolio Prioritization

## Overview

Portfolio prioritization ranks **what to build next** across initiatives, bets, or
opportunities. This is product-level work owned by Mark. It is distinct from `spec-kit`'s
RICE scoring, which ranks acceptance scenarios **inside a single spec** for engineering
sequencing. The two skills operate at different altitudes and must not be merged.

## When NOT to Use

- You are inside a single spec ranking acceptance scenarios — use `spec-kit` (which has its own RICE preset).
- The team needs a yes/no decision between two specific options, not a ranking — use `pm-decision-architect`.
- There is no clear strategic outcome to rank against — go back to `pm-product-strategist` and define the outcome first.
- The list has fewer than 4 items — ranking is overkill; just pick.

## Quick Reference

| Framework | Best for | Output |
|---|---|---|
| **RICE** (Reach × Impact × Confidence ÷ Effort) | Comparing 5–20 initiatives with rough quantitative inputs | Ranked table with score |
| **MoSCoW** (Must / Should / Could / Won't) | Scope-cutting a fixed-deadline release | Four buckets |
| **Value vs Effort** (2x2 matrix) | Visual stakeholder review of a small set | Miro 2x2 with quadrant labels |
| **Kano** (Basic / Performance / Delight) | Differentiating must-have from delight features | Three categories with examples |

Choose ONE framework per session. Mixing produces incomparable scores.

## Required Inputs

1. The list of items to rank (initiatives, bets, opportunities — not features inside a spec).
2. The strategic outcome they are being ranked against (from `docs/product/strategy/kpis.md`).
3. The constraint that forces ranking (capacity, deadline, budget).

If any input is missing, stop and ask.

## Workflow

1. **Pick the framework** using the Quick Reference. Justify the choice in one sentence.
2. **Score each item** using framework-specific criteria. Force the user to provide evidence for each score (no gut numbers).
3. **Render the matrix on Miro** for stakeholder review using `miro-mcp` `table_create` (RICE/MoSCoW) or `diagram_create` (Value-Effort 2x2). Markdown alone hides the spread.
4. **Write the final ranking to Markdown** at `docs/product/strategy/prioritization-<date>.md` — the Miro board is the review surface, the Markdown table is the decision record.
5. **Hand off** — top items go to `pm-problem-framer` (if not yet framed) or `pm-prd-builder` (if framed). Bottom items go to a "parking lot" section, not deleted.

## Behaviour Rules

- Every score must cite evidence. RICE Reach = "X users" requires the source of X.
- Confidence (in RICE) is a discount on the other inputs. A "high impact, low confidence" item should rank below a "medium impact, high confidence" item — that is the framework working as intended.
- MoSCoW "Won't" items must be explicitly listed, not omitted. Saying no out loud is half the value.
- The Miro matrix is for the workshop; the Markdown table is for the record. Do not reverse them.
- Re-rank when inputs change (new evidence, new capacity, new deadline). Stale prioritization is worse than no prioritization.

## Common Mistakes

- **Conflating with `spec-kit` RICE** — spec-kit ranks scenarios within ONE spec. This skill ranks initiatives across the portfolio. Same name, different altitude.
- **Mixing frameworks in one session** — RICE scores and MoSCoW buckets cannot be cross-compared.
- **Hiding the "Won't" bucket** — produces shadow backlogs; commitments leak in via the side door.
- **Ranking without a constraint** — without capacity/deadline/budget, every item is "high priority" and ranking is theatre.
- **Skipping the Miro review** — the spread between top and middle items is what stakeholders need to see; a sorted Markdown table flattens it.

## Render to Miro

Use `miro-mcp` for the workshop surface:

1. `table_create` with columns matching the framework (e.g., RICE: Item, Reach, Impact, Confidence, Effort, Score, Evidence).
2. `table_sync_rows` with `key_column` set to the item ID, so re-ranking updates rows in place.
3. For Value-Effort, `diagram_create` (flowchart) with four quadrants and items placed by score.
4. `context_get` to capture the final state for the Markdown synthesis.
