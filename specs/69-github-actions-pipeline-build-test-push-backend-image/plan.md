# Implementation Plan: Backend Image CI Pipeline (build, test-gated, push to Artifact Registry)

**Branch**: `feature/69-github-actions-pipeline-build-test-push-backend-image` | **Date**: 2026-06-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/69-github-actions-pipeline-build-test-push-backend-image/spec.md`

## Summary

Complete the build-and-push link of the walking-skeleton deploy chain (#89) by filling
the `TODO — build and push image` placeholder already scaffolded in
`.github/workflows/ci.yml` (left by #68). On a merge to `master`, the single CI job runs
pytest, authenticates to GCP via Workload Identity Federation (both already present),
then builds the backend image from `deploy/docker/marker/Dockerfile`, pushes it to
Artifact Registry (`australia-southeast1`, `redline-repo/redline-api`), and emits the
pushed **digest** as a job output for the downstream deploy step (#67 digest-only rule).
The same change corrects the pre-existing `main`→`master` trigger defect in `ci.yml` and
`tests.yml`.

This is infra-as-CI-config, not application code. The technical context below overrides
the Python-application preset, which does not apply.

## Technical Context

**Language/Version**: GitHub Actions workflow YAML (no application language change). Build
toolchain: Docker BuildKit / `buildx` on the runner.

**Primary Dependencies** (all pinned by commit SHA, matching repo convention in `ci.yml`):
- `actions/checkout` — already present.
- `astral-sh/setup-uv` + `uv sync` + `pavelzw/pytest-action` — existing test gate, unchanged.
- `google-github-actions/auth@v2` — existing WIF auth, unchanged (consumes `vars.WIF_PROVIDER`, `vars.GHA_SA_EMAIL`).
- `google-github-actions/setup-gcloud` — to configure Docker auth for Artifact Registry (`gcloud auth configure-docker australia-southeast1-docker.pkg.dev`).
- `docker/build-push-action` (+ `docker/setup-buildx-action`) — build + push in one step; exposes the pushed image `digest` as a step output.

**Storage**: Google Artifact Registry repo `redline-repo` in `australia-southeast1`
(provisioned by `deploy/infra/terraform/artifact_registry.tf`). Image: `redline-api`.

**Testing**: Existing pytest gate (`uv run --frozen pytest --cov`) runs inline before
build. Workflow-level verification per quickstart below (act/dry-run + a real trunk merge
once B3 is applied).

**Target Platform**: `ubuntu-latest` runner (ADR-019 — CI is Linux). Image target is
Cloud Run (ADR-022).

**Project Type**: CI/CD pipeline (single GitHub Actions workflow).

**Performance Goals**: Deploy-ready image published within 10 min of the test gate
completing (SC-002). BuildKit layer caching to keep rebuilds fast.

**Constraints**: No long-lived credentials (WIF only). Digest is the canonical handoff to
deploy. Build/push must be atomic-from-the-consumer's-view: a failed push leaves no usable
image and fails the run (FR-009).

**Scale/Scope**: One workflow file edited, two trigger lines corrected. Single
environment (ADR-023).

## Constitution Check

*GATE: re-checked after design below. No violations.*

- **XV — IaC for GCP resources**: PASS. #69 provisions no GCP resources; the AR repo, WIF
  pool/provider, SA, and `roles/artifactregistry.writer` binding all already live in
  `deploy/infra/terraform/` (#68). The workflow only *consumes* them.
- **XIV — Platform obligation follows deployment context (ADR-019)**: PASS. Workflow runs
  on `ubuntu-latest`; no Windows-only constructs.
- **XVI — Process environment as sole config source / I — SSOT**: PASS with a design rule.
  WIF provider and SA come from repo `vars` (SSOT = Terraform outputs `wif_provider_name`,
  `github_actions_sa_email`). The registry host, repo, region, and image name are a single
  SSOT concern: define them once as workflow `env:` (e.g. `REGISTRY`, `IMAGE`) derived from
  the canonical reference `australia-southeast1-docker.pkg.dev/redmarklogic-prod/redline-repo/redline-api`
  rather than repeating literals across steps. (Project id `redmarklogic-prod` already
  appears in #67's canonical image reference; reuse it, do not re-derive.)
- **XII — CLI-first tool selection (ADR-016)**: PASS. `gcloud`/`docker` via official
  actions, no bespoke API calls.
- **X — Raise on failure**: PASS. Any build/push failure fails the job (no sentinel/
  swallow); `set -euo pipefail` for any inline shell.
- **II — Hook-first**: N/A (no new agent rule).

No entries in Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/69-github-actions-pipeline-build-test-push-backend-image/
├── spec.md              # Complete
├── plan.md              # This file
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/speckit.tasks — not created here)
```

