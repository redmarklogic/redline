# Tasks: Skill SRP Enforcement

**Input**: [plan.md](plan.md)
**Prerequisites**: `.agents/skills/writing-skills/` exists; `.agents/skills/ceremony-agent-topology-sync/` exists; all 11 violation skills are readable; `.claude/agents/*.md` JDs are current

<!-- Task sizing rule: each task is a VERTICAL SLICE -- front-to-back, one complete
     new behaviour, nothing left dangling. This feature is purely documentary and
     structural. No Python code. No TDD cycle except Phase 0 (new authored SRP rule).
     Each phase is independently verifiable by reading the files it produces. -->

---

## Phase 0: SRP Rule Codification

**Purpose**: Codify the SRP rule in `writing-skills` so every future skill is governed before it is created. This is the governance anchor for all subsequent phases.

> TDD pressure scenario required (new authored rule = new behaviour per plan D1 and spec assumption). RED: confirm an agent does not flag `hiring-and-assessment` without the rule. GREEN: confirm it flags after the rule is added.

### Pressure Scenario (RED — must run before implementation)

- [ ] T001 [US1] Verify RED state: instruct a subagent to evaluate the proposed skill name `hiring-and-assessment` using the current `writing-skills` skill and confirm no flag is raised (rule does not yet exist) — document result inline before T002

### Implementation

- [ ] T002 [US1] Add `## SRP Rule` section to `.agents/skills/writing-skills/procedures/writing-skills.md` — section must contain: (a) naming constraint (single verb-noun, no "and"); (b) responsibility-statement constraint (no multi-concern "and"); (c) concrete pass/fail test format; (d) exception path with `srp-exception.md` reference; (e) link to SRP compliance pass in `sync-agent-topology`
- [ ] T003 [P] [US1] Create `.agents/skills/writing-skills/procedures/srp-exception-template.md` — template with two variants: `orchestrator` and `pipeline`; fields: `exception-category`, `coordinated-sub-concerns`, `split-reduction-rationale`, `approved-by`

### Acceptance Gate

- [ ] T004 [US1] Verify GREEN state: repeat T001 pressure scenario with rule now present — confirm subagent flags `hiring-and-assessment`; confirm `profile-optimize` passes with no flags (SC-004, SC-006)
- [ ] T005 [US1] Read `.agents/skills/writing-skills/procedures/writing-skills.md` — confirm `## SRP Rule` section exists, is scannable within 30 seconds, contains all three sub-components

---

## Phase 1: Justified Exceptions — Documentation Pass

**Purpose**: Document all 6 justified exceptions with `srp-exception.md` companion files so the SRP corpus is consistent before any splits are attempted.

> No TDD cycle — structural documentation, not new behaviour (per spec assumption).

### Implementation

- [ ] T006 [P] [US2] Create `.agents/skills/resolving-pr-issues/srp-exception.md` — category: `justified-pipeline`; sub-concerns: reproduce, fix, test, push, CI, re-consent, resolve; rationale: splitting sequential PR resolution steps destroys end-to-end coherence
- [ ] T007 [P] [US2] Create `.agents/skills/spec-kit/srp-exception.md` — category: `justified-orchestrator`; sub-concerns: specify plan, specify, tasks, implement (vendor CLI lifecycle); rationale: single concern is specification-driven development; Layer 0 vendor-managed
- [ ] T008 [P] [US2] Create `.agents/skills/mcp-cce/srp-exception.md` — category: `justified-coherent-interface`; sub-concerns: context_search, session_recall, record_decision, reindex, expand_chunk; rationale: all tools serve one concern — codebase discovery and session continuity
- [ ] T009 [P] [US2] Create `.agents/skills/ceremony-monthly-editorial-session/srp-exception.md` — category: `justified-pipeline`; sub-concerns: session facilitation, issue processing, content signal extraction, editorial calendar update; rationale: single trigger (new magazine issue), single output concern
- [ ] T010 [P] [US2] Create `.agents/skills/pm-product-strategist/srp-exception.md` — category: `justified-pipeline`; sub-concerns: JTBD analysis, OST tree, OKR alignment; rationale: three modes are sequential steps of one strategy synthesis concern
- [ ] T011 [P] [US2] Create `.agents/skills/library-management/srp-exception.md` — category: `justified-pipeline`; sub-concerns: index, rename, add, scan, metadata extract, SNZ scrape, Excel update, file rename; rationale: all operations serve one concern — digital library maintenance at `<library_root>`

