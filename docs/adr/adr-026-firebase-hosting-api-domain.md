# ADR-026 — Firebase Hosting as Zero-Cost API Domain Front Door

## Summary

`api.redmarklogic.com` is served by a Firebase Hosting rewrite proxy (Google's free
static-hosting CDN) that forwards every request to the Cloud Run backend. Cloudflare
DNS stays in DNS-only mode (grey cloud). This is the Tier-1 governance gate required
by FR-009 before any implementation work begins (issue #111).

**Deciders**: Founder (2026-06-11), Brent (DevOps)

## Status

Accepted — 2026-06-11

**ADR-022 amendment (this ADR):** The statement "No Secret Manager entries are
needed at this stage" in ADR-022's Context section is superseded. The Cloudflare API
token (Zone:DNS:Edit + Zone:Zone:Read on redmarklogic.com) is the first Secret Manager
entry. All subsequent Secret Manager usage continues to follow ADR-021 naming
conventions.

## Context

Redline's backend runs on Google Cloud Run in australia-southeast1 (ADR-022). To give
the backend a stable, professional address instead of the auto-generated
`*.run.app` URL, we need to attach a custom hostname.

**Why the obvious options were ruled out:**

- **Cloud Run domain mappings** — Google's free built-in option — are in Preview status
  and are verified unavailable in australia-southeast1 (checked 2026-06-11). Not
  production-ready.
- **Global Application Load Balancer (ALB)** — the production-grade path — costs
  ~USD 20–25/month in fixed charges even at zero traffic. The founder explicitly
  rejected this for POC stage on 2026-06-11.

**Selected route:** Firebase Hosting rewrite proxy (free tier). Firebase Hosting
(Google's content-delivery network for web apps) owns the hostname, handles TLS
certificates automatically, and forwards every incoming request to the Cloud Run
service. Cost: $0/month up to 10 GB of data transfer; $0.15/GB beyond that (no hard
stop — the existing project budget alert is the denial-of-wallet backstop).

**DNS reality:** redmarklogic.com is registered at Cloudflare and uses Cloudflare
nameservers. All DNS changes are additive — the domain carries live founder email
(`harel@redmarklogic.com`) and no pre-existing record may be modified.

## Decision

### D1 — Attachment mechanism: Firebase Hosting rewrite proxy

Firebase Hosting site `redmarklogic-api` on project `redmarklogic-prod` holds the
custom domain `api.redmarklogic.com`. A rewrite rule forwards all paths (`**`) to the
Cloud Run service `prod-redline-api` in `australia-southeast1`.

**Why it matters:** Zero monthly fixed cost; same Google-managed TLS; stable across
Cloud Run re-deploys; no load balancer needed.

**Accepted trade-off:** Requests longer than 60 seconds return HTTP 504 at the branded
address. Long-running operations must use the direct `*.run.app` URL until a paid
front-door upgrade is approved (separate, founder-gated task).

### D2 — Hostname scope: api.redmarklogic.com only

Only the `api` subdomain is in scope. The apex (`redmarklogic.com`), `www`, and any
future frontend hostnames are explicitly out of scope (website is backlog #77).

### D3 — Cloudflare tooling: Terraform provider + API v4 (scoped token)

DNS records are managed via the Terraform `cloudflare` provider (ADR-020). A scoped
API token (Zone:DNS:Edit + Zone:Zone:Read on redmarklogic.com only) is required for
Terraform and for the mandatory pre-change zone snapshot. No maintained Cloudflare DNS
CLI exists in 2026 (flarectl is frozen; wrangler has no DNS commands) — the Cloudflare
dashboard is the documented emergency fallback only.

### D4 — Cloudflare proxy mode: grey cloud (DNS-only), permanently

All DNS records for `api.redmarklogic.com` are created with `proxied = false`
(Cloudflare "grey cloud" — DNS lookup only, no traffic proxying). This is load-bearing:
orange-cloud proxying breaks Firebase's domain-ownership verification and automatic
TLS certificate renewal. Firebase Hosting already operates its own CDN edge — double
proxying adds nothing and breaks certificate issuance.

**If we skip this:** Firebase cert provisioning fails or never renews silently, and the
branded address goes dark.

### D5 — Firebase project: enable on existing redmarklogic-prod, dedicated site

Firebase is enabled on the existing `redmarklogic-prod` GCP project (no new project).
A dedicated Hosting site `redmarklogic-api` is created. Rewrites can only target Cloud
Run services in the same project. The dedicated site keeps the future website (#77)
separable.

### D6 — Rewrite config vehicle: Terraform-first (hosting_version + release resources)

The rewrite rule is expressed in Terraform HCL using
`google_firebase_hosting_version` + `google_firebase_hosting_release` (google-beta
provider, confirmed schema 2026-06-11). This satisfies Constitution XV (Terraform for
all GCP infra) and ADR-020.

The standalone Firebase CLI binary (not the npm package) is documented as a CI fallback
only. The npm `firebase-tools` package is prohibited — it would introduce a Node/npm
toolchain in violation of Constitution XVII.

A human-readable `deploy/firebase/firebase.json` is committed regardless (it is the
CI-fallback artefact and the plain-language statement of the rewrite intent).

### D7 — Cloud Run ingress: stays `all`; run.app bypass documented and accepted

Cloud Run `ingress` remains `INGRESS_TRAFFIC_ALL` and unauthenticated invocation stays
enabled. Tightening to `internal-and-cloud-load-balancing` would block Firebase Hosting
traffic (Firebase is not a Cloud Load Balancer). The direct `*.run.app` URL remains
publicly reachable — this is the accepted ADR-022 trust boundary. Tightening belongs to
the auth work (issue #73).

**If we skip documenting the bypass:** API consumers may rely on the run.app URL
thinking it is the stable address; re-creating the service would silently break them.

### D8 — Governance: this ADR accepted before any terraform apply

This ADR is the Tier-1 governance gate (FR-009) for introducing Firebase Hosting as a
new platform service. No `terraform apply` for Firebase or DNS resources may run until
this ADR is merged.

## Accepted Constraints (recorded for consumers)

| Constraint | Value | Impact |
|------------|-------|--------|
| Request duration ceiling | 60 seconds | Requests >60 s return HTTP 504 at `api.redmarklogic.com` |
| Cookie passthrough | Only `__session` literal name | Session cookies must use exactly `__session` if added (Kabilan constraint) |
| WebSockets | Not supported through this hostname | Use direct run.app URL if WebSockets are ever needed |
| Effective max body | ~32 MB (Cloud Run documented; proxy layer undocumented) | Large uploads should be handled via signed URL direct-to-GCS |
| Data transfer cost | $0 to 10 GB/mo; $0.15/GB beyond | No hard stop — budget alert is the backstop |
| run.app bypass | `https://prod-redline-api-*.run.app` remains public | Same app-level Bearer check applies; address unstable if service is recreated |

## Options Considered

| Option | What it means | Monthly cost | Availability | Complexity | Verdict |
|--------|--------------|-------------|-------------|-----------|---------|
| **Firebase Hosting rewrite (selected)** | Free CDN proxy forwarding branded hostname to Cloud Run | $0 (+ $0.15/GB egress past 10 GB) | Available australia-southeast1 | Low | **Selected** |
| Cloud Run domain mappings | Google's native free binding of custom hostname directly to Cloud Run | $0 | Not available in australia-southeast1 (Preview, excluded from region) | Low | Rejected — unavailable |
| Global ALB + serverless NEG | Production load balancer in front of Cloud Run | ~USD 20–25/month fixed | Available | High | Rejected — cost contradicts POC posture; revisit when traffic demands |
| Cloudflare orange-cloud to run.app | Route via Cloudflare proxy directly to run.app URL | $0 | Technically possible | Low | Rejected — Host-header override is Cloudflare Enterprise only |

## Consequences

**Immediate (this feature, issue #111):**

- Brent provisions: `google_firebase_project`, `google_firebase_hosting_site`,
  `google_firebase_hosting_custom_domain`, `google_firebase_hosting_version`,
  `google_firebase_hosting_release`, `cloudflare_dns_record` (TXT + A records).
- Cloudflare API token created (dashboard — documented manual exception); stored in
  Secret Manager as `prod-redline-cloudflare-api-token` (ADR-021 naming).
- Pre-change zone snapshot captured and committed before any DNS record is touched.
- `deploy/infra/terraform/versions.tf` gains google-beta and cloudflare provider pins.

**Ongoing:**

- Any change to the proxy route (switching to ALB, adding staging hostname, tightening
  ingress) requires a new or amended ADR.
- The 60-second ceiling and `__session` cookie constraint are permanent until the
  front-door is upgraded — both must be surfaced in API consumer documentation.
- Cloudflare records must remain `proxied = false`; Terraform enforces this on every
  apply (drift reverted automatically).

**Before production launch:**

- If any request path legitimately exceeds 60 seconds at the branded address, a paid
  ALB front door must be approved and provisioned (separate founder-gated task).

## Cross-References

- **ADR-020** — Infrastructure as Code with Terraform for GCP. All resources from this
  ADR are declared in `deploy/infra/terraform/`.
- **ADR-021** — Process Environment as Sole Config Source. Cloudflare token stored in
  Secret Manager per naming convention `<env>-redline-<credential>`.
- **ADR-022** — Cloud Run + Artifact Registry Hosting. This ADR extends ADR-022's
  trust-boundary approval (D7 above) and amends its "no Secret Manager entries" clause.
- **ADR-023** — Staging/Prod split. The `redmarklogic-api` site serves prod only at
  this stage; a `api-staging.redmarklogic.com` hostname is a future "could have" item.
- **Issue #111** — Implementation issue for this feature.
- **Issue #73** — B-1b SSO/IdP wiring; will tighten the trust boundary left open here.
- **Issue #77** — Future website/apex hostname (out of scope here).
- **Issue #110** — Deployed Cloud Run service (Phase 2 hard dependency).
