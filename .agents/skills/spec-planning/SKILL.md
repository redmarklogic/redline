---
name: spec-planning
description: Spec-driven planning for features and pipelines. Converts ideas into structured specs, phased plans, and checkboxable task lists. Adapted from GitHub Spec Kit patterns for this repo's agent-pipeline domain.
---

# Spec-Driven Planning

This skill provides a lightweight, template-driven approach to planning features before writing
code. It produces structured markdown artifacts that are precise enough for an AI agent to
implement from, and clear enough for a human to review.

Adapted from [GitHub Spec Kit](https://github.com/github/spec-kit) patterns, stripped of
framework dependencies and tailored for this repo's domain (CrewAI agent pipelines, Pydantic
models, Excel-based data stores, single-developer workflow).

## What This Skill Can Do

Ask for any of these by name:

| Command     | What You Get                                                               | When to Use                                                 |
| ----------- | -------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **specify** | A feature spec with requirements, acceptance scenarios, entities, and risk | You have an idea but haven't defined what "done" looks like |
| **plan**    | A phased implementation plan with architecture, models, file inventory     | You have a spec and need to decide _how_ to build it        |
| **tasks**   | A checkboxable task list with IDs, parallel markers, and file paths        | You have a plan and need atomic work items to execute       |
| **clarify** | Up to 5 targeted questions about ambiguities in a spec or plan             | A spec has vague areas or `[NEEDS CLARIFICATION]` markers   |
| **analyze** | A read-only consistency report across spec + plan + tasks                  | You want to catch gaps before starting implementation       |

## Context & Guidelines

### Scope

Activate this skill when:

- Planning a new feature, pipeline, or multi-phase project
- Converting a scratchpad/brainstorm into structured deliverables
- Breaking an existing plan into executable tasks
- Reviewing specs for completeness before implementation

### Constraints

- Output location defaults to `docs/specs/<feature-slug>/` directory, but can target `scratchpad.md`
  or any other file if explicitly requested.
- All artifacts are plain markdown -- no tooling dependencies.
- Do not duplicate project principles already captured in `.github/copilot-instructions.md` or
  other skills. Reference them instead.
- Use RFC-2119 language (MUST, SHOULD, MAY) for requirements.
- Never use emoji or unicode that emulates emoji.

### Relationship to Other Skills

- **test-driven-development**: This skill feeds requirements and acceptance criteria _into_ the TDD cycle.
  The spec's Given/When/Then scenarios become the basis for test cases.
- **python-domain-modeling**: Entity definitions in specs should follow the repo's frozen
  BaseModel / StrEnum / Field(alias=...) conventions.
- **python-class-design**: Architectural decisions in plans should respect the repo's
  composition-over-inheritance and single-responsibility principles.

---

## Procedure: `specify`

Generate a feature specification. Focus on _what_ and _why_, not _how_.

### Spec Template

```markdown
# Feature Specification: [FEATURE NAME]

**Branch**: `[branch-name]`
**Created**: [DATE]
**Status**: Draft

## Scenarios (mandatory)

<!-- Prioritize as P1 (MVP), P2, P3. Each scenario must be independently testable. -->

### Scenario 1 -- [Title] (Priority: P1)

[Describe the scenario in plain language]

**Why this priority**: [Value delivered]

**Independent test**: [How to verify this works on its own]

**Acceptance criteria**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### Scenario 2 -- [Title] (Priority: P2)

[...]

---

### Edge Cases

- What happens when [boundary condition]?
- How does the system handle [error scenario]?

## Requirements (mandatory)

### Functional Requirements

- **FR-001**: System MUST [capability]. [Rationale if non-obvious]
- **FR-002**: System MUST [capability].
- **FR-003**: [NEEDS CLARIFICATION: specific question about ambiguity]

<!-- Max 3 NEEDS CLARIFICATION markers. Beyond that, use `/clarify` to resolve. -->

### Key Entities (if data is involved)

- **[Entity]**: [What it represents, key attributes, relationships -- no implementation detail]

## Success Criteria (mandatory)

- **SC-001**: [Measurable outcome, e.g., "Pipeline processes 10 topics end-to-end"]
- **SC-002**: [Measurable outcome]

## Assumptions

- [State the assumption in plain English. Explain _why_ this gap was filled this way
  and what would change if the assumption turned out to be wrong.]

## Risks

| Risk                                                       | Impact                                                                                              | Mitigation         |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------ |
| [Risk description in plain English -- what could go wrong] | [What a stakeholder would observe if this risk materialises -- not just the technical failure mode] | [How to handle it] |
```

