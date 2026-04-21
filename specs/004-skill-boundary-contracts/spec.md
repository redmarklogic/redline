# Feature Specification: Skill Boundary Contract Rollout

**Feature Branch**: `004-skill-boundary-contracts`
**Created**: 2026-04-21
**Status**: Draft
**Input**: User description: "Add a Boundary Contract section to every skill file in .agents/skills/ that does not already have one."

## User Scenarios & Testing

### User Story 1 - Coding-Standards Skill Gets a Boundary Contract (Priority: P1)

An agent loads a coding-standards skill (e.g., `python-style`) and immediately sees what the skill applies to, what it produces, and what it does not cover -- without reading the entire document.

**Why this priority**: Coding-standards skills are the largest family (~25 skills). Completing them first covers the most ground and validates the lighter "Applies To / Produces / Does Not Cover" template.

**Independent Test**: Open any coding-standards SKILL.md that was previously "Leaky" or "Partial". Verify the Boundary Contract section exists after the overview and before the first procedural section, uses the correct template variant, and is 5-10 lines.

**Acceptance Scenarios**:

1. **Given** `python-style/SKILL.md` has no Boundary Contract section, **When** the rollout is applied, **Then** a "Boundary Contract" section with "Applies To", "Produces", and "Does Not Cover" subsections appears after the frontmatter/overview and before the first procedural heading.
2. **Given** a coding-standards skill already has a complete Boundary Contract (one of the 15 "Clean" skills), **When** the rollout runs, **Then** the file is not modified.
3. **Given** a coding-standards skill has a partial contract (e.g., has "Applies To" but no "Does Not Cover"), **When** the rollout is applied, **Then** the missing subsections are added without disturbing existing content.

---

### User Story 2 - Service/Workflow Skill Gets a Boundary Contract (Priority: P1)

An agent loads a service/workflow skill (e.g., `spec-kit`, `redline-research`, `ceremony-monthly-editorial-session`) and sees explicit Inputs, Outputs, and Out of Scope declarations including artifact names and file paths.

**Why this priority**: Service/workflow skills carry the highest integration risk -- agents hand off artifacts between them. Explicit contracts prevent scope leaks and duplicated work.

**Independent Test**: Open any service/workflow SKILL.md that was previously "Leaky" or "Partial". Verify the Boundary Contract section uses the "Inputs / Outputs / Out of Scope" template and names concrete artifacts and paths.

**Acceptance Scenarios**:

1. **Given** `spec-kit/SKILL.md` has no Boundary Contract section, **When** the rollout is applied, **Then** a "Boundary Contract" section with "Inputs", "Outputs", and "Out of Scope" subsections appears in the correct position, listing concrete artifact names and paths.
2. **Given** `brainstorming/SKILL.md` is a workflow skill, **When** the rollout is applied, **Then** its contract names what it hands off to downstream skills (e.g., validated spec ready for `spec-kit`).
3. **Given** a PM skill (e.g., `pm-prd-builder`) already has a clean contract, **When** the rollout runs, **Then** the file is not modified.

---

### User Story 3 - `writing-skills` Updated to Require Boundary Contracts (Priority: P2)

A developer creating a new skill using the `writing-skills` skill is guided to include a Boundary Contract section as a mandatory part of the skill creation checklist.

**Why this priority**: This is the prevention gate -- without it, new skills will ship without contracts, re-creating the debt this feature eliminates.

**Independent Test**: Read `writing-skills/SKILL.md` and confirm the creation checklist includes a mandatory item for "Boundary Contract section" with a reference to both template variants.

**Acceptance Scenarios**:

1. **Given** `writing-skills/SKILL.md` exists, **When** the rollout is applied, **Then** the skill creation checklist includes a mandatory item requiring a Boundary Contract section.
2. **Given** the checklist item exists, **When** a developer reads it, **Then** it references both template variants (service/workflow vs. coding-standards) and states where the section must be placed.

---

### User Story 4 - `hiring-agent-management` Gains a Pressure Scenario (Priority: P2)

The hiring-agent-management skill includes a pressure scenario for "skill submitted for approval without a boundary contract", so auditors flag missing contracts during org audits.

**Why this priority**: Complements Story 3 (creation gate) with a review gate. Together they form defence-in-depth against contract drift.

**Independent Test**: Read `hiring-agent-management/SKILL.md` and confirm a new pressure scenario exists for skills without boundary contracts.

**Acceptance Scenarios**:

1. **Given** `hiring-agent-management/SKILL.md` exists, **When** the rollout is applied, **Then** a pressure scenario titled "Skill without boundary contract submitted for approval" (or equivalent) is added to the pressure-testing section.
2. **Given** the scenario exists, **When** an auditor runs the org audit, **Then** skills missing a Boundary Contract section are flagged as non-compliant.

---

### User Story 5 - Full Rollout Across All 55 Non-Clean Skills (Priority: P3)

All 55 skills identified as "Leaky" (21) or "Partial" (34) in the org audit receive appropriate boundary contracts, batched by skill family for review efficiency.

