# Implementation Plan: Health Check Endpoint

**Date**: 2026-06-10 | **Spec**: [spec.md](spec.md)
**Status**: Draft

## Summary

Add a `GET /health` endpoint to the Marker API (the FastAPI web service running on Cloud Run). The endpoint returns `{"status": "healthy"}` with HTTP 200. It requires no authentication credentials and does not appear in the OpenAPI schema served at `/openapi.json`. This matters because Cloud Run health-check probes and Docker daemons must be able to verify liveness without holding an API token — the only current endpoint (`POST /skeletons`) requires a bearer token and a request body, making it unusable as an infrastructure probe. The change touches one new API module, one new test file, one modification to `main.py`, and one line in the development startup script.

## Technical Context

**Language**: Python 3.14
**Package manager**: uv
**Testing**: pytest (TDD workflow per `test-driven-development` skill)
**Project layout**: monorepo (`src/marker/` package)
**Architecture**: Single-package API layer. New health router follows the existing `src/marker/api/routes.py` pattern — an `APIRouter` instance included in `main.py`. No domain layer involvement (health is a platform concern, not a domain concern).
**Dev OS**: Windows | **Deploy OS**: Linux
**Domain modeling**: N/A (no new domain types)
**Layer enforcement**: import-linter contracts in `pyproject.toml` — no new imports cross existing boundaries
**Key dependencies**: FastAPI (existing), pytest + fastapi.testclient (existing)

## Design Decisions

| # | Decision | Choice | Rationale |
|---|---|---|---|
| D1 | Status field value | `"healthy"` | All FastAPI implementation books use `"healthy"`. `"ok"` has no grounding. `"pass"` (RFC-grounded) is a future breaking-change migration. |
| D2 | Auth exclusion mechanism | Router-level isolation | Mount on a dependency-free `health_router`; never via `routes.router`. Structural isolation — testable with a single no-auth assertion. |
| D3 | OpenAPI visibility | `include_in_schema=False` | Health probe is infra contract, not API consumer contract. Must not appear in `/docs`. |
| D4 | Response model | Plain dict (no Pydantic) | All FastAPI sources return plain dict for health checks. No model needed for a one-field response. |
| D5 | 503 support | Deferred | `503` is not in `http-api-standard.md §2`. No downstream dependencies exist to probe. |

## Domain Impact

**Modularity assessment**: N/A — adding an endpoint to the existing `marker.api` package. No new top-level package.
**New packages**: None
**Bounded context changes**: None
**Import-linter contract updates**: None
**Subdomain classification**: Generic (platform infrastructure, no domain logic)
**New domain terms**: None

## Architecture

```text
Request (no auth header)
    │
    ▼
FastAPI app (main.py)
    │
    ├── health_router (health.py)        ← no dependencies=
    │       GET /health
    │       include_in_schema=False
    │       returns {"status": "healthy"}
    │
    └── routes.router (routes.py)        ← has Depends(require_bearer)
            POST /skeletons
```

The health router is registered first in `main.py` so it is unambiguously outside the protected router chain. The global exception handler in `exception_handlers.py` covers any unexpected failure on this route — no per-route error handling.

## Domain Models

None. Health endpoint returns a plain dict — no Pydantic model.

## MoSCoW

| Category | Items |
|---|---|
| **Must have** | `GET /health` returns `200 {"status": "healthy"}` with no auth required; route excluded from OpenAPI schema; structural auth isolation via separate router; `run-app.ps1` readiness probe updated to `/health` |
| **Should have** | Test confirms `/health` absent from `openapi()["paths"]`; test uses bare `TestClient` (no auth override) |
| **Could have** | Nothing |
| **Won't have (this time)** | 503 degraded response; `/ping` liveness probe; dependency health checks; Pydantic response model; `"pass"/"warn"/"fail"` RFC vocabulary; response fields beyond `status` |

## Phased Delivery

### Phase 0: Health Router + Tests

**Goal**: `GET /health` returns `200 {"status": "healthy"}` unauthenticated; excluded from OpenAPI schema; full test coverage.

**TDD approach**: Write `tests/marker/api/test_health.py` first. All four test cases (see below) should fail on first run. Implement `src/marker/api/health.py` and update `main.py` until all pass.

