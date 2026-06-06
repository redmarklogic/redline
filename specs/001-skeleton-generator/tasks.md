# Tasks: GIR Skeleton Generator (Phases 0-3)

**Input**: [plan.md](plan.md)
**Testing conventions**: behavior-focused, equivalence classes, protocol-conforming fakes over mocks

## Phase 0: Value Objects

**Purpose**: Define `ProjectMetadata`. Consult Graeme for required fields before finalising.

### Design input (blocking)

- [ ] T001 [Phase 0] Consult Graeme: what fields are absolutely required in project metadata? Capture answer and update `ProjectMetadata` field list before T003.

### Project setup

- [ ] T002 [Phase 0] Add dependencies: `uv add python-docx pydantic`
- [ ] T003 [Phase 0] Update `pyproject.toml`: add `src/marker` to wheel packages, add `marker` to import-linter root packages, add marker-layers and marker-rl-independence contracts
- [ ] T004 [Phase 0] Create package skeleton: `src/marker/__init__.py`, `src/marker/py.typed`, `src/marker/domain/__init__.py`
- [ ] T005 [Phase 0] Create test package skeleton: `tests/marker/__init__.py`, `tests/marker/domain/__init__.py`

### Domain model

- [ ] T006 [Phase 0] Write failing tests in `tests/marker/domain/test_models.py`:
  - `ProjectMetadata` instantiates with all required fields (happy path)
  - `ProjectMetadata` raises `ValidationError` when a required field is missing (error state)
  - `ProjectMetadata` is immutable — assignment raises `ValidationError` (frozen check)
- [ ] T007 [Phase 0] Confirm tests fail: `python -m pytest tests/marker/domain/ -v`
- [ ] T008 [Phase 0] Create `src/marker/domain/models.py` with `ProjectMetadata` (frozen Pydantic model, fields confirmed with Graeme)

### Acceptance Gate

- [ ] T009 [Phase 0] Run: `.venv\Scripts\activate; python -m pytest tests/marker/ -v` — all green
- [ ] T010 [Phase 0] Run: `.venv\Scripts\activate; python -m importlinter` — contracts pass

---

## Phase 1: Function Contract + Tests

**Purpose**: Establish `DocumentFacade` protocol, `PythonDocxFacade`, and `build_skeleton()` signature with tests in Red state.

### Facade and engine

- [ ] T011 [Phase 1] Create `src/marker/domain/protocols.py` — `DocumentFacade` protocol (add_heading, add_paragraph, add_table, add_metadata_block, save). All parameters primitive types only (`str`, `int`, `list[str]`).
- [ ] T012 [Phase 1] Create `src/marker/functions/__init__.py`
- [ ] T013 [Phase 1] Write failing tests for `PythonDocxFacade` in `tests/marker/functions/test_engines.py`:
  - `add_heading` produces heading with correct text and level (happy path)
  - `add_table` produces table with correct headers (happy path)
  - `save` writes a readable DOCX to `tmp_path` (happy path)
  - `save` with invalid path raises `OSError` (error state)
- [ ] T014 [Phase 1] Confirm engine tests fail: `.venv\Scripts\activate; python -m pytest tests/marker/functions/test_engines.py -v`
- [ ] T015 [Phase 1] Create `src/marker/functions/engines.py` — `PythonDocxFacade` implementation

### Function stub and contract tests

- [ ] T016 [Phase 1] Create `tests/marker/conftest.py` — `RecordingFacade` (protocol-conforming fake that records all method calls for assertion; not a mock)
- [ ] T017 [Phase 1] Create `tests/marker/functions/__init__.py`
- [ ] T018 [Phase 1] Create `src/marker/functions/builders.py` — `build_skeleton(sections, metadata, output_path)` stub (signature only, raises `NotImplementedError`)
- [ ] T019 [Phase 1] Write failing contract tests in `tests/marker/functions/test_builders.py`:
  - Calling `build_skeleton` with valid args does not raise `TypeError` (signature check)
  - `build_skeleton` with empty `sections` list raises `ValueError`
  - `build_skeleton` with invalid `output_path` type raises `TypeError`
