# Implementation Plan: Skeleton Endpoint (POST /skeletons returns DOCX behind auth)

**Date**: 2026-06-09 | **Spec**: [spec.md](./spec.md) | **Branch**: `feature/51-platform-p-skeleton-endpoint-post-skeleton-returns-docx-behind-auth`
**Status**: Draft

## Summary

We are exposing Redline's existing report-skeleton builder over an authenticated HTTP endpoint — `POST /skeletons` — that returns a Word document (`.docx`) as a download. This is the system's **first north-south (external) HTTP surface**: the first interface a caller from outside the codebase crosses. The builder logic already exists (`marker.functions.builders.build_skeleton`); this feature adds only the **transport boundary** around it — a uniform, safe, authenticated contract defined by [ADR-018](../../docs/adr/adr-018-external-http-api-contract-conventions.md) and the live [HTTP API Standard](../../docs/architecture/api/http-api-standard.md). The new code is a thin HTTP layer (`src/marker/api/`): a request schema, a route that streams DOCX bytes, a bearer-auth seam, and a single global error handler producing the `{code, message, trace_id, details?}` envelope. Per Peter's architecture decision (see Design Decisions D1), the API is a new top layer **inside the `marker` package**, depending inward on the existing builder; it never reaches the document engine directly (ADR-004 stays intact).

## Technical Context

**Language**: Python 3.14
**Package manager**: uv
**Testing**: pytest (TDD workflow per `test-driven-development` skill); FastAPI `TestClient` (in-process ASGI)
**Project layout**: `monorepo` (read from `.specify/architecture.yml`; `hub_package: rl`)
**Architecture**: Sibling packages under `src/` (`marker`, `rl`), each with internal layers. `marker` gains a new top layer `api` above `functions` > `domain`. The `rl` hub is untouched by #51.
**Dev OS**: Windows | **Deploy OS**: Linux (single Cloud Run service)
**Domain modeling**: Pydantic `BaseModel` (frozen domain models already exist: `ReportStructure`, `ProjectMetadata`)
**Layer enforcement**: import-linter contracts in `pyproject.toml`. The `marker layers` contract is extended to `["api", "functions", "domain"]` (api highest).
**Primary new dependencies**: `fastapi`, `uvicorn` (serve), `python-docx` (already present — bytes-seam). Test-only: `httpx` (TestClient transport), `pytest-mock`, `openapi-spec-validator`. `schemathesis>=3.0` already present (property tests gated — see Risk Register).
**Framework-binding caveat**: FastAPI is the assumed framework (named throughout ADR-018, the live standard's "FastAPI bindings" appendix, the `python-fastapi` skill, and issue #51's "load `fastapi-http-api` skill"). The two framework-level realisations ADR-018 lists as **pending #78** — the global-exception-handler wiring and the streaming-response object — ship now as a **documented placeholder** (issue #51 "Option B" ordering). See Design Decisions D5 and Risk Register.

## Design Decisions

