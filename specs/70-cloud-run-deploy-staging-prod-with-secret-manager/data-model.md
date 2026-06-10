# Data Model: Cloud Run Deploy — Staging + Prod with Secret Manager

**Feature**: 70-cloud-run-deploy-staging-prod-with-secret-manager
**Date**: 2026-06-10

This document records the Terraform resource entities, their fields, and their relationships.
No application-layer data model changes — this feature is infrastructure-only.

---

## Entities

### 1. Cloud Run Service (`google_cloud_run_v2_service`)

| Field | Staging value | Prod value | Source |
|-------|--------------|------------|--------|
| `name` | `staging-redline-api` | `prod-redline-api` | derived: `{env}-redline-api` |
| `location` | `australia-southeast1` | `australia-southeast1` | `var.region` / ADR-022 |
| `ingress` | `INGRESS_TRAFFIC_ALL` | `INGRESS_TRAFFIC_ALL` | ADR-022 Tier-1 approval |
| `deletion_protection` | `false` | `false` | explicit — version-guard rule #1 |
| `min_instance_count` | `0` | `var.min_instances_prod` (default `1`) | FR-003, FR-004 |
| `max_instance_count` | `var.max_instances_staging` (default `3`) | `var.max_instances_prod` (default `10`) | FR-005 |
| `image` | `{region}-docker.pkg.dev/{project}/{repo}/{name}:{tag}` | same pattern | `var.image_tag` |
| `service_account` | `cloud-run-api-sa@...` | same | shared SA |
| `timeout` | `300s` | `300s` | ADR-022 §5 |
| `startup_probe.initial_delay_seconds` | `10` | `10` | FR-007 |
| `startup_probe.timeout_seconds` | `5` | `5` | FR-007 |
| `startup_probe.failure_threshold` | `3` | `3` | FR-007 |
| `startup_probe.http_get.path` | `/health` | `/health` | FR-006 / spec 004 |
| `startup_probe.http_get.port` | `8080` | `8080` | FastAPI default |

**Cardinality**: 2 instances (iterated via `for_each = toset(local.environments)`)

**State transitions**:
- New revision → startup_probe evaluates → READY (routes traffic) or NOT_READY (previous revision continues serving)
- NOT_READY revision does not replace the previous; previous revision absorbs 100% traffic (SC-006)

---

### 2. Secret Manager Secret (`google_secret_manager_secret`)

| Field | Value | Source |
|-------|-------|--------|
| `secret_id` | `{env}-redline-{credential}` | FR-008 naming convention |
| `project` | `redmarklogic-prod` | `var.project_id` |
| `replication` | `auto {}` | GCP-managed multi-region replication |

**Cardinality**: `len(environments) × len(secret_bindings)` = 2 envs × N credentials

**Examples** (with default credentials `db_password`, `api_key`):
- `staging-redline-db-password`
- `staging-redline-api-key`
- `prod-redline-db-password`
- `prod-redline-api-key`

**Naming validation**: `{env}` ∈ {`staging`, `prod`}; `{credential}` ∈ `keys(local.secret_bindings)`

---

### 3. Cloud Run Service Account (`google_service_account`)

| Field | Value |
|-------|-------|
| `account_id` | `cloud-run-api-sa` |
| `display_name` | `Cloud Run API Service Account` |
| `project` | `var.project_id` |

**Cardinality**: 1 (shared across staging and prod — single-project pattern)

---

### 4. IAM Member (`google_secret_manager_secret_iam_member`)

| Field | Value | Source |
|-------|-------|--------|
| `secret_id` | per-secret reference | `google_secret_manager_secret.secrets[key].secret_id` |
| `role` | `roles/secretmanager.secretAccessor` | least-privilege |
| `member` | `serviceAccount:{cloud_run_sa_email}` | `google_service_account.cloud_run_sa.email` |

**Cardinality**: 1 per secret (same N × 2 count) — no project-level binding

---

## Relationships

```text
google_service_account.cloud_run_sa
  └─(email)──► google_cloud_run_v2_service.api[staging]
  └─(email)──► google_cloud_run_v2_service.api[prod]
  └─(member)─► google_secret_manager_secret_iam_member[*]

google_secret_manager_secret.secrets[staging-db_password]
  └─► google_secret_manager_secret_iam_member[staging-db_password]
  └─(secret_key_ref)──► google_cloud_run_v2_service.api[staging].env[DB_PASSWORD]
  └─► [version managed out-of-band: gcloud secrets versions add staging-redline-db-password]

google_secret_manager_secret.secrets[prod-db_password]
  └─► google_secret_manager_secret_iam_member[prod-db_password]
  └─(secret_key_ref)──► google_cloud_run_v2_service.api[prod].env[DB_PASSWORD]
  └─► [version managed out-of-band: gcloud secrets versions add prod-redline-db-password]
```

---

## SSOT: `locals.secret_bindings` (FR-008)

```hcl
locals {
  secret_bindings = {
    "db_password" = "DB_PASSWORD"
    "api_key"     = "API_KEY"
  }
  environments = ["staging", "prod"]
}
```

This block is the **single source of truth** for the mapping between Secret Manager secret
name suffixes and application env-var names. Adding a new credential = one new entry here.
Cloud Run service bindings and IAM members are derived automatically via `for_each`.

---

## Validation Rules

- `image_tag` must not be empty (no default; Terraform validates at plan time)
- `min_instances_prod` must be ≥ 1 (FR-004); enforced via `validation` block in `variables.tf`
- `max_instances_staging` and `max_instances_prod` must be ≥ 1 (FR-005); enforced via `validation` blocks
- No `google_secret_manager_secret_version` resource exists in Terraform — secret values never enter Terraform state (E1)
