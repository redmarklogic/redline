# ADR-024 — Django Web Stack, Server-Rendered Frontend, Single Service

## Summary

Redline's Phase-1 product is built as a single Django application: server-rendered
Django templates with a vendored HTMX library for partial page updates, plain Django
views (no Django REST Framework) serving the skeleton-generation endpoint under the
[ADR-018](adr-018-external-http-api-contract-conventions.md) contract, Django's
built-in admin enabled at launch, and platform state (users, sessions, quota counters,
audit log) in Cloud SQL via the Django ORM. It deploys as one container to the single
Cloud Run service per environment established by
[ADR-022](adr-022-cloud-run-artifact-registry-hosting.md). The hard constraint this ADR
imposes: Django stays in the web shell — no Django import may appear in the `domain` or
`functions` packages, and no geotechnical concept may be modelled as a Django ORM model.

**Deciders**: Founder (ratified across a three-round interview, 2026-06-11), Peter
(architecture), Brent (DevOps).

## Decision

1. **Web framework: Django**, replacing the FastAPI walking-skeleton adapter. The
   generator core (`build_skeleton` behind the `DocumentFacade` of
   [ADR-002](adr-002-docx-generation-engine-facade.md)) is unchanged.
2. **No Django REST Framework.** The external HTTP surface — the skeleton-generation
   endpoint (`POST` on the skeletons resource) and health check — is served by plain
   Django views honouring the [ADR-018](adr-018-external-http-api-contract-conventions.md)
   error envelope, status codes, and binary-response conventions.
3. **Frontend: server-rendered Django templates + HTMX**, vendored as a single static
   file with no build step. Launch-day user experience is a web page: sign in, fill a
   form, download the DOCX. An API-only consumption mode is deferred to Phase 2.
4. **All-Python rule, clarified line:** the rule prohibits a *second language toolchain
   or ownership* — no additional compiler, package/version manager, or skillset
   requiring a new owner. Vendored JavaScript (no toolchain), CSS, and Python packages
   that emit JavaScript are acceptable. This is the precedent test for all future
   frontend requests.
5. **Identity, sessions, quota, and admin ride Django's batteries:** django-allauth
   (self-hosted, Sydney region) for sign-in, `django.contrib.sessions` for sessions, a
   Django model plus middleware/decorator for quota, and `django.contrib.admin` enabled
   at launch as the founder's back office (user/quota inspection, quota reset,
   blocking). The sign-in method selection (which providers, fallback policy) is
   recorded in a separate sign-in ADR.
6. **Quota policy:** configurable per-user cap, default 3, non-renewable in the free
   tier. At the limit, generation is blocked and the user sees a quota-exhaustion
   message with a Pre-Review call-to-action. The cap is platform data, edited through
   the admin — it is runtime business state, not deployment configuration, so it does
   not conflict with [ADR-021](adr-021-process-environment-as-sole-config-source.md).
7. **No document blob storage at launch.** Generated documents are returned to the user
   and not retained. An append-only audit log in Cloud SQL records timestamp, user,
   input parameters, model/template version, and a hash of the output document. Object
   storage for generated documents is a new decision if and when the Pre-Review product
   needs stored documents.
8. **Topology: one Cloud Run service per environment** (the pair established by
   [ADR-022](adr-022-cloud-run-artifact-registry-hosting.md) /
   [ADR-023](adr-023-staging-prod-split-secret-manager.md)), one container, with Cloud
   SQL (smallest tier, same region) added to the launch path as the platform state
   store. No second runtime service may be introduced without a new ADR.
9. **Walking-skeleton disposition:** the existing FastAPI adapter (~430 lines, no
   business logic) pivots to Django views — estimated one to two days. The durable
   artifact is the [ADR-018](adr-018-external-http-api-contract-conventions.md)
   contract and its tests, which are framework-neutral and survive the pivot. The
   placeholder bearer-auth dependency is discarded, replaced by allauth sessions.

## Status

Proposed — 2026-06-11

## Context

### Diagnosis

- **Stage:** pre-revenue, single founder plus agents, roughly seven weeks to the
  2026-07-31 launch backstop recorded in the active strategic bet. Launch is defined as
  the skeleton generator publicly reachable AND a sign-in-gated, verified-work-email
  signup flow with a per-user quota. The generator core works; the HTTP path is proven
  by the FastAPI walking skeleton.