### Acceptance Gate

- [ ] T012 [US2] Read all 6 `srp-exception.md` files — confirm each contains: `exception-category`, `coordinated-sub-concerns`, `split-reduction-rationale`; confirm no required field is absent

---

## Phase 2: Renames

**Purpose**: Rename `marketing-social-selling-linkedin` → `linkedin-social-selling`, `ceremony-agent-topology-sync` → `sync-agent-topology`, and `sonarqube-find-and-fix` → `sonarqube-quality-gate`; update all agent JD routing tables; mark deprecated originals.

> No TDD cycle — structural rename (per spec assumption).

### Implementation

- [ ] T013 [US2] Create `.agents/skills/linkedin-social-selling/SKILL.md` — copied content from `marketing-social-selling-linkedin/SKILL.md`; update `name:` to `linkedin-social-selling` and `description:` to single-concern statement (LinkedIn social selling for B2B) free of "and" multi-concern patterns
- [ ] T014 [P] [US2] Create `.agents/skills/linkedin-social-selling/srp-exception.md` — category: domain compound noun; rationale: `linkedin-social-selling` is a domain-specific compound, not a structural conjunction; no split needed
- [ ] T015 [US2] Update `.agents/skills/marketing-social-selling-linkedin/SKILL.md` — add `deprecated: true` and `forwarding-to: linkedin-social-selling` to frontmatter
- [ ] T016 [US2] Create `.agents/skills/sync-agent-topology/SKILL.md` — copied content from `ceremony-agent-topology-sync/SKILL.md`; update `name:` to `sync-agent-topology`; description must reflect single concern (synchronise agent topology) free of multi-concern "and" patterns
- [ ] T017 [P] [US2] Create `.agents/skills/sync-agent-topology/srp-exception.md` — category: `justified-orchestrator`; coordinated sub-steps: JD patch, gap/overlap analysis, org chart update, SRP compliance pass; rationale: single ceremony concern — topology synchronisation
- [ ] T018 [US2] Update `.agents/skills/ceremony-agent-topology-sync/SKILL.md` — add `deprecated: true` and `forwarding-to: sync-agent-topology` to frontmatter
- [ ] T019 [US3] Update `.claude/agents/john.md` — routing table: replace `marketing-social-selling-linkedin` with `linkedin-social-selling`; retain `ceremony-monthly-editorial-session` unchanged
- [ ] T020 [US3] Update `.claude/agents/harriet.md` — routing table: replace `ceremony-agent-topology-sync` with `sync-agent-topology` (first pass; full harriet update completes in Phase 3)
- [ ] T021 [US2] Create `.agents/skills/sonarqube-quality-gate/SKILL.md` — copied content from `sonarqube-find-and-fix/SKILL.md`; update `name:` to `sonarqube-quality-gate`; description updated to single-concern statement (end-to-end SonarQube quality gate) free of multi-concern "and" patterns
- [ ] T022 [P] [US2] Create `.agents/skills/sonarqube-quality-gate/srp-exception.md` — category: `justified-orchestrator`; coordinated sub-concerns: `sonarqube-scan` (static analysis trigger + wait), `sonarqube-review` (issue retrieval + FP triage), fix cycle, shift-left prevention; rationale: all steps serve one concern — end-to-end SonarQube quality gate; no agent JD routing updates needed
- [ ] T023 [US2] Update `.agents/skills/sonarqube-find-and-fix/SKILL.md` — add `deprecated: true` and `forwarding-to: sonarqube-quality-gate` to frontmatter
- [ ] T024 [US2] Update `docs/architecture/skills-architecture.md` — Layer 9 entries: add `linkedin-social-selling`, add `sync-agent-topology`, add `sonarqube-quality-gate`; mark `marketing-social-selling-linkedin`, `ceremony-agent-topology-sync`, and `sonarqube-find-and-fix` as `[deprecated]`

### Acceptance Gate

