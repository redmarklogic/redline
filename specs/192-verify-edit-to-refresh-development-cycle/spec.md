# Feature Specification: Verify Edit-to-Refresh Development Cycle

**Feature Branch**: `feature/192-verify-edit-to-refresh-development-cycle`

**Created**: 2026-06-14

**Status**: Draft

**Input**: GitHub issue [#192](https://github.com/redmarklogic/redline/issues/192) — "Verify edit-to-refresh development cycle" (Sprint 4, Work Breakdown Structure item 2.3, child of parent [#189](https://github.com/redmarklogic/redline/issues/189))

## Overview

This feature is a verification spike. A spike, in this team's working vocabulary, is a small, time-boxed investigation whose goal is to answer a question and write down the answer, rather than to ship a polished product feature. The question this spike answers is narrow but important to the whole sprint: **when a developer changes a file that the Word taskpane displays, how quickly and how reliably does that change show up in the pane?**

The Sprint 4 proof of concept is a Microsoft Word taskpane — a small web page that Word shows in a side panel — served from the team's Python stack. During the rest of the sprint, developers will repeatedly edit the taskpane's page (its HyperText Markup Language, or HTML, and its JavaScript code) and need to see those edits in Word to make progress. If that loop is slow or unreliable — for example, if it requires closing Word, regenerating certificates, or re-installing the add-in every time — the team loses hours and the sprint's hardest tasks (wiring the pane to a live document-scanning service) become painful. The founder has made the speed of this loop a constraint on the whole sprint: change a file, see it in the pane, with no compile step in between.

The supporting material the team has gathered so far (from a reference notebook of add-in sources) documents the fast "hot reload" loop only for the Node.js toolchain. Redline deliberately does **not** use Node.js for this pane — it is plain HTML and vanilla JavaScript served by a Python web server. So the Python-only edit-to-refresh loop is an unverified gap. This spike closes that gap by actually performing the loop, confirming it works, and recording the steps and the rough loop time so the next developer can reproduce it without rediscovery.

The deliverable is not new product code. The deliverable is **evidence and documentation**: a confirmation that the loop works as required, plus a written "refresh cycle" section added to the spike notes that feed the demonstration-and-skill-writeup task ([#198](https://github.com/redmarklogic/redline/issues/198)).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer sees an edit reflected in the pane without restarting Word (Priority: P1)

A developer has the Word taskpane already open and working inside desktop Word (the result of the preceding sideload task, [#191](https://github.com/redmarklogic/redline/issues/191)). They change a piece of visible text in the taskpane's HTML file on disk and save it. They then reload the pane using only the lightweight means available inside Word — right-clicking inside the pane and choosing "Reload", or closing and reopening the pane. The edited text appears. They did not have to restart Microsoft Word, regenerate the development certificate, or re-install ("re-sideload") the add-in.

**Why this priority**: This is the entire point of the spike. If this scenario fails, the sprint's most error-prone tasks become slow and frustrating, and the founder's whole-sprint constraint is violated. There is no smaller slice that delivers the value — this single scenario *is* the minimum viable outcome.

**Independent Test**: With the pane open in Word and the Python development server running, change a visible string in the taskpane HTML, save, reload the pane, and confirm by eye that the new string is shown. This is a human-performed verification (marked `[human-verify]` in the acceptance scenarios below) because it depends on the behaviour of the installed desktop Word application and its embedded web view, which cannot be exercised by an automated test in this codebase.

**Acceptance Scenarios**:

1. **Given** the taskpane is open in desktop Word and the Python development server is running, **When** a developer changes a visible string in the taskpane HTML on disk, saves it, and reloads the pane (right-click → Reload, or close and reopen), **Then** the changed string is visible in the pane without restarting Word and without re-sideloading the add-in. `[human-verify]`
2. **Given** the developer has performed the loop at least once, **When** they observe how long the loop takes from saving the file to seeing the change, **Then** the loop completes in seconds rather than minutes. `[human-verify]`

---

### User Story 2 - The verified cycle is written down so others can reproduce it (Priority: P2)

Having confirmed the loop works, the developer writes down the exact steps they used and the rough time the loop took, in a place that the later demonstration-and-skill-writeup task ([#198](https://github.com/redmarklogic/redline/issues/198)) will draw on. A future reader who has never performed this loop can follow the written steps and reproduce the result.

**Why this priority**: The confirmation in User Story 1 is worthless to the rest of the team if it lives only in one developer's head. Writing it down is what turns a one-off success into reusable team knowledge. It is P2 only because it cannot happen before the loop has actually been confirmed (User Story 1).

**Independent Test**: Open the spike notes file and confirm it contains a "refresh cycle" section that lists the reload steps and a rough loop time. This is verifiable by checking that the file exists and contains that section.

**Acceptance Scenarios**:

1. **Given** the edit-to-refresh loop has been confirmed to work, **When** the developer documents it, **Then** the spike notes that feed [#198](https://github.com/redmarklogic/redline/issues/198) contain a "refresh cycle" section recording the reload steps and the approximate loop time. Verification: the spike notes file exists and contains a "refresh cycle" section.

---

### Edge Cases

- **The embedded web view serves a stale, cached copy of the page.** The known rabbit hole for this spike is that the web view inside Word (Microsoft Edge WebView2) may hold the previous version of the page in its cache and show it again after a reload, hiding the developer's edit. If this happens, the spike must determine and record a reliable workaround — most likely instructing the Python server to send cache-disabling response headers so the web view always fetches a fresh copy. The acceptance is not met until the reload reliably shows the new content.
- **A change to server-side Python code rather than the page.** Editing the Python server module is a different loop from editing the page: the development server already restarts itself on Python changes. This spike is scoped to the page (HTML/JavaScript) edit loop, not the server-code loop; if the distinction matters to a reader, the notes should state it briefly.
- **The reload appears to do nothing.** If neither right-click → Reload nor close-and-reopen surfaces the change, the developer must escalate to the next-heaviest action and record which action was actually required, so the documented loop reflects reality rather than the hoped-for ideal.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The development setup MUST allow a developer to change the taskpane page (HTML or JavaScript) on disk and, after a lightweight in-Word reload, see that change in the open pane without restarting Microsoft Word.
- **FR-002**: The edit-to-refresh loop MUST NOT require regenerating the development certificate or re-installing (re-sideloading) the add-in for the changed content to appear.
- **FR-003**: The verified reload procedure MUST rely only on means available to a developer inside Word (such as right-clicking the pane and choosing "Reload", or closing and reopening the pane). No additional tooling that watches files and reloads automatically is to be introduced (see Out of Scope).
- **FR-004**: If the embedded web view shows a stale cached page instead of the edited page, the setup MUST be adjusted so that a reload reliably serves the current page (for example, by the server sending cache-disabling response headers), and the adjustment MUST be recorded.
- **FR-005**: The team MUST capture the confirmed reload steps and the approximate loop time in a "refresh cycle" section of the spike notes that feed task [#198](https://github.com/redmarklogic/redline/issues/198), such that a reader who has not performed the loop can reproduce it.

### Key Entities

- **Taskpane page**: The HTML and JavaScript file(s) that Word displays in the side panel, served as static files by the Python development server. The artefact a developer edits.
- **Development server**: The Python web server that serves the taskpane page over a secure connection during development. The component whose caching behaviour determines whether an edit is seen.
- **Spike notes ("refresh cycle" section)**: The written record of the confirmed loop — the reload steps and rough loop time — that seeds the demonstration-and-skill-writeup task ([#198](https://github.com/redmarklogic/redline/issues/198)).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can change a visible string in the taskpane page, reload the pane, and see the change — confirmed by direct observation in desktop Word — without restarting Word or re-sideloading the add-in.
- **SC-002**: The time from saving the edited file to seeing the change in the pane is measured in seconds, not minutes (the loop is fast enough to use repeatedly during a development session).
- **SC-003**: A second person, following only the written "refresh cycle" notes, can reproduce the loop and see an edit appear, without asking the original developer for missing steps.
- **SC-004**: The spike notes that feed [#198](https://github.com/redmarklogic/redline/issues/198) contain a "refresh cycle" section that names the reload steps and the rough loop time.

## Assumptions

- The preceding sideload task ([#191](https://github.com/redmarklogic/redline/issues/191)) is complete: the taskpane can be opened in desktop Word and the Python development server serves it over a secure connection. This spike begins from a working, sideloaded pane.
- The taskpane page is served as static files by the Python development server (no Node.js toolchain is involved), consistent with the Sprint 4 goal of a Python-served pane.
- "Lightweight reload" means the means a developer has inside Word — right-click → Reload within the pane, or closing and reopening the pane — not a full restart of the Word application.
- The spike notes that feed [#198](https://github.com/redmarklogic/redline/issues/198) are a markdown document maintained for the Sprint 4 add-in spike (parent [#189](https://github.com/redmarklogic/redline/issues/189)); the exact file path is to be fixed during planning, with the only hard requirement being that the "refresh cycle" section is discoverable by the [#198](https://github.com/redmarklogic/redline/issues/198) writer.
- This is a low-risk task scheduled within Tuesday 23 June 2026, performed after the higher-risk manifest-and-sideload task it depends on.

## Out of Scope

- **Automatic reload tooling.** No file-watcher or live-reload mechanism that detects a saved file and refreshes the pane without a manual action. For this proof of concept, a manual reload is acceptable provided the loop takes seconds, not minutes. (Explicit no-go from the source issue.)
- **The server-side Python edit loop.** Verifying how quickly changes to the Python server code take effect is a separate concern; this spike covers the page (HTML/JavaScript) edit loop only.
- **Production or deployed behaviour.** This spike concerns the local development loop only. Caching and refresh behaviour of any future deployed taskpane is not in scope.
- **Taskpane visual design.** No styling or user-experience work on the pane itself; the only edits made are throwaway, to prove that edits propagate.
