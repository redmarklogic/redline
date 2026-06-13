# Quickstart: Settings + 12-Factor Config

**Feature**: `specs/161-settings-12-factor-config` | **Date**: 2026-06-13

How to configure, boot, and verify the env-only settings once this slice lands. Commands
are PowerShell (Windows dev). RTK prefixes apply to eligible commands (`uv`, `pytest`).

## 1. Required environment variables

Copy `.env.example` to `.env` (git-ignored) and fill it. `run-app.ps1` loads `.env` into the
process environment before launching (research.md D4); the application never loads `.env`
itself (ADR-021).

```text
# Django application config (#161)
DJANGO_SECRET_KEY=           # REQUIRED, secret — generate a fresh value (see below); never the django-insecure- key
DJANGO_DEBUG=False           # default False; set True only for local debugging
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1   # REQUIRED, comma-separated; '*' is forbidden
POSTGRES_DB=redline
POSTGRES_USER=redline
POSTGRES_PASSWORD=redline
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
# Transport security — default off for staging (#161 D7); #177 enables per environment
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SECURE_HSTS_SECONDS=0
DJANGO_SESSION_COOKIE_SECURE=False
DJANGO_CSRF_COOKIE_SECURE=False
```

Generate a fresh secret key (never reuse the burned committed one):

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 2. Boot with debug disabled (the headline done-when)

```powershell
$env:DJANGO_DEBUG = "False"
python manage.py runserver 8766
```

Then request the root: `Invoke-WebRequest http://127.0.0.1:8766/ -UseBasicParsing` →
HTTP 200. With `DJANGO_DEBUG=False`, the Host header must match `DJANGO_ALLOWED_HOSTS`
(use `127.0.0.1`), otherwise Django returns 400 — that is the configured behaviour, not a bug.

## 3. Verify deploy-safety

```powershell
python manage.py check --deploy
```

Expect **zero** warnings in the SECRET_KEY (`W009`), DEBUG (`W018`), and ALLOWED_HOSTS
(`W020`) classes against a production-like env (`DJANGO_DEBUG=False`, real key, explicit
hosts). The transport-security warnings (`W004/W008/W012/W016`) are the known,
risk-accepted set for the staging window (research.md D7/D8) — #177 makes the full gate
blocking.

## 4. Confirm fail-fast on misconfiguration

```powershell
Remove-Item Env:DJANGO_SECRET_KEY -ErrorAction SilentlyContinue
python manage.py check
```

Expect the process to abort at settings import with a `pydantic.ValidationError` that names
`django_secret_key` (or `DJANGO_SECRET_KEY`) — it must NOT start on a default key.

## 5. Run the test suite

```powershell
rtk uv run pytest tests/web -v
```

Tests use `web.settings_test`, which bootstraps fixture env vars before importing the
(now fail-fast) production settings (research.md D3). The full suite, the plain
`manage.py check`, and the `prek` static gate must all stay green (FR-008).

## Expected oddities

- A fresh `run-app.ps1` with no `.env` present fails fast at the pre-launch `manage.py check`
  with a missing-variable error — this is correct (no silent dev defaults). Create `.env` first.
- `manage.py check --deploy` still reports the four risk-accepted transport warnings; that is
  expected for this slice and documented in research.md D8.
- The unapplied-migrations warning from #159 persists — migrations are #164, not this slice.
