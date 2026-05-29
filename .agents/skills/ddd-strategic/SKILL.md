---
name: ddd-strategic
description: Use when classifying subdomains, mapping bounded context relationships, running EventStorming sessions, designing anti-corruption layers, stewarding the ubiquitous language, or governing domain model evolution.
---

# Strategic DDD

## Overview

Strategic DDD decides **where** to invest modelling effort and **how** bounded contexts relate. Tactical DDD (`python-domain-modeling`) decides how to implement within a context. This skill covers the strategic layer.

**Core principle:** The domain model must reflect the team's current understanding. When the language changes, the code changes. No exceptions.

## Boundary Contract

### Applies To
- Subdomain classification decisions
- Bounded context boundary identification
- Context mapping between bounded contexts
- EventStorming facilitation (adapted for solo founder + AI agents)
- Anti-corruption layer design decisions
- Ubiquitous language stewardship
- Domain model evolution governance

### Produces
- Updated `docs/architecture/domain-model.md` sections (living project state)
- ADRs for significant boundary or classification changes (`docs/adr/`)
- Miro EventStorming boards (via `miro-mcp`)
- Context Map diagrams (Mermaid flowchart in architecture docs)

### Does Not Cover
- Tactical DDD implementation (Pydantic, Pandera, value objects) -- use `python-domain-modeling`
- System-level architecture beyond DDD (component boundaries, API design) -- use `engineering-architecture`
- Deciding what to build (features, PRDs) -- use PM skills

## Quick Reference

| Activity | Procedure | Output |
|---|---|---|
| Classify a subdomain | `procedures/subdomain-classification.md` | Rationale in `domain-model.md` subdomain table |
| Map context relationships | `procedures/context-mapping.md` | Context Map section in `domain-model.md` |
| Run an EventStorming session | `procedures/eventstorming.md` | Miro board + extracted bounded contexts |
| Design an ACL | See ACL Pattern below | ADR + code boundary |
| Steward the UL | See UL Rules below | Updated UL table in `domain-model.md` |

## Subdomain Classification

Three types. Every subdomain in `domain-model.md` must have a documented rationale.

| Type | Competitive advantage? | Complexity | Volatility | Build or buy? |
|---|---|---|---|---|
| **Core** | Yes -- differentiator | High | High | Build in-house |
| **Supporting** | No edge, but needed | Moderate | Moderate | Build (simple) or buy |
| **Generic** | Commodity | Low-moderate | Low (stable) | Buy off-the-shelf |

Classification criteria: competitive advantage, complexity, change frequency, buyability.

**Full procedure:** `procedures/subdomain-classification.md`

## Context Mapping

Eight relationship types between bounded contexts:

| Relationship | When to use |
|---|---|
| Partnership | Two contexts succeed or fail together |
| Shared Kernel | Small shared model subset; changes need both sides to agree |
| Customer-Supplier | Downstream has input on upstream priorities |
| Conformist | Downstream conforms without influence |
| Anti-Corruption Layer | Defensive translation; downstream is Core, upstream is messy |
| Open Host Service | Upstream provides a well-defined API |
| Published Language | Shared interchange format (JSON schema, protobuf) |
| Separate Ways | No integration; contexts operate independently |

**Key principle:** Map the current reality first, not the desired state. The Context Map is a diagnostic tool.

**Full procedure:** `procedures/context-mapping.md`

## Anti-Corruption Layer (ACL) Pattern

A defensive translation layer between bounded contexts. Use when the downstream context is Core and the upstream model is messy, legacy, or third-party.

**Components:**
- **Facade:** Simplified interface hiding upstream complexity
- **Adapter:** Protocol translation (HTTP to domain calls, etc.)
- **Translator:** Model mapping (upstream types to downstream domain types)

**Rule:** The ACL belongs to the downstream context. Never let external models leak into the Core domain.

**When to use ACL vs. Conformist:** If the upstream model would corrupt your Core domain vocabulary, build an ACL. If the upstream model is acceptable and stable, Conformist is cheaper.

## Ubiquitous Language Rules

1. The UL is a **team** effort, not a glossary maintained by one person.
2. Language changes MUST trigger code refactors -- the code is an enduring expression of the model.
3. Code and speech are the two enduring expressions; documents go stale.
4. Every class, method, and variable name must reflect the UL.
5. When the team discovers a better term, the code changes immediately.
6. New terms are recorded in the UL table in `docs/architecture/domain-model.md`.
7. UL is scoped per bounded context -- the same real-world concept may have different names in different contexts.

## Model Evolution Governance

1. The domain model must constantly adapt as understanding deepens.
2. Language changes require team decision (not unilateral).
3. Keep model and code synchronised -- CI at both levels.
4. Tactical evolution patterns:
   - **Value Objects:** Replace entirely (immutable by design).
   - **Entities:** Update attributes, maintain identity.
   - **Aggregates:** Keep small. One transaction per aggregate. Eventual consistency between aggregates.
5. When a model change affects multiple bounded contexts, update the Context Map first, then propagate.

## EventStorming

A collaborative workshop technique for discovering domain events, commands, and bounded context boundaries. Adapted for solo founder + AI agents: the Principal Engineer facilitates, the Domain Expert provides domain facts, the Product Manager validates problem framing.

**Full procedure:** `procedures/eventstorming.md`

**Tooling:** EventStorming outputs go to Miro (via `miro-mcp` `layout_create`), never to Mermaid. See colour mapping in the procedure.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Classifying everything as Core | Core means competitive advantage. If you can buy it, it is not Core. |
| Mapping the desired architecture instead of current reality | Context Maps diagnose; they do not prescribe. Map what exists. |
| Treating the UL as a static glossary | The UL evolves. When it changes, the code must change too. |
| Skipping EventStorming and jumping to aggregates | EventStorming reveals boundaries you cannot see from code alone. |
| Building ACLs everywhere | ACLs have maintenance cost. Use only when protecting Core from corruption. |
| Letting model changes happen without team discussion | Every model change is a team decision. No cowboy refactors. |

## Grounding Sources

Queried via `redline-research` from NotebookLM notebook `c04e18d3-e1e6-47f0-879a-d0e4a65adcb0` (Software Architecture & DDD):

- Evans -- *Domain-Driven Design* (Blue Book)
- Vernon -- *Implementing Domain-Driven Design*
- Khononov -- *Learning Domain-Driven Design*
