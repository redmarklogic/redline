# Developer Quick Start (post-migration)

This guide replaces the pre-commit setup instructions.
After migration, `prek` is the sole git hook runner for this project.

## Setup

```powershell
# 1. Install dependencies
rtk uv sync

# 2. Install git hooks
rtk uv run prek install

# 3. Verify all hooks pass
rtk uv run prek run --all-files
```

That's it. Hooks will now fire automatically on every `git commit`.

## Common Commands

| Task | Command |
|---|---|
| Install/reinstall git hooks | `uv run prek install` |
| Run all hooks against all files | `uv run prek run --all-files` |
| Run a specific hook | `uv run prek run <hook-id> --all-files` |
| List configured hooks | `uv run prek list` |
| Preview hooks without running | `uv run prek run --dry-run --all-files` |
| Update hook repo revisions | `uv run prek auto-update` |
| Validate config file | `uv run prek validate-config prek.toml` |
| Remove installed git hooks | `uv run prek uninstall` |

## Writing a New Hook

See `.agents/skills/git-hooks-create/SKILL.md` for the full procedure.

Short version:
1. Create `hooks/<descriptive_name>.py` following the template in the skill
2. Register it in `prek.toml` under the local `[[repos]]` block
3. Test: `uv run prek run <hook-id> --all-files`
4. Lint: `uv run ruff check hooks/<descriptive_name>.py`

## Config File

Hooks are configured in `prek.toml` at the repo root.
prek also accepts `.pre-commit-config.yaml` for compatibility, but this project uses `prek.toml` exclusively.

## Why prek instead of pre-commit?

- Single Rust binary — no Python dependency for the runner itself
- Faster: parallel hook execution by `priority` group
- `priority` support (already used in this project's hook config)
- Native `uv` integration for Python hook environments
- Drop-in compatible: same YAML config format accepted, plus native TOML
