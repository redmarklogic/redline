# Implementation Plan: Skill SRP Enforcement

**Date**: 2026-06-07 | **Spec**: [spec.md](spec.md)
**Status**: Draft

## Summary

This feature enforces the Single Responsibility Principle across the skills corpus. It has
three interrelated parts: (1) codify a named SRP rule in `writing-skills` so every future
skill is governed before it is created; (2) process all 12 known violations — splitting,
narrowing, or issuing documented exceptions; (3) extend `ceremony-agent-topology-sync` with
a mandatory SRP compliance pass. No net-new behaviour is introduced; all work is structural
extraction of existing concerns or procedural additions to existing artifacts. TDD pressure
scenarios are therefore scoped to the SRP rule section only (new authored rule), not to
the splits themselves.

> **Corpus update (post-spec)**: `pre-pr-checks` was renamed to `sonarqube-find-and-fix`
> after the spec was authored, introducing a 12th violation. No agent JD references this
> skill; disposition is rename → `sonarqube-quality-gate` + justified-orchestrator exception.

---

## Technical Context

**Corpus type**: Markdown skill files + agent JD files (no Python runtime involved)
**Primary artifacts touched**: `.agents/skills/*/SKILL.md`, `.claude/agents/*.md`,
`docs/architecture/skills-architecture.md`
**No Python TDD cycle**: All changes are structural extractions or documentation edits.
The RED-GREEN-REFACTOR cycle applies only to the new SRP rule authored in `writing-skills`
(per spec assumption: splits are not net-new behaviour).
**Vendor boundary**: `writing-skills`, `spec-kit`, and the `superpowers` suite are at Layer 0.
`writing-skills` is vendor-owned — the SRP rule must be added without breaking vendor-upgrade
compatibility. The rule belongs in the project extension layer unless `writing-skills`
explicitly supports a project-owned extension file. **→ See Research Phase.**
**Constitution relevance**: Principle II (Hook-First Enforcement) applies — the SRP rule
must be accompanied by a deterministic check (pre-commit hook or topology sync scan), not
just a documented instruction. Principle I (SSOT) means the SRP rule lives in exactly one
place.
**Layer 0 immutability constraint**: `writing-skills` is vendor-managed (Layer 0). Adding
content directly to it risks being overwritten on `specify upgrade`. **→ Needs resolution.**
**Key agent JD references to update** (identified from routing table scan):

| Agent JD | Skill references that may change |
|---|---|
| `harriet.md` | `hiring-agent-management`, `ceremony-agent-topology-sync` |
| `kabilan.md` | `resolving-pr-issues`, `spec-kit`, `mcp-cce` |
| `linda.md` | `library-management`, `mcp-cce` |
| `john.md` | `marketing-social-selling-linkedin`, `ceremony-monthly-editorial-session`, `mcp-cce` |
| `ron.md` | `pm-product-strategist`, `mcp-cce` |
| `peter.md` | `evaluation-architecture`, `ai-acceptable-use-policy`, `mcp-cce` |
| `graeme.md` | `mcp-cce` (narrative mention + routing) |

---

## Design Decisions