**Why this priority**: This is the bulk execution -- depends on Stories 1 and 2 proving the templates work on representative examples first.

**Independent Test**: Run a directory scan of `.agents/skills/*/SKILL.md` and verify every file contains a "Boundary Contract" section. Count should be 70 total (15 existing + 55 new).

**Acceptance Scenarios**:

1. **Given** 55 skills lack complete boundary contracts, **When** the rollout is complete, **Then** every SKILL.md under `.agents/skills/` contains a Boundary Contract section.
2. **Given** skills are grouped into families (python-*, eda-*, pm-*, marketing-*, etc.), **When** each batch is applied, **Then** skills within the same family use consistent contract language and structure.
3. **Given** a skill has partial coverage (e.g., has Inputs but no Out of Scope), **When** the rollout is applied, **Then** only the missing subsections are added; existing contract content is preserved verbatim.

---

### Edge Cases

- A skill file has an unconventional structure (no clear frontmatter/overview vs. procedural split) -- the contract section is placed after the first paragraph or description block.
- A skill has content that resembles a contract but uses different headings (e.g., "Scope" instead of "Applies To") -- treat as "Partial" and normalise to the standard template.
- A skill straddles both categories (e.g., `python-script` has coding-standards rules AND workflow steps) -- use the service/workflow template if the skill orchestrates actions; use the coding-standards template if it primarily sets rules for code review.
- The `skills-create` skill (meta-skill for creating skills) needs its own contract updated to include the contract templates as outputs.

## Requirements

### Functional Requirements

- **FR-001**: Every SKILL.md under `.agents/skills/` MUST contain a "## Boundary Contract" section after the overview/frontmatter and before the first procedural section.
- **FR-002**: Service/workflow skills MUST use the template with subsections: "### Inputs", "### Outputs", "### Out of Scope".
- **FR-003**: Coding-standards skills MUST use the template with subsections: "### Applies To", "### Produces", "### Does Not Cover".
- **FR-004**: Each Boundary Contract section MUST be 5-10 lines (excluding heading lines).
- **FR-005**: Service/workflow contracts MUST name concrete artifacts (file names, directory paths, document types) in Inputs and Outputs.
- **FR-006**: The `writing-skills/SKILL.md` creation checklist MUST include a mandatory item requiring a Boundary Contract section in every new skill.
- **FR-007**: The `hiring-agent-management/SKILL.md` MUST include a pressure scenario for skills submitted without boundary contracts.
- **FR-008**: Skills already classified as "Clean" (15 skills) MUST NOT be modified.
- **FR-009**: Skills with partial contracts MUST have missing subsections added without altering existing contract content.
- **FR-010**: No Python source code (under `src/` or `tests/`) is modified by this feature.
- **FR-011**: No agent JD files (under `.github/agents/`) are modified by this feature.
- **FR-012**: Skill logic, rules, and procedural sections within each SKILL.md MUST NOT be altered -- only the Boundary Contract section is added or completed.

### Key Entities

- **Boundary Contract**: A structured declaration within a SKILL.md file consisting of three subsections that define what the skill accepts, produces, and excludes. Two template variants exist depending on skill type.
- **Skill Family**: A group of skills sharing a common prefix (e.g., `python-*`, `pm-*`, `eda-*`, `marketing-*`) that should use consistent contract language.
- **Contract Status**: Classification from the org audit -- "Clean" (complete contract), "Partial" (incomplete contract), or "Leaky" (no contract).

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of SKILL.md files under `.agents/skills/` contain a Boundary Contract section (70 out of 70).
- **SC-002**: Every Boundary Contract section uses the correct template variant for its skill type (service/workflow vs. coding-standards).
- **SC-003**: The `writing-skills` creation checklist prevents new skills from shipping without a Boundary Contract (verified by creating a test skill and confirming the checklist flags the omission).
- **SC-004**: The `hiring-agent-management` org audit flags any future skill missing a Boundary Contract as non-compliant.
- **SC-005**: No existing skill logic, rules, or procedural content is altered by the rollout (diff review shows only additions of Boundary Contract sections).
- **SC-006**: Skills within the same family use consistent contract language (verified by family-level review during batched rollout).

## Assumptions

- The org audit classification (15 Clean, 34 Partial, 21 Leaky) is current and accurate as of 2026-04-21. Any skills added after the audit will be handled as part of the rollout.
- The PM skills (`pm-problem-framer`, `pm-hypothesis-builder`, `pm-prd-builder`, `pm-decision-architect`, `pm-product-strategist`, `pm-structural-integrity-auditor`) are the reference examples for the service/workflow contract template.
- Skills can be unambiguously classified as either "service/workflow" or "coding-standards" based on their content. The edge case of hybrid skills (see Edge Cases) is resolved by examining the skill's primary function.
- The `writing-skills` skill has a creation checklist section that can be extended with a new mandatory item.
- The `hiring-agent-management` skill has a pressure-testing section where new scenarios can be added.
- Since this is documentation-only, no CI pipeline changes, dependency updates, or test suite modifications are required.
- Validation is performed through agent-based pressure testing (per `writing-skills` TDD cycle) rather than pytest.