No `research.md` / `data-model.md` / `contracts/` needed: there are no data entities,
and the "research" (auth pattern, registry path, digest rule, Dockerfile location) is
already settled by the existing scaffold and #67/#68 and captured in Technical Context.

### Source Code (repository root)

Files touched by this feature:

```text
.github/workflows/
├── ci.yml        # EDIT: trigger main→master; replace TODO step with build+push+digest output
└── tests.yml     # EDIT: trigger main→master (dormant-trigger fix)

deploy/docker/marker/Dockerfile   # CONSUMED (read-only here; owned by #67)
deploy/infra/terraform/*.tf       # CONSUMED (read-only here; owned by #68)
```

**Structure Decision**: Edit the existing `ci.yml` job in place rather than adding a new
workflow — it already chains checkout → test → WIF auth and holds the #69 placeholder.
This honours the #68 author's scaffold, keeps a single trunk pipeline, and avoids a
`workflow_run` coupling. `tests.yml` remains the independent PR-feedback workflow.

## Implementation Approach

Ordered, each step independently verifiable:

1. **Fix triggers (FR-001).** In `ci.yml` and `tests.yml`, change `branches: [main]` →
   `branches: [master]`. **Drop `release/**` from `ci.yml`'s push trigger** (POC =
   master-only; re-added later by #107, dated 2026-06-22, when release images become
   user-facing). Keep `tests.yml`'s `pull_request` and `ci.yml`'s `workflow_call`.
   Verifiable immediately: a push to master triggers both; a `release/**` push does not
   build/push.

2. **Configure registry Docker auth.** After the existing `google-github-actions/auth`
   step, add `setup-gcloud` + `gcloud auth configure-docker australia-southeast1-docker.pkg.dev`
   (or `docker/login-action` against the AR host using the WIF access token).

3. **Build + push with digest output (FR-004/005/006/008/009).** Replace the TODO step
   with `docker/setup-buildx-action` + `docker/build-push-action`:
   - `context: .` (repo root — the Dockerfile's `COPY src/`, `COPY pyproject.toml` are
     root-relative, matching #67's `docker build … -f deploy/docker/marker/Dockerfile .`).
   - `file: deploy/docker/marker/Dockerfile`.
   - `platforms: linux/amd64` (Cloud Run runtime target; ADR-022).
   - `tags`: `${REGISTRY}/${IMAGE}:${{ github.sha }}` (immutable commit tag).
   - `push: true`; rely on the action's failure to fail the job.
   - Capture the step's `digest` output; expose it as a **job output** `image_digest`
     (consumed by the deploy issue downstream).
   - Enable BuildKit layer cache (`cache-from`/`cache-to: gha`) for SC-002.

4. **Surface the digest (FR-010).** Add a job-summary line and a job `outputs.image_digest`
   so the deploy workflow can `needs:` it (or read it from the run).

5. **Guardrails (FR-002/003).** Confirm step ordering keeps pytest before auth/build so a
   red test gate short-circuits the job (it already does; just don't reorder).

## Phase 0 / research

Settled — no open unknowns. Decisions and their sources:

| Decision | Choice | Source |
|---|---|---|
| Where build/push lives | Complete `ci.yml` in place (single job) | Founder, 2026-06-11; #68 scaffold |
| Trigger | `master` (fix `main` defect in ci.yml + tests.yml) | Founder; repo default branch |
| Test gate | Inline pytest before build (existing step) | Founder; existing `ci.yml` |
| Auth | WIF, keyless (existing step) | #68; FR-007 |
| Image source | `deploy/docker/marker/Dockerfile`, image `redline-api` | #67 |
| Registry | `…/redline-repo/redline-api`, `australia-southeast1` | #67, ADR-022 |
| Deploy handoff | Image **digest** (primary), commit-SHA tag (secondary) | #67 digest-only rule |
| Runner | `ubuntu-latest` | ADR-019 |

## Quickstart / verification

- **Static**: `actionlint` on the edited workflows; confirm SHA-pinned actions.
- **Dry**: push a no-op commit to a `release/**` or branch protection preview to confirm
  build runs without push, or use `act` locally where feasible (Windows caveat — prefer a
  real runner).
- **End-to-end (gated on B3 `terraform apply`)**: merge a trivial passing change to
  `master`; confirm (a) job runs pytest→auth→build→push, (b) `redline-api:<sha>` appears in
  Artifact Registry, (c) the run reports `image_digest`, (d) the digest is pullable.
- **Negative**: a commit with a failing test produces no image and a red run.

## Dependencies / sequencing

Executable acceptance requires B3 (`terraform apply` of `artifact_registry.tf` +
`workload_identity.tf`). The workflow edits can be authored and statically validated now;
the live build/push proves out once the AR repo and WIF binding exist in the project.
Issue #67 (Dockerfile) is already merged; issue #68 (WIF) is already merged.
