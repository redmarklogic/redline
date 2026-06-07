# Feature Specification: Skill Single Responsibility Principle (SRP) Enforcement

**Feature Branch**: `feature/45-local-redmark-sonarqube-branch-scan-workflow`

**Created**: 2026-06-07

**Status**: Draft

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Write an SRP-compliant new skill (Priority: P1)

A practitioner creating a new skill opens the `writing-skills` skill and finds a named SRP rule with a concrete test: a skill name must be a single verb-noun, the responsibility statement must contain no "and", and the name must not contain "and". The rule is unambiguous enough to pass or fail at a glance.

**Why this priority**: Without a codified rule, every new skill is a potential future violation. Defining the gate before rectifying existing violations makes the remediation permanent rather than one-off.

**Independent Test**: Can be tested by reading `writing-skills` and confirming the SRP rule section exists, contains naming constraints, and links to the audit checklist in `ceremony-agent-topology-sync`.

**Acceptance Scenarios**:

1. **Given** a practitioner is drafting a new skill named `hiring-and-assessment`, **When** they consult `writing-skills`, **Then** they find an explicit rule that rejects names containing "and" and are directed to split the skill.
2. **Given** a skill SKILL.md frontmatter `description` contains the phrase "and also manages", **When** the practitioner applies the SRP rule check, **Then** the check flags the description as a violation.
3. **Given** a practitioner proposes a valid single-concern skill named `profile-optimize`, **When** they apply the SRP check, **Then** the check passes with no flags.

---

### User Story 2 — Rectify an existing SRP violation (Priority: P1)

A practitioner tasked with splitting `hiring-agent-management` (or any of the 11 listed skills) uses the `writing-skills` skill and the new SRP rule to determine the correct split boundaries, produces focused replacement skills, and retires the original.

**Why this priority**: Codifying the rule without fixing existing violations creates a two-tier system where the stated standard contradicts the corpus. Both must move together.

**Independent Test**: Can be tested by verifying that `hiring-agent-management` is either replaced by two or more focused skills covering hiring and auditing/assessment and registry as separate concerns, or a documented decision exists explaining why the current scope is a justified exception.

**Acceptance Scenarios**:

1. **Given** the skill `hiring-agent-management` exists with three concerns in its boundary contract, **When** the SRP remediation is applied, **Then** at least two focused replacement skills exist, each with a single-verb-noun name and a responsibility statement free of "and".
2. **Given** a skill is identified as a justified orchestrator (e.g., it coordinates sub-steps of a single end-to-end concern), **When** the practitioner applies the SRP rule, **Then** a documented exception record exists and the skill is marked as an orchestrator with the coordinated sub-skills listed.
3. **Given** all 11 listed violations have been processed, **When** the skills directory is scanned, **Then** no skill name or responsibility statement in its frontmatter `description` field contains a disallowed conjunction pattern matching the SRP rule.

---

### User Story 3 — Agent JDs reflect new skill names (Priority: P2)

After a skill is split or renamed, every agent JD whose skill routing table referenced the old skill name is updated to reference the replacement skills. Routing tables are the agent's navigation layer; stale names cause silent skill-load failures.

**Why this priority**: Skill splits are incomplete until every downstream reference is updated. A broken routing table is a degraded agent with no visible error.

**Independent Test**: Can be tested by searching all `.claude/agents/*.md` files for the old skill names from the 11 violations list and confirming none remain after the update pass.

**Acceptance Scenarios**:

1. **Given** `hiring-agent-management` is split into `hire-agent`, `assess-agent`, and `maintain-registry`, **When** all agent JDs are scanned, **Then** no JD references `hiring-agent-management` as the routing target; each former reference points to the correct replacement skill.
2. **Given** a skill is kept under its original name but with narrowed scope (justified exception), **When** the JDs are reviewed, **Then** the routing table entry is updated with a note that companion skills now exist for the concerns removed from scope.

---

### User Story 4 — SRP compliance gate in topology sync (Priority: P3)

The `ceremony-agent-topology-sync` skill includes an SRP compliance pass as a named phase: scan all skill names and description fields for "and" patterns or multi-concern responsibility statements, and produce a flagged violations list as a mandatory output artifact.

**Why this priority**: Without an automated check in the sync ceremony, the SRP rule degrades over time. The topology sync is the natural enforcement point because it already reviews the full skills corpus.

**Independent Test**: Can be tested by running a topology sync (or reviewing its procedure) and confirming the SRP compliance phase is listed, produces a named output artifact, and a known violation (planted in a test skill) appears in that artifact's flagged list.

**Acceptance Scenarios**:

1. **Given** a skill named `plan-and-execute` is present in the skills directory, **When** the topology sync SRP compliance pass runs, **Then** the violation appears in the flagged violations list in the Topology Sync Report.
2. **Given** all skills pass SRP, **When** the SRP compliance pass runs, **Then** the Topology Sync Report records "SRP compliance: PASS — 0 violations" with the scan timestamp.
3. **Given** the topology sync procedure is loaded, **Then** the SRP compliance phase is listed as a mandatory phase (not optional) with its output artifact path defined.

---

### Edge Cases

