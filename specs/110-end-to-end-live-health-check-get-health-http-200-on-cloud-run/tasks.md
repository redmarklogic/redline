# Tasks: End-to-End Live Health Check on Cloud Run

**Input**: Design documents from `specs/110-end-to-end-live-health-check-get-health-http-200-on-cloud-run/`

**Prerequisites**: plan.md, spec.md, research.md (D1–D11), data-model.md, contracts/, quickstart.md

**Tests**: Not requested — verification is live (curl/CI evidence) plus `actionlint`; no pytest changes.

**Organization**: Phases follow spec story priority. Note the deliberate dependency: US2 (P1) is a blocking prerequisite of US1 (P1) — secrets and cost posture must land before the service-creating apply (spec US2 "Why this priority"; research D1/D6).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: parallelizable (different files, no dependency on an incomplete task)
- Story labels map to spec.md user stories

## Phase 1: Setup (verification only — no mutations)

- [ ] T001 [SETUP] Confirm branch `feature/110-end-to-end-live-health-check-get-health-http-200-on-cloud-run` is current and clean (`rtk git status`); confirm `deploy/docker/marker/Dockerfile` exists (issue #67 merged) and serves on port 8080 (startup-probe port, contracts/health-endpoint.md).
- [ ] T002 [P] [SETUP] Confirm GitHub repo variables `WIF_PROVIDER` and `GHA_SA_EMAIL` are set (`gh variable list`). If unset, populate from Terraform outputs `wif_provider_name` / `github_actions_sa_email` after T011 — note and continue.
- [ ] T003 [P] [SETUP] Verify starting state: `gcloud run services list --region australia-southeast1` returns 0 items (spec US1 scenario 3); record output as evidence.
- [ ] T004 [P] [SETUP] Ensure `actionlint` and `terraform >= 1.6` are available locally; `gcloud auth list` shows the founder account against project `redmarklogic-prod`.

---

## Phase 2: Foundational (Terraform code edits — block all live work)

**⚠️ CRITICAL**: No GCP mutation until these are reviewed.

- [ ] T005 [FOUND] In `deploy/infra/terraform/secrets.tf`, change secret replication `auto {}` → `user_managed` pinned to `australia-southeast1` (research D1; topology follow-up #4).
- [ ] T006 [P] [FOUND] In `deploy/infra/terraform/variables.tf`, change `min_instances_prod` validation to `>= 0 && <= 5` and default to `0`; update the description's FR reference if it cites the old bound (research D3; topology follow-up #7).
- [ ] T007 [P] [FOUND] In `deploy/infra/terraform/cloud_run.tf`, add `google_cloud_run_v2_service_iam_member` granting `roles/run.invoker` to `allUsers` on `google_cloud_run_v2_service.api["staging"]` ONLY — prod stays IAM-private (research D11; spec FR-011; without this the acceptance curl returns 403).
- [ ] T008 [FOUND] Run `terraform init` and `terraform validate` in `deploy/infra/terraform/`; confirm clean. Confirm `terraform plan` WITHOUT `-var image_tag` still fails (by-design guard — spec edge case; do not add a default).

**Checkpoint**: Founder reviews the three diffs before any apply.

---

## Phase 3: User Story 2 — Secrets and cost posture correct before go-live (P1)

**Goal**: Four secrets exist Sydney-pinned with real values; prod sleeps from first apply.

**Independent Test**: Secret material only in `australia-southeast1`; every secret has an accessible current version; prod min instances 0 (spec US2).

- [ ] T009 [US2] Targeted reviewed apply creating the four secrets only: `terraform plan/apply -target='google_secret_manager_secret.secrets' -var image_tag=bootstrap` (one-off bootstrap ordering, research D6; review: 4 secrets, nothing else; `bootstrap` tag never reaches a service).
- [ ] T010 [US2] Populate real values via `gcloud secrets versions add <id> --data-file=-` for the four secret IDs `staging-redline-db_password`, `staging-redline-api_key`, `prod-redline-db_password`, `prod-redline-api_key` — lowercase binding keys per `secrets.tf:27`; the uppercase names are container env vars, not secret IDs (values from founder, stdin only, never on disk — research D2; spec assumption on not-yet-existing backing services).  # pragma: allowlist secret
- [ ] T011 [US2] Verify: `gcloud secrets versions list` shows one enabled version per secret; `gcloud secrets describe` shows `user_managed` replication = `australia-southeast1` only. Record outputs as evidence (SC-004).

**Checkpoint**: US2 acceptance scenarios 1 and 3 verifiable (scenario 3 completes at T014).

---

## Phase 4: User Story 1 — Staging backend live and verifiable (P1) — MVP

**Goal**: `curl <staging_url>/health` → HTTP 200, JSON body `{"status": "healthy"}` (SC-001).

**Independent Test**: spec US1 — image in registry, apply, curl.

- [ ] T012 [US1] Build and push the first image manually (operational, Constitution XV): `rtk docker build -f deploy/docker/marker/Dockerfile -t australia-southeast1-docker.pkg.dev/redmarklogic-prod/redline-repo/redline-api:<sha> .` with `<sha> = rtk git rev-parse HEAD`, then `gcloud auth configure-docker australia-southeast1-docker.pkg.dev` and `rtk docker push <same-ref>` (research D6 step 3).
- [ ] T013 [US1] Full reviewed apply: `terraform plan -var image_tag=<sha>` (review: 2 Cloud Run services + staging `allUsers` invoker (D11) + IAM/outputs; prod min instances 0; no secret changes) then `terraform apply -var image_tag=<sha>` in `deploy/infra/terraform/`.
- [ ] T014 [US1] Verify services: `gcloud run services list --region australia-southeast1` shows `staging-redline-api` and `prod-redline-api` Ready (SC-002); prod min instances 0 (US2 scenario 3, SC-005); serving revision references the `<sha>` tag (SC-003).
- [ ] T015 [US1] Live acceptance: `$url = terraform output -raw staging_url; curl.exe -i "$url/health"` → HTTP 200 with JSON body equal to `{"status": "healthy"}` when parsed — wire bytes are compact `{"status":"healthy"}`; assert JSON-equality, not byte-equality (contracts/health-endpoint.md). Record full output as evidence (SC-001).
- [ ] T016 [US1] Post evidence bundle (T003, T011, T014, T015 outputs + apply summary) as a comment on issue #110 (`gh issue comment 110`).

**Checkpoint**: MVP live. STOP and validate before touching CI.

---

## Phase 5: User Story 3 — CI publishes a runnable image on every push (P2)

**Goal**: Real build+push replaces the `ci.yml` stub; deploy job scoped to the `production` environment.

**Independent Test**: A push to a watched branch yields a SHA-tagged image in Artifact Registry (spec US3). Accepted (analysis M3, founder 2026-06-11): proven at US4's merge run — the trigger flip lands last by design.

- [ ] T017 [US3] In `.github/workflows/ci.yml`, add the workflow-level `env:` block (`GCP_REGION`, `GCP_PROJECT`, `AR_REPO`, `IMAGE_NAME`) with the SSOT-pointer comment, exactly per `contracts/pipeline-outputs.md` (research D5; Constitution I deviation recorded in plan.md).
- [ ] T018 [US3] In `.github/workflows/ci.yml`, replace the stub step (lines 52-57) with: `google-github-actions/setup-gcloud` + `gcloud auth configure-docker ${{ env.GCP_REGION }}-docker.pkg.dev`, `docker/setup-buildx-action`, `docker/build-push-action` building `deploy/docker/marker/Dockerfile` for `linux/amd64`, tag `:${{ github.sha }}` from the env block; every `uses:` SHA-pinned with version comment (research D4; spec-69 T007–T009 carry-over). While editing, re-pin the pre-existing `google-github-actions/auth@v2` step to a full commit SHA with version comment — it is currently tag-pinned, violating the repo convention (critique E6). Keep pytest BEFORE auth/build/push; no `continue-on-error`/`if: always()` on gate or push (pipeline invariants 1, 4).
- [ ] T019 [US3] In `.github/workflows/ci.yml`, expose the build-push step's `outputs.digest` as job output `image_digest` and append a `$GITHUB_STEP_SUMMARY` line with `image:sha` + digest (contracts/pipeline-outputs.md; spec-69 T012–T013 carry-over).
- [ ] T020 [US3] Add `environment: production` to the deploy job in `.github/workflows/ci.yml`, and create the environment idempotently: `gh api -X PUT repos/redmarklogic/redline/environments/production` (research D9; FR-008).
- [ ] T021 [P] [US3] Run `actionlint` on `.github/workflows/ci.yml`; fix findings; confirm SHA-pinning convention holds.

**Checkpoint**: Workflow builds/pushes on its (still `main`) trigger — content proven by US4's merge run.

---

## Phase 6: User Story 4 — Merge to master runs the pipeline end-to-end (P3)

**Goal**: One merge → test → build+push → deploy → automated health check, zero manual steps (SC-006).

**Independent Test**: spec US4 — merge PR, watch single run complete all stages.

- [ ] T022 [US4] In `.github/workflows/ci.yml`, append the deploy step: `gcloud run services update staging-redline-api --image <env-block ref>:${{ github.sha }} --region ${{ env.GCP_REGION }}` — staging only, after push succeeds (research D7; CI never runs terraform).
- [ ] T023 [US4] In `.github/workflows/ci.yml`, append the health-check step: first poll the service Ready condition (`gcloud run services describe staging-redline-api --region ${{ env.GCP_REGION }} --format 'value(status.conditions[0].status)'`), then fetch the URL (`--format 'value(status.url)'`) and poll `GET <url>/health` with curl retry ≤ 120 s total, assert HTTP 200 AND body JSON-equal to `{"status": "healthy"}` (compact wire bytes `{"status":"healthy"}` — parse, don't byte-match); non-200/wrong body fails the run (research D8; FR-010; pipeline invariants 2–3; critique E2).
- [ ] T024 [US4] In `.github/workflows/ci.yml`, switch trigger to `master` only — remove `main` and `release/**` (restored by #107); keep `workflow_call`. In `.github/workflows/tests.yml`, switch `push` trigger `main` → `master` (research D10; spec-69 T004/T005 carry-over; LAST content commit on the branch).
- [ ] T025 [US4] Re-run `actionlint` on both workflows; open the PR (`gh pr create --fill`), founder reviews and merges to `master`.
- [ ] T026 [US4] Watch the post-merge run (`gh run watch`): all stages green including health check; record run URL, step summary (image digest), and health-check output as evidence on issue #110 (SC-006).

**Checkpoint**: All user stories live. Feature acceptance met.

---

## Phase 7: Polish & Cross-Cutting

- [ ] T027 [P] [POLISH] Comment on issue #69 that its authored-but-unexecuted task design (specs/69 T004–T013) was absorbed and delivered by #110 (spec-69 reconciliation; source-reconciliation step 6).
- [ ] T028 [P] [POLISH] Verify idempotency: re-run the pipeline on the already-published commit (`gh run rerun`); run succeeds, `:<sha>` tag still resolves, previously recorded digest unchanged (spec-69 T017 carry-over).
- [ ] T029 [POLISH] Confirm scale-to-zero billing posture after ~1 idle hour: `gcloud run services describe` shows min instances 0 on both services; note in issue #110 (SC-005).

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** → no dependencies; T002–T004 parallel.
- **Phase 2 (Foundational)** → blocks everything live; T005 ∥ T006 ∥ T007, then T008.
- **Phase 3 (US2)** → strictly ordered T009 → T010 → T011. BLOCKS US1 (deliberate cross-story dependency, spec US2).
- **Phase 4 (US1, MVP)** → T012 → T013 → T014 → T015 → T016. STOP/validate checkpoint.
- **Phase 5 (US3)** → independent of US1 runtime state; T017 → T018 → T019 → T020, T021 after T018. Can draft in parallel with Phase 4 but merge-ordered after it.
- **Phase 6 (US4)** → needs US3 content; T022 → T023 → T024 → T025 → T026.
- **Phase 7 (Polish)** → after T026; T027 ∥ T028.

## Implementation Strategy

MVP = Phases 1–4 (Stage 1 of issue #110): staging live, health 200, evidence on
the issue. Phases 5–6 are Stage 2 (pipeline + trigger switch + merge). The
trigger flip (T024) is deliberately the last content change so no push deploys
before the chain is proven (research D10).
