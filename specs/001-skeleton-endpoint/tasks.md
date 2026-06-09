# Tasks: Skeleton Endpoint (POST /skeletons returns DOCX behind auth)

**Input**: [plan.md](./plan.md) | [spec.md](./spec.md) | [data-model.md](./data-model.md) | [contracts/skeletons-post.md](./contracts/skeletons-post.md) | [research.md](./research.md)
**Prerequisites**: spec.md + plan.md complete. Branch `feature/51-platform-p-skeleton-endpoint-post-skeleton-returns-docx-behind-auth` checked out. Peter's placement decision (R1) and founder confirmations (request body = builder inputs; package name = `marker`) recorded.

<!-- Vertical-slice sizing: each phase is a complete, runnable increment. TDD mandatory:
     write failing test (Red) → confirm it fails → implement (Green) → refactor.
     Story labels: [US1] success download · [US2] unauth refused · [US3] uniform safe errors. -->

## Phase 0: Foundation — deps, bytes seam, app factory

**Purpose**: `marker.api` package boots an empty app; the builder can emit DOCX bytes; deps + import-linter contract are in place. Runnable, not stubbed.

### Tests (write first — must fail before implementation)

- [ ] T001 [P] [Phase 0] Write failing `test_build_skeleton_bytes_returns_docx_magic` in `tests/marker/functions/test_builders.py` (asserts `result[:4] == b"PK\x03\x04"` and `len(result) > 0`)
- [ ] T002 [P] [Phase 0] Write failing `test_create_app_returns_fastapi_instance` in `tests/marker/api/test_app.py`
- [ ] T003 [Phase 0] Confirm both tests fail (collect-error/red): `.venv\Scripts\activate; python -m pytest tests/marker/functions/test_builders.py::test_build_skeleton_bytes_returns_docx_magic tests/marker/api/test_app.py -v`

### Implementation

- [ ] T004 [Phase 0] Add deps in `pyproject.toml`: `fastapi`, `uvicorn` to `[project].dependencies`; `httpx`, `pytest-mock`, `openapi-spec-validator` to `[dependency-groups].test`; then `rtk uv sync`
- [ ] T005 [Phase 0] Extend the `marker layers` import-linter contract in `pyproject.toml` to `layers = [ "api", "functions", "domain" ]` (leave `marker independence` and `rl layers` unchanged)
- [ ] T006 [Phase 0] Add `to_bytes(self) -> bytes` to the `DocumentFacade` protocol in `src/marker/domain/protocols.py`
- [ ] T007 [Phase 0] Implement `PythonDocxFacade.to_bytes()` (save to `io.BytesIO`, return `.getvalue()`) in `src/marker/functions/engines.py` (depends T006)
- [ ] T008 [Phase 0] Implement `build_skeleton_bytes(structure: ReportStructure, metadata: ProjectMetadata) -> bytes` in `src/marker/functions/builders.py` (compose `build_metadata` + `build_sections`, return `doc.to_bytes()`; keep `build_skeleton(..., output_path)` unchanged) (depends T007)
- [ ] T009 [P] [Phase 0] Create `src/marker/api/__init__.py` and `src/marker/api/main.py` with `create_app() -> FastAPI` (empty app, `docs_url=None, redoc_url=None`)

### Acceptance Gate (both pass before Phase 1)

- [ ] T010 [Phase 0] Verify import boundaries: `rtk lint-imports` passes (`marker layers` api>functions>domain; `marker independence`)
- [ ] T011 [Phase 0] Run pytest green: `.venv\Scripts\activate; python -m pytest tests/marker/functions tests/marker/api -v`

---

## Phase 1: App wiring — error envelope + auth seam (structural guarantees)

**Purpose**: Every error routes through one handler producing the `{code,message,trace_id,details?}` envelope; the auth seam rejects unauthenticated callers with the bearer challenge. (Standard §3, §4, §7.) Serves **US2** + **US3**.

### Tests (write first — must fail)

