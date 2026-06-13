# Implementation Plan: Settings + 12-Factor Config

**Branch**: `feature/161-settings-12-factor-config` | **Date**: 2026-06-13 | **Spec**: [spec.md](spec.md)
**Status**: Draft

**Input**: Feature specification from `specs/161-settings-12-factor-config/spec.md`

## Summary

Convert the Django skeleton's framework-default `startproject` settings (landed by
#159) into environment-only configuration, fulfilling Constitution XVI / ADR-021 and
discharging the Accepted Risk #159 recorded against it. The skeleton ships three
deploy-blocking insecure defaults — a hard-coded `django-insecure-` `SECRET_KEY`,
`DEBUG = True`, and `ALLOWED_HOSTS = []` — plus a `DATABASES` block that reads the
environment but falls back to dev defaults behind `# hook: allow` exemptions. This
slice reads all of these from the process environment through a single
`pydantic-settings` `Settings` class (`env_file=None`), so a misconfigured environment
fails loudly at startup (`ValidationError`) instead of silently running on a predictable
key, debug on, or permissive hosts. It adds runtime guards the framework does not give
for free — the wildcard `'*'` host is forbidden, at least one explicit host is required
when debug is off, and the loaded secret key is rejected if it equals the burned
committed value. Transport-security settings (HSTS, SSL redirect, secure cookies) are
made environment-driven but default-off and risk-accepted for the founder-IP-locked
staging window (founder decision, 2026-06-13). The slice is confined to the web shell
(`src/web`); the generator core (`src/rl`) and the FastAPI walking skeleton (`src/marker`)
are untouched.

## Technical Context

**Language/Version**: Python 3.14 (`requires-python = ">=3.14"`)

**Primary Dependencies**: `django>=5.2.8,<6` (5.2 LTS, already pinned — unchanged by this
slice). **New**: `pydantic-settings>=2.7` (Constitution XVI / ADR-021's named structured
loader; `pydantic>=2.13.4` is already a dependency, this is its official settings
companion). See [version-guard-report.md](version-guard-report.md).

**Storage**: None added. This slice configures the `DATABASES` connection from the
environment but does not connect, migrate, or create a database — that is #164. Test
runs use the existing in-memory SQLite override in `web.settings_test`.

**Testing**: pytest + pytest-django. New unit tests for the `Settings` config class
(fail-fast on missing required vars; `'*'` rejected; burned key rejected; `DEBUG`
default; comma-separated host parsing) and an integration test that runs
`manage.py check --deploy` against a production-like environment. Existing suites
(`src/marker`, `src/web`, `src/rl`) must stay green — and must still *import*
`web.settings` after it becomes fail-fast (the sequencing trap below).

