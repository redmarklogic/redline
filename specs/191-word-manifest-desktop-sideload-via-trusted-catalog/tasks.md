# Tasks: Word manifest + desktop sideload via trusted catalog

**Input**: [plan.md](./plan.md) | [spec.md](./spec.md)
**Prerequisites**: Issue #190 merged (Flask HTTPS server, `make_cert`, taskpane.html in
`src/addin/`); project virtual environment synced (`uv sync`); desktop Microsoft Word on
Microsoft 365 or Word 2019+ (ADR-028 floor).

<!-- Each task is a vertical slice toward a working, demonstrable result. TDD is mandatory
     for the Python build function; the sideload itself is a human-verified Office side
     effect (no automated test, by the same boundary #190 drew). -->

## Phase 0: Manifest build (headless, fully testable)

**Purpose**: `python -m addin.build_manifest` writes a well-formed Word manifest whose
taskpane URL is derived from `config/dev-endpoints.json` — the address can never drift.

### Tests (write first — must fail before implementation begins)

- [x] T001 [Phase 0] Write failing tests in `tests/addin/test_build_manifest.py` against a
  `build_manifest_xml(config_path, template_path)` pure function, asserting: (a) output is
  well-formed XML (`ET.fromstring` does not raise); (b) `SourceLocation` DefaultValue equals
  `https://localhost:<port>/taskpane.html` where `<port>` is read from the same config
  fixture (no-drift, spec FR-002); (c) a Word host `Host Name="Document"` is present
  (FR-003); (d) the `WordApi` `MinVersion="1.3"` Set is present (FR-009 / ADR-028 D1); (e)
  the token `__ADDIN_BASE_URL__` does not survive in the output; (f) `AppDomain` equals the
  rendered base URL. Use ElementTree namespace wildcards (`.//{*}SourceLocation`) — the
  manifest declares a default namespace.
- [x] T002 [Phase 0] Confirm the tests fail for the right reason:
  `.venv\Scripts\activate; python -m pytest tests/addin/test_build_manifest.py -v` (Red).

### Implementation

- [x] T003 [Phase 0] Create `src/addin/manifest.template.xml` — the committed add-in-only
  (`xsi:type="TaskPaneApp"`) template: fixed `<Id>954abf42-47ef-4a32-a705-933e1fb46c57</Id>`,
  `<DisplayName DefaultValue="Redline (dev)"/>`, `<Hosts><Host Name="Document"/></Hosts>`,
  the ADR-028 `<Requirements><Sets DefaultMinVersion="1.3"><Set Name="WordApi"
  MinVersion="1.3"/></Sets></Requirements>` block, `<Permissions>ReadWriteDocument</Permissions>`,
  and `__ADDIN_BASE_URL__` tokens in `SourceLocation` and `AppDomain` (template shape in
  plan.md → Architecture). No `IconUrl` (D9 — icons omitted).
- [x] T004 [Phase 0] Implement `src/addin/build_manifest.py`: a pure
  `build_manifest_xml(config_path, template_path)` that reads the `addin` surface from
  `config/dev-endpoints.json`, computes `f"{scheme}://localhost:{port}"`, and substitutes the
  `__ADDIN_BASE_URL__` token; plus `main()` that writes the rendered XML to
  `src/addin/catalog/manifest.xml` (creating the dir) and prints the catalog folder path to
  register. Standard library only (D4).

### Acceptance Gate

- [x] T005 [Phase 0] Verify working code:
  `.venv\Scripts\activate; python -m addin.build_manifest; python -c "import xml.etree.ElementTree as ET; ET.parse('src/addin/catalog/manifest.xml')"`
  — the file is written and `ET.parse` exits 0.
- [x] T006 [Phase 0] Run pytest:
  `.venv\Scripts\activate; python -m pytest tests/addin -v` — all tests green.

---

## Phase 1: Trusted-catalog sideload (the proof — human-verified)

**Purpose**: The hello-world taskpane opens in desktop Word, loaded from the local server via
the trusted-catalog manifest, and the procedure is written down (the sprint tripwire).

- [ ] T007 [Phase 1] Bring up the #190 preconditions: `.venv\Scripts\activate; python -m
  addin.make_cert`, then start the server (`tasks\run-app.ps1`, or `$env:ADDIN_PORT=8767;
  python -m addin.server`); confirm
  `curl -k -s -o NUL -w "%{http_code}" https://localhost:8767/taskpane.html` returns `200`
  and the browser padlock shows no warning.
- [ ] T008 [Phase 1] In desktop Word, register `src/addin/catalog/` under **File → Options →
  Trust Center → Trust Center Settings → Trusted Add-in Catalogs**: paste the folder path, add
  it, tick **Show in Menu**, OK, and **restart Word**. *[human]*
- [ ] T009 [Phase 1] Open **Insert → My Add-ins → Shared Folder**, select **Redline (dev)**,
  and confirm the hello-world pane opens in the side panel. *[human-verify]*
- [ ] T010 [Phase 1] Recovery path: if the add-in is missing or shows a stale page, close
  Word, delete the Wef cache (`%LOCALAPPDATA%\Microsoft\Office\16.0\Wef\`; `16.0` is the
  current Office major-version folder — adjust if yours differs), reopen, and retry; if Word
  rejected the local folder path, share `src/addin/catalog/` and register the UNC path
  (`\\<machine>\<share>`) instead.
- [x] T011 [Phase 1] Write the runbook to
  `specs/191-word-manifest-desktop-sideload-via-trusted-catalog/spike-notes.md` capturing the
  exact steps performed (preconditions, catalog registration, the Wef cache-clear, pane
  verification, and any UNC fallback used) — the spec FR-006 deliverable and the #198 seed.

### Acceptance Gate

- [ ] T012 [Phase 1] Human-verified: the hello-world pane opens via Insert → My Add-ins →
  Shared Folder, and `spike-notes.md` exists and is reproducible by a second person
  (spec SC-003).

---

## Phase 2: Polish

**Purpose**: Clear the staleness the source reconciliation flagged and leave the harness clean.

- [x] T013 [P] [Phase 2] Fix `src/addin/README.md`: change the documented listening port from
  `3000` to `8767` (the committed source of truth) and add a one-line pointer to the
  manifest build and sideload runbook.
- [x] T014 [P] [Phase 2] Add `src/addin/catalog/` to `.gitignore` (rendered manifest is a
  generated artifact, mirroring the existing `src/addin/certs/` entry).
- [x] T015 [Phase 2] (Could) Wire `python -m addin.build_manifest` into `tasks/run-app.ps1`
  ahead of the server starts so the catalog manifest is always regenerated at launch.
- [x] T016 [Phase 2] Run full checks:
  `.venv\Scripts\activate; python -m pytest tests/addin -v; python -m ruff check src/addin tests/addin`.

### Acceptance Gate

- [x] T017 [Phase 2] All `tests/addin` tests green, ruff clean, README no longer cites port
  3000, and `git status` shows `src/addin/catalog/` ignored.

## Execution Notes

- `[P]` = parallelizable (different files, no dependency). `[Phase N]` = plan phase.
- TDD is mandatory for the build function: T001 (write failing tests) → T002 (confirm Red) →
  T003/T004 (Green) → refactor. The Phase 0 pytest gate (T006) is a hard stop.
- Phase 1 is human-verified — it is the tripwire. Do not start Phase 2 until T012 passes.
- Commit after each task or logical group (e.g. T003+T004 together).
- Constraint reminders: standard library only (no Node, no new dependency); `localhost` host
  with the port from config; the `addin` package stays outside the import-linter contracts.
- Run `python-static-checks` before declaring complete; finish with the `/make-pr` command.
