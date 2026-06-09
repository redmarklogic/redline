---
name: create-adr
description: Use when writing a new ADR, extending an existing ADR, or reviewing an ADR for structural and link-graph compliance. Contains the canonical ADR template and all content rules — single source of truth for ADR authoring.
---

# create-adr

## Boundary Contract

**Applies To:** New ADR authoring, ADR amendments, ADR link-graph compliance reviews.

**Produces:** A structurally valid ADR file in `docs/adr/`, with all outbound links conforming to the dependency DAG rule.

**Does Not Cover:** System-level design decisions that precede ADR writing — load `engineering-architecture` for that work.

---

## Principles

Immutable invariants. All ADRs must satisfy all four.

**1. Temporal Integrity.** An ADR must be intelligible in isolation, at any point in the future, without accessing external systems. Every dependency that matters must be captured inline or referenced to a permanent anchor (another ADR, or a versioned external standard).

**2. Persistence Boundary.** A live link in an ADR must point to something that persists as long as the ADR does. The ADR persistence boundary is `docs/adr/`. Sibling ADRs are permanent. External standards (RFCs, W3C specs, OpenAPI spec) are permanent enough. GitHub issues, Linear cards, Jira tickets, and internal documents outside `docs/adr/` are not. This prohibition applies to all prose sections, not just `## References`.

**3. Substance Over Pointer.** When an ADR records an open decision, constraint, or deferred question, it must state the substance inline — not merely cite the tracking artefact. The tracking artefact is optional and supplementary; the substance is mandatory. This applies equally to deferred decisions and to live-but-unresolved constraints.

**4. Immutability.** ADRs are immutable once accepted. Do not amend the body to reflect post-decision events. Create a new ADR that supersedes the prior one. The single permitted exception: updating `## Status` to `Superseded by ADR-NNN — YYYY-MM-DD` when a new ADR supersedes this one.

---

## Guidelines

### Permitted and prohibited references

| Reference type | Permitted | Form |
|---|---|---|
| Sibling ADR in `docs/adr/` | Yes | Markdown link |
| External standard (RFC, W3C, OpenAPI spec) | Yes | URL in `## References` |
| Internal document outside `docs/adr/` | Concept or title mention only | No path strings of any form — not markdown links, not backtick-wrapped paths, not plain-text paths |
| GitHub issue / PR number (`#NNN`) | No | — |
| GitHub Projects board item | No | — |
| Linear / Jira / Asana card | No | — |
| Slack permalink | No | — |
| Markdown path link to `docs/architecture/`, `specs/`, etc. | No | — |

When referring to an internal document, name the concept or document title in prose — never its path. Path strings are prohibited in all forms: markdown links, backtick-wrapped paths, and plain-text paths. A folder path is worse than a file path because it forces the reader to enumerate the directory.

*Wrong (backtick path):* "See the competitor profile in `docs/research/competitors/`."
*Wrong (markdown link):* "See the [competitor profile](../../docs/research/competitors/index.md)."
*Right (concept-level prose):* "See the competitor profile in the research knowledge base."

The prohibition applies to all prose sections, not just `## References`. The reason: both forms create a false snapshot contract — the document at that path evolves after the ADR is accepted, but the ADR does not.

### Recording open decisions — two patterns

**Pattern A: Deferred decision** — when the decision is held pending an unresolved question:

