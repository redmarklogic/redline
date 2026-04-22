# Implementation Plan: Skill Boundary Contract Rollout

**Branch**: `004-skill-boundary-contracts` | **Date**: 2026-04-21 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-skill-boundary-contracts/spec.md`

## Summary

Add a structured Boundary Contract section to every SKILL.md file under `.agents/skills/`
that does not already have one. Two template variants are used: "Inputs / Outputs / Out of
Scope" for service/workflow skills, and "Applies To / Produces / Does Not Cover" for
coding-standards skills. The rollout is phased: pilot 5 representative skills to validate
templates, update meta-skills (`writing-skills` and `hiring-agent-management`) to prevent
future drift, then batch the remaining ~50 skills by family group.

This is a documentation-only feature. No Python source code, test suites, CI pipelines, or
agent JD files are modified.

## Technical Context

**Language/Version**: N/A (documentation-only; skill files are Markdown)
**Primary Dependencies**: None (no third-party packages)
**Storage**: N/A
**Testing**: Agent-based pressure testing (subagent invocations per `writing-skills` TDD
cycle); Harriet's ORG AUDIT Step 7 for verification. No pytest.
**Target Platform**: `.agents/skills/*/SKILL.md` files (70 total)
**Project Type**: Documentation / skill infrastructure
**Performance Goals**: N/A
**Constraints**: Each Boundary Contract section must be 5-10 lines (excluding heading
lines). Existing skill logic, rules, and procedural content must not be altered.
**Scale/Scope**: 70 skills total (15 Clean, 34 Partial, 21 Leaky). 55 skills require
modification. 2 meta-skills require updates.

## Constitution Check

*GATE: Must pass before Phase 0.*

The constitution template is unpopulated for this project. Since this feature modifies
only Markdown documentation files (no Python source code, no new packages, no architectural
changes), constitution gates are satisfied by default:

- **No code changes**: FR-010 explicitly prohibits modifying `src/` or `tests/`.
- **No new dependencies**: No third-party packages are introduced.
- **No architectural impact**: No new bounded contexts, layers, or import-linter contracts.
- **TDD compliance**: Adapted to agent pressure-testing (per `writing-skills` TDD cycle)
  since there is no Python code to unit-test.

## Domain Impact

**Modularity assessment**: None. No Python packages are created or modified.
**New packages**: None.
**Bounded context changes**: None.
**Import-linter contract updates**: None.
**Subdomain classification**: N/A (documentation-only).
**New domain terms**:

| Term | Definition |
| --- | --- |
| Boundary Contract | A structured declaration within a SKILL.md file consisting of three subsections that define what the skill accepts, produces, and excludes |

## Project Structure

### Documentation (this feature)

```text
specs/004-skill-boundary-contracts/
    plan.md              # This file
    spec.md              # Feature specification
    checklists/          # Existing checklists directory
```

### Modified Files (repository root)

```text
.agents/skills/
    */SKILL.md           # 55 skill files modified (Boundary Contract added/completed)
    writing-skills/SKILL.md        # Creation checklist updated (Phase 2)
    hiring-agent-management/SKILL.md  # Pressure scenario added (Phase 2)
