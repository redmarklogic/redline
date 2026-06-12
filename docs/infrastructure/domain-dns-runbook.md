# Domain DNS Runbook: api.redmarklogic.com

> ## ⚠️ SUPERSEDED — front door torn down (ADR-027, issue #147, 2026-06-12)
>
> The Firebase Hosting front door described below was **torn down**. Firebase Hosting
> caps every request at a hard 60-second ceiling, but the product's core synchronous
> calls take three minutes or more — so every real call through `api.redmarklogic.com`
> was a guaranteed failure. **The POC API address is now the raw Cloud Run `*.run.app`
> service URL** (ADR-027 D1); `api.redmarklogic.com` no longer resolves.
>
> **Current state:** the five front-door resources (hosting site, custom domain,
> rewrite version + release, and the `api` CNAME) are destroyed. The Firebase *project*
> enablement, the Cloudflare provider + zone data source, the provider pins, and the
> Cloudflare API token secret are **retained** for the Sprint-3 website (ADR-027 D3).
>
> **This document is retained as the authoritative rollback reference.** The "Teardown"
> section near the end, read in reverse, plus Entry 005 of
> `manual-steps-to-terraform.md`, is the procedure to re-create the front door if a
> successor ADR ever reverses ADR-027 (certificate re-issuance ≤ 24 h).
>
> Everything below this banner describes the **former** front door (ADR-026, now
> superseded). Do not treat it as the live architecture.

---

