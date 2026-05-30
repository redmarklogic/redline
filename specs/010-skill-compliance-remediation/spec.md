# Feature Specification: Skill Compliance Remediation

**Feature Branch**: `010-skill-compliance-remediation`

**Created**: 2026-05-30

**Status**: Draft

**Input**: User description: "Bring all 86 skills in `.agents/skills/` into compliance with the writing-skills principles, using TDD (RED-GREEN-REFACTOR per the writing-skills Iron Law)."

## User Scenarios & Testing

### User Story 1 — Batch Description Fix (Priority: P1)

An agent loads a skill whose `description` field starts with "Standards for…" or "Conventions for…" instead of "Use when…". The agent cannot match the skill to triggering conditions because the description reads as a noun phrase, not a search-optimized trigger.

**Why this priority**: Description is the primary CSO signal; 36 skills currently fail. Without a "Use when…" trigger, the agent router cannot reliably match skills to tasks.

**Independent Test**: Grep all 82 editable SKILL.md frontmatter `description:` lines; verify every one starts with `"Use when"` and contains no workflow summary.

**Acceptance Scenarios**:

1. **Given** a SKILL.md with `description: Standards for designing maintainable Python classes`, **When** the remediation runs, **Then** the description is rewritten to `"Use when designing Python classes — responsibilities, init patterns, composition over inheritance"` (or equivalent "Use when…" form).
2. **Given** a SKILL.md whose description already starts with `"Use when…"`, **When** the audit runs, **Then** no change is made.

---

### User Story 2 — Token Efficiency Extraction (Priority: P1)

A skill's SKILL.md exceeds 500 words (or 200 for frequently-loaded skills) because full procedures, code examples, and reference tables are inline. This bloats context windows when the skill is loaded.

**Why this priority**: 49 skills fail. Inline bloat directly costs tokens on every skill load and degrades agent performance.

**Independent Test**: Run `wc -w` (or equivalent) on every SKILL.md; verify none exceeds its word-count ceiling. Verify extracted content exists in `procedures/` or sibling reference files and is cross-referenced from SKILL.md.

**Acceptance Scenarios**:

1. **Given** a SKILL.md with 1,200 words of inline procedure, **When** remediated, **Then** the procedure content lives in `procedures/<name>.md`, SKILL.md references it, and SKILL.md is under 500 words.
2. **Given** a frequently-loaded skill (loaded on every session: `using-superpowers`, `cce-mcp`, `dev-environment`) exceeding 200 words, **When** remediated, **Then** SKILL.md is under 200 words with heavy content in supporting files.
3. **Given** a skill already under its word limit, **When** the audit runs, **Then** no extraction occurs.

---

### User Story 3 — Common Mistakes Section (Priority: P2)

A skill teaches a pattern but embeds good/bad examples inline without a dedicated "Common Mistakes" section. Agents miss anti-patterns because they lack structured mistake→fix pairs.

**Why this priority**: 35 full failures + 14 partial. A structured section prevents agents from repeating known bad patterns.

**Independent Test**: Parse each SKILL.md for a `## Common Mistakes` heading with at least one structured mistake→fix pair. Verify 82/82 editable skills have this section.

**Acceptance Scenarios**:

1. **Given** a SKILL.md with inline good/bad examples but no `## Common Mistakes` section, **When** remediated, **Then** a `## Common Mistakes` section exists with structured entries (mistake description + fix).
2. **Given** a SKILL.md that already has `## Common Mistakes`, **When** the audit runs, **Then** no change is made.
3. **Given** a skill where no common mistakes are identifiable, **When** remediated, **Then** a minimal section exists with at least one domain-relevant mistake→fix pair.

---

### User Story 4 — Hardcoded Path Removal (Priority: P2)

Three skills (`library-management`, `notebooklm-index`, `notebooklm-mcp`) embed the absolute path `G:\My Drive\Library` in their description or body. This breaks portability and violates the "No Hardcoded User Paths" principle.

**Why this priority**: 3 skills fail. Small count but a clean violation of a binary principle.

**Independent Test**: Grep all SKILL.md files for drive-letter paths (`[A-Z]:\\`) and UNC paths (`\\\\`). Verify zero matches outside of hook-exempted lines.

**Acceptance Scenarios**:

1. **Given** a SKILL.md with `G:\My Drive\Library` in description or body, **When** remediated, **Then** the path is replaced with a placeholder (e.g., `<library-root>`) and a configuration note explaining how to resolve it.
2. **Given** a SKILL.md with no hardcoded paths, **When** the audit runs, **Then** no change is made.

---

### User Story 5 — Boundary Contract Addition (Priority: P2)

Five skills (`speckit-shaping-gate-check`, `speckit-source-reconciliation-run`, `speckit-static-checks-run`, `speckit-verification-gate-run`, `mental-models`) lack a `## Boundary Contract` section entirely.

**Why this priority**: Boundary contracts scope what a skill does and doesn't do. Without one, agents may misuse the skill.

**Independent Test**: Parse each SKILL.md for a `## Boundary Contract` heading. Verify 82/82 editable skills have one.

**Acceptance Scenarios**:

1. **Given** `mental-models` SKILL.md has no `## Boundary Contract`, **When** remediated, **Then** a boundary contract section exists with Applies To / Produces / Does Not Cover.
2. **Given** the 4 `speckit-*` skills are vendor-generated symlinks (AGENTS.md: "must not be edited manually"), **When** the audit encounters them, **Then** they are excluded from remediation scope with a documented exemption.
3. **Given** a SKILL.md that already has `## Boundary Contract`, **When** the audit runs, **Then** no change is made.

---

### User Story 6 — TDD Discipline Per Skill (Priority: P3)

