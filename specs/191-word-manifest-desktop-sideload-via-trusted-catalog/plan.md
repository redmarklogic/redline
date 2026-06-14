# Implementation Plan: Word manifest + desktop sideload via trusted catalog

**Date**: 2026-06-14 | **Spec**: [spec.md](./spec.md)
**Status**: Draft

## Summary

This task gives Microsoft Word an instruction sheet — an Office Add-in *manifest* (an
Extensible Markup Language, XML, file) — that points Word at the hello-world taskpane the
previous task (issue #190) already serves over locally-trusted HTTPS, and then proves that
manifest can be loaded into desktop Word on Windows. Loading is done by *sideloading via a
trusted catalog*: a folder on the developer's machine, registered in Word's Trust Center,
that Word is allowed to read add-ins from — no Microsoft 365 administration centre, no
company-wide deployment.

The technical approach has two moving parts. First, a tiny Python build step
(`src/addin/build_manifest.py`) reads the committed single source of truth for local ports
(`config/dev-endpoints.json`), fills the one variable value — the port — into a committed
manifest template, and writes the finished manifest into a local catalog folder. Deriving
the port this way means the manifest address can never drift from the address the server
actually binds. Second, a written runbook records the exact Trust Center steps, including
how to clear Word's aggressive manifest cache, so the sideload is reproducible. Everything
lives in the existing `src/addin/` package, which is dev-only and deliberately excluded from
the shipped product. This is the sprint's go/no-go tripwire task, so the plan front-loads
the risky human step and keeps the automatable part small and test-covered.

## Technical Context

**Language**: Python 3.14
**Package manager**: uv
**Testing**: pytest (Test-Driven Development, TDD, per `test-driven-development` skill)
**Project layout**: monorepo (from `.specify/architecture.yml`; hub package `rl`)
**Architecture**: `src/addin/` is a sibling package under `src/`, classified **Generic**
(dev-only tooling), already excluded from the import-linter contracts and the product wheel
by issue #190. No layered domain model applies.
**Dev OS**: Windows | **Deploy OS**: Linux (not exercised — this task is local-only)
**Domain modeling**: none (no Pydantic/Pandera models; the artifact is an XML file)
**Layer enforcement**: import-linter contracts in `pyproject.toml` — unchanged (the `addin`
package stays outside `root_packages`)
**Key dependencies**: standard library only — `json`, `pathlib`, `xml.etree.ElementTree`
(for the test's well-formedness check). No new third-party dependency; Flask (from #190)
already serves the page.

## Design Decisions

| #  | Decision | Choice | Rationale |
| -- | -------- | ------ | --------- |
| D1 | Manifest format | Add-in-only **XML** manifest (`xsi:type="TaskPaneApp"`), not the unified/JSON manifest | Best-supported route for desktop-Word trusted-catalog sideload; the issue says pick the fastest for a PoC. Unified manifest is the documented fallback. |
| D2 | Taskpane host | `localhost`; port/scheme/path from `config/dev-endpoints.json` | `localhost` is what the #190 server binds ([server.py:59](../../src/addin/server.py#L59)), what the issue's solution outline specifies, and what Office tooling expects. The #190 certificate's Subject Alternative Name covers both `localhost` and `127.0.0.1`. The port is the only value that varies, so it is the only value derived from config. |
| D3 | Address anti-drift | Build step renders a committed template, substituting a `__ADDIN_BASE_URL__` token computed from config | Satisfies spec FR-002. The config `_comment` explicitly anticipates a "future #191 manifest build" that reads it. A token (not a real port) in the template forces the build to fill it, so a stale hard-coded port cannot survive. |
| D4 | Where the build reads config | `build_manifest.py` reads `config/dev-endpoints.json` directly | The config `_comment` blesses the manifest build to read it. This is **build-time tooling** (run from the runbook or the launcher), not runtime app source, so ADR-021 ("app source must use process env, not config files") is not violated — the rule targets the Django/marker app code, not dev generators, exactly as the launcher itself reads the file. |
| D5 | Manifest identity | Fixed `<Id>` GUID `954abf42-47ef-4a32-a705-933e1fb46c57`, committed in the template | A stable identity means re-sideloading (and a second developer's machine) sees one add-in, not a new duplicate each time. |
| D6 | API requirement floor | `<Requirements><Sets DefaultMinVersion="1.3"><Set Name="WordApi" MinVersion="1.3"/></Sets></Requirements>` | ADR-028 D1 mandates this exact block and names this manifest as where it lands (Constitution Principle XIX). Independent of whether the page calls Office.js. |
| D7 | Permissions | `ReadWriteDocument` | The eventual scan/mark/replace work (#197) needs write access; declaring it now avoids a re-consent/re-sideload later. No extra sideload friction. |
| D8 | Catalog location | Local folder `src/addin/catalog/` (gitignored); rendered `manifest.xml` written there | Mirrors #190's gitignored `src/addin/certs/` pattern for generated artifacts. The developer registers this folder's path in the Trust Center. UNC-share fallback documented if a local path is refused. |
| D9 | Icons | **Omitted** from the #191 manifest | `IconUrl`/`HighResolutionIconUrl` are optional in the add-in-only schema; Word shows a default icon. Omitting them avoids 404s and committing binary assets on the tripwire task. A branded icon can be added later (the #190 server already serves `static/` at the root). |

## Domain Impact

**Modularity assessment**: No new package. The work extends the existing `src/addin/`
package (Generic subdomain) created in #190. No decision-matrix signal calls for a new
boundary — this is one more dev artifact in the same throwaway harness.
**New packages**: None.
**Bounded context changes**: None.
**Import-linter contract updates**: None — `addin` remains outside `root_packages` and the
wheel targets, as established by #190.
**Subdomain classification**: Generic (development tooling).
**New domain terms**: manifest, taskpane, trusted catalog, sideload, AppDomain, Wef cache
(see Glossary).

## Architecture

Data flow, build through to pane:

```text
config/dev-endpoints.json ──read──▶ build_manifest.py ──substitutes __ADDIN_BASE_URL__──▶
   manifest.template.xml ──renders──▶ src/addin/catalog/manifest.xml
                                                  │
        developer registers src/addin/catalog/ as a Trusted Add-in Catalog (Word Trust Center)
                                                  │
   Word reads manifest ▶ SourceLocation = https://localhost:8767/taskpane.html
                                                  │
   addin.server (Flask, HTTPS, #190) serves taskpane.html ──▶ hello-world pane opens
```

The build computes the base URL as `f"{addin.scheme}://localhost:{addin.port}"` from the
`addin` surface in the config (`scheme=https`, `port=8767`), then replaces the
`__ADDIN_BASE_URL__` token everywhere it appears in the template (`SourceLocation` and
`AppDomain`). The host (`localhost`) is fixed in the build, not taken from the config `host`
field (which is `127.0.0.1`, used only by the launcher's health probe).

**Manifest template shape** (committed at `src/addin/manifest.template.xml`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<OfficeApp xmlns="http://schemas.microsoft.com/office/appforoffice/1.1"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:type="TaskPaneApp">
  <Id>954abf42-47ef-4a32-a705-933e1fb46c57</Id>
  <Version>1.0.0.0</Version>
  <ProviderName>Redmark Logic</ProviderName>
  <DefaultLocale>en-US</DefaultLocale>
  <DisplayName DefaultValue="Redline (dev)"/>
  <Description DefaultValue="Redline taskpane — local development build (issue #191)."/>
  <SupportUrl DefaultValue="https://www.redmarklogic.com/"/>
  <AppDomains>
    <AppDomain>__ADDIN_BASE_URL__</AppDomain>
  </AppDomains>
  <Hosts>
    <Host Name="Document"/>
  </Hosts>
  <Requirements>
    <Sets DefaultMinVersion="1.3">
      <Set Name="WordApi" MinVersion="1.3"/>
    </Sets>
  </Requirements>
  <DefaultSettings>
    <SourceLocation DefaultValue="__ADDIN_BASE_URL__/taskpane.html"/>
  </DefaultSettings>
  <Permissions>ReadWriteDocument</Permissions>
</OfficeApp>
```

`<Host Name="Document"/>` is how an add-in-only manifest names **Word** (the Word document
host). The template is itself well-formed XML, so it is committed as-is; only the rendered
output carries the live URL.

## Domain Models

None. The only "model" is the manifest XML structure shown above; there are no Python
domain classes, Pydantic models, or dataframes in this task.

## MoSCoW

| Category | Items |
| -------- | ----- |
| **Must have** | Committed manifest template (Word host, `SourceLocation` token, `WordApi` 1.3 Requirements per ADR-028, `ReadWriteDocument`); `build_manifest.py` rendering well-formed XML with the port from config and no leftover token; trusted-catalog sideload that opens the hello-world pane in desktop Word *[human-verify]*; sideload runbook including the Wef cache-clear step. |
| **Should have** | TDD unit tests for the build (well-formedness, URL-from-config, Word host, 1.3 floor, no token remains); fix the stale port (3000 → 8767) in `src/addin/README.md`; gitignore `src/addin/catalog/`. |
| **Could have** | Wire `python -m addin.build_manifest` into `tasks/run-app.ps1` so the manifest is regenerated at launch. |
| **Won't have (this time)** | Unified/JSON manifest; any Office.js in the pane; custom add-in icons (Word's default is used); authentication (#193); document scanning/replace (#196/#197); Microsoft 365 admin-center or centralized deployment; CI automation of the sideload; Fluent UI / visual design. |

## Phased Delivery

### Phase 0: Manifest build (headless, fully testable)

**Goal**: `python -m addin.build_manifest` produces a well-formed Word manifest at
`src/addin/catalog/manifest.xml` whose taskpane URL is derived from `config/dev-endpoints.json`.

**TDD approach**: Write `tests/addin/test_build_manifest.py` first, against a
`build_manifest_xml()` pure function that takes a config path and returns the rendered XML
string (so it is testable without touching the real filesystem layout). Tests assert:
well-formed XML (`ET.fromstring` does not raise); `SourceLocation` equals
`https://localhost:<port>/taskpane.html` with `<port>` read from the same config fixture
(proves no-drift); a Word host (`Host Name="Document"`) is present; the `WordApi` 1.3
Requirements set is present (ADR-028); and the string `__ADDIN_BASE_URL__` does not survive
in the output. Use the ElementTree namespace wildcard (`.//{*}SourceLocation`) because the
manifest declares a default XML namespace — searching by bare tag name returns nothing
otherwise (known gotcha).

**Deliverables**:

1. `src/addin/manifest.template.xml` — the committed template shown above.
2. `src/addin/build_manifest.py` — `build_manifest_xml(config_path, template_path)` pure
   function + a `main()` that writes the rendered file into `src/addin/catalog/` and prints
   the folder path to register.
3. `tests/addin/test_build_manifest.py` — the failing-first tests above.

**Verification**:

```powershell
.venv\Scripts\activate
python -m addin.build_manifest
python -c "import xml.etree.ElementTree as ET; ET.parse('src/addin/catalog/manifest.xml')"
python -m pytest tests/addin/test_build_manifest.py -v
```

Expect: the manifest file is written; `ET.parse` exits 0 (well-formed); all tests green.

**Acceptance Gate** (both must pass before Phase 1 starts):

- [ ] Working code: `python -m addin.build_manifest` writes a manifest and `ET.parse` confirms well-formed XML
- [ ] Function files introduced — run `.venv\Scripts\activate; python -m pytest tests/addin -v` and confirm green

---

### Phase 1: Trusted-catalog sideload (the proof — human-verified)

**Goal**: The hello-world taskpane opens inside desktop Word, loaded from the local Python
server via the trusted-catalog manifest, and the procedure is written down.

**TDD approach**: Not applicable — this phase is the Office user-interface side effect that
cannot be asserted by an automated test (the same boundary #190 drew for the trust-store and
browser padlock). It is human-verified and captured as a runbook.

**Deliverables**:

1. `specs/191-word-manifest-desktop-sideload-via-trusted-catalog/spike-notes.md` — the
   step-by-step runbook (spec FR-006 / Scenario 2): preconditions (run
   `python -m addin.make_cert` then `python -m addin.server`, or `tasks/run-app.ps1`, and
   confirm the browser padlock from #190); register `src/addin/catalog/` under **File →
   Options → Trust Center → Trust Center Settings → Trusted Add-in Catalogs**, tick *Show in
   Menu*, restart Word; open **Insert → My Add-ins → Shared Folder**, choose *Redline (dev)*,
   confirm the pane opens; the **cache-clear** recovery (close Word, delete the per-user Wef
   cache under `%LOCALAPPDATA%\Microsoft\Office\16.0\Wef\`, reopen); and the **UNC-share
   fallback** if a local folder path is refused.

**Verification**:

```powershell
.venv\Scripts\activate
# Preconditions (reuses #190):
python -m addin.make_cert
tasks\run-app.ps1            # or: $env:ADDIN_PORT=8767; python -m addin.server
curl -k -s -o NUL -w "%{http_code}" https://localhost:8767/taskpane.html   # expect 200
# Then, in desktop Word, follow spike-notes.md and confirm:
#   Insert -> My Add-ins -> Shared Folder lists "Redline (dev)" and opens the hello-world pane  [human-verify]
```

**Acceptance Gate** (both must pass before Phase 2 starts):

- [ ] Human-verified: the hello-world pane opens in desktop Word via Insert → My Add-ins → Shared Folder
- [ ] `spike-notes.md` exists and a second person can follow it end-to-end (spec SC-003)

---

### Phase 2: Polish

**Goal**: Remove the staleness the source reconciliation flagged and leave the harness clean.

**Deliverables**:

1. `src/addin/README.md` — correct the documented listening port from `3000` to `8767`
   (the committed source of truth) and add a one-line pointer to the manifest/sideload.
2. `.gitignore` — add `src/addin/catalog/` (rendered manifest is a generated artifact).
3. (Could) `tasks/run-app.ps1` — invoke `python -m addin.build_manifest` before starting the
   servers so the catalog manifest is always current.

**Verification**:

```powershell
.venv\Scripts\activate
python -m pytest tests/addin -v
python -m ruff check src/addin tests/addin
```

**Acceptance Gate**:

- [ ] All `tests/addin` green and ruff clean
- [ ] README no longer cites port 3000; `git status` shows `src/addin/catalog/` untracked/ignored

## File Inventory

| Phase | New Files | Count |
| ----- | --------- | ----- |
| 0     | `src/addin/manifest.template.xml`, `src/addin/build_manifest.py`, `tests/addin/test_build_manifest.py` | 3 |
| 1     | `specs/191-.../spike-notes.md` | 1 |
| 2     | — (modifications only) | 0 |

**Modified**: `src/addin/README.md`, `.gitignore`, (Could) `tasks/run-app.ps1`.
**Total new**: ~4 | **Total deleted**: 0

## Library Best Practices

No new third-party library is introduced, so there is no Context7 version review to run. The
relevant external contract is Microsoft's **add-in-only manifest schema**, which is stable.

### xml.etree.ElementTree (standard library, test-only)

- **Import path**: `import xml.etree.ElementTree as ET`
- **API gotcha**: the manifest declares a default namespace
  (`xmlns="http://schemas.microsoft.com/office/appforoffice/1.1"`), so every element tag is
  namespaced. Searching with a bare name (`root.find("SourceLocation")`) returns `None`. Use
  the wildcard form `root.find(".//{*}SourceLocation")` (Python 3.8+) or an explicit
  namespace map.
- **Confirmed pattern**: `ET.fromstring(xml_string)` to validate well-formedness in tests;
  `ET.parse(path)` in the command-line acceptance check (matches the issue's verify command).

### Office add-in-only manifest (Microsoft schema, not a Python library)

- **Word host**: `<Hosts><Host Name="Document"/></Hosts>` — `Document` is Word.
- **Requirements**: per ADR-028 D1, `WordApi` `MinVersion="1.3"`; a host below the floor is
  silently not offered the add-in.
- **HTTPS only**: `SourceLocation` and `AppDomains` must be HTTPS — satisfied by the #190
  locally-trusted certificate.

## Risk Register

| Risk | Mitigation |
| ---- | ---------- |
| Word refuses a **local folder** as a trusted catalog (older builds expect a network share) | Runbook documents the UNC-share fallback: share `src/addin/catalog/`, register `\\<machine>\<share>` instead of the local path |
| **Manifest caching** — edits or re-adds do not appear | Runbook's cache-clear step: close Word, delete `%LOCALAPPDATA%\Microsoft\Office\16.0\Wef\` (`16.0` is the current Office major-version folder — adjust if yours differs), reopen; always restart Word after Trust Center changes |
| **ElementTree namespace** trips the tests (bare-tag finds return `None`) | Use `{*}` wildcard searches; called out in the TDD approach and Library Best Practices |
| Dev's Word is **below WordApi 1.3** → add-in silently not offered | Sideload on Microsoft 365 / Word 2019+ (ADR-028 floor); recorded in spec assumptions |
| **Certificate not trusted / server down** → blank pane mistaken for a manifest fault | Runbook preconditions run `make_cert` + server and reuse the #190 padlock check before opening Word |
| Build reads config but **ADR-021** forbids app source reading config | `build_manifest.py` is build-time tooling in the Generic dev package (like the launcher), explicitly blessed by the config `_comment`; documented in D4 |

## Glossary

| Term | Definition |
| ---- | ---------- |
| Manifest | The XML file that tells Word an add-in's identity, the web address of its taskpane, and its permissions. |
| Taskpane | The side panel inside Word that hosts the add-in's web page. |
| Trusted catalog | A folder registered in Word's Trust Center that Word is permitted to load sideloaded add-ins from. |
| Sideload | Installing an add-in for local development without any centralized/admin deployment. |
| AppDomain | A manifest entry listing the web origins the add-in is allowed to navigate to. |
| Wef cache | The per-user folder (`%LOCALAPPDATA%\Microsoft\Office\16.0\Wef\` on current Office) where Word caches sideloaded manifests; must be cleared when a change does not take effect. |
