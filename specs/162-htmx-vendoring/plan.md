# Implementation Plan: HTMX Vendoring (Dynamic Page Updates Without a Build Step)

**Date**: 2026-06-14 | **Spec**: [spec.md](./spec.md)
**Status**: Draft

## Summary

The Redline web application is a single server-rendered Django service (Architecture
Decision Record ADR-024). To make pages feel responsive without adopting a JavaScript
build toolchain, ADR-024 mandates **htmx** — a small JavaScript library that lets ordinary
Hypertext Markup Language (HTML) elements issue Hypertext Transfer Protocol (HTTP)
requests and swap the server's HTML response into the page — *vendored* as a single
pre-built file with no build step. This plan delivers that capability end to end. It
checks the htmx file into the repository, configures Django to serve it as a static asset
both locally and in the deployed cloud environment, and adds a small throwaway
demonstration page whose button performs a server round trip (sending a request, swapping
in a server-rendered fragment) to prove the capability works, including Django's
Cross-Site Request Forgery (CSRF) protection. The only affected layer is the **web shell**
(`src/web`); no domain or generator code is touched. Production static delivery is handled
by **WhiteNoise**, a pure-Python static-file server, chosen with the founder on 2026-06-14
so the htmx-dependent buttons built in issue #171 are guaranteed to work in the cloud for
the sprint demonstration. This slice deliberately stops at proving the capability; sign-in
gating (#171), the real buttons (#171), and event capture (#172) are out of scope.

## Technical Context

**Language**: Python 3.14
**Package manager**: uv
**Testing**: pytest (Test-Driven Development workflow per `test-driven-development` skill), `pytest-django` with `DJANGO_SETTINGS_MODULE=web.settings_test`
**Project layout**: monorepo (sibling packages under `src/`: `marker`, `rl`, `web`; hub package `rl`)
**Architecture**: the change is confined to the `web` shell package (`src/web`). `web` is the Django project, currently appless (views live in `web/views.py`). No new package or internal layer is introduced.
**Dev OS**: Windows | **Deploy OS**: Linux (Cloud Run container, ADR-022)
**Domain modeling**: not applicable — this slice introduces no domain model and no persistent data.
**Layer enforcement**: import-linter contracts cover `marker` and `rl` only; `web` is not under a layer contract and this slice does not touch `domain`/`functions`, so no contract change is needed. The ADR-024 "no Django import in domain/functions" guard is issue #160's scope.
**Key dependencies**: Django `>=5.2.8,<6` (already present); **new:** WhiteNoise `>=6.12,<7` (production static serving). Vendored (not a package dependency): htmx `2.0.10` as a single static file.

## Design Decisions

| #  | Decision | Choice | Rationale |
| -- | -------- | ------ | --------- |
| D1 | Front-end interactivity library | htmx **2.0.10**, minified, checked in at `src/web/static/web/vendor/htmx.min.js` | ADR-024 mandates vendored htmx, single file, no build step. 2.0.10 is the latest stable 2.x (verified npm registry, 2026-06-14). |
| D2 | Production static serving | **WhiteNoise 6.12.0** (`>=6.12,<7`): middleware immediately after `SecurityMiddleware`; `STORAGES["staticfiles"]` = `whitenoise.storage.CompressedManifestStaticFilesStorage` | Founder decision 2026-06-14 (spec Scenario 2). Pure-Python, no toolchain — passes ADR-024's all-Python line. Standard Django-on-Cloud-Run static solution. Content-hashed filenames give cache-busting, covering the stale-cache edge case for free. WhiteNoise classifiers confirm Python 3.14 + Django 5.2 support. |
| D3 | Template/static wiring | No new Django app. `STATICFILES_DIRS = [BASE_DIR / "web" / "static"]`; `TEMPLATES[0]["DIRS"] = [BASE_DIR / "web" / "templates"]` | The web shell is appless by #159's design (views at project level). Adding an app is unnecessary scope; `web` is not in `INSTALLED_APPS` as an app, so the app-directories finder would not pick up its static/templates — explicit `DIRS`/`STATICFILES_DIRS` is required. |
| D4 | Demonstration isolation | Demo views in a dedicated module `src/web/demo.py`; demo templates under `src/web/templates/web/demo/`; routes **appended** to `web/urls.py`. Root and health views untouched. | FR-006/FR-007. #171 replaces the demo; keeping it in its own module + URL namespace makes it a clean delete with no collision with #171's root-page work. |
| D5 | CSRF for htmx | Send Django's CSRF token via `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` on the demo page body. No `django-htmx` helper package. | Django's `CsrfViewMiddleware` accepts the `X-CSRFToken` header. Avoiding `django-htmx` upholds ADR-024's "single vendored file" precedent (no second front-end dependency). |
| D6 | Test-settings static storage | `settings_test.py` overrides `STORAGES["staticfiles"]` to `django.contrib.staticfiles.storage.StaticFilesStorage` (non-manifest) | The manifest storage (D2) raises `Missing staticfiles manifest entry` when a `{% static %}` tag renders before `collectstatic` runs; with `filterwarnings=["error"]` and that error, template tests would fail. The non-manifest override keeps template tests simple. The manifest/production path is validated by a dedicated `collectstatic` test instead. |
| D7 | collectstatic target | `STATIC_ROOT = BASE_DIR / "staticfiles"` (→ `src/staticfiles/`); add `src/staticfiles/` to `.gitignore` | `collectstatic` output is a build artifact, not source. Keep it out of version control. |
| D8 | Scope guard | No auth, no event capture, no real buttons, no `django-htmx`, exactly one vendored file | FR-006. These belong to #171/#172/#166. ADR-024 flags "one more vendored file" as the scope-creep vector — policed here. |

## Domain Impact

**Modularity assessment**: no new top-level package under `src/`. All work lands in the existing `web` shell package.
**New packages**: none in `src/`. One new third-party runtime dependency: `whitenoise` (Generic subdomain — off-the-shelf static-file server, no custom model).
**Bounded context changes**: none.
**Import-linter contract updates**: none. `web` is outside the `marker`/`rl` import-linter roots; `domain`/`functions` are not touched.
**Subdomain classification**: Generic (static-file delivery via an off-the-shelf library plus a vendored asset).
**New domain terms**: none (no geotechnical or business-domain concepts introduced).

## Architecture

### Two flows this slice establishes

**1. Request/response round trip (the capability, dev + prod):**

```
Browser GET /htmx-demo/
  -> web.demo.htmx_demo  ->  renders templates/web/demo/htmx_demo.html
       page <head> loads {% static 'web/vendor/htmx.min.js' %}
       page <body hx-headers='{"X-CSRFToken": "..."}'>
       button: hx-post="/htmx-demo/action/" hx-target="#result" hx-swap="innerHTML"

User clicks button
  -> htmx issues POST /htmx-demo/action/  (X-CSRFToken header attached)
  -> CsrfViewMiddleware validates token
  -> web.demo.htmx_demo_action  ->  renders templates/web/demo/_clicked.html (HTML fragment)
  -> htmx swaps fragment into #result    (no full page reload)
```

**2. Static asset pipeline:**

```
Source (checked in):      src/web/static/web/vendor/htmx.min.js
Dev (DEBUG=True):         staticfiles app serves directly from STATICFILES_DIRS via runserver
Prod build (#177 Docker): `manage.py collectstatic --noinput`  ->  STATIC_ROOT (src/staticfiles/)
                          CompressedManifestStaticFilesStorage hashes + gzips the file
Prod runtime (DEBUG=False): WhiteNoiseMiddleware serves hashed files from STATIC_ROOT
```

### Settings changes (`src/web/settings.py`, extend the existing "Static files" section)

- `STATIC_ROOT = BASE_DIR / "staticfiles"`
- `STATICFILES_DIRS = [BASE_DIR / "web" / "static"]`
- `STORAGES` dict with `"staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"}` (and the default `"default"` file storage left as Django's default). Use the `STORAGES` dict, **not** the deprecated `STATICFILES_STORAGE` setting (deprecated in Django 4.2+; would emit a deprecation warning that `filterwarnings=["error"]` turns into a test failure).
- Insert `"whitenoise.middleware.WhiteNoiseMiddleware"` into `MIDDLEWARE` immediately after `"django.middleware.security.SecurityMiddleware"`.
- `TEMPLATES[0]["DIRS"] = [BASE_DIR / "web" / "templates"]`.

### Test-settings change (`src/web/settings_test.py`)

After `from web.settings import *`, override:
`STORAGES = {**STORAGES, "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}}` (D6).

## Domain Models

None. This slice persists no data and defines no model.

## MoSCoW

| Category | Items |
| -------- | ----- |
| **Must have** | Vendored `htmx.min.js` (2.0.10) checked in; static config (`STATIC_ROOT`, `STATICFILES_DIRS`); demo page + POST endpoint proving the round trip; CSRF path working; dev serving; WhiteNoise production serving (DEBUG=False); automated tests for round trip + CSRF + production delivery; no JavaScript build step. |
| **Should have** | A minimal `base.html` seam that loads htmx (so #171 can extend it); cache-busting via the compressed-manifest storage (comes with D2). |
| **Could have** | Trivial inline styling on the demo page for legibility (no CSS framework, no extra file). |
| **Won't have (this time)** | Sign-in/auth gating (#171); the real product buttons and their page design (#171/Matt); click-to-event capture and the audit-log row (#172/#166); `django-htmx` helper; a second vendored library; Domain Name System (DNS) repoint and Hypertext Transfer Protocol Secure (HTTPS) load balancer (Sprint 4 / dropped per sprint plan). |

## Phased Delivery

### Phase 0: htmx vendored and the round trip works in development

**Goal**: A developer can open the demo page locally, click the button, and watch a page
region update in place from a server response — with the htmx library loaded from a
vendored static file and no build step anywhere. (Spec Scenario 1; FR-001, FR-002, FR-003,
FR-005, FR-006, FR-007.)

**TDD approach** (write tests first, in `tests/web/test_htmx_demo.py`):
1. `test_htmx_static_file_is_findable` — `django.contrib.staticfiles.finders.find("web/vendor/htmx.min.js")` returns a path (RED until the file + `STATICFILES_DIRS` land).
2. `test_demo_page_returns_200_and_references_htmx` — `Client().get("/htmx-demo/")` is 200 `text/html` and the body contains the static URL for `web/vendor/htmx.min.js` (proves `{% static %}` resolves).
3. `test_demo_action_post_returns_fragment` — a CSRF-enforcing client `POST /htmx-demo/action/` with a valid token returns 200 and the expected fragment markup.
4. `test_demo_action_post_without_csrf_is_forbidden` — `Client(enforce_csrf_checks=True).post(...)` without a token returns 403 (proves CSRF protection is active).
5. `test_root_and_health_unchanged` — `GET /` and `GET /health/` still return their #159 contract responses (regression pin for FR-007).

**Deliverables**:
1. `src/web/static/web/vendor/htmx.min.js` — vendored htmx 2.0.10 (exact version recorded in a sibling `htmx.min.js.VERSION` note or a comment in the plan; integrity hash captured at vendoring).
2. `src/web/templates/web/base.html` — minimal base template loading htmx via `{% static %}`.
3. `src/web/templates/web/demo/htmx_demo.html` — extends base; button with `hx-post`/`hx-target`/`hx-swap`; body carries the CSRF `hx-headers`.
4. `src/web/templates/web/demo/_clicked.html` — the server-rendered fragment returned by the action.
5. `src/web/demo.py` — `htmx_demo` (GET) and `htmx_demo_action` (POST) views.
6. `src/web/urls.py` — append `path("htmx-demo/", ...)` and `path("htmx-demo/action/", ...)` (root/health routes untouched).
7. `src/web/settings.py` — add `STATICFILES_DIRS` and `TEMPLATES[0]["DIRS"]`.
8. `tests/web/test_htmx_demo.py` — the five tests above.

**Verification**:

```
rtk pytest tests/web/test_htmx_demo.py -v   # all green
# Manual: python manage.py runserver, open /htmx-demo/, click the button, see #result update with no full reload.
```

**Acceptance Gate** (both must pass before Phase 1 starts):
- [ ] Working code: the demo page renders and the button performs the round trip under `runserver`.
- [ ] `rtk pytest tests/web -v` is green.

---

### Phase 1: htmx is served under production settings (DEBUG=False) via WhiteNoise

**Goal**: The vendored file is delivered when the application runs as it does in the cloud
(debug off, after `collectstatic`), so the interactive pages work in staging, not only on a
developer's machine. (Spec Scenario 2; FR-004.)

**TDD approach** (tests in `tests/web/test_static_serving.py`):
1. `test_whitenoise_middleware_installed_after_security` — assert `WhiteNoiseMiddleware` is present and positioned immediately after `SecurityMiddleware` in `MIDDLEWARE`.
2. `test_staticfiles_storage_is_manifest_in_base_settings` — import `web.settings` and assert its `STORAGES["staticfiles"]["BACKEND"]` is the WhiteNoise compressed-manifest backend (guards D2; the test reads the base module directly so the D6 test-settings override does not mask it).
3. `test_collectstatic_collects_htmx_and_manifest_serves_it` — run `call_command("collectstatic", "--noinput")` into a temporary `STATIC_ROOT` (via `override_settings`), then assert the hashed htmx file and a `staticfiles.json` manifest entry for `web/vendor/htmx.min.js` exist.

**Deliverables**:
1. `pyproject.toml` — add `whitenoise>=6.12,<7` to `dependencies` (Kabilan runs `uv add`/lockfile update during implementation).
2. `src/web/settings.py` — add the WhiteNoise middleware and the `STORAGES` (manifest) configuration.
3. `src/web/settings_test.py` — override `STORAGES["staticfiles"]` to the non-manifest backend (D6).
4. `.gitignore` — add `src/staticfiles/`.
5. `tests/web/test_static_serving.py` — the three tests above.

**Verification**:

```
rtk pytest tests/web -v                                  # all green, incl. Phase 0 tests
# Manual prod-like check:
#   set DJANGO_DEBUG=False (+ required env), python manage.py collectstatic --noinput,
#   start via the production server, GET the hashed htmx URL -> 200 application/javascript.
```

**Acceptance Gate** (both must pass before the slice is done):
- [ ] Working code: `collectstatic` collects the vendored file and the manifest serves it under DEBUG=False.
- [ ] `rtk pytest tests/web -v` is green and the full `prek` static gate passes.

## File Inventory

| Phase | New Files | Count |
| ----- | --------- | ----- |
| 0 | `src/web/static/web/vendor/htmx.min.js`, `src/web/templates/web/base.html`, `src/web/templates/web/demo/htmx_demo.html`, `src/web/templates/web/demo/_clicked.html`, `src/web/demo.py`, `tests/web/test_htmx_demo.py` | 6 |
| 1 | `tests/web/test_static_serving.py` | 1 |

**Modified (not new)**: `src/web/settings.py`, `src/web/settings_test.py`, `src/web/urls.py`, `pyproject.toml`, `.gitignore`.
**Total new**: ~7 | **Total deleted**: 0 (the demo files are deleted later by #171, not by this slice).

## Library Best Practices

<!-- Verified against PyPI/npm registries on 2026-06-14; WhiteNoise config confirmed against its Django integration docs. -->

### whitenoise (6.12.0)

- **Import path / config**: no import in app code. Add `"whitenoise.middleware.WhiteNoiseMiddleware"` to `MIDDLEWARE` directly after `django.middleware.security.SecurityMiddleware` and before all others.
- **API gotchas**: configure via the Django 5.2 `STORAGES` dict (`STORAGES["staticfiles"]["BACKEND"] = "whitenoise.storage.CompressedManifestStaticFilesStorage"`); do **not** use the deprecated `STATICFILES_STORAGE` string setting — it emits a `RemovedInDjango…Warning` that `filterwarnings=["error"]` converts into a test failure. The compressed-manifest storage **requires** `collectstatic` to have run before it serves; rendering `{% static %}` against it without a manifest raises — hence the D6 test-settings override.
- **Confirmed pattern**: `SecurityMiddleware` → `WhiteNoiseMiddleware` → (rest). `STATIC_ROOT` set; run `python manage.py collectstatic --noinput` in the deploy build (#177).

### htmx (2.0.10, vendored)

- **Import path**: none — a single `<script src="{% static 'web/vendor/htmx.min.js' %}"></script>` in the page `<head>`.
- **API gotchas**: htmx 2.x default swap is `innerHTML`; set `hx-target` and `hx-swap` explicitly on the button for clarity. For Django CSRF on state-changing requests, attach the token with `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` on an ancestor element (the `<body>`), so every htmx request inherits it.
- **Confirmed pattern**: vendored file at `src/web/static/web/vendor/htmx.min.js`; version 2.0.10 pinned; record the file's own Subresource Integrity (SRI) hash in the commit message or a `VERSION` sidecar for auditability (FR-005).

### Django staticfiles (5.2)

- `STATIC_URL = "static/"` already set. Source dir via `STATICFILES_DIRS`; collect target via `STATIC_ROOT`. In tests, locate assets with `django.contrib.staticfiles.finders.find(...)`.

## Risk Register

| Risk | Mitigation |
| ---- | ---------- |
| Manifest storage raises in tests when `{% static %}` renders without `collectstatic` (compounded by `filterwarnings=["error"]`) | D6: override `STORAGES["staticfiles"]` to the non-manifest backend in `settings_test.py`; validate the manifest path in a dedicated `collectstatic` test instead. |
| `#177` Docker build omits `collectstatic` → vendored file missing in staging (HTTP 500/404 only in the cloud) | Make "run `collectstatic --noinput` in the image build" an explicit, documented contract for #177; this slice's production test proves the local prod-settings path so #177 only needs to wire the build step. |
| `src/web/static` not present in the deployed container/image | Note for #177: the container must include the `src/` tree (or run `collectstatic` from source) so static files exist at build time. `collectstatic` reads from `STATICFILES_DIRS` on disk. |
| Using the deprecated `STATICFILES_STORAGE` string emits a deprecation warning → test failure under `filterwarnings=["error"]` | Use the `STORAGES` dict form (D2). |
| Scope creep: "just one more vendored file" erodes the no-build-step rule | D8: exactly one vendored file; any future addition needs an explicit decision (ADR-024 precedent). |
| Demo collides with #171's real root page | D4: demo on a dedicated `/htmx-demo/` URL in its own module; root/health untouched (FR-007 regression test). |

## Glossary

<!-- These are web-platform terms, included as reader aids because the spec's audience is
     not assumed to be web developers (per the project's plain-English writing rule). There
     are no business/geotechnical domain terms in this slice. -->

| Term | Definition |
| ---- | ---------- |
| htmx | A small JavaScript library that lets an HTML element send an HTTP request and replace part of the page with the server's HTML response, without a full page reload. |
| Vendoring | Checking a third-party file directly into the repository and serving it ourselves, instead of fetching it through a package manager or build tool. |
| Static file | A file served as-is to the browser (here, the htmx JavaScript), as opposed to a page generated per request. |
| collectstatic | A Django command that gathers all static files into one directory for the deployed app to serve. |
| CSRF (Cross-Site Request Forgery) | An attack where another site tricks a logged-in user's browser into making a state-changing request; Django blocks it by requiring a secret token on such requests. |
| WhiteNoise | A pure-Python library that lets the Django application serve its own static files efficiently when running in production (where Django's development server does not). |
