# Feature Specification: Docker Deploy Setup

**Feature Branch**: `005-docker-deploy-setup`

**Created**: 2026-06-10

**Status**: Draft

**Input**: Issue #67 — multi-stage slim/distroless image, non-root, SIGTERM handler, /health probe; deploy layout ./deploy/docker/ and ./deploy/modules/; Docker Compose; monorepo-aware.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Build and Run Backend Container (Priority: P1)

A developer builds the FastAPI backend image and runs it as a container. The container starts, passes its health probe, and serves the API identically to the bare Python process.

**Why this priority**: This is the primary deliverable — all other stories depend on a working image.

**Independent Test**: Build the image, run it, send `GET /health` — expect `200 OK` with `{"status": "healthy"}`. Confirms the service is alive and the build is correct.

**Acceptance Scenarios**:

1. **Given** a clean checkout, **When** the image is built from `deploy/docker/marker/Dockerfile`, **Then** the build completes without error and produces a runnable image.
2. **Given** the container is running, **When** `GET /health` is sent with no headers, **Then** the response is `200 OK` with body `{"status": "healthy"}`.
3. **Given** the container is running, **When** `POST /skeletons` is called with a valid token and payload, **Then** the response is a DOCX file — the API is fully functional inside the container.

---

### User Story 2 — Graceful Shutdown (Priority: P2)

An operator stops or restarts the container. In-flight requests complete and the process exits cleanly — no half-written responses, no zombie processes.

**Why this priority**: Production and CI both rely on clean shutdown. A container that ignores SIGTERM and is force-killed after a timeout leaves in-flight work incomplete.

**Independent Test**: Start the container, trigger a slow request, send SIGTERM — confirm the in-flight request completes and the process exits with code 0 within the grace window.

**Acceptance Scenarios**:

1. **Given** the container is running with an in-flight request, **When** SIGTERM is sent, **Then** the in-flight request completes before the process exits.
2. **Given** SIGTERM is sent, **When** no in-flight requests exist, **Then** the process exits with code 0 within 10 seconds.
3. **Given** the container runs as a non-root user, **When** SIGTERM is received, **Then** the signal reaches the application process (not swallowed by an init wrapper).

---

### User Story 3 — Local Stack via Docker Compose (Priority: P3)

A developer starting a local session brings up the full backend stack with a single command. No manual image-building step, no port conflicts, no missing environment variables.

**Why this priority**: Developer experience. Without Compose, each developer must remember build flags, port mappings, and env vars. Compose makes onboarding and iteration fast.

**Independent Test**: From a clean environment, run `docker compose up` — confirm the backend is reachable at a known local address within 30 seconds.

**Acceptance Scenarios**:

1. **Given** a clean environment with Docker installed, **When** `docker compose up` is run from the project root or `deploy/` directory, **Then** the backend service is reachable at its configured local address within 30 seconds.
2. **Given** `docker compose up` is running, **When** `GET /health` is sent to the local address, **Then** the response is `200 OK`.
3. **Given** `docker compose down` is run, **When** the command completes, **Then** all containers are stopped and removed with no dangling volumes.

---

### User Story 4 — Monorepo-Aware Deploy Layout (Priority: P4)

A developer adding a second service to the monorepo knows exactly where to place its Dockerfile and infra modules. The naming convention is self-evident from existing files.

**Why this priority**: Establishes the pattern all future services follow. Getting this wrong now means retrofitting the layout later.

**Independent Test**: The directory structure under `deploy/` is documented and a second service can be added by following the pattern without asking anyone.

**Acceptance Scenarios**:

1. **Given** the deploy layout is established, **When** a developer inspects `deploy/docker/`, **Then** they see one subdirectory per service, each containing its `Dockerfile`.
2. **Given** the deploy layout is established, **When** a developer inspects `deploy/modules/`, **Then** they see infrastructure modules organised by concern, with a clear naming convention.
3. **Given** a future service is added, **When** its Dockerfile is placed at `deploy/docker/<service-name>/Dockerfile`, **Then** `docker compose` can reference it without restructuring existing files.

