# Engineering Architecture — Detailed Reference

## Strategic DDD

For strategic DDD decisions that inform architectural boundaries, use the `ddd-strategic` skill:

- **Subdomain classification** determines investment level per component -- `ddd-strategic` `procedures/subdomain-classification.md`
- **Context mapping** reveals integration relationships between components -- `ddd-strategic` `procedures/context-mapping.md`
- **EventStorming** discovers bounded context boundaries from domain events -- `ddd-strategic` `procedures/eventstorming.md`
- **ACL pattern** protects Core domains from upstream corruption -- `ddd-strategic` ACL Pattern section

These feed directly into ADR decisions and component boundary design.

# Engineering Architecture

## Purpose

System-level design decisions, ADR writing, and architectural constraint expression for Redline's AI-assisted geotechnical document quality platform.

## What This Skill Covers

- System-level design decisions: component boundaries, service interfaces, API design
- ADR writing process: when to write an ADR, ADR structure, decision criteria documentation
- Technology selection framework: evaluating options against Redline's constraints (single-team startup, AI-agent development model, geotechnical domain)
- Component boundary principles grounded in Team Topologies (fracture planes) and Accelerate (loosely coupled architecture)
- Architectural constraint expression as tests (Beck's "write a failing test")
- Shaped Pitch to SpecKit plan review for architectural compliance

## Key Principle

"Every architectural constraint must be expressible as a test. If it cannot be tested, it is opinion, not architecture." (XP Explained, adapted)

## Grounding Sources (queried via `redline-research`)

- *Team Topologies* (Skelton & Pais) — team API design, fracture planes
- *Accelerate* (Forsgren, Humble & Kim) — loosely coupled architecture, deployment independence
- *Modern Software Engineering* (Farley) — incremental design, YAGNI
- *Staff Engineer* (Larson) — architect's approach to technical direction
- *XP Explained* (Beck) — tests over specifications
