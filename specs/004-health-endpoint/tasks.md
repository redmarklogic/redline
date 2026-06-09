# Tasks: Health Check Endpoint

**Input**: Design documents from `specs/004-health-endpoint/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [contracts/health-get.md](./contracts/health-get.md)

**Organization**: US1 (liveness probe) and US2 (OpenAPI exclusion) are delivered by the same implementation. US3 (run-app probe) is independent. US1 is the MVP.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to

---

## Phase 1: TDD — Health Endpoint (US1 + US2)

**Purpose**: `GET /health` returns `{"status": "healthy"}` with HTTP 200, unauthenticated, and absent from the OpenAPI schema. All four test cases green.

**WARNING CRITICAL**: Both US1 and US2 depend on this phase. US3 is independent.

### Tests (write first — must fail before implementation begins)

- [ ] T001 [US1] Write failing test `test_health_returns_200_no_auth` in `tests/marker/api/test_health.py` — bare `TestClient(app)`, no auth override, asserts `200` and `{"status": "healthy"}`
- [ ] T002 [US1] Write failing test `test_health_returns_200_with_invalid_auth` in `tests/marker/api/test_health.py` — sends `Authorization: Bearer invalid`, asserts `200`
- [ ] T003 [US1] Write failing test `test_health_response_body_shape` in `tests/marker/api/test_health.py` — asserts response JSON has exactly one key `"status"` with value `"healthy"`
- [ ] T004 [US2] Write failing test `test_health_not_in_openapi_schema` in `tests/marker/api/test_openapi.py` — asserts `"/health"` is absent from `app.openapi()["paths"]`
- [ ] T005 Confirm all four tests fail: `rtk uv run pytest tests/marker/api/test_health.py tests/marker/api/test_openapi.py::test_health_not_in_openapi_schema -v`

### Implementation

- [ ] T006 [P] [US1] Create `src/marker/api/health.py` — define `health_router = APIRouter()` with `@health_router.get("/health", include_in_schema=False)` returning `{"status": "healthy"}`. No `Depends`, no response model.
- [ ] T007 [US1] Update `src/marker/api/main.py` — add `from marker.api.health import health_router` and `app.include_router(health_router)` with no prefix and no dependencies (place before the existing `app.include_router(router)` call)

### Acceptance Gate

- [ ] T008 [US1] Verify `GET /health` returns `200` with no `Authorization` header (manual check via TestClient or curl)
- [ ] T009 Run pytest: `rtk uv run pytest tests/marker/api/test_health.py tests/marker/api/test_openapi.py -v` — all tests green including `test_health_not_in_openapi_schema`

---

## Phase 2: User Story 3 — Developer Script Readiness Check (Priority: P3)

**Goal**: `run-app.ps1` readiness probe polls `/health` and exits cleanly on `200`.

**Independent Test**: Run `run-app.ps1`; script exits the polling loop without 404 errors. The health response is the exit signal.

### Implementation

- [ ] T010 [US3] Update `run-app.ps1` — change the readiness-check URL from `$Url` (root) to `$Url/health`; verify script exits when it receives `200` from `/health`

### Acceptance Gate

- [ ] T011 [US3] Manual verification: run `run-app.ps1`, confirm readiness loop exits on `200 {"status": "healthy"}` from `/health` — no 404 in the polling output

---

## Phase 3: Polish

- [ ] T012 [P] Run full test suite: `rtk uv run pytest tests/ -v` — all tests green
- [ ] T013 [P] Run ruff: `rtk uv run ruff check src/marker/api/health.py` — clean
- [ ] T014 [P] Confirm `GET /health` is absent from `/docs` (load Swagger UI and verify no health entry)
- [ ] T015 [P] Add a `# NOTE: exempt from rate limiting` comment in `src/marker/api/health.py` above the route to make the forward-looking exemption requirement visible to future implementers (FR-006)

### Acceptance Gate

- [ ] T016 All tests green, lint clean, `/health` absent from Swagger UI

---

## Dependencies & Execution Order

- **Phase 1 (US1+US2)**: No dependencies — start immediately
- **Phase 2 (US3)**: No dependencies on Phase 1 — can run in parallel with Phase 1
- **Phase 3 (Polish)**: Depends on Phase 1 and Phase 2 complete

### Parallel Opportunities

- T006 (`health.py`) and T001–T004 (test writing) are in different files — can be worked in parallel by separate agents, but tests must fail before T006 is considered complete.
- T010 (`run-app.ps1`) is independent of all Phase 1 work — can run in a separate thread.
- T012, T013, T014 (polish) are fully parallel.

---

## Implementation Strategy

### MVP (User Story 1 only)

1. T001 → T005 (write and confirm failing tests)
2. T006 → T007 (implement health router and wire into main.py)
3. T008 → T009 (verify 200 and all tests green)
4. Ship

### Full Delivery

Phase 1 (T001–T009) → Phase 2 (T010–T011) → Phase 3 (T012–T015)

Total: 16 tasks. Estimated: half a day per plan appetite.
