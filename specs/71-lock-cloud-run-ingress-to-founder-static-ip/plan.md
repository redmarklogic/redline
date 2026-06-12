# Implementation Plan: Lock Cloud Run Ingress to Founder Static IP

**Branch**: `feature/71-lock-cloud-run-ingress-to-founder-static-ip` | **Date**: 2026-06-12 | **Spec**: [spec.md](spec.md)

**Status**: Draft

## Summary

Add a FastAPI middleware that reads the founder's static IP from an environment variable (`FOUNDER_ALLOWED_IP`) and returns HTTP 403 for any request whose source IP does not match. The middleware is registered only when `FOUNDER_ALLOWED_IP` is present in the environment, so staging and local dev are unaffected. The founder's IP is supplied as a plain (non-secret) environment variable on the prod Cloud Run service via Terraform.

Cloud Run ingress stays `INGRESS_TRAFFIC_ALL` — no network-layer changes. Removal at IAP handover: delete one middleware file, remove one `add_middleware` call, remove one env var from Terraform. Zero infrastructure cost.

**Rejected approach**: Cloud Armor + HTTPS LB (~$11/month, 7 new Terraform resources, 20 tasks). Over-engineered for one sprint of disposable scaffolding. The door is already locked (prod has no `allUsers` IAM invoker) — this feature adds an IP peephole check, not a bouncer at the street.

## Technical Context

**Language**: Python 3.14
**Package manager**: uv
**Testing**: pytest
**Project layout**: single-package (`src/marker/`)
**Dev OS**: Windows | **Deploy OS**: Linux
**Key dependencies**: FastAPI (existing), starlette `BaseHTTPMiddleware` (already a FastAPI transitive dep — no new packages)

**Terraform change**: one new env var on the prod Cloud Run service in `deploy/infra/terraform/cloud_run.tf`; one new variable in `variables.tf`

## Design Decisions

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| D1 | Enforcement layer | FastAPI middleware | $0, ~15 lines, trivially removed. Cloud Armor + LB rejected: $11/month, 7 new resources, overkill for one sprint. |
| D2 | Opt-in activation | Middleware registered only when `FOUNDER_ALLOWED_IP` env var is present | Staging and local dev are unaffected with no code branching on environment name |
| D3 | IP source header | `X-Forwarded-For` first entry | Cloud Run sets this to the actual client IP for services with `INGRESS_TRAFFIC_ALL`. Reliable; not spoofable at the Cloud Run layer. |
| D4 | IP format | Plain IP string (e.g. `203.0.113.45`), not CIDR | Simplest possible; the restriction is a single machine. CIDR adds parsing complexity with no benefit. |
| D5 | ADR-021 variance | `os.environ.get("FOUNDER_ALLOWED_IP")` used (returns None if absent) | ADR-021 prefers `os.environ["VAR"]`. Using `.get()` here is an accepted variance for disposable scaffolding — the alternative (adding a dummy value to staging) adds more noise than the variance. Documented as accepted risk. |
| D6 | Terraform ingress | `INGRESS_TRAFFIC_ALL` unchanged | No network-layer restriction needed. IAM Lock 2 (no `allUsers` invoker on prod) already blocks unauthenticated callers; this adds IP-based filtering as a second check. |

## Domain Impact

**Modularity assessment**: N/A — new file within existing `marker.api` module
**New packages**: None
**Bounded context changes**: None
**Import-linter contract updates**: None (middleware stays within `marker.api` layer)
**Subdomain classification**: Generic (scaffolding)
**New domain terms**: None

## Architecture

```text
Internet → Cloud Run (INGRESS_TRAFFIC_ALL)
               ↓
     IPAllowlistMiddleware
     reads X-Forwarded-For
     ├── IP matches FOUNDER_ALLOWED_IP → pass through to app
     └── IP does not match → return 403 (no app code runs)
               ↓
         FastAPI routes
```

Middleware is the outermost layer — registered first in `create_app()` so it runs before any route handler.

## MoSCoW

| Category | Items |
|----------|-------|
| **Must have** | `IPAllowlistMiddleware` in `src/marker/api/middleware.py`; registered in `create_app()` when env var present; `FOUNDER_ALLOWED_IP` on prod Cloud Run service in Terraform |
| **Should have** | Pytest test for middleware (allow + deny cases) |
| **Could have** | CIDR range support (single IP is sufficient for now) |
| **Won't have (this time)** | Cloud Armor, load balancer, staging restriction, monitoring |

## Phased Delivery

### Phase 0: Middleware + Terraform env var

**Goal**: Prod Cloud Run service returns 403 to any IP that is not the founder's. Staging and local dev are unaffected.

**TDD approach**: Write failing tests for `IPAllowlistMiddleware` before implementing (allow case, deny case, missing header case).

**Deliverables**:

1. `src/marker/api/middleware.py` — `IPAllowlistMiddleware(BaseHTTPMiddleware)` class
2. `src/marker/api/main.py` — `add_middleware(IPAllowlistMiddleware, ...)` call in `create_app()`, gated on env var presence
3. `tests/unit/api/test_middleware.py` — pytest tests for the three cases
4. `deploy/infra/terraform/variables.tf` — `founder_allowed_ip` variable (string, no default)
5. `deploy/infra/terraform/cloud_run.tf` — `FOUNDER_ALLOWED_IP` env var on prod service only

**Verification**:

```sh
# Unit tests
rtk uv run pytest tests/unit/api/test_middleware.py -v

# Smoke test (from founder's machine, after terraform apply)
curl https://<prod-run-url>/health
# Expect: 200

# Negative smoke test (from any other IP)
curl https://<prod-run-url>/health
# Expect: 403
```

**Acceptance Gate** (both must pass before closing the issue):

- [ ] `rtk uv run pytest tests/unit/api/test_middleware.py -v` — all green
- [ ] curl from founder IP returns non-403; curl from any other IP returns 403

---

## File Inventory

| Phase | New Files | Modified Files |
|-------|-----------|----------------|
| 0 | `src/marker/api/middleware.py`, `tests/unit/api/test_middleware.py` | `src/marker/api/main.py`, `variables.tf`, `cloud_run.tf` |

**Total new**: 2 | **Total modified**: 3

## Risk Register

| Risk | Mitigation |
|------|------------|
| `X-Forwarded-For` absent (local dev, direct invocation) | Middleware only active when `FOUNDER_ALLOWED_IP` is set; local dev doesn't set it |
| ADR-021 variance (`os.environ.get`) | Accepted for disposable scaffolding; documented in D5 above and in code comment |
| Founder's ISP changes static IP | Update `founder_allowed_ip` in `terraform.tfvars`, run `terraform apply`, redeploy — no code change needed |
| Middleware removed at IAP handover | Delete `middleware.py`, remove `add_middleware` call from `main.py`, remove Terraform env var. Three-line change. |

## Glossary

| Term | Definition |
|------|------------|
| Middleware | A function that wraps every HTTP request/response cycle — runs before route handlers and can short-circuit the request |
| X-Forwarded-For | An HTTP header that Cloud Run populates with the actual client IP address for publicly reachable services |
| Walking skeleton | Minimal end-to-end deployment proving the system can be built, deployed, and reached — not production-ready |
