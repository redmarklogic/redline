# Quickstart: Cloud Run Deploy — Staging + Prod with Secret Manager

**Feature**: 70-cloud-run-deploy-staging-prod-with-secret-manager
**Owner**: Brent (DevOps)
**Date**: 2026-06-10

This checklist is the authoritative verification sequence for feature 70.
Execute steps in order. Do not proceed past a blocking step on failure.

---

## Prerequisites (confirm before starting)

- [ ] GCP project `redmarklogic-prod` exists and `terraform apply` (spec 005) has been run
- [ ] Artifact Registry repository exists (spec 005 / issue #63)
- [ ] Container image is published to Artifact Registry (spec 005)
- [ ] `deploy/infra/terraform/` is on the feature branch
- [ ] Terraform CLI ≥ 1.6 installed: `terraform --version`
- [ ] `gcloud` CLI authenticated: `gcloud auth application-default login`
- [ ] `checkov` installed: `checkov --version`

---

## Step 0: Pre-flight image-digest check (F-RT-70-005 — BLOCKING)

Before running `terraform plan`, confirm the image you intend to deploy exists in Artifact Registry.

```bash
# Replace placeholders with actual values
IMAGE_REF="australia-southeast1-docker.pkg.dev/redmarklogic-prod/REPO/redline-api:TAG_OR_DIGEST"

gcloud artifacts docker images describe "$IMAGE_REF" --project redmarklogic-prod
```

- [ ] Command exits 0 and prints image metadata
- [ ] If exit non-zero: **STOP** — fix the image reference before continuing

---

## Step 1: Terraform validate

```bash
cd deploy/infra/terraform
terraform init
terraform validate
```

- [ ] Output: `Success! The configuration is valid.`

---

## Step 2: Terraform plan

```bash
terraform plan -var="image_tag=<YOUR_TAG_OR_DIGEST>" -out=tfplan.binary
terraform show -json tfplan.binary > tfplan.json
```

- [ ] Plan completes without errors
- [ ] Review resource additions: Cloud Run services (×2), secrets, IAM members, SA
- [ ] Confirm no `secret_data` values appear in plan output (spot-check)

---

## Step 3: checkov security gate (SC-002 — BLOCKING)

```bash
# Pass 1: static HCL scan
checkov -d deploy/infra/terraform --framework terraform --compact

# Pass 2: plan-output scan (catches plan-time resolved values that static scan misses)
checkov --file tfplan.json --framework terraform_plan --compact
```

- [ ] Zero findings of type `CKV_SECRET_*` or `CKV_GCP_*` from **both** passes
- [ ] If findings exist in either pass: **STOP** — resolve before applying

---

## Step 4: Terraform apply

```bash
terraform apply tfplan.binary
```

- [ ] Apply completes without errors
- [ ] Outputs `staging_url` and `prod_url` printed to terminal

---

## Step 5: Create secret versions (BLOCKING before Cloud Run deploy)

**Terraform does NOT create secret versions.** Secret values never enter Terraform state.
You must create at least one enabled version for every secret before Cloud Run can start —
the service will fail startup if any bound secret has no enabled version.

```bash
# Repeat for each credential (db_password, api_key, …)
echo -n "ACTUAL_VALUE" | gcloud secrets versions add staging-redline-db-password \
  --data-file=- --project redmarklogic-prod

echo -n "ACTUAL_VALUE" | gcloud secrets versions add prod-redline-db-password \
  --data-file=- --project redmarklogic-prod
```

- [ ] Each `gcloud` command succeeds and prints the new version number
- [ ] All secrets in `local.secret_bindings` have an enabled version for both environments
- [ ] If any version is missing: **STOP** — Cloud Run startup will fail

---

## Step 6: Staging smoke test

```bash
STAGING_URL=$(terraform output -raw staging_url)

# Health check
curl -sf "$STAGING_URL/health"
```

- [ ] HTTP 200 response received within 3 minutes of apply (SC-001)
- [ ] Response body indicates service healthy
- [ ] No secret values appear in response body or headers

---

## Step 7: Staging scaling verification (SC-003 proxy — scale-to-zero)

- [ ] Wait 5 minutes with no traffic to staging
- [ ] `gcloud run services describe staging-redline-api --region australia-southeast1 --project redmarklogic-prod` — confirm instance count drops to 0 (FR-003)

---

## Step 8: Production smoke test

```bash
PROD_URL=$(terraform output -raw prod_url)

curl -sf "$PROD_URL/health"
```

- [ ] HTTP 200 response (SC-001 for prod)
- [ ] Response within 1 second (SC-003 — warm instance from min-instances = 1, FR-004)

---

## Step 9: Max-instances verification (SC-005)

```bash
# Staging
gcloud run services describe staging-redline-api \
  --region australia-southeast1 --project redmarklogic-prod \
  --format="value(spec.template.metadata.annotations)"

# Prod
gcloud run services describe prod-redline-api \
  --region australia-southeast1 --project redmarklogic-prod \
  --format="value(spec.template.metadata.annotations)"
```

- [ ] Staging shows `max_instance_count` = `var.max_instances_staging` (default 3)
- [ ] Prod shows `max_instance_count` = `var.max_instances_prod` (default 10)

---

## Step 10: Idempotency test (SC-004)

```bash
# Confirm no changes without executing an apply
# Exit code 0 = no changes (idempotent). Exit code 2 = changes detected (investigate).
terraform plan -var="image_tag=<SAME_TAG>" -detailed-exitcode
```

- [ ] Command exits with code `0` — no changes planned (idempotent)
- [ ] If exit code `2`: inspect plan output, identify the drifted resource, and investigate before applying

---

## Step 11: Revision failure rollback (SC-006)

*Test only if a previous revision exists.*

- [ ] Deploy a revision with a broken health-check (e.g., set image tag to a non-existent digest)
- [ ] Cloud Run does not mark the new revision READY
- [ ] Previous revision continues serving 100% of traffic (confirm via `gcloud run revisions list`)
- [ ] Revert to the good image tag; confirm traffic returns to new READY revision

---

## Completion sign-off

- [ ] All blocking steps passed
- [ ] SC-001 through SC-006 verified
- [ ] `terraform show` output reviewed — no plaintext secrets
- [ ] PR merged to master
