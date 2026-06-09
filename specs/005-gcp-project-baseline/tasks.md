---

description: "Task list for GCP project baseline provisioning"

---

# Tasks: GCP Project Baseline

**Input**: Design documents from `specs/005-gcp-project-baseline/`

**Prerequisites**: plan.md, spec.md, research.md, contracts/inventory-schema.md

**Tests**: No automated tests (infrastructure verification uses `gcloud` CLI commands,
not pytest). Verification tasks are built into each phase.

**Organization**: Tasks follow the two user stories from spec.md. US1 and US2 can be
executed by a single operator sequentially.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (no dependency on a preceding task)
- **[Story]**: User story label (US1, US2)

## Path Conventions

- Provisioning scripts: `infra/gcp/`
- Inventory: `infra/inventory.yml`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create directory skeleton and draft inventory. No GCP calls yet.

**Gate**: Issues #48 (Cloud Run ratification) and #63 (Tier-1 infra ADR) must be
closed before Phase 2 begins. This phase does not require them.

- [ ] T001 Create directory `infra/gcp/` and empty placeholder files `bootstrap.ps1`,
  `bootstrap.sh`, `verify.ps1` in `infra/gcp/`
- [ ] T002 Create `infra/inventory.yml` with schema from
  `specs/005-gcp-project-baseline/contracts/inventory-schema.md` -- fill `project_id`
  (use `redmarklogic-prod` per research.md "Project naming convention" decision),
  `region`, `billing_account`, and `organisation_id` or `folder_id` with confirmed
  values; leave `project_number` as `"TBD"` until provisioning resolves it

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Confirm gates are clear and `gcloud` is authenticated before any provisioning.

**Gate**: #48 and #63 must be closed before this phase runs.

- [ ] T003 Verify `gcloud` CLI is installed, authenticated, and authorised:
  (a) run `gcloud auth list` and confirm the correct account is active;
  (b) run `gcloud organizations get-iam-policy <org_id>` or
  `gcloud resource-manager folders get-iam-policy <folder_id>` and confirm the
  active account holds `roles/owner` or `roles/resourcemanager.projectCreator` +
  `roles/billing.user`; provisioning fails silently if this step is skipped
- [ ] T004 Confirm the billing account ID in `infra/inventory.yml` is active:
  run `gcloud billing accounts list` and match against the recorded value
- [ ] T005 Confirm `australia-southeast1` is available for all FR-003 APIs by checking
  GCP regional availability; update `infra/inventory.yml` notes if any API has a
  caveat

**Checkpoint**: gcloud authenticated, billing account confirmed, region verified.

---

## Phase 3: User Story 1 -- Provision GCP Project Foundation (Priority: P1)

**Goal**: Create the GCP project, set the default region, enable all nine APIs,
and link billing.

**Independent Test**: Run `infra/gcp/verify.ps1` and confirm all checks pass with zero
failures.

### Implementation

- [ ] T006 [US1] Implement `infra/gcp/bootstrap.ps1` -- GCP project creation step:
  use `gcloud projects create <project_id>` with either `--organization <org_id>` or
  `--folder <folder_id>` sourced from `infra/inventory.yml`; add idempotency guard
  (run `gcloud projects describe <project_id>` first; skip create if project exists)
- [ ] T007 [US1] Add region step to `infra/gcp/bootstrap.ps1`:
  use `gcloud config set compute/region` and `gcloud config set run/region`
  sourcing the `region` value from `infra/inventory.yml`
- [ ] T008 [US1] Add API enablement step to `infra/gcp/bootstrap.ps1`:
  iterate over `apis_enabled` list from `infra/inventory.yml` and call
  `gcloud services enable` for each; idempotent by default
- [ ] T009 [US1] Add billing linkage step to `infra/gcp/bootstrap.ps1`:
  use `gcloud billing projects link` with `billing_account` from
  `infra/inventory.yml`; add guard for already-linked state
- [ ] T010 [US1] Implement `infra/gcp/bootstrap.sh` (Linux/Bash equivalent of
  `bootstrap.ps1`) -- mirrors steps T006-T009 exactly, targeting CI execution;
  use `set -euo pipefail` at the top; implement idempotency guards with
  `gcloud projects describe "$PROJECT_ID" 2>/dev/null || gcloud projects create ...`
  pattern (not PowerShell `-ErrorAction` style)
