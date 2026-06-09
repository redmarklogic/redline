# Tasks: OpenAPI Documentation

**Input**: Design documents from `specs/003-openapi-docs/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md)

**Organization**: Two changes; US1 (docs enabled) is a prerequisite for US2 (browser opens to docs).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to

---

## Phase 1: Foundational — Re-enable OpenAPI docs

**Purpose**: Enable `/docs` and `/openapi.json` in the FastAPI app. Unblocks both user stories.

**WARNING CRITICAL**: Both user stories depend on this phase.

- [ ] T001 Update `create_app()` in `src/marker/api/main.py` — remove `docs_url=None, redoc_url=None`; add `title="Marker API"`, `version="0.1.0"`
- [ ] T002 Verify `tests/marker/api/test_openapi.py` passes with docs re-enabled — run `python -m pytest tests/marker/api -v` and fix any assertion that assumed docs were disabled

**Checkpoint**: `GET /docs` returns 200 via TestClient; `GET /openapi.json` returns valid schema with POST /skeletons listed; full test suite green.

---

## Phase 2: User Story 1 — Browse Interactive API Docs (Priority: P1) MVP

**Goal**: Developer runs the app and the browser opens automatically to the Swagger UI.

**Independent Test**: Run `tasks/run-app.ps1`; browser opens to `http://127.0.0.1:8765/docs`; Swagger UI renders with "Marker API 0.1.0" header and POST /skeletons listed.

### Implementation

- [ ] T003 [US1] Update `tasks/run-app.ps1` — change `Start-Process $Url` to `Start-Process "$Url/docs"` (readiness probe on `$Url` stays unchanged)

**Checkpoint**: Running `tasks/run-app.ps1` opens the browser to `/docs`. Swagger UI shows app title, version, and the POST /skeletons endpoint.

---

## Phase 3: User Story 2 — Try a Request in the Browser (Priority: P2)

**Goal**: Developer submits a test request via Swagger UI and receives a DOCX download.

**Independent Test**: Use "Try it out" in Swagger UI; submit valid payload with a Bearer token header; receive HTTP 200 and DOCX file download.

### Implementation

- [ ] T004 [US2] Manual smoke test: open `/docs`, expand POST /skeletons, click "Try it out", submit a valid payload with `Authorization: Bearer test`, confirm 200 + DOCX download

> No code change required. This phase is a manual verification gate.

**Checkpoint**: "Try it out" produces a valid DOCX download. Submitting a payload missing a required field shows a 422 error in the UI.

---

## Phase 4: Polish

- [ ] T005 [P] Confirm `python -m pytest tests/ -v` fully green after all changes
- [ ] T006 [P] Confirm `rtk lint-imports` passes (no layer changes, but verify)

---

## Dependencies & Execution Order

- **Phase 1 (Foundational)**: No dependencies — start immediately
- **Phase 2 (US1)**: Depends on Phase 1 (docs must be enabled before run-app.ps1 is useful)
- **Phase 3 (US2)**: Depends on Phase 2 (needs app running with docs open)
- **Phase 4 (Polish)**: Depends on Phase 2 code change being committed

### Parallel Opportunities

T005 and T006 (Phase 4) can run in parallel.
T001 and T003 are in different files and can be written in parallel, but T003 is only worth verifying after T001 is deployed.

---

## Implementation Strategy

### MVP (User Story 1 Only)

1. Complete Phase 1 (T001–T002)
2. Complete Phase 2 (T003)
3. Run `tasks/run-app.ps1` and confirm browser opens to `/docs`
4. Ship

### Full Delivery

1. Phase 1 → Phase 2 → Phase 3 (manual) → Phase 4
2. Total: 4 code/verification tasks + 2 polish checks
