# Feature Specification: Migrate from pre-commit to prek

**Feature Branch**: `007-migrate-to-prek`

**Created**: 2026-05-27

**Status**: Draft

**Input**: User description: "I want to migrate from pre-commit to prek in this project."

## Background

The project already uses `prek` (v0.3.8+) as a dev dependency and the CI workflow
(`static-checks.yml`) already runs `prek -a`. The `.pre-commit-config.yaml` already
uses `priority` — a prek-only extension. However, the developer workflow, skills, and
documentation still reference `pre-commit` commands. This spec covers completing the
migration by removing `pre-commit` from the dependency graph and updating all developer-facing
references to use `prek`.

**prek overview** (v0.4.3, May 2026): A fast, Rust-native, drop-in alternative to
pre-commit with full `.pre-commit-config.yaml` compatibility, parallel hook execution
by priority, native `uv` integration, and a no-Python-dependency standalone binary.
Stars: 7,700+. Used by CPython, Apache Airflow, FastAPI.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Developer installs git hooks (Priority: P1)

A developer clones the repo and sets up their local environment. They run a single
command to install git hooks. After installation, hooks fire automatically on every
`git commit` — using `prek`, not `pre-commit`.

**Why this priority**: The install command is the first thing every developer runs.
If it still references `pre-commit`, the migration is incomplete at the most visible touch point.

**Independent Test**: Run `uv run prek install` in a clean checkout and confirm
that `.git/hooks/pre-commit` invokes `prek`, then make a trivial commit and observe
hooks firing.

**Acceptance Scenarios**:

1. **Given** a fresh checkout with `uv sync` complete, **When** the developer runs `uv run prek install`, **Then** all git hooks are installed and `pre-commit install` is not required.
2. **Given** hooks installed, **When** a `git commit` is made, **Then** all configured hooks run and any failure blocks the commit.
3. **Given** hooks installed, **When** `uv run prek run --all-files` is executed, **Then** all hooks run against all tracked files and results are reported.

---

### User Story 2 — Remove pre-commit from dev dependencies (Priority: P1)

`pre-commit` and `pre-commit-update` are removed from `pyproject.toml` so that new
developers do not install them. The `prek` dependency remains and is the sole hook runner.

**Why this priority**: Keeping both tools in dev deps creates ambiguity about which
runner is authoritative and unnecessarily increases install size.

**Independent Test**: After removing `pre-commit` and `pre-commit-update` from
`pyproject.toml` and running `uv sync`, verify they are absent from the lock file
and that `uv run prek run --all-files` still passes.

**Acceptance Scenarios**:

1. **Given** the updated `pyproject.toml`, **When** `uv sync` is run, **Then** neither `pre-commit` nor `pre-commit-update` is installed.
2. **Given** `pre-commit` is not installed, **When** `uv run prek run --all-files` is executed, **Then** all hooks run successfully (no hooks depend on the `pre-commit` Python package directly).
3. **Given** the lock file is updated, **When** a team member runs `uv sync --frozen`, **Then** the environment is reproducible without `pre-commit`.

---

### User Story 3 — Update developer workflow documentation (Priority: P2)

All skills and documentation that instruct developers to run `pre-commit` commands
are updated to the equivalent `prek` commands. No developer-facing reference to `pre-commit`
remains as an actionable instruction.

**Why this priority**: Stale docs cause confusion and erode trust in the migration.

**Independent Test**: Search all `.agents/skills/` and `AGENTS.md` for actionable
`pre-commit` CLI invocations and confirm none remain (references to the concept
"pre-commit hooks" as a generic term are acceptable; `uv run pre-commit ...` commands are not).

**Acceptance Scenarios**:

1. **Given** updated skills, **When** an agent reads `dev-environment/SKILL.md`, **Then** it finds `uv run prek install` and `uv run prek run --all-files` as the hook commands.
2. **Given** updated skills, **When** an agent reads `pre-commit-hooks-create/SKILL.md`, **Then** all test/run instructions use `prek` CLI syntax.
3. **Given** updated skills, **When** an agent reads `version-control/SKILL.md`, **Then** the pre-push check section references `prek`, not `pre-commit`.
4. **Given** updated skills, **When** an agent reads `python-module-structure/SKILL.md`, **Then** the "run checks" step uses `uv run prek run -a`.

---

### User Story 4 — Convert config to `prek.toml` (Priority: P3)

Optionally convert `.pre-commit-config.yaml` to `prek.toml` using `prek util yaml-to-toml`.
This embraces the prek-native format and makes prek-only features (like `priority`) explicit.
YAML comments are not preserved during conversion.

**Why this priority**: The YAML config works unchanged with prek. This is a housekeeping
improvement, not a correctness requirement.

**Independent Test**: Run `prek util yaml-to-toml --output prek.toml` and then
`uv run prek run --all-files` with the new TOML config — all hooks must produce
the same results as with the YAML config.

**Acceptance Scenarios**:

