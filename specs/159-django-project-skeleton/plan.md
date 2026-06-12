# Implementation Plan: Django Project Skeleton

**Branch**: `feature/159-django-project-skeleton` | **Date**: 2026-06-12 | **Spec**: [spec.md](spec.md)
**Status**: Draft

**Input**: Feature specification from `specs/159-django-project-skeleton/spec.md`

## Summary

Land the first Django project in the monorepo: a bootable web-shell skeleton that
serves HTTP 200 on `/`, passes `manage.py check` cleanly with no database or network,
and declares Django in `pyproject.toml`. It is the root of the Sprint 3 dependency
graph (settings #161, layer-guard #160, HTMX #162, Cloud Run deploy #177 all build on
it) and the first physical artifact of ADR-024's FastAPI-to-Django pivot. The slice is
strictly additive: `src/marker` (FastAPI walking skeleton) and `src/rl` (framework-free
generator core) are untouched. Approach: generate the canonical skeleton with
`django-admin startproject`, conform it to repo conventions, add one placeholder root
view, and verify with two DB-free pytest-django smoke tests.

## Technical Context

**Language/Version**: Python 3.14 (`requires-python = ">=3.14"`)

**Primary Dependencies**: `django>=5.2.8,<6` (5.2 LTS — version-guard-report.md;
cap is load-bearing, see research.md D1). Dev/test: `pytest-django` (test group).

**Storage**: None in this slice. Generated DATABASES stanza stays inert (no migrate,
no DB file). Cloud SQL wiring is #164.

**Testing**: pytest + pytest-django, DB-free smoke tests under `tests/web/`
(`GET /` == 200; `call_command("check")` clean). Existing suite must stay green.

