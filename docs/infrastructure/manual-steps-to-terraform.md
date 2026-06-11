# Manual Steps to Terraform

This file records every infrastructure action that could not be expressed as
`terraform apply` at the time it was taken. For each entry: what was done, why
it was manual, its Terraform equivalent, and how to roll it back.

Reviewed by: Peter (per ADR-020 hard constraint — all exceptions require a review entry here).

---

## Entry 001 — Cloudflare API token creation (ADR-026, issue #111)

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

## Entry 002 — Secret shell created via gcloud, then imported (ADR-026, issue #111)

**Date**: 2026-06-11 (executed)
**Actor**: Claude (gcloud, founder-supervised) + Founder (secret version)
**ADR**: ADR-021 / ADR-026

### What was done (forward change)

`gcloud secrets create prod-redline-cloudflare-api-token --replication-policy automatic`
was run before the Terraform resource (`google_secret_manager_secret.cloudflare_api_token`
in `secrets.tf`) was applied, so the founder could store the token value (Entry 001)
without waiting on the Phase 1 apply. The founder added version 1 manually.

### Why manual

Sequencing: the token needed safe storage the moment it was created; the Terraform
apply was blocked at that time on the Firebase ToS exception (Entry 003).

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

## Entry 003 — Firebase ToS acceptance + addFirebase via console (ADR-026, issue #111)

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
