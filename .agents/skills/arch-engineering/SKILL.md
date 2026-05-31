---
name: arch-engineering
description: Use when making system-level design decisions, writing ADRs, defining component boundaries, or reviewing architectural compliance of shaped work and SpecKit output.
---

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

## Quick Reference

| Activity | Output | Stored at |
|---|---|---|
| System design decision | ADR | `docs/adr/` |
| Component boundary definition | Architecture document | `docs/architecture/` |
| Technology selection | ADR | `docs/adr/` |
| Shape work for SpecKit | Shaped Pitch | `specs/shaped/` |
| Touch 2: SpecKit compliance review | Compliance verdict (inline) | — |
| Architectural constraint | Automated test | Tests directory |


## ADR Conventions

ADRs are immutable decision records, not project management tools.

- **Include**: Decision, Status, Context, Options Considered, Rationale, Consequences, References (other ADRs, external docs, RFCs, library docs only).
- **Exclude**: follow-up actions or task checklists (belong in tasks.md); links to specs, plans, or tasks (upward dependencies); scratchpad notes (ephemeral). Embed any relevant research findings directly in the ADR body instead.

See `procedures/engineering-architecture.md` for detailed rules, examples, and extended reference.

## Decision Persistence

After resolving any non-obvious design choice, call `record_decision` (via CCE MCP) immediately - not at session end. This ensures decisions survive context compaction and are available via `session_recall` in future sessions.

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
