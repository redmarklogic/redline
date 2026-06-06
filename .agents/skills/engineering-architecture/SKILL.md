---
name: engineering-architecture
description: Use when making system-level design decisions, writing ADRs, defining component boundaries, or reviewing architectural compliance of shaped work and SpecKit output.
---

# Engineering Architecture

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
- Strategic DDD decisions (subdomain classification, context mapping, EventStorming) — use `ddd-strategic`
- Tactical DDD implementation (Pydantic, value objects) — use `python-domain-modeling`
- Evaluation architecture (rubric design, LLM-as-judge) — use `evaluation-architecture`

## Strategic DDD

For strategic DDD decisions that inform architectural boundaries, use the `ddd-strategic` skill:

- **Subdomain classification** determines investment level per component — `ddd-strategic` `procedures/subdomain-classification.md`
- **Context mapping** reveals integration relationships between components — `ddd-strategic` `procedures/context-mapping.md`
- **EventStorming** discovers bounded context boundaries from domain events — `ddd-strategic` `procedures/eventstorming.md`
- **ACL pattern** protects Core domains from upstream corruption — `ddd-strategic` ACL Pattern section

These feed directly into ADR decisions and component boundary design.

## Status

**Partially grounded.** Strategic DDD content (Gaps 1-6) has been extracted from the Software Architecture & DDD notebook (`c04e18d3-e1e6-47f0-879a-d0e4a65adcb0`) and placed in the `ddd-strategic` skill. System-level architecture content (Team Topologies fracture planes, Accelerate loosely coupled architecture, component boundary principles) still requires notebook grounding from the Software Development Methodology & Engineering Organisation notebook (`cdb5e862-443d-4bb5-b24d-1393cacb5906`).
