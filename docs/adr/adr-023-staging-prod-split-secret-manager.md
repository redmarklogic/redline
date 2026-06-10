# ADR-023: Staging/Production Split with Secret Manager Bindings

## Summary

Redline runs two Cloud Run services — staging and production — in a single GCP (Google
Cloud Platform) project, isolated by separate services and separate Secret Manager
secrets named per the `{env}-redline-{credential}` convention, with all secret-to-env-var
bindings declared in one shared locals map in the Terraform configuration. This ADR is
Accepted and partially supersedes ADR-022: only ADR-022's scope statements about a
single environment and the absence of Secret Manager are replaced; the hosting decision
itself (Cloud Run + Artifact Registry, australia-southeast1, throttled CPU, 300 s
timeout, Tier-1 public-ingress approval) stands unchanged. The single most important
constraint this ADR imposes: secrets are strictly per-environment — no secret is ever
shared between staging and production, and adding a credential is a one-entry change to
the shared bindings map.

## Decision

1. **Two environments in one project.** Staging and production are separate Cloud Run
   v2 services (named `staging-redline-api` and `prod-redline-api`) within the single
   existing GCP project. No per-environment GCP projects.

2. **Secret Manager naming convention.** Every credential exists once per environment
   as a Secret Manager secret named `{env}-redline-{credential}` (e.g.
   `prod-redline-db_password`). Terraform provisions the secret shells only; secret
   *versions* (the actual values) are managed out-of-band via the gcloud CLI and never
   enter Terraform state.

3. **Single shared bindings map.** The mapping from credential key to container
   environment-variable name (e.g. `db_password` → `DB_PASSWORD`) is declared exactly
   once, in a shared Terraform locals block consumed by both environments. Cloud Run
   containers receive secrets as environment variables via secret key references
   resolving the `latest` version. Adding a new secret is a one-entry change to this
   map; no other declaration changes.

4. **Instance scaling.** Production: minimum instances ≥ 1 (validated range 1–5,
   default 1) — this enacts the "set min-instances to 1 before production launch" plan
   recorded in ADR-022 and eliminates production cold starts. Staging: minimum 0
   (scales to zero). Maximum instance caps: production 10, staging 3 (defaults,
   validated ≥ 1).

5. **Startup probe, explicit.** Each service declares an explicit startup probe:
   initial delay 10 s, timeout 5 s, failure threshold 3, HTTP GET against the
   application health endpoint on port 8080. No liveness probe is declared — this is
   intentional, not an omission.

6. **Deletion protection disabled, explicitly.** `deletion_protection = false` is set
   explicitly on both services. The Google Terraform provider 6.x changed the default
   to true; left implicit, that default would block environment teardown. Phase 1
   architecture is explicitly disposable — the environments must remain destroyable in
   a single Terraform operation. This setting is revisited before paying customers
   depend on the production service.

## Status

Accepted, partially supersedes ADR-022 (scope statements only — the hosting decision stands) — 2026-06-11

## Context

ADR-022 recorded the hosting decision for the walking-skeleton deploy chain and
explicitly scoped *out* the multi-environment split and Secret Manager entries, stating
"single environment (prod) now" and "No Secret Manager provisioning needed at this
stage — `APP_ENV` is the only runtime environment variable." ADR-022's own Ongoing
consequence mandated that any multi-environment split "requires a new or amended ADR."

In the same deploy week, the staging/production deployment specification shipped: the
Terraform configuration now provisions both environments with Secret Manager bindings.
Three statements in ADR-022 thereby became actively misleading to any agent grounding
on the ADR graph. Because accepted ADRs are immutable (amendment of the body is
prohibited), and because full supersession would wrongly discard ADR-022's still-valid
hosting decisions, the correct instrument is a new ADR that supersedes only the
out-of-scope statements. This ADR is that instrument, owed by ADR-022's own terms.

**Superseded statements in ADR-022** (everything else in ADR-022 stands):

- Out of Scope item "Multi-environment split — single environment (prod) now".
- Out of Scope item "Secret Manager entries — no secrets at this stage".
- The Context statement that no Secret Manager entries are needed and that `APP_ENV`
  is the only runtime environment variable.
- The Consequences statement "No Secret Manager provisioning needed at this stage."
- Decision point 4 (min-instances 0, deferred to "before production") — now enacted
  and replaced by Decision 4 above.

## Options Considered

- **Two Cloud Run services in one GCP project (selected).** Isolation via separate
  services, separate service-scoped secrets, separate URLs.
- **Separate GCP projects per environment.** Stronger blast-radius isolation, but
  duplicate IAM, billing, and API-enablement overhead — unjustified at solo-founder
  scale and pre-launch stage.
- **Single service with an environment switch.** No isolation; staging deploys would
  risk production traffic and share secrets. Rejected outright.
- **Secret versions managed in Terraform.** Rejected: secret values would enter
  Terraform state, expanding the secret-exposure surface.
- **Per-environment duplicated binding declarations.** Rejected: two declarations of
  the same credential map drift independently; a single shared map is the
  single-source-of-truth form (per ADR-001).

## Decision Rationale

The short-runway test decides this. Two services in one project deliver the only
isolation property that matters now — a staging deploy cannot touch production traffic
or production credentials — at zero additional standing cost (staging scales to zero).
Per-environment projects are justified only under a long-runway assumption (compliance
evidence, team growth) and are deferred. The shared bindings map keeps the
secret-injection contract in one place, which is what makes constraint testing possible
(a secret existing in one environment but not the other is a detectable drift, not a
silent divergence). The naming convention `{env}-redline-{credential}` makes
environment membership inspectable from the secret ID alone. Disabling deletion
protection is a deliberate trade: Phase 1 optimises for learning velocity and
disposability over durability, and an explicit setting survives provider-default
changes where an implicit one does not.

## Consequences

**Positive:**

- Agents grounding on the ADR graph now read an accurate description of the shipped
  topology; the misleading ADR-022 scope statements are formally retired.
- Adding a credential is a one-line map change, provisioned identically in both
  environments — no drift path.
- Production cold starts are eliminated (min instances 1, at the ~$15–20/month cost
  ADR-022 already anticipated).
- Staging remains free at idle (scales to zero).

**Negative / accepted risks:**

- Single-project blast radius: a project-level IAM or billing failure affects both
  environments. Accepted for Phase 1; revisit if compliance evidence demands project
  separation.
- Secret references resolve `latest`: a rotated secret takes effect on next instance
  start without an explicit version pin. Acceptable now; version pinning is a future
  hardening step.
- `deletion_protection = false` permits destruction of the production service by a
  Terraform operation. Accepted while the architecture is disposable; must be
  revisited before paying customers exist.

**Ongoing:**

- ADR-021 is unaffected: secrets still reach the application exclusively as process
  environment variables. ADR-022's remaining decisions (runtime, registry, region,
  CPU mode, timeout, concurrency, Tier-1 ingress approval) remain binding.
- Any move to per-environment GCP projects, secret version pinning, or enabling
  deletion protection requires a new ADR.

## References

- ADR-001 — Single Source of Truth (the shared bindings map is its application here).
- ADR-020 — Infrastructure as Code with Terraform for GCP (governs how these resources
  are declared; provider pinned to the 6.x series, which motivates Decision 6).
- ADR-021 — Process Environment as Sole Config Source (governs how the bound secrets
  reach the application).
- ADR-022 — Cloud Run + Artifact Registry Hosting (partially superseded by this ADR:
  scope statements only; the hosting decision stands).
