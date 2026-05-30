---
name: writing-plans
description: SUPERSEDED — use speckit.plan + speckit.tasks instead. This stub overrides the upstream Superpowers vendor skill to prevent conflicts with Spec-Kit's artifact pipeline.
---

## Boundary Contract

This skill is superseded in Redline by Spec-Kit's planning pipeline.

**Do not use `writing-plans`.** Use the following instead:

1. `/speckit.plan` — produces the high-level architecture plan with constitutional gates, data models, and API contracts
2. `/speckit.tasks` — derives an executable `tasks.md` from the plan with `[P]` parallelism markers

`specs/NNN/tasks.md` is the single source of truth for all implementation work.
