# Implementation Plan: Connect api.redmarklogic.com to Cloud Run Backend via Cloudflare DNS

**Date**: 2026-06-11 | **Spec**: [spec.md](spec.md)
**Status**: Draft

## Summary

Give the Redline backend a stable branded address: `https://api.redmarklogic.com`.
The backend runs (will run — deploy is issue #110) on Google Cloud Run in
australia-southeast1, where Google's free built-in domain attachment is unavailable.
The selected zero-cost route is a Firebase Hosting **rewrite proxy**: Firebase Hosting
(Google's static-hosting CDN, free tier) owns the hostname and forwards every request
to the Cloud Run service `prod-redline-api`. DNS for redmarklogic.com lives at
Cloudflare (registrar + nameservers); two additive records on the `api` subdomain
(ownership TXT + A records), both DNS-only (grey cloud), connect the hostname to
Firebase. Everything expressible in Terraform lands in `deploy/infra/terraform/`
(Constitution XV); no npm toolchain is introduced (Constitution XVII). The accepted
trade-off, recorded by ADR before implementation: requests longer than 60 seconds fail
at the branded address, and the direct `*.run.app` URL stays publicly reachable
(routing, not security).

## Technical Context

**Language**: No application code. Infrastructure feature: Terraform HCL + one JSON
config (`firebase.json`) + documentation. Python 3.14/uv/pytest apply only if a
verification script is added (none planned — verification is CLI commands).
**Project layout**: monorepo (`src/marker`, `src/rl`) — untouched by this feature.
**IaC**: Terraform under `deploy/infra/terraform/` (ADR-020; Constitution XV).
Providers: `google`/`google-beta` (Firebase resources are beta), `cloudflare`.
**CLIs**: `gcloud` (read-only/operational only), Cloudflare API v4 via curl/PowerShell
(no Cloudflare CLI exists — research Decision 3), standalone Firebase CLI binary only
as fallback (Constitution XVII forbids the npm install).
**Key constraint set**: ADR-020 (IaC), ADR-021 (env config), ADR-022 (hosting/trust
boundary), Constitution XV/XVII; version-guard: skipped (no npm deps —
[version-guard-report.md](version-guard-report.md)).

## Design Decisions

| #  | Decision | Choice | Rationale |
| -- | -------- | ------ | --------- |
| D1 | Attachment mechanism | Firebase Hosting rewrite proxy (free) | Founder 2026-06-11: $0 at POC; domain mappings unavailable in region; ALB ~$20-25/mo rejected ([research.md](research.md) Decision 1) |
| D2 | Hostname scope | `api.redmarklogic.com` only | Founder: API only; website (#77) separate; apex/MX untouched |
| D3 | Cloudflare tooling | Terraform `cloudflare` provider + API v4 (scoped token) | No maintained Cloudflare DNS CLI exists; ADR-020 |
| D4 | Proxy mode at Cloudflare | Grey cloud (DNS only), permanently | Orange cloud breaks Firebase verification/cert renewal; Firebase already a CDN |
| D5 | Firebase project | Enable on existing `redmarklogic-prod`; dedicated site `redmarklogic-api` | Rewrites require same project; keeps future website separable |
| D6 | Rewrite config vehicle | Terraform `hosting_version`/`release` if schema confirms; else CI step with standalone Firebase binary | Constitution XV first; XVII forbids npm toolchain |
| D7 | Cloud Run ingress | Stays `all` + unauthenticated invoke | Stricter setting blocks Firebase Hosting; trust boundary unchanged (ADR-022, run.app bypass documented) |
| D8 | Governance | ADR (new or ADR-022 addendum) before any apply | Constitution "ADR before code"; FR-009 Tier-1 gate for new platform service |

## Domain Impact

**Modularity assessment**: N/A — no Python packages touched.
**New packages**: None.
**Bounded context changes**: None.
**Import-linter contract updates**: None.
**Subdomain classification**: Generic (off-the-shelf platform wiring, no custom domain model).
**New domain terms**: None (infrastructure terms only — see Glossary).

## Architecture

Request flow after cutover:

```text
API consumer
    |  https://api.redmarklogic.com/...
    v
Cloudflare DNS (grey cloud - name resolution only, no proxying)
    |  A records -> Firebase Hosting edge
    v
Firebase Hosting site "redmarklogic-api"  (CDN edge, TLS cert, 60 s ceiling)
    |  rewrite { source: "**" } -> Cloud Run
    v
Cloud Run service prod-redline-api (australia-southeast1, ingress=all)

Bypass path (documented, accepted): consumer -> https://prod-redline-api-*.run.app
directly. App-level Bearer check (ADR-022) is the only gate on both paths.
```

DNS records added at Cloudflare (exact values come from the Terraform
`google_firebase_hosting_custom_domain.required_dns_updates` output — authoritative):

| Type | Name | Value | Proxy | Purpose |
|------|------|-------|-------|---------|
| TXT | `api` | per `required_dns_updates` | DNS only | Domain ownership proof |
| A (xN) | `api` | per `required_dns_updates` (classic: 199.36.158.100) | DNS only | Route to Firebase edge |

New Terraform surface (all in `deploy/infra/terraform/`):

- `firebase_hosting.tf` — `google_firebase_project`, `google_firebase_hosting_site`,
  `google_firebase_hosting_custom_domain` (google-beta;
  `wait_dns_verification = false` on first apply), plus `hosting_version`/`release`
  for the rewrite if D6's primary path holds.
- `cloudflare_dns.tf` — `cloudflare` provider + the TXT/A records, `proxied = false`,
  values wired from the custom-domain resource outputs.
- `versions.tf` — add google-beta and cloudflare provider pins.
- Cloudflare API token: created once in the dashboard (documented exception — tokens
  cannot self-provision), stored in Secret Manager, read by Terraform via variable.

## Domain Models

None. No Pydantic/Pandera models; no `src/` changes. (The only "model-adjacent" note:
future cookie-based sessions must use the literal cookie name `__session` — recorded
in the ADR so Kabilan inherits the constraint.)

## MoSCoW

| Category | Items |
| -------- | ----- |
| **Must have** | ADR recorded (D8); pre-change zone snapshot; Firebase project/site/custom-domain + Cloudflare records in Terraform; cert ACTIVE; health 200 via branded URL; zone diff shows additive-only; email round-trip verified; runbook in `docs/infrastructure/` |
| **Should have** | Rewrite config in Terraform rather than CLI fallback (D6 primary); negative checks documented (504 >60 s, run.app bypass); `X-Forwarded-Host` actuals recorded |
| **Could have** | Staging hostname (`api-staging.…`) for `staging-redline-api`; uptime check on the branded URL |
| **Won't have (this time)** | Website/apex/www (#77); paid ALB route; Cloudflare orange-cloud; locking down run.app (impossible on free route); WebSocket support through proxy |

## Phased Delivery

> Infra feature: "TDD approach" sections are replaced by explicit verification
> commands — there are no Python functions to test-first. Acceptance gates keep the
> working-end-to-end requirement.

### Phase 0: Governance + evidence baseline (no service dependency)

**Goal**: ADR accepted; Cloudflare access working; pre-change zone snapshot captured.

**Deliverables**:

1. `docs/adr/adr-0NN-firebase-hosting-api-domain.md` — D1-D8, 60 s ceiling,
   grey-cloud rule, run.app bypass, $0 posture + egress caveat ($0.15/GB past
   10 GB/mo, no hard stop, budget alert is backstop). Constitution sync check
   (`check-adr-constitution-sync` hook) decides whether the constitution needs a
   same-commit update.
2. Cloudflare API token (dashboard, scoped Zone:DNS:Edit + Zone:Zone:Read on
   redmarklogic.com only) -> Secret Manager entry; documented in the runbook.
3. `docs/infrastructure/zone-snapshot-pre-<date>.txt` — BIND export via
   `GET /zones/{zone_id}/dns_records/export`.

**Verification**:

```text
curl -s "https://api.cloudflare.com/client/v4/zones?name=redmarklogic.com" -H "Authorization: Bearer $TOKEN"
  -> success:true, zone id captured
zone snapshot file exists and contains the MX records
ADR merged (PR review counts as the gate)
```

**Acceptance Gate**:

- [ ] ADR accepted and merged; constitution sync hook green
- [ ] Zone snapshot committed; token in Secret Manager (never in repo)

---

### Phase 1: Terraform — Firebase + DNS records (no service dependency)

**Goal**: Firebase enabled on `redmarklogic-prod`, site `redmarklogic-api` exists,
custom domain attached (pending verification), Cloudflare TXT/A records live (grey),
certificate provisioning underway.

**Deliverables**:

1. `deploy/infra/terraform/firebase_hosting.tf` (resources per Architecture)
2. `deploy/infra/terraform/cloudflare_dns.tf`
3. `deploy/infra/terraform/versions.tf` — provider pins (verify
   `cloudflare_dns_record` v5 vs `cloudflare_record` v4 naming at authoring —
   research open item 1)
4. `deploy/firebase/firebase.json` — rewrite `** -> prod-redline-api
   (australia-southeast1)`, `site: redmarklogic-api`, empty `public/` dir
   (committed even if D6 primary path makes it informational)

**Verification**:

```text
terraform plan   -> only additive resources, nothing outside firebase/cloudflare/provider files
terraform apply  -> clean
Resolve-DnsName api.redmarklogic.com -Type TXT  -> ownership value present
re-export zone, diff vs snapshot -> only api.* additions; MX byte-identical
```

**Acceptance Gate**:

- [ ] Apply clean; custom-domain resource progressing toward cert (state readable)
- [ ] Zone diff additive-only — FR-004 evidence captured

---

### Phase 2: Cutover + end-to-end verification (BLOCKED BY #110 — deployed service)

**Goal**: `https://api.redmarklogic.com/<health>` serves the backend with a valid
Google Trust Services certificate.

**Deliverables**:

1. Rewrite release live (Terraform release resource, or documented CI fallback step)
2. Certificate `CERT_ACTIVE` (allow 24 h; SC-001 budget 48 h)
3. Verification evidence block appended to the runbook (commands + outputs)

**Verification**:

```text
curl -sSi https://api.redmarklogic.com/<health-path>   -> backend 200   (confirm /health vs /healthz first — research open item 2)
openssl s_client -connect api.redmarklogic.com:443 -servername api.redmarklogic.com -> GTS cert, correct CN
redeploy service image -> branded URL still serves (FR-007/SC-004)
email round-trip via founder mailbox -> delivered both directions (SC-003)
negative: >60 s request -> 504 (documented); direct run.app URL answers (expected)
```

**Acceptance Gate**:

- [ ] All five checks above pass and are recorded as evidence
- [ ] No pre-existing DNS record modified (final zone diff)

---

### Phase 3: Documentation close-out

**Goal**: Reproducible procedure exists; constraints land where consumers will look.

**Deliverables**:

1. `docs/infrastructure/domain-dns-runbook.md` — full procedure: every CLI/API/
   Terraform step, the two dashboard-only exceptions (token creation; Console
   emergency fallback), rollback notes (`firebase hosting:rollback` / record
   deletion), forwarded-header actuals (research open item 4)
2. API-consumer note (60 s ceiling + branded vs run.app URLs) in the API docs
   location governed by ADR-018 conventions
3. Board/issue updates: #111 closes via merged PR; #110 dependency satisfied

**Verification**:

```text
A reader can map every created resource/record to a documented step (SC-005)
```

**Acceptance Gate**:

- [ ] Runbook merged; spec SC-001..SC-005 each have recorded evidence

## File Inventory

| Phase | New Files | Count |
| ----- | --------- | ----- |
| 0 | `docs/adr/adr-0NN-firebase-hosting-api-domain.md`, `docs/infrastructure/zone-snapshot-pre-<date>.txt` | 2 |
| 1 | `deploy/infra/terraform/firebase_hosting.tf`, `deploy/infra/terraform/cloudflare_dns.tf`, `deploy/firebase/firebase.json` (+ `public/.gitkeep`); `versions.tf` modified | 4 new, 1 modified |
| 2 | (evidence appended to runbook) | 0 |
| 3 | `docs/infrastructure/domain-dns-runbook.md`, consumer note | 2 |

**Total new**: ~8 | **Total deleted**: 0

## Library Best Practices

### terraform-provider-google-beta (Firebase resources)

- **Import path**: provider `google-beta`; resources `google_firebase_project`,
  `google_firebase_hosting_site`, `google_firebase_hosting_custom_domain`,
  `google_firebase_hosting_version`/`_release`
- **API gotchas**: custom-domain resource needs `provider = google-beta` explicitly;
  set `wait_dns_verification = false` on first apply (records don't exist yet);
  `required_dns_updates` output is the authoritative DNS record list — do not
  hard-code values from the docs page
- **Confirmed pattern**: two-step converge — apply (get records) -> create Cloudflare
  records -> re-apply/refresh until cert ACTIVE

### terraform-provider-cloudflare

- **Import path**: `cloudflare/cloudflare`; record resource is `cloudflare_dns_record`
  in v5 (was `cloudflare_record` in v4) — pin and verify at authoring
- **API gotchas**: `proxied = false` must be explicit (grey cloud is load-bearing
  here); token via provider config from environment, never in HCL
- **Confirmed pattern**: zone ID via data source `cloudflare_zone` filtered by name

### firebase.json (rewrite)

- **Confirmed pattern**: `rewrites: [{source: "**", run: {serviceId, region}}]`;
  `region` mandatory in practice (defaults to us-central1); `public/` must exist and
  stay empty — any static file shadows the rewrite for its path

## Risk Register

| Risk | Mitigation |
| ---- | ---------- |
| Cert provisioning slow/stuck (>24 h) | Phases 0-1 start early (no service dependency); SC-001 budgets 48 h; status observable via Terraform state; Firebase support escalation documented in runbook |
| Someone flips the record to orange cloud later | ADR + runbook state grey-is-load-bearing; Terraform `proxied=false` reverts drift on next apply |
| Runaway egress bill ($0.15/GB past 10 GB/mo, no hard stop) | Existing project budget alert; noted in ADR as the denial-of-wallet surface; revisit if traffic grows |
| run.app bypass misread as a security hole | ADR + runbook state it is the accepted ADR-022 trust boundary; tightening is issue #73 scope |
| Terraform beta schema drift (`hosting_version` rewrite block) | Verify against registry before authoring (research open item 1); CLI standalone-binary fallback documented |
| Health path mismatch (/health vs /healthz) | Confirm against deployed service before Phase 2 checklist (research open item 2) |
| #110 slips (no service to point at) | Phases 0-1 have zero service dependency; native blocked-by link on the board makes the wait visible |

## Glossary

| Term | Definition |
| ---- | ---------- |
| Branded address | The hostname we own (api.redmarklogic.com) as opposed to the provider-generated run.app URL |
| Zone | The complete set of DNS records for redmarklogic.com, hosted at Cloudflare |
| Grey cloud | Cloudflare "DNS only" mode: Cloudflare answers name lookups but does not proxy traffic |
| Rewrite proxy | Firebase Hosting rule that forwards every request on the hostname to the Cloud Run service |
| Ownership TXT record | Temporary-looking but permanent DNS text record proving to Google that we control the hostname |
| Cutover | The moment DNS records go live and the branded address starts serving the backend |
