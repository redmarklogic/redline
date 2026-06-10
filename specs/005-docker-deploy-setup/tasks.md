# Tasks: Docker Deploy Setup

**Input**: [plan.md](plan.md)
**Prerequisites**: Docker Desktop installed and running; `src/marker/` codebase present

<!-- Task sizing rule: each task is a VERTICAL SLICE -- front-to-back, one complete
     new behaviour, nothing left dangling. Do not split by technical layer.
     Split by user-visible behaviour. -->

<!-- NOTE: This feature has no pytest tasks. Verification is container-level smoke
     tests via docker CLI and docker compose. The pytest gate in acceptance gates
     is replaced by a docker build/run gate. -->

## Phase 1: Deploy Layout

**Purpose**: Establish the monorepo deploy directory structure and exclusion rules so all downstream tasks have a stable location to write into.

- [x] T001 [US4] Create `deploy/docker/marker/` directory (empty, ready for Dockerfile)
- [x] T002 [US4] Create `deploy/modules/README.md` — explain directory purpose and naming convention for future infra scripts
- [x] T003 [US4] Create `.dockerignore` at repo root — exclude `.venv/`, `__pycache__/`, `.git/`, `*.pyc`, `specs/`, `docs/`, `.specify/`, `.agents/`

### Acceptance Gate

- [x] T004 [US4] Verify layout: `Test-Path deploy/docker/marker`, `Test-Path deploy/modules/README.md`, `Test-Path .dockerignore` — all return True

---

## Phase 2: Container Image (US1 + US2)

**Purpose**: Working, buildable container image. `docker build` succeeds, container serves `GET /health` → 200, runs as non-root, exits cleanly on SIGTERM.

### Implementation

- [x] T005 [US1] Create `deploy/docker/marker/Dockerfile` — builder stage: `python:3.14-slim`, install uv, copy `pyproject.toml` + `uv.lock`, run `uv sync --frozen --no-dev --no-install-project --link-mode=copy`
- [x] T006 [US2] Add runtime stage to `deploy/docker/marker/Dockerfile` — `python:3.14-slim`, copy `.venv` from builder, create non-root `appuser` (UID 1000), copy `src/`, set `ENV PYTHONPATH=/app/src`, `USER appuser`, `EXPOSE 8000`
- [x] T007 [US1] Add `HEALTHCHECK` to runtime stage in `deploy/docker/marker/Dockerfile` — `--interval=10s --timeout=3s --retries=3 --start-period=15s` probing `GET /health`
- [x] T008 [US2] Add `CMD` to runtime stage in `deploy/docker/marker/Dockerfile` — `["python", "-m", "uvicorn", "marker.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-graceful-shutdown", "10"]`

### Acceptance Gate

- [x] T009 [US1] Build image: `docker build --platform linux/amd64 -t marker:local -f deploy/docker/marker/Dockerfile .` — exits 0
- [x] T010 [US1] Run container and probe health: StatusCode 200, body `{"status":"healthy"}`
- [x] T011 [US1] Confirm non-root: `docker exec marker-test whoami` — returns `appuser`
- [x] T012 [US2] Confirm graceful stop: `docker stop marker-test` — exit code 0

---

## Phase 3: Docker Compose (US3)

**Purpose**: `docker compose up` brings the backend online at `http://localhost:8000` with no manual steps beyond `docker compose up`.

### Implementation

- [x] T013 [US3] Create `docker-compose.yml` at repo root — single `marker` service, `build.context: .`, `build.dockerfile: deploy/docker/marker/Dockerfile`, `platform: linux/amd64`, ports `${MARKER_PORT:-8000}:8000`, `APP_ENV` env var, healthcheck matching Dockerfile
- [x] T014 [P] [US3] Create `deploy/docker/marker/.env.example` — document `MARKER_PORT` (default 8000), `APP_ENV` (default development), and any future vars

### Acceptance Gate

- [x] T015 [US3] Bring stack up: StatusCode 200 on `http://localhost:8000/health`
- [x] T016 [US3] Confirm compose health status: `docker compose ps` — marker service shows status `healthy`
- [x] T017 [US3] Tear down cleanly: `docker compose down` — no project-prefixed volumes remain

---

## Phase 4: Polish

- [x] T018 [P] [US4] Create `deploy/README.md` — document the layout convention: `deploy/docker/<service>/Dockerfile` for images, `deploy/modules/` for infra scripts; include example of adding a second service
- [x] T019 [P] Verify image size: 66 MB — well under 300 MB
- [x] T020 [P] Confirm platform: `amd64`
- [x] T021 Smoke-test `MARKER_PORT` override: `MARKER_PORT=9001 docker compose up -d; Invoke-WebRequest http://localhost:9001/health; docker compose down` — StatusCode 200

### Acceptance Gate

- [x] T022 All Phase 2 and Phase 3 acceptance gates pass on a clean `docker build --no-cache`

---

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies)
- `[USN]` = maps to User Story N in spec.md
- No pytest in this feature — all verification is docker CLI smoke tests
- Used `python:3.14-slim` (Python 3.14 is stable as of June 2026; uv.lock requires >=3.14)
- Used `--link-mode=copy` in `uv sync` — project sets `link-mode = "symlink"` in pyproject.toml which breaks multi-stage builds (symlinks point to builder cache not present in runtime stage)
- Used `python -m uvicorn` in CMD — script-based invocation fails when venv is copied across stages; module invocation uses PATH-resolved Python directly
- Created `src/marker/main.py` as entry point — tasks reference `marker.main:app` but only `marker.api.main:create_app` existed
- Acceptance Gate at the end of each phase is a hard stop — do not start the next phase until it passes
- Use `finishing-a-development-branch` skill to complete the work
