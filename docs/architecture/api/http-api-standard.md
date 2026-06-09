# HTTP API Standard

**Status:** In force (v0.1)
**Grounding decision:** [ADR-018 — External HTTP API Contract Conventions](../../adr/adr-018-external-http-api-contract-conventions.md)
**Scope:** Every external (north-south) HTTP API surface Redline exposes.
**Framework binding:** Framework-agnostic at v0.1. FastAPI-specific bindings (global
exception handler wiring, streaming response, SSE channel implementation) are **pending
the #78 tech-stack session** and will be added as a "FastAPI bindings" appendix once that
session lands.

This document is the **operational** standard — the clause text agents, reviewers, and
code follow. Each clause links to ADR-018 for the decision and rationale; this document
does not repeat the "why" (ADR-001, Single Source of Truth). If a clause and ADR-018
appear to disagree, that is a drift defect to fix, not a choice.

### Terms (for the uninitiated)

- **North-south** — traffic crossing the system's outer boundary (an external caller ↔ a
  Redline service). These surfaces are governed at *high* rigour.
- **East-west** — traffic between Redline's own internal services. Redline runs as a single
  Cloud Run service today, so there is currently **no east-west HTTP** (the internal tier
  is empty — see §11).
- **SSE (Server-Sent Events)** — a one-way HTTP streaming channel (`text/event-stream`)
  where the server pushes a sequence of named events to the client over a held connection.
  Used here for progress on long-running operations.
- **OpenAPI** — a machine-readable description of an HTTP API (paths, parameters,
  responses, schemas). Used here as a *generated description*, not a hand-authored contract
  (§12).
- **Bearer token** — a credential the client sends in the `Authorization` header that
  grants access by mere possession (the holder "bears" it).

---

## 1. Resource-based, verb-free, plural-noun URIs

Resources are named with **plural nouns**. The HTTP method carries the verb; the path
never does.

- Correct: `POST /skeletons`, `GET /skeletons/{id}`
- Wrong: `POST /generateSkeleton`, `GET /getSkeleton`

Rationale → ADR-018 decision 1.

## 2. HTTP methods and status codes

| Method | Meaning |
|--------|---------|
| `GET` | Read a resource or collection. Safe and idempotent. |
| `POST` | Create a resource, or trigger an operation. |
| `PUT` | Replace a resource. Idempotent. |
| `PATCH` | Partially update a resource. |
| `DELETE` | Remove a resource. Idempotent. |

Status codes in scope:

| Code | Name | Use |
|------|------|-----|
| `200` | OK | Successful read, or synchronous create-and-return of a streamed artifact (§5). |
| `201` | Created | An addressable resource was created. MUST include a `Location` header (§5). |
| `202` | Accepted | Work accepted for asynchronous processing; client polls a job (§8). |
| `400` | Bad Request | Request is malformed or unparsable — bad JSON, wrong content type (§4). |
| `401` | Unauthorized | No/invalid credentials. MUST set `WWW-Authenticate: Bearer` (§7). |
| `403` | Forbidden | Authenticated but not permitted. |
| `422` | Unprocessable Content | Request is well-formed but fails semantic / body validation (§4). |
| `500` | Internal Server Error | Unhandled server fault. Body uses the error envelope (§3); `message` carries no internal detail. |

Rationale → ADR-018 decision 2.

## 3. Error envelope

Every error response body has this shape:

```json
{
  "code": "string — stable, machine-readable error code",
  "message": "string — human-readable, safe for display",
  "trace_id": "string — correlation id for logs/observability",
  "details": "optional — structured field-level or context detail"
}
```

- `message` **MUST NOT** contain stack traces, exception class names, file paths, SQL, or
  any internal implementation detail. It is safe to show an end user.
- The envelope is produced by **a single global exception handler** — a framework-level
  binding, not per-route `try/except`. This is what makes "no internal leakage" a
  structural guarantee testable against one handler rather than a per-route discipline.
- `details` is the place for machine-actionable specifics (e.g. a list of validation
  failures). For domain-specific validation payloads (the "violations" contract, §10), the
  concrete schema of `details` is **owned by Graeme** (see Open Decisions).

