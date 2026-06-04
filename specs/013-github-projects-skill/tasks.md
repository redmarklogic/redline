# Tasks: GitHub Projects Skill and Board Bootstrap

**Input**: [plan.md](plan.md)
**Prerequisites**: `gh` CLI ≥ 2.40 authenticated; `redmarklogic` org exists; `harell` has Owner access

<!-- Task sizing rule: each task is a VERTICAL SLICE — front-to-back, one complete
     new behaviour, nothing left dangling. -->

## Phase 0: Board Infrastructure (Founder Action — No Code)

**Purpose**: Repo transferred to `redmarklogic`; board live with full schema; `project_config.json` committed.

- [x] T001 [Phase 0] Transfer `harell/redline` to `redmarklogic` org via GitHub Settings → Danger Zone → Transfer — follow `.agents/tools/github_projects/bootstrap-runbook.md` Phase 0
- [x] T002 [Phase 0] Update local remote: `git remote set-url origin https://github.com/redmarklogic/redline.git` then `git fetch origin` — verify no error
- [x] T003 [Phase 0] Bootstrap board via CLI: run bootstrap-runbook.md Phase 1 steps 1.1–1.6 (`gh auth refresh`, `gh project create`, 8× `gh project field-create`, configure Status columns in UI, enable 4 automations in UI, create 4 milestones via `gh api`)
- [ ] T004 [Phase 0] Create 2 saved views in GitHub UI: Engineering (`-type:Ops`, default) and Ops (`type:Ops`) — **founder action required (GitHub UI only)**
- [x] T005 [Phase 0] Run `resolve_project_config(force_refresh=True)` and commit `project_config.json` — see bootstrap-runbook.md step 1.8
- [x] T006 [Phase 0] Verify: `gh project field-list N --owner redmarklogic --format json` shows ≥ 9 field names including `Type`, `Agent`, `Sprint`, `Source`, `Depends on`

### Acceptance Gate

- [x] T007 [Phase 0] `gh repo view redmarklogic/redline --json name,owner` returns `{"name": "redline", "owner": {"login": "redmarklogic"}}`
- [x] T008 [Phase 0] `project_config.json` is committed and contains all 9 field IDs (non-empty `field_ids` dict)

---

## Phase 1: Governance Layer (Retrospective — Complete)

**Purpose**: All skill registry, architecture, and agent JD artifacts committed to master.

- [x] T009 [Phase 1] Implement `schema.py` — `TaskCreate`, `TaskUpdate`, `TaskResult`, `TaskRecord`, `ProjectConfig` Pydantic v2 models in `.agents/tools/github_projects/`
- [x] T010 [Phase 1] Implement `functions.py` — 7 public functions using `gh` CLI; `_run_gh` single call-site; `shell=False` security rule
- [x] T011 [Phase 1] Fix bugs in `functions.py`: `task.primary_agent` (was `task.agent`), `min(update.agents)` (was `update.agent`), `r.primary_agent` filter (was `r.agent`), `agents=frozenset({...})` in `_item_to_record` (was invalid `agent=`)
- [x] T012 [Phase 1] Add `## Agents` and `## Depends on` sections to `_build_body` in `functions.py`
- [x] T013 [Phase 1] Create `.agents/skills/github-projects/SKILL.md` — 9 procedures, 7 guard conditions, agent access table, tool reference, Prerequisites section
- [x] T014 [Phase 1] Update `skills-lock.json` — add `github-projects` entry: `tier: functional`, `layer: 6`, `owner_agent: [mark, kabilan, matt, john, peter]`, `status: active`
- [x] T015 [Phase 1] Update `docs/architecture/skills-architecture.md` — Layer 6 table, 3 mermaid diagrams (Engineering + Product/Strategy + Knowledge/Org clusters)
- [x] T016 [P] [Phase 1] Update `.claude/agents/mark.md` — add `github-projects` trigger row to skills table
- [x] T017 [P] [Phase 1] Update `.claude/agents/kabilan.md` — add `github-projects` trigger row to skills table
- [x] T018 [P] [Phase 1] Update `.claude/agents/peter.md` — add `github-projects` trigger row to skills table
- [x] T019 [P] [Phase 1] Update `.claude/agents/matt.md` — add `github-projects` trigger row to skills table
- [x] T020 [P] [Phase 1] Update `.claude/agents/john.md` — add `github-projects` trigger row to skills table
- [x] T021 [Phase 1] Create `.agents/tools/github_projects/bootstrap-runbook.md` — Phase 0 and Phase 1 step-by-step runbook with CLI commands

