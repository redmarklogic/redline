# Implementation Plan: GitHub Projects Skill and Board Bootstrap

**Date**: 2026-06-04 | **Spec**: [spec.md](spec.md)
**Status**: In Progress

## Summary

Operationalise the Redline GitHub Projects board end-to-end: transfer the repo to the
`redmarklogic` org, bootstrap the board schema, register the `github-projects` skill
across all governance artifacts, write and test a seed script that imports open specs
as parent issues, and verify the live board reflects the correct backlog state.

The Python tool (`functions.py`, `schema.py`) and all governance artifacts (SKILL.md,
`skills-lock.json`, `skills-architecture.md`, agent JDs) were implemented in a prior
session and are treated as retrospective Phase 1 deliverables. The remaining
implementable work is the seed script and its tests.

## Concept-to-Plan Phase Mapping

| Concept Phase | Concept Name | Plan Phase | Notes |
|---|---|---|---|
| Phase 0 | Repo transfer | Phase 0 | Manual founder action; no code |
| Phase 1 | Board bootstrap | Phase 0 | Bundled — same founder session; runbook covers it |
| Phase 2 | Skill creation | Phase 1 | Retrospective — completed prior to this plan |
| Phase 3 | First-pass seeding | Phase 2 | Seed script + tests — main implementation target |
| Phase 4 | Enforcement hooks | Deferred | Requires org webhooks (after board is live and confirmed) |

## Technical Context

**Language**: Python 3.14
**Package manager**: uv
**Testing**: pytest (TDD workflow per `test-driven-development` skill)
**Architecture**: Monorepo — tooling module at `.agents/tools/github_projects/`; no `src/rl/` changes
**Dev OS**: Windows | **Deploy OS**: N/A (tooling script, not deployed)
**Domain modeling**: Pydantic v2 `BaseModel` (already in `schema.py`)
**Key dependencies**: `pydantic>=2`, `gh` CLI (already present)

## Design Decisions

| # | Decision | Choice | Rationale |
|---|---|---|---|
| D1 | Seed script location | `.agents/tools/github_projects/seed_backlog.py` | Collocated with the tool it orchestrates; not a src/rl/ module since it is a one-shot operator script, not application logic |
| D2 | Spec metadata extraction | Regex parse of `spec.md` first `#` heading for title; directory name for source pointer | spec.md headers are structurally consistent across all existing specs (001–012); no YAML frontmatter exists; spec 013 (this spec) is excluded from seeding |
| D3 | Agent assignment for seeded tasks | Default `Kabilan` for all specs; caller may override via `--agent` flag | Backlog import is a bulk operation; individual sprint assignment (agent, sprint) is Mark's `sync-this-week` concern post-seeding |
| D4 | Default dates | `start_date = today`, `target_date = today + 84 days (12 weeks)` | Placeholder dates; Mark reassigns during `sync-this-week`; spec mandates dates be set (FR-007 rejects None) |
| D5 | Dry-run mode | `--dry-run` flag prints what would be created without calling the API | Safe to run on the live board after Phase 0 completes; avoids accidental duplicate creation |
| D6 | Duplicate guard | Script does NOT deduplicate — per spec: "GitHub creates a duplicate issue; the tool does not deduplicate. Caller must verify before seeding." Log a warning before running | Matches spec assumption; dry-run is the pre-check mechanism |

## Domain Impact

**Modularity assessment**: New module within existing `.agents/tools/github_projects/` package — not a new bounded context; no import-linter contract change required (tooling is outside `src/rl/`)
**New packages**: None
**Bounded context changes**: None
**Import-linter contract updates**: None (`.agents/tools/` is not under import-linter)
**Subdomain classification**: Supporting — task management tooling, not core geotechnical logic
**New domain terms**: None

## Architecture

### Data Flow — seed_backlog

```
specs/NNN-*/spec.md
    ↓ _parse_spec_title()       extract first # heading → title
    ↓ _parse_spec_purpose()     extract ## Context first paragraph → purpose
    ↓ TaskCreate(...)           construct Pydantic model; raises ValidationError early
    ↓ create_task(task, config) create GitHub issue + set 9 board fields
    ↓ SeedResult                per-spec result (ok, issue_url, title, source)
```

### Module Layout

