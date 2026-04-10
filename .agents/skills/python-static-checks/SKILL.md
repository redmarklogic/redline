---
name: python-static-checks
description: Perform static code checks
---

# Static Checks

## Procedure

To perform static checks on the codebase, run:

```bash
uv run pre-commit run -a
```

Note that we are interested in both errors and warnings from these tools - we should always fix both.

## When to run these checks

Before submitting changes for review, **always** run these static checks. This should be done every time, even for small changes, to avoid slowing down the code review process unnecessarily.
