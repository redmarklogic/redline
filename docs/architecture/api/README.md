# API Standards Home

This directory is the Single Source of Truth (SSOT) for Redline's API conventions — the
**operational** rules that agents, reviewers, and code follow when building or reviewing
an API surface. The *decisions and rationale* behind these rules live in the relevant
Architecture Decision Records (ADRs) in `docs/adr/`; the documents here state the *current
operational rule* and link back to the ADR for the "why". They cross-link and never copy
(ADR-001, Single Source of Truth).

## What lives here

| Document | Status | Grounding ADR | Scope |
|----------|--------|---------------|-------|
| [`http-api-standard.md`](./http-api-standard.md) | **In force** | ADR-018 | External (north-south) HTTP API conventions: URIs, methods, status codes, error envelope, content negotiation, binary responses, auth pattern, async (`202`+poll) and Server-Sent Events (SSE) progress. |
| [`mcp-standard.md`](./mcp-standard.md) | **Target — dormant (not in force)** | ADR-018 (records the deferred tensions) | Model Context Protocol (MCP) surface conventions for a future MCP / AI consumer. Activates only when such a consumer arrives. |

## How to use this home

- **Building or reviewing an HTTP endpoint?** Follow `http-api-standard.md`. It is the
  live operational document — every clause is in force for v0.1.
- **Wondering *why* a rule is what it is?** Each clause links to ADR-018. The ADR carries
  the rationale, the options rejected, and the consequences. This directory does not
  repeat that reasoning.
- **Building an MCP tool?** That surface is not in force yet. `mcp-standard.md` records the
  target so the HTTP conventions do not foreclose it. Do not treat it as binding until an
  MCP consumer exists.

## Definitions used across this home

- **North-south traffic** — requests that cross the system's outer boundary: a caller
  outside the monorepo (a browser, an external integration, an AI agent) talking to a
  Redline service. These are the *external* surfaces.
- **East-west traffic** — requests between Redline's own internal services. Redline
  currently runs as a *single* Cloud Run service, so there is no east-west HTTP today; the
  internal tier is empty (see the trust-boundary clause in `http-api-standard.md`).
- **SSOT (Single Source of Truth)** — for each concern there is exactly one authoritative
  location; everything else links to it rather than copying it (ADR-001).

## Maintenance

These documents are versioned alongside the code and concern they describe. When a clause
changes, update the document here and, if the *decision* changes, record it in a new or
amended ADR — never change the rule in only one of the two places.
