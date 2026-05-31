---
name: ddd-strategic
description: Use when classifying subdomains, mapping bounded context relationships, running EventStorming sessions, designing anti-corruption layers, stewarding the ubiquitous language, or governing domain model evolution.
---

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
- System-level architecture beyond DDD (component boundaries, API design) -- use `arch-engineering`
- Deciding what to build (features, PRDs) -- use PM skills

## Quick Reference

| Activity | Procedure | Output |
|---|---|---|
| Classify a subdomain | `procedures/subdomain-classification.md` | Rationale in `domain-model.md` subdomain table |
| Map context relationships | `procedures/context-mapping.md` | Context Map section in `domain-model.md` |
| Run an EventStorming session | `procedures/eventstorming.md` | Miro board + extracted bounded contexts |
| Design an ACL | See ACL Pattern below | ADR + code boundary |
| Steward the UL | See UL Rules below | Updated UL table in `domain-model.md` |


See `procedures/ddd-strategic.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Classifying everything as Core | Core means competitive advantage. If you can buy it, it is not Core. |
| Mapping the desired architecture instead of current reality | Context Maps diagnose; they do not prescribe. Map what exists. |
| Treating the UL as a static glossary | The UL evolves. When it changes, the code must change too. |
| Skipping EventStorming and jumping to aggregates | EventStorming reveals boundaries you cannot see from code alone. |
| Building ACLs everywhere | ACLs have maintenance cost. Use only when protecting Core from corruption. |
| Letting model changes happen without team discussion | Every model change is a team decision. No cowboy refactors. |
