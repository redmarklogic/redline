---
name: python-static-checks
description: Use when running static code checks -- linting, type errors, or pre-commit validation in this repo
---

# Static Checks

## Boundary Contract

### Applies To
- All Python files before finalising any code change

### Produces
- Verified clean output from `uv run prek run -a`

### Does Not Cover
- Individual lint rules (`python-linting`)
- Type hint standards (`python-typing`)
- Test execution (`python-testing-unit`)

## Procedure

To perform static checks on the codebase, run:

```bash
rtk uv run prek run -a
```

Note that we are interested in both errors and warnings from these tools - we should always fix both.

## When to run these checks

Before submitting changes for review, **always** run these static checks. This should be done every time, even for small changes, to avoid slowing down the code review process unnecessarily.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Running static checks only at commit time | Run checks incrementally during development to keep the feedback loop short |
| Fixing type errors with 	ype: ignore without a comment explaining why | Add # type: ignore[<code>] with a note; bare suppression hides real issues silently |
| Skipping static checks before claiming a task is done | Static checks are a mandatory gate before completion — run them every time |