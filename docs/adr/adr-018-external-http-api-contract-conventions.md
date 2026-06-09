# ADR-018 — External HTTP API Contract Conventions

## Summary

Redline adopts a single set of conventions for every external (north-south) HTTP API
surface it exposes: resource-based plural-noun URIs, correct HTTP methods, a standard
status-code set, a uniform error envelope, content negotiation, streamed binary
responses, a bearer-token auth pattern, and an async (`202`+poll) escalation with
Server-Sent Events (SSE) for progress (accepted 2026-06-09). This ADR records the
decisions and their rationale; the live operational rules — the clause text agents and
reviewers act on — live in `docs/architecture/api/http-api-standard.md` and are not
duplicated here. The hard constraint: an external HTTP surface that diverges from these
conventions is a defect, not a local style choice.

## Decision

Every external HTTP API surface follows the conventions below. The authoritative,
operational form of each rule lives in `docs/architecture/api/http-api-standard.md`
(the live standard). This ADR owns the *decision and rationale*; the live standard owns
the *current operational rule*. The two cross-link and never copy each other (ADR-001,
Single Source of Truth).

The bundled decisions:

1. **Resource-based, verb-free, plural-noun URIs.** Resources are named with plural
   nouns; the HTTP method carries the verb. Example: `POST /skeletons`, not
   `POST /generateSkeleton`.
2. **Correct HTTP methods and a standard status-code set.** `GET` reads, `POST` creates
   or triggers, `PUT`/`PATCH` update, `DELETE` removes. The status codes in scope are
   `200`, `201`, `202`, `400`, `401`, `403`, `422`, `500`.
3. **Uniform error envelope.** Every error response body is `{code, message, trace_id,
   details?}`. `message` MUST NOT contain stack traces or internal implementation
   detail. The envelope is produced by a single global exception handler — a
   framework-level binding, not per-route try/except.
4. **Validation split: `422` versus `400`.** A request that is well-formed but fails
   semantic or body validation returns `422` (Unprocessable Content). A request that is
   malformed or unparseable (bad JSON, wrong content type) returns `400` (Bad Request).
5. **Creation semantics.** Creating an addressable resource returns `201` with a
   `Location` header. A synchronous create-and-return of a streamed artifact — the
   skeleton case — returns `200` with the artifact as the body. Long-running work
   escalates to `202`+poll (decision 9).
6. **Binary responses stream as the body.** A generated `.docx` is returned with
   `Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document`
   and `Content-Disposition: attachment; filename="…"`, with the bytes as the response
   body. Binary is never base64-wrapped inside a JSON envelope.
7. **Auth is a bearer-token-in-`Authorization` pattern, format-agnostic.** The contract
   requires a bearer token in the `Authorization` header; it does not mandate a specific
   token format (the standard is not "JWT only"). An identity header injected by Google
   Identity-Aware Proxy (IAP) is an acceptable carrier. A `401` response MUST set
   `WWW-Authenticate: Bearer`. The concrete provider and token format are deferred until
   the SSO provider selection decision resolves.
8. **Artifact exchange is bytes-in-body for v0.1; file-link is the recorded target.**
   v0.1 returns artifacts as bytes in the response body (a volatile interface per
   ADR-017). By-reference exchange (a file link / URI the consumer fetches) is recorded
   as the target representation, activated when an MCP consumer, any external consumer, or
   the `202`+poll path arrives.
9. **Long-running operations use `202`+poll.** Work that can take on the order of minutes
   returns `202` and a job the client polls; the intermediate result is persisted /
   checkpointed so the operation survives a dropped connection. A synchronous connection
   is never held open for minutes — Cloud Run enforces a request timeout (default 300s,
   max 3600s), so a long synchronous hold is not a reliable contract.