```
.agents/tools/github_projects/
├── __init__.py          (existing — exports unchanged)
├── schema.py            (existing — no changes)
├── functions.py         (existing — bugs fixed in prior session)
└── seed_backlog.py      (NEW — seed script + CLI entrypoint)

tests/.agents/tools/github_projects/
├── __init__.py          (NEW — package marker)
├── test_schema.py       (NEW — schema validation unit tests)
└── test_seed_backlog.py (NEW — seed logic tests with mocked create_task)
```

## MoSCoW

| Category | Items |
|---|---|
| **Must have** | `seed_backlog.py` with `--dry-run` mode; tests for schema validators; tests for `seed_backlog` with mocked API; `project_config.json` written and committed after `resolve-config` runs |
| **Should have** | CLI `--start-date` and `--target-date` overrides; per-spec skip log |
| **Could have** | `--spec-filter` regex flag to seed a subset of specs |
| **Won't have (this time)** | Deduplication logic; Phase 4 enforcement hooks; `sync-this-week` automation; any GitHub Actions changes |

## Phased Delivery

### Phase 0: Board Infrastructure (Founder Action — No Code)

**Goal**: `redmarklogic/redline` exists on GitHub and the Redline project board is
live with all 9 custom fields, 5 columns, 4 automations, 2 views, and 4 milestones.
`project_config.json` is committed.

**TDD approach**: N/A — manual steps with runbook verification commands.

**Deliverables**:

1. `github.com/redmarklogic/redline` — transferred repo (FR-000, FR-000b)
2. `github.com/orgs/redmarklogic/projects/N` — board with full schema (FR-001–FR-005)
3. `.agents/tools/github_projects/project_config.json` — committed (FR-006)

**Verification**:

```sh
gh repo view redmarklogic/redline --json name,owner
gh project list --owner redmarklogic
gh project field-list N --owner redmarklogic --format json | jq '[.fields[].name]'
```

Expected: repo owner = `redmarklogic`; project named "Redline"; 9+ field names in output.

**Acceptance Gate** (both must pass before Phase 2 starts):
- [ ] `gh repo view redmarklogic/redline` returns correct owner
- [ ] `project_config.json` committed with all 9 field IDs populated

See `.agents/tools/github_projects/bootstrap-runbook.md` for full step-by-step instructions.

---

### Phase 1: Governance Layer (Retrospective — Complete)

**Goal**: All governance artifacts exist and are consistent: SKILL.md, skills-lock.json,
skills-architecture.md, and 5 agent JDs each carry a `github-projects` trigger.

**Deliverables** (all completed in prior session):

1. `.agents/skills/github-projects/SKILL.md` — 9 procedures, 7 guards, access table
2. `skills-lock.json` — `github-projects` entry at layer 6, functional tier
3. `docs/architecture/skills-architecture.md` — Layer 6 table + 3 mermaid diagrams
4. `.claude/agents/mark.md`, `kabilan.md`, `peter.md`, `matt.md`, `john.md` — skill trigger rows
5. `.agents/tools/github_projects/functions.py` — 4 bug fixes + `_build_body` agents section
6. `.agents/tools/github_projects/bootstrap-runbook.md` — Phase 0/1 runbook

**Verification**:

```sh
# Skill file exists and has required sections
grep -c "Guard Conditions\|Agent Access Table\|Procedures\|Prerequisites" .agents/skills/github-projects/SKILL.md
# Expected: 4

# skills-lock.json has entry
python -c "import json; d=json.load(open('skills-lock.json')); print(d['skills']['github-projects'])"
```

**Acceptance Gate**:
- [x] All 6 deliverables committed to master
- [x] `skills-lock.json` contains `github-projects` with correct `tier`, `layer`, `owner_agent`

---

### Phase 2: Seed Script + Tests

**Goal**: `seed_backlog.py` reads all open specs, constructs valid `TaskCreate` objects,
and either prints a dry-run summary or calls `create_task()` for each. All schema
validators and seed logic are covered by tests that pass without a live board.

**TDD approach**: Write `test_schema.py` first (pure Pydantic validation — no subprocess),
then `test_seed_backlog.py` (mock `create_task`), then implement.

**Deliverables**:

1. `tests/.agents/tools/github_projects/__init__.py` — package marker
2. `tests/.agents/tools/github_projects/test_schema.py` — schema validation tests
3. `tests/.agents/tools/github_projects/test_seed_backlog.py` — seed logic tests
4. `.agents/tools/github_projects/seed_backlog.py` — `seed_backlog()` + `main()` CLI