- **Binding constraints:** the launch backstop; a USD ~100/month infrastructure design
  ceiling (alert at 80, hard stop-and-talk at 150); single Cloud Run service; all-Python
  team capability; an approved "all data stays in Australia" commercial claim pinning
  data to the Sydney region; first users are ~10 named co-development partner firms.
- **Theoretical-only constraints:** Phase-2 API consumers, multi-engine document
  generation at scale, horizontal scale beyond one service, pixel-perfect output. None
  of these bind at 50-signup scale and none were allowed to drive the ranking.

### Forces

Worked backwards from the launch failure mode (inversion): launch does not fail on a
weak generator — it fails if verified signup and quota do not exist by the backstop.
Hand-rolling verified-email signup, session management, a user model, and quota
accounting on FastAPI was estimated at two to four weeks of the seven remaining;
Django's batteries (allauth, sessions, ORM, admin) cover the same ground in roughly one
week. The walking-skeleton adapter was deliberately thin, so the framework pivot is a
two-way door; bespoke auth code would have been a slow-closing one.

Per-user quota requires a persistent store under every option, so Cloud SQL is
load-bearing regardless of framework. The connection-strategy analysis for Cloud SQL
(prepared by DevOps) feeds a separate infrastructure ADR; this ADR fixes only that the
store exists on the launch path and that the Django ORM is its client.

Two open items are **explicitly not decided here** (recorded so this ADR is intelligible
in isolation):

- **Launch-date conflict.** The stack-decision brief stated a 2026-09-01 launch
  expectation; the strategic-bet record holds a 2026-07-31 backstop that triggers
  mandatory bet review. Five weeks of appetite hang on which governs. It is deferred
  because it is a product/strategy call, not an architecture call; it resolves when
  product and strategy agree a single governing date. It changes appetite, not this
  ranking — Django wins under either date.
- **Privacy-policy page.** The OAuth consent screens require a published privacy-policy
  URL on the company domain. The page is marketing-site content, deferred to the
  marketing-site workstream; it resolves when that page is published. It is a launch
  checklist dependency for the sign-in flow, not a stack decision.

## Options Considered

The four stack shapes evaluated, scored against the decision brief's criteria in
priority order (time-to-demo, all-Python fit, core decoupling, signup/quota fit, Cloud
Run surface, complexity, reversibility, rework on the walking skeleton):

- **Option 1 — FastAPI-only + static or server-rendered frontend.** Keeps the walking
  skeleton as-is; wins every criterion except the one the launch dies on: verified
  signup, sessions, user model, and quota must all be hand-built or delegated to a
  hosted identity provider. Rejected: the auth gap is the rabbit hole, not the
  generator.
- **Option 2 — Django + Django REST Framework + templates.** Identical batteries to the
  chosen option, but pays DRF's serializer/viewset machinery for an API richness Phase
  1 does not need (one binary-returning endpoint plus a health check). Rejected as dead
  weight; DRF can be added later as an additive, two-way-door change if real API
  consumers appear.
- **Option 3 — Django + templates + HTMX, no DRF, plain Django views (CHOSEN).**
  Options 2 and 3 converge once DRF is recognised as unnecessary: the ADR-018 envelope
  is framework-portable JSON and does not require DRF serializers.
- **Option 4 — Django + FastAPI + JavaScript SPA (expected-reject).** Second language
  toolchain, two frameworks with structural pressure toward two deploy surfaces, fires
  every trust-boundary trigger. Rejected as textbook Second-System Effect — designing
  for an imagined Phase-2 SaaS instead of the bet in front of us.

Topology variants were evaluated with the stack: a two-service split (app + API) was
rejected for Phase 1 — it doubles cost, CI, secrets, and alerting, fires two Tier-1
trust-boundary triggers, and the asymmetry is decisive (splitting later is routine;
merging later is re-architecture). The static marketing site remains a separate,
genuinely static artifact behind the same load balancer and is not a second app service.

## Decision Rationale

- **Inversion:** rank options by how directly they remove the actual launch failure
  mode (signup + quota missing at the backstop). Django's batteries map one-to-one onto
  the kill criterion.
