# Tasks: Tear Down Firebase API Front Door (ADR-027)

**Input**: [plan.md](./plan.md)
**Prerequisites**: ADR-027 merged to master (blocking gate, FR-016); operator has `CLOUDFLARE_API_TOKEN` (from `prod-redline-cloudflare-api-token`) and GCP ADC for `terraform plan`/`apply`.

<!-- Sizing: each task is a vertical slice of the teardown. TDD/pytest gates do not
     apply — there is no Python under test. Each phase's gate is a Terraform/DNS
     verification, substituted per plan.md. -->

> **Hard execution gate**: No `terraform plan`/`apply` runs until ADR-027 is merged.
> Phase 1 HCL edits may be authored on the branch beforehand, but Phase 0's gate
> blocks the plan/apply steps.

## Phase 0: Gate verification + pre-change zone snapshot

**Purpose**: Establish the two blocking preconditions; capture the evidence baseline that protects the founder's email.

- [x] T001 [Phase 0] Confirm ADR-027 is merged on master (`git log master` / `gh`); record the merge commit in the PR description. (FR-016) — DONE: merged at commit `1bdab47` on master (2026-06-12).
- [ ] T002 [P] [Phase 0] Export the full `redmarklogic.com` Cloudflare zone record list (all records: MX, SPF/TXT, the `api` CNAME, everything) and save it as the pre-change snapshot under `docs/infrastructure/` (or attach to the PR). (FR-017) — **BLOCKED on `gcloud auth login` (stale ADC reauth).** Capture script ready: `docs/infrastructure/zone-snapshots/capture-zone-snapshot.sh pre`.
- [ ] T002b [P] [Phase 0] Capture the run.app `/health` status-code baseline BEFORE teardown: `curl -s -o NUL -w "%{http_code}" https://<run.app-url>/health` — record the value (403 expected until #114) so T015 has something concrete to compare against. (baseline for SC-003) — **BLOCKED on same auth gate** (run.app URL read needs gcloud).

### Acceptance Gate

- [ ] T003 [Phase 0] Verify ADR-027 merged AND the pre-change zone snapshot is saved (contains the founder's MX/SPF records and the `api` CNAME) AND the run.app baseline status code is recorded. Stop if any is missing. — PARTIAL: ADR-027 merge confirmed (T001); snapshot + baseline blocked on auth.

---

## Phase 1: HCL teardown edits

**Purpose**: Remove the five resources' HCL plus accompanying config so the next plan proposes exactly five destroys and nothing else.

- [x] T004 [Phase 1] In `deploy/infra/terraform/firebase_hosting.tf`: delete the `google_firebase_hosting_site.api`, `google_firebase_hosting_custom_domain.api`, `google_firebase_hosting_version.api`, and `google_firebase_hosting_release.api` blocks, and the four `firebase_*` output blocks. KEEP `google_firebase_project.default` and its comment; retitle the file header per ADR-027. (FR-001–004, FR-007, FR-012) — DONE.
- [x] T005 [P] [Phase 1] In `deploy/infra/terraform/cloudflare_dns.tf`: delete the `cloudflare_dns_record.firebase_cname` block. KEEP the `cloudflare` provider and `data.cloudflare_zone.redmarklogic`. (FR-005, FR-008, FR-013) — DONE.
- [x] T006 [P] [Phase 1] In `deploy/infra/terraform/variables.tf`: delete the `variable "firebase_cname_target"` block. (FR-009) — DONE.
- [x] T007 [P] [Phase 1] In `deploy/infra/terraform/terraform.tfvars`: delete the `firebase_cname_target = "redmarklogic-api.web.app"` line. (FR-009) — DONE.
- [x] T008 [P] [Phase 1] Delete `deploy/firebase/firebase.json`; evaluate removing `deploy/firebase/public/.gitkeep` and the `deploy/firebase/` directory if no other consumer remains. (FR-010) — DONE: both files `git rm`'d; whole `deploy/firebase/` dir gone (no other consumer).

### Acceptance Gate

- [~] T009 [Phase 1] `terraform validate` passes — no dangling references to the removed variable, outputs, or resources. (SC-007) — OFFLINE PROXY PASSED (`terraform fmt -check` clean on edited files; static grep shows no dangling refs outside comments). Authoritative `terraform validate` BLOCKED on auth (`terraform init` needs GCS backend + gcloud).
- [ ] T010 [Phase 1] `terraform plan` shows EXACTLY 5 to destroy, 0 to add, 0 to change; `google_firebase_project.default` and all keep-list resources show no changes. Any deviation = stop-the-line. (FR-006, FR-014, FR-015) — **BLOCKED on auth gate.** This is the founder review gate (T011).

---

## Phase 2: Reviewed apply + verification

**Purpose**: Apply the teardown and prove the zone and founder email are intact.

- [ ] T011 [Phase 2] Reviewer (founder) inspects the Phase 1 `terraform plan` diff in the PR and confirms exactly 5 destroys / 0 other changes before any apply. (FR-018)
- [ ] T012 [Phase 2] Run `terraform apply` (only after T011 sign-off). (FR-001–005)
- [ ] T013 [P] [Phase 2] Re-run `terraform plan` — confirm clean, no drift. (SC-001)
- [ ] T014 [P] [Phase 2] `nslookup api.redmarklogic.com` — confirm no CNAME returned. (SC-002)
- [ ] T015 [P] [Phase 2] `curl -s -o NUL -w "%{http_code}" https://<run.app-url>/health` — confirm same status as the T002b pre-teardown baseline (403 expected until #114). (SC-003)
- [ ] T016 [P] [Phase 2] `terraform output` — confirm no `firebase_*` outputs remain. (SC-006)
- [ ] T017 [Phase 2] Export the post-change zone, diff against the Phase 0 snapshot — confirm exactly one record removed (`api` CNAME, id `6b051d1e36a71373819c95a89d1db64d`) and zero other changes. (SC-004, FR-019)
- [ ] T018 [Phase 2] Founder sends and receives a test email on `redmarklogic.com` — confirm both succeed. (SC-005, FR-020)

### Acceptance Gate

- [ ] T019 [Phase 2] All of T013–T018 pass. Any failure (esp. T017 collateral change or T018 email failure) = stop-the-line; investigate before proceeding.

---

## Phase 3: Documentation + rollback record

**Purpose**: Leave a clean, documented state with a working rollback path.

- [x] T020 [P] [Phase 3] Update `docs/infrastructure/domain-dns-runbook.md` to reflect the removed front door. (FR-021) — DONE: SUPERSEDED banner added at top; body retained as rollback reference.
- [x] T021 [P] [Phase 3] Add a rollback entry to `docs/infrastructure/manual-steps-to-terraform.md` for this teardown (revert + re-apply + two-step DNS converge; cert re-issuance ≤ 24 h). (FR-022, SC-008) — DONE: Entry 005.
- [x] T022 [P] [Phase 3] In root `.env.example`: remove the `FIREBASE_CNAME_TARGET` block (lines ~69–74, which references `api.redmarklogic.com`) and declare the `run.app` URL as the POC API base URL. (`deploy/docker/marker/.env.example` does not reference the branded URL — confirmed; no change there.) (FR-011) — DONE: replaced with `API_BASE_URL` (run.app); name to be confirmed by Kabilan when Django settings land.

### Acceptance Gate

- [ ] T023 [Phase 3] Runbook updated, manual-steps rollback entry present, `.env.example` reflects the POC URL (or confirmed it never referenced the branded URL). Attach both zone snapshots to the PR.

## Execution Notes

- `[P]` = parallelizable (different files / independent checks, no dependencies).
- `[Phase N]` = which plan phase the task belongs to.
- TDD/pytest gates from the standard template do not apply — this is an IaC teardown with no Python under test. Each phase's Acceptance Gate is a Terraform/DNS verification.
- The Acceptance Gate at the end of each phase is a hard stop — do not start the next phase until it passes.
- Phase 0's gate (ADR-027 merged + zone snapshot) blocks all `terraform plan`/`apply` steps.
- The reviewed-plan gate (T011) is mandatory before T012 apply.
- Commit after each task or logical group. Use `/make-pr` to complete the work.
- Execution owner: Brent (DevOps), under founder review of the plan diff.
