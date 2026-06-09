# Research: Health Check Endpoint

**Feature**: specs/004-health-endpoint
**Date**: 2026-06-10
**Status**: Complete — no open unknowns

All design decisions were resolved prior to planning via:
- Peter (Principal Engineer) architectural analysis against ADR-018 and http-api-standard.md
- NotebookLM deep research: FastAPI Implementation notebook (5 sources)
- NotebookLM deep research: Web API Design notebook (4 sources)

---

## Decision 1: Status field value — `"healthy"` not `"ok"`

**Decision**: Use `"healthy"` as the status string.

**Rationale**: Every FastAPI implementation book that covers health check endpoints uses `"healthy"`. The value `"ok"` has no grounding in any source. The RFC-grounded vocabulary (`"pass"/"warn"/"fail"` per Mitra & Nadareishvili, *Microservices Up and Running*) is the correct long-run target — but switching from `"healthy"` to `"pass"` mid-life is a breaking contract change and is deferred explicitly. The spec notes this as an assumption.

**Alternatives considered**:
- `"ok"` — common informally but not grounded in any source
- `"pass"` — RFC-grounded but represents a deliberate future migration step

---

## Decision 2: Auth exclusion mechanism — router-level isolation

**Decision**: Mount the health route on a separate dependency-free router included via `app.include_router(health_router)`, not via `routes.router`.

**Rationale**: `routes.router` carries `require_bearer` per-route via `Depends()`. Any endpoint included via that router could silently inherit auth dependencies. The canonical FastAPI pattern (*Building Generative AI Services with FastAPI*) is explicit: place public endpoints in unprotected routers, protected endpoints in routers included with `dependencies=[...]`. This is structural isolation — testable with a single no-auth test.

**Alternatives considered**:
- Middleware path-check (`if request.url.path == "/health": skip`) — works but is harder to audit and easier to break with a rename
- ASGI `allowed_paths` whitelist (Ferraro, *FastAPI Cookbook*) — correct but over-engineered for one exempt route

---

## Decision 3: OpenAPI visibility — `include_in_schema=False`

**Decision**: Set `include_in_schema=False` on the health endpoint.

**Rationale**: The health probe is an infrastructure contract, not an API consumer contract. Exposing it in the Swagger UI introduces a no-auth, no-request-body endpoint into the developer-facing documentation surface, which the feature branch is specifically improving. The endpoint must not appear in `/openapi.json` paths.

**Alternatives considered**:
- Include in schema — rejected; pollutes the OpenAPI docs surface with an infrastructure probe

---

## Decision 4: No Pydantic response model

**Decision**: Return a plain `dict` — no `BaseModel`.

**Rationale**: All FastAPI sources that demonstrate health check implementation return a plain dict. No source in the FastAPI notebook defines a Pydantic model for health checks. Adding a model adds no value for a one-field response and is inconsistent with established practice.

---

## Decision 5: Rate-limit exemption — forward-looking constraint

**Decision**: No rate limiter is installed today. When one is added, `/health` must be in the exempt list at that point (*Building Generative AI Services with FastAPI*: "Exclude the /health endpoint from rate-limiting logic as cloud providers or Docker daemons may ping this endpoint continually").

**Rationale**: Infrastructure probes call `/health` on a continuous schedule. Rate-limiting would produce false-negative health reports, potentially causing Cloud Run to remove healthy instances.

---

## Decision 6: Two-probe pattern — deferred

**Decision**: Single `/health` endpoint only at this stage.

**Rationale**: Mitra & Nadareishvili correctly model a two-probe split (`/ping` for liveness, `/health` for readiness). The forcing function for the split is an orchestrator that can independently route traffic around a live-but-not-ready instance. Cloud Run Phase 1 does not expose that routing control. A second probe with no orchestrator consumer is dead infrastructure.

---

## Decision 7: 503 for degraded states — deferred

**Decision**: No 503 path in this cycle.

**Rationale**: `503` is not in the status code table of `http-api-standard.md §2`. Adding it requires a standards amendment. At Phase 1 there are no wired downstream dependencies — nothing to probe for degraded state. The global exception handler already covers unexpected failures with `500`.