**Feature**: Issue #111 — Connect api.redmarklogic.com to Cloud Run via Firebase Hosting
**ADR**: ADR-026 (SUPERSEDED by ADR-027 — front door torn down per issue #147)
**Last updated**: 2026-06-12 (superseded banner added; front door removed)

This runbook documents every step to create, verify, and (if needed) tear down the
connection between `api.redmarklogic.com` and the Redline Cloud Run backend.
The setup is fully reproducible from these instructions (SC-005).

---

## Architecture summary

```
API consumer
    | https://api.redmarklogic.com/...
    v
Cloudflare DNS (grey cloud — DNS lookup only, no proxying)
    | A records -> Firebase Hosting edge
    v
Firebase Hosting site "redmarklogic-api"  (CDN edge, auto-renewing TLS, 60 s ceiling)
    | rewrite { source: "**" } -> Cloud Run
    v
Cloud Run service prod-redline-api (australia-southeast1, ingress=all)

Bypass path (accepted, documented): https://prod-redline-api-*.run.app
```

**Accepted constraints (recorded per ADR-026):**
- Requests longer than 60 seconds return HTTP 504 at the branded address.
- Cookies other than `__session` are stripped by the Firebase proxy layer.
- WebSockets are not supported through this hostname.
- The direct `*.run.app` URL remains publicly accessible (ADR-022 trust boundary).

---

## Manual exceptions

Three steps in this setup cannot be automated in Terraform:

| Step | Why manual | Location |
|------|-----------|---------|
| **T002** Cloudflare API token creation | Tokens cannot self-provision; Cloudflare dashboard is the only path | See "Phase 0, Step 1" below |
| Firebase Terms of Service acceptance | Per official Firebase docs: "Accepting the Firebase Terms is not possible using the Firebase CLI, REST API, or Terraform. It can only be done using the Firebase console." One-time, account-level. Symptom before acceptance: `addFirebase` returns 403 PERMISSION_DENIED even for project Owner. | See "Phase 1, Step 3a" below |
| Console emergency fallback | Last-resort only if Terraform is unavailable | Documented in "Emergency fallback" section below |

---

## Phase 0: Governance + evidence baseline

### Step 1 — [MANUAL — FOUNDER] Create the Cloudflare API token (T002)

**This is a parallelizable founder step. Brent cannot execute it.**

1. Log in to the Cloudflare dashboard at https://dash.cloudflare.com
2. Navigate to: My Profile → API Tokens → Create Token
3. Use "Create Custom Token"
4. Set the following permissions — **nothing more**:
   - **Zone / DNS / Edit** — for zone `redmarklogic.com` only
   - **Zone / Zone / Read** — for zone `redmarklogic.com` only
5. Under "Zone Resources", select "Specific zone" → `redmarklogic.com`
6. Set an expiry if desired (recommended: 1 year)
7. Click "Continue to Summary" → "Create Token"
8. **Copy the token immediately** — it is shown only once.
9. Store the token in Secret Manager:

```powershell
# Store token in Secret Manager (ADR-021 naming: <env>-redline-<credential>)
# Run this from a machine with gcloud authenticated to redmarklogic-prod

$TOKEN = "<paste-token-here>"
$PROJECT = "redmarklogic-prod"
$SECRET_ID = "prod-redline-cloudflare-api-token"  # pragma: allowlist secret -- secret ID name, not a secret value

# Create the secret shell (Terraform may have already done this — if so, skip)
gcloud secrets create $SECRET_ID --project=$PROJECT --replication-policy=automatic

# Store the value (version managed out-of-band per ADR-023 / secrets.tf pattern)
echo -n $TOKEN | gcloud secrets versions add $SECRET_ID --project=$PROJECT --data-file=-
```

10. **Record the zone ID** (needed for the snapshot step):

```powershell
# Retrieve zone ID using the new token
$env:CF_API_TOKEN = "<your-token>"
$response = curl.exe -s "https://api.cloudflare.com/client/v4/zones?name=redmarklogic.com" `
  -H "Authorization: Bearer $env:CF_API_TOKEN" | ConvertFrom-Json
$env:CF_ZONE_ID = $response.result[0].id
Write-Host "Zone ID: $env:CF_ZONE_ID"
```

Store `CF_ZONE_ID` in your local environment for subsequent steps in this session.

---

### Step 2 — Capture the pre-change zone snapshot (T003)

**Execute BEFORE any DNS record is created or modified. This is the FR-004 / SC-002 evidence baseline.**

First, confirm no `api` record already exists (spec edge case — if one is found, stop and resolve with the founder before proceeding):

```powershell
curl.exe -s "https://api.cloudflare.com/client/v4/zones/$env:CF_ZONE_ID/dns_records?name=api.redmarklogic.com" `
  -H "Authorization: Bearer $env:CF_API_TOKEN" | ConvertFrom-Json | Select-Object -ExpandProperty result
# Expected: empty array []. If any record is returned, STOP and do not proceed.
```

Capture the full zone export in BIND format:

```powershell
curl.exe -s "https://api.cloudflare.com/client/v4/zones/$env:CF_ZONE_ID/dns_records/export" `
  -H "Authorization: Bearer $env:CF_API_TOKEN" `
  -o "docs/infrastructure/zone-snapshot-pre-2026-06-11.txt"
```

Verify the snapshot contains MX records (confirms the export is complete and email is intact):

```powershell
Select-String -Path "docs/infrastructure/zone-snapshot-pre-2026-06-11.txt" -Pattern "MX"
# Must return at least one line. If empty, the export failed — do not proceed.
```

Commit the snapshot file immediately:

```powershell
rtk git add docs/infrastructure/zone-snapshot-pre-2026-06-11.txt
rtk git commit -m "chore(infra): capture pre-change Cloudflare zone snapshot (T003, SC-002 evidence)"
```

---

### Acceptance Gate (T004)

Before proceeding to Phase 1:

- [ ] ADR-026 merged (PR review is the gate)
- [ ] Zone snapshot committed with MX records present
- [ ] `curl` with stored token returns `success: true`
- [ ] No pre-existing record found on `api.redmarklogic.com`

---

## Phase 1: Terraform — Firebase + Cloudflare DNS

### Step 3 — Verify provider schema and run terraform init (T005)

Provider schema verdicts (verified 2026-06-11):
- `google_firebase_hosting_version` rewrite `run` block: **confirmed** — uses `service_id` and `region` (snake_case).
- Cloudflare v5 resource name: **`cloudflare_dns_record`** (not the v4 name `cloudflare_record`).
- Provider pin chosen: `cloudflare ~> 5.19`, `google-beta ~> 6.0`.

```powershell
cd deploy/infra/terraform
terraform init
# Expected: "Terraform has been successfully initialized" with cloudflare and google-beta providers downloaded.
```

---

### Step 3a — [MANUAL — FOUNDER, ONE-TIME] Accept the Firebase Terms of Service

**Skip if any Firebase project already exists for this Google account.**

Google requires a human to accept the Firebase ToS; there is no API, CLI, or
Terraform path (see "Manual exceptions" above). Until accepted, every
`addFirebase` call — including Terraform's — returns `403 PERMISSION_DENIED`
even for a project Owner. `availableProjects` still lists the project (reads
are not gated), which distinguishes this from a real IAM problem.

1. Open <https://console.firebase.google.com> signed in as the account that runs Terraform
2. Click "Create a project" (or "Add project") — on the first screen, tick the
   "I accept the Firebase terms" checkbox and click Continue
3. **Cancel the wizard** — do not finish creating anything. Acceptance is
   recorded at account level the moment you continue past the checkbox.
   (If you do complete the wizard against `redmarklogic-prod`, no harm:
   reconcile with `terraform import google_firebase_project.default redmarklogic-prod`.)
4. Re-run the Step 4 apply below.

### Step 4 — First apply: Firebase resources only (T006 / T009 Step 1)

The Cloudflare variables (`firebase_ownership_txt_value`, `firebase_a_record_ips`) are left
empty/commented for this apply. The validation rules on those variables will block a
full apply, so we use `-target` to apply only Firebase resources:

```powershell
# Set the Cloudflare API token so the provider can authenticate (even if no CF resources are applied)
$env:CLOUDFLARE_API_TOKEN = (gcloud secrets versions access latest --secret=prod-redline-cloudflare-api-token --project=redmarklogic-prod)

# Review: should show only firebase_hosting.tf resources + API enablements
terraform plan `
  -target=google_firebase_project.default `
  -target=google_firebase_hosting_site.api `
  -target=google_firebase_hosting_custom_domain.api `
  -target=google_firebase_hosting_version.api `
  -target=google_firebase_hosting_release.api `
  -target=google_project_service.apis `
  -var="image_tag=sha256:placeholder"

# Founder reviews plan output before apply.
terraform apply `
  -target=google_firebase_project.default `
  -target=google_firebase_hosting_site.api `
  -target=google_firebase_hosting_custom_domain.api `
  -target=google_firebase_hosting_version.api `
  -target=google_firebase_hosting_release.api `
  -target=google_project_service.apis `
  -var="image_tag=sha256:placeholder"
```

---

### Step 5 — Read the authoritative DNS record values from Terraform output (T009 Step 2)

```powershell
terraform output firebase_custom_domain_required_dns_updates
```

This output is the **authoritative source** for the DNS values Firebase needs.

> **As executed 2026-06-11:** Firebase's current subdomain flow returned a SINGLE
> CNAME requirement — `api.redmarklogic.com CNAME redmarklogic-api.web.app`
> (required_action ADD) — not the legacy TXT-ownership + A-record pair the original
> plan assumed. Ownership verification and certificate issuance ride on that one
> record. The cert block additionally offers an `_acme-challenge` TXT (dns01) as an
> alternative to the automatic http01 check; do NOT pin it in Terraform — the value
> rotates per ACME order and would break renewals.

Record the CNAME rdata into `terraform.tfvars`:

```hcl
# Set from terraform output above:
firebase_cname_target = "redmarklogic-api.web.app"
```

---

### Step 6 — Second apply: Cloudflare DNS record created (T008 / T009 Step 3)

```powershell
# Targeted plan/apply — the CNAME record only.
# As executed 2026-06-11: the FULL plan showed unrelated drift from other specs
# (secret replacements, IAM member + org-policy destroys, Cloud Run image changes
# from the placeholder image_tag). Per T009's additive-only review rule, a full
# apply is NOT safe — target this feature's resources only.
terraform plan  -target=cloudflare_dns_record.firebase_cname -var="image_tag=sha256:placeholder"
# Review gate: plan must be exactly "1 to add, 0 to change, 0 to destroy".
terraform apply -target=cloudflare_dns_record.firebase_cname -var="image_tag=sha256:placeholder"
# Note: Cloudflare limits record comments to 100 characters (API error 9313 beyond).
```

---

### Step 7 — Verify DNS propagation and cert progression (T010)

```powershell
# Verify the CNAME (authoritative NS first, then public resolver)
Resolve-DnsName api.redmarklogic.com -Type CNAME -Server eve.ns.cloudflare.com
Resolve-DnsName api.redmarklogic.com -Server 1.1.1.1
# Expected: CNAME -> redmarklogic-api.web.app, chaining to Firebase edge
# (199.36.158.100 / 2620:0:890::100 via the web.app record)

# Check cert + host state via Terraform (output is an object: { cert, host_state })
# Note: the provider exposes `cert` (with a `state` field) and `host_state`,
# not a flat `cert_state` attribute.
terraform output firebase_custom_domain_cert_state
# Target: cert.state = CERT_ACTIVE / host_state = HOST_ACTIVE (allow up to 24 h; SC-001 budgets 48 h)
# Intermediate states: CERT_PENDING, DNS_PENDING, HOST_UNHOSTED — normal while propagating

# Verify zone diff is additive-only (FR-004 / SC-002 evidence)
curl.exe -s "https://api.cloudflare.com/client/v4/zones/$env:CF_ZONE_ID/dns_records/export" `
  -H "Authorization: Bearer $env:CF_API_TOKEN" `
  -o "zone-post-phase1.txt"
rtk git diff --no-index docs/infrastructure/zone-snapshot-pre-2026-06-11.txt zone-post-phase1.txt
# Must show ONLY additions on lines starting with "api". MX lines must be byte-identical.
```

---

### Acceptance Gate (T010)

Before proceeding to Phase 2:

- [ ] `Resolve-DnsName api.redmarklogic.com -Type TXT` returns the ownership value
- [ ] Zone diff shows only `api.*` additions; MX lines byte-identical
- [ ] `terraform output firebase_custom_domain_cert_state` is progressing toward `CERT_ACTIVE`

---

## Phase 2: Cutover + end-to-end verification (BLOCKED BY #110)

**This phase cannot start until the Cloud Run service `prod-redline-api` is deployed (issue #110).**

### Step 8 — Preflight (T011)

> **Preflight findings (2026-06-11, recorded during Phase 1):**
>
> - `prod-redline-api` and `staging-redline-api` are deployed and Ready —
>   the #110 hard dependency is satisfied.
> - **BLOCKER**: `GET https://prod-redline-api-bfyi7ev63a-ts.a.run.app/` returns
>   the Google-frontend `403 Forbidden` — prod does NOT allow unauthenticated
>   invoke (no `allUsers` run.invoker binding; the staging public-invoker binding
>   is drift pending destroy). Firebase Hosting rewrites are unauthenticated, so
>   the branded URL will 403 even at CERT_ACTIVE until the founder decides:
>   (a) grant `allUsers` roles/run.invoker on prod (spec's original assumption,
>   ADR-022 trust boundary), or (b) keep prod private and abandon the public
>   branded endpoint. Decision + IAM change belongs to #110 scope — do not
>   apply IAM from this feature.
> - Health path: `/health` exists on the app (403 at IAM layer, not 404);
>   `/healthz` returns 404. Use `/health` in T013 once invoke is permitted.

```powershell
# Confirm deployed service name
gcloud run services list --region australia-southeast1 --project redmarklogic-prod

# Confirm ingress = all (required for Firebase Hosting to reach the service)
gcloud run services describe prod-redline-api --region australia-southeast1 --project redmarklogic-prod --format="value(spec.traffic)"

# Confirm health path (/health vs /healthz — research open item 2)
# Update firebase_hosting.tf startup_probe path if different from /health
```

If the service name differs from `prod-redline-api`, update `cloudflare_dns.tf` and `firebase.json` before re-applying.

### Step 9 — Wait for CERT_ACTIVE (T012)

```powershell
# Poll cert state (allow up to 24 h) — output object: { cert, host_state }
terraform output firebase_custom_domain_cert_state
# When cert.state = CERT_ACTIVE, proceed to end-to-end verification.
```

### Step 10 — End-to-end verification (T013)

Record all outputs in this runbook as evidence (SC-001..SC-004).

```powershell
# Health check via branded address
curl.exe -sSi https://api.redmarklogic.com/health
# Expected: HTTP 200 from the Redline backend

# TLS certificate check (Google Trust Services, correct hostname)
openssl s_client -connect api.redmarklogic.com:443 -servername api.redmarklogic.com 2>&1 | Select-String "subject="
# Expected: CN=api.redmarklogic.com

# HTTP -> HTTPS redirect (FR-003)
curl.exe -sSi http://api.redmarklogic.com/health
# Expected: 301 redirect to https://api.redmarklogic.com/health

# Negative: request > 60 seconds returns 504 (accepted constraint, ADR-026 D1)
# [Manual test with a deliberately slow endpoint]

# Bypass path still works (expected — run.app URL must continue to answer)
# Replace with actual service URL from: gcloud run services describe prod-redline-api ...
curl.exe -sSi https://prod-redline-api-<hash>-ts.a.run.app/health
```

Email round-trip (SC-003): send and receive a test email to/from `harel@redmarklogic.com`
and confirm delivery in both directions. Record the timestamp of the test.

Re-deploy smoke test (SC-004):
```powershell
# Trigger a re-deploy of the service image; confirm branded URL still serves without any DNS touch
gcloud run deploy prod-redline-api --region australia-southeast1 --project redmarklogic-prod --image <same-image>
curl.exe -sSi https://api.redmarklogic.com/health
# Expected: still returns 200
```

Record observed headers (research open item 4):
```powershell
curl.exe -sSi https://api.redmarklogic.com/health | Select-String "X-Forwarded|Host|X-Original"
# Record actuals here: ___________________________________
```

---

## Rollback procedures

### Rollback: Cloudflare DNS records only

```powershell
# Remove only the Cloudflare record (leaves Firebase resources in place)
terraform destroy `
  -target=cloudflare_dns_record.firebase_cname `
  -var="image_tag=sha256:placeholder"
# Verify: api.redmarklogic.com no longer resolves; MX records unaffected
```

### Rollback: Full Firebase Hosting teardown

```powershell
# Destroy all Firebase + Cloudflare resources from this feature
terraform destroy `
  -target=google_firebase_hosting_release.api `
  -target=google_firebase_hosting_version.api `
  -target=google_firebase_hosting_custom_domain.api `
  -target=google_firebase_hosting_site.api `
  -target=cloudflare_dns_record.firebase_cname `
  -var="image_tag=sha256:placeholder"
# Note: google_firebase_project.default is intentionally excluded — removing Firebase
# from the project is a more destructive action and requires founder approval.
```

### Rollback: hosting release only (revert to previous version)

If only the rewrite config needs reverting (not the domain attachment):

```powershell
# Via Firebase CLI standalone binary (Constitution XVII: no npm install)
# Download: https://firebase.google.com/docs/cli#standalone-binary
firebase hosting:rollback --site redmarklogic-api
```

### Emergency fallback (dashboard — last resort only, violates ADR-020)

If Terraform is unavailable and DNS is broken:
1. Log into Cloudflare dashboard → redmarklogic.com → DNS Records
2. Delete the TXT and A records added for `api.redmarklogic.com`
3. Document the action in `docs/infrastructure/manual-steps-to-terraform.md` immediately

---

## Secret Manager reference

| Secret ID | What it stores | ADR-021 naming |
|-----------|---------------|----------------|
| `prod-redline-cloudflare-api-token` | Cloudflare API token (Zone:DNS:Edit + Zone:Zone:Read on redmarklogic.com) | `<env>-redline-<credential>` |

The token value is never stored in HCL, `terraform.tfvars`, or any committed file.
At plan/apply time, inject via:

```powershell
$env:CLOUDFLARE_API_TOKEN = (gcloud secrets versions access latest --secret=prod-redline-cloudflare-api-token --project=redmarklogic-prod)
```

---

## Accepted constraints reference (for API consumers)

See also: `specs/111-domain-dns-cloud-run/contracts/api-hostname.md`

| Constraint | Value |
|------------|-------|
| Request duration ceiling | 60 seconds (HTTP 504 beyond) |
| Cookies | Only `__session` passes through the proxy |
| WebSockets | Not supported at this hostname |
| Max body (effective) | ~32 MB |
| run.app bypass | `https://prod-redline-api-*.run.app` — same auth, address unstable if service is recreated |
| Data transfer billing | $0 to 10 GB/mo; $0.15/GB beyond (no hard stop) |

---

## Evidence log (populate during execution)

| Check | Evidence | Date |
|-------|---------|------|
| Pre-change zone snapshot committed | `docs/infrastructure/zone-snapshot-pre-2026-06-11.txt` (MX present; no api record of any type) | 2026-06-11 |
| No pre-existing api record found | Pre-snapshot contains no `api.*` line; Firebase `discovered` list empty | 2026-06-11 |
| ADR-026 merged | PR pending on `feature/111-domain-dns-cloud-run` | |
| CNAME resolves (was: TXT — flow changed) | `Resolve-DnsName api.redmarklogic.com` → CNAME `redmarklogic-api.web.app` on eve.ns.cloudflare.com AND 1.1.1.1 | 2026-06-11 |
| Zone diff additive-only | `git diff` pre vs `zone-post-phase1-2026-06-11.txt`: single api CNAME added, MX byte-identical, SOA serial bump only | 2026-06-11 |
| Cert state CERT_ACTIVE | CERT_VALIDATING (TEMPORARY) as of 2026-06-11 10:04Z — http01 auto-completes; recheck within 24 h | pending |
| Health 200 via branded URL (SC-001) | `curl` output | |
| TLS cert correct CN | `openssl` output | |
| HTTP→HTTPS redirect (FR-003) | `curl` output | |
| Email round-trip (SC-003) | Timestamp + direction | |
| Re-deploy smoke test (SC-004) | Before/after `curl` output | |
| Negative: >60 s → 504 | Test output | |
| run.app bypass still answers | `curl` output | |
| Observed forwarded headers (open item 4) | `curl -v` output | |
