# Quickstart: Skeleton Endpoint

How to run and verify `POST /skeletons` locally once implemented. (Plan is in [plan.md](./plan.md); this is the dev/verify loop.)

## Prerequisites

```
rtk uv sync           # installs fastapi, uvicorn, httpx, pytest-mock, openapi-spec-validator (added in Phase 0)
.venv\Scripts\activate
```

## Run the test suite (TDD loop)

```
python -m pytest tests/marker/api tests/marker/functions -v
rtk lint-imports      # marker layers (api > functions > domain) + marker independence must pass
```

## Run the app

```
python -m uvicorn marker.api.main:create_app --factory --reload --port 8000
```

## Manual verification (matches the spec scenarios)

**Success (User Story 1)** — authenticated, valid → `200` + `.docx`:

```
curl -s -D - -o skeleton.docx ^
  -H "Authorization: Bearer dev-placeholder-token" ^
  -H "Content-Type: application/json" ^
  -d "{\"sections\":[\"Introduction\",\"Site Description\",\"Conclusions\"],\"project_number\":\"GIR-001\",\"client_name\":\"Acme Corp\",\"site_address\":\"123 Example St\",\"date\":\"2026-06-09\"}" ^
  http://localhost:8000/skeletons
```

Expect: `200 OK`; `Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document`; `Content-Disposition: attachment; filename="GIR-001.docx"`; `skeleton.docx` opens in Word with the three sections + a metadata table.

**Unauthenticated (User Story 2)** — no token → `401` + challenge:

```
curl -s -D - -o NUL -H "Content-Type: application/json" -d "{}" http://localhost:8000/skeletons
```

Expect: `401`; header `WWW-Authenticate: Bearer`; body is the error envelope `{code, message, trace_id}`; no document bytes.

**Bad input (User Story 3)**:

- Missing field / empty `sections` / duplicate heading (authenticated) → `422`, envelope with `code: VALIDATION_ERROR`.
- Malformed JSON body (`-d "{not json"`) → `400`, envelope with `code: BAD_REQUEST`.
- Force an internal fault → `500`, envelope, `message` free of stack/path/class.

**OpenAPI generated (§12)**:

```
curl -s http://localhost:8000/openapi.json | python -c "import sys,json,openapi_spec_validator as v; v.validate(json.load(sys.stdin)); print('valid')"
```

## Notes

- `dev-placeholder-token` is accepted at v0.1 because token *verification* is a placeholder (presence-only) pending SSO (#50/#73/#48b). Any non-empty `Bearer` value passes; absence → `401`.
- In tests, bypass auth via `app.dependency_overrides[require_bearer]`; assert the real `401` path with a **raw** `TestClient(create_app())` (no override).