10. **Progress over SSE with a defined event envelope.** Progress for async operations is
    delivered over a Server-Sent Events (SSE) channel using a defined event envelope and
    an `acknowledge → validate → progress → terminal` sequence. An ETA (estimated time to
    completion) is best-effort, omittable, and NEVER part of the contract. Phase + message
    ship first; a calibrated ETA is added later from real run-time data.
11. **Uniform internal event model; client-facing SSE is opt-in.** Every operation emits
    internal lifecycle events using one uniform vocabulary, for audit and observability.
    Client-facing SSE is NOT the default; it activates only for async (`202`+poll)
    operations with a user-perceptible duration gap. SSE event envelopes are projections
    of the internal vocabulary, not a parallel taxonomy.
12. **One resource, multiple representations, negotiated via `Accept`.** A resource may
    have several representations selected by the client's `Accept` header — `.docx` for a
    web download, a JSON "violations" contract for the future Word task pane to apply
    in-place. The URI does not change per representation.
13. **OpenAPI 3.x is the auto-generated, format-only API description.** The OpenAPI
    document is generated from the implementation and used as a description and client-
    generation artifact only. Contract-first authoring (hand-writing the OpenAPI document
    as the source of truth, then generating server stubs) is rejected.
14. **Rigour is tiered by trust boundary; security rigour is uniform.** External /
    north-south surfaces are high-rigour (OpenAPI contract, versioning once stable,
    `# stable:` annotation per ADR-017, breaking changes require a recorded decision).
    Internal / east-west surfaces are volatile per ADR-017 — and currently the internal
    tier is empty (a single Cloud Run service, no service-to-service HTTP). Security
    rigour is uniform across tiers: there is no implicit internal trust; the *mechanism*
    for east-west auth is deferred until an east-west boundary exists, but the *principle*
    binds now.
15. **Versioning is deferred.** No `/v1/` path prefix until a second endpoint or the first
    external consumer exists. Introducing a version scheme prematurely locks a shape that
    is still being discovered (ADR-017).

## Status

Accepted — 2026-06-09

## Context

Redline is exposing its first external HTTP surface: a `POST /skeletons` endpoint that
returns a generated `.docx` behind authentication. This is the first north-south boundary
in the system — the first interface crossed by a caller that is not inside the monorepo. ADR-017 (Interface Volatility by Default) explicitly excluded
external-facing HTTP APIs from its scope and required a separate ADR when one was
introduced. This is that ADR.

The forces in play:

- **A real first endpoint forces real decisions.** URI shape, status codes, error
  format, auth carrier, and binary delivery all have to be pinned for `POST /skeletons`
  to ship. Deciding them once, as conventions, prevents every future endpoint from
  re-litigating them.
- **The artifact is binary and potentially slow.** Skeleton generation produces a `.docx`
  and may take long enough that a synchronous hold becomes unreliable under Cloud Run's
  request timeout. The conventions must cover both the fast synchronous case and the slow
  async escalation without inventing a second API style.
- **Auth is not yet decided in detail.** The SSO provider and identity format are open.
  The API conventions must commit to a *pattern* (bearer token in `Authorization`,
  IAP-injected identity acceptable) without prematurely binding a provider or token format.
- **Two future consumers are visible.** A web download (wants `.docx` bytes) and a Word
  task pane (wants a JSON violations contract to apply in-place). One resource with
  multiple representations, negotiated via `Accept`, serves both without forking the API.
- **An MCP / AI consumer is on the horizon.** The Model Context Protocol (MCP) surface is
  not in force yet, but its constraints (OAuth 2.1 + PKCE, resource links not inline
  base64, MCP progress notifications) create tensions worth recording now so the HTTP
  conventions do not foreclose them. Those tensions are captured in
  `docs/architecture/api/mcp-standard.md` as a dormant target.
- **House defaults reduce decision cost.** FastAPI + Pydantic return `422` for body
  validation by default, and RFC 9110 makes `422` a first-class core HTTP status. Adopting
  the framework and RFC defaults rather than fighting them removes a recurring source of
  friction.

