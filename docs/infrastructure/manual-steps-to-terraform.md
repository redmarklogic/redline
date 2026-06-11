# Manual Steps to Terraform Log

This file records every infrastructure change applied outside `terraform apply`,
including: out-of-band `gcloud` commands, bootstrap exceptions, and any resource
that exists but is not (yet) managed in `deploy/infra/terraform/`.

Each entry must include:
- What was done and why
- The Terraform equivalent (HCL or import command)
- A rollback procedure

Reviewed by: Peter (required before audit evidence is submitted)

---

## Entry 001 — Grant `roles/orgpolicy.policyAdmin` to founder account (2026-06-11)

### Context

Feature #110 required granting `allUsers` the `roles/run.invoker` role on the
`staging-redline-api` Cloud Run service. The GCP organisation enforces the
`constraints/iam.allowedPolicyMemberDomains` policy, which blocks `allUsers` by
default. A project-level `restore_policy` override was written in Terraform
(`deploy/infra/terraform/org_policy.tf`) to lift this restriction for
`redmarklogic-prod` only.

Applying that Terraform resource requires the `orgpolicy.setPolicy` permission,
which is NOT included in `roles/resourcemanager.organizationAdmin`. The permission
lives exclusively in `roles/orgpolicy.policyAdmin`.

### What was done

`roles/orgpolicy.policyAdmin` was granted to `user:harel@redmarklogic.com` at
the **organisation level** (`363330153915`) via `gcloud`:

```bash
gcloud organizations add-iam-policy-binding 363330153915 \
  --member="user:harel@redmarklogic.com" \
  --role="roles/orgpolicy.policyAdmin"
```

Note: this role cannot be granted at the project level
(`roles/orgpolicy.policyAdmin` is not supported as a project-level binding in GCP).
Org-level grant is therefore the minimum viable scope.

### Why this is not in Terraform

The `google_organization_iam_member` resource can manage org-level IAM, but adding
it to Terraform here would create a circular dependency: Terraform needs the
permission to apply org policy resources, and the permission grant itself would be
inside Terraform. This is a bootstrap-level concern analogous to the project and
state-bucket exceptions already documented.

The `deploy/infra/bootstrap/bootstrap.sh` script is the appropriate location for
bootstrap IAM grants. The next pass should add this grant there.

### Terraform equivalent (for bootstrap.sh or future IaC)

```hcl
resource "google_organization_iam_member" "orgpolicy_admin" {
  org_id = var.org_id
  role   = "roles/orgpolicy.policyAdmin"
  member = "user:harel@redmarklogic.com"
}
```

Or as a `gcloud` command in `bootstrap.sh`:

```bash
gcloud organizations add-iam-policy-binding "${ORG_ID}" \
  --member="user:${FOUNDER_EMAIL}" \
  --role="roles/orgpolicy.policyAdmin"
```

### Rollback

To remove the grant if needed (e.g., if a dedicated Terraform SA is used instead):

```bash
gcloud organizations remove-iam-policy-binding 363330153915 \
  --member="user:harel@redmarklogic.com" \
  --role="roles/orgpolicy.policyAdmin"
```

**Risk of rollback:** removing this grant means `terraform apply` will fail on any
future run that touches `google_project_organization_policy` resources. Only remove
if a replacement credential (e.g., a Terraform service account with this role) is
already in place.

---

## Bootstrap exceptions (pre-existing)

The following two resources were created by `deploy/infra/bootstrap/bootstrap.sh`
before Terraform state existed. They are intentionally excluded from Terraform state
to avoid the chicken-and-egg problem:

1. **GCP project** `redmarklogic-prod` — managed as a `data` source in `main.tf`.
2. **Terraform state bucket** `redmarklogic-tf-state` — read by `backend.tf`.

These are not drift — they are documented bootstrap exceptions per ADR-020.
