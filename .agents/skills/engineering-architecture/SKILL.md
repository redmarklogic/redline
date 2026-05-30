---
name: engineering-architecture
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


See `procedures/engineering-architecture.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Expressing architectural constraints as prose rules | Every constraint must be an automated test. If it cannot be tested, it is opinion, not architecture. |
| Reviewing the UI/UX Designer's design specs (Touch 1.5) | Review only SpecKit output at Touch 2; never touch the UI/UX Designer's design artifacts between Touch 1 and Touch 2. |
| Selecting technology before defining component boundaries | Define boundaries and APIs first; technology selection follows. |
| Writing detailed specifications | Write shaped Pitches (breadboard level); SpecKit's `specify` agent writes the spec. |
| Applying general principles without Redline context | Filter every notebook-sourced principle through current stage, kill criteria, and cost envelope before stating it. |
| Confusing strategic DDD decisions with system architecture | Subdomain classification and context mapping belong in `ddd-strategic`, not here. |
