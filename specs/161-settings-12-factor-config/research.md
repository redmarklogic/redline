# Research: Settings + 12-Factor Config

**Feature**: `specs/161-settings-12-factor-config` | **Date**: 2026-06-13

All decisions below resolve the spec's Assumptions and the plan's Technical Context.
No `[NEEDS CLARIFICATION]` remained after the founder's two scope decisions (2026-06-13).

---

## D1 — Configuration loader: `pydantic-settings` (not raw `os.environ`)

**Decision**: Read all environment-varying configuration through a single
`pydantic-settings` `BaseSettings` subclass with `model_config = SettingsConfigDict(env_file=None)`.

**Rationale**:
- Constitution XVI and ADR-021 explicitly name `pydantic-settings` with `env_file=None` as
  a sanctioned mechanism — it is pre-blessed, not a novel choice.
- The spec requires typed coercion (`DEBUG` -> bool, `ALLOWED_HOSTS` -> list), cross-field
  validation (`'*'` forbidden; at least one host when `DEBUG` is off), value rejection
  (loaded `SECRET_KEY` != burned literal), and aggregated startup validation — all native
  to pydantic. Raw `os.environ[...]` would hand-roll each of these.
- A required field (no default) raises `pydantic.ValidationError` when the env var is
  missing — exactly the fail-fast Constitution X and XVI want, and it reports *all* missing
  required vars at once rather than dying on the first.
- It resolves the `DEBUG` tension cleanly: a `Field(default=False)` is a *secure* default and
  is **not** caught by the `check-no-env-defaults` hook (that hook's regex targets
  `os.getenv(..., default)` / `os.environ.get(..., default)`, not pydantic field defaults).
  So `DEBUG` defaults to the safe value while `SECRET_KEY`/`ALLOWED_HOSTS`/DB stay required.

**Alternatives considered**:
- **Raw `os.environ["VAR"]`**: zero new dependency, KeyError fail-fast. Rejected — hand-rolls
  bool/list parsing and every validator; raises on the first missing var only; cannot give
  `DEBUG` a secure default without tripping the `check-no-env-defaults` hook or adding a
  `# hook: allow` to production source (forbidden by FR-002).
- **`django-environ`**: popular 12-factor helper. Rejected — it reads `.env` files (an
  ADR-021/XVI anti-pattern at the library level) and is a new dependency with no pydantic
  synergy, where `pydantic` is already in the tree.

---

## D2 — Config module placement: `src/web/config.py`, `Settings()` instantiated at import

**Decision**: Put the `Settings` class in a new `src/web/config.py`. `settings.py` imports it,
instantiates one `Settings()`, and projects its values onto the module-level Django setting
names. The instance is created at `settings.py` import time (Django reads settings as module
globals).

**Rationale**: isolating the class lets `tests/web/test_settings_config.py` instantiate
`Settings(**kwargs)` (or with a patched environment) without importing the full Django
settings module or booting Django. `settings.py` stays a thin projection layer.

**Alternatives**: inline the class in `settings.py` (rejected — cannot unit-test the schema
without importing all Django settings and their import-time side effects).

---

## D3 — Test-settings env bootstrap (the sequencing trap)

**Decision**: At the very top of `src/web/settings_test.py`, before
`from web.settings import *`, set the required env vars with
`os.environ.setdefault("DJANGO_SECRET_KEY", "<test value>")  # hook: allow -- test fixture (ADR-021)`
(and the same for `DJANGO_ALLOWED_HOSTS` and the `POSTGRES_*` vars). `DJANGO_DEBUG` may be
omitted (defaults False).

**Rationale**: `from web.settings import *` executes at module import, which instantiates
`Settings()`. Once `settings.py` is fail-fast, importing it with no env set raises
`ValidationError` and **crashes pytest collection for the whole repo**. This is the #161
analogue of #159's "hatch packages + `DJANGO_SETTINGS_MODULE` must land together" trap; the
`settings.py` conversion and this bootstrap MUST ship in the same change.
`os.environ.setdefault` is not `os.environ.get(VAR, default)` and is not matched by the
`check-no-env-defaults` hook; the explicit `# hook: allow` marker documents the sanctioned
test-fixture exemption (ADR-021 escape hatch) regardless.

**Alternatives**: a `tests/conftest.py` bootstrap (works, but scatters Django-settings
knowledge into the generic test root); rewriting `settings_test.py` to not import prod
settings (rejected — duplicates config, violates SSOT). The `setdefault` (not plain
assignment) lets a developer who *has* exported real vars keep them.

---

## D4 — Dev environment loading via `tasks/run-app.ps1`

**Decision**: `run-app.ps1` parses the repo-root `.env` and sets the corresponding
`$env:` process variables before it runs `manage.py check` and `runserver`.