- **Opportunity cost:** every week re-implementing what allauth and the admin ship for
  free is a week not spent on the wedge. ~1 week of integration versus 2–4 weeks of
  bespoke auth, against a 7-week runway.
- **Two-way doors:** the thin-adapter design of the walking skeleton makes the
  framework pivot cheap (days), and the framework-neutral ADR-018 contract plus its
  tests carry over unchanged. Django ORM models are the stickiest piece, but they are
  confined to the web shell, so the generator core's door stays two-way.
- **Surviving the Round:** on the short-runway horizon (3–6 months, ~50 users, the
  budget ceiling) only the chosen option is justified. Option 4 is arguable only under
  a 2+ year funded-team assumption and is therefore deferred by policy. Phase-1
  architecture is explicitly disposable; this stack optimises learning velocity.
- **All-Python line:** the founder set the rule's letter — the test is toolchain and
  ownership complexity, not file extension. HTMX (one vendored file, no build step)
  passes; a Node/npm toolchain does not.

### Layer guardrail (constraint-as-test)

The "stateless generator" framing survives by naming the layers honestly: the
*generator* (`build_skeleton` + facade) is stateless and pure; the *platform shell*
around it (identity, sessions, quota) is stateful and always was going to be. Therefore:

1. No code in the `domain` or `functions` packages may import Django (mirror of the
   existing FastAPI-leakage guardrail). Hook-expressible; enforced alongside the
   existing import-linter layer contracts.
2. Django ORM models hold **platform state only** — users, sessions, quota counters,
   audit-log rows. No geotechnical concept may be modelled as a Django model; domain
   stays in plain Python.
3. The web shell calls `build_skeleton` with typed inputs and receives bytes — it never
   touches document-engine types
   ([ADR-002](adr-002-docx-generation-engine-facade.md) boundary, unchanged).

The per-layer ownership table derived from this ADR lives in the layer-responsibilities
document in the architecture documentation set.

## Consequences

**Positive**

- Signup, sessions, quota, and a founder-operable back office land within the launch
  runway using maintained, widely-audited components.
- One language, one runtime, one container, one service: cost and operational surface
  stay inside the budget ceiling, and the trust boundary does not move.
- The ADR-018 contract and tests survive the pivot; the walking skeleton's purpose
  (prove the HTTP path, keep the adapter thin) is fulfilled, not wasted.
- No blob storage at launch keeps the residency surface minimal (one database, one
  region) and removes bucket/signed-URL/retention work from the critical path.

**Negative / accepted costs**

- One to two days of pivot work on the adapter; the Pydantic schemas and contract-test
  assertions carry over, the FastAPI wiring does not.
- Django ORM models introduce framework-shaped persistence in the web shell; re-platforming
  the shell later means migrating those models. Accepted: the core stays portable.
- Cloud SQL bills 24/7 (~USD 12–35/month at the smallest tier) — accepted within the
  budget ceiling as the price of multi-user state.
- Plain views mean any future rich API surface (DRF or other) is a later, additive
  decision — Phase-2 API consumers wait.
- The vendored-HTMX precedent must be policed: "one more vendored file" is the
  scope-creep vector for a second-language toolchain.

## References

- [ADR-002 — DOCX Generation Engine Selection and Facade Abstraction](adr-002-docx-generation-engine-facade.md)
- [ADR-018 — External HTTP API Contract Conventions](adr-018-external-http-api-contract-conventions.md)
- [ADR-020 — Infrastructure as Code with Terraform for GCP](adr-020-infrastructure-as-code-terraform-gcp.md)
- [ADR-021 — Process Environment as Sole Config Source](adr-021-process-environment-as-sole-config-source.md)
- [ADR-022 — Cloud Run + Artifact Registry Hosting](adr-022-cloud-run-artifact-registry-hosting.md)
- [ADR-023 — Staging/Prod Split + Secret Manager](adr-023-staging-prod-split-secret-manager.md)
- Internal documents informing this decision (named by concept per the persistence
  boundary): the strategic-bets record (kill criterion and backstop date), the Skeleton
  Generator PRD (quota acceptance criteria), the audit-trail PRD (parameters + hash
  logging), and the Cloud SQL connection-strategy analysis in the infrastructure
  documentation set.
