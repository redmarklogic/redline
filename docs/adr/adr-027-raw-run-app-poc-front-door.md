# ADR-027 — Raw run.app URL as POC Front Door; Firebase API Front Door Torn Down; Branded API Domain Deferred

## Summary

The Firebase Hosting front door for `api.redmarklogic.com`
([ADR-026](adr-026-firebase-hosting-api-domain.md)) is torn down. For the POC
(proof of concept), the API's address is the raw Cloud Run `*.run.app` URL. The
reason is a hard incompatibility discovered on 2026-06-12: synchronous API calls are
now known to take **three minutes or more**, and Firebase Hosting kills every request
at **60 seconds** (a fixed platform limit, not configurable). Every real API call
through the branded address would fail. A branded API domain is **deferred** with
explicit reopen triggers. The Firebase *project* enablement stays (it is irreversible,
costs nothing, and the Sprint-3 static website will reuse it).

**Deciders**: Founder (2026-06-12), Peter (architecture), Brent (DevOps — verified
audit and alternatives analysis).

## Status

Accepted — 2026-06-12

**Supersedes [ADR-026](adr-026-firebase-hosting-api-domain.md).** ADR-026's
decision record remains in the repository for history; its Status is marked
Superseded by this ADR.

**Constitution review (Peter, per ADR-sync duty):** checked 2026-06-12 — no
constitution principle references the front door, Firebase Hosting, cookie naming,
or the branded API address. No constitution amendment is warranted by this ADR.

## Context

### Diagnosis

- **(a) Stage.** Pre-revenue POC, single founder + agents, ~7 weeks to the
  2026-07-31 launch backstop. The Django pivot (ADR-024) is decided; the Django
  sprint backlog is the active work. The only API consumers today are the founder
  and the in-development web shell — zero external consumers. The branded address
  has **never served a successful response** (it has returned 403 since creation,
  pending the public-invoker decision in #114), so tearing it down has effectively
  zero blast radius.
- **(b) Binding constraints right now.** Synchronous skeleton/Pre-Review calls take
  **≥ 3 minutes** (founder requirement statement, 2026-06-12). The Firebase rewrite
  proxy's 60-second ceiling (ADR-026 accepted trade-off) is therefore not a
  trade-off any more — it is a guaranteed-failure path for the product's core
  operation. Cost ceiling: POC posture rejects fixed monthly front-door spend.
  Cloud Run itself is configured at 300 seconds (`timeout = "300s"`,
  `deploy/infra/terraform/cloud_run.tf`) and is raisable to 60 minutes — the
  backend was never the bottleneck.
- **(c) Theoretical-only constraints.** Brand polish of the API hostname, external
  integrator onboarding, client-visible custom error pages. None bind at
  zero-external-consumer scale.

### Verified findings (Brent audit, 2026-06-12)

The teardown decision rests on Brent's verified findings (full audit in the
2026-06-12 working notes; load-bearing facts restated here so this ADR is
self-contained):

- **Firebase 60 s ceiling is hard.** Documented, not configurable. Incompatible
  with ≥ 180 s synchronous calls.
- **No $0 branded front door supporting ≥ 180 s synchronous calls exists today:**
  - **Cloud Run domain mappings** — still Preview, still **not available in
    australia-southeast1** (re-verified 2026-06-12).
  - **Cloudflare direct proxy (orange cloud → run.app)** — broken: Cloud Run routes
    by Host header, and overriding it requires Cloudflare Enterprise.
  - **Cloudflare Worker front door** — *unverified*: docs say no set subrequest
    duration limit, but the free-plan 100 s proxy timeout may apply in practice; a
    ~10-minute empirical test against a deliberate 200 s endpoint is pending and
    would settle it. Not relied upon for this decision.
  - **Global Application Load Balancer (ALB)** — works (backend timeout configurable
    to 60 min) at ~USD 18–25/month fixed; rejected at POC stage by the founder
    (re-affirmed 2026-06-12).
- **Blast radius of teardown: effectively zero.** The branded URL never served a
  successful response; no consumer depends on it; the run.app URL is unaffected.

## Decision

### D1 — POC canonical address: the raw Cloud Run run.app URL

The API's address for the POC is the auto-generated Cloud Run URL of
`prod-redline-api` (australia-southeast1). This is now the **contractual address**
recorded in the HTTP API standard — reversing ADR-026 D7, which classed it as an
unstable bypass.

**Accepted risk, eyes open:** the run.app hostname changes if the Cloud Run service
is ever deleted and recreated. At POC stage the consumers are the founder and
Redline's own web shell — both under our control and trivially repointable. This
risk is re-evaluated at the first external consumer (reopen trigger, D4).

**Why it matters:** the run.app path honours the full Cloud Run timeout (300 s
today, configurable to 3600 s), costs $0, and requires no work.

### D2 — Teardown of the Firebase API front-door pieces

Brent destroys, via Terraform (no `terraform destroy`/`apply` before this ADR is
merged — same gate discipline as ADR-026 D8):

| Resource | Action |
|---|---|
| `google_firebase_hosting_custom_domain.api` (`api.redmarklogic.com`) | Destroy |
| `google_firebase_hosting_version.api` + `google_firebase_hosting_release.api` (the rewrite) | Destroy |
| `google_firebase_hosting_site.api` (`redmarklogic-api`) | Destroy |
| `cloudflare_dns_record.firebase_cname` (`api` CNAME) | Delete via Terraform, with the mandatory pre-change zone snapshot (additive-only zone discipline of ADR-026 D3 continues — live founder email on the zone) |
| `deploy/firebase/firebase.json` | Remove (rewrite intent no longer exists) |

### D3 — What stays

