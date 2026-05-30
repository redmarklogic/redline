---
name: pm-personas
description: Use when defining a customer archetype, GTM segment, or persona — before writing a PRD that names a user, before a strategy session that targets a market, or when an existing persona feels like a stock template rather than a real person.
---

# Personas & Customer Archetypes

## Overview

A persona is a concrete, evidence-backed stand-in for a real user segment. the Product Manager uses personas at the PRD level. the Strategy Advisor uses archetypes at the GTM/strategy level. Both must trace back to evidence — never invented for narrative convenience.

## Boundary Contract

## When NOT to Use

- PRD already cites a persona validated in research within 6 months — reuse, do not duplicate.
- Asking for a buyer/marketing target only — use `pm-product-strategist` for positioning.
- No customer evidence exists — stop and ask the user to gather research before fabricating.

## Quick Reference

| Mode | Owner | Output path |
|---|---|---|
| **Archetype** (segment-level) | the Strategy Advisor | `docs/product/relationships/archetypes/<segment>.md` |
| **Persona** (individual-level) | the Product Manager | `docs/product/relationships/users/<persona>.md` |
| **Co-drafting workshop** | the Product Manager + the Strategy Advisor | Miro board, export to Markdown when stable |

## Required Fields

1. **Name + role + firm context** — e.g., "Sarah, Senior Geotechnical Engineer, mid-tier UK consultancy".
2. **Evidence anchor** — at least 2 cited sources (interview, support ticket, sales call). No anchor = no persona.
3. **Jobs to be done** — top 3 jobs this persona is hiring our product to do.
4. **Pains** — observable, not imagined (cite the source).
5. **Gains** — what success looks like, in their words.
6. **Anti-persona** — who this is explicitly NOT.

## Drafting Workflow

1. **Gather evidence** — query `redline-research`; collect interview notes from `docs/product/resources/`.
2. **Draft on Miro** (optional, recommended for new archetypes) — `doc_create` for narrative, `table_create` for Jobs/Pains/Gains grid.
3. **Synthesize to Markdown** — write canonical version to the path in Quick Reference.
4. **Cross-link** — every PRD naming this persona MUST link back. Every bet targeting this archetype MUST link back.

## Behaviour Rules

- Never invent a name without evidence. Names come from real interviews.
- Pains are observed, not assumed. Quoted sources required.
- One archetype can have multiple personas. Personas without an archetype are red-flagged.
- A persona is stale after 12 months. Revisit before reusing.


See `procedures/pm-personas.md` for detailed rules, examples, and extended reference.

## Common Mistakes

- **Stock-photo personas** — no evidence anchor produces PRDs that flatter but solve nothing.
- **Conflating buyer with user** — the engineer using the tool is not the partner signing the contract.
- **Skipping the anti-persona** — without "who this is NOT", every feature request looks reasonable.
- **Treating persona as segment size** — sizing belongs in GTM, not the persona doc.
