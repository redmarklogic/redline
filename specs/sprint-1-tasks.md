# Walking Skeleton — Sprint 1

**Definition**: A live, authenticated `POST /skeletons` endpoint hosted on Google Cloud Platform, reachable from a real URL, that requires a valid bearer token before returning a DOCX skeleton.

**Success criterion**: Navigate to the production URL, send an authenticated request to `POST /skeletons`, receive a valid DOCX response. Unauthenticated requests are rejected with `401`.

**Milestone**: M1 — ship by 2026-06-30.

**Strategic bet**: [Bet 1 — The Free Skeleton Wedge Beats Paid Acquisition](../docs/product/strategy/strategic-bets.md)

---

## Sub-tasks (execution order)

### WS-01 — POST /skeletons endpoint + auth seam

| Field | Value |
|---|---|
| **Status** | Done |
| **Spec** | `specs/001-skeleton-endpoint/` |
| **Branch** | Merged to master via PR #90 |
| **Description** | FastAPI app with `POST /skeletons` returning a DOCX. Bearer token auth seam rejects unauthenticated callers with `401 + WWW-Authenticate: Bearer`. Error envelope, OpenAPI schema, full test coverage. |
| **Dependencies** | None. |

All 39 tasks in `specs/001-skeleton-endpoint/tasks.md` complete. This is the foundation the walking skeleton runs on.

---

### WS-02 — Health endpoint

| Field | Value |
|---|---|
| **Status** | Not Started |
| **Spec** | `specs/004-health-endpoint/spec.md` — spec written, no tasks file yet |
| **Description** | `GET /health` returns `200 {"status": "healthy"}` with no auth required. Excluded from OpenAPI schema. Required for Cloud Run liveness probes — without it, infrastructure tooling cannot verify the service is alive without holding credentials. |
| **Dependencies** | WS-01 (app factory must exist). |

The spec is complete (`specs/004-health-endpoint/spec.md`). A tasks file does not exist yet. This must be implemented before deployment — Cloud Run health checks will fail without it.

---

### WS-03 — Merge spec 003 (OpenAPI docs) to master

| Field | Value |
|---|---|
| **Status** | In Progress |
| **Spec** | `specs/003-openapi-docs/` |
| **Branch** | `feature/003-openapi-docs` — committed and ready (4b4cffa) |
| **Description** | Merge branch to master so the production deployment includes re-enabled `/docs` Swagger UI. Not strictly required for the walking skeleton success criterion, but needed before any further work branches off master. |
| **Dependencies** | None. |

---

## Dependency Graph

```text
WS-01 (endpoint + auth) [DONE]
  |
  v
WS-02 (health endpoint) ----+
                            |
WS-03 (merge to master) ----+
                            |
                            v
                     [GCP deployment — see Missing Tasks below]
                            |
                            v
                   Walking skeleton live
```

**Critical path**: WS-02 (health endpoint) is the only unstarted task with existing spec material. GCP deployment tasks do not exist on the board — see Missing Tasks section below.

---

## Deferred — not part of walking skeleton

These tasks were in the previous plan but are not needed to achieve a live authenticated endpoint on GCP. They belong in a later sprint increment.

| Task | Reason deferred |
|---|---|
| Standards Knowledge Store MVP (Feature N) | Standards references are a content quality concern, not a prerequisite for a live endpoint |
| Document Parser / LOE extraction (Feature M) | One-click LOE UX is Sprint 1 scope but not the walking skeleton definition |
| Audit Log core subset (Feature L) | Day-1 requirement per PRD, but does not block the endpoint being live and reachable |

---

## Missing Tasks — reported from Peter + Brent review

These tasks are not on the board and must be created before the walking skeleton can ship. Peter and Brent both confirmed these are blocking the critical path. No existing spec covers any of them.

| # | Task | Blocking? | Owner | Effort |
|---|---|---|---|---|
| M-01 | Health endpoint tasks file + implementation — `GET /health` returns `{"status":"healthy"}`, no auth, excluded from OpenAPI schema. Cloud Run health probe requires this before traffic is served. | **Blocking** | Kabilan | 1–2 h |
| M-02 | Dockerfile — multi-stage Python slim image; entrypoint `uvicorn marker.api.main:create_app --factory --port 8080`. ADR-019 mandates Linux-compatible production image. | **Blocking** | Kabilan | 1–2 h |
| M-03 | GCP project setup — enable 4 APIs: Cloud Run, Artifact Registry, Cloud Build, IAM. One-time setup. | **Blocking** | Brent | 0.5 h |
| M-04 | Artifact Registry repository — Docker image repository in `australia-southeast1`. Cloud Run pulls from here. | **Blocking** | Brent | 0.25 h |
| M-05 | Cloud Run service — first deploy. Image from M-04, region `australia-southeast1`, `GET /health` as liveness probe, allow unauthenticated HTTP (bearer auth enforced by app). | **Blocking** | Brent | 0.5 h |
| M-06 | URL decision — accept default Cloud Run `*.run.app` URL or map custom domain. Founder decides, Brent configures. Must be decided before M-05. | **Blocking** | Founder + Brent | 10 min decision |
| M-07 | CI/CD pipeline — GitHub Actions workflow: build image → push to Artifact Registry → deploy to Cloud Run on merge to master. | Non-blocking (manual deploy works for walking skeleton) | Brent | 2–3 h |

**Note on authentication:** Peter's recommendation (accepted): the current bearer seam — which rejects callers with no token but accepts any non-empty token — is sufficient for the walking skeleton. Real SSO (issues #50/#73/#48b) is a Sprint 2 gate condition, not a walking skeleton requirement. The URL will not be published at M1; traffic is founder-only for 20 days.
