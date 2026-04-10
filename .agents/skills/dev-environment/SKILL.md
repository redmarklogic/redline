---
name: dev-environment
description: How to bootstrap and maintain the development environment for this repo (uv, tasks, pre-commit).
---

# Development Environment

This skill describes how to set up and maintain a working dev environment for this repo.

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

### Pre-commit Hooks

This repo uses `pre-commit`.

- Install hooks with: `uv run pre-commit install`.
- Run all checks with: `uv run pre-commit run --all-files`.

## Procedure

1. From the repo root, run `tasks\dev_sync.ps1`.
2. If pre-commit hooks are not installed, run `uv run pre-commit install`.
3. Validate with `uv run pre-commit run --all-files` and a focused test run.
