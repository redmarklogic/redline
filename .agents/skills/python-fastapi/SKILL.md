---
name: python-fastapi
description: Use when implementing or testing any external (north-south) FastAPI HTTP endpoint that must conform to docs/architecture/api/http-api-standard.md (ADR-018)
paths: "src/**/*.py,tests/**/*.py"
---

## Boundary Contract

### Applies To
- Any FastAPI route on the external (north-south) HTTP surface
- The global exception handler and auth dependency wired at app startup
- Tests asserting ADR-018 HTTP contract clauses

### Produces
- Endpoints that conform to `docs/architecture/api/http-api-standard.md`

### Does Not Cover
- General mocking strategy and TestClient setup → `python-testing-api`
- General Python error handling patterns → `python-error-handling`
- Layer architecture and new-package decisions → escalate to the principal engineer
- Auth provider / token format (bearer pattern only, mechanism deferred to #73/#48b)

## Quick Reference

| Clause | FastAPI binding |
|---|---|
| §1 — plural-noun URI | `@router.post("/skeletons")` not `/skeleton` or `/generateSkeleton` |
| §2 — status codes | `status_code=200` on route decorator; see table in procedure |
| §3 — error envelope | Single `@app.exception_handler` — never per-route try/except |
| §4 — 422 vs 400 | Custom `RequestValidationError` handler inspects `type == "json_invalid"` |
| §5 — 200 for sync artifact | `status_code=200`; no `Location` header needed |
| §6 — binary response | `StreamingResponse` with correct `media_type` + `Content-Disposition` |
| §7 — auth + 401 header | `HTTPBearer(auto_error=False)` dep; raise with `headers={"WWW-Authenticate": "Bearer"}` |
| §9 — no SSE on sync route | Do not wire an SSE response on this endpoint |
| §12 — OpenAPI generated | FastAPI auto-generates; do not hand-author `/openapi.json` |
| §15 — no versioning yet | No `/v1/` prefix until second endpoint or first external consumer |

## Procedures

Load by task:

| Task | Procedure |
|---|---|
| Wiring app startup (exception handler, auth) | `procedures/app-wiring.md` |
| Writing an endpoint route | `procedures/route-conventions.md` |
| Writing ADR-018 contract tests | `procedures/contract-testing.md` (extends `python-testing-api`) |

## Live Standard

`docs/architecture/api/http-api-standard.md` is the authoritative clause text.
This skill is the FastAPI implementation binding for those clauses.
If a clause in this skill conflicts with the live standard, the live standard wins — flag the drift.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Per-route `try/except` for error envelope | One `@app.exception_handler` at app startup; never per-route |
| Singular URI (`/skeleton`) | Plural noun: `/skeletons` (ADR-018 §1) |
| Returning DOCX bytes in a JSON envelope | `StreamingResponse` with binary `media_type`; never base64 |
| 401 without `WWW-Authenticate: Bearer` header | Pass `headers={"WWW-Authenticate": "Bearer"}` on every 401 |
| `RequestValidationError` always → 422 | Inspect `type == "json_invalid"` → 400; otherwise → 422 |
| Hand-authoring `/openapi.json` | FastAPI auto-generates it; do not touch it manually |
