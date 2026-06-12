# Research: Django Project Skeleton (#159)

Phase 0 output. Resolves every open point left by spec.md Assumptions. Sources:
official Django 5.2 docs (via context7 `/websites/djangoproject_en_5_2`), PyPI,
Django install FAQ, repo `pyproject.toml`, ADR-024, `docs/architecture/layer-responsibilities.md`.
The registered NotebookLM Django notebook could not ground queries (stub sources —
see version-guard-report.md Knowledge-source note).

## D1 — Django version: 5.2 LTS, constraint `django>=5.2.8,<6`

- **Decision**: Pin to the 5.2 LTS series. Floor 5.2.8 (first patch supporting
  Python 3.14 — repo requires `>=3.14`); cap `<6` so uv does not resolve 6.0.6.
- **Rationale**: Zero Django prior art on the team (sprint risk register) favours the
  boring choice: the ecosystem the sprint depends on next (django-allauth #167/#168,
  pytest-django) certifies against LTS first; books/tutorials target <=5.x; security
  support runs to April 2028, past the 2026-07-31 launch backstop. Nothing in Sprint 3
  scope needs a 6.0-only feature (verified against 6.0 release notes).
- **Alternatives considered**:
  - **Django 6.0.6 (latest stable)** — rejected: no needed feature, larger
    novelty surface during a 7-week runway, ecosystem lag risk.
  - **Floor-only `>=5.2.8` (house style is floors without caps)** — rejected: uv
    resolves the highest satisfying version, which is 6.0.6 today. The cap is
    load-bearing; documented as a deliberate deviation from the floor-only convention.

## D2 — Placement: package `src/web/`, `manage.py` at repo root

- **Decision**: Django project package at `src/web/` (settings, urls, views, asgi,
  wsgi), settings module `web.settings`; `manage.py` at the repository root.
- **Rationale**: `layer-responsibilities.md` calls for a "Django project package (new
  in the pivot)" — a sibling of `marker`/`rl`, never inside them. Flat, uniquely named
  package matches house precedent (`marker`, `rl`) and avoids the generic `config`
  name colliding in the installed wheel namespace. Root `manage.py` makes the issue's
  done-when literal (`manage.py runserver`) and matches every Django reference's
  working assumption; it works from the root because the editable install (uv +
  hatchling) makes `web` importable everywhere.
- **Consequence (load-bearing)**: `tool.hatch.build.targets.wheel.packages` is an
  explicit list — `"src/web"` MUST be appended or `import web` fails and nothing
  boots. This is the one repo-specific trap in the slice.
- **Alternatives considered**:
  - `src/web/manage.py` — rejected: every command grows a path prefix; no offsetting
    benefit.
  - Two Scoops-style nested `config/` package — rejected: generic top-level name in
    the wheel, deeper module paths, deviates from flat-package precedent.
  - New top-level dir outside `src/` (e.g. `webapp/`) — rejected: breaks the
    monorepo's single `src/` layout and coverage `source = ["src"]`.

## D3 — Generation method: `startproject` template, then repo-conform edits

- **Decision**: Generate with `rtk uv run django-admin startproject web src`, then
  move `src/manage.py` to the repo root and apply repo conventions (module docstrings
  where ruff D-rules require, pyproject wiring per D2/D5).
- **Rationale**: startproject is upstream's SSOT for version-correct boilerplate
  (settings, asgi, wsgi entry points); hand-writing six files invites drift. The
  generated `manage.py` is path-independent (it only sets
  `DJANGO_SETTINGS_MODULE=web.settings` and delegates), so relocating it is safe.
- **Alternatives considered**: hand-write all files (rejected: drift risk, no gain);
  third-party cookiecutter templates (rejected: opinionated extras contradict the
  minimal done-when and ADR-024's no-DRF, single-service shape).

## D4 — Root URL: explicit placeholder view; keep `admin/` route

- **Decision**: Add `web/views.py` with one function view returning a minimal HTML
  200 response, wired at `path("", ...)`. Keep the default `admin/` URL entry.
- **Rationale**: startproject's default urlconf serves ONLY `admin/` — `GET /`
  returns 404 and the issue's primary done-when fails. The placeholder view is the
  smallest change that makes `/` a 200 (spec FR-001, FR-006). The admin route stays
  because ADR-024 enables `contrib.admin` at launch; it is non-functional until the
  database and identity tasks (#164, #165) land, which is documented in quickstart.
- **Alternatives considered**: redirect `/` to `/admin/` (rejected: admin login POST
  errors without a migrated DB — misleading placeholder); template-rendered page
  (rejected: templates dir + loader config exceed the slice; a plain `HttpResponse`
  suffices until #171 replaces it).

## D5 — Verification harness: pytest-django smoke tests, DB-free

- **Decision**: Add `pytest-django` to the `test` dependency group; set
  `DJANGO_SETTINGS_MODULE = "web.settings"` in `[tool.pytest]` ini options. Two smoke
  tests in `tests/web/`: (1) Django test client `GET /` returns 200; (2)
  `call_command("check")` completes with zero issues. Neither touches a database.
- **Rationale**: repo standard is pytest (`testpaths = ["tests"]`, coverage on
  `src`); FR-002/SC-002 require headless verification, and these two tests are the
  executable form of the issue's done-when. Manual `runserver` verification is
  recorded in quickstart.md as the human check.
- **Risk noted**: pytest runs with `filterwarnings = ["error"]`. If Django or
  pytest-django emits deprecation warnings on Python 3.14, add the narrowest matching
  ini filter with a comment — never a blanket ignore.
- **Alternatives considered**: Django's own test runner via `manage.py test`
  (rejected: parallel test standard already exists); no automated tests (rejected:
  violates preset TDD ordering and leaves FR-005 regression claim unverified).

## D6 — No database activity in this slice

- **Decision**: Leave the generated default DATABASES stanza (project-local SQLite
  reference) inert: never run `migrate`, never create or commit a database file.
- **Rationale**: `manage.py check` performs no DB connection and `GET /` on the
  placeholder view touches no model, so the done-when holds with no database at all.
  DATABASES wiring is #164's scope; settings-from-env is #161's (sprint WBS).
  `runserver`'s "unapplied migrations" warning is expected and harmless — documented
  in quickstart so nobody "fixes" it early.
- **Alternatives considered**: delete the DATABASES stanza (rejected: `contrib.admin`
  + sessions apps in INSTALLED_APPS make several system checks expect a database
  alias; stripping INSTALLED_APPS to avoid that fights the startproject baseline #161
  and #164 build on).

## D7 — Lint/packaging seams (mechanical, but recorded)

- ruff `INP` and `D` rule sets are active over `src/**`: generated modules keep/get
  module docstrings (`web/__init__.py` needs one — house precedent
  `rl/domain/__init__.py`); root `manage.py` gets a per-file ruff ignore only if a
  rule actually fires — prefer zero new ignores.
- deptry: `django` will be seen as used via `web.settings`/`asgi`/`wsgi` imports — no
  DEP002 entry expected.
- import-linter: NO contract change in this slice. #160 owns registering `web` and
  the django-import ban for `rl`. This slice must merely not violate the future
  contract: `src/web` imports nothing from `rl`/`marker`, and `rl`/`marker` are
  untouched (spec FR-004/FR-005).
- Windows dev / Linux deploy (Constitution XIV): generated settings use
  `pathlib.Path` BASE_DIR (5.2 default) — compliant; files land with LF endings.