Rationale → ADR-018 decision 3. Envelope informed by RFC 9457 (Problem Details).

## 4. Validation: `422` vs `400`

- **`422 Unprocessable Content`** — the request was parsed successfully but failed
  semantic or body validation (a required field missing, a value out of range, a type
  mismatch caught by the schema). This is the FastAPI + Pydantic default and is core HTTP
  per RFC 9110 §15.5.21.
- **`400 Bad Request`** — the request could not be parsed at all (malformed JSON, wrong or
  missing content type, an unreadable body).

Decision rule: *parsed but invalid → `422`; could not parse → `400`.*

Rationale → ADR-018 decision 4.

## 5. Creation and artifact-return semantics

- **Addressable resource created** → `201 Created` + `Location` header pointing at the new
  resource's URI.
- **Synchronous create-and-return of a streamed artifact** (the skeleton case: `POST
  /skeletons` returns the `.docx` immediately) → `200 OK` with the artifact as the body
  (§6). No `Location` is required because the artifact is the body, not a separately
  addressable resource.
- **Long-running work** → `202 Accepted` + a job to poll (§8). This is the documented
  escalation when synchronous return is not viable.

Rationale → ADR-018 decision 5.

## 6. Binary responses

A generated `.docx` (or any binary artifact) is returned as **raw bytes in the response
body**, with:

```
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename="<name>.docx"
```

The bytes are streamed as the body. Binary is **never** base64-encoded and wrapped inside
a JSON envelope.

Rationale → ADR-018 decision 6.

### 6a. By-reference artifact exchange — TARGET (deferred)

> **Status: TARGET / deferred — not Sprint-2.** Inline binary (§6) is the v0.1 rule. The
> by-reference path below activates only when the async (`202`+poll) path (§8) or an
> external / MCP consumer needs the `.docx` delivered by reference rather than in the
> response body. It is tracked in a dedicated infra issue and is **gated by a future infra
> ADR plus Peter's documented Tier-1 approval before any service is provisioned.** Do not
> implement ahead of that gate.

When activated, a generated `.docx` is delivered by reference (a `result_ref`, §9) backed
by Google Cloud Storage, under these binding constraints (Brent consult, 2026-06-09):

- **Signed-URL-only access.** Objects are reached exclusively through **V4 signed URLs**.
  The bucket uses **uniform bucket-level access** with **public-access-prevention enforced**;
  **no object is ever public**.
- **Short TTL ≤ retention.** The signed-URL time-to-live (TTL) is short and **never exceeds
  the object's retention / lifecycle window**.
- **Two separated identities, keyless.**
  - A **producer** identity that may only create/write objects —
    `roles/storage.objectCreator`, **not** `objectAdmin`.
  - A **signing** capability via IAM `signBlob`
    (`roles/iam.serviceAccountTokenCreator`), obtained **keyless through Workload Identity
    Federation** — **no service-account JSON key**.
  - The **consumer / reader holds no bucket IAM** at all; it only ever receives a signed URL.
- **Retention via lifecycle.** Objects expire through a **lifecycle delete-after-N-days**
  rule. A hard retention *lock* is a future-ADR design choice and is **not pre-decided here**.
- **Access logging.** **GCS Data Access audit logs** flow to a **centralised named audit
  sink**.

The bucket, IAM split, lifecycle policy, and audit sink are infrastructure decisions owned
by Brent and recorded in a **future infra ADR** (distinct from ADR-018, which is the API
contract). This standard fixes only the *envelope* expectation (`result_ref` points at a
signed-URL-fetchable artifact); the infra ADR fixes the *mechanism*.

## 7. Authentication

- The contract requires a **bearer token in the `Authorization` header**:
  `Authorization: Bearer <token>`.
- The standard is **format-agnostic** — it does not mandate JWT or any specific token
  format. An identity header injected by Google Identity-Aware Proxy (IAP) is an acceptable
  carrier of identity.
