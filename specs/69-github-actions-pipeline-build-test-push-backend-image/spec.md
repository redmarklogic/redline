# Feature Specification: Backend Image CI Pipeline (build, test-gated, push to Artifact Registry)

**Feature Branch**: `feature/69-github-actions-pipeline-build-test-push-backend-image`

**Created**: 2026-06-11

**Status**: Draft

**Input**: GitHub issue #69 — "GitHub Actions pipeline: build, test, push backend image". Purpose: action builds image, runs pytest (blocks on fail), pushes to Artifact Registry. Owner: Brent (DevOps). Part of epic #89 (walking-skeleton deploy chain, #63–#72). Blocked by B3/B4/B5.

## Context

This is the publish link of the walking-skeleton deploy chain (#89). Once the backend
test gate is green on the trunk, a container image of the backend must be built and
published to the project's image registry so the downstream Cloud Run deploy step has
a tested, traceable artifact to release. Without this link, deploys would pull
untested or hand-built images, breaking the chain's "tested artifact in, deploy out"
guarantee.

Governing decisions: ADR-022 (Cloud Run + Artifact Registry, `australia-southeast1`),
ADR-019 (Windows-dev / Linux-CI boundary — CI runs on Linux), ADR-023 (single
environment for now; staging/prod split is later), and #68 (Workload Identity
Federation — CI authenticates to the cloud without long-lived keys).

**Existing scaffold (reconciliation, 2026-06-11).** #68 already landed
`.github/workflows/ci.yml`: a single job that checks out, runs pytest, authenticates to
the cloud via Workload Identity Federation, and then holds a placeholder step
explicitly tagged for this issue (`TODO — build and push image … issue #69`). #69
**completes that job in place** — it appends build + push (emitting the image digest)
after the existing test and auth steps. It does not introduce a separate workflow.

**Two pre-existing defects #69 also corrects:** (a) both `ci.yml` and `tests.yml`
trigger on `push: branches: [main]`, but the repository's default branch is `master`,
so neither fires on trunk merges today — the trunk CI is dormant; #69 corrects both
triggers to `master`. (b) Per #67's digest-only rule, the deploy step references images
by **digest**, so the publish step must emit the pushed digest as its primary output.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Tested backend image published on every trunk merge (Priority: P1)

When a change merges to the trunk (master) and the automated test gate has passed, a
container image of the backend is built and published to the image registry, ready for
the deploy step to release.

**Why this priority**: This is the MVP. The deploy chain cannot release anything until
a tested image reliably lands in the registry on merge. Everything else is a guardrail
around this outcome.

**Independent Test**: Merge a trivial passing change to master; confirm a new image
appears in the registry tagged with that commit, and that the deploy step can resolve
and pull it.

**Acceptance Scenarios**:

1. **Given** a change is merged to master and the test gate passed, **When** the
   pipeline runs, **Then** a backend image is built and pushed to the registry.
2. **Given** the image was pushed, **When** the deploy step looks it up by commit,
   **Then** the exact tested image is resolvable and pullable.

---

### User Story 2 - Failed tests publish nothing (Priority: P1)

When the automated test gate fails on the trunk, no image is built or published — the
registry never contains an image from an untested or failing commit.

**Why this priority**: Equal-critical guardrail to Story 1. An untested image in the
registry is worse than no image, because the deploy chain trusts whatever is published.

**Independent Test**: Introduce a failing test on a branch, merge it (or simulate a
failed gate on master); confirm the pipeline does not run the build/push, the run is
marked failed, and no new image lands in the registry.

**Acceptance Scenarios**:

1. **Given** the test gate failed for a commit, **When** the pipeline is evaluated,
   **Then** no build runs and no image is pushed.
2. **Given** a build or push step itself fails, **When** the run completes, **Then**
   the run is reported failed and no partially-tagged or broken image is left
   published.

---

### User Story 3 - Every published image is traceable to its source commit (Priority: P2)

Each published image is identified by its content digest and tagged with the commit it
was built from, so the deploy step can pull an exact digest and any deployed artifact can
be traced back to source.

**Why this priority**: Provenance and a digest handoff are required for the deploy step's
lookup, rollback, and debugging, but the chain can run a first demo before traceability
is perfected — hence P2, not P1.

**Independent Test**: Merge two changes in sequence; confirm each image carries its own
commit tag and a distinct digest, and the pipeline surfaces the digest of the image it
just pushed.

**Acceptance Scenarios**:

1. **Given** a merge to master, **When** the image is pushed, **Then** it is tagged with
   the immutable commit identifier and the run surfaces the pushed image digest.
2. **Given** two merges in sequence, **When** both images are published, **Then** each
   commit tag resolves to its own image and each run reports its own digest.

---

### Edge Cases

- Test gate passes but the image build fails → run is marked failed, nothing is pushed.
- Build succeeds but the push (registry write / auth) fails → run failed, no partial or
  mistagged image published; safe to re-run.
- Two merges land close together → commit-pinned tags never collide; the moving trunk
  tag reflects the most recently completed publish.
- The same commit is re-run after a successful publish → re-pushing is safe: the
  `:<commit>` tag may move to the newly built digest, but already-pushed digests stay
  immutable and pullable, so digest-pinned deploys are unaffected (FR-011).
- A required precondition is missing (backend Dockerfile not yet present, registry
  repository not provisioned, or cloud auth not configured) → the run fails with a clear,
  actionable error rather than silently producing nothing or a broken image.
