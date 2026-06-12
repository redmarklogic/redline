# Tasks: Django Project Skeleton

**Input**: [plan.md](plan.md)
**Prerequisites**: spec.md, plan.md, research.md (D1–D7), version-guard-report.md,
contracts/root-page.md, quickstart.md. Branch `feature/159-django-project-skeleton`.

**Binding constraints (version-guard)**: Django 5.2 LTS only — consult
`https://docs.djangoproject.com/en/5.2/` exclusively; no 6.0-only APIs (template
partials, `django.tasks`, built-in CSP). Constraint `django>=5.2.8,<6` — the `<6` cap
is load-bearing (research.md D1).

**Sequencing trap (do not reorder)**: the pyproject `[tool.pytest]`
`DJANGO_SETTINGS_MODULE` line and the hatch wheel-packages `"src/web"` entry MUST land
in the same change as the generated `src/web` package (Phase 1). Adding either while
`src/web` does not exist breaks pytest collection / the editable install for the whole
repo (plan.md Structure Decision; research.md D2).

## Phase 0: Dependency declaration

**Purpose**: Django resolves from the manifest at a locked 5.2.x — issue done-when 3.

- [ ] T001 [Phase 0] In `pyproject.toml`: append `"django>=5.2.8,<6"` to
      `[project] dependencies`; append `"pytest-django>=4.12"` to
      `[dependency-groups] test`. Touch nothing else yet (see Sequencing trap).
- [ ] T002 [Phase 0] Regenerate the lockfile: `rtk uv sync`. Inspect `uv.lock` and
      confirm the resolved `django` version is `5.2.x` (>=5.2.8, not 6.x) — this
      proves the cap works.

### Acceptance Gate

- [ ] T003 [Phase 0] Verify working code:
      `rtk uv run python -c "import django; print(django.get_version())"` prints a
      `5.2.x` version.
- [ ] T004 [Phase 0] Run pytest: `rtk uv run pytest` — existing suite green,
      zero new failures (spec FR-005).

---

## Phase 1: Bootable skeleton package

**Purpose**: `src/web` exists, imports, and `manage.py check` reports zero issues —
issue done-when 2.

- [ ] T005 [Phase 1] Generate the skeleton:
      `rtk uv run django-admin startproject web src`, then `git mv src/manage.py manage.py`
      (root placement per research.md D2/D3; generated manage.py is path-independent).
