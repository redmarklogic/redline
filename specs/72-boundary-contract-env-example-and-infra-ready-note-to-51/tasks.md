# Tasks: Boundary Contract — .env.example and Infra-Ready Note

**Input**: [plan.md](plan.md)
**Prerequisites**: Terraform applied (spec-70 Cloud Run services deployed); `gcloud` ADC valid; `gh` auth valid

<!-- Vertical slice rule: Phase A (env.example) ships independently.
     Phase B (infra-ready comment) is a manual operational step, not a PR task.
     No Python changes; no pytest. -->

## Phase 0: Verify infra values

**Purpose**: Confirm the live Cloud Run values are available before editing any files.

- [ ] T001 [Phase 0] Read staging Cloud Run URL: `gcloud run services describe staging-redline-api --region=australia-southeast1 --format='value(status.url)'` — confirm output is a `*.run.app` URL
- [ ] T002 [Phase 0] Read SA email: `terraform -chdir=deploy/infra/terraform output cloud_run_sa_email` — confirm output matches `cloud-run-api-sa@redmarklogic-prod.iam.gserviceaccount.com`

### Acceptance Gate

- [ ] T003 [Phase 0] Both commands return non-empty values; no auth errors

---

## Phase 1: Update .env.example (US1)

**Purpose**: `.env.example` documents all three infra-to-app variables so a developer can configure their environment without asking Brent.

### Implementation

- [ ] T004 [US1] Open `.env.example`; confirm `API_BASE_URL` entry exists under the ADR-027 block and its annotation accurately reflects ADR-027 D1 wording (source instruction: `gcloud run services describe ... --format='value(status.url)'`). Update annotation only if wording is stale.
- [ ] T005 [US1] Add `GCP_OIDC_AUDIENCE` entry immediately after `API_BASE_URL` in `.env.example`, tagged `Non-secret`, with annotation: "Equals `API_BASE_URL` for the same env — Cloud Run OIDC tokens use the service URL as audience by default (GCP behaviour). Read same source as `API_BASE_URL`."
- [ ] T006 [US1] Add `CLOUD_RUN_SA_EMAIL` entry in `.env.example`, tagged `Non-secret`, canonical value `cloud-run-api-sa@redmarklogic-prod.iam.gserviceaccount.com`, annotation: "Cloud Run service account identity. Verify: `terraform -chdir=deploy/infra/terraform output cloud_run_sa_email`."

### Acceptance Gate

- [ ] T007 [US1] Run `detect-secrets scan .env.example` — zero new genuine secrets flagged
- [ ] T008 [US1] Read `.env.example` end-to-end; confirm all three variables are present, annotated, and no duplicate `API_BASE_URL` entry exists

---

## Phase 2: Post infra-ready comment on issue #51 (US2)

**Purpose**: Issue #51 receives the infra-ready signal and the app team has all values to proceed.

**Gate**: B7 must be cleared before this phase runs. Do not post until verified.

### Implementation

- [ ] T009 [US2] Verify B7 is cleared (check GitHub Project board or issue dependency list)
- [ ] T010 [US2] Read live staging URL via `gcloud` (T001 command) and substitute into comment template from `plan.md`; create dir `.agents/tmp/infra-ready-comment-2026-06-12/` and write body to `comment.md` there
- [ ] T011 [US2] Review `comment.md` for accidental secret values before posting
- [ ] T012 [US2] Post comment: `gh issue comment 51 --repo redmarklogic/redline --body "$(cat .agents/tmp/infra-ready-comment-2026-06-12/comment.md)"`

### Acceptance Gate

- [ ] T012 [US2] Navigate to issue #51 on GitHub; confirm comment exists with heading "Infra ready (#72)", non-secret values listed, and no raw secrets present

---

## Phase 3: Polish

- [ ] T013 [P] [Phase 3] Commit `.env.example` with message referencing issue #72
- [ ] T014 [Phase 3] Run `detect-secrets scan` on full repo — confirm baseline unchanged

### Acceptance Gate

- [ ] T015 [Phase 3] CI passes (detect-secrets hook green); no regressions

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies)
- No pytest — this feature has no Python source changes
- Phase 2 (T009-T012) is a manual operational step by Brent; it does not block the PR
- Write the comment body to `.agents/tmp/infra-ready-comment-2026-06-12/comment.md` before posting (for review and record)
- Use `/make-pr` after T013-T015 pass

## Dependency Graph

```text
T001 → T003 (gate)
T002 → T003 (gate)
T003 → T004 → T005 → T006 → T007 → T008 (gate)
T008 → T013 → T014 → T015 (gate)
T009 → T010 → T011 → T012 (independent of PR; after B7)
```

## Independent Test Criteria

| User Story | Independent Test |
|------------|-----------------|
| US1 — Developer reads .env.example | `detect-secrets scan .env.example` passes; all three vars visible in file |
| US2 — Infra-ready comment on #51 | Comment visible on issue #51 with correct content; no secrets present |
