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

## Grounding Sources (to be queried via `redline-research`)

- *Team Topologies* (Skelton & Pais) — team API design, fracture planes
- *Accelerate* (Forsgren, Humble & Kim) — loosely coupled architecture, deployment independence
- *Modern Software Engineering* (Farley) — incremental design, YAGNI
- *Staff Engineer* (Larson) — architect's approach to technical direction
- *XP Explained* (Beck) — tests over specifications

## Status

**Pending notebook grounding.** This skill requires queries to the Software Development Methodology & Engineering Organisation notebook and the Software Architecture & Domain-Driven Design notebook before the content can be fully elaborated. The structure above defines what the skill must cover; the notebook grounding will provide the specific principles, patterns, and anti-patterns.

## Who Uses This Skill

Peter (primary). Engineering agents may reference for architectural context.
