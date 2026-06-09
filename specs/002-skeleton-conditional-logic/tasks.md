# Tasks: Skeleton Conditional Section Logic — Input Model

**Input**: Design documents from `specs/002-skeleton-conditional-logic/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Format**: `[ID] [P?] [Story?] Description — file path`

- **[P]**: Parallelizable (different files, no incomplete dependencies)
- **[Story]**: User story label (US1–US4 from spec.md)

---

## Phase 1: Foundational — Input Schema

**Purpose**: Define the HTTP request contract. All user stories depend on this schema being correct.
Phase 2 (domain) can begin in parallel once `HazardCategory` is defined (T001).

**Checkpoint**: `SkeletonRequest` parses correctly; Pydantic rejects unknown enum values.

- [ ] T001 Define `HazardCategory` enum (18 values per data-model.md) in `src/marker/api/schemas.py`
- [ ] T002 Define `SectionFlags` Pydantic model (8 fields, all optional, `extra="forbid"`, frozen) in `src/marker/api/schemas.py`
- [ ] T003 Define `ReportContext` Pydantic model (`jurisdiction: Literal["NZ"]`, `report_type: Literal["GAR"]`, both required) in `src/marker/api/schemas.py`
- [ ] T004 Define `ProjectMetadataDTO` Pydantic model (4 optional fields: `project_number`, `client_name`, `site_address`, `report_date`) in `src/marker/api/schemas.py`
- [ ] T005 Define `SkeletonRequest` Pydantic model (`project_metadata: ProjectMetadataDTO | None`, `report_context: ReportContext`, `section_flags: SectionFlags | None`); delete `CreateSkeletonRequest` in `src/marker/api/schemas.py`

---

## Phase 2: Foundational — Domain Activation Function (TDD)

**Purpose**: The pure `activate_sections` function is the core of this feature. No user story can be
verified without it. All 11+ test cases from the pitch are encoded here before implementation.

**Checkpoint**: All unit tests for `activate_sections` pass; determinism confirmed.

- [ ] T006 Write failing unit tests for `activate_sections` (all test cases below) in `tests/marker/domain/test_section_activation.py`:
  - Architectural constraint 1: same input → same output (N calls, assert stability)
  - Architectural constraint 5: absent/null `section_flags` → mandatory sections only
  - Architectural constraint 6: `retaining_walls_present: True` → section id `"8.4"` in result
  - Mapping: `SLOPE_INSTABILITY` → `{"7.5", "7.7", "7.13"}` (and no others from that set)
  - Mapping: `OTHER` absent → `"7.15"` not in result
  - Mapping: `OTHER` present → `"7.15"` in result
  - Mapping: `FAULT_RUPTURE` → `"7.NZ-1"` (not `"7.15"`, not absent)
  - Mapping: `COMPRESSIBLE_SOILS` → `"7.4"` (not `"7.12"`)
  - Mapping: `FALLING_DEBRIS` → `"7.11"` without `SLOPE_INSTABILITY` in hazards
  - Mapping: `FLOODING` → `"7.14"`; `flooding_info_uncertain: True` → section id for 4.3 modifier; both together activate both independently
  - Mapping: `foundation_recommendations_required: True` → `"8.2"` and `"8.2.1"` through `"8.2.9"` all in result
  - Mandatory: section id `"7"` always in result regardless of flags
- [ ] T007 Define `SectionID` type alias, `SECTION_HEADINGS: dict[SectionID, str]` (all sections from data-model.md; NZ extensions use placeholder strings), and `SECTION_ORDER: tuple[SectionID, ...]` (guideline document order) in `src/marker/domain/section_activation.py`
- [ ] T008 Implement `activate_sections(flags: SectionFlags) -> frozenset[SectionID]` using lookup table over `HazardCategory` → `SectionID` mapping; handle `SLOPE_INSTABILITY` one-to-many mapping; handle `OTHER` explicit-only rule; handle Tier A flags; always include mandatory sections in `src/marker/domain/section_activation.py`
- [ ] T009 Run `rtk pytest tests/marker/domain/test_section_activation.py` — all tests must pass

---

## Phase 3: User Story 1 — Contextually Accurate Skeleton (Priority: P1)

**Goal**: A request with specific section flags produces a skeleton containing exactly those sections.

**Independent Test**: POST with `hazards: ["LIQUEFACTION", "SLOPE_INSTABILITY"]` + `earthworks_proposed: true`.
Confirm response is 200 and the DOCX contains Sections 7.1, 7.5, 7.7, 7.13, 8.3 — and no other conditional sections.

- [ ] T010 [US1] Write failing integration tests for US1 acceptance scenarios 1–7 in `tests/marker/api/test_routes.py`:
  - POST `hazards: [LIQUEFACTION, SLOPE_INSTABILITY]` → DOCX contains 7.1, 7.5, 7.7, 7.13 only (no other hazard sub-sections)
  - POST `earthworks_proposed: true` → DOCX contains 8.3
  - POST `foundation_recommendations_required: true` → DOCX contains 8.2 + 8.2.1–8.2.9
  - POST `retaining_walls_present: true` → DOCX contains 8.4
  - POST `hazards: [FLOODING]` + `flooding_info_uncertain: true` → DOCX contains 7.14 AND 4.3 modifier
  - POST `hazards: [FAULT_RUPTURE]` → DOCX contains 7.NZ-1 (not 7.15)
  - POST `hazards: [SLOPE_INSTABILITY]` → activated section set contains exactly 7.5, 7.7, 7.13 (no extras from that group)
- [ ] T011 [US1] Update route handler to: (1) parse `SkeletonRequest`, (2) call `activate_sections(request.section_flags or SectionFlags())`, (3) filter `SECTION_ORDER` to activated IDs, (4) map to heading strings via `SECTION_HEADINGS`, (5) construct `ReportStructure`, (6) call `build_skeleton_bytes`, (7) return DOCX response in `src/marker/api/routes.py`
- [ ] T012 [US1] Run `rtk pytest tests/marker/api/test_routes.py -k us1` — all US1 tests must pass

**Checkpoint**: US1 is fully functional. An engineer with specific site conditions receives a correctly scoped skeleton.

---

## Phase 4: User Story 2 — Safe Defaults / No Flags (Priority: P1)

**Goal**: A request with no `section_flags` returns a skeleton with mandatory sections only.

**Independent Test**: POST with no `section_flags` field. Confirm 200 and skeleton contains mandatory
sections (including Section 7 heading) but no hazard sub-sections and no conditional sections.

- [ ] T013 [US2] Write failing integration tests for US2 acceptance scenarios 1–3 in `tests/marker/api/test_routes.py`:
  - POST with no `section_flags` field → 200; skeleton has no conditional sections
  - POST with `section_flags: null` → same result
  - POST with `section_flags: {}` (all fields absent) → same result
- [ ] T014 [US2] Run `rtk pytest tests/marker/api/test_routes.py -k us2` — all US2 tests must pass (no code change expected if T011 implemented correctly; tests validate the edge case)

**Checkpoint**: Safe defaults verified. A practitioner who omits flags never receives an over-scoped skeleton.

---

## Phase 5: User Story 3 — Invalid Input Rejected (Priority: P1)

**Goal**: Unknown enum values return 422 with no document generated.

**Independent Test**: POST with `report_type: "GBR"` → 422. POST with `hazards: ["VOLCANO"]` → 422. POST
with no `report_context` → 422.

- [ ] T015 [US3] Write failing schema unit tests in `tests/marker/api/test_schemas.py`:
  - `SkeletonRequest` with `report_type: "GBR"` raises `ValidationError`
  - `SkeletonRequest` with `hazards: ["VOLCANO"]` raises `ValidationError`
  - `SkeletonRequest` without `report_context` raises `ValidationError`
- [ ] T016 [US3] Write failing integration tests for US3 acceptance scenarios 1–3 in `tests/marker/api/test_routes.py`:
  - POST `report_type: "GBR"` → 422; no DOCX bytes in response body
  - POST `hazards: ["VOLCANO"]` → 422
  - POST no `report_context` → 422
- [ ] T017 [US3] Run `rtk pytest tests/marker/api/test_schemas.py tests/marker/api/test_routes.py -k us3` — all US3 tests must pass (Pydantic `Literal` types and `HazardCategory` enum handle this; no additional implementation needed if T001–T005 are correct)

**Checkpoint**: Contract enforced. No silent defaults. Unknown values always return 422.

---

## Phase 6: User Story 4 — Auditable Generation (Priority: P2)

**Goal**: Every generation event produces a log entry containing the submitted flags and activated sections.

**Independent Test**: Generate a skeleton with specific flags. Capture log output. Assert the log entry
contains both the `section_flags` dict and the sorted `activated_sections` list.

- [ ] T018 [US4] Write failing test using `caplog` fixture in `tests/marker/api/test_routes.py`:
  - After a successful POST, assert one `INFO`-level log entry exists with `section_flags` and `activated_sections` keys
- [ ] T019 [US4] Add a structured `INFO`-level log entry to route handler after `activate_sections` call in `src/marker/api/routes.py`
- [ ] T020 [US4] Run `rtk pytest tests/marker/api/test_routes.py -k us4` — audit test must pass

**Checkpoint**: Generation events are traceable. Audit log entry includes both the input flags and the output section set.

---

## Phase 7: Polish & Verification

**Purpose**: Full suite validation, linting, and edge case verification.

- [ ] T021 Run `rtk pytest tests/marker/` — full test suite for marker package; all tests pass including regression tests from 001
- [ ] T022 [P] Run `rtk lint` (import-linter) — verify `marker independence` contract holds; no `rl → marker` or `marker → rl` imports introduced
- [ ] T023 [P] Run `rtk ruff check src/marker/api/schemas.py src/marker/domain/section_activation.py` — no ruff violations
- [ ] T024 [P] Verify edge case and always-present section tests passing: 8.5 and 8.6 present in every skeleton regardless of flags; `OTHER` absent → no 7.15; `COMPRESSIBLE_SOILS` → 7.4 not 7.12; `FALLING_DEBRIS` → 7.11 independent of `SLOPE_INSTABILITY`; `FAULT_RUPTURE` → 7.NZ-1 not 7.15

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Schema)**: No dependencies — start immediately
- **Phase 2 (Domain)**: Depends on T001 (`HazardCategory`) from Phase 1 — can overlap with T002–T005
- **Phase 3 (US1)**: Depends on Phase 1 + Phase 2 complete
- **Phase 4 (US2)**: Depends on Phase 3 complete (tests the same route with different input)
- **Phase 5 (US3)**: Depends on Phase 1 complete (schema validation is Pydantic-native); can start after T005
- **Phase 6 (US4)**: Depends on Phase 3 complete (extends the route handler)
- **Phase 7 (Polish)**: Depends on all story phases complete

### Parallel Opportunities Within Phases

```text
Phase 1: T001 → [T002 || T003] → T004 → T005
Phase 2: T006 → T007 → T008 → T009
         (T006 can begin once T001 done; T007 can begin once T001 done in parallel with T006)