Each skill remediation follows the writing-skills Iron Law: RED (document baseline failure), GREEN (apply minimal fix), REFACTOR (close loopholes). No skill is modified without a failing test first.

**Why this priority**: Ensures remediation quality and prevents regressions, but is a process constraint rather than a deliverable.

**Independent Test**: Each remediated skill has an associated pressure-scenario log or test record showing the RED→GREEN→REFACTOR cycle was followed.

**Acceptance Scenarios**:

1. **Given** a skill queued for remediation, **When** work begins, **Then** a baseline failure is documented before any change is made.
2. **Given** a skill with a documented baseline failure, **When** the fix is applied, **Then** the same test passes (GREEN).
3. **Given** a passing skill, **When** refactoring for loopholes, **Then** compliance is maintained across all 6 principles.
4. **Given** all remediations are complete, **When** a final compliance audit runs, **Then** an agent produces a full audit table with one row per skill and columns for each of the 6 principles (Frontmatter, "Use when…" desc, Boundary Contract, Token Efficiency, Common Mistakes, No Hardcoded Paths), using ✅/ℹ️/❌ per cell, and the table contains zero ❌ cells across all 82 editable skills.

---

### Edge Cases

- **Symlink skills**: The 4 `speckit-*` skills are symlinks to `.specify/extensions/`. These are vendor-managed and excluded from remediation. Audit must detect and skip them.
- **Skills with `procedures/` already**: Some skills (e.g., `writing-skills`, `spec-kit`) already have `procedures/` directories. Extraction must not duplicate existing structure.
- **Near-limit skills**: A skill at 490 words should not be extracted if it doesn't exceed 500. Only skills exceeding limits trigger extraction.
- **Description with partial "Use when"**: A description like `"Use when designing — Standards for…"` still fails because it summarizes workflow after the trigger. Must be trigger-only.
- **Hook-exempted paths**: Some hardcoded paths may carry `<!-- hook: allow -->` comments per the writing-skills "No Hardcoded User Paths" section. These are exempted.

## Requirements

### Functional Requirements

- **FR-001**: System MUST rewrite every non-compliant `description:` field to start with `"Use when [triggering conditions]"` in third person, under 500 characters, with no workflow summary.
- **FR-002**: System MUST extract inline content from any SKILL.md exceeding its word-count ceiling (500 words standard, 200 words frequently-loaded) into `procedures/` or sibling reference files.
- **FR-003**: System MUST add a `## Common Mistakes` section with structured mistake→fix pairs to every SKILL.md that lacks one.
- **FR-004**: System MUST replace hardcoded absolute paths (`G:\My Drive\Library`, drive-letter paths) with placeholders or project-relative paths, unless the line carries a `<!-- hook: allow -->` exemption.
- **FR-005**: System MUST add a `## Boundary Contract` section to every editable SKILL.md that lacks one.
- **FR-006**: System MUST skip vendor-generated symlink skills (4 `speckit-*` skills) and document the exemption.
- **FR-007**: System MUST follow the RED→GREEN→REFACTOR cycle for each skill remediation per the writing-skills Iron Law.
- **FR-008**: System MUST preserve existing compliant content — no unnecessary rewrites of passing sections.
- **FR-009**: System MUST validate the YAML frontmatter `name:` and `description:` fields remain parseable after edits.

### Key Entities

- **Skill**: A directory under `.agents/skills/<name>/` containing at minimum a `SKILL.md` file. Has frontmatter (`name`, `description`), optional `procedures/` directory, and optional supporting files.
- **Principle**: One of 6 compliance checks: Frontmatter, "Use when…" description, Boundary Contract, Token Efficiency, Common Mistakes, No Hardcoded Paths.
- **Pressure Scenario**: A test case where an agent is given a task that exercises the skill, used to verify the skill teaches the right behavior.
- **Remediation Record**: Documentation of the RED→GREEN→REFACTOR cycle for a single skill.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 82/82 editable skills pass all 6 writing-skills principles (100% compliance rate).
- **SC-002**: Zero SKILL.md files exceed their word-count ceiling (500 words standard, 200 words frequently-loaded).
- **SC-003**: Zero SKILL.md files contain hardcoded drive-letter or UNC paths outside hook-exempted lines.
- **SC-004**: Every editable SKILL.md contains both `## Boundary Contract` and `## Common Mistakes` sections.
- **SC-005**: Every `description:` field starts with `"Use when"` and contains no workflow summary.
- **SC-006**: Each remediated skill has a documented RED→GREEN→REFACTOR record showing the Iron Law was followed.
- **SC-007**: A post-remediation audit table is generated (one row per skill, six principle columns, ✅/ℹ️/❌ per cell) and contains zero ❌ cells and zero ℹ️ cells across all 82 editable skills.

## Assumptions

- The 4 `speckit-*` skills (`speckit-shaping-gate-check`, `speckit-source-reconciliation-run`, `speckit-static-checks-run`, `speckit-verification-gate-run`) are vendor-managed symlinks and excluded from remediation scope (82 editable skills, not 86).
- "Frequently-loaded skills" subject to the 200-word limit are: `using-superpowers`, `cce-mcp`, `dev-environment`, and any skill referenced in `AGENTS.md` auto-load configuration.
- Content extracted to `procedures/` retains full fidelity — no information loss, only relocation.
- The existing `writing-skills` SKILL.md and its procedures define the authoritative compliance standard; no changes to the standard itself are in scope.
- Remediation does not change skill behavior or content meaning — only structural compliance.
- Work can be batched by principle (e.g., fix all descriptions first, then all token efficiency) rather than requiring per-skill sequential TDD when the fix pattern is identical across a cohort.
