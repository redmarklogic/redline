# Tasks: Cloud Run-Ready Container Image for the Marker API

**Input**: Design documents from `specs/67-dockerfile-for-fastapi-backend-wraps-build-skeleton-as-api/`

**Prerequisites**: plan.md, spec.md

**Tests**: Container-level verification commands are part of each slice (the spec's acceptance scenarios are operational, not pytest-level). No `src/` or `tests/` changes expected (plan D6).

**Organization**: Vertical slices grouped by user story; each checkpoint leaves the repo shippable.

## Format: `[ID] [P?] [Story] Description`

---

## Phase 1: Setup

No setup tasks — the service directory, Dockerfile, compose file, and `.env.example` all exist. Constitution and plan constraints loaded (version-guard-report.md is a skip artifact; no compatibility rules apply).

---

## Phase 2: Foundational

No foundational tasks — single-file change surface, no shared prerequisites.

---

## Phase 3: User Story 1 — PORT-aware image, probe-compatible startup (P1) — MVP

**Goal**: Container honours `PORT` (default 8080) and answers `GET /health` within the Cloud Run startup-probe budget.

**Independent Test**: `rtk docker run -e PORT=8080 -p 8080:8080 <image>` → `GET localhost:8080/health` returns 200 within 10s of start.

- [x] T001 [US1] Update `deploy/docker/marker/Dockerfile` CMD per plan D1: `CMD ["sh", "-c", "exec python -m uvicorn marker.api.main:create_app --factory --host 0.0.0.0 --port ${PORT:-8080} --timeout-graceful-shutdown 10"]`. The `exec` keyword is mandatory (uvicorn must be PID 1 for FR-004).
- [x] T002 [US1] Update `deploy/docker/marker/Dockerfile` HEALTHCHECK per plan D2 to probe `localhost:${PORT:-8080}/health`, and change `EXPOSE 8000` to `EXPOSE 8080` (plan D4).
- [x] T003 [US1] Build for the Cloud Run platform and verify FR-008: `rtk docker build --platform linux/amd64 -f deploy/docker/marker/Dockerfile -t marker:67-dev .` completes successfully.
- [x] T004 [US1] Verify port behaviour (SC-001, SC-002; scenarios US1-1, US1-2, edge "arbitrary PORT"):
  - `PORT=8080` → `/health` 200 on 8080 within 10s of container start
  - no `PORT` env → `/health` 200 on 8080
  - `PORT=9000` → `/health` 200 on 9000
  - container started with NO `API_KEY` set → `/health` still 200 (edge "missing secrets")

**Checkpoint**: Image satisfies the Cloud Run runtime contract; deployable in principle.

---

## Phase 4: User Story 1 consumer alignment — compose + env docs (P1, FR-007)

**Goal**: All in-repo consumers consistent with the 8080-default behaviour.

**Independent Test**: `rtk docker compose up` → service healthy, `GET localhost:8000/health` reachable from host.

- [x] T005 [US1] Update `docker-compose.yml` per plan D3: port mapping `"${MARKER_PORT:-8000}:8080"`, healthcheck URL targets port 8080 inside the container.
- [x] T006 [P] [US1] Update `deploy/docker/marker/.env.example`: document `PORT` (optional, default 8080, injected by Cloud Run in production; compose maps host `MARKER_PORT` onto it).
- [x] T007 [US1] Verify compose flow (edge "compose consistency"): `rtk docker compose up --build -d` → healthcheck reaches healthy; `GET localhost:8000/health` returns 200 from the Windows host; `rtk docker compose down`.

**Checkpoint**: Local developer flow and production contract agree; FR-001/002/007/008 complete.

---

## Phase 5: User Story 2 — Graceful shutdown verification (P2, FR-004)

**Goal**: SIGTERM drains in-flight requests and exits 0 within 10s.

**Independent Test**: `docker stop` during an in-flight request → request completes, exit code 0.

- [x] T008 [US2] Verify SIGTERM handling (SC-003; scenarios US2-1, US2-2):
  - start container; issue an authenticated `POST /skeletons`; run `rtk docker stop <container>` while the request is in flight → response completes successfully, `rtk docker inspect <container> --format '{{.State.ExitCode}}'` shows 0, total stop time < 10s
  - idle container: `rtk docker stop` → exit 0 promptly
  - if uvicorn is NOT PID 1 inside the container (`rtk docker exec <container> ps -o pid,comm` or equivalent), T001 was implemented without `exec` — fix and re-verify

**Checkpoint**: Safe deploys verified; US1 + US2 both hold.

---

## Phase 6: User Story 3 — Security posture verification (P3, FR-003, FR-005, FR-006)

**Goal**: Non-root, build-tool-free, secret-free image — locked in with explicit checks.

**Independent Test**: Image inspection alone; no running container needed (except US1-3 end-to-end check).

- [x] T009 [P] [US3] Verify non-root (SC-004; scenario US3-1): `rtk docker inspect marker:67-dev --format '{{.Config.User}}'` returns `appuser`; in-container `id -u` returns 1000.
- [x] T010 [P] [US3] Verify runtime stage purity (SC-004; scenario US3-3): no `uv` binary present in the final image; no dev/test packages (e.g. pytest, ruff) importable in the runtime venv.
- [x] T011 [P] [US3] Verify no secrets in layers (SC-005; scenario US3-2): `rtk docker history marker:67-dev --no-trunc` and a filesystem search of the exported image show no secret values; `.env` confirmed absent (dockerignore whitelist excludes it).
- [x] T012 [US3] End-to-end contract check (SC-006; scenario US1-3): authenticated `POST /skeletons` against the running container returns a valid DOCX with the ADR-018 headers (Content-Type, Content-Disposition), matching non-containerised behaviour.

**Checkpoint**: All user stories verified independently.

---

## Phase 7: Polish

- [x] T013 [P] Add a one-command local smoke-check comment to `deploy/docker/marker/.env.example` or `deploy/README.md` (plan Should item).
- [x] T014 Confirm LF line endings on `deploy/docker/marker/Dockerfile` and `docker-compose.yml` (Constitution XIV) and run `rtk prek run --all-files` clean.

---

## Dependencies & Execution Order

- T001 → T002 (same file, sequential) → T003 (build needs both) → T004
- T005/T006 after T004 passes ([P] between themselves); T007 after both
- T008 requires T003 image and a valid local `API_KEY` env for the in-flight request
- T009–T011 only require the T003 image ([P]); T012 requires a running container
- T013/T014 last

MVP = Phases 3–4 (US1). Phases 5–6 are verification-heavy and can run same-session.

## Out of Scope (do not implement here)

- CI build-and-push with digest extraction (separate issue; digest-only rule is a deployment-reference constraint)
- Terraform changes (`cloud_run.tf` already correct)
- `/healthz` alias, distroless base, `src/` changes
