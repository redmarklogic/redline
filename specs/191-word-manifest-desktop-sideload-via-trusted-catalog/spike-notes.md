# Spike notes — sideloading the Redline taskpane into desktop Word (issue #191)

**Status:** runbook ready; the in-Word steps (§3–§4) and the final verification (§6)
are **human-verified** and must be performed on a machine with desktop Microsoft Word
(Microsoft 365 or Word 2019+, the ADR-028 floor). This file is the spec **FR-006**
deliverable and the seed for the reusable skill writeup (issue #198).

This runbook is written to be reproducible by a second person end-to-end (spec SC-003).
Everything outside Word (§1–§2) has been executed and is automatable; the Office
user-interface steps cannot be asserted by a test (the same boundary #190 drew for the
trust-store install and the browser padlock), so they are recorded here as steps.

---

## What you are doing

Loading a locally-built Word add-in **manifest** (an XML instruction sheet) into desktop
Word, by pointing Word at a folder on your machine — a **trusted catalog** — instead of
any Microsoft 365 admin deployment. Word reads the manifest, sees the taskpane address
(`https://localhost:8767/taskpane.html`), and opens the hello-world page the #190 Flask
server serves in a side panel.

```text
config/dev-endpoints.json ─▶ python -m addin.build_manifest ─▶ src/addin/catalog/manifest.xml
                                                                        │
            register src/addin/catalog/ as a Trusted Add-in Catalog (Word Trust Center)
                                                                        │
   Word reads manifest ─▶ SourceLocation = https://localhost:8767/taskpane.html
                                                                        │
   addin.server (Flask HTTPS, #190) serves taskpane.html ─▶ hello-world pane opens
```

---

## 1. Preconditions — certificate + server (reuses #190)

Run from the repository root with the project virtual environment active.

```powershell
.venv\Scripts\activate

# 1a. Generate and trust the local HTTPS certificate (one-time; idempotent).
#     Installs the dev CA into the CurrentUser Root store. If the write is denied
#     on a managed machine, re-run from an elevated (Administrator) PowerShell.
python -m addin.make_cert

# 1b. Build the manifest into the catalog folder (also done automatically by
#     tasks\run-app.ps1). Note the printed catalog folder path — you register it in §3.
python -m addin.build_manifest

# 1c. Start the addin server on the canonical port (8767, from config).
#     Either run the full launcher:
tasks\run-app.ps1
#     ...or just the addin server on its own:
$env:ADDIN_PORT='8767'; python -m addin.server
```

**Verify the server before opening Word** (a blank pane is usually a dead server or an
untrusted cert, not a manifest fault):

```powershell
curl -k -s -o NUL -w "%{http_code}" https://localhost:8767/taskpane.html   # expect: 200
```

Then open `https://localhost:8767/taskpane.html` in a desktop browser and confirm the
padlock shows with **no** "your connection is not private" warning (the #190 Scenario 2
check). If it warns, the cert is not trusted — re-run §1a, restart the browser.

---

## 2. The catalog folder

`python -m addin.build_manifest` writes the rendered manifest to:

```text
src\addin\catalog\manifest.xml
```

and prints the absolute folder path to register. The folder is gitignored (the manifest
is a generated artifact, mirroring `src/addin/certs/`). Confirm the file exists and is
well-formed:

```powershell
python -c "import xml.etree.ElementTree as ET; ET.parse('src/addin/catalog/manifest.xml'); print('OK')"
```

---

## 3. Register the catalog in Word's Trust Center  *[human]*

1. Open desktop **Word**.
2. **File → Options → Trust Center → Trust Center Settings… → Trusted Add-in Catalogs**.
3. In **Catalog Url**, paste the **absolute path to the catalog folder** printed in §1b
   (the absolute form of `<repo-root>\src\addin\catalog`), then click **Add catalog**.
4. Tick **Show in Menu** for that row.
5. Click **OK** out of both dialogs.
6. **Restart Word completely** (close all Word windows). Trust Center changes are not
   picked up until a restart.

> **If Word rejects a local folder path** (some builds expect a network share): share
> the `src\addin\catalog` folder in Windows (right-click → Properties → Sharing), then
> register the **UNC path** (`\\<machine-name>\<share-name>`) in step 3 instead of the
> local path. The manifest content is identical.

---

## 4. Open the taskpane  *[human-verify]*

1. In Word, open or create a blank document.
2. **Insert → My Add-ins → (Shared Folder tab)**.
3. Select **Redline (dev)** and click **Add**.
4. Confirm the hello-world taskpane opens in the side panel.

This opening of the pane is the **acceptance gate (T012 / spec SC-003)** and the sprint
go/no-go tripwire.

---

## 5. Recovery — clearing Word's manifest cache

Word caches sideloaded manifests aggressively; an edit, a re-add, or a stale page often
will not appear until the cache is cleared.

1. **Close Word completely.**
2. Delete the per-user Wef cache folder `%LOCALAPPDATA%\Microsoft\Office\16.0\Wef\`.
   `16.0` is the current Office major-version folder — adjust if your build differs (check
   `%LOCALAPPDATA%\Microsoft\Office\` for the version folder present).
3. Reopen Word and retry from §4.

Always restart Word after any Trust Center change (§3) before assuming the add-in is
broken.

---

## 6. Acceptance checklist (spec SC-003 / tasks T012)

- [ ] §1 server returns `200` and the browser padlock shows no warning.
- [ ] §2 `src/addin/catalog/manifest.xml` exists and is well-formed XML.
- [ ] §3 catalog folder registered, **Show in Menu** ticked, Word restarted.  *[human]*
- [ ] §4 **Redline (dev)** appears under Insert → My Add-ins → Shared Folder and the
      hello-world pane opens.  *[human-verify]*
- [ ] A second person can follow §1–§5 end-to-end without further explanation.

---

## Notes for the #198 skill writeup

- The only value that varies between machines is the **catalog folder path** (and the
  `16.0` Office-version folder in §5). Everything else is fixed in the committed template.
- The taskpane port (`8767`) is derived from `config/dev-endpoints.json` by the build, so
  it can never drift from the server — do not hard-code it anywhere.
- The two most common failures are (a) server down / cert untrusted → blank pane, caught
  by the §1 verify; and (b) stale Wef cache → old or missing add-in, fixed by §5.
- The UNC-share fallback (§3) is the documented workaround for builds that refuse a local
  folder as a trusted catalog.