| # | Decision | Choice | Rationale |
|---|---|---|---|
| D1 | Where the SRP rule lives | New project-owned extension section in `writing-skills/procedures/writing-skills.md` (not the SKILL.md stub) | `SKILL.md` is vendor-managed (Layer 0); the `procedures/` sub-file is the project-owned extension point that survives `specify upgrade`. Avoids vendor boundary violation. |
| D2 | Exception record format | Inline `srp-exception.md` companion file in the skill directory | Keeps the exception co-located with the skill it documents. Prevents orphan exception records. Follows existing `procedures/` pattern. |
| D3 | Deprecated skill retention | Mark retired skills with `deprecated: true` frontmatter + `forwarding-to:` pointer; do not delete immediately | Allows any agent that loads a retired skill to receive an explicit warning rather than a silent 404. Aligns with FR-009. Deletion deferred to next topology sync cleanup pass. |
| D4 | SRP compliance hook mechanism | Extend `ceremony-agent-topology-sync` procedure (procedural scan phase), not a git pre-commit hook | SRP violations in skill names are structural editorial decisions — they don't fit a deterministic commit-time binary check. The topology sync scan is the appropriate enforcement point per Constitution Principle III (Defence-in-Depth). A separate `check-skill-srp.py` pre-commit hook is flagged as a **Should Have** (not Must Have) for Phase 2. |
| D5 | Replacement skill naming convention | Verb-noun pairs, no "and", existing layer placement must be re-evaluated per `skills-architecture.md` placement rule | Preserves layer integrity; placement rule: "highest layer containing all referenced skills + 1". |
| D6 | Three "evaluate first" skills | `resolving-pr-issues` → justified pipeline (single end-to-end PR resolution concern, sequential steps not separable without losing coherence); `spec-kit` → justified orchestrator (wraps vendor CLI lifecycle, single concern: specification-driven development); `mcp-cce` → justified coherent MCP interface (all tools serve one concern: codebase discovery and session continuity) | Evaluated against the spec's exception criteria. Each receives a `srp-exception.md`. |

---

## Domain Impact

**New packages**: None — no Python code changes.
**Bounded context changes**: None — skills are documentation artifacts.
**Import-linter contract updates**: None.
**Subdomain classification**: N/A (no Python domain model changes).
**New domain terms**:
- `SRP Rule`: governance rule — one skill, one concern, single verb-noun name, no "and" in name or primary responsibility statement.
- `Exception Record`: companion `srp-exception.md` declaring a skill as a justified orchestrator or pipeline.
- `SRP Compliance Pass`: mandatory phase in topology sync that produces a violations list artifact.
- `Violations List`: output artifact of the SRP compliance pass.

---

## Architecture

This feature is purely documentary and procedural — no function pipeline diagram applies.
The structural topology of changes is captured in the **Phase Map** below.

### Dependency Direction of Changes

```
writing-skills (Layer 0 extension)
  ↑ referenced by
ceremony-agent-topology-sync (Layer 9) — adds SRP compliance pass that reads skill names
  ↑ referenced by
harriet.md (agent JD) — routing unchanged; harriet calls ceremony-agent-topology-sync
```

New skills produced by splits sit at the same layer as their parent (Layer 7, 8, or 9
depending on placement rule re-evaluation at split time).

---

## Constitution Check

| Principle | Impact | Status |
|---|---|---|
| I. SSOT | SRP rule lands in one place (`writing-skills/procedures/writing-skills.md` extension section). No parallel definition. | PASS |
| II. Hook-First | Topology sync scan is the enforcement mechanism (procedural, not automated hook). Pre-commit hook deferred to Should Have. Documented as a known gap in Risk Register. | CONDITIONAL — gap documented |
| III. Defence-in-Depth | Topology sync (probabilistic) + `writing-skills` rule (guidance) + optional pre-commit hook (deterministic). All three layers identified; hook is Should Have. | PASS |
| IV. Dependency Direction | New skills must not reference agents by name. Split skills stay at or below Layer 9. No upward references introduced. | PASS |
| V–XI | No Python code, no component boundaries, no domain objects, no data — not applicable. | N/A |
| XII. CLI-First | No external operations in this feature. | N/A |

**No constitution violations identified. Conditional gap on Principle II is documented in Risk Register.**

---

## MoSCoW

