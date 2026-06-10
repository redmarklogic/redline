# Implementation Plan: Cloud Run Deploy — Staging + Prod with Secret Manager

**Branch**: `feature/70-cloud-run-deploy-staging-prod-with-secret-manager` | **Date**: 2026-06-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/70-cloud-run-deploy-staging-prod-with-secret-manager/spec.md`

## Summary

Provision staging and production Cloud Run services backed by Secret Manager, declared
entirely in Terraform (ADR-020). Staging scales to zero; production holds one warm
instance. Each environment binds secrets by reference only — no secret value appears in
state, manifests, or source control. A pre-flight image-digest check guards every deploy
(F-RT-70-005). All Terraform targets the 5.x provider API.

## Technical Context

**Language/Version**: HCL (Terraform ≥ 1.6), Python 3.14 (health-check endpoint only — already implemented)

**Primary Dependencies**:
- `hashicorp/google ~> 5.0` (pinned in `deploy/infra/terraform/versions.tf`)
- `google_cloud_run_v2_service` (5.x resource schema)
- `google_secret_manager_secret` (versions managed out-of-band via `gcloud`)
- `google_secret_manager_secret_iam_binding`
- `gcloud artifacts docker images describe` (pre-flight check, not Terraform)

**Storage**: `deploy/infra/terraform/` — new files `cloud_run.tf`, `secrets.tf`, `iam.tf`; updated `variables.tf`, `outputs.tf`, `terraform.tfvars`

**Testing**:
- `terraform validate` + `terraform plan` (no apply in PR)
- `checkov` or `tfsec` against plan output (SC-002 gate: zero secret values in plain text)
- Manual smoke test: `curl https://<staging-url>/health` → HTTP 200
- Idempotency test: apply twice, diff Cloud Run service descriptions

**Target Platform**: GCP Cloud Run (australia-southeast1), Secret Manager (same project `redmarklogic-prod`)

**Project Type**: Infrastructure-as-Code — Terraform HCL only; no application code changes

**Performance Goals**:
- Staging: deploy-to-READY ≤ 3 minutes (SC-001)
- Production: first-request latency ≤ 1 second with min-instances = 1 (SC-003)

**Constraints**:
- Provider pinned to `~> 5.0` — all resources must use 5.x API surface (version-guard-report.md)
- `deletion_protection` must be set explicitly (default changed in 6.x; be explicit to avoid drift)
- `containers.env` is a list in 5.x — use list-style iteration, not set-based access
- Secret values never appear in `locals`, variable defaults, or `terraform.tfvars`
- Secret naming convention: `{env}-redline-{credential}` (e.g., `staging-redline-db-password`) — FR-008 SSOT
- CPU allocation: throttled (ADR-022 §3)
- Request timeout: 300 s (ADR-022 §5)
- Health-check probe: initial delay ≥ 10 s, timeout 5 s, failure threshold 3 (FR-007)
- Region: `australia-southeast1` (ADR-022 §1, `terraform.tfvars`)
- GCP project: `redmarklogic-prod` (single-project, multi-environment pattern)