- A push to a feature branch or a pull request → the pipeline does not build or push (it
  acts only on trunk merges).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The pipeline MUST act only on merges to the trunk (`master`). Pushes to
  feature branches and pull requests MUST NOT build or publish an image. As part of this
  work, the existing `ci.yml` and `tests.yml` triggers MUST be corrected from `main` to
  `master` so trunk CI fires (pre-existing dormant-trigger defect).
- **FR-002**: The pipeline MUST run the automated test gate (pytest) before any build or
  push, and MUST proceed to build/push only when that gate passes. This is implemented by
  completing the existing `ci.yml` job in place (test → auth → build → push), not by a
  separate workflow. (The existing `tests.yml` continues to provide PR-time feedback.)
- **FR-003**: When the test gate fails for the commit, the pipeline MUST NOT build or
  publish any image.
- **FR-004**: The pipeline MUST build the backend container image from the repository's
  backend container definition at `deploy/docker/marker/Dockerfile` (delivered by #67).
- **FR-005**: The pipeline MUST publish the built image to the project's Artifact
  Registry repository in `australia-southeast1` (per ADR-022), using the image reference
  established by #67 (`…/redline-repo/redline-api`).
- **FR-006**: The publish step MUST emit the pushed image **digest** as its primary,
  machine-readable output for the downstream deploy step (#67 digest-only rule). It MUST
  also tag the image with the immutable triggering commit identifier for human
  traceability.
- **FR-007**: The pipeline MUST authenticate to the cloud using keyless Workload Identity
  Federation (the auth step already present from #68); it MUST NOT store or use
  long-lived cloud credentials.
- **FR-008**: The pipeline MUST run on a Linux execution environment (per ADR-019).
- **FR-009**: Any failure in the build or publish steps MUST fail the run visibly and
  MUST NOT leave a partial or broken image published.
- **FR-010**: The published image digest MUST be discoverable by the downstream deploy
  step so it can resolve and pull the exact tested artifact without a manual tagging step.
- **FR-011**: Re-running the pipeline for an already-published commit MUST be safe.
  **Policy (POC):** a re-run rebuilds and re-pushes; because container builds are not
  bit-reproducible, the moving `:<commit>` tag MAY be repointed to the newly built digest.
  Previously pushed **digests remain immutable and pullable**, so any deploy that pinned a
  digest (FR-006/FR-010) is unaffected — provenance is preserved by the digest, not the
  tag. No skip-if-exists logic is required for the POC. (If, later, the `:<commit>` tag
  must be immutable, enforce it via registry tag-immutability rather than pipeline logic —
  out of scope here.)

### Key Entities

- **Backend container image**: the publishable artifact; tagged with its source commit
  and a moving trunk tag; stored in the registry repository.
- **Test gate result**: the pass/fail conclusion of the existing automated test
  workflow for a given commit; the precondition that authorises build/publish.
- **Source commit**: the provenance key linking a published image back to exact source.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of images in the registry correspond to a commit whose test gate
  passed — zero untested images are ever published.
- **SC-002**: A passing merge to the trunk results in a deploy-ready image published to
  the registry within 10 minutes of the test gate completing.
- **SC-003**: 100% of published images are traceable to their exact source commit via
  their tag.
- **SC-004**: Zero long-lived cloud credentials are stored in or used by the pipeline.
- **SC-005**: A failing test gate results in zero images published for that commit.
- **SC-006**: The downstream deploy step can resolve and pull the published image for a
  given trunk commit on the first attempt, with no manual tagging step.

## Assumptions

- The backend container definition (Dockerfile) exists and builds a runnable image
  (#67 / B4). This pipeline consumes it; it does not author it.
- An image registry repository is provisioned in `australia-southeast1` and the
  pipeline's identity has permission to write to it (infra precondition, B3 —
  `deploy/infra/terraform/artifact_registry.tf`, `workload_identity.tf` grant
  `roles/artifactregistry.writer`).
- Keyless cloud federation and a CI identity with registry-writer permission are
  configured and applied (#68 — `WIF_PROVIDER`/`GHA_SA_EMAIL` repo vars, auth step already
  present in `ci.yml`). This pipeline assumes them; it does not provision them.
- The test gate (pytest) runs inline in the same job as build/push, before them; the
  existing `tests.yml` continues to provide independent PR-time feedback.
- A single deployment environment applies for now (ADR-023); the pipeline targets the
  one registry repository. A staging/prod split, if introduced later, is out of scope
  here.
- Image retention/cleanup policy in the registry is governed separately (infra) and is
  out of scope for this pipeline.

## Dependencies

- **#67 (B4)** — backend Dockerfile at `deploy/docker/marker/Dockerfile` and the
  `redline-api` image reference / digest-only rule. Blocking for executable acceptance.
- **B3** — Artifact Registry repository provisioned (push target). Terraform present
  (`artifact_registry.tf`); blocking on `terraform apply`.
- **#68** — Workload Identity Federation + CI service account with registry-writer role.
  **Merged**; the auth step and `ci.yml` scaffold are already in place.
- **ADR-022** (Cloud Run + Artifact Registry, region), **ADR-019** (Linux CI),
  **ADR-023** (single environment for now) — governing decisions.

## Out of Scope

- Provisioning the registry repository, the Dockerfile, or the cloud identity (separate
  blocked-by issues).
- The Cloud Run deploy/release step itself (downstream issue in #89).
- Multi-environment (staging/prod) image promotion (ADR-023 — later).
- Registry image retention / garbage-collection policy.
- Re-running or owning the unit/integration test suite (the existing test workflow owns
  that gate).