- [ ] T012 [P] [Phase 1] [US2] Write failing `test_rejects_unauthenticated_with_401_and_www_authenticate` (raw `TestClient(create_app())`, asserts 401 + `www-authenticate: Bearer`) in `tests/marker/api/test_app_wiring.py`
- [ ] T013 [P] [Phase 1] [US3] Write failing `test_422_uses_error_envelope` and `test_validation_handler_returns_envelope` (no `detail` key; has `code/message/trace_id`) in `tests/marker/api/test_app_wiring.py`
- [ ] T014 [P] [Phase 1] [US3] Write failing `test_400_for_malformed_json_body` (raw `content=b"{not json"`, `Content-Type: application/json`, asserts 400 + `code: BAD_REQUEST`) in `tests/marker/api/test_app_wiring.py`
- [ ] T015 [P] [Phase 1] [US3] Write failing `test_500_envelope_contains_no_internal_detail` (patch builder to raise; assert no `/path`, `RuntimeError`, `Traceback`, `File "` in `message`) in `tests/marker/api/test_app_wiring.py`. **Use `TestClient(create_app(), raise_server_exceptions=False)`** — otherwise the unhandled exception propagates and the test never observes the 500 envelope (FastAPI testing gotcha)
- [ ] T016 [Phase 1] Add `tests/marker/api/conftest.py` with `app` fixture (`create_app()`, `dependency_overrides.clear()` teardown), an auth-bypassing client fixture (`app.dependency_overrides[require_bearer] = lambda: "test-token"`), and a separate `client_raises_off` fixture wrapping `TestClient(app, raise_server_exceptions=False)` for the 500-path test
- [ ] T017 [Phase 1] Confirm new tests fail: `.venv\Scripts\activate; python -m pytest tests/marker/api/test_app_wiring.py -v`

### Implementation

- [ ] T018 [Phase 1] [US2] Implement `require_bearer` in `src/marker/api/dependencies/auth.py` (`HTTPBearer(auto_error=False)`; raise `HTTPException(401, headers={"WWW-Authenticate": "Bearer"})` when absent; return token string otherwise). Create `src/marker/api/dependencies/__init__.py`. Docstring placeholder note: verification pending SSO #50/#73/#48b
- [ ] T019 [Phase 1] [US3] Implement `register_exception_handlers(app)` in `src/marker/api/exception_handlers.py`: `StarletteHTTPException` handler (passes `exc.headers` through), `RequestValidationError` handler (`json_invalid`→400 `BAD_REQUEST` else 422 `VALIDATION_ERROR` with `details`), **`pydantic.ValidationError` handler →422 `VALIDATION_ERROR`** (defensive — catches domain-model failures raised during DTO→domain translation so they never become 500), catch-all `Exception`→500 `INTERNAL_ERROR` (safe `message`, `logger.exception` for traceback). Module comment: wiring is the #78-gated binding (Option B placeholder)
- [ ] T020 [Phase 1] Call `register_exception_handlers(app)` inside `create_app()` in `src/marker/api/main.py` (depends T019)

### Acceptance Gate

- [ ] T021 [Phase 1] Run pytest green: `.venv\Scripts\activate; python -m pytest tests/marker/api -v` (401/400/422/500 envelope paths)

---

## Phase 2: Route + schema — the success path

**Purpose**: `POST /skeletons` accepts a valid authenticated request and streams DOCX bytes with correct headers; OpenAPI is generated and valid. (Standard §1, §5, §6, §12.) Serves **US1** (+ **US3** validation).

### Tests (write first — must fail)

- [ ] T022 [P] [Phase 2] [US1] Write failing `test_returns_docx_bytes_with_correct_headers` (mock `marker.api.routes.build_skeleton_bytes` → `b"PK\x03\x04"+...`; assert 200, DOCX `content-type`, **and that `content-type` is NOT `text/event-stream`** (§9 no-SSE), `attachment`+`.docx` in `content-disposition`, `content[:4]==b"PK\x03\x04"`) in `tests/marker/api/test_routes.py`
- [ ] T023 [P] [Phase 2] [US3] Write failing `test_rejects_missing_required_field` (422), `test_rejects_extra_fields` (422, `extra="forbid"`), `test_domain_invalid_sections_returns_422` (empty / duplicate / blank-heading sections → **422, not 500**), and `test_skeletons_route_registered_plural_unversioned` (asserts a `/skeletons` route exists and no route path contains `/v1` — §1/§14) in `tests/marker/api/test_routes.py`
- [ ] T024 [P] [Phase 2] [US1] Write failing `test_openapi_schema_is_valid` (`openapi_spec_validator.validate` on `/openapi.json`) in `tests/marker/api/test_openapi.py`
- [ ] T025 [P] [Phase 2] [US1] Write failing DTO contract tests (`valid accepted`, `missing field rejected`, `extra rejected`) in `tests/marker/api/test_schemas.py`
- [ ] T026 [Phase 2] Confirm tests fail: `.venv\Scripts\activate; python -m pytest tests/marker/api/test_routes.py tests/marker/api/test_openapi.py tests/marker/api/test_schemas.py -v`

### Implementation