**Scale/Scope**: Three new HCL files; ~4 variable additions; ~3 output additions; no Python changes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Verdict | Notes |
|-----------|---------|-------|
| I. Single Source of Truth | PASS | Secret names and env-var mappings declared once in a shared `locals` block (FR-008). `terraform.tfvars` remains the SSOT for project identifiers. No duplication across staging/prod. |
| II. Hook-First Enforcement | PASS | SC-002 requires a `checkov`/`tfsec` pre-apply gate — automated check, not human inspection alone. |
| III. Defence-in-Depth | PASS | Terraform state (deterministic), checkov/tfsec scan (deterministic), manual smoke test (probabilistic) — three independent layers. |
| IV. Dependency Direction | N/A | No skill/agent references introduced. |
| V. Facade Boundaries | N/A | Infrastructure only; no code boundary changes. |
| VI. Data-Driven Configuration | PASS | Staging/prod config differences expressed as variables (`min_instances`, secret name prefix), not conditional branches in HCL. |
| VII. Shared Taxonomy | N/A | No taxonomy changes. |
| VIII. Determinism Over LLM Inference | PASS | All values sourced from spec, ADR-022, version-guard-report.md — no inferred values. |
| IX. Citation-Only Knowledge Storage | N/A | No standards knowledge store changes. |
| XV. Infrastructure as Code | PASS | All Cloud Run and Secret Manager resources in `deploy/infra/terraform/`. No `gcloud` writes except the pre-flight read-only digest check. |
| XVI. Process Environment as Sole Config Source | PASS | Secrets injected via Secret Manager env-var bindings (not `.env` files, not `load_dotenv()`). Container reads `os.environ["VAR"]` — no default fallback. |

No violations. No complexity justification required.

## Project Structure

### Terraform (this feature)

```text
deploy/infra/terraform/
├── main.tf                  # existing — provider + project data source (no change)
├── apis.tf                  # existing — API enablement (no change; secretmanager.googleapis.com already present)
├── versions.tf              # existing — hashicorp/google ~> 5.0 (no change)
├── variables.tf             # MODIFIED — add staging/prod instance caps, container image variable
├── outputs.tf               # MODIFIED — add staging_url, prod_url outputs
├── terraform.tfvars         # MODIFIED — add image_tag, max_instances_staging, max_instances_prod
├── cloud_run.tf             # NEW — google_cloud_run_v2_service for staging + prod
├── secrets.tf               # NEW — google_secret_manager_secret resources only (no version resources)
└── iam.tf                   # NEW — IAM bindings: Cloud Run SA → Secret Manager secrets
```

### Spec artifacts

```text
specs/70-cloud-run-deploy-staging-prod-with-secret-manager/
├── spec.md                  # existing
├── plan.md                  # this file
├── research.md              # Phase 0 output
├── data-model.md            # Phase 1 output
├── quickstart.md            # Phase 1 output — manual verification checklist
└── tasks.md                 # generated by speckit.tasks
```

No Python source changes. No Dockerfile changes. No new GCP APIs required (all already in `terraform.tfvars`).

## Phase 0: Research

### Resolved Decisions

**Decision**: Use `google_cloud_run_v2_service` (not the legacy `google_cloud_run_service`).
- **Rationale**: v2 resource supports `startup_probe` and `liveness_probe` blocks natively; aligns with current GCP documentation. 5.x provider supports v2 fully.
- **Alternatives considered**: `google_cloud_run_service` (v1 — deprecated, missing probe blocks).

**Decision**: Bind secrets to Cloud Run as environment variables via `env.value_source.secret_key_ref` (not volume mounts).
- **Rationale**: Environment variable binding is simpler for a FastAPI application reading `os.environ["VAR"]`. Volume mounts add complexity with no benefit for string credentials.
- **Alternatives considered**: Secret volume mounts — viable but unnecessarily complex for env-var use cases.

**Decision**: IAM binding uses `google_secret_manager_secret_iam_member` (per-secret, per-SA) not a project-level role.
- **Rationale**: Least-privilege — Cloud Run service account can only read secrets it is explicitly bound to. Project-level `roles/secretmanager.secretAccessor` would grant access to all secrets.
- **Alternatives considered**: Project-level role — simpler HCL, but violates least-privilege. Rejected.

**Decision**: Single Cloud Run service account for both environments in the same GCP project.
- **Rationale**: Spec uses single-project multi-environment pattern (Assumptions). Two SAs would add IAM complexity without isolation benefit beyond what secret name separation already provides. Revisit if project-per-env is adopted.
- **Alternatives considered**: Separate SA per env — additional isolation but out of scope for single-project pattern.