| Category | Items |
|---|---|
| **Must have** | SRP rule section in `writing-skills` with pass/fail test and exception path (FR-001–003); all 11 violations processed (FR-004–005); agent JD routing tables updated (FR-006); `ceremony-agent-topology-sync` SRP compliance pass added (FR-007–008); deprecated skills marked (FR-009) |
| **Should have** | `check-skill-srp.py` pre-commit hook for automated name/description scanning (Constitution Principle II gap); skills-architecture.md updated for all new/retired skill entries |
| **Could have** | False-positive registry section in topology sync report format (for quickly clearing incorrectly flagged skills); a companion `srp-audit-log.md` tracking all decisions made during this feature |
| **Won't have (this time)** | Automated splitting tooling; changes to `.github/agents/` (vendor-generated SpecKit agents, explicitly out of scope); retroactive TDD pressure scenarios for existing splits |

---

## Violation Assessment

Detailed split/exception decision for each of the 11 violations:

### Justified Exceptions (document; no split)

| Skill | Category | Rationale |
|---|---|---|
| `resolving-pr-issues` | Justified pipeline | Single end-to-end PR resolution concern. Steps (reproduce → fix → test → push → CI → re-consent → resolve) are tightly coupled — splitting at any boundary would destroy the coherent workflow. Description is a triggering condition list, not a multi-concern statement. |
| `spec-kit` | Justified orchestrator | Wraps vendor CLI lifecycle (specify plan / specify / tasks / implement). Single concern: specification-driven development. The multiple CLI commands are sub-steps of one concern, not independent skills. Layer 0 vendor-managed. |
| `mcp-cce` | Justified coherent MCP interface | All tools (`context_search`, `session_recall`, `record_decision`, `reindex`, `expand_chunk`) serve one concern: codebase discovery and session continuity. Splitting by tool would fragment a unified interface. Description correctly signals single concern. |

### Splits Required

| Skill | Violation | Proposed Replacement Skills | Layer |
|---|---|---|---|
| `hiring-agent-management` | Name + description contain three concerns: hiring, auditing/PIPs, org chart/register maintenance | `hire-agent` (hiring workflow), `audit-agent` (agent audits and PIPs), `maintain-agent-registry` (org chart and agent register) | L9 |
| `ai-acceptable-use-policy` | Description lists: governance rules, DORA AI capabilities, small-batch enforcement, deliberate practice design, AI output verification mentoring, domain governance rules — 6+ concerns | `define-ai-policy` (policy structure and DORA capabilities map), `enforce-ai-batch-discipline` (PR size thresholds, author-side flagging, small-batch enforcement) | L8 |
| `ceremony-monthly-editorial-session` | Name contains "ceremony" (acceptable prefix) but description covers: running session, processing magazine issue, content signal extraction, editorial calendar update — multiple outputs suggest orchestrator pattern. Evaluate as justified pipeline. | **→ Justified pipeline exception**: single trigger (new magazine issue), single concern (process issue into content signals + calendar updates). Exception record required. | L9 |
| `evaluation-architecture` | Description lists: evaluation lifecycle design, rubric structure, LLM-as-judge, ground truth management, pipeline architecture, HITL design, production monitoring — 7 concerns | `design-eval-rubric` (rubric structure, scoring systems, LLM-as-judge), `design-eval-pipeline` (FTI architecture, HITL, production monitoring, ground truth management) | L8 |
| `pm-product-strategist` | Description: "starting new product, refreshing strategy after market shifts, roadmap lacks strategic thread, OKRs disconnected" — multiple strategy modes, but all serve one concern: product strategy synthesis (JTBD → OST → OKR). **→ Evaluate as justified pipeline.** | **→ Justified pipeline exception**: three modes are sequential steps of one strategy synthesis concern, not independent skills. Exception record required. | L9 |
| `marketing-social-selling-linkedin` | Name is a triple compound (marketing + social-selling + linkedin). But the concern is singular: LinkedIn social selling for B2B. The three pillars are sub-steps. Description covers: profile optimisation, prospecting outreach, comment campaigns — all within one concern. **→ Evaluate as justified single-focus skill; name is domain compound noun, not conjunction.** | **→ Rename to `linkedin-social-selling`** (cleaner verb-noun form) to remove the marketing-prefix collision. No split needed. Companion note in exception record for the name rationale. | L9 |
| `ceremony-agent-topology-sync` | Name is a compound (ceremony + agent-topology-sync). Concerns in description: periodic sync, agent reflection, JD patches, org chart — all sub-steps of one ceremony. **→ Justified orchestrator.** | **→ Rename to `sync-agent-topology`** (verb-noun). Exception record documents orchestrator status. | L9 |
| `library-management` | Description: indexing, renaming, adding books, scanning folders, metadata extraction, SNZ scraping, updating Excel index, renaming files — 7 operations. But all serve one concern: digital library management at `<library_root>`. **→ Evaluate as justified single-focus skill.** The operations are all sub-tasks of library maintenance. | **→ Justified pipeline exception**: all operations are steps in managing one library. Exception record required. | L7 |
| `sonarqube-find-and-fix` | Name contains structural "and" joining find + fix. Introduced after initial spec by renaming `pre-pr-checks`. Description lists scan, triage, fix, record FPs, shift-left prevention — all sub-steps of one concern: end-to-end SonarQube quality gate. No agent JD routing references. **→ Justified orchestrator.** | **→ Rename to `sonarqube-quality-gate`** (noun-qualifier + concern, no "and"). Exception record documents orchestrator wrapping `sonarqube-scan` + `sonarqube-review`. | L9 |

