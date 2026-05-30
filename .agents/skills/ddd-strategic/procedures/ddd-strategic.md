# Ddd Strategic — Detailed Reference

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

# Strategic DDD

## Overview

Strategic DDD decides **where** to invest modelling effort and **how** bounded contexts relate. Tactical DDD (`python-domain-modeling`) decides how to implement within a context. This skill covers the strategic layer.

**Core principle:** The domain model must reflect the team's current understanding. When the language changes, the code changes. No exceptions.

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

## Grounding Sources

Queried via `redline-research` from NotebookLM notebook `c04e18d3-e1e6-47f0-879a-d0e4a65adcb0` (Software Architecture & DDD):

- Evans -- *Domain-Driven Design* (Blue Book)
- Vernon -- *Implementing Domain-Driven Design*
- Khononov -- *Learning Domain-Driven Design*