- [ ] T025 [US3] Grep `.claude/agents/*.md` for `marketing-social-selling-linkedin` — confirm 0 routing table hits
- [ ] T026 [US3] Grep `.claude/agents/*.md` for `ceremony-agent-topology-sync` — confirm 0 routing table hits
- [ ] T027 [US2] Confirm `.agents/skills/linkedin-social-selling/SKILL.md`, `.agents/skills/sync-agent-topology/SKILL.md`, and `.agents/skills/sonarqube-quality-gate/SKILL.md` exist with updated frontmatter
- [ ] T028 [US2] Confirm deprecated markers (`deprecated: true`, `forwarding-to:`) present in all three retired `SKILL.md` files

---

## Phase 3: Full Splits — `hiring-agent-management` and `evaluation-architecture`

**Purpose**: Decompose `hiring-agent-management` into 3 focused skills and `evaluation-architecture` into 2; update agent JD routing tables; mark deprecated originals.

> No TDD cycle — structural extraction of already-functioning concerns.

### Implementation — `hiring-agent-management` split

- [ ] T029 [US2] Create `.agents/skills/hire-agent/SKILL.md` — single concern: hiring workflow (gap identification, JD drafting, onboarding); name `hire-agent`; description free of multi-concern "and" patterns
- [ ] T030 [P] [US2] Create `.agents/skills/audit-agent/SKILL.md` — single concern: agent audits and PIPs; name `audit-agent`; description free of multi-concern "and" patterns
- [ ] T031 [P] [US2] Create `.agents/skills/maintain-agent-registry/SKILL.md` — single concern: org chart and agent register maintenance; name `maintain-agent-registry`; description free of multi-concern "and" patterns
- [ ] T032 [US2] Distribute procedures from `.agents/skills/hiring-agent-management/procedures/` to appropriate replacement skill `procedures/` directories (hiring → `hire-agent/procedures/`; PIPs/audits → `audit-agent/procedures/`; registry → `maintain-agent-registry/procedures/`)
- [ ] T033 [US2] Update `.agents/skills/hiring-agent-management/SKILL.md` — add `deprecated: true` and `forwarding-to: hire-agent, audit-agent, maintain-agent-registry` to frontmatter

### Implementation — `evaluation-architecture` split

- [ ] T034 [P] [US2] Create `.agents/skills/design-eval-rubric/SKILL.md` — single concern: rubric structure, scoring systems, LLM-as-judge, calibration; name `design-eval-rubric`; description free of multi-concern "and" patterns
- [ ] T035 [P] [US2] Create `.agents/skills/design-eval-pipeline/SKILL.md` — single concern: FTI architecture, HITL, production monitoring, ground truth management; name `design-eval-pipeline`; description free of multi-concern "and" patterns
- [ ] T036 [US2] Update `.agents/skills/evaluation-architecture/SKILL.md` — add `deprecated: true` and `forwarding-to: design-eval-rubric, design-eval-pipeline` to frontmatter

### Agent JD routing updates

- [ ] T037 [US3] Update `.claude/agents/harriet.md` — routing table: replace `hiring-agent-management` with `hire-agent`, `audit-agent`, `maintain-agent-registry`
- [ ] T038 [US3] Update `.claude/agents/peter.md` — routing table: replace `evaluation-architecture` with `design-eval-rubric`, `design-eval-pipeline`
- [ ] T039 [US2] Update `docs/architecture/skills-architecture.md` — Layer 9: add `hire-agent`, `audit-agent`, `maintain-agent-registry`, mark `hiring-agent-management` `[deprecated]`; Layer 8: add `design-eval-rubric`, `design-eval-pipeline`, mark `evaluation-architecture` `[deprecated]`

### Acceptance Gate

- [ ] T040 [US3] Grep `.claude/agents/*.md` for `hiring-agent-management` — confirm 0 routing table hits
- [ ] T041 [US3] Grep `.claude/agents/*.md` for `evaluation-architecture` — confirm 0 routing table hits
- [ ] T042 [US2] Confirm `hire-agent`, `audit-agent`, `maintain-agent-registry`, `design-eval-rubric`, `design-eval-pipeline` SKILL.md files all exist
- [ ] T043 [US2] Confirm all 5 replacement skill names and descriptions pass SRP rule check (no disallowed "and" patterns)

---