- [ ] T027 [Phase 2] [US1] Implement `CreateSkeletonRequest` in `src/marker/api/schemas.py` (`model_config = {"extra": "forbid"}`; `sections: list[str]` with a `@field_validator` enforcing ≥1 item, no duplicates, each non-blank; `project_number/client_name/site_address: str = Field(min_length=1)`; `date: datetime.date`) — DTO carries **all** domain constraints so failures are `RequestValidationError`→422, not 500 (per data-model.md §1)
- [ ] T028 [Phase 2] [US1] Implement `router` + `@router.post("/skeletons", status_code=200)` in `src/marker/api/routes.py`: `Depends(require_bearer)`; translate DTO → `ReportStructure`/`ProjectMetadata`; call `build_skeleton_bytes`; sanitize `project_number` → `[A-Za-z0-9._-]` (fallback `"skeleton"`) for the filename; return `StreamingResponse(BytesIO(bytes), media_type=DOCX_MEDIA_TYPE, headers={"Content-Disposition": f'attachment; filename="{safe_name}.docx"'})`. No `try/except` (depends T027, T018, T008)
- [ ] T029 [Phase 2] Add `app.include_router(routes.router)` in `create_app()` (`src/marker/api/main.py`) (depends T028)

### Acceptance Gate

- [ ] T030 [Phase 2] Run pytest green and boot check: `.venv\Scripts\activate; python -m pytest tests/marker/api -v` and `python -m uvicorn marker.api.main:create_app --factory --port 8000` starts without error

---

## Phase 3: Contract sweep + #78 placeholder flagging

**Purpose**: Every in-scope ADR-018 clause has a passing test; placeholder status is explicit. Serves **US2** (adversarial) + clause completeness.

- [ ] T031 [P] [Phase 3] [US2] Write `test_rejects_malformed_token` (raw client with `Authorization: "NotBearer xyz"`; assert status in (401, 403)) in `tests/marker/api/test_routes.py`
- [ ] T032 [Phase 3] Verify the clause-coverage matrix ([contracts/skeletons-post.md](./contracts/skeletons-post.md) — single source) is fully green; add any missing clause test
- [ ] T033 [Phase 3] Review `src/marker/api/routes.py` confirms no per-route `try/except` (envelope is handler-only)
- [ ] T034 [Phase 3] Draft the PR note: clause-coverage table + explicit statement — "global exception handler wiring + streaming-response binding are a documented placeholder pending #78 (Option B); token verification is a placeholder pending SSO (#50/#73/#48b)"

### Acceptance Gate

- [ ] T035 [Phase 3] Full suite + imports green: `.venv\Scripts\activate; python -m pytest; rtk lint-imports`

---

## Phase Z: Polish & cross-cutting

- [ ] T036 [P] [Phase Z] Export `create_app` from `src/marker/api/__init__.py`
- [ ] T037 [Phase Z] Run static checks (`python-static-checks` skill): `rtk ruff check src/`, `pydoclint`, `codespell`
- [ ] T038 [Phase Z] End-to-end verify the four quickstart scenarios (200 / 401 / 422 / 400) per [quickstart.md](./quickstart.md)

### Acceptance Gate

- [ ] T039 [Phase Z] All tests green, lint + imports clean; PR note (T034) attached

---

## Dependencies & execution order

- **Phase order is strict**: 0 → 1 → 2 → 3 → Z. Each Acceptance Gate is a hard stop.
- **Within a phase**, `[P]` tasks (distinct files, no incomplete deps) run in parallel — chiefly the test-writing tasks.
- **Cross-phase deps**: T028 (route) depends on T027 (schema), T018 (auth), T008 (bytes seam). T020/T029 depend on the handlers/route they wire.
- **Story dependency note**: US1 (success) is only meaningful *behind* US2's auth seam, so Phase 1 (US2/US3) precedes Phase 2 (US1) despite US1 being P1 — the auth/envelope structure is the foundation the success path plugs into.

## MVP & incremental delivery

- **MVP = Phases 0–2** (US1 success + US2 unauth + US3 core validation). At the end of Phase 2 the endpoint satisfies issue #51's primary "Done when" items. Phase 3 completes clause coverage + the mandatory #78/SSO placeholder PR note; Phase Z is hygiene.

## Follow-ups (tracked separately — NOT #51 implementation tasks, NOT for Kabilan)

- **F1 (Peter)**: author the reconciliation ADR (`marker` sibling + API placement, name = `marker`) + update `docs/architecture/domain-model.md` Context Map, before #51 merges. Re-dispatch Peter — his subagent could not be resumed this session.
- **F2 (skill owner)** — *resolves analyze finding A6*: file a tracking issue to update `python-fastapi` + `python-testing-api` skill procedures from `rl.app.api.*` / `rl.skeleton_generator` to `marker.api.*` / `marker.functions.builders`, and correct the stale "openapi-spec-validator / pytest-httpx already in test deps" claim (only `schemathesis` is present). Until fixed, this plan's corrected paths (not the skill's) are authoritative for #51.

## Execution notes

- TDD is mandatory for every function task (Red → confirm fail → Green → refactor).
- Commit after each task or logical group. No push without founder instruction (AGENTS.md).
- Implementation is run via "Kabilan, implement specs/001-skeleton-endpoint/tasks.md" — **not** by this command.
