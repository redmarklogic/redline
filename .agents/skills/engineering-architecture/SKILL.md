---
name: engineering-architecture
description: Use when making system-level design decisions, defining component boundaries, or reviewing architectural compliance of shaped work and SpecKit output.
---

# Engineering Architecture

## Boundary Contract

### Applies To
- System-level design decisions (component boundaries, service interfaces, API design)
- Technology selection within Redline constraints
- Architectural compliance review of SpecKit output (Touch 2)

### Does Not Apply To (load the specialised skill instead)
- ADR structure, link-graph compliance, DAG rule, Status progression — see the ADR authoring skill

### Produces
- ADRs in `docs/adr/`
- Architecture documents in `docs/architecture/`
- Shaped Pitches in `specs/shaped/`
- Architectural constraint tests

### Does Not Cover
- Strategic DDD decisions (subdomain classification, context mapping, EventStorming) — use `ddd-strategic`
- Tactical DDD implementation (Pydantic, value objects) — use `python-domain-modeling`
- Evaluation architecture (rubric design, LLM-as-judge) — use `design-eval-rubric` / `design-eval-pipeline`

## Strategic DDD

For strategic DDD decisions that inform architectural boundaries, use the `ddd-strategic` skill:

- **Subdomain classification** determines investment level per component — `ddd-strategic` `procedures/subdomain-classification.md`
- **Context mapping** reveals integration relationships between components — `ddd-strategic` `procedures/context-mapping.md`
- **EventStorming** discovers bounded context boundaries from domain events — `ddd-strategic` `procedures/eventstorming.md`
- **ACL pattern** protects Core domains from upstream corruption — `ddd-strategic` ACL Pattern section

These feed directly into ADR decisions and component boundary design.

## Decision Persistence

After resolving any non-obvious design choice, call `record_decision` (via CCE MCP) immediately - not at session end. This ensures decisions survive context compaction and are available via `session_recall` in future sessions.

## Grounding Sources (queried via `redline-research`)

- *Team Topologies* (Skelton & Pais) — team API design, fracture planes
- *Accelerate* (Forsgren, Humble & Kim) — loosely coupled architecture, deployment independence
- *Modern Software Engineering* (Farley) — incremental design, YAGNI
- *Staff Engineer* (Larson) — architect's approach to technical direction
- *XP Explained* (Beck) — tests over specifications

## Common Mistakes

| Mistake | Fix |
|---|---|
| Expressing architectural constraints as prose rules | Every constraint must be an automated test. If it cannot be tested, it is opinion, not architecture. |
| Resolving a design choice without persisting it | Call `record_decision` immediately after the choice is made, not at session end. |
| Reviewing the UI/UX Designer's design specs (Touch 1.5) | Review only SpecKit output at Touch 2; never touch the UI/UX Designer's design artifacts between Touch 1 and Touch 2. |
| Selecting technology before defining component boundaries | Define boundaries and APIs first; technology selection follows. |
| Writing detailed specifications | Write shaped Pitches (breadboard level); SpecKit's `specify` agent writes the spec. |
| Applying general principles without Redline context | Filter every notebook-sourced principle through current stage, kill criteria, and cost envelope before stating it. |
| Confusing strategic DDD decisions with system architecture | Subdomain classification and context mapping belong in `ddd-strategic`, not here. |

## Status

**Partially grounded.** Strategic DDD content (Gaps 1-6) has been extracted from the Software Architecture & DDD notebook (`c04e18d3-e1e6-47f0-879a-d0e4a65adcb0`) and placed in the `ddd-strategic` skill. System-level architecture content (Team Topologies fracture planes, Accelerate loosely coupled architecture, component boundary principles) still requires notebook grounding from the Software Development Methodology & Engineering Organisation notebook (`91568710-98b3-4448-b038-04f9b48b7111`; the previously cited ID returned NOT_FOUND on live query, 2026-06-10 sync).