### Acceptance Gate

- [x] T022 [Phase 1] `python -c "import json; d=json.load(open('skills-lock.json')); print(d['skills']['github-projects'])"` — prints entry with correct fields
- [x] T023 [Phase 1] `grep -c 'github-projects' .claude/agents/mark.md .claude/agents/kabilan.md .claude/agents/peter.md .claude/agents/matt.md .claude/agents/john.md` — each file count ≥ 1

---

## Phase 2: Seed Script + Tests

**Purpose**: `seed_backlog.py` reads specs, constructs TaskCreate objects, and dry-runs without error; all tests green.

### Tests (write first — must fail before implementation begins)

- [x] T024 [Phase 2] Created `tests/.agents/tools/github_projects/conftest.py` — sys.path shim (`__init__.py` not used; dot-prefix dirs break importlib mode); `pytest_configure` in root conftest adds `.agents/tools` to sys.path
- [x] T025 [Phase 2] Wrote tests in `tests/.agents/tools/github_projects/test_schema.py` — 11 tests covering FR-007, FR-008, date validation, `primary_agent`
- [x] T026 [Phase 2] Confirmed schema tests passed immediately (schema already implemented)
- [x] T027 [Phase 2] Wrote 9 failing tests in `tests/.agents/tools/github_projects/test_seed_backlog.py`
- [x] T028 [Phase 2] Confirmed all 9 seed tests failed before implementation

### Implementation

- [x] T029 [Phase 2] Implemented `.agents/tools/github_projects/seed_backlog.py` — `_parse_spec_title`, `_parse_spec_purpose`, `SeedResult` NamedTuple, `seed_backlog()`, `main()` CLI with dry-run skip-config shortcut
- [x] T030 [Phase 2] Schema tests: 11/11 green
- [x] T031 [Phase 2] Seed tests: 9/9 green

### Acceptance Gate

- [x] T032 [Phase 2] `uv run pytest tests/.agents/tools/github_projects/ -v` — 20/20 passed
- [x] T033 [Phase 2] Dry-run listed 12 specs (003/feature/shaped skipped; 013 excluded), exited 0
- [x] T034 [Phase 2] `uv run ruff check .agents/tools/github_projects/` — all checks passed

---

## Phase 3: Live Seed Run (After Phase 0 Complete)

**Purpose**: ≥ 10 specs visible in Backlog on the live board with correct metadata.

- [ ] T035 [Phase 3] Refresh project config after board is live: `uv run python -c "from agents.tools.github_projects import resolve_project_config; resolve_project_config(N, 'redmarklogic', force_refresh=True)"` — commit updated `project_config.json`
- [ ] T036 [Phase 3] Run dry-run against live board to confirm 0 duplicates: `uv run python .agents/tools/github_projects/seed_backlog.py --project-number N --owner redmarklogic --dry-run`
- [ ] T037 [Phase 3] Seed backlog: `uv run python .agents/tools/github_projects/seed_backlog.py --project-number N --owner redmarklogic --start-date 2026-07-01 --target-date 2026-09-01`
- [ ] T038 [Phase 3] Verify: run the `list-tasks` procedure and confirm ≥ 10 items in Backlog

### Acceptance Gate

- [ ] T039 [Phase 3] `list_tasks(config, status="Backlog")` returns ≥ 10 TaskRecord objects
- [ ] T040 [Phase 3] Each record: `record.source` starts with `specs/`, `record.task_type == "Feature"`, `record.primary_agent is not None`

---

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies)
- `[Phase N]` = which plan phase the task belongs to
- TDD is mandatory for all function work (T024–T031): write failing test first, confirm fail, implement, confirm green
- Phase 0 acceptance gate is a hard stop — do not start Phase 2 implementation until T007 and T008 pass, but seed script coding (Phase 2) can proceed in parallel since tests do not require a live board
- Commit after each task or logical group
- Run `python-static-checks` before declaring Phase 2 implementation complete
- Use `finishing-a-development-branch` skill to complete the work
