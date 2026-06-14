# `addin` — Word taskpane served over locally-trusted HTTPS (issue #190)

A throwaway **development harness**: a tiny Python web server that serves a single
hello-world page (the future Microsoft Word *taskpane*) over HTTPS on `localhost`, plus a
Python script that generates and trusts the local HTTPS certificate. The point is to prove
the page can be served entirely from Python with **no Node.js toolchain** anywhere in this
folder. Sideloading into Word is a separate issue (#191) and is out of scope here.

This is a **Generic** dev-only package: it is not added to the import-linter contracts and
is not shipped in the product wheel.

## Source: the Masterjx9 template

Adapted from the open-source **Masterjx9 Outlook-Addin-TaskPane-python** template:

- Source: <https://github.com/Masterjx9/Outlook-Addin-TaskPane-python>
- The template serves add-in files from a small Flask server (`app.py`) and ships a Python
  re-implementation of Microsoft's `office-addin-dev-certs` helper under `devcerts/`.

### What we reuse

| Template file | What we take | Where it lands here |
| ------------- | ------------ | ------------------- |
| `app.py` | The Flask `static_folder` + `app.run(ssl_context=...)` serving pattern | `src/addin/server.py` |
| `devcerts/generate.py` | The `cryptography` self-signed CA + `localhost` leaf cert (SAN `localhost`) | `src/addin/make_cert.py` |
| `devcerts/install.py` + `scripts/install.ps1` | The Windows trust-store install mechanism (see below) | `src/addin/make_cert.py` |

### What we deliberately do **not** copy

- The Outlook manifest (`manifest_python.xml`) and Outlook-specific assets — the Word
  manifest is #191's job.
- The template's multi-route serving (`index`, `commands`, icons) — this slice serves only
  `/taskpane.html`.
- `datetime.utcnow()` (deprecated, raises under our `filterwarnings=error`) — we use
  timezone-aware `datetime.now(UTC)`.
- The template's cert location `~/.office-addin-dev-certs/` and `localhost.crt`/`.key`
  names — this slice writes `cert.pem`/`key.pem` into `src/addin/certs/` (gitignored).

## Confirmed certificate library

**`cryptography`** (template pins `44.0.0`; this repo resolves `>=44`, installed `49.0.0`).
Entry points used: `cryptography.x509.CertificateBuilder`, `rsa.generate_private_key`,
`x509.SubjectAlternativeName([x509.DNSName("localhost")])`, PEM serialization.

## Trust-store mechanism (T002a)

On **Windows**, the template installs the generated CA certificate into the
**CurrentUser `Root`** store via PowerShell:

```powershell
Import-Certificate -CertStoreLocation cert:\CurrentUser\Root <ca.crt>
```

with a legacy fallback using `System.Security.Cryptography.X509Certificates.X509Store("Root", "CurrentUser")`.

> The CurrentUser Root store does **not** require an elevated/administrator shell on a
> standard Windows profile, but on hardened/managed machines the write can still be denied —
> in which case `make_cert.py` prints an actionable "re-run from an administrator shell"
> message. This is the step Scenario 2 (no browser warning) hinges on.

## Reproducing both acceptance scenarios

Run from the repository root with the project virtual environment active. The
`addin` package resolves because `src/` is on the Python path (the repo's
`.pth` entry); no install step is needed. The Flask and `cryptography`
dependencies come from the `addin` dependency group (in `default-groups`, so
`uv sync` installs them).

**Listening port: `8767`** — the `addin` surface in `config/dev-endpoints.json`, the
committed single source of truth. The launcher (`tasks/run-app.ps1`) projects it into
`ADDIN_PORT`, and the #191 manifest build derives the same value, so the manifest
address can never drift from what the server binds. Running `python -m addin.server`
on its own falls back to the `ADDIN_PORT` env var (and a `3000` default if unset), so
set `$env:ADDIN_PORT='8767'` — or just use `tasks/run-app.ps1` — to match the manifest.

> **Manifest & sideload (issue #191):** `python -m addin.build_manifest` renders
> `manifest.template.xml` into `src/addin/catalog/manifest.xml`, taking the port from
> `config/dev-endpoints.json`. To load it into desktop Word via a trusted catalog,
> follow `specs/191-word-manifest-desktop-sideload-via-trusted-catalog/spike-notes.md`.

### Command 1 — generate and trust the certificate (Scenario 2)

```powershell
python -m addin.make_cert
```

Generates `certs/cert.pem` (the `localhost` leaf certificate Flask serves),
`certs/key.pem` (its private key) and `certs/ca.pem` (the signing CA), then
installs the CA into the Windows **CurrentUser `Root`** trust store via
`Import-Certificate`. If the trust-store write is denied (a hardened/managed
machine), the command prints an actionable message — **re-run it from an elevated
(Administrator) PowerShell.** The `certs/` directory is gitignored.

> Installing a certificate authority into your trust store is a security-relevant
> action; run this command yourself and only on a development machine.

### Command 2 — start the HTTPS server (Scenario 1)

```powershell
$env:ADDIN_PORT='8767'; python -m addin.server
```

Serves `https://localhost:8767/taskpane.html`. Run Command 1 first — the server
exits with a clear message if `certs/cert.pem` / `certs/key.pem` are missing.

### Verify

```powershell
# Scenario 1 — serving (certificate validation skipped with -k):
curl -k -s -o NUL -w "%{http_code}" https://localhost:8767/taskpane.html   # expect: 200
curl -k -s https://localhost:8767/taskpane.html | findstr /i "hello"        # expect: hello-world text

# Scenario 2 — trust [human-verify]:
# Open https://localhost:8767/taskpane.html in a desktop browser and confirm
# the padlock shows with NO "your connection is not private" warning.
```

## Unit tests

```powershell
python -m pytest tests/addin -v
```

The tests cover routing/body (`test_server.py`) and certificate
generation/SAN/validity (`test_make_cert.py`). The OS trust-store install and the
browser padlock are side effects that cannot be asserted portably — they are
human-verified, not unit-tested.
