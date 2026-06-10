# This Week — Sprint 2: Jun 8-14

_Synced: 2026-06-10_

## Sprint 2 — Jun 8–14

### In Progress

| Agent | Title | Target | Source |
|---|---|---|---|
| Founder | Cloud Run deploy: staging + prod with Secret Manager | 2026-06-12 | specs/70-cloud-run-deploy-staging-prod-with-secret-manager/ |
| Founder | Lock Cloud Run ingress to founder static IP | 2026-06-13 | — |

### Blocked

_Nothing blocked._

### To Review

_Nothing to review._

### Backlog (this sprint)

| Agent | Title | Target |
|---|---|---|
| Founder | GCP project and region setup with billing baseline (australia-southeast1) | 2026-06-09 ⚠ OVERDUE |
| Founder | Artifact Registry Docker repository (in-region) | 2026-06-09 ⚠ OVERDUE |
| Founder | Dockerfile for FastAPI backend (wraps build_skeleton as API) | 2026-06-10 |
| Founder | Workload Identity Federation for GitHub Actions (keyless auth) | 2026-06-10 |
| Founder | GitHub Actions pipeline: build, test, push backend image | 2026-06-11 |
| Peter | Tech stack and layer responsibilities (Django / FastAPI / frontend) | 2026-06-10 |
| Peter | API design standards → docs/architecture/api/ | 2026-06-12 |
| Founder | Boundary contract: .env.example and infra-ready note to #51 | 2026-06-13 |

### Done

- Ratify Cloud Run runtime + Artifact Registry hosting (B-1a) · ops
- Cloud Run + Artifact Registry hosting ADR and Tier-1 GCP approval · design
- Cost controls and budget cap (denial-of-wallet guard) · ops
- OpenAPI docs: enable Swagger UI and auto-open browser to /docs · feature
- Skeleton endpoint: POST /skeletons returns DOCX behind auth · feature
- Spec-Kit slash command (/spec-kit) · feature
