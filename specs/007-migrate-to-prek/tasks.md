# Tasks: Migrate from pre-commit to prek

**Input**: [plan.md](plan.md) | [spec.md](spec.md)
**Prerequisites**: `prek>=0.3.8` already in `pyproject.toml`; CI already running `prek -a`

<!-- Task sizing rule: each task is a VERTICAL SLICE -- front-to-back, one complete
     new behaviour, nothing left dangling.
     [P] = parallelizable (different files, no dependencies)
     Acceptance Gates are hard stops -- do not start the next phase until they pass. -->

---

## Phase 1: Dependency Removal

**Purpose**: Remove `pre-commit` and `pre-commit-update` from the Python environment and verify prek is the sole hook runner.

### Implementation

- [X] T001 [US2] Edit `pyproject.toml` — remove `"pre-commit>=4.2.0"` and `"pre-commit-update>=0.8.0"` from `[dependency-groups].dev`; update `"prek>=0.3.8"` → `"prek>=0.4.3"`
- [X] T002 [US2] Regenerate lock file: run `uv sync --upgrade-package prek` — auto-updates `uv.lock`

### Acceptance Gate

- [X] T003 [US2] Verify `pre-commit` absent from environment: `uv run python -c "import pre_commit"` — expected `ModuleNotFoundError`
- [X] T004 [US2] Smoke test hooks: `uv run prek run --all-files` — all hooks must pass (exit 0)

---

## Phase 2: CLI Command and Naming Updates

**Purpose**: Remove every developer-facing `pre-commit` CLI invocation and rename the `pre-commit-hooks-create` skill to `git-hooks-create`.

**Depends on**: Phase 1 Acceptance Gate passing.

### Implementation

- [X] T005 [P] [US3] Update `dev-environment/SKILL.md` in `.agents/skills/dev-environment/SKILL.md`:
  - YAML description: `(uv, tasks, pre-commit)` → `(uv, tasks, prek)`
  - Section heading: `### Pre-commit Hooks` → `### Git Hooks`
  - Body: `This repo uses \`pre-commit\`.` → `This repo uses \`prek\`.`
  - Install command: `uv run pre-commit install` → `uv run prek install` (all occurrences incl. Troubleshooting)
  - Run command: `uv run pre-commit run --all-files` → `uv run prek run --all-files` (all occurrences)
  - Dev deps table: remove `pre-commit` and `pre-commit-update` rows; update `prek` version
  - Produces bullet: `"pre-commit hooks"` → `"prek hooks"`

- [X] T006 [P] [US3] Update `version-control/SKILL.md` in `.agents/skills/version-control/SKILL.md`:
  - YAML description: `"pre-commit, and pre-push checks"` → `"prek hooks, and pre-push checks"`
  - Applies To line: same replacement
  - Before Pushing: `Run pre-commit checks` → `Run prek hooks` (both occurrences)
  - Procedure step 2: `Run pre-commit checks and targeted tests` → `Run prek hooks and targeted tests`
  - Code block: `uv run pre-commit run --all-files   # full pre-commit suite` → `uv run prek run --all-files   # full hook suite`
  - Checklist: `Pre-commit passes.` → `prek hooks pass.`

- [X] T007 [P] [US3] Update `python-module-structure/SKILL.md` in `.agents/skills/python-module-structure/SKILL.md`:
  - Procedure step 4: `uv run pre-commit run -a` → `uv run prek run -a`

