# Feature Specification: HTMX Vendoring (Dynamic Page Updates Without a Build Step)

**Branch**: `feature/162-htmx-vendoring`
**Created**: 2026-06-14
**Status**: Draft

## Overview

The Redline web application is a single Django service that renders its pages on the
server (decided in Architecture Decision Record ADR-024). For the product to feel
responsive — a user clicks a button and part of the page updates in place, instead of
the whole page reloading — the pages need a small amount of client-side behaviour.
The team has chosen **htmx** for this: htmx is a compact JavaScript library that lets
ordinary Hypertext Markup Language (HTML) elements issue Hypertext Transfer Protocol
(HTTP) requests and swap the server's HTML response into the page. The deliberate
constraint, set in ADR-024, is that this must happen with **no JavaScript build step**:
no Node.js, no package manager, no second-language toolchain that a developer would
have to learn and maintain. The library is therefore *vendored* — a single pre-built
file is checked into the repository and served directly by the application.

This feature delivers that enabling capability and proves it works end to end: the
vendored htmx file is served as a static asset, and an interactive control on a page
triggers a request to the server that swaps in a server-rendered fragment, with no full
page reload. It must work both on a developer's machine and in the deployed cloud
environment (where the application runs with debug mode switched off).

This is a small enabling slice. It is the foundation that the auth-gated button page
(issue #171) and the click-to-event-capture work (issue #172) build on. To keep the
boundary clean, this slice introduces only a throwaway demonstration page that proves
the round trip; it does **not** add sign-in gating, the real product buttons, or any
recording of user events. Those belong to #171 and #172 and may replace the demo page.

## Scenarios (mandatory)

<!-- Prioritised using RICE scoring (Reach x Impact x Confidence / Effort). Ordered by score, highest first.
     Reach interpretation for this enabling slice: the number of downstream user-facing flows it unblocks
     this sprint — the auth-gated button page (#171), click-to-event capture (#172), and future htmx pages. -->

### Scenario 1 -- A user action updates part of the page, with no build step

A page served by the web application shows an interactive control (for this slice, a
single demonstration button). When the user activates the control, the browser sends a
request to the server, and the server's HTML response replaces a specific region of the
page in place — the rest of the page does not reload. The behaviour is driven entirely
by the vendored htmx file loaded from the application's own static assets; no JavaScript
package manager, bundler, or build step exists anywhere in the project.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 3     | 3              | 90             | 1.0                  | 8.1        |

**Independent test**: Start the application locally, open the demonstration page, and
click the button. Observe that the targeted page region is replaced by content returned
from the server and that the page as a whole does not reload. Confirm with an automated
test that the request returns the expected HTML fragment, and confirm by inspection that
the repository contains no `package.json`, `node_modules`, or JavaScript build
configuration.

**Acceptance criteria**:

1. **Given** the application is running locally, **When** a browser requests the
   demonstration page, **Then** the page loads the vendored htmx file from the
   application's static assets and returns HTTP 200.
2. **Given** the demonstration page is open, **When** the user activates the interactive
   control, **Then** the server receives a request and returns an HTML fragment, and that
   fragment replaces the designated region of the page without a full page reload.
3. **Given** the interactive control issues a state-changing request, **When** that
   request reaches the server, **Then** it satisfies the application's Cross-Site Request
   Forgery (CSRF) protection and is not rejected.
4. **Given** the project as checked in, **When** a developer sets it up and runs it,
   **Then** no JavaScript build step, bundler, or package manager is required at any point.

---

### Scenario 2 -- The capability works in the deployed environment, not just locally

The same vendored file must be delivered correctly when the application runs in its
deployed configuration. Django's development server only serves static files
automatically when debug mode is on; the cloud deployment runs with debug mode off, so a
production-capable mechanism for serving static files is required. Without this, the
interactive pages would work on a developer's machine but silently fail in the cloud —
exactly where the sprint's demonstration has to run.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 3     | 1.5            | 85             | 0.5                  | 7.65       |

**Independent test**: Run the application with production-like settings (debug mode off
and static files collected), request the vendored library's static URL, and confirm a
successful response with the correct content type. Confirm the demonstration round trip
from Scenario 1 also succeeds under these settings.

**Acceptance criteria**:

1. **Given** the application is configured as it is for deployment (debug mode off, after
   static files are collected), **When** a browser requests the vendored htmx file's
   static URL, **Then** the server returns it successfully with a JavaScript content type.
2. **Given** the application is running under production-like settings, **When** the user
   activates the demonstration control, **Then** the in-place update from Scenario 1 still
   works.

---

### Edge Cases

- **State-changing request without a valid CSRF token**: the server must reject it
  (standard protection), so htmx must be configured to send the token with every
  state-changing request. The demonstration must prove the token path works.
- **Static files not collected before deployment**: if the deploy pipeline (issue #177)
  does not collect static files, the production static mechanism would not find the
  vendored file. This slice must make the requirement explicit so #177 can honour it.
- **Stale cached copy after a version bump**: if the vendored file is later updated, users
  holding a cached old copy should not be served a broken mix. The delivery mechanism
  should support cache-busting (for example, content-hashed filenames) so a future version
  change is safe.
- **A second vendored file is requested later**: ADR-024 flags "one more vendored file" as
  the scope-creep route toward a second-language toolchain. This slice vendors exactly one
  file and records it as the precedent to police.

## Requirements (mandatory)

### Functional Requirements

- **FR-001**: The web application MUST include the htmx library as a single vendored
  static file checked into the repository, introducing no JavaScript package manager,
  bundler, or build step (ADR-024 "all-Python line").
- **FR-002**: A page served by the application MUST be able to issue an HTTP request in
  response to a user action and replace a designated region of the page with the server's
  HTML response, without a full page reload.
- **FR-003**: The server endpoint that handles a state-changing request from the page MUST
  enforce the application's CSRF protection, and the page MUST send the information needed
  to pass that protection.
- **FR-004**: The vendored htmx file MUST be delivered successfully both in local
  development and when the application runs under its deployed configuration with debug
  mode off.
- **FR-005**: The exact htmx version MUST be pinned and recorded (in the repository and in
  the plan) so the vendored asset is reproducible and auditable.
- **FR-006**: This slice MUST provide a self-contained demonstration (a page plus the
  endpoint it calls) sufficient to prove FR-002 through FR-004, and MUST NOT implement
  sign-in gating, the real product buttons, or recording of user events — those are owned
  by issues #171 and #172. The demonstration may be removed or replaced when #171 lands.
- **FR-007**: This slice MUST NOT modify the application's existing root page or health
  endpoint, which are owned by other issues (#171 owns the root/home page).

### Key Entities

Not applicable. This slice introduces no persistent data. Recording user interactions is
the responsibility of the audit-log model (#166) and the click-to-capture work (#172).

## Success Criteria (mandatory)

- **SC-001**: On the demonstration page, a user action produces an in-place content update
  (no full page reload) in under one second under local development.
- **SC-002**: The vendored htmx file is delivered with a successful response in both a
  local-development run and a production-settings run (debug mode off, static files
  collected).
- **SC-003**: The project sets up and runs with no JavaScript build tool, bundler, or
  package manager added — verifiable by the absence of `package.json`, `node_modules`, and
  any JavaScript build configuration.
- **SC-004**: Automated tests prove (a) the user-action-to-HTML-fragment round trip
  including the CSRF path, and (b) successful delivery of the vendored file under
  production-like settings; these tests pass in the project's standard test run.

## Assumptions

- **htmx is a fixed product decision, not an open choice.** ADR-024 names htmx, vendored
  as a single file with no build step, as the front-end interactivity approach and the
  precedent test for all future front-end requests. This spec treats that as a given.
- **The exact htmx release is the latest stable 2.x line**, pinned at the moment of
  vendoring and recorded. The precise patch version is a download-time fact captured in
  the plan; nothing in this spec depends on a specific patch.
- **Production static delivery is in scope for this slice (founder decision, 2026-06-14).**
  The team chose to make the vendored file serve under deployed/debug-off settings now,
  rather than defer that to the deploy task (#177), so the capability is self-contained and
  the auth-gated buttons (#171) are guaranteed to work in the cloud for the sprint
  demonstration. If this assumption were reversed, Scenario 2 would move to #177 and #171
  would carry the risk of the deployed app not serving htmx. The concrete production
  mechanism is an implementation detail recorded in the plan, not in this spec.
- **The demonstration is throwaway.** Its only job is to prove the capability. The real
  user-facing page is designed and built under #171; this slice deliberately avoids
  designing that page.

## Risks

| Risk                                                        | Impact                                                                                  | Mitigation                                                                                              |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| CSRF token not sent with htmx requests                      | State-changing requests are rejected (HTTP 403); buttons appear broken                  | Configure htmx to send the CSRF token on every request; cover the path with an automated test          |
| Static files not collected in the deploy pipeline (#177)    | Vendored file missing in the cloud; interactive pages fail only in production           | Make the "collect static files" requirement explicit as a contract for #177; test under prod settings  |
| Vendored-file scope creep ("just one more file")            | Erosion of the no-build-step / all-Python rule that ADR-024 protects                    | Vendor exactly one file; record it as the policed precedent; future additions need an explicit decision |
| Stale cached copy after a future version bump               | Users served an inconsistent old/new mix                                                | Use a cache-busting delivery mechanism (content-hashed filenames) so version changes are safe           |
| Demonstration page collides with #171's real page           | Rework or merge conflict when #171 lands                                                | Put the demo on a dedicated URL; leave the root page and health endpoint untouched (FR-007)             |
