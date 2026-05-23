# Patch: dev-environment skill — Dependency Groups

> DRAFT — pending user approval. Do not promote to production.

**Target file:** `.agents/skills/dev-environment/SKILL.md`
**Session:** 2026-05-23 Topology Sync — Kabilan hire skill gaps
**Grounded by:** Peter (uv docs via Context7 `/websites/astral_sh_uv`, `pyproject.toml`)
**Drafted by:** Harriet
**Gap addressed:** Dependency management guidance — how to add/remove to named groups,
which groups exist, when to escalate, and how to confirm state.

---

## Changes

### 1. Replace the "Dependency Management" section

Replace the current "Dependency Management" section with the expanded version below.

---

**Current content:**

```markdown
## Dependency Management

- Dependencies are declared in `pyproject.toml` and locked via `uv.lock`.
- Adding, removing, or upgrading a dependency changes the project's public contract. Escalate to Peter before modifying `pyproject.toml` dependencies.
- Use `uv add <package>` to add a dependency and `uv remove <package>` to remove one. Both update `pyproject.toml` and `uv.lock` atomically.
- After any dependency change, run `uv sync` and then `uv run deptry .` to verify no transitive or missing imports were introduced.
- Never pin exact versions in `pyproject.toml` unless Peter explicitly requests it; the lockfile handles reproducibility.
```

**Replace with:**

```markdown
## Dependency Management

### How dependencies are organised

This repo uses `uv` dependency groups. Dependencies in `[dependency-groups]` are
development-time only and never published in package metadata. Four groups exist:

| Group | Contents | Installed by default? |
|---|---|---|
| `dev` | ruff, deptry, pre-commit, pydantic, openpyxl, pypdf, import-linter | Yes |
| `test` | pytest, pytest-cov, coverage | Yes |
| `doc` | mkdocs | Yes |
| `ocr` | easyocr, numpy, pypdfium2 | **No — opt-in only** |

Default sync (`uv sync`) installs `dev`, `test`, and `doc`. The `ocr` group is heavy
(GPU dependencies) and is never installed unless explicitly requested.

### Commands

```powershell
# Add a package to the dev group
uv add --group dev <package>

# Add a package to a named group (--dev is shorthand for --group dev)
uv add --group test <package>

# Remove a package
uv remove <package>                  # from project dependencies
uv remove --group dev <package>      # from a specific group

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

Stop and escalate to Peter before:
- Adding or removing anything from `[project] dependencies` (production deps — currently empty)
- Creating a new named group in `[dependency-groups]`
- Adding anything to the `ocr` group (GPU/heavy; affects CI cost and container size)
- Upgrading a pinned version that Peter explicitly requested

Do NOT escalate for:
- Adding to `dev`, `test`, or `doc` groups when Peter has already approved the package
- Running `uv sync` after a pull that changes `uv.lock`

### After any change

1. Run `uv sync` to verify the lockfile resolves cleanly.
2. Run `uv run deptry .` to verify no transitive or missing imports were introduced.
3. Commit `pyproject.toml` and `uv.lock` together in the same commit.
   Never commit one without the other.

### Version pinning

Never pin exact versions in `pyproject.toml` unless Peter explicitly requests it.
The `uv.lock` lockfile handles reproducibility. Version constraints in `pyproject.toml`
should be lower-bound only (e.g. `>=2.0.0`), not upper-bound unless there is a known
incompatibility.
```
