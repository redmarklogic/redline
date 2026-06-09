# Feature Specification: OpenAPI Documentation

**Feature Branch**: `feature/003-openapi-docs`

**Created**: 2026-06-09

**Status**: Draft

**Input**: User description: "Add OpenAPI/Swagger docs to src/marker/app/ FastAPI app. Acceptance criteria: run-app.ps1 opens browser to /docs after app starts."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Browse Interactive API Docs (Priority: P1)

A developer runs the app locally and navigates to the interactive API docs to explore available endpoints, read schema definitions, and try requests directly from the browser.

**Why this priority**: Core deliverable. Without docs enabled and the browser opening automatically, no other scenario is reachable.

**Independent Test**: Can be fully tested by running the app, waiting for startup, and confirming the browser opens to the docs page showing the POST /skeletons endpoint.

**Acceptance Scenarios**:

1. **Given** the app is started via `run-app.ps1`, **When** the server becomes ready, **Then** the browser opens automatically to `http://127.0.0.1:8765/docs`.
2. **Given** the browser is open to `/docs`, **When** the page loads, **Then** the Swagger UI renders with the API title, version, and the POST /skeletons endpoint listed.
3. **Given** the Swagger UI is loaded, **When** a developer expands the POST /skeletons endpoint, **Then** the request schema, required fields, and response schema are all visible.

---

### User Story 2 - Try a Request in the Browser (Priority: P2)

A developer uses the "Try it out" button in Swagger UI to send a POST /skeletons request and inspects the response without leaving the browser.

**Why this priority**: Makes the docs interactive and self-validating; enables quick local smoke-testing.

**Independent Test**: Can be fully tested by using the Swagger UI "Try it out" button to submit a valid request and receiving a DOCX file download.

**Acceptance Scenarios**:

1. **Given** the Swagger UI is open, **When** the developer clicks "Try it out" on POST /skeletons and submits a valid payload, **Then** the response section shows HTTP 200 and offers a file download.
2. **Given** the developer submits a request missing a required field, **When** the response arrives, **Then** the Swagger UI displays the 422 validation error details.

---

### Edge Cases

- What happens when the docs URL is opened before the server is ready? Browser shows a connection error; the startup script already handles the readiness wait, so this is not a new concern.
- What happens if a developer navigates to `/redoc`? ReDoc endpoint is also enabled at `/redoc` by default — acceptable as a bonus, no action needed.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The app MUST expose an interactive Swagger UI at `/docs`.
- **FR-002**: The app MUST expose an OpenAPI JSON schema at `/openapi.json`.
- **FR-003**: The app MUST display a human-readable title and version in the docs UI.
- **FR-004**: The startup script MUST open the browser to `/docs` (not the root URL) when the server becomes ready.
- **FR-005**: The POST /skeletons endpoint MUST appear in the generated schema with its request body and response documented.

### Key Entities

- **API metadata**: Title, version, and optional description surfaced in the docs UI header.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The docs page loads within 3 seconds of the browser being opened on a developer machine with no cold-start delay.
- **SC-002**: All currently implemented endpoints (POST /skeletons) appear in the docs without manual annotation steps.
- **SC-003**: A developer unfamiliar with the codebase can identify the required request fields and submit a valid test request within 5 minutes of opening the docs.
- **SC-004**: The startup script opens the docs page automatically — zero manual steps required after `run-app.ps1` completes.

## Assumptions

- The app runs locally on `127.0.0.1:8765`; the docs URL is therefore `http://127.0.0.1:8765/docs`.
- No authentication is required to access the `/docs` or `/openapi.json` endpoints (developer-only tooling, not exposed in production).
- ReDoc (`/redoc`) is acceptable as an additional benefit but is not a stated requirement.
- Existing endpoint metadata (path, HTTP method, request/response schema) is sufficient without adding extra annotations to routes.
- The bearer-auth dependency on POST /skeletons will render in the docs as a security requirement, which is the desired behaviour.
