# Tasks: Python-served Word taskpane over locally-trusted HTTPS

**Input**: `plan.md` in this directory
**Prerequisites**: `spec.md` and `plan.md` exist and are approved. Python 3.14 + uv
environment active. Windows development machine (an administrator/elevated shell is
needed for Phase 2's trust-store step). No Node.js is required or permitted in
`src/addin`.

<!-- Task sizing: each task is a vertical slice of user-visible behaviour. Phases
     follow plan.md. TDD is mandatory for every function file. -->

## Phase 0: Obtain and audit the Masterjx9 template

**Purpose**: Read the template's real serving and certificate code, name the actual
certificate library, and stub the README — so later phases adapt real code, not guesses.

- [ ] T001 [Phase 0] Obtain the Masterjx9 Outlook-Addin-TaskPane template (clone or download to a scratch location outside `src/`); locate its Flask serving entry point and its `office-addin-dev-certs` Python port; record the file paths.
- [ ] T002 [Phase 0] Identify the exact certificate-generation library the template's cert port imports (expected `cryptography`; confirm) and its public entry function(s).
- [ ] T002a [Phase 0] Name the trust-store install mechanism the template uses (expected Windows `certutil -addstore -user Root <cert>` or PowerShell `Import-Certificate`); record it. Scenario 2 depends on this — it must be a named mechanism, not a black box.
- [ ] T003 [Phase 0] Create `src/addin/README.md` stub recording: template source URL, which template files are reused, the confirmed certificate library, the trust-store mechanism (T002a), and a placeholder for the two run commands + chosen port.

### Acceptance Gate

- [ ] T004 [Phase 0] Verify the confirmed cert library resolves under uv: `uv pip show <cert-library>` prints a version (not "not found"). If the template uses a library not in the environment, add it via `uv add <lib>` and record in plan.md D5 note.
- [ ] T005 [Phase 0] No pytest yet (no function files). Gate is the README stub naming the real cert library and entry points.

---

## Phase 1: Flask server serves the hello-world page over HTTPS

**Purpose**: `python -m addin.server` serves `https://localhost:3000/taskpane.html`
returning 200 with hello-world HTML — Scenario 1 end-to-end (with `curl -k`).

### Tests (write first -- must fail before implementation begins)

- [ ] T006 [Phase 1] Write failing tests in `tests/addin/test_server.py` using Flask's test client: (a) `GET /taskpane.html` returns 200; (b) body contains the hello-world marker text; (c) an unknown path returns 404.
- [ ] T007 [Phase 1] Confirm tests fail (no server module yet): `.venv\Scripts\activate; python -m pytest tests/addin/test_server.py -v`

### Implementation

- [ ] T008 [P] [Phase 1] Create `src/addin/__init__.py` (package marker) and `src/addin/static/taskpane.html` (hello-world page, no app logic, no API calls, no auth — FR-005).
- [ ] T009 [Phase 1] Implement `src/addin/server.py`: `Flask(__name__, static_folder="static", static_url_path="")`, route `/taskpane.html` returning `send_static_file`, `app.run(host="localhost", port=3000, ssl_context=("certs/cert.pem","certs/key.pem"))` with cert paths resolved relative to the package dir (not CWD). Make T006 tests pass.

### Acceptance Gate

- [ ] T010 [Phase 1] Verify working code (server running in a second shell, using a cert from Phase 2 or a temporary adhoc cert): `curl -k -s -o /dev/null -w "%{http_code}" https://localhost:3000/taskpane.html` prints `200`; `curl -k -s https://localhost:3000/taskpane.html | findstr /i "hello"` shows the hello text.
- [ ] T011 [Phase 1] Run pytest: `.venv\Scripts\activate; python -m pytest tests/addin -v` — all green.

---

## Phase 2: Python certificate generation and local trust

**Purpose**: One Python command generates a trusted `localhost` certificate (no Node.js)
so the page opens in a browser with no warning — Scenario 2.

### Tests (write first -- must fail before implementation begins)

- [ ] T012 [Phase 2] Write failing tests in `tests/addin/test_make_cert.py`: running generation against a temp directory produces non-empty `cert.pem` and `key.pem`, and the parsed certificate has Subject Alternative Name (SAN) `localhost` and is currently valid. Do NOT assert the OS trust-store install (not portably testable).
- [ ] T013 [Phase 2] Confirm tests fail: `.venv\Scripts\activate; python -m pytest tests/addin/test_make_cert.py -v`

### Implementation

- [ ] T014 [Phase 2] Implement `src/addin/make_cert.py` adapting the template's cert port: write `cert.pem`/`key.pem` into `src/addin/certs/`; attempt Windows trust-store install; on failure print an actionable message naming the elevated-shell requirement (edge case). Make T012 tests pass.
- [ ] T015 [P] [Phase 2] Add `src/addin/certs/` to `.gitignore` (generated secrets must not be committed).

### Acceptance Gate

- [ ] T016 [Phase 2] Verify working code: `python -m addin.make_cert` generates the cert and trusts it (run from an elevated shell on Windows); then open `https://localhost:3000/taskpane.html` in a desktop browser and confirm NO certificate warning + padlock present `[human-verify: browser padlock]`.
- [ ] T017 [Phase 2] Run pytest: `.venv\Scripts\activate; python -m pytest tests/addin -v` — all green.

---

## Phase 3: No-Node.js audit and reproducibility doc

**Purpose**: Prove the no-Node.js premise (FR-004) and make both scenarios reproducible
by an uninitiated reviewer from the documented commands (FR-007, SC-005).

- [ ] T018 [Phase 3] Complete `src/addin/README.md`: the two commands (generate cert; start server), the chosen port, and the elevated-shell note — written for a reviewer who has never seen the template.
- [ ] T019 [Phase 3] Run the Node-artifact audit: `git ls-files src/addin | findstr /i "package.json node_modules"` — confirm NO output (FR-004, SC-004).

### Acceptance Gate

- [ ] T020 [Phase 3] `git ls-files src/addin` shows no `package.json` and no `node_modules`; README reproduces both acceptance scenarios using only the documented commands.

---

## Phase Z: Polish

- [ ] T021 [P] [Phase Z] Confirm `src/addin` is NOT added to `[tool.importlinter] root_packages` and NOT added to wheel build targets in `pyproject.toml` (it is a non-shipped Generic dev harness — plan D3).
- [ ] T022 [Phase Z] Run full add-in suite and lint: `.venv\Scripts\activate; python -m pytest tests/addin -v; python -m ruff check src/addin`
- [ ] T023 [Phase Z] Run `python-static-checks` over `src/addin` before declaring complete.

### Acceptance Gate

- [ ] T024 [Phase Z] All `tests/addin` tests green, lint clean, and both live acceptance checks (Scenario 1 `curl` 200; Scenario 2 browser padlock [human-verify]) confirmed.

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies)
- `[Phase N]` = which plan phase the task belongs to
- TDD is mandatory for all function work (`server.py`, `make_cert.py`): write failing test (Red), confirm it fails, implement (Green), refactor
- The Acceptance Gate at the end of each phase is a hard stop — do not start the next phase until it passes
- Phase 1 and Phase 2 have a soft ordering dependency only at verification time: Phase 1's live `curl` (T010) needs a cert, which Phase 2 (T014) produces. Acceptable orderings: run Phase 2's `make_cert` before T010, or use a temporary adhoc cert for T010 then re-verify after Phase 2. Unit tests in each phase are independent.
- Commit after each task or logical group
- Use `subagent-driven-development` skill (preferred) or execute tasks directly
- Run `python-static-checks` before declaring implementation complete
- Use `/make-pr` command to complete the work

> **Scope reminder (no-gos):** hello-world content only — no document scanning, no API
> calls, no auth, no Word manifest, no sideload, no deployment. Those are issues #191,
> #192, #193, #196, #197 and Sprint 5+. This slice ends at "Python serves the page over
> trusted HTTPS."
