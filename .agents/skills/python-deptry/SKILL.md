---
name: python-deptry
description: Use when fixing deptry dependency hygiene violations or understanding which deptry rules apply in this repo
---

# Python Dependency Checking (deptry)

This skill explains what deptry does, how it is configured in this repo, and how to
resolve each of its rule violations correctly.

For related topics:

- Adding/removing packages: use the `python-style` skill.
- Dev environment setup: use the `dev-environment` skill.

## Boundary Contract

### Applies To
- Dependency declarations in `pyproject.toml` and imports across all Python files

### Produces
- Clean dependency hygiene with no missing, unused, or misplaced dependencies

### Does Not Cover
- Package management commands (`python-style`)
- Dev environment bootstrap (`dev-environment`)
- Lint rules (`python-linting`)

## Procedure — Fixing Each Rule

# pyproject.toml
[project]
dependencies = ["pandas>=2.0"]  # pandas is imported in src/<package>/

[dependency-groups]
dev = ["matplotlib>=3.9"]  # matplotlib is only used in src/scripts/
```

# NEVER do this — banned by pre-commit hook
[tool.deptry.per_rule_ignores]
DEP002 = ["matplotlib"]
```


See `procedures/python-deptry.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Adding a # noqa: DEP003 suppression without checking if the import is actually needed | Remove the import first; only suppress if the dependency is truly required but indirect |
| Declaring a package in both dependencies and dev-dependencies | Keep it in one group only; deptry flags this as a duplicate |
| Ignoring deptry output because "it worked before" | Stale dependencies create install-time failures in CI � fix all violations before merging |