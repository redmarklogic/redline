# Contract: `POST /skeletons`

**This is a human-readable description, NOT a source of truth.** Per ADR-018 §12 the OpenAPI document is **generated from the implementation** (FastAPI auto-generates `/openapi.json`); it is never hand-authored. This file records the *intended observable contract* each requirement and test asserts. If the generated schema and this file disagree, fix the implementation/model — and update this file — never hand-edit `/openapi.json`.

---

## Endpoint

`POST /skeletons` — create a report skeleton and return it as a `.docx` download. (Plural noun, verb-free — Standard §1. No `/v1/` prefix — §14.)

**Auth**: required. `Authorization: Bearer <token>` (Standard §7). Token *verification* is a v0.1 placeholder (presence-only) pending SSO (#50/#73/#48b).

## Request

- `Content-Type: application/json`
- Body: `CreateSkeletonRequest` (see [data-model.md](../data-model.md) §1), `extra="forbid"`.

```json
{
  "sections": ["Introduction", "Site Description", "Conclusions"],
  "project_number": "GIR-001",
  "client_name": "Acme Corp",
  "site_address": "123 Example Street",
  "date": "2026-06-09"
}
```

## Responses

| Status | When | Body | Key headers |
|--------|------|------|-------------|
| `200 OK` | authenticated + valid | raw `.docx` bytes (streamed) | `Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document`; `Content-Disposition: attachment; filename="<safe-name>.docx"` (`project_number` sanitized to `[A-Za-z0-9._-]`, fallback `skeleton`) |
| `400 Bad Request` | body unparseable (bad JSON, wrong content type) | error envelope, `code: BAD_REQUEST` | — |
| `401 Unauthorized` | missing/invalid bearer | error envelope, `code: HTTP_401` | `WWW-Authenticate: Bearer` |
| `422 Unprocessable Content` | parsed but invalid (missing field, empty/blank/duplicate section, extra field) | error envelope, `code: VALIDATION_ERROR`, `details: [...]` | — |
| `500 Internal Server Error` | unhandled fault | error envelope, `code: INTERNAL_ERROR`, **no internal detail in `message`** | — |

`403`, `201`+`Location`, `202`+poll, SSE, and `Accept: application/json` (violations) are **out of scope** for #51 (Standard §5, §8–§10 — deferred/honesty constraint).

Error envelope shape (every non-2xx): `{ "code": str, "message": str, "trace_id": str, "details?": any }` (Standard §3).

## Clause → assertion map

| Clause | Observable assertion | Test |
|--------|----------------------|------|
| §1 plural URI | path is `/skeletons` | `test_skeletons_route_registered_plural_unversioned` |
| §3 envelope | every error body has `{code, message, trace_id}` | `test_422_uses_error_envelope`, `test_500_envelope_contains_no_internal_detail` |
| §3 no leak | `message` has no stack/class/path | `test_500_envelope_contains_no_internal_detail` |
| §4 422 vs 400 | invalid→422 (DTO **and** domain rules), unparseable→400 | `test_rejects_missing_required_field`, `test_domain_invalid_sections_returns_422`, `test_400_for_malformed_json_body` |
| §6 binary | `200`, DOCX media type, `attachment`, body starts `PK\x03\x04` | `test_returns_docx_bytes_with_correct_headers` |
| §7 auth | `401` + `WWW-Authenticate: Bearer` | `test_rejects_unauthenticated_with_401_and_www_authenticate`, `test_rejects_malformed_token` |
| §9 no SSE | response is DOCX, explicitly not `text/event-stream` | `test_returns_docx_bytes_with_correct_headers` (media-type assertion) |
| §12 OpenAPI | generated `/openapi.json` is structurally valid | `test_openapi_schema_is_valid` |
| §14 no version | no `/v1/` in any route path | `test_skeletons_route_registered_plural_unversioned` |
