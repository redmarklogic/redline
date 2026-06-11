# Implementation Plan: Cloud Run-Ready Container Image for the Marker API

**Branch**: `feature/67-dockerfile-for-fastapi-backend-wraps-build-skeleton-as-api` | **Date**: 2026-06-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/67-dockerfile-for-fastapi-backend-wraps-build-skeleton-as-api/spec.md`

## Summary

Bring the existing committed image definition (`deploy/docker/marker/Dockerfile`, commit 8f666f2) into compliance with the Cloud Run runtime contract: honour the platform-assigned `PORT` (default 8080) instead of hardcoded 8000, keep `/health` answering on the listening port within the startup-probe budget, preserve graceful SIGTERM shutdown with the port change, and align all in-repo consumers (`docker-compose.yml`, `.env.example`). Multi-stage `python:3.14-slim` build, non-root user, and secret-free layers carry forward unchanged and gain explicit verification.

## Technical Context

**Language/Version**: Python 3.14 (container runtime); Dockerfile syntax `docker/dockerfile:1`

**Primary Dependencies**: FastAPI + uvicorn (already in `uv.lock`), uv (build stage only, `ghcr.io/astral-sh/uv`)

**Storage**: N/A — stateless service, no volumes

**Testing**: pytest (existing API contract tests run unchanged inside the container); `rtk docker` build/run smoke verification for container-level behaviour

**Target Platform**: `linux/amd64` container on Google Cloud Run, `australia-southeast1` (ADR-022); also run locally via docker compose on Windows hosts (ADR-019)

**Project Type**: web-service container packaging (no application-code feature work; `src/` changes are out of scope unless verification reveals a port-binding blocker)

**Performance Goals**: cold start to `/health` HTTP 200 within the Cloud Run startup probe budget — 10s initial delay, 5s timeout, 3 failures (`cloud_run.tf`)

**Constraints**:
- `PORT` env honoured, default 8080; the default lives at the container layer, never as an `os.getenv` default in `src/` (ADR-021 / Constitution XVI)
- No secrets in any image layer; `.env` excluded from build context (the `Dockerfile.dockerignore` whitelist already excludes it)
- Image referenced by digest only in deployment; mutable tags rejected by Terraform validation (out of scope to implement — CI concern — but nothing in this feature may depend on a mutable tag)
- LF line endings for Dockerfile and compose (ADR-019 / Constitution XIV)
- No Terraform changes — `cloud_run.tf` already probes `GET /health` on 8080 (Constitution XV: any infra change would be Terraform-only anyway)

**Scale/Scope**: one service image consumed by two Cloud Run services (staging + prod, ADR-023); 3 files touched (`Dockerfile`, `docker-compose.yml`, `.env.example`) plus verification

## Constitution Check

| Principle | Assessment |
|-----------|------------|
| I (SSOT) | Port contract SSOT is `cloud_run.tf` (probe 8080) + Cloud Run's `PORT` injection. The Dockerfile defaults to the same value rather than duplicating authority — Cloud Run's injected `PORT` always wins at runtime. |
| II (Hook-first) | No new project rule introduced; no hook needed. Dockerfile linting is not an existing hook concern. |
| XIV (Platform) | Dockerfile/compose execute on Linux; LF endings required. Local compose flow remains Windows-host compatible. |
| XV (IaC) | No GCP resource change. Image push is an operational command, permitted outside Terraform. |
| XVI (Env-only config) | `PORT` default expressed in the container entrypoint, not in Python. `APP_ENV` passed through compose; secrets only at Cloud Run runtime. No `load_dotenv`, no `os.getenv` defaults introduced. |

**Accepted Risks**:
- `[red-team-skipped]` — the optional red-team gate matched trigger categories `contracts` (runtime contract) and `immutability_audit` (immutable digest) with no findings report on record. Proceeding because the hook is `optional: true` and the feature modifies an existing reviewed artifact against a live, already-reviewed infrastructure contract. Founder may run `/speckit.red-team.run specs/67-dockerfile-for-fastapi-backend-wraps-build-skeleton-as-api/spec.md` at any time before implementation.
- Shaping gate waived — no Pitch in `specs/shaped/`; maintenance-scope work on an existing committed artifact, scope fully bounded by issue #67 + live infra. Waiver recorded 2026-06-11.

## Design Decisions

- **D1 — PORT mechanism**: entrypoint becomes `CMD ["sh", "-c", "exec python -m uvicorn marker.api.main:create_app --factory --host 0.0.0.0 --port ${PORT:-8080} --timeout-graceful-shutdown 10"]`. The `exec` is mandatory: it replaces the shell so uvicorn is PID 1 and receives SIGTERM directly (preserves FR-004). A pure exec-form CMD cannot expand `${PORT}`; uvicorn does not read `PORT` natively.
- **D2 — HEALTHCHECK port**: the Docker `HEALTHCHECK` (used by compose/local only — Cloud Run ignores it and uses its own startup probe) reads the same variable: `CMD python -c "import os,urllib.request; urllib.request.urlopen(f'http://localhost:{os.environ.get(\"PORT\", \"8080\")}/health')"`. Note: `os.environ.get` with a default is permitted here — this is container tooling inside the Dockerfile, not `src/` or `scripts/` (ADR-021 scope).
- **D3 — Compose mapping**: container side moves to 8080; host side stays developer-configurable: `"${MARKER_PORT:-8000}:8080"`. Compose healthcheck targets 8080 internally. Local developer URLs (`localhost:8000`) keep working.
- **D4 — EXPOSE**: documentation-only instruction updated to 8080 to match the default.
- **D5 — No distroless migration**: founder decision 2026-06-11; `python:3.14-slim` stays.
- **D6 — No application-code change expected**: uvicorn binds whatever `--port` receives; `/health` already exists (`src/marker/api/health.py`). If verification finds otherwise, that is an escalation, not silent scope growth.

## Project Structure

### Documentation (this feature)

```text
specs/67-dockerfile-for-fastapi-backend-wraps-build-skeleton-as-api/
├── spec.md                  # Feature specification
├── plan.md                  # This file
├── version-guard-report.md  # Skip artifact (Python/uv project; npm guard N/A)
├── checklists/
│   └── requirements.md      # Spec quality checklist
└── tasks.md                 # Phase 2 output (/speckit.tasks — NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
deploy/
└── docker/
    └── marker/
        ├── Dockerfile               # MODIFY: PORT-aware CMD, HEALTHCHECK, EXPOSE
        ├── Dockerfile.dockerignore  # unchanged (already excludes .env via whitelist)
        └── .env.example             # MODIFY: document PORT (optional, default 8080)

