---

description: "Task list for GCP project baseline — Terraform IaC + one-off bootstrap"

---

# Tasks: GCP Project Baseline

**Input**: Design documents from `specs/005-gcp-project-baseline/`

**Prerequisites**: plan.md, spec.md, research.md, contracts/terraform-variables.md

**Governed by**: ADR-020 (Terraform IaC for GCP)

**Tests**: No pytest. Verification uses `terraform plan` (pre-apply diff) and `gcloud`
read-only commands post-apply.

**Organization**: Tasks follow the two user stories from spec.md. US2 depends on US1
completing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other [P] tasks in the same phase
- **[Story]**: User story label (US1, US2)

## Path Conventions

- Bootstrap script: `infra/bootstrap/`
- Terraform IaC: `infra/terraform/`

---

## Phase 1: Setup (Directory Structure and tfvars)

**Purpose**: Create the file skeleton and populate `terraform.tfvars` with confirmed
values. No GCP calls, no `terraform` commands yet.

**Gate**: Issues #48 (Cloud Run ratification) and #63 (Tier-1 infra ADR) must be
closed before Phase 2 begins. Phase 1 does not require them.

- [x] T001 Create directories `infra/bootstrap/` and `infra/terraform/`; create empty
  placeholder files: `infra/bootstrap/bootstrap.sh`, `infra/terraform/backend.tf`,
  `infra/terraform/main.tf`, `infra/terraform/variables.tf`, `infra/terraform/terraform.tfvars`,
  `infra/terraform/outputs.tf`, `infra/terraform/apis.tf`, `infra/terraform/billing.tf`
- [x] T002 Populate `infra/terraform/terraform.tfvars` using the schema from
  `specs/005-gcp-project-baseline/contracts/terraform-variables.md`; fill `project_id`
  (`redmarklogic-prod` per research.md naming decision), `region`, `billing_account`,
  exactly one of `folder_id`/`org_id`, and `state_bucket` (`redmarklogic-tf-state`);
  populate the `apis` list from FR-003

---

## Phase 2: Foundational (Prerequisites and Authorisation)

**Purpose**: Confirm all gates are clear and the operator is authenticated with the
correct IAM roles before any GCP resource is created.

**Gate**: #48 and #63 must be closed before this phase runs.

- [ ] T003 Verify `gcloud` CLI is installed and authenticated:
  (a) run `gcloud auth list` and confirm the correct account is active;
  (b) run `gcloud organizations get-iam-policy <org_id>` or
  `gcloud resource-manager folders get-iam-policy <folder_id>` and confirm the active
  account holds `roles/owner` or (`roles/resourcemanager.projectCreator` +
  `roles/billing.user`); provisioning fails silently without this check
- [ ] T004 Confirm the billing account in `terraform.tfvars` is active:
  run `gcloud billing accounts list` and match against the recorded value
- [ ] T005 Verify `terraform` CLI is installed: run `terraform version` and confirm
  version matches the constraint in `infra/terraform/versions.tf` (to be written in T006)

**Checkpoint**: gcloud authenticated with correct roles, billing confirmed, terraform CLI present.

---

## Phase 3: User Story 1 — Provision GCP Project Foundation (Priority: P1)

**Goal**: Run the bootstrap script to create the GCP project and state bucket, then
apply Terraform to enable all APIs and link billing.

**Independent Test**: Run `terraform plan` against the applied state and confirm
zero changes (idempotency). Verify all FR-003 APIs report ENABLED via
`gcloud services list --enabled --project=<project_id>`.

### Bootstrap step (pre-Terraform)

- [x] T006 [US1] Write `infra/terraform/versions.tf` (or add to `main.tf`) declaring
  the required Terraform version (`>= 1.6`) and `hashicorp/google` provider version
  (`~> 5.0`); pin to specific minor version
- [x] T007 [US1] Implement `infra/bootstrap/bootstrap.sh`:
  - `set -euo pipefail` at top
  - Step 1: idempotent project create —
    `gcloud projects describe "$PROJECT_ID" 2>/dev/null || gcloud projects create "$PROJECT_ID" --folder "$FOLDER_ID"` (or `--organization`)
  - Step 2: idempotent state bucket create —
    `gcloud storage buckets describe "gs://$STATE_BUCKET" 2>/dev/null || gcloud storage buckets create "gs://$STATE_BUCKET" --project "$PROJECT_ID" --location "$REGION"`
  - Read `PROJECT_ID`, `FOLDER_ID`/`ORG_ID`, `STATE_BUCKET`, `REGION` from
    `infra/terraform/terraform.tfvars` (parse with grep/sed or pass as env vars)
- [ ] T008 [US1] Run `infra/bootstrap/bootstrap.sh`; confirm GCP project and state
  bucket exist via `gcloud projects describe` and `gcloud storage buckets describe`

### Terraform IaC

- [x] T009 [P] [US1] Implement `infra/terraform/backend.tf`: configure GCS remote
  backend pointing at `state_bucket` value from `terraform.tfvars`
- [x] T010 [P] [US1] Implement `infra/terraform/variables.tf`: declare all variables
  matching the schema in `contracts/terraform-variables.md`
- [x] T011 [P] [US1] Implement `infra/terraform/main.tf`: configure `google` provider
  with `project` and `region` from variables; add `google_project` data source to read
  the already-created project (do not use `google_project` resource — project was created
  in bootstrap)
