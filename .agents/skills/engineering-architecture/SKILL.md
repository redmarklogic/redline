---
name: engineering-architecture
description: Use when making system-level design decisions, writing ADRs, defining component boundaries, or reviewing architectural compliance of shaped work and SpecKit output.
---

# Engineering Architecture

## Purpose

System-level design decisions, ADR writing, and architectural constraint expression for Redline's AI-assisted geotechnical document quality platform.

## Boundary Contract

### Applies To
- System-level design decisions (component boundaries, service interfaces, API design)
- ADR writing and maintenance
- Technology selection within Redline constraints
- Architectural compliance review of SpecKit output (Touch 2)

### Produces
- ADRs in `docs/adr/`
- Architecture documents in `docs/architecture/`
- Shaped Pitches in `specs/shaped/`
- Architectural constraint tests

### Does Not Cover
- Strategic DDD decisions (subdomain classification, context mapping, EventStorming) -- use `ddd-strategic`
- Tactical DDD implementation (Pydantic, value objects) -- use `python-domain-modeling`
- Evaluation architecture (rubric design, LLM-as-judge) -- use `evaluation-architecture`

## What This Skill Covers

- System-level design decisions: component boundaries, service interfaces, API design
- ADR writing process: when to write an ADR, ADR structure, decision criteria documentation
- Technology selection framework: evaluating options against Redline's constraints (single-team startup, AI-agent development model, geotechnical domain)
- Component boundary principles grounded in Team Topologies (fracture planes) and Accelerate (loosely coupled architecture)
- Architectural constraint expression as tests (Beck's "write a failing test")
- Shaped Pitch to SpecKit plan review for architectural compliance

## Key Principle

"Every architectural constraint must be expressible as a test. If it cannot be tested, it is opinion, not architecture." (XP Explained, adapted)

## Grounding Sources (to be queried via `redline-research`)

- *Team Topologies* (Skelton & Pais) — team API design, fracture planes
- *Accelerate* (Forsgren, Humble & Kim) — loosely coupled architecture, deployment independence
- *Modern Software Engineering* (Farley) — incremental design, YAGNI
- *Staff Engineer* (Larson) — architect's approach to technical direction
- *XP Explained* (Beck) — tests over specifications

## Status

**Partially grounded.** Strategic DDD content (Gaps 1-6) has been extracted from the Software Architecture & DDD notebook (`c04e18d3-e1e6-47f0-879a-d0e4a65adcb0`) and placed in the `ddd-strategic` skill. System-level architecture content (Team Topologies fracture planes, Accelerate loosely coupled architecture, component boundary principles) still requires notebook grounding from the Software Development Methodology & Engineering Organisation notebook (`cdb5e862-443d-4bb5-b24d-1393cacb5906`).

## Strategic DDD

For strategic DDD decisions that inform architectural boundaries, use the `ddd-strategic` skill:

- **Subdomain classification** determines investment level per component -- `ddd-strategic` `procedures/subdomain-classification.md`
- **Context mapping** reveals integration relationships between components -- `ddd-strategic` `procedures/context-mapping.md`
- **EventStorming** discovers bounded context boundaries from domain events -- `ddd-strategic` `procedures/eventstorming.md`
- **ACL pattern** protects Core domains from upstream corruption -- `ddd-strategic` ACL Pattern section

These feed directly into ADR decisions and component boundary design.
