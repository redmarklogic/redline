# Tasks: Backend Image CI Pipeline (build, test-gated, push to Artifact Registry)

**Input**: Design documents from `specs/69-github-actions-pipeline-build-test-push-backend-image/`

**Prerequisites**: [plan.md](plan.md) (required), [spec.md](spec.md) (user stories). No
`data-model.md`/`contracts/` (no data entities — see plan).

**Tests**: This is CI/CD configuration, not application code. "Tests" here are workflow
linting (`actionlint`) and the spec's verification scenarios run on a real runner — not
pytest. The existing pytest suite is consumed unchanged.

**Organization**: Tasks grouped by user story. **Reality check on parallelism:** US1, US2,
and US3 all edit the *same file* (`.github/workflows/ci.yml`), so they are largely
**sequential**, not parallel. `[P]` is used only where files genuinely differ.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: different files, no dependency — safe to parallelize.
- **[Story]**: US1 / US2 / US3, or `SETUP`/`FOUND`/`POLISH`.

---

## Phase 1: Setup (Shared)

**Purpose**: Confirm preconditions and tooling before editing workflows.

- [ ] T001 [SETUP] Confirm branch `feature/69-…-backend-image` is checked out and master is merged in (Dockerfile `deploy/docker/marker/Dockerfile` and `deploy/infra/terraform/workload_identity.tf` present). *(Already done this session — verify only.)*
- [ ] T002 [P] [SETUP] Confirm GitHub repo variables `WIF_PROVIDER` and `GHA_SA_EMAIL` are set (values = Terraform outputs `wif_provider_name`, `github_actions_sa_email`). If unset, this is a B3-apply prerequisite, not a code task — note and continue.
- [ ] T003 [P] [SETUP] Ensure `actionlint` is available for local workflow linting (used in T012/T013).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Make trunk CI fire and lay the shared config the build step needs. Blocks all
user stories.

**⚠️ CRITICAL**: No story work is meaningful until the workflow triggers on `master`.

