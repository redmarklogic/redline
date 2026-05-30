---
name: python-static-checks
description: Perform static code checks
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
uv run prek run -a
```

Note that we are interested in both errors and warnings from these tools - we should always fix both.

## When to run these checks

Before submitting changes for review, **always** run these static checks. This should be done every time, even for small changes, to avoid slowing down the code review process unnecessarily.
