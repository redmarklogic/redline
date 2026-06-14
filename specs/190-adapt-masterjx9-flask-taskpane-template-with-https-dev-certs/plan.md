# Implementation Plan: Python-served Word taskpane over locally-trusted HTTPS

**Date**: 2026-06-14 | **Spec**: see `spec.md` in this directory
**Status**: Draft

## Summary

We are standing up a tiny Python web server that serves a single hello-world page —
the future Microsoft Word "taskpane" — over HTTPS (encrypted web traffic) on the
developer's own machine, and a Python script that creates and trusts the local HTTPS
certificate that HTTPS requires. We do this by adapting an existing open-source project,
the **Masterjx9 Outlook-Addin-TaskPane** template, which already serves add-in files
from a small Python web server (the **Flask** framework) and already ships a Python
re-implementation of Microsoft's `office-addin-dev-certs` certificate helper. The point
is to prove the project can serve a Word add-in page entirely from Python, with **no
Node.js JavaScript toolchain** anywhere in the add-in folder. This matters because the
whole Sprint 4 paid-product proof of concept (parent issue #189) depends on a no-Node.js
serving path, and parent #189 carries a hard "stop by Wednesday" tripwire. This slice is
the foundation: serving the page over trusted HTTPS. Sideloading it into Word is a
separate issue (#191) and is out of scope here.

The work lives in a new sibling package, `src/addin/`, kept deliberately separate from
the project's Django web product (`src/web/`). Flask is the right tool for this slice
because the Masterjx9 template is Flask-based and the deliverable is a throwaway local
development harness, not the production server — production serving and deployment are
deferred to a later sprint. The Flask choice was confirmed by the founder on 2026-06-14.

## Technical Context

**Language**: Python 3.14
**Package manager**: uv
**Testing**: pytest (Test-Driven Development workflow per the `test-driven-development` skill)
**Project layout**: monorepo (sibling packages under `src/`; hub package `rl`) — read from `.specify/architecture.yml`
**Architecture**: New sibling package `src/addin/`. It is a **Generic** subdomain (off-the-shelf static file serving, no business domain model), so it has no `domain > schemas > functions` layering and is excluded from the import-linter contracts that govern `marker` and `rl`.
**Dev OS**: Windows | **Deploy OS**: not applicable this slice (local-only proof of concept; deployment deferred to Sprint 5+)
**Domain modeling**: not applicable — no Pydantic or Pandera models in this slice
**Layer enforcement**: `src/addin` is **not** added to `[tool.importlinter] root_packages` (currently `marker`, `rl`) and is **not** added to the wheel build targets (currently `src/marker`, `src/rl`, `src/web`), because it is a non-shipped development harness.
**Key dependencies**: Flask (web server + HTTPS via `ssl_context`); the certificate-generation library used by the Masterjx9 cert port (confirmed in Phase 0 — expected to be `cryptography`); `curl` (acceptance check only, already present).

## Design Decisions

| #  | Decision | Choice | Rationale |
| -- | -------- | ------ | --------- |
| D1 | Web framework for the dev server | **Flask** (kept from the template) | Lowest-effort path to acceptance on a tripwire-critical spike; template is Flask-based; this is a throwaway dev harness, not the Django product. Founder-confirmed 2026-06-14. |
| D2 | Where the code lives | New sibling package `src/addin/` | Keeps the Flask spike harness out of the Django product (`src/web/`) and out of the domain packages (`marker`, `rl`). Gives FR-004's `git ls-files` Node-artifact check an unambiguous path. |
| D3 | Package classification | Generic subdomain; excluded from import-linter and wheel build | No business domain model; not shipped in the product wheel; a dev-only harness. |
| D4 | How HTTPS is terminated | Flask `app.run(ssl_context=(cert, key))` using the template's generated certificate | Native Flask HTTPS support (confirmed via Context7); no reverse proxy needed for a localhost PoC. |
| D5 | Certificate generation + trust mechanism | Reuse the template's Python `office-addin-dev-certs` port unchanged; **name its trust-store install mechanism in Phase 0** (expected Windows `certutil -addstore` or PowerShell `Import-Certificate`) | Parent #189 states the template already solved generation; the no-go is re-researching it. But the *trust* step is what Scenario 2 hinges on, so the mechanism must be named, not assumed. |
| D6 | Listening port | **3000** (the Office add-in convention), fixed and recorded in `src/addin/README.md` | FR-006 requires one unambiguous port so the #191 manifest and the acceptance `curl` target the same value. |

## Domain Impact

**Modularity assessment**: New top-level package under `src/`. Signal from the
`python-domain-modeling` decision matrix that drove a *separate* package rather than a
subpackage of `web`: **language/framework boundary** (Flask vs Django — mixing a second
web framework into the Django app package would muddy that package's responsibility) and
**rate of change / future extraction** (this is a throwaway spike harness that may be
deleted or rewritten once the real serving path is decided, so it must be cleanly
isolable).
**New packages**: `src/addin` — a Generic dev harness. **No** import-linter contract
added (it has no internal layers and no inbound dependencies from `marker`/`rl`).
**Bounded context changes**: None. `addin` introduces no business concepts.
**Import-linter contract updates**: None. `root_packages` stays `[ "marker", "rl" ]`.
(If a future reviewer wants `addin` forbidden from importing `marker`/`rl`, that is a
later hardening step, not part of this spike.)
**Subdomain classification**: Generic.
**New domain terms**: None. ("Taskpane", "manifest", "sideload" are Microsoft Office
platform terms, defined in the Glossary, not business-domain terms.)

## Architecture

### Request flow (Scenario 1)

```text
curl / browser ──HTTPS GET /taskpane.html──▶ Flask app (src/addin/server.py)
                                              │  ssl_context=(cert.pem, key.pem)
                                              ▼
                                   send_static_file("taskpane.html")
                                              │
                                   src/addin/static/taskpane.html  ──▶  200 + hello-world HTML
```

### Certificate trust flow (Scenario 2)

```text
python -m addin.make_cert ──▶ generate self-signed cert+key for "localhost"
                                │  (template's office-addin-dev-certs port)
                                ▼
                        write cert.pem / key.pem  ──▶  install cert into Windows
                                                        trust store (may need elevated shell)
                                                        │
                                              browser opens https://localhost:3000/taskpane.html
                                                        │
                                                        ▼  no certificate warning (human-verify)
```

### Proposed package layout

```text
src/addin/
  __init__.py
  server.py          # Flask app; static_folder="static"; app.run(ssl_context=...)
  make_cert.py       # thin wrapper over the template's cert port; writes cert.pem/key.pem; trusts it
  static/
    taskpane.html    # hello-world page, no app logic
  certs/             # generated cert.pem / key.pem (gitignored)
  README.md          # the two documented commands + the chosen port (FR-007)
```

The template's serving and certificate modules are adapted into `server.py` and
`make_cert.py`. The template's Outlook manifest and any Outlook-specific assets are
**not** copied (out of scope; #191 owns the Word manifest).

## Domain Models

None. This slice has no Pydantic `BaseModel` or Pandera `DataFrameModel`. The served
page is a static HTML file; the server holds no business state. Recording this
explicitly so the tasks phase does not invent a domain layer for a static file server.

## MoSCoW

| Category | Items |
| -------- | ----- |
| **Must have** | Flask server serving `/taskpane.html` over HTTPS (FR-001, FR-002); Python cert generation + trust, no Node.js (FR-003); hello-world content only (FR-005); single documented port (FR-006); two documented commands (FR-007); zero Node.js artifacts in `src/addin` (FR-004). |
| **Should have** | Clear, loud failure on port-in-use and on denied trust-store write (edge cases). |
| **Could have** | A plain 404 for unknown paths; a one-line health route for quick liveness checks. |
| **Won't have (this time)** | The Word manifest and sideload (#191); edit-to-refresh cycle (#192); auth/bearer header (#193); any document-scanning or API logic (#196/#197); deployment to Google Cloud (Sprint 5+); import-linter contract for `addin`; Fluent UI / visual design. |

## Phased Delivery

### Phase 0: Obtain and audit the template

**Goal**: Working knowledge of the Masterjx9 template's serving and certificate modules,
and a confirmed list of the exact dependency it uses for certificate generation — so
later phases adapt real code, not assumptions.

**TDD approach**: No test-first code yet (this phase is acquisition + reading). The only
assertion is the Node-artifact audit, captured as a check in Phase 3.

**Deliverables**:

1. The template's serving entry point and certificate script identified and read, with
   the certificate library named (expected `cryptography`; confirm and record in D-table
   note if different).
2. **The trust-store install mechanism named.** Read *how* the template installs the
   generated certificate into the host trust store and record the exact mechanism —
   most likely the Windows `certutil -addstore -user Root <cert>` command, a PowerShell
   `Import-Certificate` call, or a direct library call. Scenario 2 (no browser warning)
   depends entirely on this step, so it must be a known, named mechanism before Phase 2,
   not a black box. Record it in the README stub and in plan D5.
3. A short note in `src/addin/README.md` (stub) recording: the template source, which
   files are reused, the certificate library actually used, and the trust-store
   mechanism from deliverable 2.

**Verification**:

```text
# Confirm the cert library the template depends on is named in the README stub
# and is resolvable under uv:
uv pip show <cert-library>   # e.g. cryptography -> prints version, not "not found"
```

**Acceptance Gate** (both must pass before Phase 1 starts):

- [ ] Working code: n/a this phase — gate is the README stub naming the real cert library
- [ ] Template serving + cert modules read and their public entry points recorded

---

### Phase 1: Flask server serves the hello-world page over HTTPS

**Goal**: Running `python -m addin.server` (or the documented command) serves
`https://localhost:3000/taskpane.html` returning 200 with the hello-world HTML. This
delivers Scenario 1 end-to-end (with `-k`, before trust is wired).

**TDD approach**: Write `tests/addin/test_server.py` first. Use Flask's test client and a
self-signed cert fixture to assert: (a) `GET /taskpane.html` returns 200; (b) the body
contains the hello-world marker text; (c) an unknown path returns 404 (Could-have, but
cheap to pin now). The server module `src/addin/server.py` is then written to make these
pass. (Note: the test client exercises routing/body; the HTTPS/`ssl_context` binding is
verified by the live `curl` in this phase's Verification, since the test client does not
perform a real TLS handshake.)

**Deliverables**:

1. `src/addin/__init__.py` — package marker.
2. `src/addin/static/taskpane.html` — hello-world page, no app logic.
3. `src/addin/server.py` — Flask app, `static_folder="static"`, route for
   `/taskpane.html`, `app.run(host="localhost", port=3000, ssl_context=(...))`.
4. `tests/addin/test_server.py` — the tests above.

**Verification**:

```text
# Unit tests green:
.venv\Scripts\activate; python -m pytest tests/addin -v
# Live check (server running in another shell, using a cert from Phase 2 or an adhoc cert):
curl -k -s -o /dev/null -w "%{http_code}" https://localhost:3000/taskpane.html   # expect: 200
curl -k -s https://localhost:3000/taskpane.html | findstr /i "hello"             # expect: hello-world text
```

> **Ordering note**: Phase 1's *live* `curl` check needs a certificate, which Phase 2
> produces. The two phases are not strictly sequential at verification time. Either run
> Phase 2's `make_cert` first, or use a temporary throwaway cert (Flask
> `ssl_context="adhoc"`, or an OpenSSL one-liner) for this live check and re-confirm
> after Phase 2. The *unit-test* gate below is fully independent of Phase 2.

**Acceptance Gate** (both must pass before the slice is declared serving-complete; the
live `curl` may use a temporary cert pending Phase 2):

- [ ] Working code: the server starts and the two `curl` checks pass (cert may be temporary)
- [ ] `python -m pytest tests/addin -v` is green

---

### Phase 2: Python certificate generation and local trust

**Goal**: Running the documented certificate command generates a `localhost` certificate
with Python only and installs it into the Windows trust store, so the page opens in a
browser with no certificate warning. Delivers Scenario 2.

**TDD approach**: Write `tests/addin/test_make_cert.py` first, asserting the *pure*,
testable parts: after running generation against a temp directory, `cert.pem` and
`key.pem` exist, are non-empty, and the certificate's subject/SAN is `localhost` and is
currently valid (parse with the cert library). The actual trust-store install is an
operating-system side effect that **cannot** be unit-tested portably — it is verified
manually (human-verify) and guarded by a clear error path, not asserted in pytest.

**Deliverables**:

1. `src/addin/make_cert.py` — wraps the template's cert port; writes `cert.pem`/`key.pem`
   into `src/addin/certs/`; attempts trust-store install; on failure prints an actionable
   message naming the elevated-shell requirement.
2. `tests/addin/test_make_cert.py` — generation/parse assertions (no trust-store assertion).
3. `.gitignore` entry for `src/addin/certs/`.

**Verification**:

```text
.venv\Scripts\activate; python -m pytest tests/addin -v        # cert generation tests green
python -m addin.make_cert                                       # generates + trusts (elevated shell on Windows)
# Then, in a browser, open https://localhost:3000/taskpane.html and confirm NO warning + padlock  [human-verify]
```

**Acceptance Gate** (both must pass before the slice is done):

- [ ] Working code: cert generates; browser opens the page with no warning [human-verify: browser padlock]
- [ ] `python -m pytest tests/addin -v` is green

---

### Phase 3: No-Node.js audit and reproducibility doc

**Goal**: Prove the no-Node.js premise and make both acceptance scenarios reproducible
from the repository by a reviewer with no template knowledge.

**TDD approach**: n/a (audit + documentation). The audit is a command assertion.

**Deliverables**:

1. `src/addin/README.md` (completed) — the two commands (generate cert; start server)
   and the chosen port, written for an uninitiated reviewer.
2. Confirmed-clean Node-artifact audit.

**Verification**:

```text
git ls-files src/addin | findstr /i "package.json node_modules"   # expect: NO output
```

**Acceptance Gate**:

- [ ] `git ls-files src/addin` shows no `package.json` and no `node_modules` (FR-004)
- [ ] README reproduces both scenarios with only the documented commands (FR-007, SC-005)

## File Inventory

| Phase | New Files | Count |
| ----- | --------- | ----- |
| 0 | `src/addin/README.md` (stub) | 1 |
| 1 | `src/addin/__init__.py`, `src/addin/server.py`, `src/addin/static/taskpane.html`, `tests/addin/test_server.py` | 4 |
| 2 | `src/addin/make_cert.py`, `tests/addin/test_make_cert.py`, `.gitignore` entry (edit, not new) | 2 |
| 3 | `src/addin/README.md` (completed — edit, not new) | 0 |

**Total new**: ~7 | **Total deleted**: ~0

## Library Best Practices

### Flask

- **Import path**: `from flask import Flask`. Serve static files by constructing
  `Flask(__name__, static_folder="static", static_url_path="")` and returning
  `app.send_static_file("taskpane.html")` from the route (confirmed via Context7).
- **API gotchas**: HTTPS in the development server is native — `app.run(ssl_context=(cert_path, key_path))`, or the CLI `flask run --cert=cert.pem --key=key.pem` (added in Flask 1.0; confirmed via Context7). `ssl_context="adhoc"` exists but requires `cryptography` and produces an *untrusted* cert each run — **not** used here, because Scenario 2 needs a *trusted* cert generated by the template's port.
- **Confirmed pattern**:
  ```python
  from pathlib import Path
  from flask import Flask

  HERE = Path(__file__).resolve().parent     # cert paths resolve to the package dir,
  CERT = HERE / "certs" / "cert.pem"          # NOT the process working directory, so
  KEY = HERE / "certs" / "key.pem"            # the server starts from any cwd (F4).

  app = Flask(__name__, static_folder="static", static_url_path="")

  @app.route("/taskpane.html")
  def taskpane():
      return app.send_static_file("taskpane.html")

  if __name__ == "__main__":
      app.run(host="localhost", port=3000, ssl_context=(str(CERT), str(KEY)))
  ```

### Certificate library (to confirm in Phase 0)

- **Import path**: expected `cryptography` (the standard Python self-signed cert path);
  **confirm against the template** before relying on it. If the template uses a different
  library, record it in D-table note D5 and update Technical Context.
- **API gotchas**: certificate must carry `localhost` in the Subject Alternative Name
  (SAN), not only the Common Name (CN) — modern browsers ignore CN. The template's port
  is presumed correct here; Phase 2's test parses the SAN to confirm.
- **Confirmed pattern**: deferred to Phase 0 (do not fabricate the template's API).

## Risk Register

| Risk | Mitigation |
| ---- | ---------- |
| Windows trust-store write denied without an elevated shell | `make_cert.py` detects the failure and prints an actionable "re-run from an administrator shell" message; documented in README; Scenario 2 confirmed by human-verify before declaring done |
| Template's cert port uses an unexpected/abandoned library or API | Phase 0 reads the real code and names the library before any adaptation; Phase 2 test parses the generated cert to confirm it is valid and SAN=localhost |
| Port 3000 already in use | Surface bind failure loudly; port is a single documented constant, trivially changed; record final value in README |
| Flask `ssl_context` cert paths relative to working directory | Resolve cert paths relative to the package directory, not the process CWD, so the server starts from any directory |
| `addin` accidentally imported by product code (`marker`/`rl`/`web`) | Generic dev harness must stay leaf; not added to wheel build; reviewers watch for inbound imports (formal import-linter contract deferred as a later hardening step) |

## Glossary

| Term | Definition |
| ---- | ---------- |
| Taskpane | The web panel a Microsoft Office add-in displays docked beside the document; loaded from a web URL, not from local files. |
| Sideload | Installing an Office add-in for development/testing without going through the official store — out of scope here (#191). |
| Manifest | The XML/JSON file that tells Office where to load an add-in's taskpane from — out of scope here (#191). |
| `office-addin-dev-certs` | Microsoft's Node.js tool that creates and trusts a local HTTPS certificate for add-in development; this project uses the template's **Python** re-implementation instead. |
| Subject Alternative Name (SAN) | The field in an HTTPS certificate listing the hostnames it is valid for (here, `localhost`); modern browsers require the hostname here, not in the legacy Common Name field. |
