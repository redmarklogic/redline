# This Week — Sprint 2: Jun 8-14

_Synced: 2026-06-11_

## Sprint 2 — Jun 8–14

### In Progress

| Agent | Title | Issue | Target | Source |
|---|---|---|---|---|
| Founder | GCP project and region setup with billing baseline (australia-southeast1) | #64 | 2026-06-09 ⚠ OVERDUE | deploy/infra/terraform/ |
| Founder | Artifact Registry Docker repository (in-region) | #66 | 2026-06-09 ⚠ OVERDUE | — |

### Blocked

_Nothing blocked._

### To Review

_Nothing to review._

### Backlog (this sprint)

| Agent | Title | Issue | Target |
|---|---|---|---|
| Founder | Dockerfile for FastAPI backend (wraps build_skeleton as API) | #67 | 2026-06-10 ⚠ OVERDUE |
| Founder | Workload Identity Federation for GitHub Actions (keyless auth) | #68 | 2026-06-10 ⚠ OVERDUE |
| Founder | GitHub Actions pipeline: build, test, push backend image | #69 | 2026-06-11 |
| Founder | Lock Cloud Run ingress to founder static IP | #71 | 2026-06-13 |
| Founder | Boundary contract: .env.example and infra-ready note to #51 | #72 | 2026-06-13 |
| Peter | Tech stack and layer responsibilities (Django / FastAPI / frontend) | #78 | 2026-06-10 ⚠ OVERDUE |
| Peter | API design standards → docs/architecture/api/ | #79 | 2026-06-12 |
| Founder | Skeleton Generator PRD: rule on selector and out-of-scope upload experience | #100 | 2026-06-14 |

### Done

| Title | Issue |
|---|---|
| Ratify Cloud Run runtime + Artifact Registry hosting (B-1a) | #48 |
| Cloud Run + Artifact Registry hosting ADR and Tier-1 GCP approval | #63 |
| Cost controls and budget cap (denial-of-wallet guard) | #65 |
| Cloud Run deploy: staging + prod with Secret Manager (HCL scaffold) | #70 |
| Skeleton endpoint: POST /skeletons returns DOCX behind auth | #51 |
| Spec-Kit slash command (/spec-kit) | #42 |
| OpenAPI docs: enable Swagger UI and auto-open browser to /docs | #91 |
