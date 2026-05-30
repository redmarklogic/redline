---
name: dev-environment
description: Use when bootstrapping or maintaining the development environment for this repo -- uv, tasks, or prek setup
---

# Development Environment

## Boundary Contract

**Inputs:** Repo checkout with `pyproject.toml` and `uv.lock` | **Produces:** Working `.venv`, prek hooks, task runners | **Does Not Cover:** Package management (`python-style`), tool config (`python-usethis`), dependency hygiene (`python-deptry`)

## Canonical Setup

1. Run `tasks\dev_sync.ps1` from the repo root — provisions uv, creates `.venv`, syncs all default dependencies, configures the project.
2. Install hooks: `uv run prek install`
3. Validate: `uv run prek run --all-files`

See `procedures/dependency-management.md` for uv commands, group structure, escalation rules, and version pinning.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Running `pip install` instead of `uv sync` | Use `uv sync`; `pip` bypasses the lockfile |
| Forgetting to activate the virtual environment | Run `.\.venv\Scripts\activate` first, or prefix with `uv run` |
| Editing `pyproject.toml` directly to add a dependency | Use `uv add <package>` so the lockfile updates atomically |