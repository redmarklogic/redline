# Implementation Plan: Verify Edit-to-Refresh Development Cycle

**Branch**: `feature/192-verify-edit-to-refresh-development-cycle` | **Date**: 2026-06-14 | **Spec**: [spec.md](./spec.md)

**Status**: Draft

## Summary

This is a verification spike: its job is to prove, and then write down, that a developer can change the Microsoft Word taskpane's page on disk and see that change inside Word in seconds — without restarting Word or re-installing the add-in. A "taskpane" is the small web page Word shows in a side panel; in this project it is plain HyperText Markup Language (HTML) and vanilla JavaScript served by a small Python web server (Flask), not a Node.js application.

The technical approach has two parts. First, a small, test-covered hardening of the development server so the reload is *reliable*: the embedded web view inside Word (Microsoft Edge WebView2) can cache the previous version of the page and show it again, hiding the edit; sending cache-disabling response headers (`Cache-Control: no-store`) from the server removes that failure mode entirely rather than gambling on per-machine cache behaviour. Second, a human-performed verification inside desktop Word followed by writing the confirmed steps and rough loop time into a "refresh cycle" section of this feature's runbook, which seeds the demonstration-and-skill-writeup task ([#198](https://github.com/redmarklogic/redline/issues/198)).

The affected code lives in the Generic `src/addin` package (the throwaway local development harness from [#190](https://github.com/redmarklogic/redline/issues/190)/[#191](https://github.com/redmarklogic/redline/issues/191)). No product code, no new package, no new domain model.

## Technical Context

**Language**: Python 3.14
**Package manager**: uv
**Testing**: pytest (Test-Driven Development workflow per `test-driven-development` skill)
**Project layout**: monorepo (hub package `rl`; this work is in the sibling `addin` package)
**Architecture**: `src/addin` is a Generic-subdomain sibling package, excluded from import-linter root_packages and from wheel build targets (per [#190](https://github.com/redmarklogic/redline/issues/190) decision). It serves a static page over HTTPS via Flask.
**Dev OS**: Windows | **Deploy OS**: N/A (local-only proof of concept; no deployment this sprint)
**Domain modeling**: None — no Pydantic/Pandera models in this spike.
**Layer enforcement**: import-linter contracts in `pyproject.toml` (unchanged by this spike).
**Key dependencies**: Flask (existing dev server); desktop Microsoft Word + Edge WebView2 runtime (the human-verification environment, not a code dependency).

## Design Decisions

| #  | Decision | Choice | Rationale |
| -- | -------- | ------ | --------- |
| D1 | How the pane is reloaded | In-Word right-click → "Reload" as the primary action; close-and-reopen the pane as the fallback | Honours the source no-go: no file-watcher / auto-reload tooling. These are the means a developer already has inside Word, requiring no new dependency. |
| D2 | Source of staleness | The server is **not** the cause — `taskpane()` reads the file fresh on every request ([server.py:43](../../src/addin/server.py#L43)) — so any stale page comes from the WebView2 cache, not from Python holding old content | Avoids "fixing" the wrong layer. Grounds the remedy (D3) in where the problem actually is. |
| D3 | Cache remedy | Send `Cache-Control: no-store` (and `Pragma: no-cache`) on the taskpane response **unconditionally**, not only if a stale page is observed | A development server under `debug=True` should never cache. Setting it proactively guarantees the loop on any machine regardless of WebView2 version differences, and turns the "rabbit hole" risk into a deterministic, test-covered fact. Cheap belt-and-braces for a PoC. |
| D4 | Where the spike notes live | This feature's runbook at `specs/192-verify-edit-to-refresh-development-cycle/quickstart.md`, containing a `## Refresh cycle` section | Satisfies the acceptance "file exists with a 'refresh cycle' section". The [#198](https://github.com/redmarklogic/redline/issues/198) writer (Founder) consolidates sprint spike notes into the durable taskpane skill; quickstart.md is the agreed interim home, consistent with the spike-notes pattern used in [#191](https://github.com/redmarklogic/redline/issues/191). |
| D5 | What counts as "done" for the human step | A developer observes an edited visible string appear after a reload, times the loop, and confirms it is seconds not minutes | The primary acceptance is irreducibly human (`[human-verify]`) — it depends on installed desktop Word behaviour no automated test can exercise. |

## Domain Impact

**Modularity assessment**: No new package. All changes confined to the existing Generic `src/addin` package (the local dev harness). No signal from the `python-domain-modeling` decision matrix points to a new boundary — this is throwaway tooling, not product domain.
**New packages**: None.
**Bounded context changes**: None.
**Import-linter contract updates**: None — `src/addin` remains excluded from root_packages.
**Subdomain classification**: Generic (off-the-shelf Flask dev server; no custom domain model).
**New domain terms**: None new to the project. (See Glossary for terms a non-specialist reader needs.)

## Architecture

The edit-to-refresh loop and where caching can break it:

```text
Developer edits          Python Flask dev server            Word taskpane (WebView2)
src/addin/static/        (src/addin/server.py)              inside desktop Word
taskpane.html
    |                            |                                   |
    | 1. save file              |                                   |
    |-------------------------->| (no restart needed: file is       |
    |                           |  read fresh on each GET, L43)      |
    |                           |                                   |
    |                           |   2. developer: right-click→Reload |
    |                           |<----------------------------------|  GET /taskpane.html
    |                           |                                   |
    |                           |---- 200 + Cache-Control: no-store ->|  3. fresh page shown
    |                           |     (D3: forces WebView2 to refetch)|     edit is visible
```

Without D3, step 3 risks the WebView2 cache returning the *previous* response, so the developer sees the old page even though the server would have served the new one. `no-store` instructs the web view never to reuse a cached copy.

## Domain Models

None. This spike introduces no data models.

## MoSCoW

| Category | Items |
| -------- | ----- |
| **Must have** | (a) Server sends `Cache-Control: no-store` on the taskpane response, covered by a unit test (FR-004). (b) Human verification in desktop Word: edited visible string appears after an in-Word reload with no Word restart and no re-sideload (FR-001, FR-002, SC-001). (c) `## Refresh cycle` section written to quickstart.md with steps + rough loop time (FR-005, SC-004). |
| **Should have** | Loop confirmed to be seconds not minutes (SC-002); reload procedure limited to in-Word means only (FR-003); notes reproducible by a second person (SC-003). |
| **Could have** | A one-line note in the runbook distinguishing the page-edit loop from the Python server-code loop (server already auto-restarts under `use_reloader=True`). |
| **Won't have (this time)** | File-watcher / live-reload tooling; verification of the server-code edit loop; any deployed-caching behaviour; taskpane visual design. |

## Phased Delivery

### Phase 0: Reliable reload (cache-busting headers)

**Goal**: The development server never lets the web view serve a stale page — the taskpane response carries `Cache-Control: no-store`. Working code, green tests.

**TDD approach**: Write the test first in `tests/addin/test_server.py`: a request to `/taskpane.html` returns a `Cache-Control` header whose value disables storing (`no-store`). Watch it fail, then add the header in `src/addin/server.py` `taskpane()` to make it pass.

**Deliverables**:

1. `tests/addin/test_server.py` — new test asserting the no-store cache header on the taskpane response.
2. `src/addin/server.py` — `taskpane()` returns `Cache-Control: no-store` (and `Pragma: no-cache`) alongside the existing `Content-Type`.

**Verification**:

```
.venv\Scripts\activate; rtk python -m pytest tests/addin/test_server.py -v
# expect: all green, including the new cache-header test
```

**Acceptance Gate** (both must pass before Phase 1 starts):
- [ ] Working code: the server starts and serves `/taskpane.html` with the cache header.
- [ ] Function file modified: `rtk python -m pytest tests/addin -v` is green.

---

### Phase 1: Human verification + documented refresh cycle

**Goal**: A developer confirms the loop in desktop Word and records it. This phase produces evidence and documentation, not automated tests — its acceptance is human observation.

**TDD approach**: Not applicable — this phase exercises installed desktop Word, which no automated test in this codebase can drive. The automated guarantee that the loop *can* work (the cache header) was delivered in Phase 0.

**Deliverables**:

1. Performed verification: with the pane sideloaded (from [#191](https://github.com/redmarklogic/redline/issues/191)) and the server running, edit a visible string in `src/addin/static/taskpane.html`, save, reload the pane in Word, observe the change, and time the loop.
2. `specs/192-verify-edit-to-refresh-development-cycle/quickstart.md` — a runbook whose `## Refresh cycle` section records the confirmed reload steps and the rough loop time (FR-005), reproducible by a second person.

**Verification**:

```
# Human-verify (cannot be automated):
#  1. python -m addin.make_cert  (if certs absent); python -m addin.server
#  2. open the sideloaded pane in desktop Word
#  3. change "Hello, world" to a new string in taskpane.html, save
#  4. right-click the pane -> Reload  (fallback: close + reopen the pane)
#  5. confirm the new string shows; Word was NOT restarted; add-in NOT re-sideloaded
#  6. note the seconds elapsed
# Doc check:
grep -i "refresh cycle" specs/192-verify-edit-to-refresh-development-cycle/quickstart.md
```

**Acceptance Gate**:
- [ ] `[human-verify]` Edited string visible after reload, no Word restart, no re-sideload (SC-001).
- [ ] `[human-verify]` Loop is seconds, not minutes (SC-002).
- [ ] quickstart.md exists and contains a `## Refresh cycle` section with steps + rough loop time (SC-004).

## File Inventory

| Phase | New / Modified Files | Count |
| ----- | -------------------- | ----- |
| 0 | `src/addin/server.py` (modified), `tests/addin/test_server.py` (modified) | 0 new / 2 modified |
| 1 | `specs/192-verify-edit-to-refresh-development-cycle/quickstart.md` (new) | 1 new |

**Total new**: ~1 | **Total modified**: ~2 | **Total deleted**: 0

## Library Best Practices

### Flask

- **Import path**: `from flask import Flask` (already in use).
- **API gotchas**: A view may return a `(body, status, headers)` tuple; `headers` is a dict merged into the response. The existing `taskpane()` already returns `(text, 200, {"Content-Type": ...})` — add the cache keys to that same dict rather than constructing a `Response` object, to keep the diff minimal.
- **Confirmed pattern**: `return TASKPANE.read_text(...), 200, {"Content-Type": "text/html", "Cache-Control": "no-store", "Pragma": "no-cache"}`.

## Risk Register

| Risk | Mitigation |
| ---- | ---------- |
| WebView2 still serves a stale page despite `no-store` (older runtime, aggressive caching) | Fallback reload action is close-and-reopen the pane (forces a fresh navigation); record in the runbook whichever action was actually required. |
| The pane is not actually sideloaded yet ([#191](https://github.com/redmarklogic/redline/issues/191) human steps incomplete) | This spike depends on [#191](https://github.com/redmarklogic/redline/issues/191)'s sideload; if blocked, Phase 1 cannot run. Phase 0 (cache header + test) is independent and can land regardless. |
| quickstart.md is inside a spec dir that could later be archived (as [#191](https://github.com/redmarklogic/redline/issues/191)'s was), losing the notes before [#198](https://github.com/redmarklogic/redline/issues/198) consumes them | [#198](https://github.com/redmarklogic/redline/issues/198) (Founder) consolidates the refresh-cycle section into the durable taskpane skill; until then the section is the seed, not the final home. Noted for the [#198](https://github.com/redmarklogic/redline/issues/198) owner. |

## Glossary

| Term | Definition |
| ---- | ---------- |
| Taskpane | The small web page Microsoft Word displays in a side panel; here, plain HTML + JavaScript served by Python. |
| Sideload | Installing a Word add-in for development from a trusted local source rather than from the official store. |
| WebView2 | The Microsoft Edge web view embedded in desktop Word that renders the taskpane; it has its own cache. |
| Hot reload | A development loop where a saved file change appears in the running app without a manual rebuild; here verified for the Python-served pane. |
| Spike | A short, time-boxed investigation whose output is an answer plus written notes, not shipped product features. |