- [X] T008 [US3] Update content of `.agents/skills/pre-commit-hooks-create/SKILL.md` (apply before rename in T009):
  - YAML `name`: `pre-commit-hooks-create` → `git-hooks-create`
  - YAML `description`: `"How to implement, register, and test project-specific pre-commit hooks in tasks/hooks/."` → `"How to implement, register, and test project-specific git hooks in hooks/."`
  - Title: `# Bespoke Pre-commit Hooks` → `# Bespoke Git Hooks`
  - Opening sentence: `"project-specific pre-commit hooks"` → `"project-specific git hooks"`
  - Outputs: `registration in \`.pre-commit-config.yaml\`` → `registration in \`prek.toml\``
  - When-to-write: `"Use an upstream pre-commit repo"` → `"Use an upstream hook repo"`
  - File Placement section: `Registration: \`.pre-commit-config.yaml\`` → `Registration: \`prek.toml\``
  - Hook template docstring: `"""Pre-commit hook to` → `"""Git hook to`
  - Section heading: `### 2. Register in \`.pre-commit-config.yaml\`` → `### 2. Register in \`prek.toml\``
  - Replace YAML registration block with TOML equivalent (see plan.md P3.4 for block)
  - Section 3: `"Pre-commit hook enforcement"` → `"Git hook enforcement"`
  - Section 4 test command: `uv run pre-commit run <hook-id> --all-files` → `uv run prek run <hook-id> --all-files`

- [X] T009 [US3] Rename skill directory: `Rename-Item ".agents/skills/pre-commit-hooks-create" ".agents/skills/git-hooks-create"` (depends on T008)

- [X] T010 [P] [US3] Update `AGENTS.md`:
  - `dev-environment` description: `"(uv, tasks, pre-commit)"` → `"(uv, tasks, prek)"`
  - `version-control` description: `"pre-commit, and pre-push checks"` → `"prek hooks, and pre-push checks"`
  - Both occurrences of `pre-commit-hooks-create` → `git-hooks-create`; description → `"Writing bespoke git hooks"`

- [X] T011 [P] [US3] Update `docs/people/skills-taxonomy.md`:
  - `dev-environment` row: `(uv, tasks, pre-commit)` → `(uv, tasks, prek)`
  - `version-control` row: `pre-commit, pre-push` → `prek hooks, pre-push`
  - `pre-commit-hooks-create` row key → `git-hooks-create`; description → `Writing bespoke git hooks`

- [X] T012 [P] [US3] Update `.github/agents/rl.kabilan.agent.md`:
  - Line ~121: `"I MUST NOT create new pre-commit hooks"` → `"I MUST NOT create new git hooks"`
  - Line ~189 (×2): `Pre-commit hooks (bug fixes) | \`pre-commit-hooks-create\`` → `Git hooks (bug fixes) | \`git-hooks-create\``

- [X] T013 [P] [US3] Update `skills-lock.json`: rename key `"pre-commit-hooks-create"` → `"git-hooks-create"`

- [X] T014 [P] [US3] Update hook script docstrings in `hooks/` — change `"""Pre-commit hook` → `"""Git hook` in:
  - `hooks/check-no-env-loader.py`
  - `hooks/clean-quarto-intermediates.py`
  - `hooks/clean-quarto-artifacts.py`
  - `hooks/check-no-user-paths.py`
  - `hooks/check-no-section-rules.py`
  - `hooks/check-no-env-defaults.py`
  - `hooks/check-no-debug-statements.py`
  - `hooks/check-no-dataclass-in-domain.py`
  - `hooks/check-no-argparse.py`
  - `hooks/check-no-archive-imports.py`
  - `hooks/check-hook-adr-reference.py`
  - `hooks/fix-doc-sync.py`: `"the pre-commit autofix convention"` → `"the autofix convention"`
  - Inspect and update if needed: `hooks/check-banned-words.py`, `hooks/check-skills-documented.py`, `hooks/check-skill-has-red-phase.py`, `hooks/check_overused_underscore.py`

### Acceptance Gate