*Prohibited:*
> The auth decision is deferred (see issue #73).

*Required:*
> The bearer-token carrier is established. The identity provider and token format are deferred until an SSO provider is selected. Once resolved, the auth carrier defined in this ADR must be revisited.

Structure: `[what is deferred] is deferred because [constraint]. It resolves when [trigger].`

**Pattern B: Live-but-unresolved constraint** — when a constraint is known but the mechanism is not yet decided:

*Prohibited:*
> The format is constrained by #78.

*Required:*
> The concrete mechanism is deferred pending the tech-stack decision. The constraint it must satisfy is: [constraint statement]. This constraint is revisited in the same commit that closes the open decision.

A bare `#NNN` reference as the sole expression of a constraint is always a violation of Principle 3.

### Status value progression

| Status | Meaning | Transition rule |
|---|---|---|
| `Proposed` | Draft — under review, not yet binding | Author sets on creation |
| `Accepted` | Decision recorded and binding on the codebase | Set when the founder approves |
| `Deprecated` | Decision no longer applies; no successor exists | Use when the constraint is lifted and the context has dissolved |
| `Superseded by ADR-NNN — YYYY-MM-DD` | A newer ADR replaces this one | Set this AND create the successor ADR in the same commit |

`Proposed → Accepted` is the normal path. `Accepted → Superseded` requires a new ADR authored in the same commit. `Accepted → Deprecated` is used only when there is no replacement decision and the constraint is fully lifted.

### What to exclude

- Follow-up actions — belong in tasks, not ADRs.
- Links to specs, plans, or shaped pitches — they sit above ADRs in the hierarchy and must not be referenced from here.
- Scratchpad notes — ephemeral.
- GitHub issue numbers, board items, or any project-management artefact.
- Markdown path links to documents outside `docs/adr/`.

---

## ADR Dependency DAG Rule

ADRs form a directed acyclic graph (DAG). Correct dependency direction:

```
Constitution ADRs (e.g., ADR-001)
    ↓
Domain ADRs (e.g., ADR-018)
    ↓
Operational standards (docs/architecture/, docs/infrastructure/, etc.)
```

**Definitions.** A *constitution ADR* establishes a cross-cutting invariant that all other ADRs derive from (e.g., ADR-001). A *domain ADR* records a specific implementation decision that derives from one or more constitution ADRs.

**Link rules:**

1. An ADR may reference another ADR only at an equal or higher constitutional level (upward or lateral-without-back-reference).
2. An ADR must not reference documents outside `docs/adr/` by path in any form — not markdown links, not backtick-wrapped paths, not plain-text paths. Concept or title mention in prose is permitted; any path string is not.
3. Operational standards may include a single "Grounding decision: ADR-NNN" pointer. The reverse — an ADR linking by path to its derived operational document — is a DAG violation.
4. Constitution ADRs must not name individual domain ADRs by file reference. Extract any such registry to a separate non-ADR file.

**Two violation patterns to avoid:**

- **Cycle:** ADR-A references ADR-B; ADR-B references ADR-A.
- **Downward cross-boundary link:** ADR-018 links by path to `docs/architecture/api/http-api-standard.md`, which back-references ADR-018.

---

## Pre-Flight Checklist

Scan **all prose sections** — not just `## References` — before saving or committing.

- [ ] No bare `#NNN` GitHub issue or PR references anywhere in the document.
- [ ] No markdown path links to documents outside `docs/adr/` anywhere in the document.
- [ ] No backtick-wrapped strings containing `/` that point outside `docs/adr/` (regex: `` `[^`]*/[^`]*` `` where the path does not begin with `docs/adr/`). Plain-text paths are equally prohibited.
- [ ] No referenced peer ADR back-references this ADR (check both directions).
- [ ] No follow-up action lists, scratchpad notes, or project-management artefacts in any section.
- [ ] If this is a constitution-level ADR: no individual domain ADR is named by file reference.
- [ ] If this ADR supersedes or amends another: the superseded ADR's `## Status` is updated in the same commit.
- [ ] Every open decision or deferred question states the substance inline (not just a ticket pointer).

---

## Template

Copy verbatim for every new ADR. Save to `docs/adr/adr-NNN-short-title.md`.

```markdown
# ADR-NNN: Title

## Summary

One paragraph (3–5 sentences): restate the decision in plain language, its current status,
and the single most important constraint it imposes. Written so an agent or tool can
determine whether this ADR is relevant to a question without reading the full document.

## Decision

Describe the architectural choice in one or two sentences.

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-NNN] — YYYY-MM-DD

## Context

Summarise the forces leading to this decision. Capture relevant background, constraints,
and objectives.

## Options Considered

- Option A
- Option B
- Option C

## Decision Rationale

Explain why the selected option best meets the context, considering trade-offs and rejected
alternatives.

## Consequences

Detail the positive and negative outcomes expected from this decision.

## References

List sibling ADRs and external standards (RFCs, W3C specs) that informed this decision.
Internal documents may be named by concept or title in prose. No path strings of any form — not markdown links, not backtick-wrapped paths, not plain text.
No GitHub issue numbers or project-management artefacts.
```

---

## Cross-Reference

Load `engineering-architecture` when the system-level design decision has not yet been made. `create-adr` governs the writing and link-graph compliance of the record itself, not the upstream design work.

After an ADR is accepted, determine whether `.specify/memory/constitution.md` needs updating — consult the `adr-constitution-sync` skill if available in the current skills registry.