## Phase 4: Narrow + Split — `ai-acceptable-use-policy`

**Purpose**: Split `ai-acceptable-use-policy` into 2 focused skills; update peter's routing table; mark deprecated original.

> No TDD cycle — structural extraction.

### Implementation

- [ ] T044 [US2] Create `.agents/skills/define-ai-policy/SKILL.md` — single concern: policy document structure, DORA AI capabilities map, acceptable-use stance; name `define-ai-policy`; description free of multi-concern "and" patterns
- [ ] T045 [P] [US2] Create `.agents/skills/enforce-ai-batch-discipline/SKILL.md` — single concern: PR size thresholds, author-side flagging, small-batch enforcement, deliberate practice design, AI output verification mentoring; name `enforce-ai-batch-discipline`; description free of multi-concern "and" patterns
- [ ] T046 [US2] Update `.agents/skills/ai-acceptable-use-policy/SKILL.md` — add `deprecated: true` and `forwarding-to: define-ai-policy, enforce-ai-batch-discipline` to frontmatter
- [ ] T047 [US3] Update `.claude/agents/peter.md` — routing table: replace `ai-acceptable-use-policy` with `define-ai-policy`, `enforce-ai-batch-discipline`
- [ ] T048 [US2] Update `docs/architecture/skills-architecture.md` — Layer 8: add `define-ai-policy`, `enforce-ai-batch-discipline`; mark `ai-acceptable-use-policy` `[deprecated]`

### Acceptance Gate

- [ ] T049 [US3] Grep `.claude/agents/*.md` for `ai-acceptable-use-policy` — confirm 0 routing table hits
- [ ] T050 [US2] Confirm `define-ai-policy` and `enforce-ai-batch-discipline` SKILL.md files exist and pass SRP rule check

---

## Phase 5: Topology Sync SRP Compliance Pass

**Purpose**: Extend `sync-agent-topology` with a mandatory SRP compliance phase producing a `violations-list.md` artifact; add a reusable standalone scan procedure.

> No TDD cycle — procedural extension.

### Implementation

- [ ] T051 [US4] Add mandatory "SRP Compliance Pass" phase to `.agents/skills/sync-agent-topology/procedures/run-topology-sync.md` — phase inserted after Gap & Overlap Analysis; phase must: scan all `SKILL.md` frontmatter `name` and `description` fields for "and" patterns; produce `violations-list.md` in Topology Sync Report folder; report columns: skill name, field flagged, pattern matched, disposition (new-violation / known-exception / false-positive); phase marked as mandatory (not optional)
- [ ] T052 [US4] Update `.agents/skills/sync-agent-topology/SKILL.md` Output Artifacts table — add `violations-list.md` as required artifact; topology sync run cannot be marked complete without it
- [ ] T053 [US4] Create `.agents/skills/sync-agent-topology/procedures/srp-scan-procedure.md` — standalone reusable SRP scan procedure containing: scan algorithm; "and" pattern definition (structural conjunction vs grammatical "and" vs domain compound noun); domain compound noun allowlist and false-positive rules; exception record lookup instructions; reference to `srp-exception.md` files created in Phases 1–4 as skip-list entries

### Acceptance Gate

- [ ] T054 [US4] Read `.agents/skills/sync-agent-topology/procedures/run-topology-sync.md` — confirm "SRP Compliance Pass" phase exists, is listed as mandatory, and output artifact path (`violations-list.md`) is defined (SC-005)
- [ ] T055 [US4] Read `.agents/skills/sync-agent-topology/SKILL.md` — confirm `violations-list.md` is in Output Artifacts table
- [ ] T056 [US4] Read `.agents/skills/sync-agent-topology/procedures/srp-scan-procedure.md` — confirm it distinguishes structural "and" from grammatical "and" and domain compound nouns; confirm known exception skills from Phases 1–4 are referenced as skip-list entries

---

## Phase 6: Final Audit and Sweep

**Purpose**: Confirm all success criteria met by scan; sweep narrative JD mentions; finalise registry; produce closure artifact.

### Implementation

