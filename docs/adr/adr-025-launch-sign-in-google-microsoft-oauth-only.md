# ADR-025 — Launch Sign-In: Google + Microsoft OAuth Only, via Self-Hosted django-allauth

## Summary

At launch, users sign in with "Sign in with Google" or "Sign in with Microsoft" buttons
only — no passwords, no email-link fallback — implemented with self-hosted
django-allauth on the Django stack of
[ADR-024](adr-024-django-web-stack-single-service.md), with credentials and user data
pinned to the Sydney region. A pre-agreed trigger governs the only planned change: the
moment a named co-development partner cannot sign in (wrong ecosystem, or their IT
blocks third-party sign-in apps), an email-link fallback is added as a bounded
retrofit. Personal-domain emails (e.g. gmail.com, outlook.com) are allowed but flagged
and excluded from the signup kill metric. The hard constraint: no hosted identity
provider and no transactional email service may join the launch path.

**Deciders**: Founder (ratified 2026-06-11), Peter (architecture), Brent (DevOps).

## Decision

1. **Sign-in methods at launch:** Google OAuth and Microsoft OAuth (OpenID Connect
   sign-in scopes only), via django-allauth's standard providers. No password
   authentication. No email-verification fallback.
2. **Pre-agreed retrofit trigger:** when any named co-development partner is blocked —
   their firm is on neither ecosystem, or their tenant requires admin consent that is
   refused — an email-link fallback is added then. The fallback decision at that time
   must choose between an Australia-region email provider and a founder-approved
   wording carve-out to the "all data stays in Australia" claim, because mainstream
   transactional email providers process mail through US infrastructure.
3. **Personal-domain emails: allow but flag.** Sign-ups from consumer domains can use
   the product but are excluded from the 50-verified-work-email-signup kill metric in
   the active strategic bet. Consequence: the Microsoft app registration is configured
   for work *and* personal account types, and the Google client does not filter to
   Workspace accounts.
4. **Self-hosted django-allauth over a hosted identity provider** (Auth0, GCP Identity
   Platform). A hosted provider would expand the trust boundary (a Tier-1 gate under
   the infrastructure approval rule), add cost, and route identity data through US
   processing — contradicting the residency claim. Adding Google and Microsoft as
   OAuth identity providers fires no Tier-1 provisioning gate: no new GCP service, no
   new GCP IAM principal type, and egress is the standard OAuth token exchange; the
   required architectural consultation is satisfied by this ADR itself.
5. **Verification posture:** "verified work email" is inherited from the identity
   provider; no email-sending infrastructure exists at launch. The two OAuth client
   secrets live in Secret Manager via the established Terraform secret-bindings
   pattern, Sydney-pinned. The OAuth app registrations themselves are not
   Terraform-manageable and are recorded as documented manual steps with rollback
   entries, per the exception process of
   [ADR-020](adr-020-infrastructure-as-code-terraform-gcp.md).

## Status

Proposed — 2026-06-11
Amended — 2026-06-12 (Amendment 1: dual-track session establishment; founder-ratified)

## Amendment 1 — Dual-Track Authentication (2026-06-12)

**Deciders:** Founder (2026-06-12), Peter (architecture).
**Grounding:** Office Word task-pane authentication research, 2026-06-12 — durable
copy at
`docs/research/software-development/20260612-office-taskpane-addin-authentication.md`.
Companion decision: [ADR-027](adr-027-raw-run-app-poc-front-door.md) (Firebase
front-door teardown), same change set.

The provider selection above (Google + Microsoft OAuth, self-hosted django-allauth,
no passwords, no email fallback) is **unchanged**. What this amendment changes is
the *session-establishment* architecture downstream of OAuth completion.

### A1 — Dual-track authentication is first-class; neither track is dormant

Redline's API supports **two session mechanisms as first-class contract**:

1. **Session cookies** — for the browser website (Django sessions via
   `django.contrib.sessions`, per ADR-024 decision 5).
2. **Bearer tokens** (`Authorization: Bearer <token>`) — for the Word task-pane
   add-in and any machine client.

