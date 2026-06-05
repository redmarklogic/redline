# Implementation Plan: [FEATURE]

**Date**: [DATE] | **Spec**: [link or "see above"]
**Status**: Draft

## Summary

[One paragraph: what we are building and the technical approach]

## Technical Context

**Language**: Python 3.12
**Package manager**: uv
**Testing**: pytest (TDD workflow per `test-driven-development` skill)
**Architecture**: Layered (domain > enrichment > schemas > functions > calculators)
**Dev OS**: Windows | **Deploy OS**: Linux
**Domain modeling**: Pydantic BaseModel, Pandera DataFrameModel
**Layer enforcement**: import-linter contracts in `pyproject.toml` (see `.agents/skills/spec-kit/references/import-linter.md`)
**Key dependencies**: [e.g., pandas, openpyxl, pydantic]

## Design Decisions

| #  | Decision            | Choice        | Rationale |
| -- | ------------------- | ------------- | --------- |
| D1 | [What was decided]  | [The choice]  | [Why]     |

## Domain Impact

**New packages**: [None / list with target import-linter contract]
**Bounded context changes**: [None / describe]
**Import-linter contract updates**: [None / show proposed TOML block]
**Subdomain classification**: [Core / Supporting / Generic]
**New domain terms**: [None / term: definition]

<!-- Core = full DDD (aggregates, domain events, rich domain model) -->
<!-- Supporting = simpler patterns (transaction scripts, thin domain layer) -->
<!-- Generic = off-the-shelf libraries, no custom domain model -->

## Architecture

Produce a **Function Pipeline Diagram** showing how functions chain together — inputs,
output types, and data flow from source to sink. See
`.agents/skills/mermaid-diagrams/procedures/function-pipeline-diagram.md` (Phase 1).

Save the diagram as `pipeline-diagram.md` in this spec folder.
Reference it here with a relative link: [pipeline-diagram.md](pipeline-diagram.md)

> **Founder approval gate**: get sign-off on the pipeline shape before proceeding to
> Domain Models. Do not produce the class diagram until the pipeline is approved.

## Domain Models

After the pipeline diagram is approved, produce a **class diagram** detailing the value
object fields, types, and relationships. See
`.agents/skills/mermaid-diagrams/procedures/function-pipeline-diagram.md` (Phase 2).

Save the diagram as `class-diagram.md` in this spec folder.
Reference it here with a relative link: [class-diagram.md](class-diagram.md)

This is the programmer's implementation brief and the code reviewer's compliance
blueprint. The class diagram travels with tasks.md through to code review.

## MoSCoW

| Category                  | Items                                            |
| ------------------------- | ------------------------------------------------ |
| **Must have**             | [Non-negotiable for this release]                |
| **Should have**           | [Important but not critical]                     |
| **Could have**            | [Desirable if time permits]                      |
| **Won't have (this time)** | [Explicitly out of scope for this iteration]    |

## Phased Delivery

### Phase 0: Foundation

**Goal**: [What this phase delivers -- must be runnable working code, not stubs]

**TDD approach**: [Which functions will be written test-first; reference test file paths]

**Deliverables**:

1. [File path -- what it contains]
2. [File path -- what it contains]

**Verification**:

```
[Command to run + what to look for in output]
```

**Acceptance Gate** (both must pass before Phase 1 starts):
- [ ] Working code: the deliverables above run end-to-end without errors
- [ ] If any function file was modified or introduced: run `.venv\Scripts\activate; python -m pytest tests/[affected modules] -v` and confirm green

---

### Phase N: [Name]

**Goal**: [What working code this phase delivers]

**TDD approach**: [Which functions will be written test-first; reference test file paths]

**Deliverables**: [...]

**Verification**:

```
[Command to run + what to look for in output]
```

**Acceptance Gate** (both must pass before next phase starts):
- [ ] Working code: the deliverables above run end-to-end without errors
- [ ] If any function file was modified or introduced: run `.venv\Scripts\activate; python -m pytest tests/[affected modules] -v` and confirm green

## File Inventory

| Phase | New Files | Count |
| ----- | --------- | ----- |
| 0     | [...]     | N     |
| 1     | [...]     | N     |

**Total new**: ~N | **Total deleted**: ~N

## Library Best Practices

<!-- Populated after Context7 MCP review of each key dependency -->

### [package-name]

- **Import path**: [confirmed import]
- **API gotchas**: [removed/renamed kwargs, changed defaults]
- **Confirmed pattern**: [minimal code pattern for this plan's usage]

## Risk Register

| Risk       | Mitigation  |
| ---------- | ----------- |
| [...]      | [...]       |
