# Contract: GET /health

**Type**: REST endpoint
**Feature**: specs/004-health-endpoint
**Standard**: http-api-standard.md (v0.1)
**Stability**: Volatile (ADR-017 — not yet declared stable)

---

## Endpoint

```
GET /health
```

## Authentication

None. No `Authorization` header required or inspected.

## Request

No request body. No query parameters. No path parameters.

## Response — Healthy (200 OK)

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{"status": "healthy"}
```

**Field definitions:**

| Field | Type | Value | Notes |
|---|---|---|---|
| `status` | string | `"healthy"` | Fixed value. Future migration to `"pass"` is a deliberate breaking change — see research.md Decision 1. |

## Response — Unhealthy (500 Internal Server Error)

If an unexpected exception occurs, the global exception handler returns the standard error envelope (http-api-standard.md §3):

```json
{
  "code": "string",
  "message": "string",
  "trace_id": "string"
}
```

No `503` response. Degraded-state signalling is deferred until a readiness probe with downstream dependencies is implemented.

## OpenAPI Visibility

This endpoint is **excluded from the OpenAPI schema** (`include_in_schema=False`). It does not appear in `/openapi.json` or the Swagger UI at `/docs`.

## Rate Limiting

This endpoint is exempt from any rate limiter applied to other endpoints. Infrastructure probes (Cloud Run, Docker daemon) call it continuously on a schedule.

## Constraints

- Response time MUST be under 100ms under normal operating conditions (SC-004).
- Route MUST be mounted on a dependency-free router — not on `routes.router`.
- No per-route error handling. The global exception handler covers all unexpected failures.
