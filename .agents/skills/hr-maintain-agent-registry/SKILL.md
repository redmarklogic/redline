---
name: hr-maintain-agent-registry
description: Use when updating the org chart, agent register, or skills taxonomy to reflect a hire, deprecation, role change, or post-Topology-Sync promoted state.
---

# Maintain Agent Registry

## Overview

The People artifacts (`agent-register.md`, `org-chart.md`, `skills-taxonomy.md`) are the single source of truth for the current agent topology. They must reflect reality at the end of every session that changes agent scope, hires, or deprecations.

## Artifacts Owned

| Artifact | Path | Update trigger |
|---|---|---|
| Agent register | `docs/people/agent-register.md` | Any hire, deprecation, or role boundary change |
| Org chart | `docs/people/org-chart.md` | Any hire, deprecation, or reporting line change |
| Skills taxonomy | `docs/people/skills-taxonomy.md` | Any new, deprecated, or reassigned skill |

## When to Run

- After a new agent is promoted from draft to `.claude/agents/`
- After an agent is deprecated
- After a Topology Sync promotes JD patches
- After any skill split, rename, or deprecation in this feature set

## Boundary Contract

- Registry updates reflect promoted state only — draft JDs do not appear in the register
- All three People artifacts must be updated in the same session (no partial updates)

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
