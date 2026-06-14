# Feature Specification: Python-served Word taskpane over locally-trusted HTTPS

**Branch**: `feature/190-adapt-masterjx9-flask-taskpane-template-with-https-dev-certs`
**Created**: 2026-06-14
**Status**: Draft

## Context (plain-English summary)

Microsoft Word add-ins are small web applications that load inside a panel — the
"taskpane" — docked next to the open document. Word does not render that panel from
files on disk; it loads the panel from a web address, and Microsoft requires that
address to use HTTPS (the encrypted form of web traffic) even when everything runs on
the developer's own machine. The usual way to build such an add-in relies on the
Node.js JavaScript toolchain (the `npm` package manager, the `webpack` bundler, and
Microsoft's `office-addin-dev-certs` helper that creates and trusts the local HTTPS
certificate). This project has a standing rule to avoid introducing a second language
toolchain alongside Python.

This feature removes the Node.js dependency for the *serving* half of the problem. It
adapts an existing open-source template — the **Masterjx9 Outlook-Addin-TaskPane**
project — which has already done the hard part: it serves an add-in's web files from a
small Python web server and includes a Python re-implementation of Microsoft's
certificate helper, so the mandatory local HTTPS certificate can be generated and
trusted entirely from Python. The deliverable here is narrow: a Python process that,
when started, serves a hello-world taskpane page over HTTPS at `localhost`, backed by a
certificate the local machine trusts, with no Node.js artifacts anywhere in the add-in
folder.