- [ ] T011 [US1] Implement `infra/gcp/verify.ps1` -- read-only checks covering
  SC-002 through SC-005 (SC-001 runtime is measured in T012, not by this script):
  - `gcloud projects describe <project_id>` -- project exists (SC-003)
  - `gcloud config get-value compute/region` -- equals `australia-southeast1` (SC-003)
  - `gcloud billing projects describe <project_id>` -- billing linked and active (SC-005)
  - `gcloud services list --enabled` -- all FR-003 APIs present (SC-002)
  - Exit code 0 on full pass, non-zero with named failing check on any failure
- [ ] T012 [US1] Run `infra/gcp/bootstrap.ps1` against a clean state; confirm it
  completes in under 15 minutes (SC-001); record actual runtime in a comment at the
  top of `bootstrap.ps1`
- [ ] T013 [US1] Run `infra/gcp/verify.ps1`; confirm all checks pass; capture output
  as evidence in `specs/005-gcp-project-baseline/verify-output.txt` (add this path
  to `.gitignore` -- it may contain live project identifiers)
- [ ] T014 [US1] Re-run `infra/gcp/bootstrap.ps1` on the already-provisioned project;
  confirm zero resource changes (idempotency, SC-004)

**Checkpoint**: GCP project exists, region set, APIs enabled, billing linked,
verify.ps1 passes, idempotency confirmed.

---

## Phase 4: User Story 2 -- Consistent Environment Identity (Priority: P2)

**Goal**: Record the resolved `project_number` in `infra/inventory.yml` and confirm
downstream scripts can read canonical values without contacting the infrastructure owner.

**Independent Test**: Read `project_id` and `region` from `infra/inventory.yml` and
confirm they match `gcloud config get-value project` and `gcloud config get-value
compute/region` exactly.

### Implementation

- [ ] T015 [US2] Populate `project_number` in `infra/inventory.yml` with the value
  returned by `gcloud projects describe <project_id> --format='value(projectNumber)'`
- [ ] T016 [US2] Add a README section to `infra/` documenting how to consume
  `inventory.yml` and which keys are safe to reference in downstream scripts
- [ ] T017 [US2] Cross-reference `infra/inventory.yml` in `docs/architecture/` or
  equivalent shared location so deploy-chain issue owners (#65-#72) can find the
  canonical project ID and region without asking the infrastructure owner

**Checkpoint**: inventory.yml is complete, project_number populated, README exists,
cross-reference recorded.

---

## Phase N: Polish and Cross-Cutting Concerns

- [ ] T018 [P] Add a one-line comment at the top of `infra/inventory.yml` declaring
  it as the SSOT (Constitution I) and listing the ADR it is grounded in once #63 is
  accepted
- [ ] T019 Update `specs/005-gcp-project-baseline/checklists/requirements.md` to
  mark all items confirmed post-implementation

---

## Dependencies and Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies -- start immediately.
- **Phase 2 (Foundational)**: Requires gates #48 and #63 closed. Blocks Phases 3 and 4.
- **Phase 3 (US1)**: Depends on Phase 2 completion.
- **Phase 4 (US2)**: Depends on Phase 3 completion (project_number only known post-provisioning).
- **Phase N (Polish)**: After Phase 4.

### Within Phase 3

- T006-T009 are sequential steps within `bootstrap.ps1`; each adds to the same file.
- T010 (`bootstrap.sh`) can be written in parallel with T007-T009 once T006 is done.
- T011 (`verify.ps1`) can be written in parallel with T008-T010.
- T012-T014 are sequential validation runs.

### Parallel Opportunities

- T006 and T010/T011 drafting can overlap once T006 establishes the script skeleton.

---

## Implementation Strategy

### MVP (User Story 1 Only)

1. Phase 1: Create directory structure and draft `inventory.yml`.
2. Phase 2: Confirm authentication and billing.
3. Phase 3: Implement and run `bootstrap.ps1`, confirm `verify.ps1` passes.
4. Validate: all FR-003 APIs enabled, billing linked, region correct.

### Full Delivery

1. MVP above.
2. Phase 4: Populate `project_number`, write README, add cross-reference.
3. Phase N: SSOT annotation, checklist sign-off.

---

## Notes

- No pytest. Verification is via `gcloud` CLI commands in `verify.ps1`.
- `inventory.yml` is the only cross-feature artifact; all other files are internal.
- `bootstrap.sh` is a CI companion to `bootstrap.ps1` -- kept in sync manually until
  a CI job (issue #69) automates it.
- Do not commit credentials or billing key material. `billing_account` stores the
  account ID only (safe to version-control per research.md).
