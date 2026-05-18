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

## Quick Reference

| Activity | Output | Stored at |
|---|---|---|
| System design decision | ADR | `docs/adr/` |
| Component boundary definition | Architecture document | `docs/architecture/` |
| Technology selection | ADR | `docs/adr/` |
| Shape work for SpecKit | Shaped Pitch | `specs/shaped/` |
| Touch 2: SpecKit compliance review | Compliance verdict (inline) | — |
| Architectural constraint | Automated test | Tests directory |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Expressing architectural constraints as prose rules | Every constraint must be an automated test. If it cannot be tested, it is opinion, not architecture. |
| Reviewing Matt's design specs (Touch 1.5) | Review only SpecKit output at Touch 2; never touch Matt's design artifacts between Touch 1 and Touch 2. |
| Selecting technology before defining component boundaries | Define boundaries and APIs first; technology selection follows. |
| Writing detailed specifications | Write shaped Pitches (breadboard level); SpecKit's `specify` agent writes the spec. |
| Applying general principles without Redline context | Filter every notebook-sourced principle through current stage, kill criteria, and cost envelope before stating it. |
| Confusing strategic DDD decisions with system architecture | Subdomain classification and context mapping belong in `ddd-strategic`, not here. |

## Grounding Sources (queried via `redline-research`)

- *Team Topologies* (Skelton & Pais) — team API design, fracture planes
- *Accelerate* (Forsgren, Humble & Kim) — loosely coupled architecture, deployment independence
- *Modern Software Engineering* (Farley) — incremental design, YAGNI
- *Staff Engineer* (Larson) — architect's approach to technical direction
- *XP Explained* (Beck) — tests over specifications

## Strategic DDD

For strategic DDD decisions that inform architectural boundaries, use the `ddd-strategic` skill:

- **Subdomain classification** determines investment level per component -- `ddd-strategic` `procedures/subdomain-classification.md`
- **Context mapping** reveals integration relationships between components -- `ddd-strategic` `procedures/context-mapping.md`
- **EventStorming** discovers bounded context boundaries from domain events -- `ddd-strategic` `procedures/eventstorming.md`
- **ACL pattern** protects Core domains from upstream corruption -- `ddd-strategic` ACL Pattern section

These feed directly into ADR decisions and component boundary design.
