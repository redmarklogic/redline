# Tasks: [FEATURE NAME]

**Input**: [Link to plan]
**Prerequisites**: [What must exist before starting]

<!-- Task sizing rule: each task is a VERTICAL SLICE -- front-to-back, one complete
     new behaviour, nothing left dangling. Do not split by technical layer (schema +
     logic + UI as three tasks). Split by user-visible behaviour.

     When a task feels too big, hammer the scope: trim the edges until the core
     fits the appetite. Do not extend the time budget; reduce what counts as done. -->

## Phase 0: [Name]

**Purpose**: [One line -- must describe a working, runnable deliverable]

- [ ] T001 [Phase 0] ...
- [ ] T002 [P] [Phase 0] ...
- [ ] T003 [P] [Phase 0] ...

### Acceptance Gate

- [ ] T004 [Phase 0] Verify working code: [runnable command]
- [ ] T005 [Phase 0] If function files modified -- run pytest: `.venv\Scripts\activate; python -m pytest tests/[affected] -v` -- all tests green

---

## Phase N: [Name]

**Purpose**: [One line -- must describe a working, runnable deliverable]

### Tests (write first -- must fail before implementation begins)

- [ ] T0XX [Phase N] Write failing test for [function] in tests/.../test_X.py
- [ ] T0XX [Phase N] Confirm test fails: `.venv\Scripts\activate; python -m pytest tests/.../test_X.py -v`

### Implementation

- [ ] T0XX [P] [Phase N] Create ... in src/.../X.py
- [ ] T0XX [Phase N] Implement ... in src/.../Y.py (depends on T0XX)

### Acceptance Gate

- [ ] T0XX [Phase N] Verify working code: [runnable command]
- [ ] T0XX [Phase N] Run pytest: `.venv\Scripts\activate; python -m pytest tests/[affected] -v` -- all tests green

---

## Phase Z: Polish

- [ ] TXXX [P] [Phase Z] Update __init__.py exports in src/.../
- [ ] TXXX [Phase Z] Run full test suite and lint: `.venv\Scripts\activate; python -m pytest; python -m ruff check src/`
- [ ] TXXX [Phase Z] Run end-to-end verification: [specific command]

### Acceptance Gate

- [ ] TXXX [Phase Z] All tests green and lint clean

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies)
- `[Phase N]` = which plan phase the task belongs to
- TDD is mandatory for all function work: write failing test (Red), confirm it fails, implement (Green), refactor
- The Acceptance Gate at the end of each phase is a hard stop -- do not start the next phase until it passes
- If any function file was modified or introduced, the pytest gate is mandatory
- Commit after each task or logical group
- Use `subagent-driven-development` skill (preferred) or execute tasks directly
- Run `python-static-checks` before declaring implementation complete
- Use `/make-pr` command to complete the work
