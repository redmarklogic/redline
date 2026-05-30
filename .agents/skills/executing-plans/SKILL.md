---
name: executing-plans
description: SUPERSEDED — use subagent-driven-development reading specs/NNN/tasks.md instead. This stub overrides the upstream Superpowers vendor skill to prevent conflicts with Spec-Kit's artifact pipeline.
---

## Boundary Contract

This skill is superseded in Redline by `subagent-driven-development` reading from Spec-Kit's task list.

**Do not use `executing-plans`.** Use the following instead:

1. Ensure `specs/NNN/tasks.md` exists (produced by `/speckit.tasks`)
2. Invoke `subagent-driven-development` with `specs/NNN/tasks.md` as input

`subagent-driven-development` provides two-stage review per task (spec compliance → code quality) and subagent isolation that `executing-plans` does not.
