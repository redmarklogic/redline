# Research: Migrate from pre-commit to prek

**Phase 0 — All NEEDS CLARIFICATION resolved**

## prek Compatibility with this Project's Hooks

### Decision
All hooks in `.pre-commit-config.yaml` are fully compatible with prek.

### Evidence

| Language | Hooks in config | prek support |
|---|---|---|
| `system` | all local hooks (deptry, import-linter, all `hooks/*.py`) | Full — prek runs `entry` directly in system PATH/venv |
| `python` | ruff, ruff-format, codespell, validate-pyproject, pyproject-fmt, ensure-dunder-all | Full |
| `fail` | forbidden-copier-rej-files, forbidden-testpy-files, forbidden-ipynb-files | Full |
| `node` | none | N/A |

Source: prek languages.md (fetched 2026-05-27) — all four languages above are listed as fully supported.

### prek-only Features Already in Use

The existing `.pre-commit-config.yaml` already uses `priority` at the hook level — a prek-only
extension. This confirms the project was already targeting prek semantics before formal migration.

---

## Command Mapping: pre-commit → prek

| pre-commit command | prek equivalent | Notes |
|---|---|---|
| `pre-commit install` | `prek install` | Identical behaviour |
| `pre-commit run --all-files` | `prek run --all-files` | prek alias: `-a` |
| `pre-commit run <id> --all-files` | `prek run <id> --all-files` | Identical |
| `pre-commit run -a` | `prek run -a` | Identical short form |
| `pre-commit autoupdate` | `prek auto-update` | Preferred spelling; `autoupdate` is a compatibility alias |
| `pre-commit clean` | `prek cache clean` | Reorganised under `prek cache` |
| `pre-commit gc` | `prek cache gc` | Reorganised under `prek cache` |
| `pre-commit uninstall` | `prek uninstall` | Identical |

Source: prek compatibility.md (fetched 2026-05-27).

---

## pre-commit-update Replacement

### Decision
`pre-commit-update` (Python package for auto-updating hook revisions) is superseded by `prek auto-update`.

### Rationale
- `prek auto-update` updates all repos to latest revisions with `--dry-run`, `--exit-code`, and `--cooldown-days` support
- No separate package needed — it is built into prek
- `pre-commit-update` has no functionality that `prek auto-update` does not cover

---

## Config Format: YAML vs TOML

### Decision
Migrate to `prek.toml` (P3). Use `prek util yaml-to-toml` for conversion.

### Rationale
- `prek.toml` is the native format; YAML comments not preserved but hook logic is
- prek precedence: `prek.toml` > `.pre-commit-config.yaml` (so both can coexist during transition)
- Once `prek.toml` is verified, deleting `.pre-commit-config.yaml` leaves no ambiguity
- `ci.autofix_prs: false` top-level key (pre-commit-ci specific) — prek ignores unknown top-level keys; safe to remove from TOML

### TOML Hook Registration Pattern

YAML (current):
```yaml
- repo: local
  hooks:
    - id: my-hook
      name: My hook
      entry: uv run hooks/my_hook.py
      language: system
      always_run: true
      pass_filenames: false
      priority: 1
```

TOML equivalent (prek.toml):
```toml
[[repos]]
repo = "local"

[[repos.hooks]]
id = "my-hook"
name = "My hook"
entry = "uv run hooks/my_hook.py"
language = "system"
always_run = true
pass_filenames = false
priority = 1
```

---

## Complete Pre-commit Reference Inventory

Files requiring **active CLI instruction changes** (actionable commands):

| File | Change required |
|---|---|
| `.agents/skills/dev-environment/SKILL.md` | `pre-commit install` / `pre-commit run` → prek |
| `.agents/skills/version-control/SKILL.md` | `pre-commit run --all-files` → prek |
| `.agents/skills/python-module-structure/SKILL.md` | `pre-commit run -a` → prek |
| `.agents/skills/pre-commit-hooks-create/SKILL.md` | commands + config refs + skill name |

Files requiring **naming/branding changes** (no CLI change but "pre-commit" as tool name):

| File | Change required |
|---|---|
| `AGENTS.md` | skill name `pre-commit-hooks-create` → `git-hooks-create`; descriptions |
| `docs/people/skills-taxonomy.md` | same as AGENTS.md |
| `.github/agents/rl.kabilan.agent.md` | skill name + "pre-commit hooks" → "git hooks" |
| `skills-lock.json` | key rename |
| `.agents/skills/pre-commit-hooks-create/` | directory rename |

Files requiring **docstring updates** (hooks/*.py):

All 11 hook scripts whose docstring starts with `"""Pre-commit hook` — change to `"""Git hook`.

Files requiring **config reference updates** (P3 only):

| File | Change required |
|---|---|
| `.pre-commit-config.yaml` | DELETED |
| `prek.toml` | NEW |
| `.agents/skills/git-hooks-create/SKILL.md` | `.pre-commit-config.yaml` → `prek.toml` |
| `docs/people/drafts/skills/customization-mechanism-triage/SKILL.md` | config file refs |

Files that use "pre-commit" only as a **generic git concept** (no change needed):

- `docs/research/**/*.md` — research documents use "pre-commit" to mean "before a commit" — acceptable
- `docs/people/drafts/skills/version-control-pr-discipline-patch.md` — draft; will be superseded
- `.agents/skills/resolving-pr-issues/SKILL.md` — "pre-commit hook" as generic git term + community hook catalog link; update link to prek docs if desired (low priority)
- `docs/people/drafts/skills/python-domain-modeling-layer-arch-patch.md` — "at pre-commit time" = "before commit" — acceptable generic usage
