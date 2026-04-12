# Implementation Plan: [FEATURE]

**Date**: [DATE] | **Spec**: [link or "see above"]
**Status**: Draft

## Summary

[One paragraph: what we are building and the technical approach.
Write as if the reader has never seen this codebase before: explain acronyms,
name the affected layers, and state *why* this change matters before *how* it works.]

## Technical Context

**Language**: Python 3.12
**Package manager**: uv
**Testing**: pytest (TDD workflow per `test-driven-development` skill)
**Project layout**: [Read from `.specify/architecture.yml`: `monorepo` or `single-package`]
**Architecture**: [Monorepo: sibling packages under `src/`, each with optional internal layers (domain > schemas > functions). Single-package: layered (domain > schemas > functions). Add project-specific higher layers above `functions` only when needed.]
**Dev OS**: Windows | **Deploy OS**: Linux
**Domain modeling**: Pydantic BaseModel, Pandera DataFrameModel
**Layer enforcement**: import-linter contracts in `pyproject.toml` (see `.agents/skills/spec-kit/references/import-linter.md`)
**Key dependencies**: [e.g., pandas, openpyxl, pydantic]

## Design Decisions

| #  | Decision            | Choice        | Rationale |
| -- | ------------------- | ------------- | --------- |
| D1 | [What was decided]  | [The choice]  | [Why]     |

## Domain Impact

**Modularity assessment**: [Monorepo projects only: new top-level package under `src/`
or subpackage of existing package -- state which signals from the `python-domain-modeling`
decision matrix drove the choice (language boundary, conceptual cohesion, general vs
special, rate of change, future extraction). Single-package projects: N/A]
**New packages**: [None / list with target import-linter contract]
**Bounded context changes**: [None / describe]
**Import-linter contract updates**: [None / show proposed TOML block]
**Subdomain classification**: [Core / Supporting / Generic]
**New domain terms**: [None / term: definition]

<!-- Core = full DDD (aggregates, domain events, rich domain model) -->
<!-- Supporting = simpler patterns (transaction scripts, thin domain layer) -->
<!-- Generic = off-the-shelf libraries, no custom domain model -->

## Architecture

[Data flow diagrams, state machines, layer rules, worksheet schemas --
whatever is needed to make the implementation unambiguous]

## Domain Models

[For each new model: module path, class name, key fields, frozen/mutable.
Code sketches are fine here -- they will become real code in implementation.]

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

## Glossary

<!-- Problem-domain terms only: concepts from the business or analytical domain
     this project is solving (e.g. "skeleton", "GIR", "acceptance criteria").
     Do NOT include technical stack terms (pytest, Pydantic, import-linter, etc.) -->

| Term | Definition |
| ---- | ---------- |
| [term] | [plain-English definition, one sentence max] |