**Revised violation tally** (post-assessment):

| Category | Count | Skills |
|---|---|---|
| Justified exception (document only) | 6 | `resolving-pr-issues`, `spec-kit`, `mcp-cce`, `ceremony-monthly-editorial-session`, `pm-product-strategist`, `library-management` |
| Rename only (no split) | 3 | `marketing-social-selling-linkedin` → `linkedin-social-selling`, `ceremony-agent-topology-sync` → `sync-agent-topology`, `sonarqube-find-and-fix` → `sonarqube-quality-gate` |
| Full split required | 2 | `hiring-agent-management` (→ 3 skills), `evaluation-architecture` (→ 2 skills) |
| Narrow + split | 1 | `ai-acceptable-use-policy` (→ 2 skills) |

---

## Phased Delivery

### Phase 0: SRP Rule Codification

**Goal**: The SRP rule is authored and discoverable in `writing-skills`. Exception path is
defined. The rule is the governance anchor for all subsequent phases.

**TDD approach**: Per `writing-skills` Iron Law, a pressure scenario must fail before the
rule is written. One subagent test: instruct an agent to create a new skill named
`hiring-and-assessment` without the rule present — confirm it does not flag the name.
Then add the rule and confirm the same agent flags it. This is the only RED-GREEN cycle
in this feature (new authored rule = new behaviour).

**Deliverables**:

1. `.agents/skills/writing-skills/procedures/writing-skills.md` — new `## SRP Rule` section
   added. Contains: (a) naming constraint (single verb-noun, no "and"); (b) responsibility
   statement constraint (no multi-concern "and"); (c) pass/fail test format; (d) exception
   path with `srp-exception.md` template; (e) link to audit checklist in topology sync.
2. `.agents/skills/writing-skills/procedures/srp-exception-template.md` — template for
   exception records (orchestrator and pipeline variants).

**Verification**:

```
Read .agents/skills/writing-skills/procedures/writing-skills.md
Confirm: section "## SRP Rule" exists, contains naming constraints, pass/fail test format,
and exception path. Section is scannable in < 30 seconds (SC-004).
```

**Acceptance Gate** (both must pass before Phase 1 starts):
- [ ] Working rule: SRP section exists with all three sub-components (naming constraint, responsibility constraint, exception path)
- [ ] Pressure scenario RED-GREEN confirmed: subagent flags `hiring-and-assessment` with rule present; does not flag without

---

### Phase 1: Justified Exceptions — Documentation Pass

**Goal**: The 6 justified exceptions are documented with `srp-exception.md` companion files.
No skill is split. Each exception record is self-contained and references the exception
template from Phase 0.

