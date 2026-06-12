# Feature Specification: Tear Down Firebase API Front Door (ADR-027)

**Feature Branch**: `feature/147-tear-down-firebase-api-front-door-adr-027`

**Created**: 2026-06-12

**Status**: Draft

**Input**: GitHub issue [#147](https://github.com/redmarklogic/redline/issues/147) — "Tear down Firebase API front door (ADR-027)". Governing decision: ADR-027 (supersedes ADR-026).

## Overview

The branded API address (`api.redmarklogic.com`) is served through Firebase Hosting, which terminates every request at a hard 60-second platform ceiling. The product's core synchronous calls take three minutes or more, so every real call through that address is a guaranteed failure. ADR-027 decides to remove the Firebase front door and adopt the raw Cloud Run (`*.run.app`) address for the proof of concept. This change executes that decision: it destroys the five Firebase/DNS resources that form the front door, cleans up the accompanying configuration, preserves the irreversible and reusable pieces, and proves the founder's live email on the same domain is untouched.

The branded URL has never served a successful response (403 since creation, no public-invoker permission) and no consumer depends on it, so the blast radius is effectively zero. The `run.app` address is unaffected.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Remove the guaranteed-failure path before public access lands (Priority: P1)

As the infrastructure owner, the moment the public-access work (#114) is fixed, the advertised branded API address must not return a 504 timeout on every real call. The Firebase front door — site, custom domain, rewrite version, release, and the `api` CNAME — is removed so that no guaranteed-failure path is left live in production.

**Why this priority**: This is the entire purpose of the change. Leaving the front door live means a known-broken address becomes publicly reachable the instant #114 lands, plus dead infrastructure that confuses every future session.

**Independent Test**: After teardown, `nslookup api.redmarklogic.com` returns no CNAME (the branded address no longer resolves or serves TLS). The five target resources are absent from Terraform state. This alone delivers the value: the broken front door is gone.

**Acceptance Scenarios**:

1. **Given** the five Firebase/DNS resources exist in Terraform state, **When** the teardown is applied, **Then** `terraform plan` reports exactly five destroys and zero changes to any other resource.
2. **Given** the teardown has been applied, **When** `nslookup api.redmarklogic.com` is run, **Then** no `api` CNAME record is returned.
3. **Given** the teardown has been applied, **When** `terraform plan` is run again, **Then** the plan is clean with no drift.
4. **Given** the teardown has been applied, **When** `terraform output` is inspected, **Then** no `firebase_*` outputs remain.

### User Story 2 - Prove the founder's live email and the rest of the zone are untouched (Priority: P1)

As the domain owner, the founder's live email runs on `redmarklogic.com`. The DNS deletion (the single `api` CNAME) is the one exception to the additive-only DNS discipline, so every other zone record — MX, SPF/TXT, and all others — must be provably unchanged. A full zone snapshot is captured before any change and diffed against a post-change export.

**Why this priority**: Co-equal P1. An undetected collateral change to MX or SPF records would break the founder's email — a far worse outcome than the broken front door this change removes. The proof obligation is blocking.

**Independent Test**: A pre-change zone export and a post-change zone export are diffed; the diff shows exactly one record removed (the `api` CNAME) and zero other changes. A send/receive email test confirms the founder's mailbox still works.

**Acceptance Scenarios**:

1. **Given** no change has been made yet, **When** the teardown work begins, **Then** a full Cloudflare zone record export exists as a saved artifact attached to the change.
2. **Given** a pre-change snapshot exists, **When** the post-change zone export is diffed against it, **Then** exactly one record is removed (`api CNAME redmarklogic-api.web.app`, id `6b051d1e36a71373819c95a89d1db64d`) and every other record (MX, SPF/TXT, all others) is byte-for-byte identical.
3. **Given** the teardown has been applied, **When** the founder sends and receives a test email, **Then** both succeed.
4. **Given** the teardown is being executed, **When** any zone record beyond the single `api` CNAME would be touched, **Then** the work stops (stop-the-line event) and is not applied.

### User Story 3 - Preserve reusable and irreversible pieces; leave a clean, documented state (Priority: P2)

As a future session operator, the pieces that the Sprint-3 website will reuse, and the pieces that cannot be undone, must survive the teardown. The configuration left behind must be internally consistent: no dangling variables, outputs, or references to the removed front door, and documentation (runbook, manual-steps rollback entry, environment example) updated to reflect that the `run.app` address is now the POC API address.

**Why this priority**: P2 — the change is functionally complete after P1, but a half-cleaned state (orphaned variables, stale docs pointing at the dead branded URL) creates exactly the future-session confusion this change exists to prevent. The keep-list is also load-bearing: destroying a "keep" item (e.g. the Firebase project) would be irreversible or would break Sprint-3 reuse.

**Independent Test**: `terraform validate` passes after the HCL cleanup with no undefined-variable or dangling-reference errors; the kept resources remain in state; the runbook, manual-steps rollback entry, and environment example reflect the `run.app` address.

**Acceptance Scenarios**:

1. **Given** the HCL cleanup is complete, **When** Terraform configuration is validated, **Then** it validates with no references to the removed resources, the removed variable, or the removed outputs.
2. **Given** the teardown has been applied, **When** Terraform state is inspected, **Then** every keep-list item (Firebase project, cloudflare provider, zone data source, google-beta provider pin, Cloudflare API token secret) is still present.
3. **Given** the teardown is merged, **When** the DNS runbook and manual-steps document are read, **Then** the runbook reflects the removed front door and the manual-steps document contains a rollback entry for this teardown.
4. **Given** the teardown is merged, **When** the environment example is read, **Then** it declares the `run.app` URL as the working POC API base URL and no longer points to the branded API address.

### Edge Cases

- **Plan shows more or fewer than five destroys**: stop-the-line. The change is bounded to exactly five resource destructions; any deviation means the state or HCL diverged from the audited footprint and must be reconciled before applying.
- **Plan shows changes to a keep-list resource**: stop-the-line. The Firebase project, providers, zone data source, and the Cloudflare token secret must show zero changes.
- **Post-change zone diff shows any record other than the `api` CNAME changed**: stop-the-line; do not proceed, investigate the collateral change.
- **Firebase project destroy attempted**: must not happen — the provider implements no delete and the resource is intentionally retained. A plan that proposes destroying it is a defect in the HCL edits.
- **Rollback needed after teardown**: re-creation is possible at any time by reverting the change and re-applying, then the documented two-step DNS converge; certificate re-issuance can take up to 24 hours.

## Requirements *(mandatory)*

### Functional Requirements

**Destruction (exactly five resources, in dependency order):**

- **FR-001**: The change MUST destroy `google_firebase_hosting_release.api` (the live activation of the rewrite rule).
- **FR-002**: The change MUST destroy `google_firebase_hosting_version.api` (the `** -> prod-redline-api` rewrite rule).
- **FR-003**: The change MUST destroy `google_firebase_hosting_custom_domain.api` (`api.redmarklogic.com` attachment and its TLS certificate).
- **FR-004**: The change MUST destroy `google_firebase_hosting_site.api` (the `redmarklogic-api` hosting site).
- **FR-005**: The change MUST delete `cloudflare_dns_record.firebase_cname` (the `api CNAME redmarklogic-api.web.app` record, id `6b051d1e36a71373819c95a89d1db64d`) via Terraform destroy only — never via the Cloudflare dashboard (ADR-020).
- **FR-006**: The change MUST destroy exactly these five resources and no others. A plan proposing any additional destruction or any change to a non-target resource is a stop-the-line event.

**Configuration cleanup (same change set):**

- **FR-007**: The change MUST remove the destroyed resources' HCL blocks from `firebase_hosting.tf` (the site, custom domain, version, and release blocks) and the four `firebase_*` output blocks.
- **FR-008**: The change MUST remove the `cloudflare_dns_record.firebase_cname` block from `cloudflare_dns.tf`.
- **FR-009**: The change MUST remove the `firebase_cname_target` variable from `variables.tf` and its assigned value from `terraform.tfvars`.
- **FR-010**: The change MUST remove the Firebase Hosting configuration file `deploy/firebase/firebase.json` (ADR-027 D2: the rewrite intent no longer exists). *(Reconciliation note: required by ADR-027 D2; not enumerated in the issue body — see Assumptions.)*
- **FR-011**: The change MUST update the environment example so it declares the `run.app` URL as the POC API base URL and no longer references the branded `api.redmarklogic.com` address, if and only if the environment example currently references the branded URL.

**Retention (keep-list — must survive):**

- **FR-012**: The change MUST retain `google_firebase_project.default` in both Terraform state and HCL (it is irreversible, zero-cost, and reused by the Sprint-3 website). Its explanatory comment is kept; the file header is retitled per ADR-027.
- **FR-013**: The change MUST retain the `cloudflare` provider configuration and the `data.cloudflare_zone.redmarklogic` data source (all future DNS automation depends on them).
- **FR-014**: The change MUST retain the `google-beta` provider configuration in `versions.tf` (required by `google_firebase_project`; reused by Sprint-3 hosting).
- **FR-015**: The change MUST retain the Cloudflare API token in Secret Manager (`prod-redline-cloudflare-api-token`) and the Firebase Terms-of-Service acceptance.

**Safety gates and proof obligations:**

- **FR-016**: The change MUST NOT be planned or applied until ADR-027 is merged (front-door architecture is a decision, not an execution choice).
- **FR-017**: The change MUST capture a full Cloudflare zone record export as a saved artifact before any change is applied, and MUST attach it to the change for review.
- **FR-018**: The change MUST be applied only after a reviewer has inspected the `terraform plan` diff and confirmed it shows exactly five destroys and zero other changes.
- **FR-019**: After apply, the change MUST produce a post-change zone export and diff it against the pre-change snapshot, demonstrating exactly one record removed and zero other changes.
- **FR-020**: After apply, the founder MUST confirm email send/receive on `redmarklogic.com` still works.

**Documentation (same change set):**

- **FR-021**: The change MUST update `docs/infrastructure/domain-dns-runbook.md` to reflect the removed front door.
- **FR-022**: The change MUST add a rollback entry to `docs/infrastructure/manual-steps-to-terraform.md` for this teardown.

### Key Entities

- **Firebase API front door**: the composite of the hosting site (`redmarklogic-api`), the custom domain attachment (`api.redmarklogic.com` + TLS cert), the rewrite version (`** -> prod-redline-api`), the release that activates it, and the `api` CNAME DNS record. The unit being destroyed.
- **Cloudflare zone (`redmarklogic.com`)**: the DNS zone carrying the founder's live email records (MX, SPF/TXT) alongside the single `api` CNAME being removed. The protected entity — only one of its records may change.
- **Keep-list**: the Firebase project enablement, the Cloudflare provider + zone data source, the google-beta provider pin, and the Cloudflare API token secret. Pieces that are irreversible and/or reused by Sprint-3; must survive.
- **Zone snapshot pair**: the pre-change and post-change full zone exports whose diff is the evidence that collateral damage did not occur.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After apply, a re-run `terraform plan` is clean — zero drift.
- **SC-002**: The branded address is gone — `nslookup api.redmarklogic.com` returns no CNAME (the address no longer resolves or serves TLS).
- **SC-003**: The `run.app` address is unaffected — a health check against the Cloud Run service URL returns the same status code as before teardown (403 expected until #114 lands; that is a separate, known issue).
- **SC-004**: The post-change zone export diffed against the pre-change snapshot shows exactly one record removed (the `api` CNAME) and zero other changes — MX, SPF/TXT, and every other record identical.
- **SC-005**: The founder confirms email send and receive on `redmarklogic.com` after the change.
- **SC-006**: No `firebase_*` outputs remain in `terraform output`.
- **SC-007**: Terraform configuration validates after cleanup with no dangling references to the removed resources, variable, or outputs.
- **SC-008**: Rollback is demonstrably available — reverting the change and re-applying re-creates the front door (certificate re-issuance budgeted up to 24 h, within the 48 h SC budget).

## Assumptions

- **Primary authority**: Issue #147 is the primary authority for execution ordering, safety gates, and the verification checklist. ADR-027 is the primary authority for architectural scope (what is torn down vs. kept). Where they differ, the resolution is recorded below.
- **`firebase.json` removal (reconciliation resolution)**: ADR-027 D2 explicitly lists `deploy/firebase/firebase.json` for removal; the issue #147 destroy/cleanup tables omit it. ADR-027 governs scope, so the file is in scope for this change (FR-010). The empty `deploy/firebase/public/.gitkeep` placeholder and the `deploy/firebase/` directory are removed with it if doing so leaves no other consumer; this is left to plan-stage judgement.
- **Environment example scope**: FR-011 resolved during analysis — only root `.env.example` references the branded URL (a `FIREBASE_CNAME_TARGET` var block, lines ~69–74); `deploy/docker/marker/.env.example` does not. Root file is edited; the marker file is untouched.
- **run.app health baseline**: SC-003 compares post-teardown to a pre-teardown baseline; that baseline status code is captured in Phase 0 (task T002b) before any change, since run.app returns 403 until #114 lands.
- **ADR-027 is merged** before any `terraform plan`/`apply` is run (FR-016). This change produces the spec/plan/tasks artifacts regardless; the gate binds only the execution (apply), which is out of this spec-kit phase's scope.
- **Cloud Run `run.app` URL hash**: the exact service URL hash for the health-check verification (SC-003) is read from the live Cloud Run service at execution time, not hard-coded here.
- **Zone snapshot location**: the pre/post zone exports are saved under `docs/infrastructure/` or attached to the change for review; exact path is a plan-stage detail.
- **DNS deletion mechanism**: the `api` CNAME is removed only through Terraform destroy, never the Cloudflare dashboard (ADR-020). This is the single sanctioned exception to the otherwise additive-only DNS discipline.
- **Rollback recoverability**: nothing destroyed by this change is unrecoverable; the only irreversible piece (Firebase project enablement) is intentionally retained.

## Dependencies

- **ADR-027 merged** (blocking gate for execution; see FR-016).
- **Pre-change Cloudflare zone snapshot** (blocking gate; FR-017).
- Cloudflare API token in Secret Manager (`prod-redline-cloudflare-api-token`) available to the operator for the zone export and Terraform run.
- Existing Terraform state containing the five target resources.
- Reference: ADR-027 (`docs/adr/adr-027-raw-run-app-poc-front-door.md`), `docs/infrastructure/domain-dns-runbook.md`, `docs/infrastructure/manual-steps-to-terraform.md` (Entries 002, 004), issues #114, #79, #111.
