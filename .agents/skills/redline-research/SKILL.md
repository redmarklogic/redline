---
name: redline-research
description: Use when asked to "research", "investigate", "look up", or "find out" something in the Redline knowledge base — before any online search.
---
# Redline Research

Queries multiple NotebookLM knowledge bases with iterative cross-referencing and writes a
cited research document to `docs/research/YYYYMMDD-<topic>.md`.

**REQUIRED SUB-SKILL:** Use `notebooklm-mcp` to confirm authentication before querying any notebook.

## When to Use

- User asks to "research", "investigate", "look up", or "find out" something in the Redline knowledge base.

## When NOT to Use

- The answer is clearly in project docs (`docs/architecture/`, `docs/concepts/`) — read those first without querying notebooks.
- The question requires real-time or current-events data (knowledge bases are static).
- The user explicitly says "search online" or "look it up on the web" — use web search instead.

## Quick Reference — Notebooks by Topic

| Topic area | Notebooks |
|---|---|
| Engineering theory & standards | Engineering Standards, Ground Engineering Magazine |
| Geotechnical domain | GBR, Geotechnical Report Workflows, Risk Assessment in Engineering |
| AI & software architecture | AI System Engineering, Software Architecture & DDD |
| Process & product | BPM, Product Roadmapping, Writing Specs, Information Architecture & KM |
| Communication & documentation | Engineers' Guide to Technical Communication |
| Founder strategy _(Advisory Board only)_ | Redline Founder Memos |

**Advisory Board only** notebooks: skip entirely unless the user's session context explicitly
identifies them as an advisory board member. Do not mention skipped notebooks.

## Key Constraints

- **NEVER** use online search unless the user explicitly requests it with "search online" or "look it up on the web".
- Always read `docs/architecture/` before formulating notebook queries.
- Never overwrite an existing `docs/research/` file without asking.
- **Advisory Board only** notebooks: skip unless the session context identifies the user as advisory board.

For notebook URLs, project context files, the full query procedure (Steps 1–8), output
template, naming rules, and anti-patterns, see [PROCEDURE.md](PROCEDURE.md).