Phase 5: T015 can run in parallel with Phase 3 (T010–T012) — both depend on Phase 1 only
```

### Critical Path

```text
T001 → T007 → T008 → T009 → T010 → T011 → T012
              (activate_sections tests + impl + pass → route wiring → US1 tests pass)
```

---

## Implementation Strategy

### MVP (US1 + US2 + US3 — all P1)

1. Complete Phase 1 (Schema)
2. Complete Phase 2 (Domain function, TDD)
3. Complete Phase 3 (Route wiring, US1)
4. Complete Phases 4 + 5 (US2 + US3 — thin; mostly tests of existing code)
5. **STOP and VALIDATE**: Run full test suite; confirm 001 regression tests still pass

### Increment 2 (US4 — P2)

6. Complete Phase 6 (Audit logging)
7. Complete Phase 7 (Polish)

---

## Notes

- T002 and T003 are parallelizable (both add new models to `schemas.py` at different class positions)
- Phase 5 (US3 validation) is nearly free implementation-wise — Pydantic `Literal` types and `HazardCategory` enum reject invalid values automatically once T001–T005 are done
- The `SECTION_ORDER` constant in T007 must be verified manually against the pitch activation table (Part 3) before T008 is written — get this wrong and all route tests fail
- NZ extension headings (7.NZ-1, 7.NZ-2, 7.NZ-3) use placeholder strings in `SECTION_HEADINGS`; this does not block any test
- Sections 8.5 and 8.6 are in `SECTION_ORDER` and `SECTION_HEADINGS` as always-included; no flag controls them