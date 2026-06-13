# Version-Guard Report: Settings + 12-Factor Config

**Feature**: `specs/161-settings-12-factor-config` | **Date**: 2026-06-13
**Hook**: `before_plan` / `speckit.version-guard.check` (mandatory) — **SATISFIED**
**Source of truth for versions**: context7 `/pydantic/pydantic-settings` (queried 2026-06-13);
installed `pyproject.toml`.

## Stack under this slice

| Component | Constraint | Status |
|---|---|---|
| Python | `>=3.14` (`requires-python`) | Unchanged |
| Django | `>=5.2.8,<6` (5.2 LTS; cap load-bearing per #159 research D1) | **Unchanged** — this slice does not touch the Django pin |
| pydantic | `>=2.13.4` (already a dependency; supports Python 3.14) | Unchanged |
| **pydantic-settings** | **NEW: `>=2.7`** (floor-only) | **Add to `[project] dependencies`** |

## Why `pydantic-settings>=2.7`, floor-only (no cap)

- pydantic-settings 2.x is the current major, aligned with pydantic 2.x — there is **no
  major-version trap** like Django's `<6` cap, so the house floor-only pin style applies
  (unlike #159's deliberate Django cap).
- It is the official settings companion to pydantic; since `pydantic>=2.13.4` already
  resolves and supports Python 3.14, the matching pydantic-settings release does too.
- **Implementation-time check (binding)**: when adding the dependency, run
  `rtk uv add pydantic-settings` and confirm uv resolves a release that supports Python 3.14
  alongside the locked `pydantic` 2.13.x. If uv resolves a version with a known 3.14 gap,
  raise the floor to the first compatible release and record it here.

## Binding API constraints (pydantic-settings v2)

These patterns are mandatory for the `Settings` class (`web/config.py`); deviating
re-introduces the failure modes they prevent.

1. **Disable dotenv loading** — `model_config = SettingsConfigDict(env_file=None)`. ADR-021 /
   Constitution XVI require the application to never read a `.env` file. `env_file=None` is
   the documented switch (context7).
2. **List parsing from a comma-separated value** — pydantic-settings JSON-decodes complex
   types (e.g. `list[str]`) from env by default, so `DJANGO_ALLOWED_HOSTS=a,b` raises a JSON
   error. Set `enable_decoding=False` on the model **and** parse with a
   `field_validator(..., mode="before")` that splits on `,`. (context7: "Disable JSON
   Parsing Globally" + before-validator example.) Without this the hostname list cannot be
   supplied in the natural comma form.
3. **Required vs default** — a field with no default is required and raises
   `pydantic.ValidationError` when absent (fail-fast). A `Field(default=...)` provides a
   default that is **not** caught by the `check-no-env-defaults` hook (that hook matches
   `os.getenv`/`os.environ.get` only). Use this only for `DEBUG` (secure default `False`) and
   the transport toggles — never for `SECRET_KEY`, `ALLOWED_HOSTS`, or the `POSTGRES_*` vars.
4. **Case-insensitive env matching** — field names map to env vars case-insensitively, so
   field `django_secret_key` reads `DJANGO_SECRET_KEY`; no explicit alias needed (research.md D5).

## Compatibility rules for tasks

- Any task touching `web/config.py` MUST use the `env_file=None` + `enable_decoding=False`
  pattern above; a list field without the before-validator is a defect.
- The Django pin (`>=5.2.8,<6`) MUST NOT be widened by this slice.
- No new dependency beyond `pydantic-settings` may be introduced without a fresh
  version-guard pass and a plan amendment.