- [ ] T057 Grep `.agents/skills/*/SKILL.md` for ` and ` in `name:` fields — confirm only exception-documented skills remain; document any newly discovered violations
- [ ] T058 [P] Grep `.claude/agents/*.md` for all 12 original violation skill names — confirm 0 routing table hits across all agents (SC-003)
- [ ] T059 [P] Grep `.claude/agents/*.md` for retired skill names in free-text narrative sections — update or annotate any non-routing-table references found
- [ ] T060 Read `docs/architecture/skills-architecture.md` — confirm all 9 new skill directories are registered; all 6 deprecated skills are marked `[deprecated]`; registry is complete and current
- [ ] T061 Create `specs/016-skill-srp-enforcement/audit-log.md` — one-page record of all 12 violation decisions: skill name, decision (split / rename / exception / narrow+split), replacement skills or exception category, rationale summary; serves as feature closure artifact

### Acceptance Gate

- [ ] T062 SC-001: all 12 violations processed — confirm count: 6 exceptions, 3 renames, 2 full splits, 1 narrow+split
- [ ] T063 SC-002: 0 disallowed "and" patterns in skill names (excluding exception-documented skills) — grep confirms
- [ ] T064 SC-003: 0 retired skill names in agent JD routing tables — grep confirms
- [ ] T065 SC-004: SRP rule discoverable in `writing-skills` in < 30 seconds — read and time-check confirms
- [ ] T066 SC-005: topology sync SRP compliance phase is mandatory; `violations-list.md` is a required artifact — procedure read confirms
- [ ] T067 SC-006: SRP pass/fail determinable from `writing-skills` alone — confirm no cross-reference to another document is required to reach a verdict

---

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies on incomplete tasks in same phase)
- `[US1]` / `[US2]` / `[US3]` / `[US4]` = user story label from spec.md
- No TDD cycle except Phase 0 (T001 RED scenario, T004 GREEN confirmation)
- No pytest — all artifacts are Markdown; verification is by reading files and running grep
- Acceptance Gate at end of each phase is a hard stop — do not start the next phase until it passes
- Splits are structural extractions: no new behaviour, no RED-GREEN cycle required (per spec assumption)
- Deprecated skills retain their directories and SKILL.md with `deprecated: true` — do not delete until next topology sync cleanup pass
- Use `finishing-a-development-branch` skill to complete the work
- All code (skill content) subject to founder review before committing

## Dependency Order

```
Phase 0 (SRP Rule) → Phase 1 (Exceptions) → Phase 2 (Renames) → Phase 3 (Splits A)
                                                               → Phase 4 (Split B)
Phase 2 must complete before Phase 5 (sync-agent-topology must exist as renamed skill)
Phase 3 + Phase 4 must complete before Phase 5 (exception skip-list must be complete)
Phase 5 must complete before Phase 6 (SRP scan procedure must exist for final audit)
```

## Parallel Opportunities

| Phase | Parallel tasks |
|---|---|
| Phase 0 | T003 (exception template) parallel with T002 (SRP rule section) — different files |
| Phase 1 | T006–T011 all parallel — 6 independent `srp-exception.md` files in separate skill dirs |
| Phase 2 | T013+T014 parallel; T016+T017 parallel; T021+T022 parallel (sonarqube dirs); T019+T020+T024 parallel after new dirs exist |
| Phase 3 | T029+T030+T031 parallel; T034+T035 parallel; T037+T038 parallel |
| Phase 4 | T044+T045 parallel |
| Phase 6 | T057+T058+T059+T060 parallel |

## Task Summary

| Phase | Tasks | User Stories covered |
|---|---|---|
| Phase 0: SRP Rule | T001–T005 | US1 |
| Phase 1: Exceptions | T006–T012 | US2 |
| Phase 2: Renames | T013–T028 | US2, US3 |
| Phase 3: Full Splits | T029–T043 | US2, US3 |
| Phase 4: Narrow + Split | T044–T050 | US2, US3 |
| Phase 5: Topology Sync | T051–T056 | US4 |
| Phase 6: Audit & Sweep | T057–T067 | US2, US3 (closure) |
| **Total** | **67 tasks** | **US1–US4** |

**MVP scope**: Phase 0 alone delivers SC-004 and SC-006 — the SRP rule is codified and testable. Phases 1–4 deliver SC-001 and SC-002. Phase 5 delivers SC-005. Phase 6 closes SC-003.
