# Feature Specification: Django Project Skeleton

**Feature Branch**: `feature/159-django-project-skeleton`

**Created**: 2026-06-12

**Status**: Draft

**Input**: GitHub issue [#159](https://github.com/redmarklogic/redline/issues/159) — "Django project skeleton". Purpose: serves Bet 1 (Free Skeleton Wedge) -> KR1 SSO-gated signup. First Django in repo. Source: `docs/product/tasks/sprint-3-goal.md` (WBS 1.1). Done when: `manage.py runserver` returns 200 on `/`; `manage.py check` clean; Django added to pyproject deps.

**Governing decisions**: ADR-024 (Django web stack, single service) fixed the framework choice; this spec does not re-litigate it. Layer ownership per `docs/architecture/layer-responsibilities.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Boot the web shell locally (Priority: P1)

A developer on the team clones the repository, installs dependencies with the standard project install, starts the development server, and receives a successful page response at the root URL. This is the sprint's anchor task: every other Sprint 3 task (settings, data layer, SSO, deploy) builds on a bootable web shell, and the Wednesday tripwire ("Django app running in the cloud") depends on it existing first.

**Why this priority**: Issue #159 is the root of the Sprint 3 dependency graph (`1.1 -> (1.3, 2.1)`, `1.1 -> 6.2`). Nothing downstream can start until the shell boots.

**Independent Test**: On a fresh clone, run the documented install and server-start commands; request `/` and observe HTTP 200.

**Acceptance Scenarios**:

1. **Given** a fresh clone with dependencies installed, **When** the developer starts the development server and requests `/`, **Then** the response status is HTTP 200 (issue done-when: "`manage.py runserver` returns 200 on `/`").
2. **Given** the running development server, **When** the developer requests `/`, **Then** a minimal placeholder page is returned — no sign-in, navigation, or product content (those arrive in #167–#173).

---

### User Story 2 - Machine-checkable configuration health (Priority: P2)

A developer (or CI job) runs the framework's built-in system check and gets a clean result, proving the project configuration is internally consistent without booting a server or talking to any external service.

**Why this priority**: The issue's second done-when ("`manage.py check` clean") is the regression tripwire downstream tasks (#161 settings, #164 databases) will re-run after every change they make to the skeleton.

**Independent Test**: Run the system check in a headless shell with no database or network access; observe zero reported issues.

**Acceptance Scenarios**:

1. **Given** the skeleton as merged, **When** the system check runs locally or headless (CI), **Then** it reports zero issues and exits 0.
2. **Given** the skeleton as merged, **When** the system check runs with no external services (no database server, no network), **Then** it still completes cleanly.

---

### User Story 3 - Reproducible dependency declaration (Priority: P3)

A developer adds the web framework to the project's dependency manifest so any teammate or CI runner resolves the identical version set with the standard install command.

**Why this priority**: Issue done-when ("Django added to pyproject deps"). Without the manifest entry and updated lockfile, US1 and US2 work only on the original author's machine.

**Independent Test**: On a clean environment, run the standard dependency install from the manifest; the framework resolves and imports.

**Acceptance Scenarios**:

1. **Given** the merged manifest and lockfile, **When** a teammate runs the standard project install on a clean environment, **Then** the framework installs at the locked version and the server boots (US1) without manual steps.

---

### Edge Cases

- Fresh clone, no prior environment: boot must require only documented standard commands (install, run) — no undocumented setup steps.
- Headless / no-database environment (CI): the system check must pass without a provisioned database; database wiring belongs to #164.
- Existing API coexistence: the current walking-skeleton API (`src/marker`) keeps working; its test suite passes unchanged. Fixed-port convention (FR-008): marker on 8765, Django on 8766, port 8000 never used — both apps run side by side via `tasks/run-app.ps1`.
- Repeated boots: starting and stopping the dev server repeatedly leaves no state requiring cleanup.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The repository MUST contain a runnable web-application shell project whose development server serves the root URL `/` with HTTP 200.
- **FR-002**: The shell project MUST pass the framework's built-in system check with zero reported issues, both locally and in a headless environment with no external services.
- **FR-003**: The web framework dependency MUST be declared in the project dependency manifest (`pyproject.toml`) with the lockfile updated, so the standard project install resolves it reproducibly.
- **FR-004**: The shell project MUST be placed as a web-shell-layer package. No web-framework import may be introduced into the domain, schemas, or functions packages (ADR-024 guardrail; the automated import contract itself is delivered by #160, but this slice must not create violations for it to find).
- **FR-005**: All pre-existing application surfaces and their tests (the `src/marker` API walking skeleton, `src/rl` core) MUST remain passing — this slice is additive.
- **FR-006**: The root URL response MUST be a minimal placeholder: no authentication, no session behaviour, no product content (deferred to #167–#173 per the sprint WBS).
- **FR-007**: The shell project MUST expose a `/health/` endpoint that returns HTTP 200 with JSON body `{"status": "healthy"}` — no auth, no DB access, no side effects. This is the infrastructure liveness probe consumed by `run-app.ps1` and later by Cloud Run startup probes (#177).
- **FR-008**: `tasks/run-app.ps1` MUST start both the marker (FastAPI) and web (Django) development servers on every invocation — no mode switch, no parameters. Project-convention ports are fixed constants in the script: marker on 8765, Django on 8766 (never 8000 — reserved by common tooling). If either port is already occupied by any process, the script MUST fail immediately with a clear error naming the PID; wildcard-bound listeners (`0.0.0.0`/`::`) count as occupying the port; it MUST NOT kill foreign processes. Before launching either server it MUST run `manage.py check` synchronously, capture stdout and stderr, and abort if exit code is non-zero (log-analysis gate). After both servers start it MUST poll `GET /health` (marker) and `GET /health/` (Django); if any app does not respond 200 within 30 seconds the script MUST report which app failed and exit non-zero (fail closed — callers read the exit code).

### Out of Scope (this slice)

| Concern | Owned by |
|---|---|
| Settings from environment / 12-factor boot | #161 |
| Layer-guard import contract (automated enforcement) | #160 |
| HTMX vendoring | #162 |
| Database configuration and migrations | #164 |
| User/identity models, audit log | #165, #166 |
| SSO (Google, Microsoft) | #167, #168 |
| Cloud Run deployment on merge | #177 |
| Removal or pivot of the `src/marker` FastAPI adapter | Parent #153 follow-on work |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer on a fresh clone reaches a running local web shell with a successful root-page response using at most the documented install + run commands (two commands), in under 5 minutes.
- **SC-002**: The configuration system check reports 0 issues in both interactive and headless runs.
- **SC-003**: The pre-existing test suite passes at the same rate as before this change (zero new failures).
- **SC-004**: The four directly dependent Sprint 3 tasks (#160 layer-guard, #161 settings, #162 HTMX, 6.2/#177 deploy) plus transitive #164 can start against the merged skeleton without restructuring it (their stated inputs — a bootable project, a settings module location, a dependency entry — all exist).
- **SC-005**: `tasks/run-app.ps1` (no arguments) starts both apps: `manage.py check` reports zero issues before any server launches, marker is live at `http://127.0.0.1:8765/health`, Django is live at `http://127.0.0.1:8766/health/`, both return HTTP 200 within 30 seconds.

## Assumptions

- ADR-024 governs the stack: the framework decision (Django, no DRF, server-rendered templates) is made; this feature only lands the skeleton. The spec names the framework where the issue's done-when criteria do.
- The existing FastAPI walking skeleton (`src/marker`) coexists with the new shell during the pivot; removing or pivoting it is parent-scope (#153 / ADR-024 item 9), not this slice.
- Framework-default project-local configuration (including the default local database backend reference in settings) is acceptable for this slice; environment-only configuration lands in #161 (ADR-021 compliance is that task's done-when, not this one's).
- The root placeholder page carries no commitment to final UI; #171 replaces it with the auth-gated button page.
- Framework version: current stable LTS line, pinned at plan time after a version-compatibility check against the repo's `requires-python = ">=3.14"` (version-guard gate before planning).
- Exact package name and path for the shell inside the `src/` monorepo layout (per `.specify/architecture.yml`: monorepo, hub package `rl`) is a plan-phase decision guided by `docs/architecture/layer-responsibilities.md` ("Django project package, new in the pivot" — a sibling of, not inside, the domain packages).
- Implementation is performed by Kabilan on founder instruction (issue: "Kabilan implements"); this spec/plan/tasks pipeline stops before implementation.