- [x] T012 [US1] Implement `infra/terraform/apis.tf`: one `google_project_service`
  resource per entry in `var.apis` using `for_each`; set `disable_on_destroy = false`
- [x] T013 [US1] Implement `infra/terraform/billing.tf`: `google_billing_project_info`
  resource linking `var.billing_account` to the project; add idempotency note (resource
  is safe to re-apply)
- [x] T014 [US1] Implement `infra/terraform/outputs.tf`: output `project_number`
  (from data source), `project_id`, `region`, `state_bucket`
- [ ] T015 [US1] Run `terraform init` from `infra/terraform/`; confirm remote state
  initializes against the GCS bucket created in T008
- [ ] T016 [US1] Run `terraform plan`; review diff — expect resources for all FR-003
  APIs and billing linkage; confirm no unexpected additions
- [ ] T017 [US1] Run `terraform apply`; confirm exit code 0 and all resources show
  `Apply complete`
- [ ] T018 [US1] Verify post-apply state:
  - `gcloud services list --enabled --project=<project_id>` — all FR-003 APIs present (SC-002)
  - `gcloud billing projects describe <project_id>` — billing linked and active (SC-005)
  - `terraform output project_number` — non-empty value returned (SC-003)
- [ ] T019 [US1] Re-run `terraform apply`; confirm `0 to add, 0 to change, 0 to destroy`
  (idempotency, SC-004); record timing against SC-001 (< 15 min end-to-end)

**Checkpoint**: GCP project exists, all APIs enabled, billing linked, Terraform state clean,
idempotency confirmed.

---

## Phase 4: User Story 2 — Consistent Environment Identity (Priority: P2)

**Goal**: Confirm downstream scripts can read canonical identifiers from
`terraform.tfvars` and `terraform output` without contacting the infrastructure owner.

**Independent Test**: Read `project_id` and `region` from `terraform.tfvars` and confirm
they match `terraform output project_id` and `gcloud config get-value compute/region`.

- [x] T020 [US2] Add a `README.md` to `infra/` documenting:
  - Purpose of each subdirectory (`bootstrap/`, `terraform/`)
  - How to consume canonical values: read from `terraform.tfvars` for static references;
    use `terraform output` for post-apply values like `project_number`
  - The ADR-020 constraint: no console changes to Terraform-managed resources
- [x] T021 [US2] Cross-reference `infra/terraform/terraform.tfvars` from the project's
  shared architecture docs (or a pointer in `docs/architecture/`) so deploy-chain issue
  owners (#65-#72) know where to find project ID and region without asking
- [x] T022 [US2] Add `specs/005-gcp-project-baseline/verify-output.txt` to `.gitignore`
  (may contain live project identifiers); capture `terraform output` result there as
  post-apply evidence

**Checkpoint**: README exists, cross-reference recorded, terraform output captured.

---

## Phase N: Polish and Cross-Cutting Concerns

- [x] T023 [P] Add SSOT comment at top of `infra/terraform/terraform.tfvars`
  referencing ADR-001 and ADR-020; add ADR-020 reference to `infra/bootstrap/bootstrap.sh`
  header
- [x] T024 Update `specs/005-gcp-project-baseline/checklists/requirements.md` to
  mark all items confirmed post-implementation; add FR-008 (IaC requirement) to the
  checklist and mark it checked

---

## Dependencies and Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately.
- **Phase 2 (Foundational)**: Requires gates #48 and #63 closed. Blocks Phases 3 and 4.
- **Phase 3 (US1)**: Depends on Phase 2. Bootstrap (T006-T008) must complete before
  Terraform steps (T009-T019).
- **Phase 4 (US2)**: Depends on Phase 3 (project_number only available post-apply).
- **Phase N**: After Phase 4.

### Within Phase 3

- T006-T008 (bootstrap) are sequential; must complete before T015 (`terraform init`).
- T009, T010, T011, T012, T013, T014 are marked [P] — all Terraform file authoring can
  proceed in parallel once T006 establishes the versions constraint.
- T015-T019 are sequential (`init` → `plan` → `apply` → `verify` → `idempotency check`).

---

## Implementation Strategy

### MVP (User Story 1 Only)

1. Phase 1: Create directory structure, populate `terraform.tfvars`.
2. Phase 2: Confirm auth and billing.
3. Phase 3: Bootstrap, write Terraform files, `init` → `plan` → `apply` → verify.
4. Validate: all FR-003 APIs enabled, billing linked, idempotency confirmed.

### Full Delivery

1. MVP above.
2. Phase 4: README, cross-reference, output capture.
3. Phase N: SSOT annotations, checklist sign-off.

---

## Notes

- `google_project` resource is NOT used — the project is created by `bootstrap.sh`
  to avoid the state-backend chicken-and-egg problem. Use a `data "google_project"`
  source instead to read project attributes into Terraform state.
- `disable_on_destroy = false` on `google_project_service` prevents APIs being
  disabled if Terraform is ever destroyed — safe default for a production project.
- `terraform.tfvars` is version-controlled and safe. It contains no secrets — only
  project ID, region, billing account ID, and API names.
- `billing_account` is an account ID (format `XXXXXX-XXXXXX-XXXXXX`), not a key.
  Safe to commit.
