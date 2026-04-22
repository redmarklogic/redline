---
name: python-deptry
description: How deptry enforces dependency hygiene and how to fix its rule violations in this repo.
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

## Context & Guidelines

### Scope

Apply whenever deptry reports a violation, when adding or removing a dependency, or when
moving code between `src/<package>/` (the installable library) and `src/scripts/` or `src/notebooks/`.

### What deptry Does

deptry is a static analysis tool that checks whether the dependencies declared in
`pyproject.toml` match what the code actually imports. It catches:

| Rule   | Description                           | Meaning                                                       |
| ------ | ------------------------------------- | ------------------------------------------------------------- |
| DEP001 | Missing dependency                    | Code imports a package not listed in `[project.dependencies]` |
| DEP002 | Unused dependency                     | A declared dependency is never imported by scanned code       |
| DEP003 | Transitive dependency                 | Code imports a package that is only available transitively    |
| DEP004 | Misplaced dev dependency              | A dev-only package is imported in non-dev (library) code      |
| DEP005 | Standard library listed as dependency | A stdlib module is declared as a project dependency           |

### `uv add` vs `uv add --dev` (package vs dev dependency)

Understanding this distinction is essential for fixing DEP002 and DEP004.

**`uv add <pkg>`** adds to `[project.dependencies]`. These are **runtime** dependencies
that ship with the package when it is installed by end users or deployed. Only list
packages here if code under `src/<package>/` (the installable library) imports them.

**`uv add --dev <pkg>`** adds to `[dependency-groups] dev`. These are **development-only**
dependencies (linters, test runners, notebook tooling, visualisation libraries used only
in scripts/notebooks). They are installed during development (`uv sync`) but are **not**
included when the package is distributed.

**Rule of thumb**:

- If `src/<package>/` imports it → `uv add <pkg>` (runtime).
- If only `src/scripts/`, `src/notebooks/`, `tests/`, or tooling uses it → `uv add --dev <pkg>`.

### Repo Configuration

In `pyproject.toml`:

```toml
[tool.deptry]
extend_exclude = ["src/notebooks", "src/scripts", "src/archive"]
experimental_namespace_package = true
```

- `extend_exclude` tells deptry to skip notebooks, scripts, and archived code. These
  directories use dev dependencies that are intentionally absent from
  `[project.dependencies]`. This is the correct way to prevent false-positive DEP002
  violations — not `per_rule_ignores`.
- `experimental_namespace_package` enables namespace-package detection.

### Banned Configuration

The `[tool.deptry.per_rule_ignores]` table is **banned** in this repo and enforced by the
`ban-toml-fields` pre-commit hook. Never suppress deptry rules — fix the root cause
instead.

### Running deptry

```powershell
uv run deptry src
```

deptry also runs automatically as a pre-commit hook (id: `deptry`).

## Procedure — Fixing Each Rule

### DEP001 — Missing dependency

The package is imported but not declared.

1. Determine whether the import belongs in library code (`src/<package>/`) or dev code
   (`src/scripts/`, `src/notebooks/`, `tests/`).
2. If library code: `uv add <pkg>`.
3. If dev code: `uv add --dev <pkg>`, and confirm the file's directory is listed in
   `extend_exclude`.

### DEP002 — Unused dependency

A declared dependency is never imported by scanned code.

1. Check whether the package is actually used in an excluded directory (scripts,
   notebooks, archive). If so, the dependency likely belongs in `[dependency-groups] dev`,
   not `[project.dependencies]`.
   - Move it: `uv remove <pkg>; uv add --dev <pkg>`.
2. If the package is genuinely unused everywhere, remove it: `uv remove <pkg>`.

### DEP003 — Transitive dependency

Code imports a package that is not a direct dependency (it comes in transitively through
another package).

1. Add it as an explicit dependency: `uv add <pkg>` (or `uv add --dev <pkg>` for dev
   code).

### DEP004 — Misplaced dev dependency

A dev dependency is imported in library code under `src/<package>/`.

1. If the library genuinely needs the package at runtime: `uv remove --dev <pkg>; uv add <pkg>`.
2. If the import is a mistake (e.g., a test helper leaked into library code): remove the
   import and refactor.

### DEP005 — Standard library as dependency

A stdlib module is listed in `[project.dependencies]`.

1. Remove it: `uv remove <pkg>`.

## Pre-commit Hook Enforcement

deptry runs as a pre-commit hook (id: `deptry`). The `ban-toml-fields` hook additionally
prevents re-introduction of `[tool.deptry.per_rule_ignores]`.

## Examples

### Good: Package used only in scripts → dev dependency

```toml
# pyproject.toml
[project]
dependencies = ["pandas>=2.0"]  # pandas is imported in src/<package>/

[dependency-groups]
dev = ["matplotlib>=3.9"]  # matplotlib is only used in src/scripts/
```

### Bad: Suppressing deptry instead of fixing the issue

```toml
# NEVER do this — banned by pre-commit hook
[tool.deptry.per_rule_ignores]
DEP002 = ["matplotlib"]
```