- [ ] T006 [Phase 1] Conform generated files to repo conventions: module docstring in
      `src/web/__init__.py` (house precedent `src/rl/domain/__init__.py`); keep
      generated docstrings elsewhere; LF line endings (Constitution XIV); make NO
      functional edits to `settings.py` (env-only boot is #161 — do not start it).
- [ ] T007 [Phase 1] In `pyproject.toml`, same commit as T005/T006: append
      `"src/web"` to `tool.hatch.build.targets.wheel.packages`; add
      `ini_options.DJANGO_SETTINGS_MODULE = "web.settings"` under `[tool.pytest]`;
      re-run `rtk uv sync` to refresh the editable install.

### Acceptance Gate

- [ ] T008 [Phase 1] Verify working code: `rtk uv run python -c "import web"` succeeds
      AND `rtk uv run python manage.py check` prints
      `System check identified no issues (0 silenced).` with exit code 0, headless
      (no database, no network).
- [ ] T009 [Phase 1] Run pytest: `rtk uv run pytest` — existing suite green (pytest
      collection must survive the pytest-django wiring).

---

## Phase 2: Root page serves 200 (TDD)

**Purpose**: `GET /` returns a 200 placeholder page — issue done-when 1, contract
`contracts/root-page.md`.

### Tests (write first — must fail before implementation begins)

- [ ] T010 [Phase 2] Write tests in `tests/web/test_skeleton.py` (new file, both
      DB-free per research.md D5): `test_root_url_returns_200` — Django test client
      `GET /` expects 200 and `text/html` content type (will FAIL: startproject
      urlconf serves only `admin/`); `test_system_check_clean` —
      `django.core.management.call_command("check")` raises nothing (passes already —
      regression pin for done-when 2, not a Red test; mark with a comment).
- [ ] T011 [Phase 2] Confirm the Red state:
      `rtk uv run pytest tests/web/test_skeleton.py -v` — `test_root_url_returns_200`
      fails with 404; `test_system_check_clean` passes.

### Implementation

- [ ] T012 [Phase 2] Create `src/web/views.py`: one function view named `root`
      returning a minimal placeholder HTML 200 response (`django.http.HttpResponse`;
      no template, no DB, no session access — contract root-page.md; research.md D4).
- [ ] T013 [Phase 2] Edit `src/web/urls.py`: add `path("", views.root)` ahead
      of the existing `admin/` entry; keep the admin route (ADR-024 admin-at-launch;
      non-functional until #164/#165 — documented, not removed).

### Acceptance Gate

- [ ] T014 [Phase 2] Verify working code: `rtk uv run pytest tests/web/ -v` — both
      tests green. Then the manual done-when check per quickstart.md §3:
      `rtk uv run python manage.py runserver 127.0.0.1:8766` and
      `GET http://127.0.0.1:8766/` returns HTTP 200 (port 8766 is the project
      convention for the Django app — never 8000; the unapplied-migrations warning
      is expected — quickstart "Expected oddities").
- [ ] T015 [Phase 2] Run pytest: `rtk uv run pytest` — full suite green.

---

## Phase 3: Health endpoint and run-app.ps1 integration

**Purpose**: Infrastructure liveness probe at `/health/` (FR-007) and developer launcher
script updated with log-analysis gate (FR-008, SC-005).

### Tests (write first — must fail before implementation begins)

- [ ] T019 [Phase 3] In `tests/web/test_skeleton.py`, add `test_health_returns_200` —
      Django test client `GET /health/` expects 200 and `application/json` content type,
      and JSON body `{"status": "healthy"}` (will FAIL: endpoint does not exist yet).

### Implementation

- [ ] T020 [Phase 3] In `src/web/views.py`, add a `health` function view that returns
      `django.http.JsonResponse({"status": "healthy"})` — no DB access, no auth, no
      session (contract: `contracts/health-endpoint.md`).
- [ ] T021 [Phase 3] In `src/web/urls.py`, add `path("health/", views.health)` ahead
      of the root entry. Trailing slash is Django convention; `APPEND_SLASH = True`
      (startproject default) handles redirect from `/health`.

### Acceptance Gate

- [ ] T022 [Phase 3] `rtk uv run pytest tests/web/ -v` — all three tests green
      (root 200, health 200, check clean).

---

## Phase 4: run-app.ps1 launcher update

**Purpose**: Single command starts both apps with log-analysis gating and liveness
checks before the browser opens (FR-008, SC-005).

Port convention (fixed constants — never use 8000):

- marker (FastAPI): **8765**
- web (Django): **8766**

- [ ] T023 [Phase 4] Update `tasks/run-app.ps1` (already implemented — verify and
      confirm it matches the spec):
      - No parameters. Both apps always start.
      - Port guard: `Get-NetTCPConnection` on each port before launch; if occupied by
        any PID, print error naming the PID and `exit 1` — do NOT kill the process.
      - Django pre-flight: run `manage.py check` synchronously, capture stdout+stderr;
        if exit code is non-zero, print output and `exit 1`.
      - Start both server windows via `Start-Process pwsh -NoExit`.
      - Poll `http://127.0.0.1:8765/health` (marker) and
        `http://127.0.0.1:8766/health/` (Django), check `StatusCode -eq 200`.
      - Open browser tabs: `/docs` (marker) and `/` (Django) once each is ready.

### Acceptance Gate

- [ ] T024 [Phase 4] Manual verification (SC-005): run `tasks/run-app.ps1` with no
      arguments — system check output shows zero issues, both server windows open,
      marker ready at `http://127.0.0.1:8765/health`, Django ready at
      `http://127.0.0.1:8766/health/`, both browser tabs open.
      Then confirm port-guard: with port 8766 artificially occupied, script prints
      the offending PID and exits without starting either server.

---

## Phase Z: Polish

- [ ] T016 [Phase Z] Run full static gates: `rtk prek run --all-files` — ruff
      (D/INP rules on new files), deptry (django must register as used — no DEP002
      entry), import-linter (existing contracts untouched), codespell. Prefer fixing
      findings over adding ignores; a per-file ignore for root `manage.py` is the
      only pre-approved exception (research.md D7), and only if a rule actually fires.
- [ ] T017 [Phase Z] Walk quickstart.md end-to-end on a clean environment
      (`rtk uv sync` then §2–§4 verbatim) — proves spec SC-001 (two commands to a
      running shell) and SC-002.

### Acceptance Gate

- [ ] T018 [Phase Z] All tests green, all static gates clean, quickstart walkthrough
      evidence recorded in the PR description (commands + output).

## Execution Notes

- `[P]` = parallelizable — none marked: this slice is a strict dependency chain with
  heavy single-file (pyproject.toml) contention.
- Phase mapping to spec stories: Phase 0 = US3, Phase 1 = US2 (+ US1 foundation),
  Phase 2 = US1, Phase Z = cross-cutting regression proof (FR-005, SC-001–SC-003).
- TDD is mandatory for function work: Red (T010–T011) before Green (T012–T013).
- Each Acceptance Gate is a hard stop — do not start the next phase until it passes.
- If `filterwarnings = ["error"]` trips on a Django/pytest-django deprecation warning
  during T009/T011, add the narrowest matching filter with a comment — never a
  blanket ignore (research.md D5).
- Commit after each task or logical group. Implementation is Kabilan's, on founder
  instruction only.
- Use `subagent-driven-development` skill (preferred) or execute tasks directly.
- Run `python-static-checks` before declaring implementation complete.
- Use `finishing-a-development-branch` skill to complete the work.