**TDD approach**: None — this is structural documentation, not new behaviour.

**Deliverables**:

1. `.agents/skills/resolving-pr-issues/srp-exception.md` — justified pipeline record
2. `.agents/skills/spec-kit/srp-exception.md` — justified orchestrator record
3. `.agents/skills/mcp-cce/srp-exception.md` — justified coherent MCP interface record
4. `.agents/skills/ceremony-monthly-editorial-session/srp-exception.md` — justified pipeline
5. `.agents/skills/pm-product-strategist/srp-exception.md` — justified pipeline
6. `.agents/skills/library-management/srp-exception.md` — justified pipeline

**Verification**:

```
For each of the 6 skills above:
- Read srp-exception.md
- Confirm: exception category (orchestrator | pipeline | coherent-interface) is stated
- Confirm: coordinated sub-concerns are listed
- Confirm: reason splitting would reduce coherence is stated
```

**Acceptance Gate**:
- [ ] All 6 exception records exist and contain required fields

---

### Phase 2: Renames

**Goal**: `marketing-social-selling-linkedin` and `ceremony-agent-topology-sync` are renamed
to SRP-compliant verb-noun names. All agent JD references updated. Skills-architecture.md
updated. Deprecated markers added to old directories.

**TDD approach**: None — structural rename.

**Deliverables**:

1. `.agents/skills/linkedin-social-selling/SKILL.md` — copied from `marketing-social-selling-linkedin`, name and description updated
2. `.agents/skills/marketing-social-selling-linkedin/SKILL.md` — `deprecated: true`, `forwarding-to: linkedin-social-selling` added to frontmatter
3. `.agents/skills/sync-agent-topology/SKILL.md` — copied from `ceremony-agent-topology-sync`, name updated
4. `.agents/skills/ceremony-agent-topology-sync/SKILL.md` — `deprecated: true`, `forwarding-to: sync-agent-topology` added
5. `.agents/skills/sync-agent-topology/srp-exception.md` — orchestrator exception record (ceremony structure is justified)
6. `.agents/skills/linkedin-social-selling/srp-exception.md` — domain compound noun rationale record
7. `.agents/skills/sonarqube-quality-gate/SKILL.md` — copied from `sonarqube-find-and-fix`, name updated to `sonarqube-quality-gate`, description updated to single-concern statement free of multi-concern "and"
8. `.agents/skills/sonarqube-quality-gate/srp-exception.md` — justified-orchestrator exception record; sub-concerns: `sonarqube-scan` (static analysis), `sonarqube-review` (triage + false-positive recording), fix cycle, shift-left prevention; rationale: all steps serve one concern — end-to-end SonarQube quality gate
9. `.agents/skills/sonarqube-find-and-fix/SKILL.md` — `deprecated: true`, `forwarding-to: sonarqube-quality-gate` added to frontmatter
10. `.claude/agents/john.md` — routing table updated: `ceremony-monthly-editorial-session` → retained; `marketing-social-selling-linkedin` → `linkedin-social-selling`
11. `.claude/agents/harriet.md` — routing table: `ceremony-agent-topology-sync` → `sync-agent-topology`
12. `docs/architecture/skills-architecture.md` — Layer 9 map updated with new names, old names marked `[deprecated]`

**Verification**:

```
Grep .claude/agents/*.md for "marketing-social-selling-linkedin" → 0 results (routing tables only)
Grep .claude/agents/*.md for "ceremony-agent-topology-sync" → 0 routing table results
Grep .claude/agents/*.md for "sonarqube-find-and-fix" → 0 results (no agent JD references this skill)
Confirm .agents/skills/linkedin-social-selling/SKILL.md exists
Confirm .agents/skills/sync-agent-topology/SKILL.md exists
Confirm .agents/skills/sonarqube-quality-gate/SKILL.md exists
```

