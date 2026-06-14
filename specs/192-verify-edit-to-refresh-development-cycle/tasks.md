# Tasks: Verify Edit-to-Refresh Development Cycle

**Input**: [plan.md](./plan.md)
**Prerequisites**: [#191](https://github.com/redmarklogic/redline/issues/191) sideload complete — the taskpane can be opened in desktop Microsoft Word and the Python development server (`python -m addin.server`) serves it over locally-trusted HTTPS. Phase 0 below is independent of [#191](https://github.com/redmarklogic/redline/issues/191) and can land regardless; Phase 1 requires the sideloaded pane.

<!-- Vertical-slice sizing: Phase 0 is one complete behaviour (reload is never stale).
     Phase 1 is one complete behaviour (loop confirmed + written down). Not split by layer. -->

## Phase 0: Reliable reload (cache-busting headers)

**Purpose**: The development server never lets the embedded web view serve a stale page — the taskpane response carries `Cache-Control: no-store`. Runnable server + green tests.

### Tests (write first — must fail before implementation begins)

- [ ] T001 [Phase 0] Write failing test in `tests/addin/test_server.py`: a GET of `/taskpane.html` returns a response whose `Cache-Control` header contains `no-store` (and assert `Pragma: no-cache` is present).
- [ ] T002 [Phase 0] Confirm the test fails (header not yet sent): `.venv\Scripts\activate; rtk python -m pytest tests/addin/test_server.py -v`

### Implementation

- [ ] T003 [Phase 0] In `src/addin/server.py` `taskpane()`, add `"Cache-Control": "no-store"` and `"Pragma": "no-cache"` to the existing response-headers dict (keep `Content-Type`). Minimal diff — do not introduce a `Response` object (plan: Library Best Practices).

### Acceptance Gate

- [ ] T004 [Phase 0] Verify working code: start the server on the configured add-in port and confirm the header is served — `.venv\Scripts\activate; $env:ADDIN_PORT='8767'; rtk python -m addin.server` then `curl -k -I https://localhost:8767/taskpane.html` shows `Cache-Control: no-store`. Bare `python -m addin.server` defaults to port 3000 ([server.py:28](../../src/addin/server.py#L28)); `ADDIN_PORT` must be set so the curl port matches (8767 from `config/dev-endpoints.json`). Cert via `rtk python -m addin.make_cert` first if absent.
- [ ] T005 [Phase 0] Function file modified — run pytest: `.venv\Scripts\activate; rtk python -m pytest tests/addin -v` — all tests green.

---

## Phase 1: Human verification + documented refresh cycle

**Purpose**: A developer confirms the edit-to-refresh loop in desktop Word and writes it down so a second person can reproduce it. Acceptance is human observation plus a documented runbook — there is no automated test for installed-Word behaviour.

### Verification (human — cannot be automated)

- [ ] T006 [Phase 0→1 bridge] Start the dev server **via the launcher** so the bound port matches the manifest, and open the already-sideloaded pane in desktop Word: `rtk python -m addin.make_cert` (if certs absent), then `tasks/run-app.ps1` (sets `ADDIN_PORT=8767` and rebuilds the catalog manifest so the pane URL matches the bound port — see `run-app.ps1:140,155`), then open the pane (per [#191](https://github.com/redmarklogic/redline/issues/191) runbook). Do **not** launch bare `python -m addin.server` here — it binds port 3000 and the pane, which loads `https://localhost:8767`, will fail.
- [ ] T007 [Phase 1] `[human-verify]` Change a visible string in `src/addin/static/taskpane.html` (e.g. the `Hello, world` heading), save, then reload the pane with right-click → Reload. Confirm the new string appears **without restarting Word and without re-sideloading** the add-in (FR-001, FR-002, SC-001).
- [ ] T008 [Phase 1] `[human-verify]` If right-click → Reload does not surface the change, use the fallback (close and reopen the pane) and record which action was actually required (Edge Case: dead reload).
- [ ] T009 [Phase 1] `[human-verify]` Time the loop from save to visible change; confirm it is seconds, not minutes (SC-002).

### Documentation

- [ ] T010 [Phase 1] Create `specs/192-verify-edit-to-refresh-development-cycle/quickstart.md` with a `## Refresh cycle` section recording: the exact reload steps used, which reload action worked (Reload vs reopen), the rough loop time, and a one-line note distinguishing the page-edit loop from the Python server-code loop (server auto-restarts under `use_reloader=True`). Must be reproducible by a reader who has not performed the loop (FR-005, SC-003, SC-004).

### Acceptance Gate

- [ ] T011 [Phase 1] `[human-verify]` Confirm SC-001 and SC-002 both observed (edit visible after reload, no restart/re-sideload, loop in seconds).
- [ ] T012 [Phase 1] Doc check: `grep -i "refresh cycle" specs/192-verify-edit-to-refresh-development-cycle/quickstart.md` returns the section heading; section contains steps + rough loop time.

---

## Phase Z: Polish

- [ ] T013 [P] [Phase Z] Run full add-in test suite and lint: `.venv\Scripts\activate; rtk python -m pytest tests/addin -v; rtk ruff check src/addin`
- [ ] T014 [Phase Z] Run `python-static-checks` skill before declaring complete.
- [ ] T015 [Phase Z] Complete the work via `/make-pr`.

### Acceptance Gate

- [ ] T016 [Phase Z] All add-in tests green and lint clean; quickstart.md `## Refresh cycle` section present.

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies).
- `[Phase N]` = which plan phase the task belongs to.
- TDD is mandatory for the one function change (T001→T002→T003): write failing test (Red), confirm it fails, implement (Green).
- The Acceptance Gate at the end of each phase is a hard stop — do not start the next phase until it passes. Phase 0 is the only phase with automated tests; Phase 1 gates on human observation + the documented runbook.
- `[human-verify]` tasks (T007–T009, T011) require the founder/developer in desktop Word — they cannot be completed headlessly.
- Commit after each logical group. Use `/make-pr` to complete (T015).
- **Spec-kit hard stop**: this command does not run implementation. Kabilan implements Phase 0; the founder/developer performs Phase 1 human-verify.