**Target Platform**: Linux container (Cloud Run) at deploy time (#177); authored on
Windows — Constitution XIV (`pathlib`, LF, cross-platform env) applies.

**Project Type**: Configuration change inside the existing `src/web` web-shell package.

**Performance Goals**: N/A — startup-time configuration; no request-path load characteristics.

**Constraints**: ADR-021 binding — no dotenv import, no default to a security-relevant
var in `src/`; the existing `check-no-env-loader` and `check-no-env-defaults` hooks must
pass with no new `# hook: allow` exemptions in production source. Additive/non-regressing
(FR-008). `'*'` host forbidden by the project's own validation (FR-004).

**Scale/Scope**: 1 new source module (`src/web/config.py`), 4 modified files
(`settings.py`, `settings_test.py`, `pyproject.toml`, `.env.example`,
`tasks/run-app.ps1`), 2 new test files. No data model, no API surface, no UI.

## Constitution Check

*GATE: evaluated before Phase 0 research; re-checked after design. Constitution v1.8.0.*

| Principle | Verdict | Notes |
|---|---|---|
| I (SSOT) | PASS | The `Settings` class is the single config authority; `.env.example` documents required vars but holds no authoritative values. No duplicated config source introduced. |
| II (Hook-first) | PASS | No new *agent rule* added. The ADR-021 enforcement hooks already exist; this slice makes production source conform to them. The `'*'`-forbidden and burned-key guards are runtime config validators (Principle X), not repo-rule hooks. |
| X (Raise on Failure) | PASS (reinforced) | Fail-fast is the design: missing required vars raise `pydantic.ValidationError` at startup; no sentinel default. This slice removes sentinel-style dev defaults, strengthening X. |
| XIV (Platform by deployment) | PASS | Env vars read cross-platform; `pathlib` BASE_DIR unchanged; LF endings. `run-app.ps1` `.env` loading is Windows dev tooling (`.claude`/`tasks` scope), no portability obligation. |
| XVI (Env as sole config) | **FULFILLED** | This is the task that discharges #159's XVI Accepted Risk. All environment-varying config (SECRET_KEY, DEBUG, ALLOWED_HOSTS, DATABASES) is read from the process environment via `pydantic-settings` with `env_file=None` — the exact mechanism XVI names. No `src/` source loads `.env`; no security-relevant var has a fallback default. |
| XVII (All-Python) | PASS | `pydantic-settings` is Python; no second toolchain. `run-app.ps1` is existing PowerShell dev tooling, not a new toolchain. |
| XVIII (Stateless core / framework in shell) | PASS | All changes live in `src/web`; the core (`src/rl`) and `src/marker` are untouched. `SECRET_KEY`/config is platform/shell concern, never a domain concept. No ORM model created. |

**New dependency gate (XVII / Domain Impact)**: `pydantic-settings` is a new third-party
dependency. It is pre-blessed by Constitution XVI ("use ... `pydantic-settings` with
`env_file=None`") and ADR-021 ("`pydantic-settings` is the recommended structured config
alternative"). No architectural escalation beyond this plan is required; the choice and
its single alternative (raw `os.environ[...]`) are recorded in
[research.md](research.md) D1. **Surfaced to founder for veto in the plan report.**

**Red-team gate (before_plan, optional hook)**: this spec's entire subject is
security-critical config (SECRET_KEY exposure, DEBUG error-page disclosure, Host-header
validation). Founder decision (2026-06-13): **SATISFIED-by-reference to RT-159**
(`specs/159-django-project-skeleton/red-team-findings-2026-06-12.md`) — that session
produced this task's security requirements (F-001/F-006 ALLOWED_HOSTS, F-008 burned key,
F-009 `check --deploy`), which the spec encodes verbatim (FR-004/005/007). No fresh
findings report generated this run; founder may request `/speckit.red-team.run` against
this spec before implementation.

**Version-guard (before_plan, mandatory hook)**: SATISFIED —
[version-guard-report.md](version-guard-report.md). Django 5.2 line unchanged;
`pydantic-settings>=2.7` floor-only pin (no major-version cap needed — 2.x is the current
major aligned with `pydantic` 2.x). Binding API constraints recorded (the
`enable_decoding=False` + before-validator pattern for list parsing; `env_file=None`).

## Project Structure

### Documentation (this feature)

```text
specs/161-settings-12-factor-config/
├── spec.md
├── plan.md                    # this file
├── research.md                # Phase 0 — decisions D1–D8
├── data-model.md              # Phase 1 — the Settings config schema (fields, validators)
├── quickstart.md              # Phase 1 — env setup, boot DEBUG=False, check --deploy
├── version-guard-report.md    # before_plan hook output (binding constraints)
├── checklists/
│   └── requirements.md
└── tasks.md                   # Phase 2 (/speckit.tasks — not created by plan)
```

No `contracts/` directory: this slice exposes no HTTP/API/CLI contract — it is internal
configuration. The "contract" is the `Settings` schema, captured in
[data-model.md](data-model.md).

### Source Code (repository root)

```text
src/web/
├── config.py          # NEW — pydantic-settings Settings class: env_file=None;
│                       #   required SECRET_KEY/ALLOWED_HOSTS/POSTGRES_*; DEBUG default
│                       #   False; validators (forbid '*', forbid burned key, >=1 host
│                       #   when DEBUG off, comma-split hosts); transport-security toggles
├── settings.py        # MODIFIED — reads every env-varying value from a single
│                       #   Settings() instance; removes hard-coded SECRET_KEY/DEBUG,
│                       #   ALLOWED_HOSTS=[], and the DATABASES dev defaults + hook:allow
│                       #   markers; adds env-driven transport-security settings (default off)
└── settings_test.py   # MODIFIED — bootstraps required env vars (setdefault + # hook: allow)
                        #   BEFORE `from web.settings import *`, so test collection can
                        #   import the now-fail-fast settings module

tests/web/
├── test_settings_config.py   # NEW — unit tests on Settings (TDD anchor): missing
│                              #   required var -> ValidationError; '*' rejected; burned
│                              #   key rejected; DEBUG default False; DEBUG off + empty
│                              #   hosts rejected; comma-separated hosts parsed
└── test_settings_deploy.py   # NEW — integration: manage.py check --deploy against a
                               #   production-like env -> 0 warnings in the SECRET_KEY/
                               #   DEBUG/ALLOWED_HOSTS classes

.env.example        # MODIFIED — new "Django application config (#161)" section documenting
                    #   DJANGO_SECRET_KEY (blank), DJANGO_DEBUG, DJANGO_ALLOWED_HOSTS,
                    #   POSTGRES_* (already used by settings), transport-security toggles
tasks/run-app.ps1   # MODIFIED — load .env into the process environment before running
                    #   `manage.py check` (now fail-fast) and `runserver` (shell-load,
                    #   ADR-021 Python ban N/A — PowerShell, not src/)
pyproject.toml      # MODIFIED — [project] dependencies += "pydantic-settings>=2.7"
uv.lock             # regenerated by uv
```

**Structure Decision**: a dedicated `src/web/config.py` holds the `Settings` class so the
config schema is unit-testable in isolation (instantiate `Settings(...)` with explicit
kwargs / patched env) without importing the full Django settings module. `settings.py`
imports `config` and projects its values onto the module-level Django setting names Django
requires at import time.

## Phase 0 — Research

Complete: [research.md](research.md). Decisions D1 (loader = pydantic-settings vs raw
`os.environ`), D2 (config module placement + Settings-at-import), D3 (test-settings env
bootstrap — the sequencing trap), D4 (dev env loading via `run-app.ps1` reading `.env`),
D5 (env var names + field mapping), D6 (`'*'` / burned-key / host-count validators),
D7 (transport-security: env-driven, default-off, risk-accepted), D8 (`check --deploy`
disposition table). No NEEDS CLARIFICATION remained after the founder's two scope
decisions (2026-06-13).

## Phase 1 — Design & Contracts

- **Config schema**: [data-model.md](data-model.md) — the `Settings` class field-by-field
  (name, env var, type, required/default, validator). This replaces a `contracts/`
  directory: the only interface this slice exposes is the set of environment variables it
  consumes, which the schema fully specifies.
- **Contracts**: none — no HTTP/API/CLI surface added (the placeholder root and `/health/`
  views from #159 are unchanged).
- **Quickstart**: [quickstart.md](quickstart.md) — the required env vars, booting with
  `DJANGO_DEBUG=False`, and verifying with `manage.py check --deploy`; the expected
  fail-fast error when a required var is absent.
- **Agent context update**: skipped — `.github/copilot-instructions.md` does not exist in
  this repo checkout (same as #159).

## Phase 2 — Task Generation Approach

`/speckit.tasks` decomposes along the spec's user stories with tests-first ordering:

1. **US1 foundation, tests-first** — write `tests/web/test_settings_config.py` asserting
   the target behaviour of the not-yet-existing `Settings` class (missing var raises;
   defaults; parsing), then create `src/web/config.py` to pass them.
2. **Sequencing-critical pair (must land together)** — `settings.py` env conversion AND
   the `settings_test.py` env bootstrap in the *same* change: the moment `settings.py`
   becomes fail-fast, `from web.settings import *` in the test settings breaks collection
   unless the bootstrap is present. This mirrors #159's "hatch packages + DJANGO_SETTINGS_MODULE
   in one change" trap.
3. **US2 fail-fast proof** — a test that importing/instantiating with a required var unset
   aborts and names the var; confirm the ADR-021 hooks pass over `settings.py`.
4. **US3 deploy-safety** — `tests/web/test_settings_deploy.py` running `check --deploy`;
   record the disposition table (D8) for the risk-accepted transport warnings.
5. **US4 secret isolation** — assert the loaded key != the burned literal.
6. **Dev ergonomics + docs** — `.env.example` section, `run-app.ps1` `.env` load, then the
   regression gate (full suite green, plain `manage.py check` clean, `prek` static gate).

Version-guard constraints (pydantic-settings list-parsing gotcha; `env_file=None`) bind
every task touching `config.py`.

## Complexity Tracking

| Violation / deviation | Why needed | Simpler alternative rejected because |
|---|---|---|
| New dependency `pydantic-settings` | Constitution XVI / ADR-021 name it as the structured loader; the spec needs typed parsing (bool DEBUG, list hosts), cross-field validation (`'*'` forbidden, >=1 host when DEBUG off), burned-key rejection, and aggregated fail-fast — all native to it | Raw `os.environ[...]`: no new dep, but hand-rolls bool/list parsing and every validator, raises on the *first* missing var rather than reporting all, and cannot give DEBUG a secure default without tripping the `check-no-env-defaults` hook (D1) |
| `settings_test.py` sets env via `setdefault` + `# hook: allow` | `from web.settings import *` runs at collection; a fail-fast `settings.py` would crash the entire pytest run on import unless required vars exist first. ADR-021 sanctions the escape hatch precisely for test fixtures | A `tests/conftest.py` env bootstrap: works but puts Django-settings knowledge in the generic test root; keeping it in the test settings module localizes it to where the import happens. Not importing prod settings in tests: duplicates config, violates SSOT (I) |
| `run-app.ps1` loads `.env` into the process env | After defaults are removed, `manage.py check` (run by the launcher before servers start) itself fails fast without the env vars present; the launcher must supply them. PowerShell shell-load is the ADR-021-sanctioned "shell loads `.env`" ergonomic, outside the Python ban | Requiring developers to export vars manually each session: high-friction, easy to forget, makes the merged branch appear broken on a fresh `run-app.ps1` |
| Transport-security warnings risk-accepted, not resolved | Founder decision (2026-06-13): staging is founder-IP-locked (#178) and TLS-terminated at Cloud Run; HSTS/redirect/secure-cookies are tuned at real deploy (#177). Settings are made env-driven now so #177 flips them per environment with no code change | Enabling HSTS/SSL-redirect/secure-cookies now: some are infra concerns that may misbehave behind Cloud Run's proxy before #177 exists; risk of shipping settings that need rework |
| `pydantic-settings` list field needs `enable_decoding=False` + before-validator | By default pydantic-settings JSON-decodes complex types from env, so `DJANGO_ALLOWED_HOSTS=a,b` would raise a JSON error; the documented pattern parses a comma-separated string instead (version-guard binding constraint) | Requiring operators to write `["a","b"]` JSON in the env var: unergonomic and error-prone for a hostname list |