| #  | Decision | Choice | Rationale |
| -- | -------- | ------ | --------- |
| D1 | Where the HTTP API layer lives | New top layer `src/marker/api/` **inside** the existing `marker` package — not `rl`, not a new sibling | Peter's architecture decision (founder-routed). The endpoint wraps the skeleton builder, which lives in `marker`; #51 spans one bounded context, so routing through the `rl` hub buys nothing. The `marker`/`rl` import-independence contract stands. (See research.md for the full decision.) |
| D2 | Dependency direction | `api → functions → domain`; transport imports the builder + domain models; builder/domain import nothing in `api`; `api` never imports `functions.engines` or `python-docx` | Keeps the builder unaware it is called over HTTP (the CLI `create_skeleton.py` keeps working unchanged); preserves ADR-004's primitives-only facade boundary by never letting transport near the engine. Enforced by extending the `marker layers` import-linter contract. |
| D3 | Bytes seam (builder returns bytes, not a path) | Add `DocumentFacade.to_bytes() -> bytes` (a `BytesIO` save) + a functions-layer `build_skeleton_bytes(structure, metadata) -> bytes`; keep `build_skeleton(..., output_path)` for the CLI | The HTTP contract needs in-memory bytes streamed in the body (Standard §6); the existing builder only writes to disk. `bytes` is a primitive → the facade addition is ADR-004-compliant. Seam lives in `functions`, not `api` (Peter interim §2), so it is framework-agnostic and survives #78. |
| D4 | Request body shape | A transport DTO `CreateSkeletonRequest` in `api/schemas.py` (`extra="forbid"`) mirroring the builder inputs (sections + project metadata); the route translates it into the domain `ReportStructure` / `ProjectMetadata` before calling the builder | Founder-confirmed: #51 is a thin wrapper over `build_skeleton`. Transport DTO stays separate from the domain model so HTTP-only concerns never leak inward (`python-testing-api`: DTOs and domain models must be separate classes). |
| D5 | Error envelope + 422/400 + auth | Single global exception handler (`register_exception_handlers`) at app startup; `RequestValidationError` → 422, `json_invalid` → 400, **`pydantic.ValidationError` (raised in DTO→domain translation) → 422**; one `require_bearer` dependency → 401 + `WWW-Authenticate: Bearer`; token *verification* stubbed | Structural guarantee per Standard §3 — never per-route `try/except`. Patterns taken verbatim from the `python-fastapi` `app-wiring.md` procedure. The handler **wiring** and the **streaming-response object** are the only #78-gated pieces; they ship as a placeholder flagged in the PR (Option B). Token verification is a placeholder pending SSO (#50 / #73 / #48b). |
| D6 | No `/v1/`, no SSE, generated OpenAPI | Unversioned path `/skeletons`; no `text/event-stream`; FastAPI auto-generates `/openapi.json` | Standard §14 (versioning deferred), §9 (synchronous-endpoint honesty constraint — no SSE), §12 (OpenAPI generated from implementation, never hand-authored). |

## Domain Impact

**Modularity assessment**: No new top-level package. A new **internal layer** (`api`) is added to the existing `marker` package. Signals from the decision matrix: *conceptual cohesion* (the HTTP surface for the skeleton context belongs with that context) and *rate of change* (transport is volatile per ADR-017; isolating it in its own layer contains the churn). Routing through `rl` was rejected — no cross-context composition exists yet.
**New packages**: None.
**Bounded context changes**: None to the boundary itself; the `marker` context gains a delivery (transport) layer. The *recorded* Context Map in `docs/architecture/domain-model.md` is stale (predates the `marker` package) — **Peter owns a documentation-reconciliation ADR + Context Map update**; tracked as a follow-up, **does not block #51** (see research.md §Reconciliation).
**Import-linter contract updates**: Extend the existing `marker layers` contract:

```toml
[[tool.importlinter.contracts]]
name = "marker layers"
type = "layers"
layers = [ "api", "functions", "domain" ]   # was [ "functions", "domain" ] — api added on top
containers = [ "marker" ]
```

The `marker independence` and `rl layers` contracts are unchanged.
**Subdomain classification**: Supporting (thin transport over an existing builder; transaction-script style, no rich domain model added).
**New domain terms**: None. (Transport terms — error envelope, bearer token — are stack terms, not domain terms.)

## Architecture

**Layering (one-way dependencies):**

```
HTTP request
   │
   ▼
marker.api            (NEW top layer — transport / north-south boundary)
   ├─ main.py                 create_app(): FastAPI factory; registers handlers; includes router
   ├─ routes.py               POST /skeletons → StreamingResponse(.docx bytes)
   ├─ schemas.py              CreateSkeletonRequest (extra="forbid") — transport DTO
   ├─ exception_handlers.py   register_exception_handlers(): envelope, 422/400 split, 500-safe
   └─ dependencies/auth.py    require_bearer(): 401 + WWW-Authenticate: Bearer (verification stubbed)
   │   (imports inward ▼; never imports functions.engines or python-docx)
   ▼
marker.functions      (EXISTING)
   └─ builders.py             build_skeleton(..., output_path)  [unchanged, CLI]
                              build_skeleton_bytes(structure, metadata) -> bytes  [NEW seam]
   │
   ▼
marker.domain         (EXISTING)
   ├─ models.py               ReportStructure, ProjectMetadata  [unchanged]
   └─ protocols.py            DocumentFacade + .to_bytes() -> bytes  [NEW method]
```

