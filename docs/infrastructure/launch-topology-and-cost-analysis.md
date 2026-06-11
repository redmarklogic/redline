# Launch Topology and Cost Analysis

**Author**: Brent (DevOps)
**Date**: 2026-06-11
**Relates to**: issue #78 (Part B), issue #48b, ADR-020, ADR-022, ADR-023; carries follow-ups into #74, #75, #76, #77
**Status**: Decisions ratified by founder interview 2026-06-11 (three rounds). This document is the infrastructure record of those decisions. Peter is authoring the stack Architecture Decision Record (ADR) in parallel; where this document says "the stack ADR", read his forthcoming record on the Django + HTMX technology decision. This document records infrastructure consequences only — it does not amend the ADR namespace.

> **Plain-language glossary** (used throughout):
> - **Cloud Run** — Google's service that runs our app in a container and bills only while it is working.
> - **Cloud SQL** — Google's managed database service; unlike the app, it bills around the clock.
> - **LB (Load Balancer)** — the single public "front door" carrying the company domain and the HTTPS certificate.
> - **DNS (Domain Name System)** — the global address book mapping our domain name to our servers; changes take 24–48 hours to propagate worldwide.
> - **IAP (Identity-Aware Proxy)** — Google's login gate placed in front of a web service.
> - **OAuth** — the standard that lets a user sign in with an existing Google or Microsoft account instead of a new password.
> - **SA (Service Account)** — the identity a service runs as; determines what it may touch.
> - **Tier-1** — any infrastructure change that expands the trust boundary; requires documented Peter consultation before I provision anything.
> - **GCS (Google Cloud Storage)** — Google's file/blob storage service ("buckets").

---

## 1. Topology decision

**Decided: Topology A — one single Cloud Run service runs the whole app** (Django pages + document endpoint + admin), as a staging/prod pair per ADR-023. The existing Terraform services `staging-redline-api` / `prod-redline-api` (`deploy/infra/terraform/cloud_run.tf`) carry the new stack unchanged in shape — **zero new Cloud Run services**.

The #77 marketing site is a **separate static bucket** behind the same load balancer. It is genuinely static (Jekyll-generated files) and is *not* evidence for a "static frontend" topology: the app's pages are rendered fresh per request by Django + HTMX, which a bucket cannot do.

### Rejected alternatives (A/B/C analysis with costs)

Ballpark USD/month, Sydney (`australia-southeast1`), MVP traffic, staging+prod pairs included:

