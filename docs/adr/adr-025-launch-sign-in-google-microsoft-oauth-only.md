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
