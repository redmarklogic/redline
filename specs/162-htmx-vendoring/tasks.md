# Tasks: HTMX Vendoring (Dynamic Page Updates Without a Build Step)

**Input**: [plan.md](./plan.md) | [spec.md](./spec.md)
**Prerequisites**: Django web shell (#159) present and green; settings load via `web.config.Settings` (#161). Branch `feature/162-htmx-vendoring`.

<!-- Each phase is a vertical slice (front-to-back, one complete behaviour). TDD is mandatory:
     write the failing test, confirm Red, implement to Green. Acceptance Gate is a hard stop. -->

## Phase 0: htmx vendored and the round trip works in development

**Purpose**: Open `/htmx-demo/` locally, click the button, and a page region updates in place
from a server response — htmx loaded from a vendored static file, no build step. (Spec Scenario 1; FR-001/002/003/005/006/007.)

### Tests (write first -- must fail before implementation begins)

- [ ] T001 [Phase 0] Write failing tests in `tests/web/test_htmx_demo.py` (4 tests): (a) `finders.find("web/vendor/htmx.min.js")` returns a path; (b) `GET /htmx-demo/` is 200 `text/html` and body contains the static URL for `web/vendor/htmx.min.js`; (c) `POST /htmx-demo/action/` with a valid CSRF token returns 200 and the expected fragment markup; (d) `Client(enforce_csrf_checks=True).post("/htmx-demo/action/")` without a token returns 403. (Root/health regression for FR-007 is already pinned by `tests/web/test_skeleton.py` — do not duplicate.)
- [ ] T002 [Phase 0] Confirm the tests fail: `rtk pytest tests/web/test_htmx_demo.py -v` (RED — routes/views/file/templates absent).

### Implementation

- [ ] T003 [P] [Phase 0] Vendor htmx 2.0.10 minified to `src/web/static/web/vendor/htmx.min.js` (download the exact 2.0.10 release file, e.g. `https://unpkg.com/htmx.org@2.0.10/dist/htmx.min.js`; do not hand-edit). Record the version and the file's Subresource Integrity (SRI) hash in the commit message for FR-005 auditability.
- [ ] T004 [P] [Phase 0] Create `src/web/templates/web/base.html` — minimal HTML document that loads htmx via `<script src="{% static 'web/vendor/htmx.min.js' %}"></script>` and provides a `{% block content %}`.
- [ ] T005 [Phase 0] Create `src/web/templates/web/demo/htmx_demo.html` (extends `web/base.html`) with a button carrying `hx-post="/htmx-demo/action/"`, `hx-target="#result"`, `hx-swap="innerHTML"`, an empty `<div id="result">`, and `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` on the `<body>`. Depends on T004.
- [ ] T006 [P] [Phase 0] Create `src/web/templates/web/demo/_clicked.html` — the server-rendered HTML fragment returned by the action (static content; must NOT echo any request input — XSS-safe by construction).
- [ ] T007 [P] [Phase 0] Create `src/web/demo.py` with `htmx_demo(request)` (GET → render `htmx_demo.html`) and `htmx_demo_action(request)` (POST → render `_clicked.html`). Typed signatures, Google-style docstrings (match `src/web/views.py`).
- [ ] T008 [Phase 0] In `src/web/settings.py` (extend the existing "Static files" section): add `STATICFILES_DIRS = [BASE_DIR / "web" / "static"]` and set `TEMPLATES[0]["DIRS"] = [BASE_DIR / "web" / "templates"]`. Do not touch DB/secret/host config (#161's domain).
- [ ] T009 [Phase 0] Append routes to `src/web/urls.py`: `path("htmx-demo/", demo.htmx_demo)` and `path("htmx-demo/action/", demo.htmx_demo_action)` (import `from web import demo`). Leave the root and `health/` routes unchanged (FR-007). Depends on T007.

### Acceptance Gate

- [ ] T010 [Phase 0] Verify working code: `python manage.py runserver`, open `/htmx-demo/`, click the button — `#result` updates from the server with no full page reload.
- [ ] T011 [Phase 0] Run pytest: `rtk pytest tests/web -v` — all green (the 4 new tests plus the existing skeleton tests).

---

## Phase 1: htmx is served under production settings (DEBUG=False) via WhiteNoise

**Purpose**: The vendored file is delivered when the app runs as in the cloud (debug off,
after `collectstatic`), so interactive pages work in staging, not only locally. (Spec Scenario 2; FR-004.)

### Tests (write first -- must fail before implementation begins)

- [ ] T012 [Phase 1] Write failing tests in `tests/web/test_static_serving.py` (3 tests): (a) `WhiteNoiseMiddleware` is in `MIDDLEWARE` immediately after `django.middleware.security.SecurityMiddleware`; (b) importing `web.settings` directly, its `STORAGES["staticfiles"]["BACKEND"]` is `whitenoise.storage.CompressedManifestStaticFilesStorage`; (c) `call_command("collectstatic", "--noinput")` into a temp `STATIC_ROOT` (via `override_settings`) produces a hashed `htmx` file and a `staticfiles.json` manifest entry for `web/vendor/htmx.min.js`.
- [ ] T013 [Phase 1] Confirm the tests fail: `rtk pytest tests/web/test_static_serving.py -v` (RED — WhiteNoise not wired).

### Implementation

- [ ] T014 [Phase 1] Add `whitenoise>=6.12,<7` to `[project].dependencies` in `pyproject.toml`; refresh the lockfile (`rtk uv lock` / `rtk uv sync`). New runtime dependency (plan D2).
- [ ] T015 [Phase 1] In `src/web/settings.py`: insert `"whitenoise.middleware.WhiteNoiseMiddleware"` immediately after `SecurityMiddleware`; add `STATIC_ROOT = BASE_DIR / "staticfiles"`; add a `STORAGES` dict with `"staticfiles"` → `whitenoise.storage.CompressedManifestStaticFilesStorage` (use the `STORAGES` dict, NOT the deprecated `STATICFILES_STORAGE` string). Depends on T014.
- [ ] T016 [Phase 1] In `src/web/settings_test.py` (after `from web.settings import *`): override `STORAGES` so `"staticfiles"` uses `django.contrib.staticfiles.storage.StaticFilesStorage` (non-manifest), so template tests render `{% static %}` without `collectstatic` (plan D6). Depends on T015.
- [ ] T017 [P] [Phase 1] Add `src/staticfiles/` to `.gitignore` (under the "Django stuff" section).

### Acceptance Gate

- [ ] T018 [Phase 1] Verify prod-like delivery: with required env set and `DJANGO_DEBUG=False`, run `python manage.py collectstatic --noinput`, start the app with `DEBUG=False` (WhiteNoise serves collected static under any debug setting), and `GET` the hashed htmx static URL — 200 with a JavaScript content type (`text/javascript` or `application/javascript`).
- [ ] T019 [Phase 1] Run pytest: `rtk pytest tests/web -v` — all green (Phase 0 + Phase 1 tests).

---

## Phase Z: Polish & Cross-Cutting

- [ ] T020 [P] [Phase Z] Confirm no JavaScript build footprint was introduced: repository contains no `package.json`, `node_modules`, or JS bundler config (SC-003).
- [ ] T021 [Phase Z] Record for issue #177 (Cloud Run deploy) that the image build MUST run `python manage.py collectstatic --noinput` before serving (the compressed-manifest storage needs the manifest). The requirement is in plan.md Risk Register; ensure it is visible to whoever picks up #177 (e.g., a one-line note on the #177 issue). No application code.
- [ ] T022 [Phase Z] Run the full suite and lint: `rtk pytest` and `rtk ruff check src/` — all green, no findings.
- [ ] T023 [Phase Z] Run the static gate: `rtk prek run --all-files` — exit 0 (per `python-static-checks`).

### Acceptance Gate

- [ ] T024 [Phase Z] All tests green, lint clean, `prek` gate exit 0; demo round trip works under `runserver` and the vendored file is served under production settings.

## Dependencies & Execution Notes

- **Phase order**: Phase 0 → Phase 1 → Phase Z. Each Acceptance Gate is a hard stop.
- **Within Phase 0**: T001 before T002 (Red); T004 before T005; T003/T004/T006/T007 are `[P]` (different files); T009 depends on T007; T008 independent. Implement only after T002 confirms Red.
- **Within Phase 1**: T012 before T013 (Red); T014 → T015 → T016 chained (same settings surface); T017 is `[P]`.
- `[P]` = parallelizable (different files, no incomplete-task dependency). `[Phase N]` = owning plan phase.
- TDD is mandatory for every function/view: failing test (Red) → confirm fail → implement (Green).
- Commit after each task or logical group. Run `python-static-checks` before declaring complete; finish with the branch-completion skill.
- **Scope guard (FR-006/D8)**: no auth, no event capture, no real product buttons, no `django-htmx`, exactly one vendored file. Those belong to #171/#172/#166.

## Implementation Strategy

- **MVP = Phase 0**: the round trip provable locally is the smallest shippable proof of the htmx capability. Phase 1 hardens it for the cloud (required for the sprint demo, so not optional this sprint).
- Phase 0 is independently testable (`rtk pytest tests/web/test_htmx_demo.py`); Phase 1 is independently testable (`rtk pytest tests/web/test_static_serving.py`).
- Total tasks: 24 (Phase 0: 11, Phase 1: 8, Phase Z: 5). New test files: 2 (`test_htmx_demo.py`, `test_static_serving.py`). New source/asset files: 5 (`htmx.min.js`, `base.html`, `htmx_demo.html`, `_clicked.html`, `demo.py`). Modified: `settings.py`, `settings_test.py`, `urls.py`, `pyproject.toml`, `.gitignore`.
