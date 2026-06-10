# Research: Cloud Run Deploy — Staging + Prod with Secret Manager

**Feature**: 70-cloud-run-deploy-staging-prod-with-secret-manager
**Date**: 2026-06-10
**Status**: Complete — all NEEDS CLARIFICATION resolved

---

## Decision 1: Cloud Run resource version

- **Decision**: Use `google_cloud_run_v2_service` (v2 resource)
- **Rationale**: v2 resource supports `startup_probe` and `liveness_probe` natively in the 5.x provider. The legacy `google_cloud_run_service` (v1) lacks explicit probe blocks. All current GCP documentation targets v2.
- **Alternatives considered**: `google_cloud_run_service` (v1) — deprecated, missing probe support.
- **Source**: version-guard-report.md ref: https://registry.terraform.io/providers/hashicorp/google/5.45.2/docs/resources/cloud_run_v2_service

---

## Decision 2: Secret binding method

- **Decision**: Bind secrets as environment variables via `env.value_source.secret_key_ref`
- **Rationale**: FastAPI application reads secrets via `os.environ["VAR"]` (ADR-021). Env-var binding is the natural fit. Volume mounts add filesystem complexity with no benefit for string credentials.
- **Alternatives considered**: Secret volume mounts — viable for file-based config but unnecessary here.
- **Source**: https://cloud.google.com/run/docs/configuring/secrets

---

## Decision 3: IAM scope for secret access

- **Decision**: `google_secret_manager_secret_iam_member` per secret (least-privilege)
- **Rationale**: Cloud Run service account should only access secrets it is explicitly declared to use. A project-level `roles/secretmanager.secretAccessor` would grant access to all secrets in the project, violating least-privilege.
- **Alternatives considered**: `google_project_iam_member` with `roles/secretmanager.secretAccessor` — simpler but over-privileged. Rejected.
- **Source**: ADR-020 §IV (IAM governance through Terraform)

---

## Decision 4: Service account topology

- **Decision**: Single Cloud Run service account (`cloud-run-api-sa@redmarklogic-prod.iam.gserviceaccount.com`) bound to secrets for both staging and prod environments
- **Rationale**: Single-project multi-environment pattern (spec Assumptions). Two SAs would add IAM complexity without meaningful isolation benefit beyond what separate secret names already provide.
- **Alternatives considered**: Separate SA per environment — adds isolation but increases IAM boilerplate in a single-project setup. Revisit if project-per-env is adopted.
- **Source**: spec.md Assumptions + ADR-022

---

## Decision 5: Pre-flight image-digest validation (F-RT-70-005)

- **Decision**: Shell pre-flight check using `gcloud artifacts docker images describe` before `terraform apply`
- **Rationale**: Terraform cannot validate Artifact Registry image existence during plan phase without a data source that introduces a hard dependency on AR being populated. An out-of-band shell check is simpler, explicit, and surfaceable in `quickstart.md` as a mandatory step.
- **Alternatives considered**: `data "google_artifact_registry_docker_image"` — available in 5.x provider but adds implicit plan dependency; opaque failure mode if registry is unreachable.
- **Source**: red-team-findings.md F-RT-70-005 (open OQ)

---

## Decision 6: Secret version placeholder strategy

- **Decision**: Create `google_secret_manager_secret_version` with `secret_data = "REPLACE_ME"` placeholder
- **Rationale**: Cloud Run deploy fails with "no enabled version" if a secret has no versions. Terraform-managed placeholder version prevents this while making the out-of-band rotation pattern explicit. Brent rotates actual values via `gcloud secrets versions add` before first real traffic.
- **Alternatives considered**: Omit version resource and require manual version creation before apply — fragile; order-of-operations error would silently fail the first deploy.
- **Source**: GCP Secret Manager docs + spec edge case "secret version disabled or deleted"

---

## Decision 7: `deletion_protection` explicit setting

- **Decision**: Set `deletion_protection = false` explicitly on both Cloud Run services
- **Rationale**: 5.x default is `false` but 6.x changes the default to `true`. Being explicit protects against accidental lock-out if the provider is upgraded without a migration run. Required by version-guard-report.md rule #1.
- **Source**: version-guard-report.md compatibility rules, row 1

---

## Decision 8: Health-check probe placement

- **Decision**: Use `startup_probe` block (not `liveness_probe`) for the readiness gate
- **Rationale**: `startup_probe` is the correct probe type for Cloud Run v2 service revision readiness — it gates traffic routing until the probe passes. `liveness_probe` is for ongoing health monitoring. FR-007 requires readiness gating; `startup_probe` satisfies this.
- **Alternatives considered**: `liveness_probe` only — does not gate initial traffic routing; revision could be marked READY before the application is fully initialised.
- **Source**: GCP Cloud Run docs + version-guard-report.md §Cloud Run v2 reference

---

## No NEEDS CLARIFICATION items remain.

All spec requirements, ADR constraints, and red-team findings are addressed in the design.
