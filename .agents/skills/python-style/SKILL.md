---
name: python-style
description: Use when applying Python style conventions in this repo -- uv usage, formatting rules, or idiomatic Python patterns
---

# Python Style

This skill defines general Python coding conventions for this repo.

For related topics:

- Lint rules and suppressions: use the `python-linting` skill.
- Type hints: use the `python-typing` skill.
- Error handling: use the `python-error-handling` skill.
- Function design: use the `python-function-design` skill.
- Docstrings: use the `python-documentation` skill.

## Boundary Contract

### Applies To
- All Python modules under `src/` and test files under `tests/`

### Produces
- Code conforming to repo formatting, naming, constant-organisation, and import conventions

### Does Not Cover
- Lint rule enforcement and suppressions (`python-linting`)
- Type annotations (`python-typing`)
- Error handling patterns (`python-error-handling`)
- Function decomposition and signatures (`python-function-design`)
- Docstring format and content (`python-documentation`)

## Refactoring & Maintenance

- **No default backward compatibility**: Unless explicitly instructed, do not maintain backward compatibility with external systems (APIs, legacy files, databases, or external consumers) during refactors or renames.
- **De-clutter immediately**: Delete deprecated shims, old constants, and retired types immediately as part of any refactor. Assume internal consistency is the priority.


See `procedures/python-style.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using && to chain commands in a PowerShell terminal | Use ; to chain commands on Windows; && is not supported in PowerShell |
| Running pip install instead of uv add | Always use uv for package management in this repo; pip bypasses the lockfile |
| Using tabs for indentation | Always use spaces (4-space indent); tabs cause TabError in mixed codebases |