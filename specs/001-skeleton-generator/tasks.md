# Tasks: GIR Skeleton Generator (Phases 0-3)

**Input**: [plan.md](plan.md)
**Prerequisites**: python-docx and pydantic installed via `uv add`
**Testing conventions**: `python-testing-unit` skill (behavior-focused, equivalence classes, protocol-conforming fakes)

## Phase 0: Foundation -- DocumentFacade and PythonDocxFacade

**Purpose**: Establish the `marker` package with domain models, facade protocol, and a working python-docx implementation.

### Project setup

- [ ] T001 [Phase 0] Add python-docx and pydantic dependencies: `uv add python-docx pydantic`
- [ ] T002 [Phase 0] Update `pyproject.toml`: add `src/marker` to `tool.hatch.build.targets.wheel.packages`, add `marker` to `tool.importlinter.root_packages`, add marker layers contract and marker-rl independence contract
- [ ] T003 [Phase 0] Create package structure: `src/marker/__init__.py`, `src/marker/py.typed`, `src/marker/domain/__init__.py`, `src/marker/functions/__init__.py`
- [ ] T004 [Phase 0] Create test package structure: `tests/marker/__init__.py`, `tests/marker/domain/__init__.py`, `tests/marker/functions/__init__.py`

### Domain layer (models, protocols, definitions)

