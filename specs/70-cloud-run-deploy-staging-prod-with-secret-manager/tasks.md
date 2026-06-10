# Tasks: Cloud Run Deploy — Staging + Prod with Secret Manager

**Input**: [plan.md](plan.md)
**Spec**: [spec.md](spec.md)
**Prerequisites**: GCP project `redmarklogic-prod` exists; Artifact Registry repo and
container image are published (spec 005 / issue #63); Terraform CLI ≥ 1.6 installed;
`gcloud` CLI authenticated; `checkov` installed.

**Version guard**: `hashicorp/google ~> 5.0` — all HCL must target 5.x API surface.
No 6.x/7.x patterns. `deletion_protection = false` explicit. `startup_probe` explicit.
`containers.env` list-style iteration only.

---

<!-- Task sizing rule: each task is a VERTICAL SLICE — one complete new behaviour,
     nothing left dangling. Split by infrastructure behaviour, not by technical layer. -->

## Phase 0: Pre-Flight & Scaffolding

**Purpose**: Validate deploy prerequisites and create the Terraform file skeleton — a
runnable `terraform validate` passes with no new resources yet applied.

- [ ] T001 Pre-flight: verify container image digest exists in Artifact Registry before any Terraform work — run `gcloud artifacts docker images describe australia-southeast1-docker.pkg.dev/redmarklogic-prod/<REPO>/redline-api@sha256:<DIGEST> --project redmarklogic-prod`; if exit non-zero STOP and resolve before T002. **Must be a digest (sha256:...), not a mutable tag. Obtain from: `gcloud artifacts docker images list REPO --include-tags --format='value(DIGEST)'`**
- [ ] T002 Create `deploy/infra/terraform/cloud_run.tf` with placeholder `# Cloud Run services — implementation in T010` comment and HCL file header
- [ ] T003 [P] Create `deploy/infra/terraform/secrets.tf` with placeholder `# Secret Manager secrets — implementation in T006` comment and HCL file header
- [ ] T004 [P] Create `deploy/infra/terraform/iam.tf` with placeholder `# IAM bindings — implementation in T008` comment and HCL file header

### Acceptance Gate

- [ ] T005 Run `terraform init && terraform validate` in `deploy/infra/terraform/` — output must be `Success! The configuration is valid.`

---

## Phase 1: Variables & Outputs Foundation

**Purpose**: Declare all variables and outputs required by US1–US3 so the HCL type
system enforces constraints before any resource is written.

### Implementation

- [ ] T006 Add to `deploy/infra/terraform/variables.tf`: `image_tag` (string, no default, description "Image digest to deploy — must be sha256:DIGEST, not a mutable tag"), `min_instances_prod` (number, default 1, validation ≥ 1 AND ≤ 5 per block below, FR-004), `max_instances_staging` (number, default 3, validation ≥ 1, FR-005), `max_instances_prod` (number, default 10, validation ≥ 1, FR-005), `artifact_registry_repo` (string, no default), `image_name` (string, default "redline-api"). Include the following validation block for `min_instances_prod`:

  ```hcl
  validation {
    condition     = var.min_instances_prod >= 1 && var.min_instances_prod <= 5
    error_message = "min_instances_prod must be between 1 and 5."
  }
  ```

- [ ] T007 Add to `deploy/infra/terraform/terraform.tfvars`: `artifact_registry_repo`, `max_instances_staging = 3`, `max_instances_prod = 10` — do NOT set `image_tag` in tfvars (must be supplied at plan time)
- [ ] T008 Add to `deploy/infra/terraform/outputs.tf`: `staging_url` (Cloud Run staging service URI), `prod_url` (Cloud Run prod service URI), `cloud_run_sa_email` (service account email for IAM audit)

### Acceptance Gate

- [ ] T009 Run `terraform validate` in `deploy/infra/terraform/` — must pass; confirm new variable validation blocks appear in plan output when `image_tag` is omitted (expect "No value for required variable")

---

## Phase 2: Service Account (Foundational — Blocks US1 and US2)

**Purpose**: Provision the Cloud Run service account so IAM bindings and Cloud Run
service resource can reference `google_service_account.cloud_run_sa.email`.

### Tests (write first — must fail before implementation begins)

- [ ] T010 Write failing `terraform plan` test: in `deploy/infra/terraform/` run `terraform plan -var="image_tag=sha256:test" -detailed-exitcode 2>&1 | Select-String "cloud_run_sa"` — confirm output shows no resource yet (test fails as expected before T011)

### Implementation

- [ ] T011 Add `google_service_account` resource `cloud_run_sa` to `deploy/infra/terraform/iam.tf`: `account_id = "cloud-run-api-sa"`, `display_name = "Cloud Run API Service Account"`, `project = var.project_id`

### Acceptance Gate

- [ ] T012 Run `terraform plan -var="image_tag=sha256:test"` — plan must show `+ google_service_account.cloud_run_sa` in the planned additions; no errors

---

## Phase 3: Secret Manager Secrets (US1 + US2 — Secret isolation per environment)

**Purpose**: Declare `google_secret_manager_secret` resources for all credentials
across both environments using the FR-008 SSOT `locals.secret_bindings` map. No
`google_secret_manager_secret_version` resources — secret values never enter Terraform state.

### Tests (write first — must fail before implementation begins)

- [ ] T013 Write failing plan assertion: `terraform plan -var="image_tag=sha256:test" -detailed-exitcode 2>&1 | Select-String "secret_manager_secret\."` — confirm zero secret resources in plan before T014

### Implementation

- [ ] T014 Add `locals` block to `deploy/infra/terraform/secrets.tf` with `secret_bindings = { "db_password" = "DB_PASSWORD", "api_key" = "API_KEY" }` and `environments = ["staging", "prod"]` — this is the FR-008 SSOT; all env-var names and secret name suffixes are defined here only. **IMPORTANT: `local.environments` and `local.secret_bindings` are both defined in `secrets.tf` and consumed by `cloud_run.tf`. Do not split or move these locals — the cross-file dependency is intentional and module-scoped.** When writing `secrets.tf`, add a comment in the `locals` block: `# Cross-file dependency: local.environments and local.secret_bindings are consumed by cloud_run.tf — do not move or split.`
- [ ] T015 Add `google_secret_manager_secret` resource `secrets` to `deploy/infra/terraform/secrets.tf` using `for_each` over `setproduct(local.environments, keys(local.secret_bindings))`; `secret_id = "${each.value.env}-redline-${each.value.credential}"`; `replication { auto {} }` — no `google_secret_manager_secret_version` resource (E1 / FR-002)

### Acceptance Gate

- [ ] T016 Run `terraform plan -var="image_tag=sha256:test"` — plan must show `+ google_secret_manager_secret.secrets["staging-db_password"]`, `["staging-api_key"]`, `["prod-db_password"]`, `["prod-api_key"]` (4 resources); confirm zero `secret_version` resources; confirm no `secret_data` attribute in plan output

---

## Phase 4: IAM Bindings (Foundational — Blocks US1 + US2 traffic)

**Purpose**: Bind the Cloud Run service account to `roles/secretmanager.secretAccessor`
on each secret individually (least-privilege). One `google_secret_manager_secret_iam_member`
per secret — no project-level binding.

### Tests (write first — must fail before implementation begins)

- [ ] T017 Write failing plan assertion: `terraform plan -var="image_tag=sha256:test" -detailed-exitcode 2>&1 | Select-String "iam_member"` — confirm zero IAM member resources before T018

### Implementation

- [ ] T018 Add `google_secret_manager_secret_iam_member` resource `secret_access` to `deploy/infra/terraform/iam.tf` using the same `for_each` key set as `secrets`; `role = "roles/secretmanager.secretAccessor"`; `member = "serviceAccount:${google_service_account.cloud_run_sa.email}"`; `secret_id = google_secret_manager_secret.secrets[each.key].secret_id`

### Acceptance Gate

- [ ] T019 Run `terraform plan -var="image_tag=sha256:test"` — plan must show 4 `google_secret_manager_secret_iam_member` resources (one per secret); each bound to `cloud_run_api_sa` email; no project-level IAM bindings

---

## Phase 5: Cloud Run Staging Service (US1 — Staging accepts live traffic)

**Purpose**: Deploy the staging Cloud Run service with min-instances = 0 (scale-to-zero),
secrets injected via `env.value_source.secret_key_ref`, and explicit `startup_probe`.
Independent test: staging service becomes READY and `/health` returns HTTP 200.

### Tests (write first — must fail before implementation begins)

- [ ] T020 Write failing plan assertion: `terraform plan -var="image_tag=sha256:test" -detailed-exitcode 2>&1 | Select-String "cloud_run_v2_service.*staging"` — confirm zero Cloud Run resources before T021

### Implementation

- [ ] T021 Add `google_cloud_run_v2_service` resource `api` to `deploy/infra/terraform/cloud_run.tf` using `for_each = toset(local.environments)`; name `"${each.key}-redline-api"`; location `var.region`; ingress `"INGRESS_TRAFFIC_ALL"`; `deletion_protection = false` (explicit — version-guard rule #1, 5.x)
- [ ] T022 Add `template` block to the Cloud Run service in `deploy/infra/terraform/cloud_run.tf`: `service_account = google_service_account.cloud_run_sa.email`; `scaling { min_instance_count = each.key == "prod" ? var.min_instances_prod : 0; max_instance_count = each.key == "prod" ? var.max_instances_prod : var.max_instances_staging }`; `timeout = "300s"` (ADR-022)
- [ ] T023 Add `containers` block to the Cloud Run service template in `deploy/infra/terraform/cloud_run.tf`: `image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_registry_repo}/${var.image_name}:${var.image_tag}"`; dynamic `env` block iterating `local.secret_bindings` using list-style iteration (5.x — version-guard rule #2); each `env` block uses `value_source.secret_key_ref { secret = google_secret_manager_secret.secrets["${each.key}-${env.key}"].secret_id; version = "latest" }`
- [ ] T024 Add explicit `startup_probe` block to the containers block in `deploy/infra/terraform/cloud_run.tf`: `initial_delay_seconds = 10`; `timeout_seconds = 5`; `failure_threshold = 3`; `http_get { path = "/health"; port = 8080 }` (FR-007 — all values explicit, no API defaults relied upon)

### Acceptance Gate

- [ ] T025 Run `terraform validate && terraform plan -var="image_tag=sha256:test"` — plan must show `+ google_cloud_run_v2_service.api["staging"]` and `+ google_cloud_run_v2_service.api["prod"]`; confirm `startup_probe` block present; confirm `deletion_protection = false` explicit; confirm no `liveness_probe` absent-warning (accepted risk E2 per plan.md)
- [ ] T026 Run checkov two-pass gate (SC-002 — blocking): `checkov -d deploy/infra/terraform --framework terraform --compact` then `terraform plan -var="image_tag=sha256:test" -out=tfplan.binary && terraform show -json tfplan.binary > tfplan.json && checkov --file tfplan.json --framework terraform_plan --compact` — zero `CKV_SECRET_*` or `CKV_GCP_*` findings in both passes

---

## Phase 6: Staging Deploy & Smoke Test (US1 acceptance)

**Purpose**: Apply Terraform to staging and verify end-to-end: READY status, health
check HTTP 200, secrets present in container but absent from config, scale-to-zero.

### Implementation

- [ ] T027 Pre-apply: create secret versions out-of-band for all staging secrets — `echo -n "ACTUAL_VALUE" | gcloud secrets versions add staging-redline-db-password --data-file=- --project redmarklogic-prod` and repeat for `staging-redline-api-key`; confirm each command exits 0 (E1 mandatory pre-traffic step)
- [ ] T028 Run `terraform apply -var="image_tag=<DIGEST>"` — apply must complete without errors; `staging_url` and `prod_url` outputs printed

### Acceptance Gate (US1)

- [ ] T029 [US1] Smoke test staging: `STAGING_URL=$(terraform output -raw staging_url); curl -sf "$STAGING_URL/health"` — HTTP 200 within 3 minutes (SC-001)
- [ ] T030 [US1] Confirm secrets absent from config: `terraform show -json | Select-String -NotMatch "secret_data"` — zero `secret_data` plaintext values in state; confirm Cloud Run service env var names match `local.secret_bindings` values (FR-002)
- [ ] T031 [US1] Scale-to-zero verification (FR-003): wait 5 minutes with no traffic; run `gcloud run revisions list --service=redline-api-staging --region=australia-southeast1 --project=redmarklogic-prod --format="table(name,status.observedGeneration,status.conditions[0].status)"` — zero active instances is confirmed when Cloud Monitoring metric `run.googleapis.com/container/instance_count` shows 0, or by observing 0 instances in the GCP console for the staging service. Note: `observedGeneration` alone does not confirm scale-to-zero; use the Monitoring metric or console view as the definitive check.

---

## Phase 7: Production Deploy & Warm-Instance Test (US2 — Production with cold-start mitigation)

**Purpose**: Promote the same verified image digest to production with min-instances ≥ 1.
Separate production secrets. Independent test: prod `/health` returns HTTP 200 within
1 second; at least one instance remains warm after 10 minutes idle.

### Implementation

- [ ] T032 [US2] Create secret versions out-of-band for all production secrets — `echo -n "ACTUAL_VALUE" | gcloud secrets versions add prod-redline-db-password --data-file=- --project redmarklogic-prod` and repeat for `prod-redline-api-key`; confirm each command exits 0; confirm prod secrets have no staging values (FR-008 environment isolation)

### Acceptance Gate (US2)

- [ ] T033 [US2] Smoke test production: `PROD_URL=$(terraform output -raw prod_url); curl -sf "$PROD_URL/health"` — HTTP 200 within 1 second (SC-003; warm instance from `min_instances_prod = 1`, FR-004)
- [ ] T034 [US2] Verify warm instance after 10 minutes idle: `gcloud run services describe prod-redline-api --region australia-southeast1 --project redmarklogic-prod` — at least 1 active instance; no cold-start delay on next request (FR-004)
- [ ] T035 [US2] Confirm staging/prod secret name isolation: run `gcloud run services describe redline-api-prod --region=australia-southeast1 --project=redmarklogic-prod --format="yaml(spec.template.spec.containers[0].env)"` and confirm every `valueFrom.secretKeyRef.name` value starts with `prod-redline-` (not `staging-redline-`). This verifies the actual isolation mechanism — not just that HTTP 200 is returned.

---

## Phase 8: Max-Instances Cap Verification (US3 — Cost protection)

**Purpose**: Confirm both services show an explicit max-instances cap matching the
agreed values in `terraform.tfvars`. Independent test: `gcloud` describe output shows
`max_instance_count` ≤ cap for both environments.

### Acceptance Gate (US3)

- [ ] T036 [US3] Verify staging max-instances cap: `gcloud run services describe staging-redline-api --region=australia-southeast1 --project=redmarklogic-prod --format="value(spec.template.scaling.maxInstanceCount)"` — confirm value = `var.max_instances_staging` (default 3, SC-005)
- [ ] T037 [US3] Verify prod max-instances cap: `gcloud run services describe prod-redline-api --region=australia-southeast1 --project=redmarklogic-prod --format="value(spec.template.scaling.maxInstanceCount)"` — confirm value = `var.max_instances_prod` (default 10, SC-005)
- [ ] T038 [US3] Confirm `max_instances_staging` and `max_instances_prod` are declared in `deploy/infra/terraform/variables.tf` with validation blocks (≥ 1) and documented values in `terraform.tfvars`

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Idempotency proof, rollback verification, and final SC-002 gate.

- [ ] T039 [P] Idempotency test (SC-004): `terraform plan -var="image_tag=<SAME_DIGEST>" -detailed-exitcode` — must exit code 0 (no changes); if exit code 2 inspect plan output and resolve drift before marking complete
- [ ] T040 [P] Rollback test (SC-006): deploy a revision with a non-existent image digest; confirm Cloud Run does NOT mark new revision READY; confirm previous revision continues serving 100% traffic via `gcloud run revisions list --service staging-redline-api --region australia-southeast1 --project redmarklogic-prod`; redeploy good digest and confirm traffic returns
- [ ] T041 Final checkov two-pass gate (SC-002 — repeat after all resources added): `checkov -d deploy/infra/terraform --framework terraform --compact` then regenerate `tfplan.json` and `checkov --file tfplan.json --framework terraform_plan --compact` — zero findings in both passes
- [ ] T042 Final `terraform show` review: `terraform show -json | python -c "import sys,json; d=json.load(sys.stdin); assert 'secret_data' not in json.dumps(d), 'FAIL: secret_data found in state'; print('CLEAN: no secret_data in state')"` — script exits non-zero if `secret_data` is present; pass only on `CLEAN` output. PowerShell alternative: `terraform show -json | Select-String "secret_data"` — any match is a FAIL; no output is a PASS (SC-002 final confirmation)

### Acceptance Gate

- [ ] T043 All SC-001 through SC-006 verified; quickstart.md checklist signed off; no plaintext secrets in `terraform show` output; PR ready for review

---

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies on incomplete tasks)
- `[USN]` = which user story the task delivers
- TDD applied to infrastructure: write a failing `terraform plan` assertion (Red), confirm it shows no resource, implement the HCL (Green)
- The Acceptance Gate at the end of each phase is a hard stop — do not start the next phase until it passes
- T001 (image-digest pre-flight) is a BLOCKING gate; never skipped (F-RT-70-005)
- T026 and T041 (checkov two-pass gate) are BLOCKING; zero findings required in both passes (SC-002)
- T027 and T032 (secret version creation) must run before `terraform apply` in their respective phases (E1)
- No `google_secret_manager_secret_version` resource in Terraform — all secret versions managed out-of-band via `gcloud` (E1 / FR-002)
- Version guard in effect: `hashicorp/google ~> 5.0` — no 6.x/7.x API patterns; `deletion_protection = false` explicit; `startup_probe` explicit; list-style `containers.env` iteration
- `liveness_probe` intentionally absent (accepted risk E2 per plan.md §Health-Check Probe Configuration)
- Use `finishing-a-development-branch` skill to complete the work