- [X] T015 [US1] [US3] Verify no actionable `pre-commit` CLI references remain in skills/agents/docs:
  ```powershell
  Select-String -Path ".agents/skills/**/*.md","AGENTS.md",".github/agents/*.md" `
    -Pattern "uv run pre-commit|pre-commit install|pre-commit run" -Recurse
  ```
  Expected: 0 matches
- [X] T016 [US1] Verify skill renamed: `Test-Path ".agents/skills/pre-commit-hooks-create"` → False; `Test-Path ".agents/skills/git-hooks-create"` → True
- [X] T017 [US1] Install hooks via prek: `uv run prek install` — no errors
- [X] T018 [US1] Run all hooks: `uv run prek run --all-files` — exit 0

---

## Phase 3: Config File Migration

**Purpose**: Replace `.pre-commit-config.yaml` with `prek.toml` as the sole hook config; eliminate all YAML config references.

**Depends on**: Phase 2 Acceptance Gate passing.

### Implementation

- [X] T019 [US4] Convert YAML config to TOML: `uv run prek util yaml-to-toml --output prek.toml`
  - Review generated `prek.toml`: verify all `priority` values preserved, `always_run`/`pass_filenames` options correct, `additional_dependencies` block for `codespell` present
  - Remove `ci.autofix_prs` key (has no effect without pre-commit-ci)
  - Re-add any important operational comments lost in conversion

- [X] T020 [US4] Smoke test with TOML: `uv run prek run --all-files` — all hooks pass with `prek.toml` present alongside YAML

- [X] T021 [US4] Delete YAML config: `Remove-Item ".pre-commit-config.yaml"` (depends on T020 passing)

- [X] T022 [P] [US4] Update `.agents/skills/git-hooks-create/SKILL.md` registration block — replace YAML example with TOML:
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

- [X] T023 [P] [US4] Update `docs/people/drafts/skills/customization-mechanism-triage/SKILL.md`: (SKIPPED — file does not exist)
  - Replace `".pre-commit-config.yaml"` → `"prek.toml"` in comparison table and decision guidance
  - Update example reference: `"hooks/ directory + prek.toml"`

### Acceptance Gate

- [X] T024 [US4] Validate TOML config: `uv run prek validate-config prek.toml` — exit 0
- [X] T025 [US4] Confirm YAML deleted: `Test-Path ".pre-commit-config.yaml"` — expected False
- [X] T026 [US4] Final hook run: `uv run prek run --all-files` — exit 0 with TOML as sole config

---

## Phase 4: Polish

**Purpose**: Full verification that all three user stories are satisfied end-to-end.

- [X] T027 [P] Verify `pre-commit` absent from lock file: `Select-String -Path uv.lock -Pattern "pre-commit"` — expected 0 matches
- [X] T028 [P] Verify `uv sync --frozen` reproduces environment without `pre-commit`
- [X] T029 Run full verification gate from plan.md (all 6 checks):
  ```powershell
  # 1. Package absent
  rtk uv run python -c "import pre_commit" 2>&1
  # 2. Hooks pass
  rtk uv run prek run --all-files
  # 3. No CLI references
  Select-String -Path ".agents/skills/**/*.md","AGENTS.md",".github/agents/*.md" `
    -Pattern "uv run pre-commit|pre-commit install|pre-commit run" -Recurse
  # 4. YAML config deleted
  Test-Path ".pre-commit-config.yaml"
  # 5. TOML config valid
  rtk uv run prek validate-config prek.toml
  # 6. Skill renamed
  Test-Path ".agents/skills/pre-commit-hooks-create"
  Test-Path ".agents/skills/git-hooks-create"
  ```

### Acceptance Gate

- [X] T030 All 6 verification checks pass; no regressions in hook behaviour

---

## Dependency Graph

```
T001 → T002 → T003 → T004 (Phase 1 gate)
                          ↓
              T005–T014 (Phase 2, parallelizable within)
                          ↓
              T009 (rename dir, depends on T008)
                          ↓
              T015–T018 (Phase 2 gate)
                          ↓
              T019 → T020 → T021
              T022, T023 (parallel, depend on T019)
                          ↓
              T024–T026 (Phase 3 gate)
                          ↓
              T027–T029 (parallel)
                          ↓
              T030 (final gate)
```

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies on incomplete tasks)
- `[USn]` = maps to User Story n from spec.md
- Acceptance Gates are hard stops — do not start the next phase until they pass
- T008 must complete before T009 (content edit before directory rename)
- T020 must pass before T021 (smoke test before destructive delete)
- Commit after each phase gate passes
- Use `finishing-a-development-branch` skill after T030 passes