**Request → response flow for `POST /skeletons`:**

1. `require_bearer` dependency runs first. No/invalid `Authorization: Bearer` → raise `HTTPException(401, headers={"WWW-Authenticate": "Bearer"})` → global handler emits envelope. (Token verification is a stub: presence-only at v0.1.)
2. FastAPI parses + validates the body against `CreateSkeletonRequest`. Unparseable → `RequestValidationError(json_invalid)` → global handler → `400`. Parsed-but-invalid (missing field, blank/duplicate heading, empty sections) → `RequestValidationError` → `422`. Both via the envelope.
3. Route translates the DTO → domain `ReportStructure` + `ProjectMetadata`. The DTO mirrors **all** domain constraints, so a semantic failure is caught at step 2 as `RequestValidationError` → `422`; a defensive `pydantic.ValidationError` → `422` handler covers anything that slips through the DTO — it must **never** fall to the catch-all `500` (see data-model §1; this is the top analyze finding).
4. Route calls `build_skeleton_bytes(structure, metadata)` → `bytes`.
5. Route returns `StreamingResponse(BytesIO(bytes), media_type=DOCX_MEDIA_TYPE, headers={Content-Disposition: attachment; filename="<safe-name>.docx"}, status_code=200)`, where `<safe-name>` is `project_number` sanitized to `[A-Za-z0-9._-]` (fallback `"skeleton"`) — an unsanitized value could break/inject the header.
6. Any unhandled exception → catch-all handler → `500` with a safe `message` (no stack/path/class leak); full traceback goes to the logger only.

**Layer rules (enforced):** `functions`/`domain` MUST NOT import `marker.api` (import-linter `marker layers`). `marker.api` MUST NOT import `marker.functions.engines` or `docx`. `marker` MUST NOT import `rl` and vice-versa (`marker independence`).

## Domain Models

**New / changed (sketches — become real code in implementation):**