- A `401` response **MUST** set `WWW-Authenticate: Bearer` (RFC 9110 §11.6.1).
- The concrete provider and token format are **deferred to the SSO decision** (issues #73 /
  #48b). This standard fixes the *pattern*; the SSO decision fixes the *mechanism*.

Rationale → ADR-018 decision 7.

## 8. Long-running operations: `202`+poll

For work that can take on the order of minutes:

1. The trigger request returns `202 Accepted` and a job identifier (`job_id`).
2. The client polls a job-status resource until the job reaches a terminal state.
3. The intermediate result is **persisted / checkpointed** so the operation survives a
   dropped connection or a server restart.
4. A synchronous connection is **never** held open for minutes. Google Cloud Run enforces a
   per-request timeout (default 300 seconds, configurable up to 3600), so a long
   synchronous hold is not a reliable contract.

The durable store used for the checkpoint is an **Open Decision** (below).

Rationale → ADR-018 decision 9.

## 9. Progress over SSE — event envelope

Progress for an async (`202`+poll) operation is delivered over a **Server-Sent Events
(SSE)** channel. Each event carries this envelope:

| Field | Type | Required | Meaning |
|-------|------|----------|---------|
| `event` | string | yes | The lifecycle event name (see sequence below). A projection of the internal event vocabulary (§13). |
| `phase` | string | yes | Human-readable current phase (e.g. `"validating"`, `"rendering"`). |
| `percent` | number | optional | 0–100 completion estimate. Omit when not meaningfully computable. |
| `eta_seconds` | number | optional | Best-effort estimated seconds to completion. **NEVER a contract** — omittable, and may be wrong. Ship without it first (see Open Decisions). |
| `message` | string | optional | Human-readable status line for display. |
| `job_id` | string | yes | The job this event belongs to (correlates with the `202` response). |
| `result_ref` | string | optional | Present on the terminal success event: a reference to the produced artifact (the by-reference target, ADR-018 decision 8). |

**Event sequence:** `acknowledge → validate → progress* → terminal`

1. `acknowledge` — the server has accepted the job and is starting work.
2. `validate` — input validation is running / passed.
3. `progress` — zero or more progress events as work proceeds (`percent` / `phase` /
   `message` update here).
4. `terminal` — exactly one terminal event ends the stream: either success (carrying
   `result_ref`) or failure (carrying the error envelope shape from §3).

`eta_seconds` is best-effort and **never** part of the contract — clients must function
correctly when it is absent or inaccurate. Phase + message ship first; a calibrated ETA is
added later from real run-time data.

**Honesty constraint (binding).** A **synchronous** endpoint (e.g. `POST /skeletons`, §5)
emits **no client-facing SSE** and **MUST NOT** present a UI that implies real-time server
progress — no determinate percentage, no ticking checkmarks, no per-step server timers.
Those assert a real-time server channel that synchronous endpoints deliberately do not have.
A v0.1 "working" state is permitted only as an **illustrative client-side** indicator (no
implied SSE); see Open Decisions.

**Phase-driven upgrade seam.** The client progress indicator is modelled from day one as a
**phase-driven component**: it renders the *current phase* from a phase descriptor and is
agnostic to where that descriptor comes from. In v0.1 the phases are supplied on a
**client timer** (illustrative). When the Pre-Review pipeline (Bet 2) lands, the **same
component** swaps its data source to the **real SSE phase events** (§9) — and only then may
a *determinate* representation be unlocked. The data source is the seam; the component does
not change.

Rationale → ADR-018 decision 10.

## 10. Content negotiation — one resource, multiple representations

A resource may be returned in several representations, selected by the client's `Accept`
header. The URI does **not** change per representation.

- `Accept: application/vnd.openxmlformats-officedocument.wordprocessingml.document` → the
  `.docx` artifact (web download).
- `Accept: application/json` → a **JSON "violations" contract** the client applies
  in-place (the future Word task pane). The concrete schema of this violations payload is
  **owned by Graeme** (Open Decisions).

Rationale → ADR-018 decision 12.

## 11. Trust-boundary tiering

Rigour is tiered by where the surface sits relative to the system's trust boundary.
**Security rigour is uniform across tiers** — there is no implicit internal trust.

**Classifier — is a surface external (north-south) or internal (east-west)?**

- **External (north-south):** the caller is outside the monorepo / outside the trust
  boundary — a browser, an external integration, an AI/MCP consumer, an IAP-fronted client.
  → **High rigour.**
- **Internal (east-west):** the caller is another Redline-owned service inside the trust
  boundary. → **Volatile per ADR-017.**

| Tier | Rigour | Rules |
|------|--------|-------|
| External / north-south | High | OpenAPI description generated (§12); versioning once stable (§14); `# stable:` annotation per ADR-017 before any consumer may rely on it; breaking changes require a recorded decision. |
| Internal / east-west | Volatile (ADR-017) | No stability guarantee unless explicitly declared. **Currently empty** — see note. |

> **Dated note (2026-06-09):** Redline currently runs as a **single Cloud Run service**.
> There is **no east-west HTTP** today, so the internal tier is **empty**. When a second
> service is introduced and an east-west boundary appears, this note is removed and the
> internal-tier rules (including the deferred east-west security mechanism, Open Decisions)
> take effect.

**Security note:** the *mechanism* for east-west authentication is deferred until an
east-west boundary exists, but the *principle* — no implicit internal trust — binds now and
applies to whatever mechanism is later chosen.

Rationale → ADR-018 decision 14.

## 12. OpenAPI — generated, format-only

The OpenAPI 3.x document is **generated from the implementation** and used as a description
and client-generation artifact only. It is not hand-authored as a source of truth.
Contract-first authoring (writing the OpenAPI document first, generating server stubs from
it) is rejected at this stage.

Rationale → ADR-018 decision 13.

## 13. Internal event model — client-facing SSE is a projection

- **Every operation** emits internal lifecycle events using **one uniform vocabulary**, for
  audit and observability. This applies to all operations, synchronous and asynchronous.
- **Client-facing SSE is NOT the default.** It activates only for async (`202`+poll)
  operations with a **user-perceptible duration gap**. The activation threshold is an Open
  Decision (≈10s+, TBD).
- The SSE event envelopes (§9) are **projections** of the internal vocabulary — a filtered,
  client-safe view — not a separate, parallel taxonomy. The internal vocabulary is the
  source; the SSE envelope derives from it.
- **Synchronous endpoints emit internal events for audit only.** Because there is no
  client-facing SSE on a synchronous endpoint, the client UI MUST NOT fabricate determinate
  progress from internal events (§9 honesty constraint). The phase-driven progress component
  (§9) is the upgrade seam: its data source switches from a client timer to real SSE phase
  events when Pre-Review activates client-facing SSE.

Rationale → ADR-018 decision 11.

## 14. Versioning — deferred

No `/v1/` path prefix is introduced until **a second endpoint or the first external
consumer** exists. Once an external surface is stable and has a consumer, versioning and
the `# stable:` annotation (ADR-017) apply, and breaking changes require a recorded
decision.

Rationale → ADR-018 decision 15.

---

## Open Decisions

These are recorded gaps, not settled rules. Each will be resolved when a forcing function
arrives.

1. **SSE activation threshold.** The user-perceptible duration gap that turns on
   client-facing SSE (§13) is TBD — provisionally ≈10 seconds or more of expected runtime.
   To be calibrated from real run-time data.
   - *Resolved for v0.1 (Mark + Matt consult, 2026-06-09):* the synchronous skeleton ships
     **no** client-facing SSE. Its "working" state is an **illustrative client-side
     phase-driven indicator** — an indeterminate branded animation with present-tense
     descriptive captions, **no percentages, no checkmarks, no per-step timers**, minimum
     readable display ≈1.5–2.5s. The **honesty constraint** (§9) binds: it must not imply
     real-time server progress that was deliberately not built. The indicator is modelled as
     the **phase-driven component** (§9) so its data source can later swap to **real SSE
     phase events arriving with the Pre-Review pipeline (Bet 2)** — that is the upgrade seam.
     Tracked as a standalone UX task; design spec authored by Matt in `docs/product/design/`.
2. **ETA calibration approach.** How `eta_seconds` (§9) is computed once it ships. Until a
   calibration approach exists, the field is omitted. ETA is never a contract regardless.
   *Moot for v0.1:* the synchronous indicator surfaces no ETA at all (entry 1).
3. **Durable store for the checkpoint.** The persistence mechanism backing the `202`+poll
   intermediate result (§8) is not yet chosen.
4. **East-west security mechanism.** The concrete authentication mechanism for internal
   service-to-service traffic (§11) is deferred until an east-west boundary exists. The
   no-implicit-trust principle binds now.
5. **Violations-JSON schema.** The concrete schema of the JSON "violations" representation
   (§10) and of the `details` field for domain validation (§3) is **owned by Graeme** and
   awaits his definition. No domain-content schema activates without Graeme's sign-off.
   - *Home (Graeme consult, 2026-06-09):* the schema is authored by **Graeme** (on founder
     approval) at `docs/knowledge/geotechnical/report-writing/violations-json-schema.md`.
     That doc is the single source of truth for the domain content; this standard references
     it and does **not** restate it.
   - *Ownership boundary (verbatim):* "Peter owns the container (transport envelope,
     JSON-in-details, HTTP semantics, structural shape); Graeme owns the content (domain
     fields, severity vocabulary, taxonomy-node binding, standards-citation requirement). No
     violations-content schema activates without Graeme's sign-off."
   - *Domain constraints the schema must satisfy (Graeme):* every violation carries a
     mandatory **`taxonomy_node`** drawn from the canonical **10-node taxonomy**
     (`docs/knowledge/geotechnical/report-writing/checklist-taxonomy-cross-jurisdiction.md`,
     per ADR-007) — no free text; any cited clause is a **reference into the Standards
     Registry** (`docs/concepts/02-standards-registry/standards-registry.md`, per
     ADR-008/006), **never LLM-authored text** (Principle VIII) — the LLM may *propose*, a
     deterministic post-step confirms against the registry; **`severity`** (`high|medium|low`)
     and **`depth_level`** are **orthogonal and both required**, per the ADR-007 rule
     dimension model.
   - *Open OOXML gap (owned by Peter / Kabilan, not Graeme):* **location-anchoring** — how a
     violation anchors to a span in the `.docx` so a Word comment attaches — is an open
     Office Open XML design question and is **not** a domain decision.
