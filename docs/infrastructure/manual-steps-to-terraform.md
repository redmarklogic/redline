# Manual Steps to Terraform

This file records every infrastructure action that could not be expressed as
`terraform apply` at the time it was taken. For each entry: what was done, why
it was manual, its Terraform equivalent, and how to roll it back.

Reviewed by: Peter (per ADR-020 hard constraint — all exceptions require a review entry here).

---

## Entry 001 — Cloudflare API token creation (ADR-026, issue #111)

**Date**: 2026-06-11 (pending — founder step, not yet executed)
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
