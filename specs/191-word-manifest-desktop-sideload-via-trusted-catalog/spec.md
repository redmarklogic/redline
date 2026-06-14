# Feature Specification: Word manifest + desktop sideload via trusted catalog

**Branch**: `feature/191-word-manifest-desktop-sideload-via-trusted-catalog`
**Created**: 2026-06-14
**Status**: Draft
**Source**: GitHub issue [#191](https://github.com/redmarklogic/redline/issues/191) (Work Breakdown Structure item 2.2 of parent [#189](https://github.com/redmarklogic/redline/issues/189); see `docs/product/tasks/sprint-4-goal.md`)

## Overview

Microsoft Word can be extended with *add-ins*: small web applications that appear in
a side panel — the *taskpane* — inside the Word window. Word does not run the add-in's
code directly. Instead it reads a *manifest*, an Extensible Markup Language (XML) file
that tells Word the add-in's name, the web address that serves its user interface, and
the permissions it needs. Word then loads the web page named in the manifest into the
taskpane.

The previous task (issue #190, now merged) produced a small Python web server that
serves a placeholder "hello-world" taskpane page over a locally-trusted, encrypted
(HyperText Transfer Protocol Secure, HTTPS) connection on the developer's own machine.
What is still missing is the manifest that points Microsoft Word at that page, and a
dependable way to load that manifest into a copy of Word running on a Windows desktop so
a developer can actually see the panel open. This task closes that gap.

The chosen loading method is *sideloading via a trusted catalog*. "Sideloading" means
installing the add-in for local development without publishing it through any company-wide
deployment system or the Microsoft 365 administration centre. The "trusted catalog" is an
ordinary folder on the developer's machine that has been registered inside Word's Trust
Center as a location Word is permitted to read add-ins from. Once the folder is registered
and Word is restarted, the add-in appears under **Insert → My Add-ins → Shared Folder**,
and opening it should display the hello-world panel.

This is the single riskiest step in the Sprint 4 proof of concept and the sprint's
go/no-go *tripwire*: the founder's stop-rule is, verbatim, "If by Wednesday we have not
seen a working Microsoft taskpane, we will stop." It is risky for a specific reason: the
team's existing research notes only cover sideloading into *Outlook on the web*. The
desktop-Word path is an explicit, acknowledged knowledge gap, and this task is what
closes it. Word is also known to cache manifests aggressively, which can make edits look
as though they had no effect — a common source of wasted time that the written procedure
must address.

## Scenarios (mandatory)

<!-- RICE = Reach x Impact x Confidence / Effort. Scenarios are listed in execution
     order rather than strict RICE rank: Scenario 1 is the load-bearing proof and must
     succeed before Scenario 2 has any value, so leading with it reflects true priority
     even though its larger effort lowers its RICE number. -->

### Scenario 1 — A developer opens the Python-served taskpane inside desktop Word

A developer has the issue #190 server running locally and its development certificate
trusted. They register the trusted catalog folder in Word's Trust Center, restart Word,
open **Insert → My Add-ins → Shared Folder**, and select the Redline add-in. The
hello-world taskpane opens in the side panel, served over HTTPS from the local Python
server. This is the proof the whole sprint's critical path depends on.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 3     | 3              | 65             | 1.5                  | 3.9        |

**Independent test**: With the server running and the catalog trusted, opening the add-in
from Word's Shared Folder list displays the hello-world pane. Verified by a human at the
Word user interface (cannot be asserted by an automated test).

**Acceptance criteria**:

1. **Given** the manifest file, **When** it is parsed as XML, **Then** it is well-formed
   — verifiable with `python -c "import xml.etree.ElementTree as ET; ET.parse('<manifest path>')"`.
2. **Given** the manifest, **When** its taskpane address is read, **Then** it matches the
   address the local server actually serves (`https://localhost:8767/taskpane.html` — the
   loopback host the #190 server binds, with the port taken from `config/dev-endpoints.json`),
   with no hand-edited value that can drift from the server.
3. **Given** the catalog folder registered in Word's Trust Center and Word restarted,
   **When** the developer opens Insert → My Add-ins → Shared Folder, **Then** the add-in
   is listed and, when opened, displays the hello-world taskpane. *[human-verify]*

---

### Scenario 2 — A second person reproduces the sideload from a written runbook

A developer who did not perform the original sideload follows a written, step-by-step note
and reaches the same result: the taskpane open in desktop Word. The note covers
registering the catalog, clearing Word's manifest cache when a change does not appear, and
confirming the pane opened. This runbook is a required input to the taskpane skill writeup
(issue #198) and the foundation that the edit-to-refresh check (#192) and the
auth-compatibility check (#193) build on.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 3     | 1.5            | 90             | 0.25                 | 16.2       |

**Independent test**: A spike-notes file exists in the feature directory containing the
ordered sideload steps; a second person can follow it end-to-end without verbal help.

**Acceptance criteria**:

1. **Given** the sideload has been performed, **When** the steps are written down, **Then**
   a step-by-step note exists in the spike notes covering catalog registration, the Word
   manifest-cache clear, and pane verification — sufficient for the #198 skill writeup.

---

### Edge Cases

- **Word caches the manifest.** Word stores a copy of sideloaded manifests under the
  per-user *Wef* cache folder in `%LOCALAPPDATA%`. After editing or re-adding the add-in,
  the change may not appear until the cache is cleared and Word restarted. The runbook must
  state how to clear it.
- **Development certificate not trusted.** If the issue #190 certificate authority was
  never installed (the `python -m addin.make_cert` step), Word loads a blank or errored
  pane because the HTTPS connection is rejected. This is a precondition, not a defect of
  this task.
- **Server not running / wrong port.** If the Python server is not running, or is bound to
  a different port than the manifest names, the pane shows a connection error. The single
  source of truth for the address (`config/dev-endpoints.json`) exists precisely to prevent
  the port half of this mismatch.
- **Host form (`localhost` vs `127.0.0.1`).** The #190 certificate is valid for both forms.
  The manifest uses `localhost` because that is what the #190 server binds, what the issue's
  solution outline specifies, and the form Office tooling conventionally expects; `127.0.0.1`
  (the value in the dev-endpoints `host` field, used by the launcher's health probe) remains
  a certificate-covered fallback if Word objects.
- **Managed or hardened machine.** Group policy on a managed Windows device can block
  trusted catalogs or trust-store writes, in which case sideloading fails through no fault
  of the manifest. This proof targets an ordinary developer machine.
- **Word below the declared API floor.** The manifest requires `WordApi` 1.3 (FR-009,
  ADR-028); a Word host below that floor (for example Word 2016 perpetual) is silently not
  offered the add-in at all. The proof must run on Microsoft 365 or Word 2019+.

## Requirements (mandatory)

### Functional Requirements

- **FR-001**: A Microsoft Word add-in manifest MUST exist and MUST be well-formed XML when
  parsed.
- **FR-002**: The manifest MUST direct Word to load the taskpane from the address the local
  development server actually serves (`https://localhost:8767/taskpane.html`). The variable
  part of that address — scheme, port, and path — MUST originate from the single shared
  source of truth (`config/dev-endpoints.json`, `addin` surface) so it cannot drift from the
  server; the host is the loopback name the #190 server binds (`localhost`). Rationale: the
  launcher already reads this file, and a hand-typed port in the manifest would silently
  break whenever the configured port changes.
- **FR-003**: The manifest MUST declare Microsoft Word as the host application and MUST open
  the page as a taskpane (not a content or dialog surface).
- **FR-004**: The add-in MUST be loadable into desktop Word on Windows by the trusted
  shared-folder catalog method (registered in Word's Trust Center). It MUST NOT require the
  Microsoft 365 administration centre or any centralized/company-wide deployment.
- **FR-005**: With the catalog trusted and Word restarted, the add-in MUST appear under
  Insert → My Add-ins → Shared Folder and, when opened, MUST display the hello-world
  taskpane. *[human-verify]*
- **FR-006**: A step-by-step sideload runbook MUST be written to the spike notes, covering
  catalog registration, clearing Word's manifest cache, and verifying the pane — detailed
  enough to seed the issue #198 skill writeup and to be repeated by another person.
- **FR-007**: The taskpane MUST be loaded over HTTPS using the locally-trusted certificate
  produced in issue #190; the manifest MUST NOT introduce an insecure (HTTP) address.
- **FR-008**: The work MUST NOT introduce any Node.js toolchain or other second-language
  build tooling, consistent with the project's all-Python constraint and the #190 package's
  Generic, dev-only status.
- **FR-009**: The manifest MUST declare the project's Word application programming interface
  (API) minimum-version floor exactly as mandated by ADR-028 decision D1 — a `Requirements`
  block requiring `WordApi` minimum version `1.3`. ADR-028 explicitly designates this
  manifest as where that block lands, and Constitution Principle XIX makes the floor a binding
  commitment. (The hello-world pane itself makes no Office.js calls yet; the floor is declared
  now so the add-in's host requirement is honest and stable for the scanning and replace work
  in #197.)

### Key Entities

- **Add-in manifest**: the XML file describing the add-in to Word — a unique identifier, the
  display name, the host (Word), the taskpane source address, and the required permissions
  and capabilities.
- **Trusted catalog**: a folder on the developer's machine, registered in Word's Trust
  Center, from which Word is permitted to load sideloaded add-ins.
- **Dev-endpoints configuration** (`config/dev-endpoints.json`): the committed, non-secret
  single source of truth for every local surface's port, scheme, and path; the manifest
  derives its scheme, port, and path from the `addin` entry (host = `localhost`).
- **Sideload runbook**: the spike-notes document recording the exact, repeatable steps to
  register the catalog, clear the manifest cache, and open the pane.

## Success Criteria (mandatory)

- **SC-001**: A developer can make the hello-world taskpane open in desktop Word by
  following the runbook from a standing start (server running, certificate trusted) in under
  10 minutes.
- **SC-002**: Changing the add-in port in one place (the dev-endpoints configuration) updates
  both the running server and the manifest's address, with no manual edit to the manifest —
  i.e. zero opportunities for the address to drift.
- **SC-003**: A second person reproduces the sideload to an open pane using only the written
  runbook, with no verbal assistance.
- **SC-004**: A working Microsoft Word taskpane is demonstrably sideloaded on or before the
  Wednesday (Jun 24) tripwire checkpoint, satisfying the sprint stop-rule.

## Assumptions

- **Manifest format: the add-in-only XML manifest, not the newer unified manifest.** The
  XML add-in manifest is the established, best-supported route for sideloading into desktop
  Word through a trusted catalog; the unified (JavaScript Object Notation, JSON) manifest is
  oriented toward Microsoft 365 and Teams distribution. The issue directs us to "pick
  whichever sideloads fastest for a PoC; do not research both deeply," so we default to the
  XML manifest. If desktop Word rejects it, the unified manifest is the fallback.
- **Host form: `localhost`.** The #190 server binds `localhost`, the issue's solution outline
  says to point URLs at `https://localhost:<port>`, and Office tooling conventionally uses
  `localhost`; the #190 certificate's Subject Alternative Name covers both `localhost` and
  `127.0.0.1`, so either resolves and validates. The manifest therefore uses `localhost` with
  the port from the dev-endpoints configuration. (`127.0.0.1` appears in that configuration's
  `host` field for the launcher's health probe; it is a certificate-covered fallback, not the
  manifest host.)
- **Issue #190 is in place.** The certificate has been generated and trusted
  (`python -m addin.make_cert`) and the server is runnable (`python -m addin.server`, or via
  `tasks/run-app.ps1`). #191 depends on #190, which is merged to `master`.
- **An ordinary Windows developer machine with desktop Word installed**, meeting the ADR-028
  minimum Word API floor, and without managed-device policy that blocks trusted catalogs.
- **The pane stays a static hello-world page.** No document scanning, API calls, or
  authentication are added here; those arrive in issues #192, #193, #196, and #197.

## Risks

| Risk                                                                 | Impact                                                                    | Mitigation                                                                                                              |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Desktop-Word sideload differs from the documented Outlook-web path (the knowledge gap) | The pane never opens; the sprint tripwire fires and work stops            | Riskiest task scheduled first (Monday); trusted-catalog is a Microsoft-documented method; timeboxed to 2 days; XML→unified-manifest and `127.0.0.1`→`localhost` fallbacks identified up front |
| Word's aggressive manifest caching                                   | Edits appear to have no effect; hours lost chasing a phantom failure       | The runbook documents (and where possible scripts) clearing the `%LOCALAPPDATA%` Wef cache and a full Word restart       |
| Certificate not trusted or server not running                        | Blank or errored pane that looks like a manifest fault                     | Runbook states the #190 preconditions and reuses the #190 browser-padlock verification before touching Word              |
| Office add-in-domain handling of the loopback host                    | Pane fails to load despite a valid certificate                             | Manifest uses `localhost` (what the server binds and Office expects); certificate covers `127.0.0.1` too as a fallback     |
| Managed-machine policy blocks the trusted catalog                    | Sideloading fails for reasons outside this task                           | Target an ordinary developer machine; record the limitation in the runbook for anyone on a managed device                |