6. **FastAPI bindings.** Framework-specific realisations (global exception handler wiring,
   streaming response, SSE channel) are pending the #78 tech-stack session.

## References

- [ADR-018 — External HTTP API Contract Conventions](../../adr/adr-018-external-http-api-contract-conventions.md)
  (the decision and rationale behind every clause here)
- ADR-001 — Single Source of Truth (the ADR/doc split this document observes)
- ADR-017 — Interface Volatility by Default (tiering and deferral logic)
- RFC 9110, *HTTP Semantics* — methods, status codes, `422`, `WWW-Authenticate`:
  https://www.rfc-editor.org/rfc/rfc9110
- RFC 9457, *Problem Details for HTTP APIs* — error-envelope shape:
  https://www.rfc-editor.org/rfc/rfc9457
- Server-Sent Events (WHATWG HTML, `text/event-stream`):
  https://html.spec.whatwg.org/multipage/server-sent-events.html
- OpenAPI Specification 3.x: https://spec.openapis.org/oas/latest.html
- Google Cloud Run request timeout: https://cloud.google.com/run/docs/configuring/request-timeout
- Google Cloud IAP signed identity headers: https://cloud.google.com/iap/docs/signed-headers-howto
- Office Open XML `.docx` MIME type (Office.js / OOXML):
  https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/working-with-the-shared-string-table
- NotebookLM: *Web API Design* (resource modelling, content negotiation, versioning)
- NotebookLM: *FastAPI Implementation* (validation defaults, exception handling, streaming)
- NotebookLM: *AI System Engineering* (event vocabulary, async lifecycle, observability)
