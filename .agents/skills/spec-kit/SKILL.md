---
name: spec-kit
description: Use when planning a feature, writing a specification, breaking work into tasks, or executing an implementation plan - wraps GitHub Spec Kit CLI for specification-driven development
---

## Boundary Contract

## When to Use

- Planning a new feature, pipeline, or multi-phase project
- Converting a brainstorm or research doc into structured deliverables
- Breaking an existing plan into executable tasks
- Reviewing specs for completeness before implementation
- Executing a plan task-by-task


See `procedures/spec-kit.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Invoking /speckit.implement directly instead of using Kabilan | Always use Kabilan to execute a tasks.md � he loads Redline conventions that the generic template omits | <!-- hook: allow -->
| Editing vendor-generated spec-kit files manually | All Redline-specific extensions belong in .specify/extensions.yml; manual edits are overwritten by specify upgrade |
| Starting speckit.specify before a shaped Pitch exists | Spec-kit requires a shaped Pitch from Peter; unshaped work enters planning with undefined scope | <!-- hook: allow -->