- [ ] T004 [FOUND] In `.github/workflows/ci.yml`, change the push trigger `branches: [main]` → `branches: [master]` and **remove `release/**`** from the push trigger (POC = master-only; re-added by #107 on 2026-06-22). Keep `workflow_call`. (FR-001)
- [ ] T005 [P] [FOUND] In `.github/workflows/tests.yml`, change `push: branches: ["main"]` → `["master"]` (keep `pull_request`). Independent file — parallel with T004. (FR-001, dormant-trigger fix)
- [ ] T006 [FOUND] In `ci.yml`, add a single SSOT `env:` block at job (or workflow) scope: `REGISTRY: australia-southeast1-docker.pkg.dev`, `IMAGE: redmarklogic-prod/redline-repo/redline-api`. Values match `deploy/infra/terraform/terraform.tfvars` (`project_id = redmarklogic-prod`, `region = australia-southeast1`) — the **canonical source**. Add a comment in `ci.yml` pointing to `terraform.tfvars` so the duplication is traceable and drift is catchable (GHA cannot read TF state, so this `env` block is a deliberate, documented second copy). (Constitution I/XVI)

**Checkpoint**: A push to `master` triggers `ci.yml`; config is defined once.

---

## Phase 3: User Story 1 - Tested image published on trunk merge (P1) [MVP]

**Goal**: On a passing master merge, build the backend image and push it to Artifact Registry.

**Independent Test**: Merge a trivial passing change to master → `redline-api:<sha>` appears
in the registry and is pullable.

- [ ] T007 [US1] In `ci.yml`, after the existing `google-github-actions/auth@v2` step, add `google-github-actions/setup-gcloud` and `gcloud auth configure-docker australia-southeast1-docker.pkg.dev` (SHA-pinned). (FR-005, FR-007)
- [ ] T008 [US1] In `ci.yml`, add `docker/setup-buildx-action` (SHA-pinned) before the build. (FR-004)
- [ ] T009 [US1] In `ci.yml`, replace the `TODO — build and push image` step with `docker/build-push-action` (SHA-pinned): **`context: .` (repo root — the Dockerfile uses root-relative `COPY src/`, `COPY pyproject.toml`)**, `file: deploy/docker/marker/Dockerfile`, **`platforms: linux/amd64` (Cloud Run target)**, `tags: ${{ env.REGISTRY }}/${{ env.IMAGE }}:${{ github.sha }}`, `push: true`, BuildKit cache (`cache-from`/`cache-to: type=gha`). Give the step an `id` for output capture. (FR-004, FR-005, FR-006 tag, FR-008, FR-009)

**Checkpoint**: US1 functional — a green master merge publishes a commit-tagged image.

---

## Phase 4: User Story 2 - Failed tests publish nothing (P1)

**Goal**: A red test gate (or a failed build/push) leaves no image published.

**Independent Test**: Push a commit with a failing test → job is red, no image in registry.

- [ ] T010 [US2] In `ci.yml`, verify step ordering keeps `pytest` (existing `pavelzw/pytest-action` step) **before** auth/buildx/build-push, so a failing gate short-circuits the job. Do not reorder; add a comment locking the contract. (FR-002, FR-003)
- [ ] T011 [US2] Confirm no `continue-on-error: true` / `if: always()` on the build/push or test steps (a failure must fail the job and skip the push). (FR-009)

**Checkpoint**: US1 + US2 hold — failures publish nothing.

---

## Phase 5: User Story 3 - Digest provenance handoff (P2)

**Goal**: Surface the pushed image digest for the downstream deploy step; tag by commit.

**Independent Test**: Merge two changes → each run reports a distinct `image_digest` and a
distinct `:<sha>` tag.

- [ ] T012 [US3] In `ci.yml`, expose the build-push step's `outputs.digest` as a **job output** `image_digest` (`jobs.<job>.outputs.image_digest: ${{ steps.<id>.outputs.digest }}`). (FR-006, FR-010)
- [ ] T013 [US3] In `ci.yml`, append a `$GITHUB_STEP_SUMMARY` line printing the pushed `image:sha` and digest for human traceability. (FR-006, SC-003)

**Checkpoint**: All three stories functional in one job.

---

## Phase 6: Polish & Verification

- [ ] T014 [P] [POLISH] Run `actionlint` on `ci.yml` and `tests.yml`; fix any findings. Confirm every `uses:` is SHA-pinned (repo convention).
- [ ] T015 [POLISH] Execute the [plan.md](plan.md) quickstart end-to-end **once B3 (`terraform apply` of `artifact_registry.tf` + `workload_identity.tf`) is applied**: green-merge publish, negative failing-test run, digest pullable. Record evidence (run URL, registry listing, digest) for the verification-gate.
- [ ] T016 [P] [POLISH] Add a one-line note to GitHub issue #69 that the pipeline gates on the inline pytest step (reconciling the issue's "runs pytest" wording with the completed `ci.yml` scaffold).
- [ ] T017 [POLISH] Verify idempotency (FR-011) **after B3 apply**: re-run the pipeline on an already-published commit; confirm the run succeeds, the `:<sha>` tag resolves, and a previously recorded digest is still pullable (digest-pinned deploys unaffected). No skip-if-exists logic expected for POC.

---

## Dependencies & Execution Order

- **Setup (T001–T003)**: no dependencies.
- **Foundational (T004–T006)**: T004 (and T006) block all stories; T005 is independent (different file).
- **US1 (T007–T009)**: after T004/T006. T007 → T008 → T009 (same file, ordered).
- **US2 (T010–T011)**: after T009 (verifies ordering of the now-complete job).
- **US3 (T012–T013)**: after T009 (depends on the build-push step `id`).
- **Polish (T014–T016)**: T014 after all edits; T015 after T014 **and** B3 apply; T016 anytime.

### External prerequisite (not a #69 task)

- **B3** — `terraform apply` of `deploy/infra/terraform/` so the AR repo + WIF binding exist
  in the project. Live acceptance (T015) cannot pass until this lands. Author/lint
  (T001–T014) can complete now.

## Parallel Opportunities

Limited by single-file editing. Genuinely parallel: **T002 ∥ T003**, **T004 ∥ T005**
(different files), **T014 ∥ T016**. Everything in US1→US2→US3 is sequential on `ci.yml`.

## Implementation Strategy

MVP = T001–T009 (Setup + Foundational + US1): a tested image lands in the registry on
master merge. T010–T013 add the failure guardrail and the digest handoff the deploy step
needs. T015 proves it end-to-end once infra is applied.

## Notes

- All `uses:` MUST be SHA-pinned (matches `ci.yml`/`tests.yml` convention; supply-chain).
- No application code changes; do not touch `src/` or the Dockerfile (owned by #67).
- Commit workflow edits together; the change is small and cohesive.