### Spec Rules

1. Each scenario gets a priority (P1/P2/P3). P1 = MVP.
2. Acceptance criteria use Given/When/Then format.
3. Requirements use `FR-###` IDs and RFC-2119 verbs (MUST/SHOULD/MAY).
4. Mark genuinely ambiguous requirements with `[NEEDS CLARIFICATION: specific question]`.
   Hard limit: max 3 per spec. If more ambiguity exists, recommend running `clarify`.
5. Success criteria use `SC-###` IDs and must be measurable.
6. Entities describe _what_, not _how_ (no field types, no code).
7. Assumptions section documents any gaps you filled with reasonable defaults.
8. **Write Assumptions and Risks for an uninitiated reader.** Assume the audience
   knows the project domain (e.g., wastewater treatment, accounting) but _not_
   the technical method (statistics, machine learning, spatial modelling).
   Concretely:
   - Avoid unexplained jargon. If a technical term is essential, define it in
     parentheses on first use (e.g., "R-squared -- a score from 0 to 1 showing how
     well the model fits the data").
   - The Assumptions bullets must state _why_ the assumption matters in plain
     English, not just restate the technical choice.
   - The Risk Impact column must describe what a stakeholder would notice
     (e.g., "the map would misrepresent emissions near the pond edge"), not just
     the failure mode name (e.g., "unstable coefficients").
   - This rule applies to all spec types but is most critical for statistical
     modelling, ML, and spatial analysis specs.

---

## Procedure: `plan`

Generate a phased implementation plan from an existing spec. Focus on _how_ to build it.

### Plan Template

```markdown
# Implementation Plan: [FEATURE]

**Date**: [DATE] | **Spec**: [link or "see above"]
**Status**: Draft

## Summary

[One paragraph: what we're building and the technical approach]

## Technical Context

**Language**: Python 3.12
**Key Dependencies**: [e.g., CrewAI, Pydantic, openpyxl, pandas]
**Testing**: pytest (see `test-driven-development` skill)
**Layer Rules**: [Reference importlinter.ini or state constraints]

## Design Decisions

| #   | Decision           | Choice       | Rationale |
| --- | ------------------ | ------------ | --------- |
| D1  | [What was decided] | [The choice] | [Why]     |

## Architecture

[Data flow diagrams, state machines, layer rules, worksheet schemas --
whatever is needed to make the implementation unambiguous]

## Domain Models

[For each new model: module path, class name, key fields, frozen/mutable.
Code sketches are fine here -- they will become real code in implementation.]

## Phased Delivery

### Phase 0: Foundation

**Goal**: [What this phase delivers -- must be runnable working code, not stubs]

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

**New files**:
```

[File tree]

```

**Deliverables**: [...]

**Verification**:
```

[Command to run + what to look for in output]

```

**Gold standard task (Phase Nb)**:
- Human reviews output
- Curates N best examples into `examples.yaml`
- Top examples promoted into next phase's prompt

**Acceptance Gate** (both must pass before next phase starts):
- [ ] Working code: the deliverables above run end-to-end without errors
- [ ] If any function file was modified or introduced: run `.venv\Scripts\activate; python -m pytest tests/[affected modules] -v` and confirm green

---

## File Inventory

| Phase | New Files | Count |
|-------|-----------|-------|
| 0 | [...] | N |
| 1 | [...] | N |

**Total new**: ~N | **Total deleted**: ~N

## Risk Register

| Risk | Mitigation |
|------|-----------|
| [...] | [...] |
```

### Plan Rules

1. Every phase has: Goal, TDD approach, Deliverables, Verification command, Acceptance Gate.
2. Verification must be a runnable command (`.venv\Scripts\activate; python -m ...`).
3. Acceptance Gates are hard pass/fail stops. The next phase MUST NOT start until both
   acceptance gate items are checked off.
4. Every phase MUST end with working, runnable code. Stubs, pseudocode, or placeholder
   implementations are NOT permitted as phase deliverables.
5. If a phase modifies or introduces any function file, running pytest on the affected
   test modules is a mandatory gate item. The next phase MUST NOT start until all tests pass.
6. All new or modified functions MUST be written test-first (Red -> Green -> Refactor)
   following the `test-driven-development` skill. The TDD approach section in each phase names the
   functions and their test file paths.
7. Gold Standard tasks (Phase Nb) appear after each agent/deliverable phase.
   The human curates examples that feed into the next phase's prompt.
8. File Inventory lists every new and deleted file, grouped by phase.
9. Design Decisions table captures choices with rationale (not just the choice).
10. Domain model sketches include module path, class name, and key fields.
11. Architecture section includes state machines, data flow, or schemas as needed.

### Post-Plan Step: Library Best Practices (mandatory)

After the initial plan draft is written, use the Context7 MCP to fetch best practices
and latest documentation for every third-party package listed in Technical Context.
Then update the plan file with a **Library Best Practices** section.

**Procedure**:

1. For each package in `Key Dependencies`, call `resolve-library-id` with the package
   name to get its Context7-compatible library ID.
2. Call `get-library-docs` with `mode='code'` for API references and code examples.
   Use a focused `topic` argument (e.g., `topic='OLS regression formula API'`) rather
   than fetching the full docs.
3. For each package, record any API calls, class names, or argument names that differ
   from what the plan currently assumes. Common traps: removed kwargs, renamed methods,
   changed import paths, new preferred idioms.
4. Append a `## Library Best Practices` section to the plan file with one subsection per
   package. Each subsection MUST include:
   - The exact import path confirmed in the docs.
   - Any API gotchas or removed/renamed kwargs that affect this plan.
   - A minimal confirmed code pattern for the primary usage in this plan.
5. If a library finding requires changing a Design Decision, update the decision table
   and note the source (e.g., "D4 updated after Context7 review").

**Skip condition**: If a package is a well-known stdlib module (e.g., `pathlib`,
`os`, `json`) or already has a Library Best Practices entry from a prior Context7
review in this plan, skip it.

### Complexity Tracking

If the plan deviates from established repo conventions (skills, layer rules, etc.),
document the deviation:

| Deviation              | Why Needed | Simpler Alternative Rejected Because |
| ---------------------- | ---------- | ------------------------------------ |
| [e.g., new dependency] | [reason]   | [why simpler approach fails]         |

---

## Procedure: `tasks`

Generate a checkboxable task list from an existing plan. Every task is atomic and
file-specific.

### Task Format

Every task MUST follow this format:

```
- [ ] T### [P?] [Phase?] Description with exact file path
```

**Components**:

1. **Checkbox**: Always `- [ ]`
2. **Task ID**: Sequential `T001`, `T002`, ... across the entire document
3. **[P] marker**: Present ONLY if the task can run in parallel with adjacent tasks
   (different files, no dependency on incomplete tasks)
4. **[Phase N] label**: Which plan phase this task belongs to
5. **Description**: Clear action verb + exact file path

**Good examples**:

- `- [ ] T001 [Phase 0] Create PipelineStatus enum in src/misquoted/domain/value_objects/pipeline.py`
- `- [ ] T002 [P] [Phase 0] Create PipelineEntry model in src/misquoted/domain/value_objects/pipeline.py`
- `- [ ] T010 [Phase 1] Write Cultural Radar prompt in src/misquoted/crewai/agents/cultural_radar/prompt.py`

**Bad examples**:

- `- [ ] Create the model` (missing ID, phase, file path)
- `- [ ] T001 Implement stuff` (vague, no file path)
- `T001 Create model` (missing checkbox)

### Tasks Template

```markdown
# Tasks: [FEATURE NAME]

**Input**: [Link to plan]
**Prerequisites**: [What must exist before starting]

## Phase 0: [Name]

**Purpose**: [One line -- must describe a working, runnable deliverable]

- [ ] T001 [Phase 0] ...
- [ ] T002 [P] [Phase 0] ...
- [ ] T003 [P] [Phase 0] ...

### Acceptance Gate

- [ ] T004 [Phase 0] Verify working code: [runnable command that exercises this phase's deliverables]
- [ ] T005 [Phase 0] If function files modified/introduced -- run pytest: `.venv\Scripts\activate; python -m pytest tests/[affected] -v` -- all tests green

---

## Phase N: [Name]

**Purpose**: [One line -- must describe a working, runnable deliverable]

### Tests (write first -- must fail before implementation begins)

- [ ] T0XX [Phase N] Write failing test for [function] in tests/.../test_X.py
- [ ] T0XX [Phase N] Confirm test fails: `.venv\Scripts\activate; python -m pytest tests/.../test_X.py -v`

### Implementation

- [ ] T0XX [P] [Phase N] Create ... in src/.../X.py
- [ ] T0XX [Phase N] Implement ... in src/.../Y.py (depends on T0XX)

### Acceptance Gate

- [ ] T0XX [Phase N] Verify working code: [runnable command that exercises this phase's deliverables]
- [ ] T0XX [Phase N] Run pytest on affected modules: `.venv\Scripts\activate; python -m pytest tests/[affected] -v` -- all tests green

---

## Phase Z: Polish

- [ ] TXXX [P] [Phase Z] Update **init**.py exports in src/.../
- [ ] TXXX [Phase Z] Run full test suite and lint: `.venv\Scripts\activate; python -m pytest; python -m ruff check src/`
- [ ] TXXX [Phase Z] Run end-to-end verification: [specific command]

### Acceptance Gate

- [ ] TXXX [Phase Z] All tests green and lint clean

## Execution Notes

- [P] = parallelizable (different files, no dependencies)
- [Phase N] = which plan phase the task belongs to
- TDD is mandatory for all function work: write failing test (Red), confirm it fails, implement (Green), refactor
- The Acceptance Gate at the end of each phase is a hard stop -- do not start the next phase until it passes
- If any function file was modified or introduced, the pytest gate is mandatory
- Commit after each task or logical group
```

### Tasks Rules

1. Task IDs are globally sequential (T001 through TXXX) -- no resets per phase.
2. TDD is mandatory for all function work: write the failing test first, confirm it fails,
   implement to green, then refactor. Never write implementation before its test.
3. Every phase that modifies or introduces function files MUST include an Acceptance Gate
   section with: (a) a runnable working-code verification task, and (b) a pytest task.
   Both must be checked off before the next phase starts.
4. The pytest Acceptance Gate task is a hard stop -- the next phase MUST NOT start
   until it is checked off with all tests green.
5. Use `[P]` only when tasks are truly independent (different files, no data dependency).
6. Every task includes an exact file path.
7. Tasks must be specific enough to implement without re-reading the plan.
8. Phase 0 may consist of config, models, or scaffolding without function files; in that
   case the pytest gate is omitted but the working-code verification task is still required.

---

## Procedure: `clarify`

Scan a spec for ambiguities and ask up to 5 targeted questions.

### How It Works

1. **Scan** the spec across 7 categories, rating each Clear / Partial / Missing:
   - Functional scope and behavior
   - Domain and data model (entities, state transitions)
   - Interaction flow (user journeys, error/empty states)
   - Non-functional attributes (performance, scale, reliability)
   - Integration and external dependencies
   - Edge cases and failure handling
   - Terminology consistency
2. **Prioritize** findings by `Impact x Uncertainty` -- highest risk first.
3. **Ask** up to 5 questions, one at a time:
   - Multiple-choice: recommend the best option, allow custom input.
   - Short-answer: suggest an answer with reasoning.
4. **Integrate** each accepted answer back into the spec immediately.
5. **Stop** when: all resolved, user says "done", or 5 questions asked.

### Clarify Rules

1. Hard limit: 5 questions maximum.
2. One question at a time -- never reveal the full queue.
3. After each answer, update the spec inline (replace `[NEEDS CLARIFICATION]` markers).
4. Never introduce new ambiguity while resolving existing ones.

---

## Procedure: `analyze`

Read-only cross-check for consistency across spec, plan, and tasks.

### Detection Passes

Run these 6 checks (max 30 findings total):

1. **Duplication**: Near-duplicate requirements or tasks.
2. **Ambiguity**: Vague language without metrics, unresolved `[NEEDS CLARIFICATION]` markers.
3. **Underspecification**: Requirements without tasks, tasks referencing undefined models.
4. **Skill alignment**: Conflicts with repo skills (layer rules, naming, testing conventions).
5. **Coverage gaps**: Requirements with no tasks, phases with no verification.
6. **Inconsistency**: Terminology drift, contradictory statements, ordering conflicts.

### Severity Levels

- **CRITICAL**: Skill violations, missing required artifacts, zero-coverage requirements.
- **HIGH**: Duplicate/conflicting requirements, untestable criteria.
- **MEDIUM**: Terminology drift, missing edge-case coverage.
- **LOW**: Style/wording, minor redundancy.

### Output Format

```markdown
## Analysis Report: [Feature]

| ID  | Category | Severity | Location | Summary                          | Recommendation      |
| --- | -------- | -------- | -------- | -------------------------------- | ------------------- |
| A01 | Coverage | HIGH     | FR-003   | No task maps to this requirement | Add task in Phase 2 |

### Metrics

- Total requirements: N
- Total tasks: N
- Coverage: X%
- Critical findings: N
- Unresolved clarifications: N
```

### Analyze Rules

1. **Read-only** -- never modify any file.
2. Report findings, then offer: "Want me to suggest fixes for the top N issues?"
3. Limit to 30 findings. Prioritize CRITICAL and HIGH.

---

## Inputs / Outputs / Validation

### Inputs

- A feature idea, scratchpad, or existing plan in any format.
- For `plan`: an existing spec (from `specify` or equivalent).
- For `tasks`: an existing plan (from `plan` or equivalent).
- For `clarify`: an existing spec with ambiguities.
- For `analyze`: spec + plan + tasks (all three).

### Outputs

- `specify` -> `spec.md` (or inline in scratchpad)
- `plan` -> `plan.md` (or inline in scratchpad)
- `tasks` -> `tasks.md` (or inline in scratchpad)
- `clarify` -> Updated spec with resolved ambiguities
- `analyze` -> Read-only report (never modifies files)

### Validation

- Spec: All 3 mandatory sections present (Scenarios, Requirements, Success Criteria).
  At most 3 `[NEEDS CLARIFICATION]` markers. Every requirement has an `FR-###` ID.
- Plan: Every phase has Goal + TDD approach + Deliverables + Verification + Acceptance Gate.
  Every Acceptance Gate has both a working-code item and (if function files are touched)
  a pytest item. File Inventory accounts for all new/deleted files.
- Tasks: Every task has checkbox + ID + phase label + file path. IDs are globally sequential.
  Tests precede implementation per phase. Every phase that touches function files has an
  Acceptance Gate section with a pytest task. The pytest task is checked off only when
  all tests are green.
