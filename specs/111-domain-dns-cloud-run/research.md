# Research: Connect api.redmarklogic.com to Cloud Run Backend

**Date**: 2026-06-11
**Inputs**: Two DevOps (Brent) research passes, verified against official docs 2026-06-11
(`.agents/tmp/dns-domain-research-2026-06-11/findings.md` and `findings-firebase.md` —
session artifacts; durable facts are consolidated here).

## Decision 1 — Attachment mechanism: Firebase Hosting rewrite proxy

- **Decision**: Front `api.redmarklogic.com` with Firebase Hosting (free tier) and a
  rewrite rule proxying all paths to the Cloud Run service `prod-redline-api` in
  australia-southeast1.
- **Rationale**: Founder decision 2026-06-11 — POC stage, zero monthly cost mandated.
  Firebase Hosting rewrites support australia-southeast1, cost $0 within 10 GB/month
  transfer, and keep ADR-022's no-load-balancer posture.
- **Alternatives considered**:
  - *Cloud Run domain mappings (free, Preview)* — rejected: verified unavailable in
    australia-southeast1; Google labels it not production-ready.
  - *Global external Application Load Balancer + serverless NEG* — rejected for now:
    ~USD 20-25/month fixed cost at zero traffic; contradicts POC cost posture and
    ADR-022's no-LB statement. Documented upgrade path when traffic/long requests
    demand it.
  - *Cloudflare orange-cloud proxy straight to run.app* — rejected: Host-header
    override is Cloudflare Enterprise-only; unsupported by Google.

## Decision 2 — Accepted constraints of the proxy route

- **Decision**: Accept and document: 60-second request ceiling (504 beyond it),
  cookies stripped except `__session`, WebSockets unsupported through the proxy,
  effective body limit assumed 32 MB (Cloud Run's documented limit; Hosting layer
  undocumented).
- **Rationale**: Founder accepted the 60 s ceiling explicitly (2026-06-11). Bearer
  header auth (ADR-022) passes through; no cookie/WebSocket usage exists today.
- **Alternatives**: paying for the ALB to lift the ceiling — deferred (Decision 1).

## Decision 3 — Cloudflare automation: API v4 + Terraform provider; no CLI exists

- **Decision**: Manage Cloudflare DNS via Terraform (`cloudflare` provider) for
  permanent records; Cloudflare API v4 with a scoped token for one-time lookups and
  the pre-change zone snapshot. Token scope: Zone:DNS:Edit + Zone:Zone:Read on
  redmarklogic.com only; stored in Secret Manager.
- **Rationale**: No maintained official Cloudflare DNS CLI exists in 2026: flarectl is
  frozen on the legacy cloudflare-go v0 branch (absent from current v7); wrangler has
  no zone-DNS commands. Terraform matches ADR-020 and Constitution XV.
- **Alternatives**: flarectl (dead end), wrangler (wrong tool), dashboard clicks
  (violates reproducibility requirement FR-005; kept only as documented fallback).

## Decision 4 — Cloudflare proxy mode: grey cloud (DNS only), permanently

- **Decision**: All records for `api.redmarklogic.com` (ownership TXT + A records) are
  created with `proxied = false` and stay that way.
- **Rationale**: Orange-cloud proxying interferes with Firebase's domain verification
  and certificate issuance/renewal; Firebase Hosting already fronts with its own CDN,
  so double-proxying adds nothing.
- **Alternatives**: orange cloud + SSL Full (strict) — only relevant to the ALB route
  (where DNS-authorization certs are proxy-immune); not applicable to Firebase.

## Decision 5 — Firebase on the existing GCP project, dedicated site

- **Decision**: Enable Firebase on `redmarklogic-prod` (no new project); create a
  dedicated Hosting site `redmarklogic-api`.
- **Rationale**: Rewrites only reach Cloud Run services in the same project; a second
  project would split billing/IAM/audit for no benefit. Dedicated site keeps the
  future website (#77) separable.
- **Alternatives**: separate Firebase project — rejected (breaks rewrites); default
  site — workable, but couples API hosting to any future site on the same project.

## Decision 6 — Implementation vehicle: Terraform-first; no npm toolchain

- **Decision**: Express everything possible in HCL under `deploy/infra/terraform/`:
  `google_firebase_project`, `google_firebase_hosting_site`,
  `google_firebase_hosting_custom_domain` (google-beta), `cloudflare` provider records.
  The rewrite config goes through `google_firebase_hosting_version` +
  `google_firebase_hosting_release` if the registry schema confirms Cloud Run rewrite
  support; otherwise fall back to a CI step running the **standalone Firebase CLI
  binary** (not the npm package).
- **Rationale**: Constitution XV / ADR-020 (Terraform for all GCP infra) and
  Constitution XVII (All-Python toolchain — `npm install -g firebase-tools` would
  introduce a Node/npm toolchain; the standalone binary download does not).
- **Alternatives**: npm-installed firebase-tools (violates Constitution XVII);
  Firebase Console wizard (violates ADR-020; kept as documented emergency fallback).

## Decision 7 — Cloud Run ingress stays `all`; run.app bypass documented

- **Decision**: Keep `ingress = all` and unauthenticated invocation on the service.
  Document prominently that the direct `*.run.app` URL remains publicly reachable and
  bypasses the branded domain; app-level Bearer check (ADR-022) is the only gate.
- **Rationale**: `internal-and-cloud-load-balancing` blocks Firebase Hosting traffic
  (Hosting is not a Cloud Load Balancer). This matches the existing ADR-022 Tier-1
  trust boundary; tightening belongs to the auth work (issue #73).
- **Alternatives**: locking ingress to LB-only — impossible while using the free
  Firebase proxy; that is the paid-ALB path.

## Decision 8 — Governance artifacts required before implementation

- **Decision**: One ADR addendum/new ADR recording: Firebase Hosting adoption (new
  platform service, Tier-1 gate per FR-009), the 60 s ceiling, the grey-cloud rule,
  the run.app bypass note, and the $0 cost posture with the billed-egress
  denial-of-wallet caveat ($0.15/GB past 10 GB/month, no hard stop; existing budget
  alert is the backstop).
- **Rationale**: Constitution "ADR before code"; ADR-022 cross-references; FR-009.
- **Alternatives**: silent adoption — prohibited.

## Verification baseline

- Pre-change Cloudflare zone snapshot via `GET /zones/{zone_id}/dns_records/export`
  (BIND format) — proves MX/email records untouched (FR-004, SC-002).
- Cert state observable via the Terraform resource reaching `CERT_ACTIVE`; allow up to
  24 h (SC-001's 48 h budget covers this).
- End-to-end: health endpoint 200 via `https://api.redmarklogic.com`; negative check:
  >60 s request returns 504; direct run.app URL still answers (expected).

## Open items (resolve at implementation time, tracked in tasks)

1. `google_firebase_hosting_version` rewrite-block schema and `cloudflare_dns_record`
   v5 vs `cloudflare_record` v4 naming — verify against the Terraform registries when
   authoring HCL.
2. Health endpoint path: `/health` vs `/healthz` — confirm against the deployed
   service (#110) before writing the verification checklist.
3. firebase-tools acceptance of WIF `external_account` credentials — only relevant if
   the CLI fallback path is used in CI.
4. Host header / forwarded headers seen by the backend through the rewrite — verify
   empirically at first deploy; record actuals in `docs/infrastructure/`.
5. Treat the custom-domain resource's `required_dns_updates` output as the
   authoritative DNS record list (docs page may lag the live flow).