This is one slice of a larger, time-boxed proof of concept (parent issue #189). The
companion work — writing the Word add-in manifest and sideloading the add-in into
desktop Word — is explicitly out of scope here and is handled in issue #191. This slice
proves only that Python can serve the page over trusted HTTPS.

## Why this matters (the bet behind it)

The Sprint 4 goal is a working end-to-end demonstration of the paid product surface: a
Word taskpane with a "Check document" button that scans the document for forbidden
terms and marks them inline. That whole surface depends on being able to serve the
taskpane from the project's Python stack without adopting Node.js. Parent issue #189
carries a hard tripwire — "if by Wednesday we have not seen a working Microsoft
taskpane, we will stop." This feature is the first, foundational step toward clearing
that tripwire: before the page can be sideloaded into Word (#191), Python must be able
to serve it over trusted HTTPS at all. If this step fails, the whole no-Node.js
approach is in doubt.

## Scenarios (mandatory)

Scenarios are ordered by RICE score (Reach × Impact × Confidence ÷ Effort), highest
first. "Reach" is expressed as the number of developers who exercise the path per
proof-of-concept run; this is internal tooling, so reach is small by nature and Impact
and Confidence carry the ranking.

### Scenario 1 -- Serve the hello-world taskpane page over HTTPS

A developer starts the Python server on their machine. They issue an HTTP request to
the taskpane page at `https://localhost:<port>/taskpane.html`, deliberately ignoring
certificate validation for this raw check. The server responds successfully and returns
the hello-world page content.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 1     | 3              | 90             | 0.5                  | 5.4        |

**Independent test**: Start the server, then run
`curl -k -s -o /dev/null -w "%{http_code}" https://localhost:<port>/taskpane.html` and
confirm it prints `200`. A second `curl` without `-o /dev/null` confirms the body is the
expected hello-world HyperText Markup Language (HTML). No Word, no manifest, and no
certificate trust are required for this test — the `-k` flag tells `curl` to skip
certificate validation, isolating the serving behaviour from the trust behaviour in
Scenario 2.

**Acceptance criteria**:

1. **Given** the Python server is running, **When** a client requests
   `https://localhost:<port>/taskpane.html` (certificate validation skipped), **Then**
   the server returns HyperText Transfer Protocol (HTTP) status `200` with the
   hello-world HTML as the body.
2. **Given** the served HTML, **When** it is inspected, **Then** it contains
   human-readable hello-world content only — no document-scanning logic, no API calls,
   and no application behaviour (those arrive in later issues).

---

### Scenario 2 -- Open the page in a browser with no certificate warning

A developer generates the local development certificate using the template's Python
certificate script and lets it install into the operating system's trust store. They
then open `https://localhost:<port>/taskpane.html` in a desktop browser. The browser
loads the page directly, showing the secure padlock, with no "your connection is not
private" interstitial blocking the page.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 1     | 3              | 65             | 0.5                  | 3.9        |

**Independent test**: After running the certificate-generation script, open the page
URL in a browser and visually confirm there is no certificate warning and the padlock is
present. Confidence is lower than Scenario 1 because trusting a certificate in the
Windows certificate store can require an elevated (administrator) shell and the exact
behaviour depends on the host machine's configuration. This step is marked
`[human-verify: browser padlock]` — it is confirmed by a person looking at the browser,
not by an automated assertion.

**Acceptance criteria**:

1. **Given** the certificate-generation script has been run and reported success,
   **When** the certificate's presence in the trust store is checked, **Then** a
   certificate for `localhost` is found and marked trusted.
2. **Given** the certificate is trusted, **When** the page URL is opened in a desktop
   browser, **Then** the page renders with no certificate warning blocking it
   `[human-verify: browser padlock]`.

---

### Edge Cases

- What happens when the chosen port is already in use by another process? The server
  must fail loudly with a clear message rather than appear to start and then be
  unreachable.
- What happens when the certificate-generation script is run without administrator
  privileges and the trust-store write is denied? The failure must be visible and
  actionable (a clear instruction to re-run from an elevated shell), not a silent
  partial success that later surfaces as a browser warning.
- What happens when a certificate from a previous run already exists? Re-running the
  script must not leave the machine in a broken state (for example, two conflicting
  `localhost` certificates).
- What happens when the developer requests a path other than `taskpane.html`? Out of
  scope for this slice, but the server must not crash; a plain 404 is acceptable.

## Requirements (mandatory)

### Functional Requirements

- **FR-001**: A Python process MUST serve a static hello-world taskpane page at the
  path `/taskpane.html`.
- **FR-002**: The server MUST serve that page over HTTPS (Transport Layer Security), not
  plain HTTP, because Microsoft Word add-ins require an HTTPS source even on `localhost`.
- **FR-003**: The system MUST generate a local development certificate for `localhost`
  using a Python script (the template's port of `office-addin-dev-certs`) and MUST be
  able to install that certificate into the host machine's trust store, with no Node.js
  tooling involved.
- **FR-004**: The add-in folder MUST contain no Node.js artifacts — specifically no
  `package.json` file and no `node_modules` directory — verifiable with `git ls-files`.
- **FR-005**: The served page MUST contain hello-world content only; it MUST NOT include
  document-scanning logic, outbound API calls, or authentication code (those belong to
  later issues #193, #196, #197).
- **FR-006**: The listening port MUST be a single, documented value so that the
  acceptance `curl` command and the sideload manifest (#191) can target it
  unambiguously.
- **FR-007**: Starting the server and generating the certificate MUST each be a single
  documented command, so a reviewer can reproduce both acceptance scenarios from the
  repository without prior knowledge of the template's internals.

### Key Entities

- **Taskpane page**: the static HTML document served at `/taskpane.html`. For this slice
  it holds hello-world content only. It is the artifact Word will later load (#191).
- **Development certificate**: the self-signed certificate (and its private key) for
  `localhost`, generated by the Python script and installed into the host trust store so
  browsers and Word accept the HTTPS connection without warning.
- **Taskpane server**: the Python process that binds the documented port, terminates
  HTTPS using the development certificate, and serves the taskpane page and any static
  assets it references.

## Success Criteria (mandatory)

- **SC-001**: `curl -k -s -o /dev/null -w "%{http_code}"
  https://localhost:<port>/taskpane.html` prints `200` against the running server.
- **SC-002**: The served body is the hello-world HTML (non-empty, human-readable, no
  application logic).
- **SC-003**: After running the certificate script, the taskpane URL opens in a desktop
  browser with no certificate warning blocking the page `[human-verify: browser
  padlock]`.
- **SC-004**: `git ls-files` over the add-in path returns no `package.json` and no
  `node_modules` entries.
- **SC-005**: A reviewer can reproduce both acceptance scenarios using only the two
  documented commands (generate certificate; start server) and the documented port —
  no undocumented manual steps.

## Assumptions

- **Web framework — keep the template's Flask server for this slice.** Issue #190 offers
  "keep Flask or port the few routes to FastAPI ... decide on contact, do not research."
  The Masterjx9 template ships on Flask (a lightweight Python web framework), and this
  slice serves two static routes. Keeping Flask is the lowest-effort path to the
  acceptance criteria and adds no value-at-risk to the spike, so it is the assumed
  choice. This is a *local development harness for the proof of concept*, not the
  deployed production server, so it does not conflict with the project's ratified
  Django web stack (issue #78) — production serving and deployment are explicitly
  deferred to a later sprint. If this assumption is wrong (the team wants the spike
  itself to validate the eventual production framework), the serving routes would be
  re-pointed to FastAPI or Django, changing effort but not the acceptance criteria.
  **This is the one decision flagged for founder confirmation before planning.**
- **Single localhost port, chosen once and documented.** The exact number does not
  affect the outcome as long as it is fixed and recorded so #191's manifest can match it.
- **Windows is the target development operating system.** The project runs on Windows 11;
  certificate trust uses the Windows certificate store and may require an elevated
  (administrator) shell, as parent #189 notes.
- **The template's certificate port is functionally equivalent to
  `office-addin-dev-certs`.** Parent #189 states the Masterjx9 project already solved
  this; this slice adapts it rather than re-researching certificate generation.
- **Only the template's serving and certificate layers are reused.** The template targets
  Outlook; its Outlook manifest and any Outlook-specific code are ignored here (the Word
  manifest is #191's job).

## Risks

| Risk                                                                 | Impact                                                                                          | Mitigation                                                                                                  |
| -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Windows certificate-store trust fails without an elevated shell      | Scenario 2 cannot be confirmed; browser shows a certificate warning and Word may later refuse the page | Run the certificate script from an administrator shell; document the requirement; confirm trust before declaring done |
| Framework choice (Flask vs FastAPI vs Django) is reopened later      | Rework if the spike's server must become the production server                                  | Treat this slice as a throwaway dev harness; record the Flask decision and its reversibility; confirm with founder before planning |
| Chosen port collides with another local process                      | Server appears to start but is unreachable; wastes debugging time on the tripwire-critical path | Pick an uncommon port, document it, and surface bind failures loudly                                        |
| Hidden Node.js dependency inside the template (a stray `package.json`) | Violates the no-Node.js premise that is the whole reason for the spike                          | Audit the adapted folder with `git ls-files`; FR-004 makes this an explicit acceptance gate                |
| Template's certificate port diverges from current `office-addin-dev-certs` behaviour on a modern Windows build | Certificate generated but not trusted; silent Scenario 2 failure                                | Verify trust empirically in a browser (human-verify), not by assuming the script succeeded                 |