**Acceptance Gate**:
- [ ] No routing table entry in any `.claude/agents/*.md` references the old names
- [ ] New skill directories exist with updated frontmatter
- [ ] Deprecated markers in place on all three retired directories

---

### Phase 3: Full Splits — `hiring-agent-management` and `evaluation-architecture`

**Goal**: The two skills requiring full splits are decomposed. Three replacement skills for
`hiring-agent-management`, two for `evaluation-architecture`. All agent JD routing tables
updated. Deprecated markers on retired skills.

**TDD approach**: None — structural extraction of already-functioning concerns.

**Deliverables**:

1. `.agents/skills/hire-agent/SKILL.md` — hiring workflow (gap identification → JD drafting → onboarding)
2. `.agents/skills/audit-agent/SKILL.md` — agent audits and PIPs
3. `.agents/skills/maintain-agent-registry/SKILL.md` — org chart and agent register maintenance
4. `.agents/skills/hiring-agent-management/SKILL.md` — `deprecated: true`, `forwarding-to: hire-agent, audit-agent, maintain-agent-registry`
5. `.agents/skills/hiring-agent-management/procedures/` — procedures distributed to appropriate replacement skill directories
6. `.agents/skills/design-eval-rubric/SKILL.md` — rubric structure, scoring, LLM-as-judge, calibration
7. `.agents/skills/design-eval-pipeline/SKILL.md` — FTI architecture, HITL, production monitoring, ground truth management
8. `.agents/skills/evaluation-architecture/SKILL.md` — `deprecated: true`, `forwarding-to: design-eval-rubric, design-eval-pipeline`
9. `.claude/agents/harriet.md` — routing: `hiring-agent-management` → `hire-agent`, `audit-agent`, `maintain-agent-registry`
10. `.claude/agents/peter.md` — routing: `evaluation-architecture` → `design-eval-rubric`, `design-eval-pipeline`
11. `docs/architecture/skills-architecture.md` — Layer 8 and Layer 9 entries updated

**Verification**:

```
Grep .claude/agents/*.md for "hiring-agent-management" → 0 routing table references
Grep .claude/agents/*.md for "evaluation-architecture" → 0 routing table references
Confirm hire-agent, audit-agent, maintain-agent-registry SKILL.md files exist
Confirm design-eval-rubric, design-eval-pipeline SKILL.md files exist
```

**Acceptance Gate**:
- [ ] No agent JD routing table references retired skill names
- [ ] All replacement skills have single-verb-noun names and descriptions free of multi-concern "and"
- [ ] Deprecated skills marked with forwarding pointers

---

### Phase 4: `ai-acceptable-use-policy` Narrow + Split

**Goal**: `ai-acceptable-use-policy` is narrowed and split into two focused skills. Agent JD
routing updated.

**TDD approach**: None — structural extraction.

**Deliverables**:

1. `.agents/skills/define-ai-policy/SKILL.md` — policy document structure, DORA AI capabilities map, acceptable-use stance
2. `.agents/skills/enforce-ai-batch-discipline/SKILL.md` — PR size thresholds, author-side flagging, small-batch enforcement, deliberate practice design, AI output verification mentoring
3. `.agents/skills/ai-acceptable-use-policy/SKILL.md` — `deprecated: true`, `forwarding-to: define-ai-policy, enforce-ai-batch-discipline`
4. `.claude/agents/peter.md` — routing: `ai-acceptable-use-policy` → `define-ai-policy`, `enforce-ai-batch-discipline`
5. `docs/architecture/skills-architecture.md` — Layer 8 updated

**Verification**:

```
Grep .claude/agents/*.md for "ai-acceptable-use-policy" → 0 routing table references
Confirm define-ai-policy, enforce-ai-batch-discipline SKILL.md files exist
```

**Acceptance Gate**:
- [ ] Replacement skills pass SRP rule check (no "and" in names or primary responsibility statements)
- [ ] Peter's routing table updated

---

### Phase 5: Topology Sync SRP Compliance Pass

