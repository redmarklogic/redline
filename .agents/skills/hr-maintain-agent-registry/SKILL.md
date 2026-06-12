---
name: hr-maintain-agent-registry
description: Use when updating the org chart, agent register, or skills taxonomy to reflect a hire, deprecation, role change, or post-Topology-Sync promoted state.
---

# Maintain Agent Registry

## Overview

The People artifacts (`agent-register.md`, `org-chart.md`, `skills-taxonomy.md`, `skills-gaps.md`) are the single source of truth for the current agent topology. They must reflect reality at the end of every session that changes agent scope, hires, or deprecations. Note the split per ADR-001: `skills-taxonomy.md` holds the category vocabulary and live-skill catalog only; gap, pending, and deprecation state goes to `skills-gaps.md`; ownership lives in `skills-lock.json`.

## Artifacts Owned

| Artifact | Path | Update trigger |
|---|---|---|
| Agent register | `docs/people/agent-register.md` | Any hire, deprecation, or role boundary change |
| Org chart | `docs/people/org-chart.md` | Any hire, deprecation, or reporting line change |
| Skills taxonomy & catalog | `docs/people/skills-taxonomy.md` | Any new, renamed, or retired live skill (catalog row + category) |
| Skills gaps ledger | `docs/people/skills-gaps.md` | Any gap identified, lifecycle state change, or pending action resolved |

## When to Run

- After a new agent is promoted from draft to `.claude/agents/`
- After an agent is deprecated
- After a Topology Sync promotes JD patches
- After any skill split, rename, or deprecation in this feature set

## Boundary Contract

- Registry updates reflect promoted state only — draft JDs do not appear in the register
- All affected People artifacts must be updated in the same session (no partial updates)

## Cross-References

- A Topology Sync must complete before any registry update that reflects a hire or deprecation

## Common Mistakes

| Mistake | Fix |
|---|---|
| Updating the register before the draft JD is promoted | Registry reflects promoted state only — update after user approves and promotes |
| Updating one artifact and not the others | All three People artifacts must be consistent — update all in one session |

See `procedures/refactor.md` for agent refactor and registry procedures.
See `procedures/jd-frontmatter-governance.md` for JD frontmatter rules.
See `procedures/prompt-rewriting-rules.md` for prompt rewriting conventions.
