# Feature Specification: Cloud Run-Ready Container Image for the Marker API

**Feature Branch**: `feature/67-dockerfile-for-fastapi-backend-wraps-build-skeleton-as-api`

**Created**: 2026-06-11

**Status**: Draft

**Input**: GitHub issue [redmarklogic/redline#67](https://github.com/redmarklogic/redline/issues/67) — "Dockerfile for FastAPI backend (wraps build_skeleton as API)" plus issue comments (unblock notes from #64 and #66) and founder reconciliation decisions (2026-06-11).

## Source Reconciliation

Authoritative sources, in priority order when they conflict:

| Priority | Source | Authority over |
|----------|--------|----------------|
| 1 | Live infrastructure (`deploy/infra/terraform/cloud_run.tf`, `artifact_registry.tf`) | Probe path, port, registry, image reference format |
| 2 | Issue #67 comments (unblock notes, 2026-06-09/10) | Runtime env vars, registry path, digest-only rule |
| 3 | ADR-021, ADR-022, ADR-023 | Config-from-environment rule, hosting constraints |
| 4 | Issue #67 body | Original intent (multi-stage, non-root, health, SIGTERM) |

Canonical values:

| Item | Value | Source |
|------|-------|--------|
| Health path | `GET /health` (NOT `/healthz`; issue body superseded — founder decision 2026-06-11) | `cloud_run.tf` startup probe; `src/marker/api/health.py` |
| Probe port | 8080 (Cloud Run injects `PORT`; default 8080) | `cloud_run.tf` startup probe |
| Probe budget | initial delay 10s, timeout 5s, failure threshold 3 | `cloud_run.tf` |
| Base image strategy | `python:3.14-slim` multi-stage (distroless rejected — founder decision 2026-06-11) | Existing Dockerfile; founder |
| Registry | `australia-southeast1-docker.pkg.dev/redmarklogic-prod/redline-repo/redline-api` | Issue comment (#66 unblock) |
| Image reference | digest-only (`@sha256:<DIGEST>`); mutable tags rejected by Terraform validation | Issue comment; `variables.tf` |
| Runtime secrets | `API_KEY`, `DB_PASSWORD` injected by Cloud Run from Secret Manager — never baked into the image | Issue comment (#64 unblock); ADR-023 |
| Non-secret env | `APP_ENV` only | ADR-021 |
| Runtime identity | non-root; Cloud Run service account `cloud-run-api-sa@redmarklogic-prod.iam.gserviceaccount.com` | Issue comment |

**Existing artifact decision**: `deploy/docker/marker/Dockerfile` (commit 8f666f2) is **updated in place**, not replaced. Its multi-stage build, non-root user, and graceful-shutdown setup carry forward. The spec covers only the gaps between that file and the Cloud Run runtime contract.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cloud Run operator deploys the image and it becomes ready (Priority: P1)

The operator (Brent, or CI acting on his behalf) builds the image, pushes it to Artifact Registry by digest, and points the Cloud Run service at it. The container starts, listens on the port Cloud Run assigns, answers the startup probe on `/health`, and the service reaches the ready state without manual intervention.

**Why this priority**: This is the entire purpose of the issue — the image is the deployment unit for the first production web flow. Without probe-passing startup on the Cloud Run-assigned port, nothing deploys.

**Independent Test**: Run the container locally with `PORT=8080` set and no other special configuration; `GET /health` on port 8080 returns success within the probe budget (10s initial delay, 5s timeout).

**Acceptance Scenarios**:

1. **Given** the built image, **When** the container starts with environment variable `PORT=8080`, **Then** the application listens on port 8080 and `GET /health` returns HTTP 200 within 10 seconds of container start.
2. **Given** the built image, **When** the container starts with no `PORT` variable set, **Then** the application listens on port 8080 (the Cloud Run default) and `GET /health` returns HTTP 200.
3. **Given** the running container with valid `API_KEY` set, **When** an authenticated `POST /skeletons` request is made, **Then** the response is a valid DOCX document identical in behaviour to a non-containerised run.

---

### User Story 2 - Operator stops or replaces the service without dropping requests (Priority: P2)

When Cloud Run scales down or replaces a revision, it sends the container a termination signal. In-flight requests complete, no new work is accepted, and the process exits cleanly within the termination grace window.

**Why this priority**: Skeleton generation returns a document in a single response; a dropped request means a user-visible failure. Required for safe deploys but the service can technically go live without it being verified.

**Independent Test**: Start the container, issue a request, send SIGTERM mid-request; the request completes and the process exits with code 0 within 10 seconds.

**Acceptance Scenarios**:

1. **Given** a running container with an in-flight request, **When** SIGTERM is delivered to PID 1, **Then** the in-flight request completes successfully and the process exits with code 0 within 10 seconds.
2. **Given** an idle running container, **When** SIGTERM is delivered, **Then** the process exits with code 0 promptly (well under the grace window).

---

### User Story 3 - Security reviewer confirms the image posture (Priority: P3)

A reviewer (SOC 2 evidence trail) inspects the image and confirms: the process runs as a non-root user, the runtime image contains no build tooling or development dependencies, and no secret values exist in any image layer.

**Why this priority**: Already largely satisfied by the existing Dockerfile; this story locks the posture in as verifiable requirements so regressions are caught.

**Independent Test**: Inspect the image — the configured user is non-root (UID 1000), build tools are absent from the runtime stage, and a layer scan finds no secret material.

**Acceptance Scenarios**:

1. **Given** the built image, **When** the effective user is inspected, **Then** it is UID 1000 (`appuser`), not root.
2. **Given** the built image, **When** its layers are searched for `API_KEY` or `DB_PASSWORD` values, **Then** no secret values are present (only variable names may appear in documentation files such as `.env.example`).
3. **Given** the runtime stage of the image, **When** its contents are inspected, **Then** no package installer tooling used only at build time and no development-only dependencies are present.

---

### Edge Cases

- `PORT` set to a non-default value (e.g. 9000): the application must honour it — Cloud Run is free to assign any port.
- Probe fires before the application finishes importing: startup must complete within the probe budget (10s initial delay + 3 retries x 5s timeout) on Cloud Run's smallest configured instance.
- SIGTERM grace window expires with a request still running: the platform sends SIGKILL; the container must not corrupt state (skeleton generation is stateless, so the only requirement is that no partial response is presented as complete).
- Required secrets (`API_KEY`) absent at runtime: per ADR-021 the process assumes its environment is correct; authentication-dependent requests fail at request time — the container itself must still start and pass `/health` (the health endpoint requires no secrets).
- Local developer compose flow: `docker-compose.yml` port mapping and healthcheck must stay consistent with whatever port behaviour the image adopts.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The container MUST listen on the port given by the `PORT` environment variable, defaulting to 8080 when unset. The currently hardcoded port 8000 violates the Cloud Run contract and MUST be removed.
- **FR-002**: The container MUST serve `GET /health` returning HTTP 200 on the listening port, with total cold-start-to-healthy time inside the Cloud Run startup probe budget (10s initial delay, 5s timeout, 3 failures).
- **FR-003**: The container process MUST run as a non-root user (carried forward from the existing Dockerfile; UID/GID 1000).
- **FR-004**: On SIGTERM, the container MUST stop accepting new connections, let in-flight requests finish, and exit 0 within a 10-second graceful-shutdown window.
- **FR-005**: The image MUST be built in multiple stages so the runtime stage contains the application and its production dependencies only — no build tooling, no development or test dependencies.
- **FR-006**: The image MUST NOT contain any secret values. `API_KEY` and `DB_PASSWORD` are injected at runtime by the platform; `APP_ENV` is the only non-secret environment variable the deployment sets directly (ADR-021/ADR-023).
- **FR-007**: All consumers of the image inside the repository (`docker-compose.yml` port mapping, healthcheck command, and `deploy/docker/marker/.env.example`) MUST be updated to stay consistent with the `PORT` behaviour in FR-001.
- **FR-008**: The image MUST be buildable for `linux/amd64` (the Cloud Run target platform), regardless of the developer's host platform (ADR-019: Windows dev, Linux deployment).

### Key Entities

- **Container image**: the single deployable unit — multi-stage build on `python:3.14-slim`, holding the Marker API application and production dependencies; identified in deployment exclusively by immutable digest.
- **Runtime contract**: the set of environment inputs the platform provides (`PORT`, `APP_ENV`, `API_KEY`, `DB_PASSWORD`) and probes it performs (`GET /health`); the image must function given exactly these inputs and nothing else.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A container started with `PORT=8080` and no other special setup answers `GET /health` with HTTP 200 in under 10 seconds from start.
- **SC-002**: The same image started with `PORT` unset, or set to an arbitrary valid port, behaves identically on that port — zero configuration changes needed between local and Cloud Run runs.
- **SC-003**: A SIGTERM delivered during an in-flight skeleton request results in a completed response and a clean exit (code 0) within 10 seconds, in 100% of test runs.
- **SC-004**: Image inspection shows a non-root configured user and a runtime layer set free of build tooling and dev/test dependencies.
- **SC-005**: A search of all image layers finds zero secret values.
- **SC-006**: An authenticated `POST /skeletons` request against the running container returns a DOCX response that passes the same contract tests as the non-containerised application.

## Assumptions

- The health path is `/health` (founder decision 2026-06-11); the issue body's `/healthz` is superseded by live infrastructure and the implemented endpoint.
- The base image remains `python:3.14-slim`; distroless was considered and rejected (founder decision 2026-06-11).
- The existing committed Dockerfile is the starting point and is updated in place, not rewritten.
- CI build-and-push automation (digest extraction after push, wiring into the deploy pipeline) is **out of scope** for this issue — this issue delivers the image definition and its local verification only. The digest-only rule constrains how the image is *referenced*, which CI implements separately.
- The "B1" symbolic dependency flagged in the issue comments was resolved by #64/#66 going live (Artifact Registry and Cloud Run infrastructure exist); no further baseline work blocks this issue.
- The application requires no secrets to start and serve `/health`; only `/skeletons` requires `API_KEY` at request time.
- Skeleton generation is stateless; no volume mounts or persistence requirements exist for this image.
