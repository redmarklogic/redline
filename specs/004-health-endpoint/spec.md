# Feature Specification: Health Check Endpoint

**Feature Branch**: `feature/004-health-endpoint`

**Created**: 2026-06-10

**Status**: Draft

**Input**: User description: "Add a health/status endpoint that returns HTTP 200 when the service is healthy, without authentication, so infrastructure tooling and OpenAPI consumers can verify the service is running."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Infrastructure Probe (Priority: P1)

An automated infrastructure probe (Cloud Run health checker, Docker daemon, or uptime monitor) needs to verify the service is alive without holding credentials. It sends a bare HTTP request and expects a clean, unambiguous signal.

**Why this priority**: Without this, the only liveness signal is a real endpoint that requires a valid auth token and request body — infrastructure tooling cannot hold credentials and cannot construct a valid request. This is the primary forcing function for the endpoint.

**Independent Test**: Can be fully tested by sending a GET request with no Authorization header and verifying a 200 response with the expected body. Delivers the core infrastructure contract in isolation.

**Acceptance Scenarios**:

1. **Given** the service is running, **When** a probe sends `GET /health` with no headers, **Then** the service responds with `200 OK` and body `{"status": "healthy"}`.
2. **Given** the service is running, **When** a probe sends `GET /health` with no `Authorization` header, **Then** the response is `200 OK` — the absence of credentials does not produce a `401`.
3. **Given** the service is running, **When** a probe sends `GET /health` with an invalid or expired `Authorization` header, **Then** the response is still `200 OK` — auth credentials are ignored, not validated, on this endpoint.

---

### User Story 2 - Developer Verification via OpenAPI Docs (Priority: P2)

A developer navigating the OpenAPI documentation page (`/docs`) wants to confirm the service is reachable without needing to obtain an API token first. They look for a health check entry but do not find one — the health probe is not exposed as an API consumer contract.

**Why this priority**: The OpenAPI docs surface (`/docs`) is developer-facing. Surfacing an infrastructure probe there as an API endpoint would pollute the documented API surface with a contract that has no request body, no auth, and no domain meaning. The developer experience is better without it in the docs.

**Independent Test**: Can be fully tested by loading the OpenAPI schema from `/openapi.json` and confirming the `/health` path is absent from it.

**Acceptance Scenarios**:

1. **Given** the service is running, **When** a developer fetches `/openapi.json`, **Then** the response does not include `/health` in the `paths` object.
2. **Given** the service is running, **When** a developer loads `/docs`, **Then** the health check endpoint does not appear in the Swagger UI endpoint list.

---

### User Story 3 - Developer Script Readiness Check (Priority: P3)

A developer starting the local development environment runs the `run-app.ps1` script, which waits for the service to be ready before reporting success. The script now polls `/health` instead of the root path, receiving a meaningful positive signal rather than a 404.

**Why this priority**: The existing readiness probe polls the root path (`/`), which returns 404. A 404 is technically a response (the process is alive) but is not a meaningful health signal — the script cannot distinguish "service alive but 404-ing" from "service returning 404 because it is misconfigured." The health endpoint makes this check unambiguous.

**Independent Test**: Can be tested by running `run-app.ps1` and confirming the script exits the readiness wait loop upon receiving `200` from `/health`.

**Acceptance Scenarios**:

1. **Given** the service is starting up, **When** the readiness check in `run-app.ps1` polls the health endpoint, **Then** the script advances to "ready" only when it receives `200 OK` from `/health`.
2. **Given** the health endpoint returns `200`, **When** the readiness loop receives the response, **Then** the script prints a success message and exits the polling loop.

---

### Edge Cases

- What happens when the service process is alive but a future unhandled exception occurs? The global error handler produces a `500` — the infrastructure probe correctly interprets this as unhealthy.
- What happens when `/health` is called with a request body? The body is ignored — GET endpoints do not process request bodies.
- What happens if the health response is included in rate-limiting logic? Infrastructure probes call `/health` continuously; rate-limiting would cause false negatives. The endpoint must be exempt from any rate limiter introduced in future cycles.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The service MUST expose a `GET /health` endpoint that returns `200 OK` when the service is running normally.
- **FR-002**: The health endpoint MUST NOT require authentication credentials of any kind. A request with no `Authorization` header MUST receive `200 OK`.
- **FR-003**: The health endpoint MUST NOT appear in the OpenAPI schema served at `/openapi.json`. It is an infrastructure contract, not a consumer API contract.
- **FR-004**: The health response body MUST be `{"status": "healthy"}`. No additional fields.
- **FR-005**: The health endpoint MUST be isolated from all endpoints that require authentication — it MUST NOT inherit auth requirements from any protected router or middleware.
- **FR-006**: The health endpoint MUST be exempt from any rate-limiting logic applied to other endpoints, now and in future cycles.
- **FR-007**: The development environment readiness probe in `run-app.ps1` MUST be updated to poll `/health` instead of the root path.

### Out of Scope (this cycle)

- Dependency health checks (database, external services) — deferred until a downstream dependency exists in code.
- `503 Service Unavailable` response for degraded states — deferred; requires a standards amendment.
- A separate liveness probe endpoint (`/ping`) — deferred until Cloud Run requires independent probe routing.
- Response fields beyond `status` (version, uptime, timestamp).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Infrastructure probes can verify service liveness without credentials — zero false negatives caused by auth rejection on `/health`.
- **SC-002**: The OpenAPI schema at `/openapi.json` contains zero entries for `/health` — the endpoint is not exposed as a consumer API contract.
- **SC-003**: The development readiness script succeeds and exits the polling loop upon receiving a healthy response from `/health` — no 404-based false positives.
- **SC-004**: A request to `/health` with no headers returns a response in under 100 milliseconds under normal operating conditions — the probe adds negligible latency to health-check cycles.

## Assumptions

- The service runs as a single Cloud Run instance with no independent liveness/readiness probe routing — a single `/health` endpoint is sufficient for this deployment topology.
- No rate limiter is currently installed; the rate-limit exemption requirement is a forward-looking constraint for when one is added.
- The response value `"healthy"` is the correct term for v0.1; migration to the RFC-grounded `"pass"` vocabulary is a future breaking-change decision, not a scope item here.
- The global error handler already covers unexpected failures with `500` — no per-endpoint error handling is needed on `/health`.
- Infrastructure probe frequency (Cloud Run default) is within normal operating parameters; no caching of the health response is required at this stage.
