# Contract: Health Endpoint

Infrastructure liveness probe. Not user-facing; consumed by `tasks/run-app.ps1` (dev)
and Cloud Run startup probes (#177, production).

The ADR-018 JSON envelope does NOT apply — this endpoint is not on the API surface
(`src/marker`). It is a bare liveness signal on the web surface (`src/web`), consistent
with the pattern established by `src/marker/api/health.py`.

## GET /health/

| Aspect | Contract |
|---|---|
| Method / path | `GET /health/` |
| Auth | None. No session, cookie, or header required |
| Success | `200 OK`, `Content-Type: application/json` |
| Body | `{"status": "healthy"}` — JSON-equality asserted, not byte-equality (serialiser whitespace may vary) |
| Side effects | None — no DB read/write, no session creation |
| Redirect | `GET /health` (no trailing slash) receives a 301 redirect to `/health/` via Django's `APPEND_SLASH = True` default — callers should follow redirects or use the canonical trailing-slash form |

## Comparison rule

Assert JSON-equality (parse, then compare the object), never byte-equality.
`JsonResponse` default serialises compact; a literal string match against
pretty-printed spec form will fail.

## Consumers

| Consumer | Tolerance |
|---|---|
| `tasks/run-app.ps1 -App django` | Polls up to 30 × 1 s; 200 = ready, else warning |
| `tests/web/test_skeleton.py` | Asserts 200 + `application/json` + JSON-equal body |
| Cloud Run startup probe (#177) | 10 s initial delay, 3 failures × 5 s timeout (same as marker probe) |

## Out of contract

- No `{"checks": [...]}` sub-system detail (database, cache) — that is a later task
  once #164 (database) lands. This probe is liveness only, not readiness.
- No rate-limit exemption header needed at dev time; Cloud Run does not rate-limit
  its own startup probes.