**Goal**: `ceremony-agent-topology-sync` (now `sync-agent-topology`) procedure is extended
with a mandatory SRP compliance phase. The phase produces a named violations list artifact
as part of the Topology Sync Report. The phase is mandatory — a sync run cannot be marked
complete without it.

**TDD approach**: None — procedural extension.

**Deliverables**:

1. `.agents/skills/sync-agent-topology/procedures/run-topology-sync.md` — updated with new
   mandatory Phase: "SRP Compliance Pass" inserted after Gap & Overlap Analysis. Phase
   defines: scan all `SKILL.md` frontmatter `name` and `description` fields for "and"
   patterns; produce `violations-list.md` in the Topology Sync Report folder; report
   format includes skill name, field flagged, pattern matched, and disposition
   (new-violation / known-exception / false-positive).
2. `.agents/skills/sync-agent-topology/SKILL.md` — Output Artifacts table updated to
   include `violations-list.md` as a required artifact.
3. `.agents/skills/sync-agent-topology/procedures/srp-scan-procedure.md` — standalone
   SRP scan procedure (reusable outside full topology sync): scan algorithm, "and" pattern
   definition, false-positive rules (domain compound nouns, grammatical "and" vs
   multi-concern "and"), exception record lookup.

**Verification**:

```
Read .agents/skills/sync-agent-topology/procedures/run-topology-sync.md
Confirm: "SRP Compliance Pass" phase exists, is listed as mandatory (not optional),
output artifact path is defined.
Read .agents/skills/sync-agent-topology/SKILL.md
Confirm: violations-list.md in Output Artifacts table.
```

**Acceptance Gate**:
- [ ] SRP compliance phase listed as mandatory in topology sync procedure
- [ ] `violations-list.md` defined as a required output artifact
- [ ] Scan procedure distinguishes structural "and" from grammatical "and" and domain compound nouns
- [ ] Known exceptions from Phases 1–4 are referenced as skip-list entries

---

### Phase 6: Final Audit and Sweep

**Goal**: SC-002 and SC-003 confirmed by scan. All remaining narrative JD references
(outside routing tables) to retired skill names identified and updated. Registry entries
confirmed.

**TDD approach**: None — verification pass.

**Deliverables**:

1. Full scan of `.agents/skills/*/SKILL.md` frontmatter `name` fields — 0 disallowed "and"
   patterns in non-exception skills (SC-002).
2. Full scan of `.claude/agents/*.md` — 0 routing table references to retired skill names
   (SC-003).
3. Narrative mention sweep — any free-text references to retired skill names in agent JDs
   updated or noted.
4. `docs/architecture/skills-architecture.md` — complete and current, all new skills
   registered, all deprecated skills marked.
5. `specs/016-skill-srp-enforcement/audit-log.md` — one-page record of all decisions made
   (split, exception, rename) with rationale summary. Serves as the feature's closure
   artifact.

**Verification**:

```
Grep .agents/skills/*/SKILL.md for " and " in name: fields → returns only exception skills
Grep .claude/agents/*.md for all retired skill names → 0 routing table hits
Read docs/architecture/skills-architecture.md → all 11 original violations resolved
```

**Acceptance Gate** (feature closure):
- [ ] SC-001: 100% of 11 violations processed (split, narrowed, or documented as exceptions)
- [ ] SC-002: 0 disallowed "and" patterns in skill names (excluding exception records)
- [ ] SC-003: 0 retired skill names in agent JD routing tables
- [ ] SC-004: SRP rule discoverable in `writing-skills` in < 30 seconds
- [ ] SC-005: Topology sync SRP compliance phase is mandatory with violations list artifact
- [ ] SC-006: SRP pass/fail determinable from `writing-skills` alone

---

## File Inventory