- [ ] T005 [Phase 0] Write failing tests in `tests/marker/domain/test_models.py` -- test behavior, not value-object round-trips:
  - Test `SkeletonConfig.is_enabled()` returns `False` for absent flags (happy path)
  - Test `SkeletonConfig.is_enabled()` returns `True` for explicitly enabled flags
  - Test `SkeletonConfig` with unknown flag name (not in definition's `condition_flags`) raises `ValueError` (error state)
  - Note: Do NOT test `SectionSpec`, `ReportDefinition`, or `ProjectMetadata` round-trips directly -- these are frozen Pydantic value objects exercised indirectly through builder tests
- [ ] T006 [Phase 0] Confirm test fails: `.venv\Scripts\activate; python -m pytest tests/marker/domain/test_models.py -v`
- [ ] T007 [Phase 0] Create `src/marker/domain/models.py` with frozen Pydantic models: `TableSpec`, `SectionSpec`, `ReportDefinition`, `SkeletonConfig` (dict-based `flags`), `ProjectMetadata`
- [ ] T008 [Phase 0] Create `src/marker/domain/protocols.py` with `DocumentFacade` protocol (add_heading, add_paragraph, add_table, add_metadata_block, save) -- all parameters are primitive types only
- [ ] T009 [Phase 0] Create `src/marker/domain/definitions.py` with `NZ_GIR` `ReportDefinition` instance: canonical heading strings, table column headers, condition flags, section tree as `SectionSpec` children

### Functions layer (engine implementation)

- [ ] T010 [Phase 0] Write failing test for `PythonDocxFacade` in `tests/marker/functions/test_engines.py`: test `add_heading` produces correct heading text and level (happy path); test `add_table` produces table with correct headers; test `save` produces a readable DOCX file (use `tmp_path` fixture); test `save` with invalid path raises an error (error state)
- [ ] T011 [Phase 0] Confirm test fails: `.venv\Scripts\activate; python -m pytest tests/marker/functions/test_engines.py -v`
- [ ] T012 [Phase 0] Create `src/marker/functions/engines.py` with `PythonDocxFacade` implementation

### Acceptance Gate

- [ ] T013 [Phase 0] Run full marker test suite: `.venv\Scripts\activate; python -m pytest tests/marker/ -v` -- all tests green
- [ ] T014 [Phase 0] Run import-linter: `.venv\Scripts\activate; python -m importlinter` -- all contracts pass

---

## Phase 1: Mandatory and Conditional GIR Sections

**Purpose**: Build section generation logic producing all mandatory sections with conditional inclusion/exclusion and sequential renumbering.

### Tests (write first)

- [ ] T015 [Phase 1] Create `tests/marker/conftest.py` with `RecordingFacade` -- a protocol-conforming fake (not a mock) that implements `DocumentFacade` and records all method calls with arguments for later assertion
- [ ] T016 [Phase 1] Write failing tests for `build_sections()` in `tests/marker/functions/test_builders.py` using equivalence classes (not exhaustive combinations):
  - Happy path -- default config (all flags disabled): all mandatory sections present, no conditional sections, sections after Section 2 numbered 3/4/5 (Residual risk / Further work / Applicability)
  - Single conditional -- `flags={"foundation_assessment": True}`: Section 3 present, remaining sections numbered 4/5/6
  - Heading-wrapping boundary -- `flags={"slope_stability": True}` only: Section 2.4 heading is "Slope stability assessment" (no parent wrapper)
  - Multiple conditionals interacting -- `flags={"slope_stability": True, "fault_rupture": True}`: Section 2.4 heading is "Other geotechnical hazards" with subsections 2.4.1 and 2.4.2
  - Dependent flags -- `flags={"foundation_assessment": True, "ground_improvement": True}`: ground improvement subsection present in Section 3
  - Table structure -- Document Control version table has six mandatory columns
  - Table structure -- Geotechnical Model Table has six mandatory columns
  - End state -- appendix headings present in order A-D
- [ ] T017 [Phase 1] Confirm tests fail: `.venv\Scripts\activate; python -m pytest tests/marker/functions/test_builders.py -v`

### Implementation

- [ ] T018 [Phase 1] Create `src/marker/functions/builders.py` with `build_sections(definition: ReportDefinition, config: SkeletonConfig, facade: DocumentFacade)` function implementing:
  - Mandatory front matter headings (Document control, Table of contents, Client summary)
  - Mandatory Section 1 with subsections
  - Mandatory Section 2 with subsections (including Geotechnical Model Table)
  - Conditional Section 2.4 (hazard subsections with dynamic heading logic)
  - Conditional Section 2.5
  - Conditional Section 3 (foundation assessment with subsections)
  - Remaining mandatory sections with sequential renumbering
  - References heading
  - Appendix headings A-D

### Acceptance Gate

- [ ] T019 [Phase 1] Run builder tests: `.venv\Scripts\activate; python -m pytest tests/marker/functions/test_builders.py -v` -- all tests green
- [ ] T020 [Phase 1] Run full marker test suite: `.venv\Scripts\activate; python -m pytest tests/marker/ -v` -- all tests green

---

## Phase 2: Project Metadata Population

**Purpose**: Populate the Document Control block and cover page metadata from a `ProjectMetadata` object.

### Tests (write first)

- [ ] T021 [Phase 2] Write failing tests for `build_metadata()` in `tests/marker/functions/test_builders.py`:
  - Happy path -- project number, client name, site address, date, and document code appear in facade calls
  - End state -- Document Control version table is populated with metadata fields
  - Error state -- missing required metadata fields raise appropriate errors
- [ ] T022 [Phase 2] Confirm tests fail: `.venv\Scripts\activate; python -m pytest tests/marker/functions/test_builders.py::test_build_metadata -v`

### Implementation

- [ ] T023 [Phase 2] Add `build_metadata(metadata: ProjectMetadata, facade: DocumentFacade)` to `src/marker/functions/builders.py`

### Acceptance Gate

- [ ] T024 [Phase 2] Run builder tests: `.venv\Scripts\activate; python -m pytest tests/marker/functions/test_builders.py -v` -- all tests green
- [ ] T025 [Phase 2] Run full marker test suite: `.venv\Scripts\activate; python -m pytest tests/marker/ -v` -- all tests green

---

## Phase 3: Orchestrator and End-to-End Validation

**Purpose**: Wire section builder and metadata builder into `build_skeleton()` and validate with real DOCX output.

### Tests (write first)

- [ ] T026 [Phase 3] Write failing integration tests in `tests/marker/test_integration.py` (use `tmp_path` for all DOCX output):
  - Happy path -- `build_skeleton()` with default config produces a DOCX file at the specified path
  - End state -- reopening the DOCX with `Document()` finds all mandatory headings in order
  - End state -- reopening the DOCX finds the Geotechnical Model Table with correct column headers
  - End state -- reopening the DOCX finds project metadata values in the document text
  - Different starting state -- `flags={"foundation_assessment": True}` produces correctly numbered sections
  - Different starting state -- default flags (all disabled) produces renumbered sections (no gap)
  - Error state -- saving to an invalid/non-writable path raises an appropriate error
- [ ] T027 [Phase 3] Confirm tests fail: `.venv\Scripts\activate; python -m pytest tests/marker/test_integration.py -v`

### Implementation

- [ ] T028 [Phase 3] Add `build_skeleton(definition, config, metadata, facade, path)` orchestrator to `src/marker/functions/builders.py`
- [ ] T029 [P] [Phase 3] Update `src/marker/__init__.py` exports: expose `build_skeleton`, `ReportDefinition`, `SkeletonConfig`, `ProjectMetadata`, `PythonDocxFacade`, `NZ_GIR`

### Acceptance Gate

- [ ] T030 [Phase 3] Run integration tests: `.venv\Scripts\activate; python -m pytest tests/marker/test_integration.py -v` -- all tests green
- [ ] T031 [Phase 3] Run full test suite: `.venv\Scripts\activate; python -m pytest tests/marker/ -v` -- all tests green
- [ ] T032 [Phase 3] Run lint and import checks: `.venv\Scripts\activate; python -m ruff check src/marker/; python -m importlinter` -- all clean

---

## Phase Z: Polish

- [ ] T033 [P] [Phase Z] Run full project test suite: `.venv\Scripts\activate; python -m pytest -v`
- [ ] T034 [P] [Phase Z] Run ruff format: `.venv\Scripts\activate; python -m ruff format src/marker/ tests/marker/`
- [ ] T035 [Phase Z] Run full static checks: `.venv\Scripts\activate; python -m ruff check src/; python -m importlinter; python -m deptry src/`
- [ ] T036 [Phase Z] Update `docs/architecture/domain-model.md`: add marker bounded context, update subdomain classification, add new domain terms

### Acceptance Gate

- [ ] T037 [Phase Z] All tests green, lint clean, import contracts passing

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies)
- `[Phase N]` = which plan phase the task belongs to
- TDD is mandatory for all function work: write failing test (Red), confirm it fails, implement (Green), refactor
- Follow `python-testing-unit` skill: behavior-focused tests, equivalence classes over exhaustive permutations, protocol-conforming fakes over mocks, happy path first then error states
- Use `RecordingFacade` (protocol-conforming fake) for builder tests, not generic `mocker.patch`
- Each test describes its equivalence class (happy path / single conditional / interacting conditionals / error state / end state / different starting state)
- The Acceptance Gate at the end of each phase is a hard stop -- do not start the next phase until it passes
- If any function file was modified or introduced, the pytest gate is mandatory
- Commit after each task or logical group
- Use `subagent-driven-development` skill (preferred) or execute tasks directly
- Run `python-static-checks` before declaring implementation complete
- Use `finishing-a-development-branch` skill to complete the work
