---
name: hr-hire-agent
description: Use when hiring a new agent — identifying skill gaps that justify a new hire, drafting a job description, onboarding the new agent, or refreshing a single agent's JD for detected drift.
---

# Hire Agent

## Overview

New agents exist only when justified by strategy and cognitive load. Before any hire, the gap must be mapped to a skill that no existing agent owns. The JD is derived from that skill gap — never written in isolation.

## Modes

| Mode | Trigger | Output |
|---|---|---|
| HIRE | A skill gap cannot be absorbed by an existing agent | Draft JD + onboarding checklist |
| REFRESH | A single agent's JD has drifted from current strategy or ADRs | Targeted JD patch |

## When NOT to Hire

- Single-function silos ("we need an agent just for X")
- Reactive hires without a strategy anchor
- "Nice to have" roles with no orphaned responsibility

## Boundary Contract

- Gap identification precedes JD drafting — always
- All new JD files go to `docs/people/drafts/agents/` first (draft-first constraint)
- Topology Sync must run before finalising any new hire

## Cross-References

- Run `hr-maintain-agent-registry` after a hire is approved to update org chart

## Common Mistakes

| Mistake | Fix |
|---|---|
| Writing a JD before identifying the skill gap | Map the gap to an existing or new skill first; the JD is derived from skills, not written in isolation |
| Finalising a new hire without running a Topology Sync | Run a Topology Sync before promoting the draft JD — topology changes affect routing for all agents |

See `procedures/hire.md` for the full HIRE workflow.
See `procedures/refresh.md` for the REFRESH workflow.
See `procedures/session-start-staleness-check.md` for the session-start staleness check.
