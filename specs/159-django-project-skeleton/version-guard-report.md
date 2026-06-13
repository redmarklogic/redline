# Version Guard Report

Generated: 2026-06-12 (before_plan hook `speckit.version-guard.check`, adapted for a
Python/uv project — the npm lockfile flow degrades to uv.lock + PyPI + official docs).

## Version Status

| Package | Locked | Latest Stable | Status |
|---------|--------|---------------|--------|
| django | not yet locked — proposed constraint `>=5.2.8,<6` | 6.0.6 (PyPI, 2026-06-12) | Deliberately one major behind: pinned to 5.2 LTS (research.md D1). Not drift — a recorded decision. |
| python (runtime) | `requires-python = ">=3.14"` (pyproject) | 3.14.x | Compatible: Django 5.2 supports Python 3.14 from 5.2.8 (official FAQ matrix) |
| fastapi | 0.136.3 | — | Untouched by this slice |
| pydantic | 2.13.4 | — | Untouched by this slice |
| uvicorn | 0.49.0 | — | Untouched by this slice |

Sources: PyPI JSON (`https://pypi.org/pypi/Django/json` — latest 6.0.6, classifiers
3.12/3.13/3.14), Django install FAQ version matrix
(`https://docs.djangoproject.com/en/6.0/faq/install/` — 5.2 row: 3.10–3.14, 3.14 added
in 5.2.8), context7 `/websites/djangoproject_en_5_2` (startproject + check semantics).

## Known Issues

No known unpatched issues for the 5.2 series at its latest patch release: Django's
security policy lands fixes in the newest patch of every supported series, and the
lockfile will resolve the newest `5.2.x`. Verify at lock time against
`https://www.djangoproject.com/weblog/` (security releases) — the GHSA/npm-audit flow
of the stock hook does not apply to PyPI; treat this as a degraded lookup, not a clean
bill of health.

## Compatibility Rules (mandatory)

### django (locked 5.2.x — latest is 6.0.x)

These rules keep generated code valid on the locked LTS. The validate hook checks them
after implementation.

| # | DON'T | DO instead |
|---|----------|--------------|
| 1 | Use template partials (`{% partialdef %}` — Django 6.0+) | Whole templates or `{% include %}` |
| 2 | Use the built-in background tasks framework (`django.tasks`, 6.0+) | No async/background work in this slice at all |
| 3 | Use built-in Content-Security-Policy settings (6.0+) | Omit CSP here; security headers are later work (#176 and beyond) |
| 4 | Install Django < 5.2.8 on this repo's Python 3.14 | Constraint floor `>=5.2.8` (first 5.2 patch supporting 3.14) |
| 5 | Copy settings/API patterns from Django 6.0 docs or tutorials | Use the 5.2 docs exclusively: `https://docs.djangoproject.com/en/5.2/` |

## Upgrade Guidance (informational)

Django 6.0 (current stable) adds template partials, a background-tasks framework, and
built-in CSP support; none is needed by Sprint 3 scope. 5.2 LTS receives security
support until April 2028 — well past the 2026-07-31 launch backstop. Moving to 6.x
later is an additive, single-major hop.

## Migration References

- **django** (locked 5.2.x): <https://docs.djangoproject.com/en/5.2/> — startproject and
  check verified via context7 `/websites/djangoproject_en_5_2`
- **django** (latest 6.0.x): <https://docs.djangoproject.com/en/6.0/releases/6.0/>
- Version/Python matrix: <https://docs.djangoproject.com/en/6.0/faq/install/>

### Current-Version References

- **django 5.2 ref index**: <https://docs.djangoproject.com/en/5.2/ref/>
- **django-admin reference (startproject, check, runserver)**:
  <https://docs.djangoproject.com/en/5.2/ref/django-admin/>

## Knowledge-source note

The `django-application-development` NotebookLM notebook (registered per-task Django
reference for Sprint 3) could not ground any query: all 10 sources are pasted-text
book summaries, not book content. Flagged to the Knowledge Operator (Linda). This
report relies on official docs via context7 and PyPI instead.