| Item | Disposition | Why |
|---|---|---|
| `google_firebase_project.default` (Firebase enabled on `redmarklogic-prod`) | **Stays** | Irreversible (provider implements no delete; account-level ToS acceptance is permanent), zero cost, zero risk — and the Sprint-3 static website reuses it |
| Cloudflare API token + Secret Manager entry `prod-redline-cloudflare-api-token` | **Stays** | Needed for any future DNS automation, including Sprint-3 website DNS |
| google-beta / cloudflare provider pins in `versions.tf` | **Stay** | Reused by Sprint-3 website hosting |

The 2026-06-11 Firebase work is not written off: it bought the permanent project
enablement, the DNS automation tooling, and the process literacy that Sprint 3's
website (a genuinely good fit for Firebase Hosting — static content, no long
requests) will reuse under its own site ID.

### D4 — Branded API domain: deferred, with reopen triggers

A branded hostname for the API is deferred — not abandoned. The deferral terminates
when **any** of these fires:

1. **Sprint-3 website DNS work touches the domain.** When the website workstream
   is editing the `redmarklogic.com` zone anyway, the marginal cost of deciding the
   API hostname question drops; revisit then (including the pending ~10-minute
   Cloudflare Worker empirical test if a $0 answer is still wanted).
2. **First external consumer.** An integrator outside Redline's control must not be
   handed an address that changes on service recreation (the D1 accepted risk stops
   being acceptable).
3. **Income enabling the ~USD 18–25/month global ALB.** The ALB is the
   production-grade answer: configurable timeout to 60 minutes, and it additionally
   unlocks **control over client-visible platform error pages** (custom error
   responses at the edge), which no $0 option offers.

On reopen, the decision is a new ADR; nothing here pre-selects the mechanism.

### D5 — Consequences for the HTTP API standard (v0.2, same change set)

The teardown dissolves two ADR-026 constraints and reshapes a third; the standard
is amended in the same change set as this ADR:

1. **Synchronous request budget** is Cloud Run's configured timeout — **300 s
   today, configurable up to 3600 s** — not 60 s. The known ≥ 3-minute synchronous
   calls fit inside the current configuration.
2. **The `__session` cookie-name constraint dies with the proxy.** Firebase was the
   only layer that stripped cookies; Cloud Run passes cookies through unaltered.
   (Auth architecture consequences are recorded in the ADR-025 amendment, same
   change set.)
3. **Platform-error surface slims.** The Firebase proxy-504 error class disappears.
   What remains inherent to the platform and outside the application's control:
   Google Front End **403** (IAM/invoker layer), Cloud Run **429/503**
   (scaling/instance caps), and Cloud Run **504** (request-timeout breach). The
   standard's platform-error tolerance clause covers these.

## Options Considered

| Option | Timeout ceiling | Monthly cost | Verdict |
|---|---|---|---|
| **Raw run.app URL (selected)** | 300 s (raisable to 60 min) | $0 | **Selected** — only $0 option that meets ≥ 180 s today; instability risk acceptable at POC |
| Keep Firebase front door | 60 s hard | $0 | Rejected — guaranteed failure for the core operation |
| Cloud Run domain mappings | service timeout | $0 | Rejected — still unavailable in australia-southeast1 (re-verified 2026-06-12) |
| Cloudflare direct proxy to run.app | n/a | $0 | Rejected — Host-header override is Enterprise-only; confirmed dead end |
| Cloudflare Worker front door | unverified ≥ 180 s (free-plan 100 s wall may apply) | $0 | Not selected — pending a ~10-minute empirical test; revisit under D4 trigger 1 |
| Global ALB + serverless NEG | configurable to 60 min | ~USD 18–25 | Rejected at POC — cost; becomes the default answer under D4 trigger 3 |
| Async-only API (202+poll) as the front-door fix | any | $0 infra | Not a front-door decision — application redesign on its own timeline (§8 of the standard already prefers 202+poll for minutes-long work); does not remove the need for a working synchronous path at POC |

## Consequences

**Immediate:**

- Brent executes the D2 teardown (Terraform, zone snapshot first) after this ADR
  merges.
- The HTTP API standard goes to v0.2 in the same change set (D5).
- ADR-026's Status is marked Superseded by ADR-027.
- Issue #114 (public invoker) now gates the run.app URL directly — there is no
  second hostname to reason about.

**Ongoing:**

- All API documentation, OAuth redirect URIs, and client configuration use the
  run.app URL. OAuth registrations already target the stable Cloud Run service
  URLs (ADR-025 noted redirect URIs are not a blocker), so no rework there.
- Any future front-door change is a new ADR (D4).

**Accepted costs:**

- No branded API address at POC — demos and docs carry a `*.run.app` URL.
- Service recreation breaks the address; mitigated by control over all current
  consumers and by D4 trigger 2.

## Cross-References

- **[ADR-026](adr-026-firebase-hosting-api-domain.md)** — superseded by this ADR.
- **[ADR-022](adr-022-cloud-run-artifact-registry-hosting.md)** — Cloud Run hosting;
  the run.app trust boundary this ADR now makes canonical.
- **[ADR-024](adr-024-django-web-stack-single-service.md)** — single-service Django
  stack; the 300 s Cloud Run timeout configuration context.
- **[ADR-025](adr-025-launch-sign-in-google-microsoft-oauth-only.md)** — sign-in
  ADR; amended in the same change set (dual-track auth; `__session` retirement).
- `docs/architecture/api/http-api-standard.md` v0.2 — the operational standard
  carrying these constraints.
- **Issue #79** — API standards revisit (decision side closed by this ADR).
- **Issue #114** — production public-invoker posture (unchanged in substance, now
  applies to the canonical address).
- Brent's Firebase audit and alternatives analysis, 2026-06-12 (working notes;
  load-bearing findings restated in Context above).