The conventions are filtered through Redline's current stage: Phase 1, solo founder + AI
agents, a single Cloud Run service, learning velocity prioritised over durability
(ADR-017). They are deliberately scoped to the *external* surface and deliberately defer
everything that does not yet have a forcing function (versioning, east-west security
mechanism, file-link exchange, ETA calibration).

## Options Considered

- **Option A — RPC-style verb URIs (`POST /generateSkeleton`).** Rejected: couples the
  URL to the operation name, scatters the verb across both method and path, and does not
  generalise to multiple representations of one resource. The plural-noun resource model
  is the web-API-design consensus and composes with content negotiation.
- **Option B — Base64-wrapped binary inside a JSON envelope.** Rejected: inflates payload
  size by ~33%, forces the client to decode before saving, and prevents the browser from
  treating the response as a file download. Streaming bytes with the correct
  `Content-Type` / `Content-Disposition` is the idiomatic and cheaper path.
- **Option C — Synchronous hold for long-running generation.** Rejected: Cloud Run
  enforces a request timeout; holding a connection for minutes is unreliable and wastes a
  request slot. `202`+poll with a persisted checkpoint is the durable pattern.
- **Option D — Contract-first OpenAPI authoring.** Rejected at this stage: hand-authoring
  the OpenAPI document as the source of truth adds drag (stub generation, drift between
  hand-written contract and implementation) before the API shape is proven. ADR-017's
  volatility logic applies — generate the description from the implementation instead.
- **Option E — Mandate a specific token format (JWT only).** Rejected: pre-empts the open
  SSO provider selection decision and excludes the IAP-injected-identity carrier. A
  format-agnostic bearer pattern keeps the auth decision where it belongs.
- **Option F — Introduce `/v1/` versioning now.** Rejected: a single endpoint with no
  external consumer has nothing to version against. Premature versioning locks a shape
  still under discovery (ADR-017). Defer until a second endpoint or first external
  consumer.
- **Option G — No conventions; decide per endpoint.** Rejected: produces exactly the
  inconsistency ADR-001 and ADR-017 exist to prevent, and forces every future endpoint to
  re-argue settled questions.

## Decision Rationale

The selected conventions are the intersection of three constraints filtered through
Redline's Phase-1 context:

1. **Framework and RFC defaults, not house inventions.** FastAPI + Pydantic emit `422`
   for body-validation failures by default, and RFC 9110 §15.5.21 defines `422
   Unprocessable Content` as core HTTP. Adopting the default rather than remapping it to
   `400` removes a standing source of per-route friction and keeps the generated OpenAPI
   honest. `400` is reserved for genuinely malformed/unparseable requests, where the
   distinction carries real diagnostic value.

2. **A single boundary, decided once.** Because every external response shares one error
   envelope, one status-code set, and one auth pattern, a reviewer has exactly one place
   to check conformance and a client author has exactly one model to learn. The single
   global exception handler is what makes "`message` never leaks internals" enforceable
   rather than aspirational — it is a structural guarantee, not a per-route discipline.

3. **Defer what has no forcing function.** Versioning, the east-west security mechanism,
   file-link artifact exchange, and ETA calibration are all recorded as targets but not
   built, because none has a present consumer. This is ADR-017's volatility logic applied
   to the external surface: commit to the *pattern* now, bind the *mechanism* when a real
   consumer arrives. The auth decision is the clearest case — the bearer pattern binds
   today; the provider and token format wait for the SSO provider selection decision.

The `202`+poll + SSE design is the one place the conventions invest ahead of strict
need, and the justification is concrete: Cloud Run's request timeout makes a synchronous
hold for a minutes-long generation unreliable, so the async escalation is a reliability
requirement, not a feature. Even there, the investment is staged — phase + message ship
first; the ETA is explicitly kept out of the contract until real run-time data exists to
calibrate it.

## Consequences

**Positive**

