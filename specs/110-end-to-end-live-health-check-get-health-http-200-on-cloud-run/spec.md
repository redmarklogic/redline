# Feature Specification: End-to-End Live Health Check on Cloud Run

**Feature Branch**: `feature/110-end-to-end-live-health-check-get-health-http-200-on-cloud-run`

**Created**: 2026-06-11

**Status**: Draft

**Input**: GitHub issue [#110](https://github.com/redmarklogic/redline/issues/110) — "End-to-end live health check: GET /health → HTTP 200 on Cloud Run"

## Source Reconciliation Summary

Primary authority: issue #110 delivery plan, corrected against the codebase and the
founder-ratified launch-topology decisions (2026-06-11). Conflicts resolved with the
founder before this spec was written:

| Item | Resolution | Decided by |
|------|------------|------------|
| Health response body | App contract wins: `{"status": "healthy"}` (issue #110 said `{"status": "ok"}` — superseded) | Founder, 2026-06-11 |
| Shaping gate | Waived — issue #110 staged plan + ratified topology doc provide scope and appetite | Founder, 2026-06-11 |
| Prod warm instance | Scale-to-zero fix included in scope (topology follow-up #7) | Founder, 2026-06-11 |
| Secret population | Real values populated during this feature (not placeholders); Sydney replication pinning must precede population (topology follow-up #4) | Founder, 2026-06-11 |

### Canonical values (SSOT: `deploy/infra/terraform/terraform.tfvars`)

| Item | Value | Source |
|------|-------|--------|
| GCP project | `redmarklogic-prod` | terraform.tfvars |
| Region | `australia-southeast1` | terraform.tfvars |
| Artifact Registry repo | `redline-repo` | terraform.tfvars |
| Image name | `redline-api` | variables.tf (default) |
| Full image path | `australia-southeast1-docker.pkg.dev/redmarklogic-prod/redline-repo/redline-api:<commit-sha>` | cloud_run.tf |
| Service names | `staging-redline-api`, `prod-redline-api` | cloud_run.tf |
| Image tag policy | Immutable commit SHA, supplied at apply time via `-var image_tag=<sha>` — never stored in tfvars | terraform.tfvars design note |
| Health endpoint | `GET /health`, port 8080, returns `{"status": "healthy"}` | cloud_run.tf startup_probe; src/marker/api/health.py |
| Service URL outputs | `staging_url`, `prod_url` | cloud_run.tf |
| Secrets | `db_password` → `DB_PASSWORD`, `api_key` → `API_KEY`, per environment | secrets.tf `secret_bindings` |
| CI workflow | `.github/workflows/ci.yml`, WIF auth via repo vars `WIF_PROVIDER`, `GHA_SA_EMAIL` | ci.yml |
| Default branch | `master` (ci.yml currently triggers on `main`/`release/**` — mismatch to fix) | repo settings; ci.yml |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Staging backend is live and verifiable (Priority: P1)

The founder provisions the existing Cloud Run infrastructure with a real container
image and verifies the staging backend is publicly reachable: calling the health
endpoint of the staging service returns HTTP 200 with the contract body.

**Why this priority**: This is the issue's acceptance criterion and the walking
skeleton's first live milestone (epic #89). Everything else exists to make this
repeatable.

**Independent Test**: Build and push an image manually, run `terraform apply` with
that image tag, then `curl <staging_url>/health` — HTTP 200 with
`{"status": "healthy"}` proves the full chain (image → registry → service → app).

**Acceptance Scenarios**:

1. **Given** a backend image exists in Artifact Registry tagged with a commit SHA,
   **When** infrastructure is applied with that image tag, **Then** the
   `staging-redline-api` service exists in GCP and reports Ready.
2. **Given** the staging service is deployed, **When** an unauthenticated client
   requests `<staging_url>/health`, **Then** the response is HTTP 200 with body
   `{"status": "healthy"}`.
3. **Given** no infrastructure has been applied yet, **When** the founder lists
   Cloud Run services in the project, **Then** zero services exist (verified
   starting state).

---

### User Story 2 - Secrets and cost posture are correct before go-live (Priority: P1)

Real secret values are stored Sydney-pinned before any service starts, and the
production service sleeps (zero warm instances) from its first deployment, so the
first apply creates no compliance debt and no undecided cost.

**Why this priority**: Both are blocking prerequisites for User Story 1, not
follow-ups. A service revision referencing an empty secret fails to deploy, so the
health check can never pass without populated secrets. The ratified data-residency
decision requires pinning before real secret material lands, and the ratified
cold-start policy requires production to sleep by default.

**Independent Test**: After apply, secret material is stored only in the Sydney
region, every environment secret has an accessible current version, and the
production service shows zero minimum instances.

**Acceptance Scenarios**:

1. **Given** secrets exist with no versions, **When** secret replication is changed
   to Sydney-pinned and real values are added, **Then** every secret in both
   environments has a current accessible version stored only in `australia-southeast1`.
2. **Given** secrets are populated, **When** infrastructure is applied, **Then**
   both service revisions deploy successfully (no failed revision from missing
   secret versions).
3. **Given** the ratified scale-to-zero default, **When** infrastructure is
   applied, **Then** the production service has minimum instances 0 and accrues no
   idle compute cost.

---

### User Story 3 - CI publishes a runnable image on every push (Priority: P2)

A push to a deployable branch automatically builds the backend container image and
pushes it to Artifact Registry tagged with the commit SHA, replacing the current
placeholder step.

**Why this priority**: Removes the manual build/push from the deploy chain. Without
it the live service exists but cannot be updated except by hand.

**Independent Test**: Push a commit to a branch the workflow watches; the workflow
run completes the build-and-push step and the image with that commit's SHA tag is
visible in Artifact Registry.

**Acceptance Scenarios**:

1. **Given** the CI workflow runs on a watched branch, **When** the build-and-push
   step executes, **Then** an image tagged with the triggering commit SHA exists in
   `australia-southeast1-docker.pkg.dev/redmarklogic-prod/redline-repo/redline-api`.
2. **Given** the deploy job is configured with the `production` GitHub Actions
   environment, **When** the job runs, **Then** it consumes secrets/variables scoped
   to that environment.

---

### User Story 4 - Merge to master runs the pipeline end-to-end (Priority: P3)

Merging to the repository's default branch (`master`) triggers the full pipeline:
test → build → push → deploy → automated health check, with no manual steps.

**Why this priority**: Last stage of the issue's delivery plan. Valuable only after
User Stories 1-3 prove each link manually.

**Independent Test**: Merge the feature PR to `master`; observe a single workflow
run that ends with a passing automated health check against the staging URL.

**Acceptance Scenarios**:

1. **Given** the workflow trigger currently watches `main`/`release/**`, **When**
   the trigger is corrected to the default branch, **Then** a merge to `master`
   starts the pipeline (and pushes to `main` no longer would).
2. **Given** a merge to `master`, **When** the pipeline completes, **Then** every
   stage succeeded including an automated HTTP 200 health check against the staging
   service, with no manual intervention.

---

### Edge Cases

- Secret version missing or inaccessible at deploy time → the service revision
  fails to deploy. Prevented by User Story 2 ordering (populate before apply);
  if it occurs, the failed revision must not affect the previously serving revision.
- `image_tag` not supplied at apply time → apply fails fast (by design — mutable
  tags are deliberately rejected). The error must not be "fixed" by adding a
  default tag.
- Image pushed but startup probe fails (app crash, wrong port) → service reports
  not Ready; health check from outside returns non-200. The pipeline must surface
  this as a failure, not report deploy success.
- WIF authentication fails in CI (repo vars unset/stale) → build-and-push step
  fails before any push; no partial image state.
- Changing secret replication on an existing secret is a replace, not an in-place
  update — values must be re-added after the replacement; ordering matters
  (pin first, then populate, per ratified follow-up #4).
- Health endpoint is exempt from rate limiting — repeated probe calls (Cloud Run
  startup probe + CI check + manual curl) must not throttle each other.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The CI workflow MUST build the backend container image and push it to
  the canonical Artifact Registry path, replacing the existing placeholder step.
- **FR-002**: Every pushed image MUST be tagged with the immutable commit SHA of the
  triggering commit; mutable tags (e.g. `latest`) MUST NOT be used for deployment.
- **FR-003**: Secret replication MUST be Sydney-pinned (`australia-southeast1`,
  user-managed) BEFORE any real secret value is stored (ratified data-residency
  decision, topology follow-up #4).
- **FR-004**: Real secret values MUST be populated for every secret binding in both
  environments before the first infrastructure apply, so service revisions can
  resolve their secret references.
- **FR-005**: Cloud Run infrastructure MUST be provisioned from the existing IaC
  with the image tag supplied at apply time; the apply MUST create both
  `staging-redline-api` and `prod-redline-api` services in Ready state.
- **FR-006**: The production service MUST default to zero minimum instances
  (scale-to-zero); the current lower bound of 1 MUST be corrected (ratified
  cold-start policy, topology follow-up #7).
- **FR-007**: The staging service URL MUST be obtainable from infrastructure
  outputs, and `GET <staging_url>/health` MUST return HTTP 200 with JSON body
  `{"status": "healthy"}` — compared as parsed JSON, not byte-for-byte (the
  serializer emits compact JSON without spaces).
- **FR-008**: The deploy job MUST run under a GitHub Actions environment named
  `production`, so deployment secrets/variables are scoped to that environment.
- **FR-009**: The CI workflow trigger MUST match the repository's default branch
  (`master`), replacing the current `main`/`release/**` trigger. This change MUST
  land only after FR-001 through FR-008 are verified (staged delivery).
- **FR-010**: After merge to the default branch, the pipeline MUST run end-to-end —
  test, build, push, deploy, automated health check against the staging URL — with
  no manual steps, and MUST fail visibly if the health check does not return HTTP 200.
- **FR-011**: The staging service MUST be publicly invocable without
  authentication, declared in IaC (unauthenticated-invoker grant on staging
  only). The grant is service-wide by nature — invoker IAM cannot be scoped to a
  path, so the ENTIRE staging API surface is public, not just the health
  endpoint; this is accepted for the walking skeleton (no real data) and
  revisited at front-door work (#74/#75). The production service MUST remain
  IAM-private — no public invoker — until #74/#75 decides its exposure.

### Key Entities

- **Backend image**: The containerised backend, identified by registry path +
  commit-SHA tag. Produced by CI (or manually in Stage 1), consumed by the Cloud
  Run services.
- **Staging service** (`staging-redline-api`): The publicly invocable service
  (unauthenticated-invoker grant) whose health endpoint is the acceptance target.
  Scales to zero when idle.
- **Production service** (`prod-redline-api`): Created by the same apply; receives
  no traffic in this feature; IAM-private (no public invoker); must sleep (zero
  minimum instances).
- **Environment secrets**: Per-environment secret values (`DB_PASSWORD`, `API_KEY`
  for staging and prod), Sydney-pinned, each with an accessible current version.
- **Pipeline run**: A single workflow execution tying commit SHA → image tag →
  deployed revision → health check result.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `curl <staging_url>/health` returns HTTP 200 with JSON body
  `{"status": "healthy"}`, compared as parsed JSON (issue #110 acceptance, body
  corrected per reconciliation).
- **SC-002**: Listing Cloud Run services in the project shows both services in
  Ready state (was zero before this feature).
- **SC-003**: An image tagged with a real commit SHA is present in Artifact
  Registry, and the serving revision references exactly that tag.
- **SC-004**: All secret material for both environments is stored only in the
  Sydney region, and every secret has an accessible current version.
- **SC-005**: The production service reports zero minimum instances; idle compute
  cost for the pair is ~$0 (within the ratified cost ceiling).
- **SC-006**: A single merge to `master` produces one pipeline run that completes
  every stage including the automated health check, with zero manual intervention.

## Assumptions

- Shaping waived by founder (2026-06-11): issue #110's staged delivery plan plus
  the founder-ratified launch-topology document substitute for a shaped Pitch.
- Workload Identity Federation is already functional (issue #68 merged): the CI
  auth step works and repo variables `WIF_PROVIDER` / `GHA_SA_EMAIL` are set.
- The Dockerfile from issue #67 builds a runnable image listening on port 8080
  with `/health` served — no application code changes are needed or in scope.
- "Real secret values" for services that do not exist yet (no database is
  provisioned): the canonical credential is generated and stored now and becomes
  the value the future service is configured with. No placeholder rotation later.
- The `production` GitHub Actions environment is created in repo settings by the
  founder or an authorised maintainer (repo Settings → Environments) — repository
  configuration, not code.
- The budget/runaway-bill safeguard (topology follow-up #8) is a prerequisite for
  production *traffic*, not for this health-check deployment; it remains out of
  scope here.
- Terraform state backend (GCS bucket `redmarklogic-tf-state`) exists from
  bootstrap; `terraform init` succeeds against it.

## Out of Scope

- Custom domain / HTTPS certificate (follow-ups #74/#75).
- Production traffic, public access to `prod-redline-api`, IAP, OAuth wiring, and
  the runaway-bill safeguard.
- Any application code change (health endpoint body is fixed by contract).
- Database provisioning (Cloud SQL) and its connection strategy ADR.
