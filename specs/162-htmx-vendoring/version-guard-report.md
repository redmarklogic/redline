# Version Guard Report — Skipped

No npm dependency sources found (no `package-lock.json`, `package.json`, or other
JavaScript lockfile). This is expected and correct for issue #162: the feature deliberately
introduces **no** Node.js toolchain (ADR-024 "all-Python line"), and htmx is vendored as a
single static file rather than installed as an npm package. The automated npm version check
therefore has nothing to scan.

## Manual version verification (non-npm)

The version guard's automation only covers npm packages, so the versions this feature
depends on were verified by hand on 2026-06-14 and pinned in the plan:

| Component | Source of truth | Version pinned | Verified | Notes |
|-----------|-----------------|----------------|----------|-------|
| htmx (vendored JS file) | npm registry `htmx.org/latest` | `2.0.10` (exact) | latest stable 2.x | Vendored file `src/web/static/web/vendor/htmx.min.js`; record the file's SRI hash at vendoring (FR-005). |
| WhiteNoise (Python dep) | PyPI `whitenoise/json` | `>=6.12,<7` (latest 6.12.0) | classifiers list Python 3.14 **and** Django 5.2 | New runtime dependency for production static serving (plan D2). |
| Django (existing dep) | `pyproject.toml` | `>=5.2.8,<6` | unchanged | No change in this slice. |

## Known Issues

No known issues found for the pinned versions (manual check: htmx 2.0.10 and WhiteNoise
6.12.0 have no outstanding critical/high advisories as of 2026-06-14).

## Compatibility Rules (mandatory)

No npm compatibility rules — no npm packages in scope. The Django-5.2-specific guidance for
this slice (use the `STORAGES` dict, not the deprecated `STATICFILES_STORAGE` string) is
recorded in the plan's Library Best Practices and Risk Register.
