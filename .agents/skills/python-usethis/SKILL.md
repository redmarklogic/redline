---
name: python-usethis
description: Use when adding, removing, or inspecting development tools with the usethis CLI -- pre-commit hooks, pyproject.toml config, or dependencies in this repo
---

# python-usethis

`usethis` is a CLI tool that automates the wiring of development tools into a Python
project. A single command adds the dependency, the `pyproject.toml` configuration block,
and the pre-commit hook for a given tool — replacing the error-prone manual steps of
doing each in isolation.

## Boundary Contract

### Applies To
- Dev tool integration via the `usethis` CLI in this repo

### Produces
- Correctly wired tool configurations in `pyproject.toml` and pre-commit hooks

### Does Not Cover
- Dev environment bootstrap (`dev-environment`)
- Lint rules (`python-linting`)
- Dependency hygiene (`python-deptry`)


See `procedures/python-usethis.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Manually editing pyproject.toml to add a dev tool instead of using usethis | Use usethis tool add <name> — it adds the correct config section and dependencies atomically |
| Running usethis outside the repo root | Always run from the repo root where pyproject.toml lives |
| Using usethis to add a tool that is already configured | Run usethis tool show first to check current status before adding |