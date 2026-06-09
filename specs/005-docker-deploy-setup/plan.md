# Implementation Plan: Docker Deploy Setup

**Date**: 2026-06-10 | **Spec**: [spec.md](spec.md)
**Status**: Draft

## Summary

We are introducing the container build and local development stack for the `marker` FastAPI service (the API from issue #51). The deliverable is a multi-stage `Dockerfile` under `deploy/docker/marker/`, a `docker-compose.yml` at the repo root for single-command local startup, and a placeholder `deploy/modules/` directory for future infrastructure scripts. This change establishes a monorepo-aware deploy layout so additional services can be added without reorganising existing files. No Python application code changes. The runtime image is a non-root, slim Python image with a SIGTERM-aware uvicorn process targeting `linux/amd64` (Cloud Run + CI).

## Technical Context

**Language**: Python 3.14
**Package manager**: uv
**Testing**: pytest (N/A for this feature — verification is container-level smoke tests via docker CLI)
**Project layout**: monorepo (`src/marker/`)
**Architecture**: FastAPI service containerised with multi-stage Docker build; orchestrated locally with Docker Compose v2
**Dev OS**: Windows | **Deploy OS**: Linux
**Domain modeling**: N/A (infrastructure feature, no new domain models)
**Layer enforcement**: N/A (no new Python packages)
**Key dependencies**: Docker (build + runtime), Docker Compose v2, uvicorn (already in service)

## Design Decisions

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| D1 | Health probe path | `GET /health` | Authoritative per `src/marker/api/health.py`; issue #67's `/healthz` is a typo |
| D2 | Runtime base image | `python:3.14-slim` | Distroless Python requires manually copying the venv — adds complexity without proportionate gain at this stage; slim is lean and debuggable |
| D3 | SIGTERM handling | Native uvicorn + `--timeout-graceful-shutdown 10` | uvicorn handles SIGTERM natively when started as PID 1 via `CMD ["uvicorn", ...]`; no init shim needed |
| D4 | Non-root user | Dedicated `appuser` (UID 1000) created in Dockerfile | Standard pattern; avoids runtime UID conflicts |
| D5 | Compose file location | Repo root `docker-compose.yml` | Developer ergonomics: `docker compose up` works from project root without `-f` flags; Dockerfiles referenced via relative path |
| D6 | Platform target | `linux/amd64` | Cloud Run and CI are amd64; arm64 developers build with `--platform linux/amd64` |
| D7 | `deploy/modules/` initial content | Placeholder `README.md` only | No infra scripts exist yet; establishes the convention for future CI scripts and startup helpers |

## Domain Impact

**Modularity assessment**: N/A — no new Python packages. All new files are Docker/YAML/docs under `deploy/`.
**New packages**: None
**Bounded context changes**: None
**Import-linter contract updates**: None
**Subdomain classification**: Generic (off-the-shelf Docker tooling, no custom domain logic)
**New domain terms**: None

## Architecture

### Deploy layout

```text
deploy/
  docker/
    marker/
      Dockerfile        # multi-stage, non-root, linux/amd64
      .env.example      # documents required and optional env vars
  modules/
    README.md           # placeholder; future: startup scripts, CI helpers
docker-compose.yml      # repo root — local dev stack entry point
.dockerignore           # repo root — excludes .venv, __pycache__, .git, specs, docs
```

### Dockerfile — multi-stage structure

```dockerfile
# Stage 1: builder (python:3.13-slim — upgrade to 3.14-slim when published)
  COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
  COPY pyproject.toml uv.lock ./
  RUN uv sync --frozen --no-dev --no-install-project

Stage 2: runtime (python:3.13-slim)
  COPY --from=builder /app/.venv /app/.venv
  RUN addgroup --gid 1000 appgroup && adduser --uid 1000 --gid 1000 appuser
  COPY src/ /app/src/
  ENV PYTHONPATH=/app/src
  USER appuser
  EXPOSE 8000
  HEALTHCHECK --interval=10s --timeout=3s --retries=3 --start-period=15s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
  CMD ["uvicorn", "marker.main:app", "--host", "0.0.0.0", "--port", "8000",
       "--timeout-graceful-shutdown", "10"]
```

### Docker Compose structure

```yaml
services:
  marker:
    build:
      context: .
      dockerfile: deploy/docker/marker/Dockerfile
    platform: linux/amd64
    ports:
      - "${MARKER_PORT:-8000}:8000"
    environment:
      - APP_ENV=${APP_ENV:-development}
    healthcheck:
      test: ["CMD", "python", "-c",
             "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 15s
```

### Signal flow — SIGTERM

```text
docker stop / compose down
    -> SIGTERM -> uvicorn (PID 1)
    -> uvicorn drains in-flight requests (up to --timeout-graceful-shutdown 10s)
    -> uvicorn exits 0
    -> Docker removes container
```

## MoSCoW

| Category | Items |
|----------|-------|
| **Must have** | `deploy/docker/marker/Dockerfile` (multi-stage, non-root, SIGTERM), `docker-compose.yml` at repo root, health probe on `GET /health`, `deploy/modules/README.md` placeholder, `.dockerignore` |
| **Should have** | Explicit `platform: linux/amd64` in compose build config, `MARKER_PORT` env var override, `deploy/docker/marker/.env.example` |
| **Could have** | Multi-platform build targeting arm64, `docker-compose.override.yml` for local dev secrets |
| **Won't have (this time)** | Terraform / cloud-provider modules in `deploy/modules/`, CI pipeline integration, production image push, multi-service compose stack |

## Phased Delivery

### Phase 0: Deploy Layout + Dockerfile

**Goal**: Working, buildable container image for the `marker` service. `docker build` succeeds and `GET /health` returns 200 in a running container.

**TDD approach**: No pytest — verification is manual `docker build` + PowerShell health check probe.

**Deliverables**:

1. `deploy/docker/marker/Dockerfile` — multi-stage, non-root appuser, HEALTHCHECK, CMD uvicorn
2. `deploy/modules/README.md` — placeholder explaining directory purpose and naming convention
3. `.dockerignore` — excludes `.venv/`, `__pycache__/`, `.git/`, `*.pyc`, `specs/`, `docs/`

**Verification**:

```powershell
# Build
rtk docker build --platform linux/amd64 -t marker:local -f deploy/docker/marker/Dockerfile .

# Run
rtk docker run --rm -d --name marker-test -p 8000:8000 marker:local

# Health probe
Invoke-WebRequest http://localhost:8000/health
# Expected: StatusCode 200, Content: {"status":"healthy"}

# Confirm non-root
rtk docker exec marker-test whoami
# Expected: appuser

# Confirm clean SIGTERM
rtk docker stop marker-test
# Expected: exits within 10s, exit code 0
rtk docker logs marker-test | Select-String "Shutting down"
```

**Acceptance Gate** (both must pass before Phase 1 starts):

- [ ] Working code: image builds and `GET /health` returns 200 in a running container
- [ ] Container exits within 10 seconds of `docker stop` with exit code 0

---

### Phase 1: Docker Compose + Smoke Validation

**Goal**: `docker compose up` brings the backend online at `http://localhost:8000`. Single command, no manual steps.

**TDD approach**: Shell-level smoke: `docker compose up -d` → poll `/health` → assert 200 → `docker compose down`.

**Deliverables**:

1. `docker-compose.yml` (repo root) — single-service `marker` stack, platform `linux/amd64`, `MARKER_PORT` override
2. `deploy/docker/marker/.env.example` — documents `MARKER_PORT`, `APP_ENV`, and any future vars

**Verification**:

```powershell
rtk docker compose up -d
Start-Sleep -Seconds 20

Invoke-WebRequest http://localhost:8000/health
# Expected: 200 OK, {"status":"healthy"}

rtk docker compose ps
# Expected: marker service status "healthy"

rtk docker compose down
# Expected: containers stopped, no dangling volumes
rtk docker volume ls
# Expected: no project-prefixed volumes remain
```

**Acceptance Gate** (both must pass before marking complete):

- [ ] Working code: `docker compose up -d` → service healthy within 30s → `GET /health` returns 200
- [ ] `docker compose down` completes cleanly with no dangling volumes

## File Inventory

| Phase | New Files | Count |
|-------|-----------|-------|
| 0 | `deploy/docker/marker/Dockerfile`, `deploy/modules/README.md`, `.dockerignore` | 3 |
| 1 | `docker-compose.yml`, `deploy/docker/marker/.env.example` | 2 |

**Total new**: 5 | **Total deleted**: 0

## Library Best Practices

### uvicorn (graceful shutdown)

- **Import path**: `uvicorn` (already a project dependency)
- **API gotchas**: `--timeout-graceful-shutdown` defaults to 0 (no wait). Must set explicitly.
- **Confirmed pattern**: `CMD ["uvicorn", "marker.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-graceful-shutdown", "10"]` — uvicorn as PID 1 receives SIGTERM directly.

### Docker multi-stage build with uv

- **Pattern**: Builder stage installs deps into `/app/.venv` via `uv sync --frozen --no-dev`; runtime stage copies only `.venv` and `src/` — build tooling never enters the runtime layer.
- **uv in builder**: `COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv` — pin to a digest in production.
- **PYTHONPATH**: Set `ENV PYTHONPATH=/app/src` so `marker.main` is importable without editable install.

## Risk Register

| Risk | Mitigation |
|------|------------|
| uvicorn fails to find `marker.main:app` inside container | Set `ENV PYTHONPATH=/app/src` in runtime stage; verify with `docker run --entrypoint python marker:local -c "from marker.main import app"` |
| Non-root user lacks write permission to dirs used by report generation | Audit `build_skeleton()` for filesystem writes; ensure target dirs owned by `appuser` or point to `/tmp` |
| `python:3.14` not yet stable on Docker Hub | Use `python:3.13-slim` as fallback; update to 3.14 once image is published; pin exact digest |
| Port conflict on developer machine | `MARKER_PORT` env var in compose overrides the host port; documented in `.env.example` |
| Cross-platform build fails on arm64 developer machine | Explicit `platform: linux/amd64` in compose and `--platform linux/amd64` in build command |

## Glossary

| Term | Definition |
|------|------------|
| Deploy layout | The directory convention under `deploy/` governing where Dockerfiles and infrastructure scripts live for each service in the monorepo |
| Graceful shutdown | Completing in-flight requests before a service process exits after receiving SIGTERM |
| Multi-stage build | A Docker build technique using a heavyweight builder to install dependencies, copying only runtime artefacts into a lean final image |
