# Manual Steps to Terraform

This file records every infrastructure action that could not be expressed as
`terraform apply` at the time it was taken. For each entry: what was done, why
it was manual, its Terraform equivalent, and how to roll it back.

Reviewed by: Peter (per ADR-020 hard constraint — all exceptions require a review entry here).

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

## Entry 002 — Cloudflare API token creation (ADR-026, issue #111)

**Date**: 2026-06-11 (executed — token created by founder, stored in Secret Manager version 1)
**Actor**: Founder (Harel Lustiger)
**ADR**: ADR-026 D3

### What was done (forward change)

A scoped Cloudflare API token was created in the Cloudflare dashboard with:

- Permission: Zone / DNS / Edit — limited to zone `redmarklogic.com`
- Permission: Zone / Zone / Read — limited to zone `redmarklogic.com`

The token value was stored in Secret Manager as:
`prod-redline-cloudflare-api-token` (project: `redmarklogic-prod`)

### Why manual

Cloudflare API tokens cannot self-provision. The Cloudflare Terraform provider
requires an existing API token to authenticate before it can manage any resources —
creating the first token is an inherent bootstrap exception. There is no Cloudflare
CLI capable of token creation.

This is the same class of exception as the GCP project and Terraform state bucket
created by `bootstrap.sh` — a one-time bootstrap action that unlocks all subsequent
automation.

### Terraform equivalent

There is no `cloudflare_api_token` resource in the Cloudflare Terraform provider.
This step has no Terraform equivalent and remains a permanent documented manual
exception.

The downstream resources that the token enables (DNS records in `cloudflare_dns.tf`)
are fully managed by Terraform.

### Rollback

To revoke the token (e.g. if compromised):

1. Log into the Cloudflare dashboard → My Profile → API Tokens
2. Find the token named for this project and click "Roll" or "Delete"
3. If rolling: update the Secret Manager secret with the new value:

   ```powershell
   $NEW_TOKEN = "<new-token>"
   echo -n $NEW_TOKEN | gcloud secrets versions add prod-redline-cloudflare-api-token --project=redmarklogic-prod --data-file=-
   ```

4. If deleting: remove the Secret Manager secret (only if decommissioning the feature):

   ```powershell
   gcloud secrets delete prod-redline-cloudflare-api-token --project=redmarklogic-prod
   ```

Any DNS records managed by Terraform (cloudflare_dns.tf) remain in place after
token rotation — Terraform simply uses the new token on the next apply.

---

## Entry 003 — Secret shell created via gcloud, then imported (ADR-026, issue #111)

**Date**: 2026-06-11 (executed)
**Actor**: Claude (gcloud, founder-supervised) + Founder (secret version)
**ADR**: ADR-021 / ADR-026

### What was done (forward change)

`gcloud secrets create prod-redline-cloudflare-api-token --replication-policy automatic`
was run before the Terraform resource (`google_secret_manager_secret.cloudflare_api_token`
in `secrets.tf`) was applied, so the founder could store the token value (Entry 002)
without waiting on the Phase 1 apply. The founder added version 1 manually.

### Why manual

Sequencing: the token needed safe storage the moment it was created; the Terraform
apply was blocked at that time on the Firebase ToS exception (Entry 004).

### Terraform equivalent / reconciliation

Reconciled the same day — no drift remains:

```powershell
terraform import google_secret_manager_secret.cloudflare_api_token projects/redmarklogic-prod/secrets/prod-redline-cloudflare-api-token
```

Secret versions stay out-of-band by design (ADR-023 pattern — Terraform manages the
shell, never the value).

### Rollback

`terraform destroy -target=google_secret_manager_secret.cloudflare_api_token`
(destroys shell + versions) — only when decommissioning the feature.

---

## Entry 004 — Firebase ToS acceptance + addFirebase via console (ADR-026, issue #111)

**Date**: 2026-06-11 (executed)
**Actor**: Founder (Harel Lustiger)
**ADR**: ADR-026

### What was done (forward change)

1. Accepted the Firebase Terms of Service for the `harel@redmarklogic.com` account
   in the Firebase console (first-ever Firebase use on this account).
2. Completed the console "Add Firebase to a Google Cloud project" wizard against
   `redmarklogic-prod` (Blaze plan inherited, Google Analytics off).

### Why manual

Per official Firebase documentation: "Accepting the Firebase Terms is not possible
using the Firebase CLI, REST API, or Terraform. It can only be done using the
Firebase console." Until accepted, every `addFirebase` call — including Terraform's
`google_firebase_project` — returns `403 PERMISSION_DENIED` even for a project
Owner. Diagnostic signature: `availableProjects` lists the project (reads pass)
while the `addFirebase` write 403s. An accept-then-cancel attempt did NOT register
acceptance; completing the wizard did.

### Terraform equivalent / reconciliation

Reconciled the same day — no drift remains:

