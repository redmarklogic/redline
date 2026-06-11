# Data Model: End-to-End Live Health Check on Cloud Run

**Date**: 2026-06-11 | **Plan**: [plan.md](plan.md)

No database entities — this feature's "data" is deploy-chain state in GCP and
GitHub. Entities, identity, and state transitions below.

## Backend Image

| Field | Value / Rule |
|---|---|
| Identity | `australia-southeast1-docker.pkg.dev/redmarklogic-prod/redline-repo/redline-api:<commit-sha>` |
| Tag rule | Immutable full commit SHA only; `latest` prohibited (FR-002) |
| Digest | `sha256:...` — exposed as CI job output `image_digest` for provenance |
| Producer | CI build-push step (Stage 2) or manual `docker build`/`push` (Stage 1) |
| Consumers | Cloud Run services (via `image_tag` apply-time var); CI deploy step |

States: `absent → pushed` (no mutation; a new commit produces a new tag).

## Cloud Run Service (×2)

| Field | staging | prod |
|---|---|---|
| Name | `staging-redline-api` | `prod-redline-api` |
| Min instances | 0 | 0 (after `variables.tf` fix — was forced ≥ 1) |
| Max instances | 3 | 10 |
| Ingress | all traffic | all traffic |
| Invoker IAM | `allUsers` → `roles/run.invoker` (D11) | none — IAM-private |
| Probe | `GET /health` :8080, 10 s delay, 3 × 5 s | same |
| Traffic | health checks only | none (out of scope) |
| Owner | Terraform (shape); CI updates serving image only (D7) | Terraform only |

States: `absent → deploying → Ready` (apply) and `Ready → deploying → Ready`
(CI image update). A failed revision must never replace a serving Ready revision.

## Environment Secret (×4)

| Field | Value / Rule |
|---|---|
| Identity | `<env>-redline-<binding-key>` (lowercase keys, `secrets.tf:27`): `staging-redline-db_password`, `staging-redline-api_key`, `prod-redline-db_password`, `prod-redline-api_key`. Env-var names inside the container are the uppercase values (`DB_PASSWORD`, `API_KEY`) |
| Replication | `user_managed` pinned `australia-southeast1` (after `secrets.tf` fix — was `auto`) |
| Version | Exactly one current accessible version after population; referenced as `latest` by the service |
| Value rule | Real values (founder ruling); generated-now credentials become canonical for future backing services; never on disk, never in Terraform state |

State transitions (order is load-bearing, D1):
`unpinned, no versions → pinned, no versions (apply) → pinned, populated (gcloud)`.
Pinning after population would force replace + re-add.

## Pipeline Run

| Field | Value / Rule |
|---|---|
| Identity | One workflow run per push to `master` (after Stage 2 trigger switch) |
| Stages | test → auth (WIF) → build+push → deploy (staging only) → health check |
| Job outputs | `image_digest` (from build-push step) |
| Environment | deploy job bound to GitHub environment `production` |
| Invariants | pytest precedes push (red gate publishes nothing); no `continue-on-error` on gate/push/deploy/check; failure of any stage fails the run visibly |

## GitHub Environment

| Field | Value / Rule |
|---|---|
| Name | `production` |
| Created via | `gh api -X PUT repos/redmarklogic/redline/environments/production` (idempotent) |
| Holds | deployment-scoped secrets/vars when they exist (none required yet; `WIF_PROVIDER`/`GHA_SA_EMAIL` remain repo-level) |