**Binding rule: session cookies MUST NOT be the only authentication mechanism.**
The research finding is load-bearing: cookies set by the API's origin are blocked
or unreliable inside Word task panes — all third-party cookies are blocked in Mac
WKWebView (ITP, not disableable in the embedded control), the Office-on-the-web
task pane is a cross-origin iframe where every API cookie is by definition
third-party, and Chromium is partitioning/phasing out third-party cookies on
Windows WebView2. Every viable add-in auth path terminates in a bearer header on
fetch. A cookie-coupled session model would have to be retrofitted later at high
cost; designing the dual track in now is cheap.

The in-pane sign-in pattern for the add-in is **independent login via the Office
Dialog API** (`displayDialogAsync` → provider sign-in → redirect landing page →
`messageParent` hands the token to the pane). This is Microsoft's documented
first-class pattern for non-Microsoft identity providers and dissolves the
Google-email-vs-Microsoft-email identity-mismatch problem: the add-in runs the
product's own sign-in, so the API sees the same identity it sees on the web.

### A2 — OAuth completion is decoupled from "set cookie"

The OAuth callback terminates in a **session-establishment primitive**, not an
inline `Set-Cookie`. The flow is structured as *authorization-code →
session-establishment step*, where that step either:

- sets a session cookie (browser website), or
- hands a token to the Office-dialog `messageParent` landing page (add-in).

This is a design-shape constraint on the Sprint-3 django-allauth implementation —
near-free now, expensive to retrofit.

### A3 — Stable internal user ID with (provider, subject) identity rows

The user model carries a **stable internal user ID**, with provider identities
stored as **`(provider, subject)` rows** linked to it — even while every user has
exactly one row. This one-time schema decision makes future account linking (a
second provider on the same account) and a future Microsoft-identity row additive
instead of a migration.

### A4 — The `__session` cookie-name constraint is retired

ADR-026 required any session cookie crossing the branded address to be named
exactly `__session` (Firebase proxy passed only that literal name). ADR-027 tears
that proxy down; Cloud Run passes cookies through unaltered. **The constraint is
void.** Django's default session-cookie naming applies; no Kabilan workaround is
needed.

### Explicitly deferred (with triggers) under this amendment

| Deferred item | Trigger |
|---|---|
| Bearer-token issuance/validation implementation, token format, dialog-page plumbing | Word add-in epic kickoff (first task-pane consumer scheduled) — the *contract* is first-class now; the *implementation* ships with its first consumer |
| Nested App Authentication (NAA)/Office SSO as a convenience accelerator; Entra app registration | Add-in epic, and only if double sign-in is a measured complaint |
| Email-matching SSO linking (Microsoft token email → Google-created account) | Deferred indefinitely — **nOAuth account-takeover risk**: Entra ID `email` claims can be unverified/user-mutable; any future matching requires verified-claim gating plus one-time proof of ownership |
| Account-linking UI (multi-provider per account) | First real support cases of mismatched emails |

## Context

### Diagnosis

- **Stage:** pre-revenue, ~7 weeks to the 2026-07-31 launch backstop. Launch is defined
  as the generator publicly reachable AND a sign-in-gated, verified-work-email signup
  flow. Sign-in sits directly on the kill-metric critical path.
- **Binding constraints:** the backstop; the approved "all data stays in Australia"
  commercial claim; ~10 named co-development partner firms as the entire initial user
  population; no transactional email capability exists and building deliverability
  (sender-reputation DNS, spam-filter survival at conservative firms) is its own
  project.
- **Theoretical-only constraints:** enterprise SAML federation, multi-tenant org
  management, identity-provider scale pricing. None bind at 50-signup scale.

### Forces

The one launch failure that cannot be patched quickly is a co-development partner stuck
at the login screen. Australian/New Zealand engineering firms are predominantly
Microsoft 365 shops with a Google Workspace minority, so covering both ecosystems
covers nearly all named partners. Registration cost on our side is near zero: Google
sign-in-only scopes (openid, email, profile) are classified non-sensitive and require
no app-verification review (same-day), and Microsoft Entra app registration is instant
and free. The genuine lead-time risk is on the *partner* side: conservative firms set
tenant policy to "admin consent required" for third-party apps, and that approval can
take days to weeks and is outside our control.