| Phase | New Files | Modified Files | Deprecated |
|---|---|---|---|
| 0 | `writing-skills/procedures/writing-skills.md` (section add), `writing-skills/procedures/srp-exception-template.md` | — | — |
| 1 | 6 × `srp-exception.md` | — | — |
| 2 | `linkedin-social-selling/SKILL.md`, `sync-agent-topology/SKILL.md`, `sonarqube-quality-gate/SKILL.md`, 3 × `srp-exception.md` | `john.md`, `harriet.md`, `skills-architecture.md` | `marketing-social-selling-linkedin`, `ceremony-agent-topology-sync`, `sonarqube-find-and-fix` |
| 3 | `hire-agent/SKILL.md`, `audit-agent/SKILL.md`, `maintain-agent-registry/SKILL.md`, `design-eval-rubric/SKILL.md`, `design-eval-pipeline/SKILL.md` | `harriet.md`, `peter.md`, `skills-architecture.md` | `hiring-agent-management`, `evaluation-architecture` |
| 4 | `define-ai-policy/SKILL.md`, `enforce-ai-batch-discipline/SKILL.md` | `peter.md`, `skills-architecture.md` | `ai-acceptable-use-policy` |
| 5 | `sync-agent-topology/procedures/srp-scan-procedure.md` | `sync-agent-topology/procedures/run-topology-sync.md`, `sync-agent-topology/SKILL.md` | — |
| 6 | `specs/016-skill-srp-enforcement/audit-log.md` | `skills-architecture.md` (final), narrative JD mentions | — |

**Total new skill directories**: 9 (hire-agent, audit-agent, maintain-agent-registry,
design-eval-rubric, design-eval-pipeline, define-ai-policy, enforce-ai-batch-discipline,
linkedin-social-selling, sonarqube-quality-gate)
**Total renames**: 3 (marketing-social-selling-linkedin, ceremony-agent-topology-sync, sonarqube-find-and-fix)
**Total deprecated (not deleted)**: 6 (hiring-agent-management, evaluation-architecture,
ai-acceptable-use-policy, marketing-social-selling-linkedin, ceremony-agent-topology-sync,
sonarqube-find-and-fix)
**Total exception records**: 9 (6 justified exceptions + 3 rename rationale records)

---

## Risk Register

| Risk | Mitigation |
|---|---|
| `writing-skills` is Layer 0 vendor-managed — direct SKILL.md edits overwritten on `specify upgrade` | SRP rule placed in `procedures/writing-skills.md` (project-owned extension file), not in `SKILL.md` stub. Verify procedures/ directory is excluded from vendor upgrade scope before Phase 0. |
| Agent JDs that reference retired skills via narrative prose (not routing tables) are missed in the sweep | Phase 6 explicitly sweeps narrative mentions in addition to routing table entries. Grep pattern covers both structured and free-text contexts. |
| Split skill boundaries are contested — a split that looks clean in the plan looks wrong in execution | Each split deliverable requires founder review before the deprecated marker is applied. The deprecated skill stays accessible until the replacement is validated. |
| `ceremony-monthly-editorial-session` and `pm-product-strategist` exceptions may be challenged — they could be seen as needing splits | Exception rationale is documented in `srp-exception.md` with explicit criterion: "splitting would destroy end-to-end coherence of a single trigger → single output concern". Founder can override at Phase 1 review. |
| Constitution Principle II (Hook-First) gap: SRP rule has no pre-commit hook | Documented as known gap. `check-skill-srp.py` hook is Should Have. If deferred beyond this feature, a follow-up spec is created. |
| `sync-agent-topology` procedures/ directory may not yet exist (skill was previously `ceremony-agent-topology-sync`) | Phase 2 creates the new skill directory from scratch; Phase 5 adds procedure files. No assumption of existing procedures/ content in the renamed skill. |
| Topology sync SRP scan may produce false positives on domain compound nouns (e.g., `command-and-control`) | `srp-scan-procedure.md` explicitly defines a domain compound noun allowlist and distinguishes structural conjunctions from domain terms. False-positive disposition column in violations list. |
