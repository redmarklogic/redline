---
name: python-style
description: General Python style and repo conventions (uv usage, formatting, idioms).
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

## Context & Guidelines

### Scope

Apply whenever you add or refactor Python code under `src/` or tests under `tests/`.

### Dependency Management (uv)

- Use `uv` for package management.
- When adding a dependency, prefer `uv add <package>` so `pyproject.toml` and `uv.lock` stay
  consistent.

### Line Length

- Follow the Ruff configuration in `pyproject.toml` (currently 100 characters).

### General Python Practices

- Never use mutable default arguments.
- Use context managers (`with`) for file/resource management.
- Use `is` for comparing with `None`, `True`, and `False`.
- Prefer f-strings for string formatting.
- Prefer list comprehensions / generator expressions when they improve readability.
- Prefer `enumerate()` over manual counters.

### Constants Organization

- **Module-specific constants**: Define in the module where they are used if they are only used there.
- **Cross-cutting constants** (used by 2+ modules in the same package): Move to `src/<package>/domain/constants.py`.
- **Feature-specific shared constants**: For a multi-agent or multi-component feature (e.g., CrewAI workflows), place shared constants in `src/<package>/<feature>/domain/constants.py`.
- Avoid scattering duplicated constants across modules; centralize when you notice repetition.
- When one layer wraps another (for example, flow/service wrapping a factory), keep default ownership in one module and import those constants in wrappers; do not shadow defaults with `None` sentinels and conditional forwarding.

For the full CrewAI directory layout and conventions, use the `python-crewai` skill.

### Repo Convention: Accessing Package Files

For full path resolution conventions (package files via `importlib.resources`, repo-root
via `repo_`, banned patterns), use the `python-paths` skill.

## Procedure

1. Write clear, readable Python first.
2. Ensure Ruff and formatting rules are satisfied (see linting skill).
3. Keep dependency changes via `uv add` and `uv lock`.

## Refactoring & Maintenance

- **No default backward compatibility**: Unless explicitly instructed, do not maintain backward compatibility with external systems (APIs, legacy files, databases, or external consumers) during refactors or renames.
- **De-clutter immediately**: Delete deprecated shims, old constants, and retired types immediately as part of any refactor. Assume internal consistency is the priority.