**Open item, stated inline:** the founder's partner-firm survey is outstanding — for
each of the ten firms: (1) Microsoft 365, Google Workspace, or other? (2) does their IT
block third-party sign-in apps? It is deferred because only the founder can obtain
these facts; it resolves when the firms are walked. If any firm is on neither ecosystem
or blocks consent, the retrofit trigger in Decision 2 fires. Until then, this decision
stands on the ecosystem-coverage argument, not on confirmed per-firm facts.

**Launch checklist dependency, stated inline:** the Google production consent screen
requires the company domain in its authorized-domains list (a one-time DNS ownership
verification riding the existing domain/load-balancer work) and a published
privacy-policy URL on that domain (marketing-site workstream). Both are sequencing
dependencies, not decisions of this ADR. Redirect URIs are not a blocker: both
providers accept multiple URIs, so registrations proceed now against the stable Cloud
Run service URLs, with the final app subdomain added later.

## Options Considered

- **Option A — Email + verification link only.** Works for every email system, but puts
  email deliverability on the critical path and routes personal data through US email
  infrastructure, conflicting with the residency claim. Rejected.
- **Option B — Google only.** Smallest build, but AU/NZ engineering firms are
  predominantly Microsoft shops — high risk of locking out the exact users the kill
  metric counts. Rejected.
- **Option C — Google + Microsoft, no password, no fallback (CHOSEN).** Covers both
  dominant work-email ecosystems; no email infrastructure; no residency wrinkle;
  verification inherited from the identity providers.
- **Option D — Google + Microsoft + email fallback.** Nobody locked out, but the most
  build, email work lands on the critical path "just in case", reopens the residency
  wrinkle, and the fallback is weakest-link verification. Rejected.
- **Hosted identity provider (any option's implementation variant).** Rejected: Tier-1
  trust-boundary expansion, recurring cost, US-processing residency wrinkle — only
  arguable on a 2+ year horizon, so deferred under the Surviving-the-Round rule.

## Decision Rationale

- **Inversion:** launch fails on a partner locked out of login, not on a missing fourth
  sign-in method. Cover the two ecosystems the partners actually use; build nothing
  speculative.
- **Last responsible moment:** the email fallback is a known, bounded retrofit costing
  days; building it now costs critical-path weeks plus a residency carve-out decided
  under no real pressure. Deferring it until a real, named user is blocked converts an
  upfront cost into a contingent one with a pre-agreed trigger.
- **Margin of safety on the kill metric:** allow-but-flag for personal domains keeps a
  real sole practitioner out of the "turned away" column without letting a
  metric-definition dispute contaminate a future kill decision.

## Consequences

**Positive**

- No email-sending infrastructure, no sender-reputation DNS work, and no residency
  carve-out at launch; the Australia claim stays clean.
- Both registrations are free and same-day on our side; quota and identity arrive
  together inside the launch runway.
- The retrofit path is pre-agreed, so a blocked partner produces a planned response,
  not an emergency design session.

**Negative / accepted costs**

- A partner firm on on-premise email, or with a hostile consent policy, cannot sign up
  until the fallback ships — accepted, with the partner survey as the early-warning
  mechanism and partner-side IT approval as the longest uncontrolled lead time.
- Two OAuth app registrations are manual, console-maintained artifacts outside
  Terraform — documented with rollback entries under the
  [ADR-020](adr-020-infrastructure-as-code-terraform-gcp.md) exception process.
- Dependence on two external identity providers' availability for all sign-ins; no
  degraded-mode login exists at launch.
- Flagged personal-domain users consume quota and support attention while contributing
  nothing to the kill metric — accepted as the cost of not turning away sole
  practitioners.

## References

- [ADR-020 — Infrastructure as Code with Terraform for GCP](adr-020-infrastructure-as-code-terraform-gcp.md)
- [ADR-024 — Django Web Stack, Server-Rendered Frontend, Single Service](adr-024-django-web-stack-single-service.md)
- OpenID Connect Core 1.0 (openid.net/specs/openid-connect-core-1_0.html)
- Google OAuth sensitive-scope verification documentation
  (developers.google.com/identity/protocols/oauth2/production-readiness/sensitive-scope-verification)
- Internal documents informing this decision (named by concept): the strategic-bets
  record (kill-metric definition), and the round-3 sign-in review in the stack-interview
  working notes (ephemeral; substance captured inline above).