**Deliverables**:

1. `src/marker/api/health.py` — new file; defines `health_router = APIRouter()` with a single `GET /health` route
2. `src/marker/api/main.py` — add `app.include_router(health_router)` (no prefix, no dependencies)
3. `tests/marker/api/test_health.py` — new file; four test cases

**Verification**:

```powershell
rtk uv run pytest tests/marker/api/test_health.py -v
```

Expected: 4 passed, 0 failed.

**Acceptance Gate** (both must pass before Phase 1 starts):

- [ ] Working code: `GET /health` returns `200 {"status": "healthy"}` with no `Authorization` header
- [ ] Tests: `pytest tests/marker/api/test_health.py -v` → 4 passed, 0 failed

---

### Phase 1: OpenAPI Assertion + Run-App Probe

**Goal**: Confirm `/health` is absent from the OpenAPI schema; update `run-app.ps1` readiness probe.

**TDD approach**: Add assertion to `tests/marker/api/test_openapi.py` first. Update `run-app.ps1` after confirming the test passes.

**Deliverables**:

1. `tests/marker/api/test_openapi.py` — add `test_health_not_in_openapi_schema` assertion
2. `run-app.ps1` — update readiness-check URL from root (`$Url`) to `$Url/health`

**Verification**:

```powershell
rtk uv run pytest tests/marker/api/test_openapi.py -v
```

Expected: all existing tests pass + `test_health_not_in_openapi_schema` passes.

Run-app verification: start the app with `run-app.ps1` and confirm the readiness loop exits cleanly on `/health`.

**Acceptance Gate**:

- [ ] `pytest tests/marker/api/test_openapi.py -v` → all pass including `test_health_not_in_openapi_schema`
- [ ] `run-app.ps1` exits the readiness loop without 404 errors

## File Inventory

| Phase | File | Status |
|---|---|---|
| 0 | `src/marker/api/health.py` | New |
| 0 | `src/marker/api/main.py` | Modified |
| 0 | `tests/marker/api/test_health.py` | New |
| 1 | `tests/marker/api/test_openapi.py` | Modified |
| 1 | `run-app.ps1` | Modified |

**Total new**: 2 | **Total modified**: 3 | **Total deleted**: 0

## Library Best Practices

### fastapi.APIRouter

- **Import path**: `from fastapi import APIRouter`
- **API gotchas**: `include_in_schema=False` is set on the **route decorator**, not on the router. Setting it on the router suppresses all routes in that router from the schema; setting it on the individual route is more precise.
- **Confirmed pattern**:

  ```python
  health_router = APIRouter()

  @health_router.get("/health", include_in_schema=False)
  def health() -> dict:
      return {"status": "healthy"}
  ```

### fastapi.testclient.TestClient

- **Import path**: `from fastapi.testclient import TestClient`
- **Confirmed pattern** (no-auth test):

  ```python
  def test_health_returns_200_no_auth(app):
      client = TestClient(app)  # no dependency override — structural test
      response = client.get("/health")
      assert response.status_code == 200
      assert response.json() == {"status": "healthy"}
  ```

## Risk Register

| Risk | Mitigation |
|---|---|
| Future rate limiter is added without exempting `/health` | The plan explicitly records the exemption requirement; the tasks.md acceptance criteria for Phase 0 will reference it |
| `include_in_schema=False` is accidentally set on the router instead of the route | Test `test_health_not_in_openapi_schema` catches this — it asserts on the schema output, not the decorator |
| Auth isolation breaks if `health_router` is accidentally included via `routes.router` | The no-auth test (`TestClient(app)` with no override) is the structural enforcement — it fails immediately if auth is accidentally required |

## Glossary

| Term | Definition |
|---|---|
| Health probe | An automated HTTP request made by infrastructure tooling to verify a service is alive and able to respond |
| Liveness | A service is alive if its process is running and can accept connections |
| Readiness | A service is ready if it is alive and its downstream dependencies (database, etc.) are functional — not applicable at Phase 1 |
| `include_in_schema` | A FastAPI route parameter that controls whether the endpoint appears in the generated OpenAPI schema |