- [ ] T020 [Phase 1] Confirm builder contract tests fail (Red): `.venv\Scripts\activate; python -m pytest tests/marker/functions/test_builders.py -v`

### Acceptance Gate — Phase 1

- [ ] T021 [Phase 1] Engine tests green, builder contract tests in Red (both expected states confirmed)
- [ ] T022 [Phase 1] Run: `.venv\Scripts\activate; python -m pytest tests/marker/functions/test_engines.py -v` — all green

---

## Phase 2: Section Generation

**Purpose**: Implement `build_skeleton()` to produce a DOCX with headings from `list[str]`.

### Tests (write first)

- [ ] T023 [Phase 2] Extend `tests/marker/functions/test_builders.py` with section generation tests using `RecordingFacade`:
  - Happy path: `["Introduction", "Methodology", "Conclusion"]` → `add_heading` called three times in order with correct text
  - Single section: `["Executive Summary"]` → `add_heading` called once
  - Empty list: `[]` → raises `ValueError`
  - Special characters in heading name → rendered as provided, no transformation
- [ ] T024 [Phase 2] Confirm tests fail: `.venv\Scripts\activate; python -m pytest tests/marker/functions/test_builders.py -v`

### Implementation

- [ ] T025 [Phase 2] Implement `build_sections(sections, facade)` in `src/marker/functions/builders.py`
- [ ] T026 [Phase 2] Wire `build_sections` into `build_skeleton()` — replace `NotImplementedError` stub

### Integration

- [ ] T027 [Phase 2] Write integration test in `tests/marker/test_integration.py` (use `tmp_path`):
  - `build_skeleton()` with three sections produces a DOCX at the specified path
  - Reopening DOCX with `Document()` finds all three headings in order
  - Saving to non-writable path raises `OSError`

### Acceptance Gate — Phase 2

- [ ] T028 [Phase 2] Run: `.venv\Scripts\activate; python -m pytest tests/marker/ -v` — all green
- [ ] T029 [Phase 2] Open generated DOCX manually — verify headings are present and ordered (founder review)

---

## Phase 3: Metadata Table

**Status**: Blocked — requires two design inputs:

- [ ] T030 [Phase 3, blocked] Design session with Graeme: confirm required metadata fields and canonical order
- [ ] T031 [Phase 3, blocked] Decide table placement: Document Control block, cover page, or both

When unblocked, Phase 3 adds `build_metadata(metadata, facade)` and integrates it into `build_skeleton()`. Tasks to be written after design sessions complete.

---

## Phase Z: Polish

- [ ] T032 [Phase Z] Run full project test suite: `.venv\Scripts\activate; python -m pytest -v`
- [ ] T033 [Phase Z] Run ruff format: `.venv\Scripts\activate; python -m ruff format src/marker/ tests/marker/`
- [ ] T034 [Phase Z] Run static checks: `.venv\Scripts\activate; python -m ruff check src/; python -m importlinter; python -m deptry src/`
- [ ] T035 [Phase Z] Update `docs/architecture/domain-model.md`: add marker bounded context, new domain terms
- [x] T036 [Phase Z] Write ADR: error handling policy (raise vs. return sentinel) — done: ADR-014
- [ ] T037 [Phase Z] Update `src/marker/__init__.py` exports: `build_skeleton`, `ProjectMetadata`, `PythonDocxFacade`

### Acceptance Gate — Phase Z

- [ ] T038 [Phase Z] All tests green, lint clean, import contracts passing, ADR written

---

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies)
- TDD is mandatory: write failing test → confirm it fails → implement → refactor
- Use `RecordingFacade` (protocol-conforming fake) for builder tests — not `mocker.patch`
- Acceptance Gate at each phase is a hard stop — do not start next phase until it passes
- Commit after each phase acceptance gate
- Founder reviews working code at each phase gate before next phase begins
- Phase 3 tasks are intentionally thin until design sessions complete