**Rationale**: after the dev-default fallbacks are removed, the `manage.py check` gate that
`run-app.ps1` already runs *before* launching servers (#159 FR-008) will itself fail fast
without the env vars present. The launcher is the natural place to supply them. This is the
ADR-021/XVI "the shell loads `.env`" ergonomic — `run-app.ps1` is PowerShell dev tooling in
`tasks/`, outside the Python `src/`/`scripts/` scope of the dotenv ban. `.env` stays
git-ignored and out of the Docker build context.

**Alternatives**: require manual `$env:` exports each session (rejected — high friction,
makes a fresh `run-app.ps1` appear broken); a Python entrypoint loading dotenv (rejected —
violates ADR-021 directly).

---

## D5 — Environment variable names and field mapping

**Decision**: pydantic-settings matches env var names to field names case-insensitively, so
field names are the lowercase of the env var. No aliases needed.

| Field | Env var | Notes |
|---|---|---|
| `django_secret_key` | `DJANGO_SECRET_KEY` | required |
| `django_debug` | `DJANGO_DEBUG` | default `False` |
| `django_allowed_hosts` | `DJANGO_ALLOWED_HOSTS` | required, comma-separated |
| `postgres_db` | `POSTGRES_DB` | required (was dev-defaulted) |
| `postgres_user` | `POSTGRES_USER` | required |
| `postgres_password` | `POSTGRES_PASSWORD` | required |
| `postgres_host` | `POSTGRES_HOST` | required |
| `postgres_port` | `POSTGRES_PORT` | required |
| transport toggles | `DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_SECURE_HSTS_SECONDS`, `DJANGO_SESSION_COOKIE_SECURE`, `DJANGO_CSRF_COOKIE_SECURE` | default off (D7) |

**Rationale**: `DJANGO_` prefix for Django-app settings avoids collision and reads clearly;
the existing `POSTGRES_*` names are preserved (already used by the current `settings.py` and
by `docker-compose.yml`). Keeping the `POSTGRES_*` names means the local Compose Postgres
service and the app share one set of variables.

**Note**: no `env_prefix` is set on the model because `DJANGO_*` and `POSTGRES_*` do not
share a single prefix; field names carry the full lowercase env name.

---

## D6 — Validators: `'*'` forbidden, host count, burned key

**Decision**: three validators on `Settings`:
1. `field_validator("django_allowed_hosts", mode="before")` — split the comma-separated
   string into a list and reject any entry equal to `"*"` (FR-004). Requires
   `enable_decoding=False` on the model so pydantic does not try to JSON-decode the value
   first (see version-guard-report.md).
2. `model_validator(mode="after")` — if `django_debug` is `False`, require at least one
   non-empty host (FR-004 / RT-159 F-001: `DEBUG=False` + empty hosts 400s every request).
3. `field_validator("django_secret_key", mode="after")` — reject the exact burned literal
   `django-insecure-ql2$-gjhyjwygz&@)uxs4(bba=5a&q5auyv^ka!vzwcbfo!h99` (FR-005 / RT-159
   F-008). The test fixture key is a different value, so this validator is safe under test.

**Rationale**: these are the spec's non-negotiable guards (US3, US4). Encoding them as
pydantic validators makes them fail-fast at startup and directly unit-testable.

**Alternatives**: enforce in `settings.py` after reading raw values (rejected — splits the
validation logic away from the schema and is harder to test in isolation).

---

## D7 — Transport security: env-driven, default-off, risk-accepted

**Decision**: expose `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, `SESSION_COOKIE_SECURE`,
`CSRF_COOKIE_SECURE` (and `SECURE_PROXY_SSL_HEADER` handling) as env-driven settings
defaulting to off/0/False. Do not enable them in this slice.

**Rationale**: founder decision (2026-06-13, "Risk-accept transport now"). Staging is
founder-IP-locked (#178) and HTTPS-terminated at Cloud Run; turning on HSTS/SSL-redirect
before the real deploy (#177) risks redirect loops or HSTS pinning against a URL that may
change. Making them env-driven now means #177 enables them per environment with no code
change. Each corresponding `check --deploy` warning is risk-accepted with this rationale
(D8). The full `check --deploy` gate becomes blocking in #177's pipeline (RT-159 F-009).

**Alternatives**: fully harden now (founder rejected — premature, may need retuning behind
the Cloud Run proxy); leave the settings absent (rejected — #177 would then need a code
change to enable them).

---

## D8 — `manage.py check --deploy` disposition table

`check --deploy` raises the warnings below. This slice **resolves** the SECRET_KEY / DEBUG /
ALLOWED_HOSTS classes and **risk-accepts** the transport-security ones (D7).

| Warning | Check | Disposition in #161 |
|---|---|---|
| `security.W009` | weak/short `SECRET_KEY` | **Resolved** — real key from env (FR-005); test asserts != burned literal |
| `security.W018` | `DEBUG=True` in deploy | **Resolved** — `DEBUG` env-driven, default False; prod-like env runs False (FR-003) |
| `security.W020` | `ALLOWED_HOSTS` empty | **Resolved** — required, explicit, `'*'` forbidden, >=1 host when DEBUG off (FR-004) |
| `security.W004` | `SECURE_HSTS_SECONDS` not set | **Risk-accepted** (D7) — env-driven, enabled at #177 |
| `security.W008` | `SECURE_SSL_REDIRECT` off | **Risk-accepted** (D7) — TLS terminates at Cloud Run; enabled at #177 |
| `security.W012` | `SESSION_COOKIE_SECURE` off | **Risk-accepted** (D7) — enabled at #177 |
| `security.W016` | `CSRF_COOKIE_SECURE` off | **Risk-accepted** (D7) — enabled at #177 |

`tests/web/test_settings_deploy.py` asserts the first three classes raise **zero** warnings
against a production-like env; the risk-accepted four are documented here, not silenced in
code. The blocking `check --deploy --fail-level WARNING` pipeline gate is #177's
responsibility, not this slice's.
