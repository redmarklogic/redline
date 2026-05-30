# Change Manifest: Migrate from pre-commit to prek

**Phase 1 design artifact** — Complete mapping of every file change required.

## Notation

- `EDIT` — modify existing file
- `DELETE` — remove file
- `NEW` — create new file
- `RENAME` — rename file or directory

---

## P1 — Dependency Changes

### `pyproject.toml` — EDIT

```diff
 [dependency-groups]
 dev = [
   "codespell>=2.4.2",
   "deptry>=0.25.1",
   "import-linter>=2.11",
   "openpyxl>=3.1.5",
-  "pre-commit>=4.2.0",
-  "pre-commit-update>=0.8.0",
-  "prek>=0.3.8",
+  "prek>=0.4.3",
   "pydantic>=2.13.3",
   "pypdf>=6.10.2",
   "pyproject-fmt>=2.21.0",
   "ruff>=0.15.8",
 ]
```

### `uv.lock` — EDIT (auto via `uv sync --upgrade-package prek`)

Removed entries: `pre-commit`, `pre-commit-update` and all their transitive-only dependencies.
Updated entry: `prek` bumped to latest (≥0.4.3).

---

## P2 — Skill and Documentation Changes

### `.agents/skills/dev-environment/SKILL.md` — EDIT

| Location | Before | After |
|---|---|---|
| YAML description | `"...dev environment for this repo (uv, tasks, pre-commit)."` | `"...dev environment for this repo (uv, tasks, prek)."` |
| Produces bullet | `"pre-commit hooks"` | `"prek hooks"` |
| Section heading | `### Pre-commit Hooks` | `### Git Hooks` |
| Description line | `This repo uses \`pre-commit\`.` | `This repo uses \`prek\`.` |
| Install command | `uv run pre-commit install` | `uv run prek install` |
| Run command | `uv run pre-commit run --all-files` | `uv run prek run --all-files` |
| Dev deps table `dev` row | `..., pre-commit, pre-commit-update, prek, ...` | `..., prek, ...` |
| Troubleshooting step 2 | `uv run pre-commit install` | `uv run prek install` |
| Troubleshooting step 3 | `uv run pre-commit run --all-files` | `uv run prek run --all-files` |

### `.agents/skills/version-control/SKILL.md` — EDIT

| Location | Before | After |
|---|---|---|
| YAML description | `"...pre-commit, and pre-push checks."` | `"...prek hooks, and pre-push checks."` |
| Applies To | `pre-commit, and pre-push checks` | `prek hooks, and pre-push checks` |
| Before Pushing | `Run pre-commit checks (use the \`dev-environment\` skill).` | `Run prek hooks (use the \`dev-environment\` skill).` |
| Procedure step 2 | `Run pre-commit checks and targeted tests` | `Run prek hooks and targeted tests` |
| Code block | `uv run pre-commit run --all-files   # full pre-commit suite` | `uv run prek run --all-files   # full hook suite` |
| Checklist | `Pre-commit passes.` | `prek hooks pass.` |

### `.agents/skills/python-module-structure/SKILL.md` — EDIT

| Location | Before | After |
|---|---|---|
| Procedure step 4 | `uv run pre-commit run -a` | `uv run prek run -a` |

### `.agents/skills/pre-commit-hooks-create/SKILL.md` → `git-hooks-create/SKILL.md` — EDIT + RENAME DIR

Content changes (applied before directory rename):

| Location | Before | After |
|---|---|---|
| YAML `name` | `pre-commit-hooks-create` | `git-hooks-create` |
| YAML `description` | `"...project-specific pre-commit hooks in tasks/hooks/."` | `"...project-specific git hooks in hooks/."` |
| Title | `# Bespoke Pre-commit Hooks` | `# Bespoke Git Hooks` |
| Opening line | `"project-specific pre-commit hooks that live inside the repository under \`tasks/hooks/\`."` | `"project-specific git hooks that live inside the repository under \`hooks/\`."` |
| Outputs | `registration in \`.pre-commit-config.yaml\`` | `registration in \`prek.toml\`` |
| When-to-write decision | `**Use an upstream pre-commit repo**` | `**Use an upstream hook repo**` |
| File Placement | `Registration: \`.pre-commit-config.yaml\` (local repo block)` | `Registration: \`prek.toml\` (local hooks block)` |
| Hook template docstring | `"""Pre-commit hook to <describe what it checks>.` | `"""Git hook to <describe what it checks>.` |
| Section heading | `### 2. Register in \`.pre-commit-config.yaml\`` | `### 2. Register in \`prek.toml\`` |
| Registration block | YAML (see below) | TOML (see below) |
| Governing skill note | `"Pre-commit hook enforcement" section` | `"Git hook enforcement" section` |
| Test command | `uv run pre-commit run <hook-id> --all-files` | `uv run prek run <hook-id> --all-files` |