- Every external endpoint shares one shape: one URI style, one status-code set, one error
  envelope, one auth pattern. New endpoints inherit the conventions instead of re-deciding
  them.
- The single global exception handler makes "no internal detail in `message`" a structural
  guarantee enforceable by one test against one handler.
- Content negotiation lets the web download and the future Word task pane consume one
  resource without forking the API.
- The `202`+poll + SSE escalation gives a durable answer to long-running generation that
  survives Cloud Run's request timeout and dropped connections.
- Deferring versioning, east-west security mechanism, file-link exchange, and ETA
  calibration keeps Phase-1 velocity while recording each as an explicit, searchable
  target.

**Negative**

- The live standard (`docs/architecture/api/http-api-standard.md`) must be kept current as
  the operational source; this ADR intentionally does not carry the clause text, so the
  two must stay cross-linked and not drift apart (ADR-001 discipline).
- The async path (`202`+poll, persisted checkpoint, SSE) is more machinery than a
  synchronous endpoint. It is justified only where a user-perceptible duration gap exists;
  applying it to fast operations would be over-engineering.
- Framework-specific bindings (the FastAPI realisation of the global exception handler,
  the streaming response, the SSE channel) are pending the tech-stack session. Until
  then the standard is framework-agnostic and some clauses cannot yet be hook-enforced.
- The bearer-token *pattern* is fixed but the *mechanism* is not; any endpoint shipping
  before the SSO provider selection decision resolves carries a placeholder auth carrier
  that must be revisited.

## Constitution Impact

**None.** These are operational conventions for a single product surface — the external
HTTP API — not a new cross-cutting architectural principle. They derive from existing
principles already in the constitution (ADR-001 Single Source of Truth governs the
ADR↔live-doc split; ADR-017 Interface Volatility governs the tiering and deferral logic)
rather than introducing a new one. No constitution amendment is warranted and the
`check-adr-constitution-sync` hook should not be treated as triggered by this ADR: the
decision adds no cross-cutting invariant for the constitution to summarise. If a future
ADR elevates any of these conventions into a system-wide invariant (for example, a uniform
auth principle once east-west surfaces exist), that ADR — not this one — carries the
constitution amendment.

## References

- ADR-001 — Single Source of Truth (the ADR owns the decision; the live standard owns the
  operational rule; they cross-link, never copy)
- ADR-017 — Interface Volatility by Default (this ADR is the external-HTTP-API ADR that
  ADR-017 §Scope required; tiering and deferral logic derive from it)
- ADR-011 — Hook-first Enforcement (testable rules become hooks once the framework binding
  lands)
- `docs/architecture/api/http-api-standard.md` — the live operational standard (in force)
- `docs/architecture/api/mcp-standard.md` — the dormant MCP target standard
- RFC 9110, *HTTP Semantics* — methods, status codes, `422 Unprocessable Content`,
  `WWW-Authenticate`: https://www.rfc-editor.org/rfc/rfc9110
- RFC 9457, *Problem Details for HTTP APIs* — informs the error-envelope design:
  https://www.rfc-editor.org/rfc/rfc9457
- Server-Sent Events (WHATWG HTML, `text/event-stream`):
  https://html.spec.whatwg.org/multipage/server-sent-events.html
- OpenAPI Specification 3.x: https://spec.openapis.org/oas/latest.html
- Google Cloud Run request timeout: https://cloud.google.com/run/docs/configuring/request-timeout
- Google Cloud Identity-Aware Proxy (IAP) signed identity headers:
  https://cloud.google.com/iap/docs/signed-headers-howto
- Model Context Protocol specification: https://modelcontextprotocol.io/specification
- NotebookLM: *Web API Design* (resource modelling, content negotiation, versioning)
- NotebookLM: *FastAPI Implementation* (validation defaults, exception handling, streaming)
- NotebookLM: *AI System Engineering* (event vocabulary, observability, async lifecycle)