**Verification**:

```sh
rtk uv run pytest tests/.agents/tools/github_projects/ -v
rtk uv run python .agents/tools/github_projects/seed_backlog.py --dry-run
```

Expected: all tests green; dry-run prints one line per spec in `specs/` with no API calls.

**Acceptance Gate** (both must pass before Phase 3 starts):

- [ ] `rtk uv run pytest tests/.agents/tools/github_projects/ -v` — all green
- [ ] `rtk uv run python .agents/tools/github_projects/seed_backlog.py --dry-run` — lists ≥ 12 specs without error

---

### Phase 3: Live Seed Run (After Phase 0 Complete)

**Goal**: Top open specs visible on the Redline board in Backlog with correct source,
type, and agent fields. Founder can filter by agent and sprint.

**TDD approach**: N/A — integration step against live board; verification is observational.

**Deliverables**:

1. Board items for specs/001 through specs/012 in Backlog (spec 013 excluded — it is governance overhead, not a product feature; seeding it would create a circular board entry)
2. `project_config.json` committed (refreshed after board is live)

**Verification**:

```python
from agents.tools.github_projects import resolve_project_config, list_tasks
config = resolve_project_config(N, "redmarklogic")
backlog = list_tasks(config, status="Backlog")
print(f"{len(backlog)} items in Backlog")
assert len(backlog) >= 10
```

**Acceptance Gate**:
- [ ] `list_tasks(config, status="Backlog")` returns ≥ 10 items
- [ ] Each item has non-None `source`, `task_type`, and `agents` (primary_agent)

## File Inventory

| Phase | New Files | Count |
|---|---|---|
| 0 | `.agents/tools/github_projects/project_config.json` | 1 |
| 1 | `.agents/skills/github-projects/SKILL.md`, `bootstrap-runbook.md`, 5 agent JDs updated | 2 new + 7 modified |
| 2 | `tests/.agents/tools/github_projects/__init__.py`, `test_schema.py`, `test_seed_backlog.py`, `.agents/tools/github_projects/seed_backlog.py` | 4 |
| 3 | None (runtime operation) | 0 |

**Total new**: ~7 | **Total modified**: ~7 (from prior session)

## Library Best Practices

### pydantic (v2)

- **Import path**: `from pydantic import BaseModel, ValidationError, model_validator`
- **API gotchas**: `frozenset` fields with `min_length=1` enforce non-empty at construction; `model_validator(mode="after")` runs after all field validators
- **Confirmed pattern**: `TaskCreate(agents=frozenset({"Kabilan"}), ...)` — use `frozenset` literal, not `set`

### subprocess / gh CLI

- **Import path**: `import subprocess`
- **API gotchas**: Always `shell=False`, args as list — confirmed in existing `_run_gh`
- **Confirmed pattern**: already locked in `functions.py`; seed script never calls subprocess directly

## Risk Register

| Risk | Mitigation |
|---|---|
| Board doesn't exist when seed runs | `resolve_project_config` raises `RuntimeError` with clear message; seed script surfaces it before any issue creation |
| Spec with no `spec.md` | Skip with logged warning; continue to next spec (matches spec edge case assumption) |
| Duplicate issue on re-run | `--dry-run` flag allows verification; seed script logs warning at startup not to re-run without checking |
| `gh auth` missing `project` scope | `create_task` returns `status_code=401`; seed script aggregates errors and reports at end |
| stale `project_config.json` after schema change | `resolve_project_config(force_refresh=True)` in bootstrap step; covered by bootstrap-runbook.md |

## Glossary

- **GIR**: Geotechnical Investigation Report — the primary output document type Redline generates
- **board item**: A GitHub Projects v2 item that links to a GitHub Issue and carries custom field values
- **ProjectConfig**: Pydantic model caching GitHub Projects field node IDs; persisted to `project_config.json`
- **primary_agent**: The single agent name written to the board's `Agent` single-select field (first alphabetically when multiple agents are assigned)
- **seed**: One-time bulk import of existing specs as parent issues in the Backlog column
- **SKILL.md**: Agent-readable procedure reference in `.agents/skills/<name>/SKILL.md`; loaded on demand by agents when a trigger condition matches
