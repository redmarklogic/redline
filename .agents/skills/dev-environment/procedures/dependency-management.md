# Dependency Management Reference

## Dependency Groups

| Group | Contents | Installed by default? |
|---|---|---|
| `dev` | codespell, deptry, import-linter, openpyxl, prek>=0.4.3, pydantic, pypdf, pyproject-fmt, ruff | Yes |
| `test` | pytest, pytest-cov, coverage | Yes |
| `doc` | mkdocs | Yes |
| `ocr` | easyocr, numpy, pypdfium2 | **No — opt-in only** |

Default sync (`uv sync`) installs `dev`, `test`, and `doc`. The `ocr` group is GPU-heavy and never installed unless explicitly requested.

## Commands

```powershell
# Add a package to the dev group
rtk uv add --dev <package>

# Add to a named group
rtk uv add --group test <package>

# Remove a package
rtk uv remove --group dev <package>

# Sync default groups (dev + test + doc)
rtk uv sync

# Include opt-in ocr group
rtk uv sync --group ocr

# Frozen sync (CI/CD — enforce lockfile)
rtk uv sync --frozen

# Inspect dependency tree
rtk uv tree
```

## After Any Dependency Change

1. Run `uv sync` to verify the lockfile resolves cleanly.
2. Run `uv run deptry .` to check for transitive or missing imports.
3. Commit `pyproject.toml` and `uv.lock` together in the same commit.

## Escalation Rules

Stop and escalate to the Principal Engineer before:
- Adding or removing anything from `[project] dependencies` (production deps)
- Creating a new named group in `[dependency-groups]`
- Adding anything to the `ocr` group (GPU/heavy; affects CI cost)
- Upgrading a version the Principal Engineer has explicitly pinned

Do NOT escalate for:
- Adding to `dev`, `test`, or `doc` groups when already approved
- Running `uv sync` after a pull that changes `uv.lock`

## Version Pinning

Never pin exact versions in `pyproject.toml` unless explicitly requested. Use lower-bound only (e.g. `>=2.0.0`). The `uv.lock` lockfile handles reproducibility.