**Decision**: Pre-flight image-digest check via `gcloud artifacts docker images describe` (shell script / manual step) before `terraform apply`.
- **Rationale**: F-RT-70-005 open item. Terraform cannot query Artifact Registry before planning; the check must be a separate pre-apply step. A shell one-liner satisfies the requirement without adding a Terraform data source.
- **Alternatives considered**: `data "google_artifact_registry_docker_image"` — available in 5.x but adds implicit plan dependency on registry availability. Out-of-band shell check is simpler and more explicit.

**Decision**: Terraform declares `google_secret_manager_secret` resources only (name, replication, labels). No `google_secret_manager_secret_version` resource is managed by Terraform.
- **Rationale**: Storing `secret_data` as a tracked Terraform attribute — even a placeholder — creates a state entry that will record a real secret value if the resource is ever imported or refreshed after manual rotation. Terraform state in GCS holds all attribute values in plaintext; this directly violates FR-002. All secret versions (initial and rotations) are created out-of-band by Brent using `gcloud secrets versions add`.
- **Required manual pre-traffic step**: Before any Cloud Run deploy, Brent must create at least one enabled secret version for every secret resource. Cloud Run startup will fail with "no enabled version" if this step is skipped.
- **Alternatives considered**: `google_secret_manager_secret_version` with `secret_data = "REPLACE_ME"` placeholder — rejected because the same tracked attribute will record real values on import or refresh, violating FR-002 (E1).

All NEEDS CLARIFICATION items resolved. See full notes in `research.md`.

## Phase 1: Design

### Data Model

See [data-model.md](data-model.md) for full entity definitions.

Key entities:

| Entity | Terraform Resource | Cardinality |
|--------|-------------------|-------------|
| Cloud Run Service | `google_cloud_run_v2_service` | 2 (staging, prod) |
| Secret | `google_secret_manager_secret` | N × 2 envs (one per credential per env) |
| IAM Member | `google_secret_manager_secret_iam_member` | 1 per secret (CR SA → secret) |
| Cloud Run SA | `google_service_account` | 1 (shared, least-privilege) |

**Note**: `google_secret_manager_secret_version` is intentionally absent from Terraform. Secret versions are managed out-of-band via `gcloud secrets versions add` (E1 — required manual pre-traffic step).

### Secret Naming Convention (FR-008 SSOT)

```hcl
locals {
  # Canonical secret → env-var mapping.
  # Add new credentials here; staging and prod names are derived automatically.
  secret_bindings = {
    "db_password" = "DB_PASSWORD"
    "api_key"     = "API_KEY"
  }

  environments = ["staging", "prod"]
}
```

Secret Manager name: `${env}-redline-${credential}` (e.g., `staging-redline-db-password`).
Cloud Run env var: value from `secret_bindings` map (e.g., `DB_PASSWORD`).

This locals block is the single definition — staging and prod Cloud Run services both iterate the same map.

### Cloud Run Service Configuration (per environment)

```hcl
resource "google_cloud_run_v2_service" "api" {
  for_each = toset(local.environments)

  name     = "${each.key}-redline-api"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  deletion_protection = false  # explicit — 5.x default is false; set to survive terraform destroy

  template {
    service_account = google_service_account.cloud_run_sa.email

    scaling {
      min_instance_count = each.key == "prod" ? var.min_instances_prod : 0
      max_instance_count = each.key == "prod" ? var.max_instances_prod : var.max_instances_staging
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_registry_repo}/${var.image_name}:${var.image_tag}"

      # Secret env-var bindings — iterated from locals.secret_bindings
      dynamic "env" {
        for_each = local.secret_bindings
        content {
          name = env.value
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.secrets["${each.key}-${env.key}"].secret_id
              version = "latest"
            }
          }
        }
      }

      startup_probe {
        initial_delay_seconds = 10
        timeout_seconds       = 5
        failure_threshold     = 3
        http_get {
          path = "/health"
          port = 8080
        }
      }
    }

    timeout = "300s"
  }
}
```

