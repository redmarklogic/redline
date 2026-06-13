# Tasks: Settings + 12-Factor Config

**Input**: [plan.md](plan.md)
**Prerequisites**: spec.md, plan.md, research.md (D1–D8), data-model.md,
version-guard-report.md, quickstart.md. Branch `feature/161-settings-12-factor-config`.
Builds on the merged #159 skeleton (`src/web`, root `manage.py`, `web.settings`/`web.settings_test`).

**Binding constraints (version-guard)**: `pydantic-settings>=2.7` (new dep, floor-only).
The `Settings` class MUST use `SettingsConfigDict(env_file=None, enable_decoding=False)`
and parse the comma-separated host list with a `field_validator(mode="before")` — a list
field without it raises a JSON error (version-guard-report.md §"Binding API constraints").
Django pin `>=5.2.8,<6` MUST NOT be widened. ADR-021 hooks (`check-no-env-loader`,
`check-no-env-defaults`) MUST pass with no new `# hook: allow` in production source.

**Sequencing trap (do not reorder)**: the moment `src/web/settings.py` instantiates
`Settings()` at import (Phase 2), `from web.settings import *` in `src/web/settings_test.py`
will raise `ValidationError` and break pytest collection for the WHOLE repo unless the
test-settings env bootstrap lands in the SAME change. Phase 1 (the `config.py` class + its
unit tests) is safe in isolation because it does not touch `web.settings`. (Mirrors #159's
"pytest wiring + package in one change" trap — plan.md Phase 2; research.md D3.)

## Phase 0: Dependency declaration

**Purpose**: `pydantic-settings` resolves from the manifest at a Python-3.14-compatible 2.x — plan dep gate.

- [ ] T001 [Phase 0] In `pyproject.toml`, append `"pydantic-settings>=2.7"` to
      `[project] dependencies` (alphabetical position, after `psycopg`). Touch nothing else.
- [ ] T002 [Phase 0] Regenerate the lockfile: `rtk uv add pydantic-settings` (or
      `rtk uv sync`). Inspect `uv.lock`: confirm `pydantic-settings` resolves to a 2.x
      release compatible with the locked `pydantic` 2.13.x and Python 3.14. If uv resolves a
      version with a known 3.14 gap, raise the floor and record it in version-guard-report.md.

### Acceptance Gate

- [ ] T003 [Phase 0] Verify working code:
      `rtk uv run python -c "import pydantic_settings; print(pydantic_settings.__version__)"`
      prints a 2.x version.
- [ ] T004 [Phase 0] Run pytest: `rtk uv run pytest` — existing suite green, zero new
      failures (FR-008).

---

## Phase 1: Settings config class (TDD)

**Purpose**: `web.config.Settings` reads and validates the environment in isolation — the
US1/US2/US4 core. Safe to build before wiring `settings.py` (does not import `web.settings`).

### Tests (write first — must fail before implementation begins)

- [ ] T005 [Phase 1] Create `tests/web/test_settings_config.py` (new file) covering
      `web.config.Settings` via `monkeypatch.setenv`/`delenv` (each test sets exactly the
      env it needs):
      - `test_missing_secret_key_raises` — `DJANGO_SECRET_KEY` unset -> `pydantic.ValidationError`
        naming the field (FR-002, US2).
      - `test_missing_required_aggregates` — several required vars unset -> one
        `ValidationError` listing all of them (D1 aggregation).
      - `test_debug_defaults_false` — `DJANGO_DEBUG` unset, other required vars set ->
        `settings.django_debug is False` (FR-003, US2 scenario 2).
      - `test_wildcard_host_rejected` — `DJANGO_ALLOWED_HOSTS="*"` -> `ValidationError`
        (FR-004, US3 scenario 2).
      - `test_allowed_hosts_comma_split` — `DJANGO_ALLOWED_HOSTS="localhost, example.com"`
        -> `["localhost", "example.com"]` (D6).
      - `test_debug_off_requires_host` — `DJANGO_DEBUG=False` + `DJANGO_ALLOWED_HOSTS=""`
        -> `ValidationError` (FR-004 / RT-159 F-001).
      - `test_burned_secret_key_rejected` — `DJANGO_SECRET_KEY=<burned literal>` ->
        `ValidationError` (FR-005, US4); a fresh key is accepted.
- [ ] T006 [Phase 1] Confirm the Red state:
      `rtk uv run pytest tests/web/test_settings_config.py -v` — all new tests fail with
      `ModuleNotFoundError: web.config` (or import error). No accidental passes.

