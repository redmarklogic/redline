---
name: dev-environment
description: How to bootstrap and maintain the development environment for this repo (uv, tasks, prek).
---

# Development Environment

This skill describes how to set up and maintain a working dev environment for this repo.

## Boundary Contract

### Inputs
- Repository checkout with `pyproject.toml` and `uv.lock`

### Outputs
- Working development environment with `uv sync`, prek hooks, and task runners

### Out of Scope
- Package management commands (`python-style`)
- Tool configuration details (`python-usethis`)
- Dependency hygiene checks (`python-deptry`)

## Context & Guidelines

### Scope

Apply when setting up a new machine, repairing a broken environment, or advising contributors.

### Canonical Setup Path

Prefer the repo task scripts over ad-hoc commands.

- Primary: run `tasks\dev_sync.ps1` from the repo root.
  - This provisions `uv`, creates/repairs `.venv`, syncs dependencies, and configures the project.

### Installing `uv`

This repo uses `uv` for dependency management.

- Windows (PowerShell): prefer the repo's automation via `tasks\dev_sync.ps1`.
- Linux/macOS (shell): prefer the repo's automation where available; otherwise install `uv` per the
  official installer.

### Syncing Dependencies

- Use `uv sync` to reproduce the environment from `pyproject.toml` and `uv.lock`.
- In CI-like contexts, use `uv sync --frozen` to ensure the lockfile is respected.

### Git Hooks

This repo uses `prek`.

- Install hooks with: `uv run prek install`.
- Run all checks with: `uv run prek run --all-files`.

## Dependency Management

### How dependencies are organised

This repo uses `uv` dependency groups. Dependencies in `[dependency-groups]` are
development-time only and never published in package metadata. Four groups exist:

| Group | Contents | Installed by default? |
|---|---|---|
| `dev` | codespell, deptry, import-linter, openpyxl, prek>=0.4.3, pydantic, pypdf, pyproject-fmt, ruff | Yes |
| `test` | pytest, pytest-cov, coverage | Yes |
| `doc` | mkdocs | Yes |
| `ocr` | easyocr, numpy, pypdfium2 | **No — opt-in only** |

Default sync (`uv sync`) installs `dev`, `test`, and `doc`. The `ocr` group is heavy
(GPU dependencies) and is never installed unless explicitly requested.

### Commands

```powershell
# Add a package to the dev group (--dev is shorthand for --group dev)
uv add --dev <package>

# Add a package to a named group
uv add --group test <package>

# Remove a package (specify group if it's not in project dependencies)
uv remove <package>
uv remove --group dev <package>

# Sync the default groups (dev + test + doc)
uv sync

# Sync and include the opt-in ocr group
uv sync --group ocr

# Frozen sync — enforce lockfile without updating (CI/CD use)
uv sync --frozen

# Inspect the installed dependency tree
uv tree
```

### Escalation rules

Stop and escalate to the Principal Engineer before:
- Adding or removing anything from `[project] dependencies` (production deps — currently empty)
- Creating a new named group in `[dependency-groups]`
- Adding anything to the `ocr` group (GPU/heavy; affects CI cost and container size)
- Upgrading a version that the Principal Engineer has explicitly pinned

Do NOT escalate for:
- Adding to `dev`, `test`, or `doc` groups when the Principal Engineer has already approved the package
- Running `uv sync` after a pull that changes `uv.lock`

### After any change

1. Run `uv sync` to verify the lockfile resolves cleanly.
2. Run `uv run deptry .` to verify no transitive or missing imports were introduced.
3. Commit `pyproject.toml` and `uv.lock` together in the same commit. Never commit one without the other.

### Version pinning

Never pin exact versions in `pyproject.toml` unless the Principal Engineer explicitly requests it.
The `uv.lock` lockfile handles reproducibility. Version constraints should be lower-bound
only (e.g. `>=2.0.0`), not upper-bound unless there is a known incompatibility.

## Procedure

1. From the repo root, run `tasks\dev_sync.ps1`.
2. If prek hooks are not installed, run `uv run prek install`.
3. Validate with `uv run prek run --all-files` and a focused test run.
