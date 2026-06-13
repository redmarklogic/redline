# Data Model: Settings + 12-Factor Config

**Feature**: `specs/161-settings-12-factor-config` | **Date**: 2026-06-13

This slice creates **no persisted domain entities** (no database tables, no ORM models —
that is #164/#165/#166). The only "model" is the configuration schema: the
`pydantic-settings` `Settings` class that reads and validates the process environment at
startup. It is recorded here in place of a `contracts/` directory.

## Config schema — `web.config.Settings`

`class Settings(BaseSettings)` with `model_config = SettingsConfigDict(env_file=None,
enable_decoding=False)`. One instance is created at `web.settings` import time and its
values are projected onto Django's module-level setting names.

| Field | Env var | Type | Required? | Default | Validation |
|---|---|---|---|---|---|
| `django_secret_key` | `DJANGO_SECRET_KEY` | `str` | Yes | — | Must NOT equal the burned `django-insecure-ql2$…fo!h99` literal (FR-005) |
| `django_debug` | `DJANGO_DEBUG` | `bool` | No | `False` | Secure default; absence never yields `True` (FR-003). Accepted true forms documented in `.env.example` |
| `django_allowed_hosts` | `DJANGO_ALLOWED_HOSTS` | `list[str]` | Yes | — | Comma-separated -> list (before-validator); any entry `"*"` rejected; >=1 host required when `django_debug` is `False` (FR-004) |
| `postgres_db` | `POSTGRES_DB` | `str` | Yes | — | — |
| `postgres_user` | `POSTGRES_USER` | `str` | Yes | — | — |
| `postgres_password` | `POSTGRES_PASSWORD` | `str` | Yes | — | — |
| `postgres_host` | `POSTGRES_HOST` | `str` | Yes | — | — |
| `postgres_port` | `POSTGRES_PORT` | `str` | Yes | — | Kept as `str` (Django `DATABASES["PORT"]` accepts a string; matches current behaviour) |
| `django_secure_ssl_redirect` | `DJANGO_SECURE_SSL_REDIRECT` | `bool` | No | `False` | Risk-accepted off for staging (D7) |
| `django_secure_hsts_seconds` | `DJANGO_SECURE_HSTS_SECONDS` | `int` | No | `0` | Risk-accepted off for staging (D7) |
| `django_session_cookie_secure` | `DJANGO_SESSION_COOKIE_SECURE` | `bool` | No | `False` | Risk-accepted off for staging (D7) |
| `django_csrf_cookie_secure` | `DJANGO_CSRF_COOKIE_SECURE` | `bool` | No | `False` | Risk-accepted off for staging (D7) |

### Validators (see research.md D6)

1. **`django_allowed_hosts` before-validator** — accept a `str` (comma-separated) or a `list`;
   strip whitespace, drop empties, split on `,`; raise `ValueError` if any entry is `"*"`.
   (`enable_decoding=False` prevents pydantic-settings from JSON-decoding the raw value first.)
2. **model after-validator** — `if not django_debug and not django_allowed_hosts: raise ValueError`.
3. **`django_secret_key` after-validator** — `if value == BURNED_LITERAL: raise ValueError`.

### Failure behaviour

- A missing required env var -> `pydantic.ValidationError` at `Settings()` construction ->
  raised at `web.settings` import -> the process does not start (Constitution X / XVI, FR-002).
- pydantic aggregates: a single `ValidationError` lists every missing/invalid field, so the
  operator sees all problems at once, each naming its field.

## Mapping onto Django settings (`web.settings`)

```text
SECRET_KEY                 <- settings.django_secret_key
DEBUG                      <- settings.django_debug
ALLOWED_HOSTS              <- settings.django_allowed_hosts
DATABASES["default"][...]  <- settings.postgres_*   (no dev-default fallbacks; no # hook: allow)
SECURE_SSL_REDIRECT        <- settings.django_secure_ssl_redirect
SECURE_HSTS_SECONDS        <- settings.django_secure_hsts_seconds
SESSION_COOKIE_SECURE      <- settings.django_session_cookie_secure
CSRF_COOKIE_SECURE         <- settings.django_csrf_cookie_secure
```

All other Django settings (INSTALLED_APPS, MIDDLEWARE, TEMPLATES, AUTH_PASSWORD_VALIDATORS,
i18n, static, DEFAULT_AUTO_FIELD) are unchanged from the #159 skeleton.
