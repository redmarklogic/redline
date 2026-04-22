---
name: python-usethis
description: When and how to use the usethis CLI to add, remove, and inspect development tools (pre-commit hooks, pyproject.toml config, dependencies) in this repo.
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

## Context & Guidelines

### Scope

Apply this skill when:

- Adding or removing a development tool (formatter, linter, test runner, etc.) to/from
  the repo.
- Checking which tools are currently active.
- Generating a dry-run summary of what a tool addition would do before committing to it.

### Invocation pattern

Always use `uvx` so that `usethis` runs in an isolated environment and does not need to
be declared as a project dependency:

```powershell
uvx usethis tool <tool-name>
```

Do **not** install `usethis` into the project venv or declare it in `pyproject.toml`.

### Available tools

| Tool name       | What it wires up                                                |
| --------------- | --------------------------------------------------------------- |
| `pyproject-fmt` | Canonical formatting for `pyproject.toml`; adds pre-commit hook |
| `ruff`          | Ruff linter and/or formatter; adds pre-commit hook              |
| `deptry`        | Dependency hygiene linter; adds pre-commit hook                 |
| `pre-commit`    | Installs the pre-commit framework itself                        |
| `pytest`        | Pytest test runner; adds `[tool.pytest.ini_options]` config     |
| `codespell`     | Spell checker; adds pre-commit hook                             |
| `coverage`      | Coverage.py; adds `[tool.coverage]` config                      |
| `mkdocs`        | Documentation site generator                                    |

### Options

| Flag        | Effect                                                      |
| ----------- | ----------------------------------------------------------- |
| `--remove`  | Undoes the tool addition (removes dependency, config, hook) |
| `--how`     | Prints what the command _would_ do; makes no changes        |
| `--frozen`  | Skips updating the lockfile and venv (useful in CI)         |
| `--offline` | Uses cached packages only; disables network access          |
| `--quiet`   | Suppresses informational output                             |

## Procedure

### Adding a tool

1. Run `uvx usethis tool <tool-name>` from the repo root.
2. Review the printed `✔` (automated) and `☐` (manual) action summary.
3. Run the tool once to normalize any existing files (e.g., `uv run pyproject-fmt pyproject.toml`).
4. Commit `pyproject.toml`, `uv.lock`, and `.pre-commit-config.yaml` together.

### Removing a tool

```powershell
uvx usethis tool <tool-name> --remove
```

### Inspecting tool status

```powershell
uvx usethis list
```

Prints a table of all tools `usethis` knows about and whether each is currently active in
the project.

### Dry run before committing

```powershell
uvx usethis tool <tool-name> --how
```

Prints a human-readable description of every change that would be made, without touching
any file.

## Examples

### Add pyproject-fmt

```powershell
uvx usethis tool pyproject-fmt
uv run pyproject-fmt pyproject.toml   # normalize existing file
```

### Remove deptry

```powershell
uvx usethis tool deptry --remove
```

### Check what adding ruff would do

```powershell
uvx usethis tool ruff --how
```

## References

- [usethis-python documentation](https://usethis.readthedocs.io/)
- [pyproject-fmt documentation](https://pyproject-fmt.readthedocs.io/)