### Implementation

- [ ] T007 [Phase 1] Create `src/web/config.py` per data-model.md: `Settings(BaseSettings)`
      with `model_config = SettingsConfigDict(env_file=None, enable_decoding=False)`; fields
      and validators exactly as the schema table (required `django_secret_key`,
      `django_allowed_hosts`, `postgres_*`; `django_debug` default `False`; transport
      toggles default off). Validators: comma-split + `'*'` reject (before), `>=1` host when
      `DEBUG` off (model after), burned-literal reject (after). Define the burned literal as
      a module constant with `# pragma: allowlist secret`.

### Acceptance Gate

- [ ] T008 [Phase 1] Verify working code: `rtk uv run pytest tests/web/test_settings_config.py -v`
      — all green (Red -> Green).
- [ ] T009 [Phase 1] Run pytest: `rtk uv run pytest` — full suite still green (`web.settings`
      not yet changed, collection unaffected).

---

## Phase 2: Wire settings.py to the environment (sequencing-critical — one change)

**Purpose**: production `settings.py` reads everything from `Settings()`; the test-settings
bootstrap keeps collection alive. US1 + FR-001/006. **T010 and T011 MUST be the same commit.**

### Implementation

- [ ] T010 [Phase 2] Edit `src/web/settings.py`: `from web.config import Settings`;
      `settings = Settings()` at module top; set `SECRET_KEY = settings.django_secret_key`,
      `DEBUG = settings.django_debug`, `ALLOWED_HOSTS = settings.django_allowed_hosts`, and
      `DATABASES["default"]` from `settings.postgres_*` — REMOVE the hard-coded
      `django-insecure-` key, `DEBUG = True`, `ALLOWED_HOSTS = []`, and every
      `os.environ.get("POSTGRES_*", "...")` dev default AND its `# hook: allow` marker.
- [ ] T011 [Phase 2] Edit `src/web/settings_test.py` (SAME commit as T010): before
      `from web.settings import *`, add `import os` and `os.environ.setdefault(...)` for
      `DJANGO_SECRET_KEY` (a fresh fixture key, NOT the burned literal), `DJANGO_ALLOWED_HOSTS`
      (`"testserver,localhost"`), and the `POSTGRES_*` vars — each line tagged
      `# hook: allow -- test fixture (ADR-021 escape hatch)`. Add `# noqa: E402` to the
      `from web.settings import *` line. Keep the in-memory SQLite `DATABASES` override.

### Acceptance Gate

