# MCP Standard

> **TARGET — NOT IN FORCE.** This document records the conventions a future Model Context
> Protocol (MCP) surface will follow. It **activates only when an MCP / AI consumer
> arrives**. Until then it is dormant: nothing here is binding, and no current endpoint is
> obliged to satisfy it. Its purpose now is to record the deferred tensions so the live
> HTTP standard (`http-api-standard.md`) does not foreclose them.

**Status:** Target — dormant (not in force)
**Grounding decision:** [ADR-018 — External HTTP API Contract Conventions](../../adr/adr-018-external-http-api-contract-conventions.md)
(records why these tensions are deferred)
**Activates when:** an MCP-based or AI consumer of Redline's generation capability is
introduced.

### What is MCP? (for the uninitiated)

The Model Context Protocol (MCP) is an open protocol that lets an AI application (the
"host", e.g. an LLM-based assistant) connect to external systems that expose **Tools**
(actions the AI can invoke) and **Resources** (data the AI can read). Redline would act as
an MCP *server*, exposing its generation capability to AI consumers.

---

## Deferred tensions recorded now

These are the points where an MCP surface would differ from, or constrain, the live HTTP
standard. They are recorded so the HTTP conventions stay compatible with a future MCP
surface.

### 1. Authentication — OAuth 2.1 with mandatory PKCE, no token passthrough

- The MCP surface authenticates with **OAuth 2.1**, and **PKCE (Proof Key for Code
  Exchange) is mandatory**.
- **No token passthrough.** The MCP server MUST NOT accept a token issued for a different
  audience and forward it onward. Each surface validates tokens issued for itself.
- This is a *stricter* mechanism than the live HTTP standard's format-agnostic bearer
  pattern (§7 of `http-api-standard.md`). The HTTP bearer pattern is chosen specifically so
  that an OAuth 2.1 bearer token is a valid carrier — the HTTP standard does not foreclose
  this.

### 2. Tool vs Resource mapping

- **Tool** = the generation *trigger*. Invoking the tool is what asks Redline to generate
  an artifact. This maps to the HTTP `POST /skeletons` trigger.
- **Resource** = the *produced artifact* (the generated `.docx` or its representation). The
  AI consumer reads the resource after the tool runs.

### 3. Resource Links, not inline base64

- The produced artifact is exchanged as a **Resource Link** — a URI the consumer fetches —
  **not** as inline base64 embedded in the tool result.
- This is the **by-reference (file-link) target** already recorded in ADR-018 (decision 8)
  and in the live HTTP standard. The MCP surface is one of the consumers that forces the
  by-reference representation to activate.

### 4. Progress via MCP progress notifications

- Long-running generation reports progress using **MCP progress notifications**, not the
  SSE channel of the HTTP standard.
- These MCP notifications map to **the same internal event vocabulary** (§13 of
  `http-api-standard.md`). The SSE envelope and the MCP progress notification are two
  client-facing *projections* of one internal event model — they do not define separate
  vocabularies.

---

## Relationship to the live HTTP standard

| Concern | Live HTTP standard (in force) | MCP standard (target) |
|---------|-------------------------------|------------------------|
| Auth | Format-agnostic bearer in `Authorization` (§7) | OAuth 2.1 + mandatory PKCE, no passthrough |
| Artifact exchange | Bytes-in-body for v0.1; by-reference is the target (decision 8) | Resource Link (URI), never inline base64 |
| Progress | SSE channel, event envelope (§9) | MCP progress notifications |
| Event model | One internal vocabulary; SSE is a projection (§13) | Same internal vocabulary; MCP notifications are a projection |

The single internal event vocabulary is the shared spine: whichever client-facing channel
is used (SSE for the web client, MCP notifications for an AI consumer), both are
projections of the same source.

## References

- [ADR-018 — External HTTP API Contract Conventions](../../adr/adr-018-external-http-api-contract-conventions.md)
- [`http-api-standard.md`](./http-api-standard.md) — the live, in-force HTTP standard
- Model Context Protocol specification: https://modelcontextprotocol.io/specification
- MCP authorization (OAuth 2.1, PKCE, no token passthrough):
  https://modelcontextprotocol.io/specification/draft/basic/authorization
- OAuth 2.1 (IETF draft): https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1
- RFC 7636, *Proof Key for Code Exchange (PKCE)*: https://www.rfc-editor.org/rfc/rfc7636
- NotebookLM: *AI System Engineering* (tool/resource modelling, event vocabulary)
- NotebookLM: *Web API Design* (by-reference vs inline representation)