### Health-Check Probe Configuration (FR-007)

Explicit `startup_probe` block — no reliance on API defaults (which are removed in 6.x):
- `initial_delay_seconds = 10` (≥ 10 s, FR-007)
- `timeout_seconds = 5`
- `failure_threshold = 3`
- Path: `/health` (implemented by spec 004)
- Port: 8080 (FastAPI default)

**Accepted risk — liveness probe not configured (E2)**: No `liveness_probe` block is defined in this feature. Rationale: Phase 1 scope targets first-deploy correctness; production runs a single warm instance and is expected to be redeployed on failure rather than restarted in-place. A degraded-but-not-crashed instance will continue receiving traffic until a new deploy is triggered. This is an accepted operational risk for Phase 1 under single-instance production. Revisit when an uptime SLA is formalised (Phase 2).

### Secret Manager Resources

```hcl
# One secret resource per (env, credential) combination
resource "google_secret_manager_secret" "secrets" {
  for_each = {
    for pair in setproduct(local.environments, keys(local.secret_bindings)) :
    "${pair[0]}-${pair[1]}" => { env = pair[0], credential = pair[1] }
  }

  secret_id = "${each.value.env}-redline-${each.value.credential}"
  project   = var.project_id

  replication {
    auto {}
  }
}
```

### IAM Bindings (Least-Privilege)

One `google_secret_manager_secret_iam_member` per secret: Cloud Run SA bound to `roles/secretmanager.secretAccessor` on each secret individually. No project-level binding.

### Pre-Flight Image-Digest Check (F-RT-70-005)

Documented in `quickstart.md` as a mandatory pre-apply step. Shell command:

```bash
gcloud artifacts docker images describe \
  REGION-docker.pkg.dev/PROJECT/REPO/IMAGE@sha256:DIGEST \
  --project PROJECT
```

If the command returns exit code non-zero, the deploy procedure stops. This check is listed as Task T-000 (first task, blocking).

### Instance Configuration (Variables)

| Variable | Type | Staging default | Prod default | Description |
|----------|------|----------------|--------------|-------------|
| `min_instances_prod` | `number` | — | `1` | Warm instance count for prod (FR-004) |
| `max_instances_staging` | `number` | `3` | — | Cost cap for staging (FR-005) |
| `max_instances_prod` | `number` | — | `10` | Cost cap for prod (FR-005) |
| `image_tag` | `string` | — | — | Image tag or digest to deploy (no default — must be explicit) |
| `artifact_registry_repo` | `string` | — | — | AR repository name |
| `image_name` | `string` | `redline-api` | — | Container image name |

### SC-002 Verification Gate

`checkov` scans both the HCL source directory and the JSON plan output before apply. The gate passes when zero findings of type `SECRET_IN_PLAINTEXT` or equivalent are returned from either pass. This is a blocking pre-apply step documented in `quickstart.md`.

Two-pass command (E3 — both required):
```bash
# Pass 1: static HCL scan
checkov -d deploy/infra/terraform --framework terraform --compact

# Pass 2: plan-output scan (catches plan-time resolved values that static scan misses)
checkov --file tfplan.json --framework terraform_plan --compact
```

### New Outputs

| Output | Value | Consumer |
|--------|-------|----------|
| `staging_url` | Cloud Run staging service URL | Brent — smoke test |
| `prod_url` | Cloud Run prod service URL | Brent — smoke test |
| `cloud_run_sa_email` | Service account email | IAM audit |

## Phase 2: Implementation Tasks

See [tasks.md](tasks.md) (generated by speckit.tasks).

---

## Extension Hooks

**Optional Hook**: critique
Command: `/speckit.critique.run`
Description: Challenges the spec and plan through product and engineering lenses

Prompt: Run spec critique before proceeding to tasks?
To execute: `/speckit.critique.run`