```powershell
terraform import google_firebase_project.default redmarklogic-prod
```

All downstream Firebase resources (site, custom domain, version, release) were
created by Terraform normally after the import.

### Rollback

Firebase cannot be removed from a GCP project via Terraform (the provider
deliberately does not implement delete for `google_firebase_project`). Disabling
requires Google support or project deletion — out of scope; acceptance is
account-level and permanent.

---

## Entry 005 — Firebase API front-door teardown + sanctioned DNS deletion (ADR-027, issue #147)

**Date**: 2026-06-12 (HCL authored; `terraform apply` gated on founder review of the plan diff)
**Actor**: Brent (DevOps), under founder review of the plan diff
**ADR**: ADR-027 D2/D3 (supersedes ADR-026)

### What was done (forward change)

The Firebase Hosting front door for `api.redmarklogic.com` was torn down because
Firebase Hosting caps every request at a hard 60-second ceiling, while the product's
core synchronous calls take three minutes or more — every real call through the
branded address was a guaranteed failure (ADR-027). The POC API address is now the
raw Cloud Run `*.run.app` URL (ADR-027 D1).

Five Terraform resources destroyed in reverse-dependency order (single change set):

1. `google_firebase_hosting_release.api`
2. `google_firebase_hosting_version.api`
3. `google_firebase_hosting_custom_domain.api` (`api.redmarklogic.com` + its TLS cert)
4. `google_firebase_hosting_site.api` (`redmarklogic-api`)
5. `cloudflare_dns_record.firebase_cname` — the `api CNAME redmarklogic-api.web.app`
   record (id `6b051d1e36a71373819c95a89d1db64d`), deleted **via Terraform destroy
   only**, never the Cloudflare dashboard (ADR-020).

Accompanying HCL/config cleanup in the same change set: removed the four `firebase_*`
output blocks, the `firebase_cname_target` variable and its `terraform.tfvars` value,
the `cloudflare_dns_record.firebase_cname` block, and the file
`deploy/firebase/firebase.json` (plus the now-empty `deploy/firebase/` directory). The
root `.env.example` branded-URL block was replaced with an `API_BASE_URL` (run.app)
entry.

### Why this is recorded here (not a manual exception)

This change is fully Terraform-applied — it is NOT a manual/out-of-band action. It is
recorded here because the CNAME deletion is **the single sanctioned exception to the
additive-only DNS discipline** (ADR-026 D3 / ADR-020): the founder's live email
(MX/SPF) runs on the same `redmarklogic.com` zone, so the deletion is guarded by a
mandatory pre-change zone snapshot diffed against a post-change export, and gated on
founder review of the `terraform plan` diff (must show **exactly 5 destroys, 0 other
changes** — any deviation is a stop-the-line event).

### What stays (ADR-027 D3 — must NOT be destroyed)

- `google_firebase_project.default` — Firebase project enablement is irreversible
  (provider implements no delete; ToS acceptance is account-level/permanent), zero
  cost, and reused by the Sprint-3 website. Retained in HCL and state.
- `cloudflare` provider + `data.cloudflare_zone.redmarklogic` read-only data source.
- `google-beta` / `cloudflare` provider pins in `versions.tf`.
- Cloudflare API token secret `prod-redline-cloudflare-api-token` (Entry 002/003).

### Rollback (re-create the front door)

Recreation is possible at any time — nothing destroyed here is unrecoverable:

1. `git revert` the teardown commit (or check out the pre-teardown HCL), restoring the
   four hosting resource blocks, the `firebase_cname` record, the `firebase_cname_target`
   variable + tfvars value, the outputs, and `deploy/firebase/firebase.json`.
2. Inject the Cloudflare token and run the two-step DNS converge documented in
   `domain-dns-runbook.md`:
   - `terraform apply` (creates the site, custom domain with
     `wait_dns_verification = false`, version, release, and the `api` CNAME),
   - then `terraform apply`/`refresh` a second time so Firebase verifies ownership and
     progresses the certificate to `CERT_ACTIVE` / `HOST_ACTIVE`.
3. **Certificate re-issuance can take up to 24 h** (within the 48 h success-criteria
   budget, SC-008).

**Risk of rollback:** re-creating the front door restores the 60-second request
ceiling — the exact guaranteed-failure path ADR-027 removed. Only roll back if ADR-027
is itself reversed by a successor ADR.

---

## Bootstrap exceptions (pre-existing)

The following two resources were created by `deploy/infra/bootstrap/bootstrap.sh`
before Terraform state existed. They are intentionally excluded from Terraform state
to avoid the chicken-and-egg problem:

1. **GCP project** `redmarklogic-prod` — managed as a `data` source in `main.tf`.
2. **Terraform state bucket** `redmarklogic-tf-state` — read by `backend.tf`.

These are not drift — they are documented bootstrap exceptions per ADR-020.