Registration block replacement:

**Before (YAML):**
```yaml
- repo: local
  hooks:
    - id: <hook-id-kebab-case>
      name: <Short human-readable description>
      entry: uv run tasks/hooks/<hook_name>.py
      language: system
      always_run: true
      pass_filenames: false
```

**After (TOML):**
```toml
[[repos]]
repo = "local"

[[repos.hooks]]
id = "<hook-id-kebab-case>"
name = "<Short human-readable description>"
entry = "uv run hooks/<hook_name>.py"
language = "system"
always_run = true
pass_filenames = false
```

Directory rename:
```powershell
Rename-Item ".agents/skills/pre-commit-hooks-create" ".agents/skills/git-hooks-create"
```

### `AGENTS.md` — EDIT

| Location | Before | After |
|---|---|---|
| `dev-environment` description | `"...dev environment for this repo (uv, tasks, pre-commit)"` | `"...dev environment for this repo (uv, tasks, prek)"` |
| `version-control` description | `"Commit conventions, hygiene, pre-commit, and pre-push checks"` | `"Commit conventions, hygiene, prek hooks, and pre-push checks"` |
| Skill name (x2) | `**\`pre-commit-hooks-create\`**` | `**\`git-hooks-create\`**` |
| Skill description (x2) | `"Writing bespoke pre-commit hooks"` | `"Writing bespoke git hooks"` |

### `docs/people/skills-taxonomy.md` — EDIT

| Location | Before | After |
|---|---|---|
| `dev-environment` row | `Bootstrap and maintain dev environment (uv, tasks, pre-commit)` | `Bootstrap and maintain dev environment (uv, tasks, prek)` |
| `version-control` row | `Commit conventions, hygiene, pre-commit, pre-push` | `Commit conventions, hygiene, prek hooks, pre-push` |
| Skill name | `pre-commit-hooks-create` | `git-hooks-create` |
| Skill description | `Writing bespoke pre-commit hooks` | `Writing bespoke git hooks` |

### `.github/agents/rl.kabilan.agent.md` — EDIT

| Location | Before | After |
|---|---|---|
| Line ~121 | `I MUST NOT create new pre-commit hooks` | `I MUST NOT create new git hooks` |
| Line ~189 (x2) | `Pre-commit hooks (bug fixes) \| \`pre-commit-hooks-create\`` | `Git hooks (bug fixes) \| \`git-hooks-create\`` |

### `skills-lock.json` — EDIT

Rename JSON key:
```diff
-  "pre-commit-hooks-create": {
+  "git-hooks-create": {
```

### `hooks/*.py` — EDIT (docstrings only, 11+ files)

Pattern: replace `"""Pre-commit hook` with `"""Git hook` in module docstrings.

Additionally in `hooks/fix-doc-sync.py`:
- `"the pre-commit autofix convention"` → `"the autofix convention"`

---

## P3 — Config File Migration

### `.pre-commit-config.yaml` — DELETE

Removed after `prek.toml` is verified.

### `prek.toml` — NEW

Generated via:
```powershell
rtk uv run prek util yaml-to-toml --output prek.toml
```

Post-conversion review checklist:
- [ ] All 17+ hooks present
- [ ] `priority` values preserved on all hooks
- [ ] `always_run` / `pass_filenames` correct
- [ ] `additional_dependencies = ["tomli"]` preserved for codespell hook
- [ ] `args` arrays correct for all hooks
- [ ] `ci.autofix_prs` top-level key removed (no effect without pre-commit-ci)
- [ ] Operational comments re-added where needed

### `.agents/skills/git-hooks-create/SKILL.md` — EDIT (additional P3 changes)

All remaining `".pre-commit-config.yaml"` literal strings → `"prek.toml"`.
Registration block already updated in P2.4.

### `docs/people/drafts/skills/customization-mechanism-triage/SKILL.md` — EDIT

| Location | Before | After |
|---|---|---|
| Comparison table | `\`.git/hooks/pre-commit\` or \`.pre-commit-config.yaml\`` | `\`.git/hooks/pre-commit\` or \`prek.toml\`` |
| Decision guidance | `hooks/ directory + .pre-commit-config.yaml` | `hooks/ directory + prek.toml` |
| Example decision row | `"git pre-commit hook" (\`hooks/\` directory + \`.pre-commit-config.yaml\`)` | `"git hook" (\`hooks/\` directory + \`prek.toml\`)` |