- `marker/api/schemas.py` — `CreateSkeletonRequest(BaseModel)`, `model_config = {"extra": "forbid"}`. Fields mirror the builder inputs:
  - `sections: list[str]` (≥1, unique, non-blank) — maps to `ReportStructure`.
  - `project_number: str`, `client_name: str`, `site_address: str`, `date: datetime.date` — map to `ProjectMetadata`.
  - DTO carries `@field_validator`s mirroring the domain rules (sections ≥1/unique/non-blank; metadata strings `min_length=1`) so failures are caught as `RequestValidationError` → `422`. The route then constructs `ReportStructure.model_validate({"Sections": [{"Heading": s} for s in sections]})` and `ProjectMetadata.model_validate({...})`; a defensive `pydantic.ValidationError` → `422` handler guarantees a domain rule the DTO does not mirror still returns `422`, never `500` (the frozen domain models' own validation does **not** auto-convert to `422` — see data-model §1).
- `marker/domain/protocols.py` — add `DocumentFacade.to_bytes(self) -> bytes`.
- `marker/functions/engines.py` — `PythonDocxFacade.to_bytes()` saves to a `BytesIO` and returns `.getvalue()`.
- `marker/functions/builders.py` — add `build_skeleton_bytes(structure: ReportStructure, metadata: ProjectMetadata) -> bytes` composing `build_metadata` + `build_sections` then `doc.to_bytes()`.

**Reused unchanged:** `ReportStructure`, `ProjectMetadata`, `SectionHeading` (`marker.domain.models`).

## MoSCoW

| Category | Items |
| -------- | ----- |
| **Must have** | `POST /skeletons` returns `200` + DOCX bytes with correct `Content-Type`/`Content-Disposition` (§6); `401` + `WWW-Authenticate: Bearer` when unauthenticated (§7); uniform error envelope on every error with no internal leakage (§3); `422` for parsed-but-invalid, `400` for unparseable (§4); single global exception handler (§3); no `/v1/` prefix (§14); no SSE (§9); generated OpenAPI (§12); one contract test per in-scope clause; PR note stating handler is placeholder vs final (#78). |
| **Should have** | Bytes seam in `functions` (D3) so the builder stays disk-free for HTTP; adversarial auth test (malformed `Authorization` scheme); 500-safety test patching the builder to raise. |
| **Could have** | Schemathesis property-based conformance test (gated on principal-engineer approval — see Risk Register); request-ID middleware to share one `trace_id` across log + response. |
| **Won't have (this time)** | LOE upload / metadata extraction (Feature M); standards-grounded clause content (Feature N); quota + audit trail; conditional section logic (blocked pending Peter shaping); `202`+poll / SSE progress; `Accept: application/json` violations representation; by-reference (signed-URL) artifact exchange; real token verification (SSO #50/#73/#48b); versioning. |

## Phased Delivery

> TDD throughout: write the failing test first, then the code. Tests live under `tests/marker/api/` (mirroring `src/marker/api/`) plus `tests/marker/functions/` for the bytes seam. Contract-test patterns come verbatim from `python-fastapi/procedures/contract-testing.md` and `python-testing-api` — **with import paths corrected to `marker.api.*`** (the skill's `rl.app.api.*` / `rl.skeleton_generator` paths are stale placeholders — see research.md §Skill-path drift).

### Phase 0: Foundation — deps, bytes seam, app factory

**Goal**: The `marker.api` package exists with a bootable empty app, dependencies are installed, the import-linter contract is extended, and the builder can produce DOCX bytes. Runnable, not stubbed.

**TDD approach**:
- `tests/marker/functions/test_builders.py` — add `test_build_skeleton_bytes_returns_docx_magic` (asserts `result[:4] == b"PK\x03\x04"` and is non-empty). Write first.
- `tests/marker/api/test_app.py` — `test_create_app_returns_fastapi_instance`. Write first.

**Deliverables**:
1. `pyproject.toml` — add `fastapi`, `uvicorn` to `dependencies`; add `httpx`, `pytest-mock`, `openapi-spec-validator` to the `test` group; extend `marker layers` import-linter contract to `["api","functions","domain"]`.
2. `src/marker/domain/protocols.py` — `DocumentFacade.to_bytes() -> bytes`.
3. `src/marker/functions/engines.py` — `PythonDocxFacade.to_bytes()`.
4. `src/marker/functions/builders.py` — `build_skeleton_bytes(structure, metadata) -> bytes`.
5. `src/marker/api/__init__.py`, `src/marker/api/main.py` — `create_app()` (empty app, docs disabled in prod).

**Verification**:

```
rtk uv sync
rtk lint-imports            # marker layers + independence contracts pass
.venv\Scripts\activate; python -m pytest tests/marker/functions/test_builders.py tests/marker/api/test_app.py -v
```

**Acceptance Gate** (both must pass before Phase 1):
- [ ] Working code: `create_app()` boots; `build_skeleton_bytes` returns valid DOCX bytes end-to-end.
- [ ] `python -m pytest tests/marker/functions tests/marker/api -v` green; `lint-imports` green.

---

### Phase 1: App wiring — error envelope + auth seam (structural guarantees)

**Goal**: Every error routes through one handler producing the envelope; auth seam rejects unauthenticated callers with the bearer challenge. (Standard §3, §4, §7.)

**TDD approach** (all written first; patterns from `contract-testing.md`):
- `tests/marker/api/test_app_wiring.py` — `test_rejects_unauthenticated_with_401_and_www_authenticate`; `test_422_uses_error_envelope`; `test_400_for_malformed_json_body`; `test_validation_handler_returns_envelope` (no `detail` key); `test_500_envelope_contains_no_internal_detail`.

**Deliverables**:
1. `src/marker/api/dependencies/auth.py` — `require_bearer` (presence-only; `HTTPBearer(auto_error=False)`; 401 + `WWW-Authenticate: Bearer`). **Placeholder note in docstring**: verification pending SSO #50/#73/#48b.
2. `src/marker/api/exception_handlers.py` — `register_exception_handlers(app)`: `StarletteHTTPException` (passes `headers` through — carries `WWW-Authenticate`), `RequestValidationError` (`json_invalid`→400 else 422), **`pydantic.ValidationError`→422** (defensive, for DTO→domain translation failures), catch-all `Exception`→500-safe. **Placeholder note**: wiring is the #78-gated binding (Option B).
3. `src/marker/api/main.py` — `create_app()` calls `register_exception_handlers`.

**Verification**:

```
.venv\Scripts\activate; python -m pytest tests/marker/api/test_app_wiring.py -v
```

**Acceptance Gate**:
- [ ] Working code: a raw `TestClient(create_app())` returns the envelope for 401/400/422/500 paths.
- [ ] `python -m pytest tests/marker/api -v` green.

---

### Phase 2: Route + schema — the success path

**Goal**: `POST /skeletons` accepts a valid authenticated request and streams DOCX bytes with correct headers; OpenAPI is generated and valid. (Standard §1, §5, §6, §12.)

**TDD approach** (written first):
- `tests/marker/api/test_routes.py` — `test_returns_docx_bytes_with_correct_headers` (mock `marker.api.routes.build_skeleton_bytes`, assert `200`, `Content-Type`, `Content-Disposition`, `content[:4]==b"PK\x03\x04"`); `test_rejects_missing_required_field` (422); `test_rejects_extra_fields` (422, `extra="forbid"`).
- `tests/marker/api/test_openapi.py` — `test_openapi_schema_is_valid` (`openapi_spec_validator.validate`).
- `tests/marker/api/test_schemas.py` — DTO contract tests (valid accepted; missing field rejected; extra rejected).

**Deliverables**:
1. `src/marker/api/schemas.py` — `CreateSkeletonRequest` (D4).
2. `src/marker/api/routes.py` — `router`; `@router.post("/skeletons", status_code=200)`; DTO→domain translation; `StreamingResponse`. Depends on `require_bearer`.
3. `src/marker/api/main.py` — `app.include_router(routes.router)`.

**Verification**:

```
.venv\Scripts\activate; python -m pytest tests/marker/api -v
```

**Acceptance Gate**:
- [ ] Working code: authenticated valid request downloads a `.docx` that opens in Word; unauthenticated request is refused.
- [ ] `python -m pytest tests/marker/api -v` green.

---

### Phase 3: Contract sweep + #78 placeholder flagging

**Goal**: Every in-scope ADR-018 clause has a passing test; the clause-coverage table is in the PR; the #78 placeholder status is stated explicitly.

**TDD approach**: complete the clause-coverage matrix (below). Add the adversarial auth test (`test_rejects_malformed_token`). Confirm no per-route `try/except` exists (review + the structural 500-safety test).

**Deliverables**:
1. Any remaining clause tests to fill the matrix.
2. PR description: clause-coverage table + an explicit statement — *"The global exception handler wiring and streaming-response binding ship as a documented placeholder pending #78 (Option B). Token verification is a placeholder pending SSO (#50/#73/#48b)."*

**Clause coverage matrix**: the authoritative clause→test mapping is the "Clause → assertion map" in [contracts/skeletons-post.md](./contracts/skeletons-post.md) — single source per ADR-001 (not duplicated here). Every row must be green before PR.

**Acceptance Gate**:
- [ ] All matrix rows green; `lint-imports` green; full `pytest` green.
- [ ] PR states placeholder-vs-final for the exception handler and auth verification.

## File Inventory

| Phase | New / Changed Files | Count |
| ----- | ------------------- | ----- |
| 0 | `pyproject.toml` (Δ), `marker/domain/protocols.py` (Δ), `marker/functions/engines.py` (Δ), `marker/functions/builders.py` (Δ), `marker/api/__init__.py`, `marker/api/main.py`; tests: `tests/marker/api/test_app.py`, `tests/marker/functions/test_builders.py` (Δ) | 6 src + 2 test |
| 1 | `marker/api/dependencies/__init__.py`, `marker/api/dependencies/auth.py`, `marker/api/exception_handlers.py`, `marker/api/main.py` (Δ); tests: `tests/marker/api/conftest.py`, `tests/marker/api/test_app_wiring.py` | 4 src + 2 test |
| 2 | `marker/api/schemas.py`, `marker/api/routes.py`, `marker/api/main.py` (Δ); tests: `tests/marker/api/test_routes.py`, `tests/marker/api/test_openapi.py`, `tests/marker/api/test_schemas.py` | 3 src + 3 test |
| 3 | tests: clause-coverage fill-ins (in existing files) | 0 new |

**Total new src files**: ~9 | **Total new test files**: ~6 | **Total deleted**: 0

## Library Best Practices

<!-- Confirm against Context7 MCP during implementation before relying on these. -->

### fastapi
- **Import path**: `from fastapi import FastAPI, APIRouter, Depends, HTTPException`; `from fastapi.responses import StreamingResponse`; `from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials`; `from fastapi.exceptions import RequestValidationError`; `from starlette.exceptions import HTTPException as StarletteHTTPException`.
- **API gotchas**: register the exception handler on `StarletteHTTPException` (not `fastapi.HTTPException`) so 401 `headers` flow through. `HTTPBearer(auto_error=False)` lets `require_bearer` raise the custom 401 with `WWW-Authenticate`.
- **Confirmed pattern**: see `python-fastapi/procedures/app-wiring.md` and `route-conventions.md` (paths corrected to `marker.api.*`).

### python-docx
- **Import path**: `from docx import Document`.
- **API gotcha**: `Document.save()` accepts a file-like object — pass `io.BytesIO()` to get bytes without touching disk (the D3 seam).

### openapi-spec-validator
- **Import path**: `from openapi_spec_validator import validate`.
- **Note**: NOT currently in the test group — Phase 0 adds it. (The `python-testing-api` skill's claim that it is "already in test deps" is stale — see research.md.)

## Risk Register

| Risk | Mitigation |
| ---- | ---------- |
| **#78 overturns FastAPI** (the issue title names "Django / FastAPI / frontend"). | Peter's interim layering isolates the framework-specific pieces to two seams (handler wiring, streaming object). The DTO→domain translation, the bytes seam, and the builder survive a framework swap. Plan commits to FastAPI (named by ADR-018, the standard, the skill, and #51 itself) and flags the residual risk in the PR. |
| **Global handler / streaming binding is #78-gated** but #51 ships first (Option B). | Ship as a documented placeholder; flag explicitly in the PR; track a follow-up before any external consumer relies on the endpoint. The route is structured to *raise* (not catch) and *return bytes*, so finalising the binding is additive, not a rewrite. |
| **Auth mechanism deferred** (SSO #50/#73/#48b open). | `require_bearer` enforces presence + 401/`WWW-Authenticate` now; token verification is a stubbed placeholder behind one seam. Only the seam's internals change when SSO lands. |
| **`json_invalid` is a Pydantic-v2 internal type**, not a stable API — a future upgrade could silently revert 400→422. | Dedicated `test_400_for_malformed_json_body` guards the split; failure is caught by CI, not in production silence. |
| **Skill import paths are stale** (`rl.app.api.*`, `rl.skeleton_generator`). | Plan corrects all paths to `marker.api.*` / `marker.functions.builders`. Flag the `python-fastapi` + `python-testing-api` skill drift as a follow-up for the skill owner (research.md §Skill-path drift). |
| **Schemathesis property tests** need principal-engineer approval and can hit downstream services without overrides. | Keep as a "Could have"; do not add `@schema.parametrize()` until Peter approves and dependency overrides are confirmed. |
| **Context Map / ADR-001 staleness** (rl-vs-marker). | Peter owns the reconciliation ADR + `domain-model.md` update before #51 merges; does not block the plan or the code. |

## Glossary

| Term | Definition |
| ---- | ---------- |
| skeleton | A structured but empty geotechnical report document (`.docx`): section headings + a project-metadata table, no engineering content. |
| GIR / Geotechnical Assessment Report | The report type whose structure the skeleton scaffolds (NZ, residential/low-risk). |
| north-south | Traffic crossing the system's outer boundary (an external caller ↔ a Redline service) — the high-rigour tier governed by ADR-018. |