---

### Edge Cases

- What happens when the image is built on a machine with a different CPU architecture (arm64 vs amd64)? The build must specify the target platform explicitly so CI and local builds produce compatible images.
- What happens if the non-root user inside the container lacks write permissions to a temp directory the app needs? App must either not write to the filesystem or target a directory that the non-root user owns.
- What happens when the health probe is called before the app has finished startup? The probe must only return 200 after the ASGI server is accepting connections — not on process start.
- What happens if a developer has a port conflict on the local host? The Compose file must document the port mapping and how to override it via an environment variable or `.env` file.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The build system MUST produce a container image for the `marker` FastAPI service using a multi-stage build that minimises final image size.
- **FR-002**: The final container image MUST run all processes as a non-root user.
- **FR-003**: The container MUST handle SIGTERM by completing in-flight requests and exiting cleanly within a configurable grace period (default: 10 seconds).
- **FR-004**: The container MUST expose a health check that probes `GET /health` and reports healthy when the service responds `200 OK`.
- **FR-005**: A Docker Compose configuration MUST bring up the backend stack with a single `docker compose up` command.
- **FR-006**: All Dockerfiles MUST reside under `deploy/docker/<service-name>/Dockerfile`.
- **FR-007**: All infrastructure modules and scripts MUST reside under `deploy/modules/`.
- **FR-008**: The Docker Compose file MUST reference service Dockerfiles by relative path so the layout is self-contained.
- **FR-009**: The deploy layout MUST support adding further services without restructuring existing files.
- **FR-010**: The target platform (amd64/arm64) MUST be specified explicitly in the build configuration so cross-architecture builds are deterministic.

### Key Entities

- **Service image**: The built container image for a single service. Identified by service name and version tag. Has a build context, Dockerfile path, and target platform.
- **Deploy layout**: The directory structure under `deploy/` — `docker/<service>/Dockerfile` for images, `modules/` for infra scripts. Governs where all deployment artefacts live.
- **Compose stack**: The set of services defined in the Docker Compose file. Describes port mappings, env vars, health checks, and inter-service dependencies.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Container starts and passes its health probe within 30 seconds of launch — zero false-negative health failures on a clean start.
- **SC-002**: Container exits cleanly within 10 seconds of receiving SIGTERM — no force-kill required.
- **SC-003**: No process inside the running container runs as UID 0 — verified by inspecting the container's process list.
- **SC-004**: `docker compose up` brings the backend online with zero manual steps beyond installing Docker — confirmed by a developer following the README from a clean clone.
- **SC-005**: Final image size is under 300 MB — multi-stage build removes build tooling from the runtime layer.
- **SC-006**: A second service can be added to the monorepo deploy layout by following the existing pattern, with no changes to the `marker` service configuration.

## Assumptions

- The `marker` FastAPI service (issue #51) is the first and currently the only service being containerised; the layout must anticipate additional services but need not automate their addition.
- `deploy/modules/` holds infrastructure scripts (e.g., startup scripts, init helpers) — not Terraform or cloud-provider modules unless explicitly decided later.
- Docker Compose is used for local development only; production deployment topology is out of scope for this spec.
- The health endpoint at `GET /health` returning `{"status": "healthy"}` is the authoritative liveness probe — per `src/marker/api/health.py` and spec 004. Issue #67's `/healthz` reference is a typo.
- No external services (database, cache) are required by the `marker` service at this stage; the Compose file contains a single service.
- The grace period for SIGTERM handling defaults to 10 seconds; this matches common container orchestration defaults and can be overridden via env var.
- Platform target defaults to `linux/amd64` (CI and Cloud Run); local arm64 developers build with `--platform linux/amd64` or enable multi-platform builds.