docker-compose.yml                   # MODIFY: container port 8080, healthcheck, mapping

src/                                 # NO CHANGES (D6)
tests/                               # NO CHANGES (container verification is build/run-level)
```

**Structure Decision**: monorepo layout (`.specify/architecture.yml`); all changes confined to the existing `deploy/docker/marker/` service directory and the root compose file, matching the documented `deploy/` convention (`deploy/README.md`).

## Implementation Phases

Each phase maps to a spec user story and is independently verifiable.

### Phase A — PORT-aware image (US1: FR-001, FR-002, FR-008)

Modify the Dockerfile per D1/D2/D4. Build for `linux/amd64`. Verify:
- `PORT=8080` run → `GET localhost:8080/health` returns 200 in < 10s (SC-001, scenario US1-1)
- no `PORT` set → listens on 8080 (SC-002, scenario US1-2)
- `PORT=9000` run → listens on 9000 (SC-002, edge case)

### Phase B — Consumer alignment (US1: FR-007)

Update `docker-compose.yml` (D3) and `.env.example`. Verify: `rtk docker compose up` → healthcheck passes, `localhost:8000/health` reachable from the host.

### Phase C — Graceful shutdown verification (US2: FR-004)

With the D1 entrypoint in place, verify SIGTERM behaviour:
- `docker stop` during an in-flight `POST /skeletons` → request completes, exit code 0, total < 10s (SC-003, scenarios US2-1, US2-2)
- Confirms `exec` made uvicorn PID 1 (a regression here means D1 was implemented without `exec`)

### Phase D — Security posture verification (US3: FR-003, FR-005, FR-006)

No new build work expected; lock in the posture with checks:
- `docker inspect` → user is `appuser`/UID 1000 (SC-004, scenario US3-1)
- runtime stage contains no uv binary and no dev/test dependencies (SC-004, scenario US3-3)
- layer search for secret values comes back empty (SC-005, scenario US3-2)
- authenticated `POST /skeletons` against the container passes the same contract expectations as local (SC-006, scenario US1-3)

### Scenario coverage map

| Spec scenario | Plan phase |
|---|---|
| US1-1 (PORT=8080, /health 200 < 10s) | A |
| US1-2 (PORT unset → 8080) | A |
| US1-3 (POST /skeletons returns DOCX) | D |
| US2-1 (SIGTERM mid-request) | C |
| US2-2 (SIGTERM idle) | C |
| US3-1 (non-root) | D |
| US3-2 (no secrets in layers) | D |
| US3-3 (no build tooling in runtime) | D |
| Edge: arbitrary PORT | A |
| Edge: probe budget on cold start | A |
| Edge: missing secrets, /health still up | A (verify /health without API_KEY set) |
| Edge: compose consistency | B |

## MoSCoW

| Priority | Items |
|---|---|
| Must | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008 (all phases A–D) |
| Should | Documented one-command local smoke check in `.env.example`/`deploy/README.md` comments |
| Could | hadolint Dockerfile lint (new tooling — only if zero friction) |
| Won't (this feature) | CI build-and-push with digest extraction; distroless migration; `/healthz` alias; Terraform changes |

## Domain Impact

None. No geotechnical domain content; Graeme consultation not required. Pure deployment infrastructure.

## Complexity Tracking

No constitution violations to justify. The only nuance — shell-wrapped CMD (D1) — is required by the `PORT` expansion constraint and keeps signal semantics via `exec`; simpler exec-form CMD cannot satisfy FR-001.