```

No files under `src/`, `tests/`, or `.github/agents/` are modified.

## MoSCoW

| Category | Items |
| --- | --- |
| **Must have** | Boundary Contract section in all 70 SKILL.md files (FR-001); correct template variant per skill type (FR-002, FR-003); 5-10 line length (FR-004); concrete artifacts in service/workflow contracts (FR-005); no modification of Clean skills (FR-008); no alteration of existing skill logic (FR-012) |
| **Should have** | `writing-skills` creation checklist updated (FR-006); `hiring-agent-management` pressure scenario added (FR-007); consistent contract language within skill families (SC-006) |
| **Could have** | A summary index of all boundary contracts for quick reference |
| **Won't have (this time)** | Automated pre-commit hook to enforce Boundary Contract presence; machine-readable contract format (YAML frontmatter); cross-skill dependency graph derived from contracts |

## Design Decisions

| # | Decision | Choice | Rationale |
| --- | --- | --- | --- |
| D1 | Rollout sequencing | Pilot (5 skills) then meta-skills then batched rollout | Validates both template variants on representative examples before committing to bulk changes. Catches template issues early. |
| D2 | Pilot skill selection | python-style, python-linting, spec-kit, brainstorming, redline-research | Covers both template variants (3 coding-standards + 2 service/workflow). Includes skills from different audit statuses (Leaky and Partial). Spec explicitly names these as acceptance scenario targets. |
| D3 | Batch grouping strategy | By skill family prefix (python-\*, pm-\*, eda-\*, marketing-\*, etc.) | Same-family skills share domain vocabulary and integration patterns, making consistency review natural. Reviewer can assess one family at a time. |
| D4 | Template variant assignment | Service/workflow if the skill orchestrates actions or produces artifacts; coding-standards if it primarily sets rules for code review | Matches the spec's edge case guidance. Hybrid skills (e.g., `python-script`) are resolved by examining primary function. |
| D5 | Verification method | Harriet's ORG AUDIT Step 7 (agent-based) | No Python code exists to pytest. The org audit already classifies skills by contract status, making it the natural verification mechanism. |
| D6 | Partial skill handling | Add only missing subsections; preserve existing contract content verbatim | FR-009 requires additive-only changes. Avoids introducing regressions in skills that already have partial contracts. |

## Skill Classification Reference

### Skill Families (70 total)

| Family | Count | Template Variant | Skills |
| --- | --- | --- | --- |
| python-\* | 24 | Coding-standards | python-class-design, python-crewai, python-data-ingestion, python-deptry, python-documentation, python-domain-modeling, python-error-handling, python-function-design, python-linting, python-mcp-tools, python-module-structure, python-paths, python-patterns, python-performance, python-pins-data-version-control, python-plot-colors, python-script, python-script-numbering, python-static-checks, python-style, python-testing-api, python-testing-unit, python-typing, python-usethis |
| pm-\* | 9 | Service/workflow | pm-decision-architect, pm-hypothesis-builder, pm-personas, pm-prd-builder, pm-prioritization, pm-problem-framer, pm-product-strategist, pm-roadmap, pm-structural-integrity-auditor |
| eda-\* | 4 | Coding-standards | eda-codebook, eda-interpreting-data, eda-qa, eda-visual-design |
| marketing-\* | 4 | Service/workflow | marketing-ai-content-review, marketing-content-big-5, marketing-product-led-seo, marketing-social-selling-linkedin |
| qmd-\* | 2 | Coding-standards | qmd-narrative-design, qmd-tables |
| Superpowers | 11 | Service/workflow | brainstorming, dispatching-parallel-agents, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, using-git-worktrees, using-superpowers, verification-before-completion, writing-skills |
| Infra/tooling | 10 | Mixed | dev-environment, doc-updater, git-push-batched, miro-mcp, notebooklm-mcp, pre-commit-hooks-create, security, skills-create, spec-kit, version-control |
| Standalone | 6 | Mixed | ceremony-monthly-editorial-session, data-tidy, hiring-agent-management, redline-research, strategy-pre-mortem, test-driven-development |

Template variant for "Mixed" families is determined per-skill based on D4 criteria.

## Phased Delivery

### Phase 1: Pilot -- 5 Priority Skills

**Goal**: Validate both template variants on representative skills from different families
and audit statuses. Prove the contract format, placement rules, and line-length constraint
work in practice before scaling.

**Pilot skills**:

| Skill | Family | Template Variant | Audit Status |
| --- | --- | --- | --- |
| python-style | python-\* | Coding-standards | Leaky |
| python-linting | python-\* | Coding-standards | Leaky/Partial |
| spec-kit | Infra/tooling | Service/workflow | Leaky/Partial |
| brainstorming | Superpowers | Service/workflow | Leaky |
| redline-research | Standalone | Service/workflow | Leaky |

**Approach**:

1. Read each pilot SKILL.md to determine current contract status (Clean/Partial/Leaky).
2. Classify the skill as service/workflow or coding-standards per D4.
3. Identify the correct insertion point: after the overview/frontmatter, before the first
   procedural heading (e.g., "## When to Use", "## Setup", "## Rules").
4. For Leaky skills: write a complete Boundary Contract section (all 3 subsections).
5. For Partial skills: add only the missing subsections, preserving existing content.
6. Verify each contract is 5-10 lines (excluding headings) per FR-004.
7. For service/workflow contracts: ensure Inputs and Outputs name concrete artifacts
   (file names, paths, document types) per FR-005.

**Deliverables**:

- 5 modified SKILL.md files with complete Boundary Contract sections
- Pilot review notes (inline in this plan or as commit messages)

**Verification**:

Run Harriet's ORG AUDIT Step 7 against the 5 pilot skills. All 5 must classify as "Clean".

```text
Invoke Harriet (hiring-agent-management skill) and request:
"Run ORG AUDIT Step 7 (Skill Boundary Contracts) against these 5 skills:
python-style, python-linting, spec-kit, brainstorming, redline-research.
Report contract status for each."
```

**Acceptance Gate**:

- [ ] All 5 pilot skills have a complete Boundary Contract section
- [ ] Each contract uses the correct template variant for its skill type
- [ ] Each contract is 5-10 lines (excluding headings)
- [ ] Service/workflow contracts name concrete artifacts and paths
- [ ] No existing skill logic or procedural content was altered (diff review)
- [ ] Harriet's ORG AUDIT Step 7 classifies all 5 as "Clean"

---

### Phase 2: Meta-Skill Updates

**Goal**: Update `writing-skills` and `hiring-agent-management` to prevent future contract
drift. This creates defence-in-depth: a creation gate (writing-skills) and a review gate
(hiring-agent-management).

**Prerequisites**: Phase 1 acceptance gate passed.

**Approach**:

1. **writing-skills/SKILL.md** (FR-006):
   - Read the skill creation checklist section.
   - Add a mandatory checklist item requiring a Boundary Contract section in every new
     skill.
   - The item must reference both template variants and state placement rules (after
     overview, before first procedural section).
   - Add the two template variant examples as reference material within the skill.

2. **hiring-agent-management/SKILL.md** (FR-007):
   - Read the pressure-testing section.
   - Add a pressure scenario: "Skill without boundary contract submitted for approval".
   - The scenario must describe the expected auditor behaviour: flag the skill as
     non-compliant and require a Boundary Contract before approval.

3. **Both meta-skills**: If either skill itself lacks a complete Boundary Contract, add
   one as part of this phase (eating our own dog food).

**Deliverables**:

- Modified `writing-skills/SKILL.md` with updated creation checklist
- Modified `hiring-agent-management/SKILL.md` with new pressure scenario
- Both meta-skills have their own Boundary Contracts (if not already Clean)

**Verification**:

1. Agent pressure-test: invoke a subagent with the `writing-skills` skill and ask it to
   create a new skill. Confirm it requires a Boundary Contract section as part of the
   creation checklist.

2. Agent pressure-test: invoke a subagent with the `hiring-agent-management` skill and
   submit a mock skill for audit that lacks a Boundary Contract. Confirm the auditor flags
   it as non-compliant.

3. Run Harriet's ORG AUDIT Step 7 against `writing-skills` and `hiring-agent-management`.

```text
Invoke Harriet: "Run ORG AUDIT Step 7 against writing-skills and
hiring-agent-management. Report contract status."
```

**Acceptance Gate**:

- [ ] `writing-skills` creation checklist includes mandatory Boundary Contract item
- [ ] The checklist item references both template variants and placement rules
- [ ] `hiring-agent-management` has a pressure scenario for missing boundary contracts
- [ ] Agent pressure-test: new skill creation flags missing contract
- [ ] Agent pressure-test: audit flags skill without contract as non-compliant
- [ ] Both meta-skills themselves have complete Boundary Contracts
- [ ] Harriet's ORG AUDIT Step 7 classifies both as "Clean"

---

### Phase 3: Batched Rollout -- Remaining Skills

**Goal**: Add or complete Boundary Contract sections for all remaining skills (~50,
depending on how many were addressed in Phases 1-2). Batch by family for consistency
review.

**Prerequisites**: Phase 2 acceptance gate passed.

**Approach**:

Process each batch sequentially. Within a batch, skills can be processed in parallel
(they are independent files with no cross-dependencies).

**Batch 1: python-\* family** (~22 remaining after pilot)

All coding-standards template. Ensure consistent language across the family:
- "Applies To" should reference the same scope patterns (e.g., "All Python modules
  under `src/`" or "Python files during code review")
- "Produces" should name what the skill's rules generate (e.g., "Compliant code
  following [specific convention]")
- "Does Not Cover" should reference sibling skills where appropriate

**Batch 2: pm-\* family** (9 skills)

All service/workflow template. PM skills are the reference examples per the spec's
assumptions. Verify the existing Clean ones match the expected format and use them as
the consistency standard for any Partial/Leaky ones.

**Batch 3: eda-\* family** (4 skills)

Coding-standards template. These share a common EDA workflow context.

**Batch 4: marketing-\* family** (4 skills)

Service/workflow template. These share John's marketing workflow context.

**Batch 5: qmd-\* family** (2 skills)

Coding-standards template.

**Batch 6: Superpowers family** (~9 remaining after pilot)

Service/workflow template. These are obra/superpowers skills with workflow-oriented
contracts.

**Batch 7: Infra/tooling family** (~9 remaining after pilot)

Mixed templates. Classify each per D4:
- Service/workflow: doc-updater, git-push-batched, miro-mcp, notebooklm-mcp, spec-kit
  (done in pilot), skills-create
- Coding-standards: dev-environment, pre-commit-hooks-create, security, version-control

**Batch 8: Standalone skills** (~5 remaining after pilot)

Mixed templates. Classify each per D4:
- Service/workflow: ceremony-monthly-editorial-session, strategy-pre-mortem
- Coding-standards: data-tidy, test-driven-development
- Service/workflow: hiring-agent-management (done in Phase 2)

**Per-batch deliverables**:

- All SKILL.md files in the batch have complete Boundary Contract sections
- Consistency review within the batch (same family uses consistent language)

**Per-batch verification**:

Run Harriet's ORG AUDIT Step 7 against the batch. All skills in the batch must classify
as "Clean".

```text
Invoke Harriet: "Run ORG AUDIT Step 7 against all [family] skills:
[list skill names]. Report contract status for each."
```

**Final Verification (after all batches)**:

Run Harriet's ORG AUDIT Step 7 against all 70 skills. Every skill must classify as "Clean".

```text
Invoke Harriet: "Run ORG AUDIT Step 7 against all skills under
.agents/skills/. Report contract status for each. Expected: 70/70 Clean."
```

**Acceptance Gate**:

- [ ] Every SKILL.md under `.agents/skills/` contains a Boundary Contract section (70/70)
- [ ] Every contract uses the correct template variant (SC-002)
- [ ] Skills within the same family use consistent contract language (SC-006)
- [ ] No existing skill logic or procedural content was altered (SC-005, diff review)
- [ ] Partial skills had only missing subsections added (FR-009)
- [ ] Clean skills were not modified (FR-008)
- [ ] Harriet's ORG AUDIT Step 7 reports 70/70 Clean

## File Inventory

### Phase 1: Pilot (5 files modified)

| Action | File |
| --- | --- |
| Modified | `.agents/skills/python-style/SKILL.md` |
| Modified | `.agents/skills/python-linting/SKILL.md` |
| Modified | `.agents/skills/spec-kit/SKILL.md` |
| Modified | `.agents/skills/brainstorming/SKILL.md` |
| Modified | `.agents/skills/redline-research/SKILL.md` |

### Phase 2: Meta-Skills (2 files modified)

| Action | File |
| --- | --- |
| Modified | `.agents/skills/writing-skills/SKILL.md` |
| Modified | `.agents/skills/hiring-agent-management/SKILL.md` |

### Phase 3: Batched Rollout (~48 files modified)

All remaining `.agents/skills/*/SKILL.md` files not addressed in Phases 1-2.
Exact count depends on how many of the 55 non-Clean skills overlap with pilot
and meta-skill phases (7 addressed in Phases 1-2, ~48 remaining).

### Files NOT Modified

| Category | Reason |
| --- | --- |
| `src/**` | FR-010: No Python source code modified |
| `tests/**` | FR-010: No test files modified |
| `.github/agents/**` | FR-011: No agent JD files modified |
| 15 "Clean" skills | FR-008: Already have complete Boundary Contracts |

## Template Reference

### Service/Workflow Template

```markdown
## Boundary Contract

### Inputs
- [Concrete artifact name, file path, or document type]
- [Another input]

### Outputs
- [Concrete artifact name, file path, or document type]
- [Another output]

### Out of Scope
- [What this skill does NOT do, referencing the skill that does]
```

### Coding-Standards Template

```markdown
## Boundary Contract

### Applies To
- [What files, modules, or code this skill governs]

### Produces
- [What the skill's rules produce when followed]

### Does Not Cover
- [What is excluded, referencing sibling skills where appropriate]
```

## Glossary

| Term | Definition |
| --- | --- |
| Boundary Contract | A structured 3-subsection declaration in a SKILL.md that defines what the skill accepts, produces, and excludes. Prevents scope leaks between skills. |
| Skill Family | A group of skills sharing a common name prefix (e.g., `python-*`, `pm-*`) that should use consistent contract language. |
| Contract Status | Classification from the ORG AUDIT: "Clean" (complete contract), "Partial" (some subsections present), or "Leaky" (no contract section). |
| Harriet's ORG AUDIT | An agent-based audit workflow defined in the `hiring-agent-management` skill. Step 7 specifically evaluates skill boundary contract completeness. |
| Pressure Test | An agent-based verification method where a subagent is invoked with a skill and tested against edge-case scenarios to confirm correct behaviour. |
| Template Variant | One of two contract formats: "Inputs / Outputs / Out of Scope" (service/workflow) or "Applies To / Produces / Does Not Cover" (coding-standards). |
