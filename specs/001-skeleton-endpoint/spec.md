# Feature Specification: Skeleton Endpoint (POST /skeletons returns DOCX behind auth)

**Feature Branch**: `feature/51-platform-p-skeleton-endpoint-post-skeleton-returns-docx-behind-auth`

**Created**: 2026-06-09

**Status**: Draft

**Input**: GitHub issue [#51](https://github.com/redmarklogic/redline/issues/51) — "Platform P — skeleton endpoint: POST /skeletons returns DOCX behind auth". Grounded in [ADR-018](../../docs/adr/adr-018-external-http-api-contract-conventions.md) and the live [HTTP API Standard](../../docs/architecture/api/http-api-standard.md).

## Overview

Redline exposes its first external (north-south) HTTP surface: an authenticated endpoint that turns an existing internal skeleton-builder into a callable web operation returning a Word document. This is the first end-to-end web flow — a caller from outside the system asks for a report skeleton and receives a downloadable `.docx`. The value of this feature is not new generation logic (the builder already exists); it is a **uniform, safe, authenticated contract** at the system boundary that every future endpoint will inherit.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authenticated caller downloads a skeleton document (Priority: P1)

An authenticated caller submits a well-formed skeleton request and receives a Word document they can open and edit. This is the primary value path — the reason the endpoint exists.

**Why this priority**: Without the success path, there is no product. This is the minimum viable slice — it proves the boundary works end to end (auth accepted, request processed, binary artifact returned as a download).

**Independent Test**: Submit a valid request with valid credentials; confirm the response is a successful download whose body is a `.docx` that opens in Word and contains the requested sections and project metadata.

**Acceptance Scenarios**:

1. **Given** a caller with valid credentials and a well-formed skeleton request, **When** they create a skeleton at `POST /skeletons`, **Then** they receive `200 OK` with the `.docx` as the response body.
2. **Given** the successful response, **When** the caller inspects the response headers, **Then** `Content-Type` is `application/vnd.openxmlformats-officedocument.wordprocessingml.document` and `Content-Disposition` is `attachment; filename="<name>.docx"`.
3. **Given** the successful response, **When** the caller saves the body to disk, **Then** the file opens in Word and contains the requested section headings and the project metadata table — the bytes are the document itself, not a wrapped/encoded payload.

---

### User Story 2 - Unauthenticated caller is refused (Priority: P1)

A caller with no credentials (or invalid credentials) is denied access and told how to authenticate. The artifact is never produced or returned to an unauthenticated caller.

**Why this priority**: The endpoint is "behind auth" by definition. An unauthenticated path that leaks the artifact, or that fails without a recoverable challenge, defeats the feature's purpose and is a security defect. It ships in the same slice as P1.

**Independent Test**: Submit a request without credentials; confirm refusal with the standard authentication challenge and no document body.

**Acceptance Scenarios**:

1. **Given** a caller with no credentials, **When** they call `POST /skeletons`, **Then** they receive `401` and the response sets `WWW-Authenticate: Bearer`.
2. **Given** a caller with no/invalid credentials, **When** they call `POST /skeletons`, **Then** the response body is the uniform error envelope and contains **no** document bytes.

---

### User Story 3 - Callers receive uniform, safe errors (Priority: P2)

Every failure — bad credentials, invalid input, malformed input, or an internal fault — returns the same error shape, and that shape never leaks internal implementation detail. A client author learns one error model.

**Why this priority**: Uniform, safe errors are what make the boundary trustworthy and the contract learnable. It depends on P1/P2 existing but is independently testable per failure mode.

**Independent Test**: Drive each failure mode (401, 422, 400, 500) and confirm each returns the same envelope shape with a display-safe message.

**Acceptance Scenarios**:

1. **Given** an authenticated caller submits a request body that parses but fails validation (e.g. an empty sections list, a duplicate heading, a missing metadata field), **When** they call `POST /skeletons`, **Then** they receive `422` with the uniform error envelope.
2. **Given** a caller submits a malformed or unparsable request (bad JSON, wrong content type), **When** they call `POST /skeletons`, **Then** they receive `400` with the uniform error envelope.
3. **Given** any error response (`401`, `400`, `422`, `500`), **When** the caller reads `message`, **Then** it is human-readable and contains no stack traces, exception/class names, file paths, or other internal detail.
4. **Given** any error response, **When** the caller parses the body, **Then** it has the shape `{code, message, trace_id, details?}`.

---

### Edge Cases

- **Empty sections list** → parsed-but-invalid → `422`.
- **Duplicate section headings** → parsed-but-invalid → `422`.
- **Blank/whitespace-only heading** → parsed-but-invalid → `422`.
- **Missing required metadata field** (project number, client name, site address, date) → parsed-but-invalid → `422`.
- **Malformed JSON or wrong content type** → unparsable → `400`.
- **Valid auth + valid body, but document generation faults internally** → `500` with the uniform envelope and no internal leakage.
- **Expired/invalid token** → `401` with `WWW-Authenticate: Bearer` (treated as unauthenticated for this endpoint; finer-grained `403` is out of scope until roles exist).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose a resource at path `/skeletons` that accepts `POST` — a plural-noun, verb-free URI with the verb carried by the method (ADR-018 §1).
- **FR-002**: On a valid authenticated request, the system MUST return `200 OK` with the generated document as the response body; no `Location` header is required (ADR-018 §5).
- **FR-003**: The successful document response MUST set `Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document` and `Content-Disposition: attachment; filename="<name>.docx"`, with the document bytes as the body. The artifact MUST NOT be base64-encoded or wrapped inside a JSON envelope (ADR-018 §6).
- **FR-004**: A request with absent or invalid credentials MUST return `401` and MUST set the `WWW-Authenticate: Bearer` response header (ADR-018 §7).
- **FR-005**: Every error response (`401`, `422`, `400`, `500`) MUST use the uniform error envelope `{code, message, trace_id, details?}` (ADR-018 §3).
- **FR-006**: The `message` field of any error response MUST NOT contain stack traces, exception or class names, file paths, query text, or any other internal implementation detail; it MUST be safe to display to an end user (ADR-018 §3).
- **FR-007**: A request body that parses successfully but fails semantic/body validation MUST return `422`; a request that cannot be parsed at all (malformed JSON, wrong/missing content type) MUST return `400` (ADR-018 §4).
- **FR-008**: The error envelope MUST be produced by a single, centralized error-handling mechanism shared across all routes — not by per-route handling — so that "no internal leakage" is a structural guarantee verifiable in one place (ADR-018 §3).
- **FR-009**: The endpoint MUST NOT emit Server-Sent Events or present any real-time server-progress channel; as a synchronous operation it makes no claim of streamed server progress (ADR-018 §9 honesty constraint).
- **FR-010**: The endpoint path MUST NOT carry a `/v1/` (or any other) version prefix (HTTP API Standard §14 = ADR-018 decision 15).
- **FR-011**: The API description (OpenAPI document) MUST be generated from the implementation, not hand-authored (ADR-018 §12).
- **FR-012**: Each in-scope ADR-018 clause MUST be covered by at least one test that asserts the externally observable HTTP contract (status code, header, body shape) — not an internal implementation detail.

### Key Entities *(include if feature involves data)*

- **Skeleton request**: the caller-supplied input describing the document to build. Comprises a **report structure** (an ordered, non-empty list of unique section headings) and **project metadata** (project number, client name, site address, date). *(Assumption — mirrors the inputs of the existing builder; see Assumptions.)*
- **Skeleton document**: the generated `.docx` artifact returned as the response body — the report skeleton (metadata table + section headings).
- **Error envelope**: the uniform failure representation `{code, message, trace_id, details?}` returned by every non-success response.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the in-scope ADR-018 clauses (§1, §3, §4, §5, §6, §7, §9, §12, §14) have at least one passing test asserting the observable HTTP contract.
- **SC-002**: An authenticated caller submitting a valid request receives, every time, a downloadable file that opens in Word and contains the requested sections and metadata.
- **SC-003**: An unauthenticated caller receives `401` with the `WWW-Authenticate: Bearer` challenge and never receives document bytes — 100% of unauthenticated attempts.
- **SC-004**: Across all four error paths (`401`, `400`, `422`, `500`), no response body exposes internal implementation detail in `message` — verified by inspection of each path.
- **SC-005**: The published API description is generated from the running implementation and matches observed behavior (no hand-authored drift between description and endpoint).

## Assumptions

- **Request body mirrors the existing builder inputs.** The request carries a report structure (sections) plus project metadata (project number, client name, site address, date) — the inputs of the existing `build_skeleton` operation. Richer, LOE-driven generation (document parsing / metadata extraction), standards-grounded clause content, quota enforcement, and the audit trail are **separate features and out of scope** for this endpoint. *(This is the one materially scope-shaping assumption; flagged for confirmation.)*
- **Auth is the bearer pattern; the mechanism is deferred.** The endpoint requires a bearer token in `Authorization`; the concrete provider and token format are deferred to the SSO decision (depends on **#50**; provider/format per #73 / #48b). Until that resolves, a **placeholder bearer carrier** is used and explicitly flagged.
- **The global error handler ships as a documented placeholder pending #78.** Per issue #51's "Option B — #78 ordering" note, the framework-level binding of the single global exception handler ships as a documented placeholder pending the tech-stack session (**#78**). The placeholder MUST be flagged in the PR and tracked as a follow-up before any external consumer relies on the endpoint. The PR MUST state explicitly whether the handler is final (#78-aligned) or a placeholder.
- **Synchronous return is viable.** Generation completes within the request timeout; the long-running `202`+poll / SSE escalation (ADR-018 §8–§9) is **not** triggered and is out of scope here.
- **Filename derivation.** The `Content-Disposition` filename is derived from the request (e.g. the project number); the exact derivation rule is an implementation detail.

## Dependencies

- **#50 — SSO integration**: supplies the auth carrier the endpoint sits behind (the issue lists this as the dependency). The bearer *pattern* is fixed now; the *mechanism* arrives with SSO.
- **#78 — tech-stack session**: supplies the framework binding for the single global exception handler (and streaming response). Drives the Option B placeholder above.
- **ADR-018 / HTTP API Standard**: the authoritative contract every requirement here cites.
- **Existing builder**: `build_skeleton(structure, metadata, output_path)` in `marker.functions.builders`, with domain models `ReportStructure` and `ProjectMetadata` in `marker.domain.models`.

## Out of Scope

- LOE upload and metadata extraction (Feature M / Document Parser).
- Standards grounding and mandatory clause boilerplate content (Feature N / Standards Knowledge Store).
- Quota enforcement and the generation audit trail.
- Conditional section logic (blocked pending Peter shaping per the skeleton-generator PRD).
- The `202`+poll asynchronous path, SSE progress events, and the JSON "violations" content-negotiation representation (ADR-018 targets, deferred).
- By-reference artifact exchange via signed URLs / object storage (ADR-018 §6a target, deferred behind a future infra ADR).
- Versioning and the `# stable:` annotation (deferred until a second endpoint or first external consumer — HTTP API Standard §14).
- **Cross-origin (CORS) configuration** for the browser client. CORS is a platform/deployment concern (Platform P / SSO #50), not part of the endpoint *contract* this feature defines. If the web app and the API end up on different origins, CORS is wired at the platform layer, not here.
- **Request-size and section-count limits, and rate limiting.** The free-tier quota (3–5 documents per user, ~100 pages each) is a separate feature in the skeleton-generator PRD; #51 adds no per-request size cap or rate limiter.

> **Citation convention**: clause numbers in this spec are **HTTP API Standard** §-numbers. They equal the ADR-018 decision-numbers except for versioning (ADR-018 *decision 15* ≡ Standard *§14*). Issue #51's "§15" refers to the ADR decision-number.