- A skill whose name contains a hyphenated domain term that looks like "and" (e.g., `command-and-control`) — the SRP rule must distinguish structural conjunctions from domain-specific compound nouns.
- A skill covering a pipeline of tightly-coupled steps where splitting would destroy coherence (e.g., `resolving-pr-issues`) — the rule must accommodate justified pipelines with a documented exception path.
- A skill whose `description` field uses "and" grammatically (e.g., "Use when creating and editing...") rather than as a multi-concern marker — the rule must target multi-concern "and" in responsibility statements, not all occurrences of "and".
- Agent JDs that reference a now-retired skill name via a free-text narrative section rather than a routing table — the update pass must cover both structured routing tables and narrative mentions.
- A skill that already exists in narrow form but was incorrectly listed as a violation — the audit must be able to clear false positives with a brief rationale.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `writing-skills` skill MUST contain a named SRP rule section that defines: (a) a skill name must be a single verb-noun pair; (b) the skill owns exactly one concern end-to-end; (c) no "and" is permitted in the name or in the primary responsibility statement.
- **FR-002**: The SRP rule MUST include a concrete pass/fail test format usable by a practitioner without additional tools.
- **FR-003**: The SRP rule MUST define an exception path for justified orchestrators and justified pipelines, requiring a documented exception record.
- **FR-004**: Each of the 11 identified SRP violations MUST be processed: either split into focused replacement skills, narrowed in scope with excess concerns extracted, or retained with a documented justified-exception record.
- **FR-005**: Each replacement or narrowed skill MUST have a single-verb-noun name and a `description` field free of multi-concern "and" patterns.
- **FR-006**: Every agent JD in `.claude/agents/` that references a renamed or retired skill MUST be updated so all skill routing table entries point to current, valid skill names.
- **FR-007**: The `ceremony-agent-topology-sync` skill MUST include an SRP compliance pass as a mandatory named phase, producing a flagged violations list as a required output artifact in the Topology Sync Report.
- **FR-008**: The SRP compliance pass MUST check both skill names and frontmatter `description` fields for multi-concern indicators.
- **FR-009**: Skills retired through splitting MUST either be removed from the skills directory or marked with a `deprecated` status and a forwarding pointer to the replacement skills, so no agent loads a retired skill without warning.

### Key Entities

- **Skill**: A directory under `.agents/skills/<name>/` containing at minimum a `SKILL.md` with frontmatter `name` and `description` fields, a boundary contract section, and optional `procedures/` files.
- **SRP Rule**: The named governance rule stating that each skill owns one concern, has a single-verb-noun name, and has no "and" in name or primary responsibility statement.
- **Exception Record**: A documented rationale (inline comment in the skill or a companion `srp-exception.md`) declaring a skill as a justified orchestrator or pipeline, listing the coordinated sub-concerns and the reason splitting would reduce coherence.
- **Routing Table**: The skill-to-task mapping section in an agent JD that determines which skill is loaded for a given task type.
- **SRP Compliance Pass**: The named phase in the topology sync procedure that scans the skills corpus and produces a violations list.
- **Violations List**: The output artifact of the SRP compliance pass, listing skill names and the specific pattern that triggered the flag.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the 11 identified violations are processed (split, narrowed, or documented as exceptions) before the feature is closed.
- **SC-002**: Zero skill names in the corpus contain a disallowed "and" pattern after remediation, as confirmed by a scan of all `SKILL.md` frontmatter `name` fields.
- **SC-003**: Zero agent JDs reference a retired skill name in their routing tables after the update pass.
- **SC-004**: The `writing-skills` skill's SRP rule section is discoverable in under 30 seconds by a practitioner consulting it cold (i.e., it appears as a named, scannable section — not buried in prose).
- **SC-005**: The topology sync procedure contains an SRP compliance phase such that a topology sync run cannot be marked complete without producing a violations list artifact (even if the list is empty).
- **SC-006**: A practitioner applying the SRP rule to a new skill can determine pass/fail without consulting any document other than `writing-skills`.

## Assumptions

- The 11 skills listed in the requirements are the known violations at the time of specification; the actual audit may uncover additional violations, which are in scope for the same feature.
- "Justified orchestrator" and "justified pipeline" are the two recognised exception categories; no other exception types are assumed without explicit founder approval.
- The `resolving-pr-issues` skill is treated as a candidate pipeline (not a presumed violation) — the split vs. retain decision is deferred to the planning/implementation phase.
- The `spec-kit` skill (the agent-facing skill, not the CLI) is treated as a candidate orchestrator — evaluation of whether it needs splitting is in scope.
- `mcp-cce` is treated as a candidate coherent MCP interface — evaluation of whether `cce-index`, `cce-recall`, and `cce-persist` should be separate is in scope.
- Agent JDs in `.github/agents/` (vendor-generated SpecKit agents) are out of scope for routing table updates; only `.claude/agents/` JDs are in scope.
- Splitting a skill does not require writing new TDD pressure scenarios before merging, provided the split is a structural extraction of an already-functioning concern (not a new behaviour). The full RED-GREEN-REFACTOR cycle applies only to net-new skills.
- The skills architecture registry (`docs/architecture/skills-architecture.md`) must be updated for any new or retired skill entry, but registry updates are a sub-task of implementation, not a separate feature.
