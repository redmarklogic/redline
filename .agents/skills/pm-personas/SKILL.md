---
name: pm-personas
description: Use when defining a customer archetype, GTM segment, or persona — before writing a PRD that names a user, before a strategy session that targets a market, or when an existing persona feels like a stock template rather than a real person.
---

# Personas & Customer Archetypes

## Overview

A persona is a concrete, named stand-in for a real user segment. Mark uses personas at the
PRD level (Sarah, the senior engineer at a mid-tier UK consulting firm). Ron uses archetypes
at the GTM/strategy level (mid-tier UK geotechnical consultancies, 50–200 engineers). Both
must trace back to evidence — never invented for narrative convenience.

## When NOT to Use

- The PRD already cites a persona that has been validated in research within the last 6 months — reuse, do not duplicate.
- The user is asking for a buyer/marketing target only — that is a GTM segment definition; load `pm-product-strategist` for positioning instead.
- No customer evidence exists yet — stop and ask the user to gather research (interview notes, support tickets, sales call recordings) before fabricating a persona.

## Quick Reference

| Mode | Owner | Output |
|---|---|---|
| **Archetype** (segment-level) | Ron | `docs/product/relationships/archetypes/<segment>.md` |
| **Persona** (individual-level, used in PRDs) | Mark | `docs/product/relationships/users/<persona>.md` |
| **Co-drafting workshop** | Mark + Ron | Miro board for collaborative shaping; export to Markdown when stable |

## Required Fields

Every persona document must contain:

1. **Name + role + firm context** — e.g., "Sarah, Senior Geotechnical Engineer, mid-tier UK consultancy".
2. **Evidence anchor** — at least 2 cited sources (interview, support ticket, sales call, notebook excerpt). No anchor = no persona.
3. **Jobs to be done** — the top 3 jobs this persona is hiring our product to do.
4. **Pains** — observable, not imagined (cite the source).
5. **Gains** — what success looks like for this persona, in their words.
6. **Anti-persona** — who this is explicitly NOT (prevents scope drift).

## Drafting Workflow

1. **Gather evidence** — query `redline-research` for relevant notebook excerpts; collect interview notes from `docs/product/resources/`.
2. **Draft on Miro** (optional but recommended for new archetypes) — use `miro-mcp` `doc_create` for the narrative, `table_create` for the Jobs/Pains/Gains grid. Co-edit with stakeholders.
3. **Synthesize to Markdown** — once the persona stabilises, write the canonical version to the path in the Quick Reference table.
4. **Cross-link** — every PRD that names this persona MUST link back to the Markdown file. Every strategic bet that targets this archetype MUST link back too.

## Behaviour Rules

- Never invent a name without evidence. "Sarah" must come from a real interview, not from a vibe.
- Pains are observed, not assumed. If the persona doc says "Sarah is frustrated by X", there must be a quoted source.
- One archetype can have multiple personas (e.g., "mid-tier UK consultancy" archetype contains "Sarah the senior engineer" and "James the practice lead"). Personas without an archetype are red-flagged.
- A persona is stale after 12 months. Revisit before reusing in a new PRD.

## Common Mistakes

- **Using stock-photo personas with no evidence anchor** — produces PRDs that flatter the team but solve no real problem.
- **Conflating buyer with user** — the engineer using the tool is not the firm partner who signs the contract. Separate them.
- **Skipping the anti-persona** — without "who this is NOT", every feature request looks reasonable.
- **Drafting in Markdown alone for a new archetype** — you lose the collaborative shaping that Miro enables. Use Miro for new archetypes, Markdown for existing ones.
- **Treating persona = customer segment size** — sizing belongs in GTM, not in the persona doc. Keep them separate.

## Render to Miro

For collaborative archetype workshops, use `miro-mcp`:

1. `doc_create` — narrative summary at the top of a frame.
2. `table_create` with columns "Job", "Pain", "Gain", "Evidence" — the core grid.
3. `diagram_create` (entity_relationship) — for archetype hierarchies (segment → personas).
4. Export back to Markdown when stable; the Markdown file is canonical.