| Dimension | **A: single service (CHOSEN)** | **B: two services (Django + FastAPI) — REJECTED** | **C: API container + static frontend bucket — NOT AVAILABLE** |
|---|---|---|---|
| What it means | One container does everything | Two apps talk to each other over the network | One container does the API; app pages are plain files in a bucket |
| Cloud Run compute | ~$0–5 sleeping; ~$15–40 warm prod | Double A: ~$0–10 / ~$30–80 warm | Same as A (+~$0.10–1 bucket) |
| Load balancer (#74) | ~$20–30 flat | ~$20–30 flat | ~$20–30 flat |
| **Total ballpark** | **~$25–70/mo** (pre-database) | **~$50–110/mo** | **~$25–70/mo** |
| CI/CD surfaces | 1 pipeline (×2 envs) | 2 pipelines, 2 image repos, coordinated releases | 1 pipeline + trivial file copy |
| Service accounts / secrets | 1 SA; current secrets map as-is | 2 SAs; per-secret bindings double; service-to-service token config | 1 SA; statics need zero secrets |
| Tier-1 triggers | None new | **Two** (internal trust boundary; second secret-reading identity) | One borderline (public bucket egress path) |
| New failure modes | None | Network partition, token expiry/clock skew, version skew between apps | Cache staleness (minor) |

**Why B was rejected:** roughly double cost and operational load; fires two Tier-1 triggers; and it is the only hard-to-reverse option on the table — splitting a monolith later (A→B) is routine, but merging two services with an auth contract back into one (B→A) is a re-architecture. We chose the reversible branch.

**Why C was unavailable:** C requires a static app frontend. The decided stack (Django + HTMX, server-rendered per request) has no static frontend artifact — under that stack, C collapses to A. C would only have existed under a FastAPI-headless stack, which failed the Bet-1 sign-in/quota criterion.

**Standing rule (agreed with Peter):** topology is a decision, not a by-product of the first Dockerfile. Any future second deploy surface is a **stop-and-ADR event**, not a sprint task.

**If we had skipped this:** topology would have been decided implicitly by whoever wrote the first frontend Dockerfile, with the cost and Tier-1 consequences discovered after the fact.

---

## 2. Cost model and budget controls

### Decided steady-state cost picture (single-service Django stack)

| Item | Monthly cost (USD) | Notes |
|---|---|---|
| App compute (Cloud Run, staging + prod) | ~$0–5 sleeping / ~$15–40 warm prod | See cold-start policy, section 4 |
| Database (Cloud SQL, **smallest tier — confirmed on launch path**) | ~$12–35 | Bills 24/7 — databases do not scale to zero. Holds users, quotas, Django admin data, and the append-only audit log (parameters + hash) |
| Front door (load balancer + domain + certificate, #74/#75) | ~$20–30 flat | On critical path per the domain decision, section 5 |
| Storage, logging, secrets, registry | ~$1–5 | Rounding noise at our scale |
| **Steady-state total** | **~$40–75/mo** (up to ~$110 with warm prod + front door) | Inside the decided ceiling |

### Decided budget control numbers (founder-ratified, round 2)

| Control | Number | What it does |
|---|---|---|
| Design ceiling | **$100/mo** | The envelope I design within; any proposal exceeding it goes back to the founder first |
| Billing alert | **$80/mo** | Alarm fires while there is still room to react — deliberately below the ceiling (an alert *at* the ceiling is a notification of failure, not a control) |
| Hard stop-and-talk | **$150/mo** | Triggers the runaway-bill safeguard and a founder conversation |

These numbers feed the **runaway-bill safeguard** (a "denial-of-wallet" control: budget alert → Pub/Sub message → small function that caps how many app copies may spin up). The safeguard is a standing prerequisite before any production traffic — it is wired to these founder-named numbers, not to numbers I invented.

**If we skip wiring these:** the first surprise bill is the founder's problem instead of a designed control with the founder's name on the threshold.

### No GCS blob storage at launch (ratified)

Generated documents are **not** stored; the audit trail is an append-only log in Cloud SQL (request parameters + content hash). Consequence for infrastructure: the Cloud Storage bucket, signed-URL policy, retention policy, and access-log sink all **drop off the launch path** (deferred to the Pre-Review sprint). Smaller launch surface, smaller residency surface, fewer SOC 2 (security audit) controls to evidence at launch. My standing "DOCX via Cloud Storage" outcome is deferred accordingly. (The #77 marketing bucket is unrelated — public website files only, no user data.)

---

## 3. Tier-1 trigger ledger

Record of which trust-boundary gates fired during this decision cycle, and why the ones that did not fire, did not.

| Item | Tier-1? | Disposition |
|---|---|---|
| Topology A (single service) | **No** | Public HTTPS ingress already approved (ADR-022). Adding the load balancer + login gate (#74/#76) changes the *gate*, not the boundary — covered by the successor auth ADR work |
| Topology B (two services) | **Would have fired twice** | (1) New internal trust boundary — service-to-service authentication, a new identity-to-identity relationship; (2) a second service account able to read production secrets. Rejected, so neither fires |
| #77 marketing bucket | **Borderline, recorded** | New public-content egress path on the load balancer. Low risk (public-by-design website files, no user data). Recorded in the ADR trail rather than provisioned silently |
| Cloud SQL on launch path | **No new trigger** | Private resource inside the existing project boundary; connection strategy analysis already on file (`cloud-run-connection-strategy.md` — VPC connector trigger condition now met; Peter finalises the connection-strategy ADR before production traffic hits the database) |
| Hosted identity provider (Auth0 / GCP Identity Platform) | **Would have fired** | New external service holding our user identities + a residency wrinkle (US processing). Rejected in favour of self-hosted django-allauth — see next row |
| **django-allauth self-hosted (Google + Microsoft OAuth)** | **Does not fire — reasoned, not assumed** | The Tier-1 rule gates *GCP service provisioning* that expands the trust boundary, adds egress paths, or adds new IAM principal types. Option C (two sign-in buttons) adds **no new GCP service** (a Google OAuth client configuration is not a service; the Microsoft registration lives outside GCP entirely), **no new GCP IAM principal type** (end users authenticate to Django/allauth, not to Google's IAM), and the only egress is standard outbound HTTPS token exchange — no new path carrying our data out. Architecturally we *do* extend trust to two external identity providers, but the rule's purpose is "documented Peter consultation before the boundary moves" — and Peter is authoring the ADR that moves it. Consultation satisfied by construction; recorded here as the documentation trail |
| Transactional email provider (rejected sign-in fallback) | **Would have fired** | Mainstream providers route mail through US infrastructure — direct conflict with the Australia residency promise (section 8). Kept off the launch path; pre-agreed retrofit trigger: any named partner blocked at sign-in |

---

## 4. Cold-start policy and the demo-warm flip

**Decided (round 2):** sleep by default everywhere; flip production warm before scheduled demos.

**Plain English:** when nobody is using the app, it sleeps and costs nothing; the first visitor after a quiet period waits ~2–5 seconds while it wakes (a "cold start"). Keeping one copy always awake costs ~$15–40/mo. We pay for warmth only when humans we care about are watching. Note the database does **not** sleep — scale-to-zero saves the app's compute cost only.

| Environment | Default | Demo mode |
|---|---|---|
| Staging | Always sleeps (min instances 0) | Never warmed — staging warmth benefits no customer |
| Production | Sleeps (min instances 0) | 1 warm instance, flipped before a scheduled demo, flipped back after |

### The flip procedure (one-line Terraform change)

1. In `deploy/infra/terraform/terraform.tfvars`, set `min_instances_prod = 1` (demo) or `0` (default).
2. Run `terraform plan` — confirm the only diff is the prod service's minimum instance count.
3. `terraform apply` via the normal review path. Reverse with the same one-line change after the demo.

Rollback is the same edit in reverse; no data or traffic impact either direction.

> **⚠ Discrepancy found — must be fixed before the decided default is real.** Current Terraform does **not** match the ratified decision: `variables.tf` defaults `min_instances_prod = 1` (warm) and its validation block **forbids zero** (`min_instances_prod >= 1 && <= 5`). As wired today, production is always-warm and the decided scale-to-zero default cannot even be expressed. Required change (founder-reviewed, not yet applied): relax validation to `>= 0 && <= 5` and set the default to `0`. Until then we are silently paying for warmth the founder decided not to buy.

**If we skip the fix:** ~$15–40/mo of undecided spend continues, and the "one-line flip" promise is false in the direction that matters.

---

## 5. Domain and DNS sequencing

**Decided (round 2):** one shared company domain at launch — marketing site at the apex (`ourdomain.com`), app at a subdomain (`app.ourdomain.com`), one load balancer fronting both. This pulls **#74 (load balancer) and #75 (DNS + TLS certificate) onto the critical path now.**

**The immovable constraint:** DNS propagation — the worldwide address-book update — takes **24–48 hours** and cannot be accelerated. Sequencing is designed so that wait happens early and once:

| Step | What | Lead time | Depends on |
|---|---|---|---|
| 1 | Reserve static IP address; provision load balancer + certificate (#74/#75, Terraform) | Hours of work; certificate issues only after DNS points at us | — |
| 2 | Create DNS records: apex → marketing bucket route, `app.` → Cloud Run route, **plus the Search Console TXT verification record (section 6) in the same change** | **24–48 h propagation** | Step 1 (needs the IP) |
| 3 | Google-managed certificate activates | Up to ~24 h after DNS resolves | Step 2 |
| 4 | Add `app.<domain>` redirect URIs to both OAuth registrations (2-minute edit, no re-approval) | Minutes | Step 3 |
| 5 | Login gate placement (#76) on the load balancer | — | Steps 1–3 |

**Plan rule:** steps 1–3 must complete **at least one week before launch**, not launch week. The DNS wait is free if scheduled early and becomes the binding constraint if discovered late.

**If we skip the sequencing:** we discover the 24–48 hour lead time the week of launch, with the certificate and the OAuth redirect URIs queued behind it.

---

## 6. OAuth sign-in registrations — manual-step plan and rollback

**Decided (round 3, #48b):** sign-in is **Google + Microsoft OAuth buttons, no password, no email fallback** (django-allauth, self-hosted). Pre-agreed retrofit trigger: the moment any named partner is blocked (wrong ecosystem or their IT policy), we add the email-link fallback then — a bounded days-scale retrofit, deliberately not built speculatively now.

Q1a ratified: personal-domain emails (gmail.com / outlook.com) are **allowed but flagged** — usable, excluded from the 50-signup kill metric. Infrastructure consequence: the **Microsoft app registration uses the "organizational + personal Microsoft accounts" account type**, and the Google client does not filter to Workspace accounts.

### Why these are manual steps (ADR-020 honesty note)

OAuth consent screens and standard OAuth clients are largely **not manageable from Terraform** in the Google provider, and the Microsoft registration lives in Microsoft Entra — outside GCP entirely (adding a whole second Terraform provider for one resource fails our own toolchain test). Both registrations are therefore **documented manual steps under ADR-020's exception process**: each gets an entry in `docs/infrastructure/manual-steps-to-terraform.md` with its rollback procedure **at the time I perform it** (not yet performed — this document is the plan).

### Registration plan

| Step | Detail | Lead time |
|---|---|---|
| G1 | Google: configure OAuth consent screen, publish to production status. Sign-in-only scopes (`openid`, `email`, `profile`) are classified **non-sensitive — no Google verification review required**; same-day | Same day |
| G2 | Google: consent screen requires the company domain in its **authorized domains** list → needs one-time domain-ownership verification (Search Console) → one DNS TXT record → **folded into the #74/#75 DNS change** (section 5, step 2) | Rides the 24–48 h DNS window |
| G3 | Google: consent screen requires a **privacy-policy URL and home-page URL** on the domain → page on the #77 marketing site (Mark/John own content; dependency flagged) | Blocks G1 completion |
| G4 | Create Google OAuth client; register redirect URIs against the **stable `*.run.app` URLs now** (`staging-redline-api` / `prod-redline-api`); add `app.<domain>` URI post-#74/#75 (both providers accept multiple URIs — 2-minute edit, no re-approval) | Same day |
| M1 | Microsoft: Entra ID app registration — instant, free, account type "organizational + personal" per Q1a | Same day |
| M2 | **Partner-side risk (longest uncontrolled lead time):** conservative firms often require their IT department's admin consent for third-party sign-in apps — days to weeks, outside our control. Mitigation is the founder's outstanding homework: walk the ten partner firms, ask (1) M365 / Google Workspace / other? (2) does IT block third-party sign-in apps? Blocked firms should start internal approval **now** | Days–weeks, partner-side |

### Rollback notes (per registration)

- **Google:** delete the OAuth client ID in the Cloud Console credentials page; revert the consent screen to testing status. No user data is held in the registration itself. Remove the two Secret Manager entries via Terraform (`secret_bindings` map edit + `terraform apply`).
- **Microsoft:** delete the Entra app registration (this invalidates all issued tokens for our app). Remove the corresponding Secret Manager entries the same way.
- **DNS TXT record (Search Console):** delete the TXT record; verification lapses harmlessly.
- Each rollback is recorded alongside its forward step in `manual-steps-to-terraform.md` when executed.

---

## 7. Secret distribution

The two OAuth client secrets follow the established ADR-023 pattern — **two one-line additions to the `secret_bindings` map** in `deploy/infra/terraform/secrets.tf` (the map is the single point of change; `cloud_run.tf` picks them up automatically for both environments):

```hcl
secret_bindings = {
  "db_password"             = "DB_PASSWORD"             # pragma: allowlist secret
  "api_key"                 = "API_KEY"                 # pragma: allowlist secret
  "google_oauth_secret"     = "GOOGLE_OAUTH_CLIENT_SECRET"   # pragma: allowlist secret  # name TBC vs Kabilan's settings.py
  "microsoft_oauth_secret"  = "MICROSOFT_OAUTH_CLIENT_SECRET" # pragma: allowlist secret  # name TBC vs Kabilan's settings.py
}
```

Rules carried forward unchanged: secrets reach the app **only via Secret Manager at runtime** (never literal environment values in service config); secret *values* are set out-of-band via `gcloud` per the existing pattern; environment-variable **names must be confirmed against Kabilan's Django settings before I provision** (my standing shape-mismatch obligation — django-allauth's expected names govern, not my guesses). A `DJANGO_SECRET_KEY` binding will also arrive when Kabilan requests it — same one-line pattern.

Both new secrets are created **already Sydney-pinned** (section 8) — no migration needed for them.

---

## 8. Residency pin — scope

**Decided:** the "all customer data stays in Australia" promise is approved, and with it the technical pin.

| Item | Current state | Decided state |
|---|---|---|
| Secret Manager replication (`secrets.tf`) | `auto {}` — Google may replicate secret material to any region worldwide | `user_managed` pinned to `australia-southeast1` (Sydney). **Note:** changing replication on an existing secret is not an in-place update — existing secrets are replaced (new secret + re-add value via `gcloud` + old one destroyed). Founder-reviewed `terraform plan` will show this explicitly |
| Cloud Run, Artifact Registry | Already `australia-southeast1` | No change (standing region constraint) |
| Cloud SQL (when provisioned) | — | Created in `australia-southeast1` from day one |
| OAuth client secrets (new) | — | Created already-pinned; never exist unpinned |
| Blob storage | None at launch | Pin applies if/when the Pre-Review-sprint bucket arrives |

**Scope honesty for the promise:** the pin covers data *at rest in our infrastructure*. Sign-in token exchange necessarily transits Google's and Microsoft's identity services (that is how "Sign in with Google/Microsoft" works for every product); and keeping transactional email off the launch path (section 3, last row) is precisely what keeps the promise clean — an email fallback through a mainstream US-routed provider would have broken it. If the retrofit trigger ever fires, the choice at that moment is an Australian-region email provider or a Mark-coordinated wording carve-out. **External-facing wording of the promise goes through Peter's sign-off per my standing external-communications gate.**

---

## 9. Carry-out checklist

Concrete follow-ups, one row per item. Nothing here is applied yet — every Terraform item goes through founder-reviewed `terraform plan` first.

| # | Item | Where | Trigger / sequencing | Owner |
|---|---|---|---|---|
| 1 | Load balancer + static IP + certificate; **fold the Search Console TXT record into the same DNS change** | #74 / #75 | Start now — 24–48 h DNS lead; complete ≥1 week pre-launch | Brent |
| 2 | Login-gate placement on the load balancer (single service simplifies it: one backend, one gate; #77 bucket rides the same gate decision) | #76 | After #74/#75; aligned with successor auth ADR | Brent (GCP side) |
| 3 | Privacy-policy + home-page URL on marketing site — **blocks Google consent-screen production status** | #77 | Flagged to Mark/John; needed before G1 completes | Mark / John |
| 4 | `secrets.tf`: replication `auto` → `user_managed` Sydney pin (existing secrets replaced — values re-added via `gcloud`) | `deploy/infra/terraform/secrets.tf` | Before any real user secret lands; before OAuth secrets created | Brent |
| 5 | `secrets.tf`: two `secret_bindings` entries for OAuth client secrets (+ `DJANGO_SECRET_KEY` on Kabilan's request) — env-var names confirmed against Django settings first | `deploy/infra/terraform/secrets.tf` | With Kabilan's allauth work | Brent (names: Kabilan confirms) |
| 6 | `.env.example` delta: add annotated entries for `GOOGLE_OAUTH_CLIENT_SECRET`, `MICROSOFT_OAUTH_CLIENT_SECRET`, `DJANGO_SECRET_KEY`, database connection values — typed, annotated (format / source service / prefix), names per Kabilan. Current file holds only SonarQube/Context7 tooling entries — the app-infra contract section does not exist yet | `.env.example` | Before Kabilan is unblocked on allauth/DB work | Brent |
| 7 | **Fix `variables.tf` to allow the decided scale-to-zero default** (validation `>= 0`; default `min_instances_prod = 0`) — see section 4 discrepancy | `deploy/infra/terraform/variables.tf` | Next Terraform change; currently paying for undecided warmth | Brent |
| 8 | Wire budget controls: $80 alert / $100 ceiling / $150 hard stop → runaway-bill safeguard (budget → Pub/Sub → instance-cap function) | New Terraform (billing budget et al.) | **Prerequisite before any production traffic** | Brent |
| 9 | Cloud SQL smallest-tier provisioning (Sydney, backups + point-in-time recovery) + VPC connector (trigger condition in `cloud-run-connection-strategy.md` now met) + schema contract to Kabilan | `deploy/infra/terraform/` | After Peter finalises the connection-strategy ADR | Brent (ADR: Peter) |
| 10 | OAuth registrations (Google + Microsoft) as documented manual steps with rollback entries, per section 6 plan | `docs/infrastructure/manual-steps-to-terraform.md` (at execution time) | G3 (privacy page) and G2 (TXT) gate Google; Microsoft any time; Q1a account-type setting locked in | Brent |
| 11 | Founder homework: walk ten partner firms — email ecosystem + IT third-party-app policy; blocked firms start internal approval ASAP (longest uncontrolled lead time) | — | This week | Founder |
| 12 | Update `cloud-run-connection-strategy.md` "Outbound Connections: none" section when Cloud SQL + OAuth token exchange land (its own rule requires this) | `docs/infrastructure/cloud-run-connection-strategy.md` | With items 9 / 10 | Brent |

---

*Cross-references: Peter's forthcoming stack ADR (Django + HTMX decision and layer-responsibility table) is the architectural decision of record; this document is its infrastructure companion, the same relationship `cloud-run-connection-strategy.md` holds to ADR-022.*