1. **Given** `prek.toml` created from the YAML config, **When** `uv run prek run --all-files` is run, **Then** all hooks pass (same results as with `.pre-commit-config.yaml`).
2. **Given** `prek.toml` is present, **When** `.pre-commit-config.yaml` is removed, **Then** `prek` uses `prek.toml` and all hooks continue to fire on commit.

---

### Edge Cases

- Some hooks use `language: system` with `uv run` entry points. Confirm prek handles these correctly (it does — `language: system` is fully supported).
- The `priority` field is already used in `.pre-commit-config.yaml`. Prek already supports this as an extension; no changes needed there.
- The `ci.autofix_prs: false` top-level key is a pre-commit-ci setting. Confirm prek ignores unknown top-level keys gracefully (it does — prek tolerates unknown keys for forward compatibility).
- `uv-sync` and `uv-export` hooks from `astral-sh/uv-pre-commit` must still resolve correctly under prek (they are standard pre-commit hooks and prek is fully compatible).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Developers MUST be able to install git hooks using `uv run prek install`.
- **FR-002**: `pre-commit` and `pre-commit-update` MUST be removed from `[dependency-groups].dev` in `pyproject.toml`.
- **FR-003**: `prek` MUST remain (or be upgraded) in `[dependency-groups].dev` with an appropriate minimum version constraint (`>=0.4.3` recommended).
- **FR-004**: `uv.lock` MUST be regenerated to reflect the removed dependencies.
- **FR-005**: `dev-environment/SKILL.md` MUST be updated: the "Pre-commit Hooks" section heading and all `uv run pre-commit ...` instructions MUST be replaced with `prek` equivalents.
- **FR-006**: `pre-commit-hooks-create/SKILL.md` MUST be updated: all `uv run pre-commit run <hook-id> --all-files` instructions MUST use `prek run <hook-id> --all-files`.
- **FR-007**: `version-control/SKILL.md` MUST be updated: `uv run pre-commit run --all-files` MUST become `uv run prek run --all-files`.
- **FR-008**: `python-module-structure/SKILL.md` MUST be updated: `uv run pre-commit run -a` MUST become `uv run prek run -a`.
- **FR-009**: The dev dependency table in `dev-environment/SKILL.md` MUST reflect the updated `dev` group (no `pre-commit`, no `pre-commit-update`).
- **FR-010**: `AGENTS.md` skill descriptions that say "pre-commit" as an active instruction (e.g., "Bootstrap and maintain the dev environment for this repo (uv, tasks, pre-commit)") MUST be updated to reference prek where appropriate.
- **FR-011** *(optional — P3)*: `.pre-commit-config.yaml` MAY be converted to `prek.toml` using `prek util yaml-to-toml`. If converted, `.pre-commit-config.yaml` MUST be deleted.

### Key Entities

- **prek**: The Rust-native git hook manager replacing pre-commit.
- **`.pre-commit-config.yaml`**: Existing hook configuration file (compatible with prek as-is; optionally replaced by `prek.toml`).
- **`prek.toml`**: Native prek configuration format (TOML); equivalent to `.pre-commit-config.yaml` but prek-only.
- **`pyproject.toml`**: Dev dependency declarations — source of truth for what tooling is installed.
- **Dev skills**: `.agents/skills/dev-environment/SKILL.md`, `pre-commit-hooks-create/SKILL.md`, `version-control/SKILL.md`, `python-module-structure/SKILL.md`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `pre-commit` and `pre-commit-update` do not appear in `uv.lock` after migration.
- **SC-002**: `uv run prek install` succeeds in a clean environment and installs working git hooks.
- **SC-003**: `uv run prek run --all-files` passes all checks (same pass/fail results as current `uv run pre-commit run --all-files`).
- **SC-004**: Zero occurrences of `uv run pre-commit` remain in any developer-facing skill or documentation file.
- **SC-005**: CI (`static-checks.yml`) continues to pass without modification (it already uses `prek -a`).
- **SC-006** *(optional)*: If `prek.toml` is adopted, `uv run prek run --all-files` passes with the TOML config and `.pre-commit-config.yaml` is deleted.

## Assumptions

- prek is fully compatible with all hooks in the current `.pre-commit-config.yaml` (confirmed: all use `language: system`, `language: python`, `language: fail` — all supported).
- The `priority` field in the existing YAML config is already a prek extension; no YAML modifications are needed before migration.
- No hooks currently hard-depend on the `pre-commit` Python package at runtime (hooks invoke `uv run ...` entry points, not pre-commit internals).
- The CI workflow (`static-checks.yml`) already uses `prek` and requires no changes.
- `pre-commit-update` (used for auto-updating hook revisions) is superseded by `prek auto-update`.
- Conversion to `prek.toml` is a separate, optional step (P3) and does not block P1/P2 work.
- `AGENTS.md` and agent `.md` files that mention "pre-commit hooks" as a concept (not a CLI invocation) do not need to be changed — only actionable CLI instructions need updating.
