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

## Run commands and port

<!-- Completed in Phase 3. -->

- **Listening port**: `3000` (the Office add-in convention; see plan D6).
- Generate + trust the certificate: _(documented in Phase 3)_
- Start the server: _(documented in Phase 3)_