**Target Platform**: Linux container (Cloud Run) at deploy time (#177); authored on
Windows — Constitution XIV (pathlib, LF) applies.

**Project Type**: Web-service shell package inside the existing `src/` monorepo.

**Performance Goals**: N/A — placeholder page; no load characteristics this slice.

**Constraints**: Additive-only (FR-005); no framework import may reach `rl`/`marker`
(FR-004, Constitution XVIII); no env-var reads added (XVI letter — 12-factor boot
is #161); all-Python toolchain (XVII).

**Scale/Scope**: 7 new source files (6 package modules + root `manage.py`) + 1 test
file + pyproject wiring. No data model, no auth, no UI beyond one placeholder response.

## Constitution Check

*GATE: evaluated before Phase 0 research; re-checked after design. Constitution v1.8.0.*

| Principle | Verdict | Notes |
|---|---|---|
| I (SSOT) | PASS | Skeleton generated from upstream `startproject` (canonical source); no duplicated authority introduced |
| II (Hook-first) | PASS | No new rule introduced here; the django-import ban becomes an import-linter contract in #160 (already a sprint task) |
| V (Facade boundaries) | PASS | No layer crossing added — placeholder view calls nothing in `rl` |
| X (Raise on failure) | PASS | No failure-signalling code in slice; generated boilerplate returns no sentinels |
| XIV (Platform by deployment) | PASS | `pathlib.Path` BASE_DIR (5.2 default), LF endings; runs on Windows dev + Linux CI |
| XVI (Env as sole config) | PASS (letter) / DEFERRED (spirit) | Generated settings read no env vars and use no dotenv — the letter holds. Hard-coded dev `SECRET_KEY` + `DEBUG=True` are the startproject baseline; "boots from env only, DEBUG=False boots" is exactly #161's done-when (sprint WBS 1.3). **Accepted Risk**, owned by #161. |
| XVII (All-Python) | PASS | Django is Python; no second toolchain |
| XVIII (Stateless core / framework in shell) | PASS | Django confined to new `src/web`; `rl`/`marker` untouched; no ORM models created at all |

**Red-team gate (before_plan, optional hook)**: triggers matched on keyword scan —
`regulatory_path` ("compliance"), `immutability_audit` ("audit log"), `contracts`
("contract", "schema") — all occurrences sit in the spec's Out-of-Scope table and
governance references, not in delivered behaviour. No findings report exists.
**WAIVED — Accepted Risk [red-team-skipped]**: "Slice ships an unauthenticated static
placeholder page; every triggering keyword refers to work owned by #160/#161/#165/#166.
Red team re-qualifies when those slices enter spec-kit." Founder may override by
requesting `/speckit.red-team.run` before implementation.

**Deploy-order risk (recorded for the sprint, not this slice)**: WBS dependency
`1.1 -> 6.2` lets the Cloud Run deploy (#177) ship this skeleton before settings
hardening (#161). If that ordering occurs, staging serves `DEBUG=True` behind the
founder-IP ingress lock (#178). Sprint accepts this for the Wednesday tripwire,
and #161 is day-1 work specifically to close the window fast.

## Project Structure

### Documentation (this feature)

```text
specs/159-django-project-skeleton/
├── spec.md
├── plan.md                    # this file
├── research.md                # Phase 0 — decisions D1–D7
├── data-model.md              # Phase 1 — records "no entities this slice"
├── quickstart.md              # Phase 1 — install/run/verify commands
├── version-guard-report.md    # before_plan hook output (binding constraints)
├── contracts/
│   └── root-page.md           # GET / placeholder contract
├── checklists/
│   └── requirements.md
└── tasks.md                   # Phase 2 (/speckit.tasks — not created by plan)
```

### Source Code (repository root)

```text
manage.py                      # NEW — Django CLI entry (moved from src/, path-independent)
src/
├── marker/                    # existing FastAPI walking skeleton — UNTOUCHED
├── rl/                        # existing generator core (domain/schemas/functions) — UNTOUCHED
├── scripts/                   # existing — UNTOUCHED
└── web/                       # NEW — Django web shell (ADR-024 layer home)
    ├── __init__.py            # module docstring (ruff D104, house precedent)
    ├── settings.py            # startproject baseline, 5.2 defaults, no env reads
    ├── urls.py                # path("", views.root) + default admin/ route
    ├── views.py               # NEW — root view (HTTP 200 placeholder) + health view (FR-007)
    ├── asgi.py                # generated entry point (used by #177)
    └── wsgi.py                # generated entry point

tests/
└── web/
    └── test_skeleton.py       # NEW — smoke: GET / == 200; GET /health/ == 200; check() clean; DB-free

tasks/
└── run-app.ps1                # MODIFIED — add -App django branch (FR-008)

pyproject.toml                 # MODIFIED:
                               #   [project] dependencies += "django>=5.2.8,<6"
                               #   [dependency-groups] test += "pytest-django>=4.12"
                               #   [tool.hatch] build.targets.wheel.packages += "src/web"
                               #   [tool.pytest] ini_options.DJANGO_SETTINGS_MODULE = "web.settings"
uv.lock                        # regenerated by uv
```

**Structure Decision**: `src/web` package + root `manage.py`, settings module
`web.settings` (research.md D2/D3). The single repo-specific trap: hatchling's wheel
package list is explicit — omitting `"src/web"` means `import web` fails everywhere.

## Phase 0 — Research

Complete: [research.md](research.md). Decisions D1 (version), D2 (placement),
D3 (generation method), D4 (root view + admin route), D5 (test harness), D6 (no DB),
D7 (lint/packaging seams). No NEEDS CLARIFICATION remained.

## Phase 1 — Design & Contracts

- **Data model**: none this slice — [data-model.md](data-model.md) records the empty
  set and points at #165/#166 for the first real models.
- **Contracts**: [contracts/root-page.md](contracts/root-page.md) — `GET /` returns
  `200 text/html`, no auth, no cookies required, body content placeholder-only.
  The ADR-018 envelope does NOT apply to this page (it is not the API surface);
  envelope middleware is #176.
- **Quickstart**: [quickstart.md](quickstart.md) — install, boot, verify, and the
  two expected oddities (unapplied-migrations warning; admin route present but
  non-functional until #164/#165).
- **Agent context update**: skipped — `.github/copilot-instructions.md` does not
  exist in this repo checkout.

## Phase 2 — Task Generation Approach

`/speckit.tasks` decomposes along the user stories: US3 (dependency declaration)
first — it unblocks everything; then US1 (skeleton boots, placeholder view) with
tests-first ordering; then US2 (check clean headless) as the verification slice;
closing with regression proof (full suite green) per FR-005. Version-guard
Compatibility Rules (5.2-only APIs) bind every task.

## Complexity Tracking

| Violation / deviation | Why needed | Simpler alternative rejected because |
|-----------|------------|-------------------------------------|
| Version cap `<6` deviates from floor-only dependency style | uv resolves highest available — floor-only installs Django 6.0.6, defeating the LTS decision (D1) | Floor-only pin: silently lands the wrong major |
| XVI spirit deferred (hard-coded dev SECRET_KEY, DEBUG=True) | startproject baseline; #161 owns env-only boot as its done-when | Doing #161's work here: breaks one-slice-one-task sprint decomposition and its dependency order |
| Red-team gate waived [red-team-skipped] | Keyword hits are out-of-scope references only; no qualifying surface ships | Running red team on a placeholder page: ceremony without findings surface |
| `/health/` returns JSON on the web (template) surface | Liveness probe consumed by `run-app.ps1` and Cloud Run (#177) — JSON is the universal probe format; the view has no user-facing role | Returning HTML: `run-app.ps1` would need an HTML parser to verify the response; JSON equality is trivial |
| `manage.py check` used as the startup log-analysis gate in `run-app.ps1` | Django's built-in system check validates all installed apps, URL patterns, and settings before the server opens a socket — it IS the startup log | Grepping the `runserver` stdout window: `Start-Process` spawns a separate terminal; stdout is not capturable without subprocess redirection that breaks the interactive dev-server UX |
| `run-app.ps1` fails hard on port conflict instead of killing the occupant | Port 8765 and 8766 are fixed constants — a foreign process on either port is always unexpected state; auto-killing it destroys unknown work silently | Silent kill: a developer running SonarQube or another tool on the same port loses their session with no warning |
| Both apps always start — no `-App` mode switch | A mode switch introduces a latent variable: the developer must remember which mode they ran, and the health-check URLs differ between modes, increasing cognitive load | `-App` flag: two mental models for the same script; port 8766 vs 8765 becomes context-dependent rather than fixed |