- [ ] T012 [Phase 2] Verify working code: `rtk uv run python -c "import web.settings_test"`
      succeeds, and `rtk uv run pytest` — FULL suite green (collection survived the fail-fast
      switch; this is the trap's proof).
- [ ] T013 [Phase 2] Verify ADR-021 hooks pass over the changed source:
      `rtk prek run check-no-env-defaults --files src/web/settings.py src/web/config.py` and
      `rtk prek run check-no-env-loader --files src/web/settings.py src/web/config.py` — both
      exit 0 with no new exemptions in production source (FR-002).
- [ ] T014 [Phase 2] Verify fail-fast manually (quickstart §4):
      `Remove-Item Env:DJANGO_SECRET_KEY; rtk uv run python manage.py check` aborts with a
      `ValidationError` naming the missing var — does NOT start on a default (US2).

---

## Phase 3: Transport toggles + deploy-safety pin

**Purpose**: make transport-security settings env-driven (default-off, D7) and pin
`manage.py check --deploy` clean for the SECRET_KEY/DEBUG/ALLOWED_HOSTS classes. US3 + FR-007.
Note: the three target warnings are already resolved by Phase 2 — `test_settings_deploy.py`
is a **regression/characterization pin**, not a Red test (same status #159 gave its
`test_system_check_clean`); the transport toggles (T015) do not change `check --deploy`
output because they default off (the four warnings stay, risk-accepted, never silenced).

### Implementation

- [ ] T015 [Phase 3] In `src/web/config.py` + `src/web/settings.py`: project the transport
      toggles (`SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `SESSION_COOKIE_SECURE`,
      `CSRF_COOKIE_SECURE`) from `Settings` onto Django settings, all default-off (D7). Do
      NOT enable them. No code silences the four risk-accepted warnings (research.md D8).

### Tests (regression pin)

- [ ] T016 [Phase 3] Create `tests/web/test_settings_deploy.py`: with a production-like env
      (`monkeypatch.setenv` for a fresh `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`,
      `DJANGO_ALLOWED_HOSTS=example.com`, `POSTGRES_*`), collect deploy checks via
      `django.core.checks.run_checks(include_deployment_checks=True)` and assert the result
      contains NO message whose `.id` is `security.W009`/`W018`/`W020` (the resolved classes),
      and DOES contain the four risk-accepted transport ids (`W004`/`W008`/`W012`/`W016`) —
      documenting, in an executable form, that they are accepted-not-silenced.

### Acceptance Gate

- [ ] T017 [Phase 3] Verify working code: `rtk uv run pytest tests/web/test_settings_deploy.py -v`
      — green; and manually `rtk uv run python manage.py check --deploy` (quickstart §3)
      shows zero `W009/W018/W020` and only the four known transport warnings.
- [ ] T018 [Phase 3] Run pytest: `rtk uv run pytest` — full suite green.

---

## Phase 4: Developer ergonomics + documentation

**Purpose**: a fresh `run-app.ps1` boots both apps from `.env`; required vars documented. FR-008/009.

- [ ] T019 [P] [Phase 4] In `.env.example`, add a "Django application config (#161)" section
      documenting `DJANGO_SECRET_KEY` (blank, secret), `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`,
      `POSTGRES_*`, and the four transport toggles, matching quickstart.md §1 (non-secret
      example values; secret left blank).
- [ ] T020 [Phase 4] In `tasks/run-app.ps1`, load the repo-root `.env` into the process
      environment (`$env:`) BEFORE the existing pre-launch `manage.py check` step (research.md
      D4). Parse each line `KEY=VALUE` by splitting on the FIRST `=` only (secret keys can end
      in `=` padding); skip blank lines and `#` comments; do not override vars already set in
      the shell. This is PowerShell dev tooling (outside ADR-021's Python scope).

### Acceptance Gate

- [ ] T021 [Phase 4] Verify working code: with a populated `.env`, `tasks/run-app.ps1` runs
      `manage.py check` clean and starts both apps (marker 8765, Django 8766) returning 200 on
      their health endpoints (SC-005 from #159 still holds; Django now boots from `.env`).
- [ ] T022 [Phase 4] Negative check: with `DJANGO_SECRET_KEY` removed from `.env`,
      `run-app.ps1` fails fast at the `manage.py check` gate naming the missing var (no silent default).

---

## Phase 5: Polish & regression gate

- [ ] T023 [P] [Phase 5] Confirm no configuration literal remains: grep `src/web/settings.py`
      for `django-insecure`, `DEBUG = True`, `ALLOWED_HOSTS = []`, and `# hook: allow` — all
      absent (SC-001). The burned literal exists ONLY as the rejection constant in `config.py`
      (intentional re-commit of an already-burned value, carrying `# pragma: allowlist secret`).
- [ ] T024 [Phase 5] Run the full static gate: `rtk prek run --all-files` — ruff, codespell,
      deptry (confirms `pydantic-settings` is a declared+used dep), and the ADR-021 hooks all
      pass.
- [ ] T025 [Phase 5] Run the full suite with coverage: `rtk uv run pytest` — all green, plain
      `rtk uv run python manage.py check` reports zero issues (FR-008 regression pin).

### Acceptance Gate

- [ ] T026 [Phase 5] All tests green, static gate clean, both `manage.py check` (clean) and
      `manage.py check --deploy` (only the four risk-accepted transport warnings) behave as
      documented. Ready for `/make-pr`.

> **Boundary note (SC-004, A2):** the "staging and production keys are distinct from each
> other" half of SC-004 is **operational**, verified by Brent at Secret Manager provisioning
> (ADR-023), not by #161 code — the app can only assert the loaded key != the burned literal
> (T007/T005). This is the spec's stated Out-of-Scope split, recorded here so the gap is explicit.

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies); `[Phase N]` = plan phase.
- TDD is mandatory for `config.py` work: Red (T005/T006) -> Green (T007/T008).
- The Acceptance Gate at the end of each phase is a hard stop — do not start the next phase
  until it passes. Phase 2's T010+T011 are a single atomic commit (sequencing trap).
- Commit after each task or logical group. Run `python-static-checks` before declaring complete.
- Implementation is Kabilan's on founder instruction; this pipeline stops before code.
- Complete the work with `/make-pr`.
