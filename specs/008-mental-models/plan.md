# Implementation Plan: Mental Models Skill

**Branch**: `feature/token-optimisation` | **Date**: 2026-05-27 | **Spec**: [specs/008-mental-models/spec.md](spec.md)
**Status**: Draft

## Summary

Create a bottom-layer agent skill at `.agents/skills/mental-models/` that provides a reusable, agent-agnostic library of mental model reference files. The skill has no knowledge of agents or other skills — it is a pure Markdown library organised into category subfolders. Five advisory/expert agent JDs (Ron, Mark, Graeme, Peter, Matt) gain a `## Mental Models` section referencing the skill. The `resolving-pr-issues` skill is refactored to replace its inline 5-Whys label with a pointer to the library.

## Technical Context

**Artifact type**: Static Markdown files (no Python code)
**File format**: Markdown with YAML frontmatter (skills) and plain Markdown (model files)
**Testing**: grep-based verification — no pytest (no code changes)
**Architecture**: Bottom-layer skill library — consumed by agent JDs and other skills; never consumes
**Dev OS**: Windows | **Authoring tool**: VS Code
**Source material**: NotebookLM notebook `c56b0801-40c9-4208-b31f-72ed360da184` (Super Thinking, The Great Mental Models Vol.1, The Decision Book, The Art of Strategy)

## Design Decisions

| #  | Decision | Choice | Rationale |
| -- | -------- | ------ | --------- |
| D1 | Skill structure | Approach A: category subfolders, agent assignment in SKILL.md | Decouples models from agents; extensible without restructuring |
| D2 | SKILL.md layer position | Bottom layer — no agent/skill knowledge | Prevents circular dependencies; library must be unconditionally importable |
| D3 | Model curation strategy | Hybrid 4+1: 4 universal + 1 role-specific per agent | Fixes both failure modes (generic answers + wrong tool for domain) at lowest maintenance cost |
| D4 | Role calibration location | Agent JDs only (not in model files) | Model files stay standalone; calibration stays with the agent it belongs to |
| D5 | Universal models | Circle of Competence, Inversion, Second-Order Thinking, Probabilistic Thinking | Non-negotiable epistemic hygiene across all advisory roles (Ron's recommendation) |
| D6 | 5 Whys inclusion | Add `root_cause_analysis/five-whys.md` as 11th file | Required to support `resolving-pr-issues` refactor |

## Domain Impact

**New packages**: None (no Python code)
**Bounded context changes**: None
**Import-linter contract updates**: None
**Subdomain classification**: Generic (agent infrastructure, no domain model)
**New domain terms**: Accountable Response Protocol — the three-question check every advisory agent must satisfy: (1) what reasoning pattern used, (2) what would falsify the conclusion, (3) what is outside competence

## Architecture

### Layer diagram

```
[Agent JDs]           ← consumers (reference skill)
[Other skills]        ← consumers (e.g. resolving-pr-issues)
        ↓
[mental-models/]      ← THIS SKILL (bottom layer, no outbound references)
        ↓
[Source notebooks]    ← authoring reference only (not runtime dependency)
```

### Folder layout

```
.agents/skills/mental-models/
  SKILL.md                              ← pure model catalog/index
  general_thinking/
    circle-of-competence.md
    inversion.md
    second-order-thinking.md
    probabilistic-thinking.md
  root_cause_analysis/
    five-whys.md
  strategic_decisions/
    reversible-vs-irreversible.md
    ooda-loop.md
  self_awareness/
    cognitive-biases.md
  risk_analysis/
    black-swan.md
  communication/
    third-story.md
```

### Model file contract (6-section schema)

Every model file **must** contain exactly these sections in order:
1. `## What it is` — 1-2 sentence definition
2. `## Core principle` — the single most important insight
3. `## When to invoke` — trigger conditions (bullet list)
4. `## How to apply` — step-by-step or guidance
5. `## Anti-patterns` — common misapplications
6. `## Source` — book title and author

**Hard constraint**: No agent names, agent JD references, or other skill references in any model file.

### SKILL.md contract

- Lists all model files grouped by category
- Each entry: model name → one-line trigger description → relative file path
- No agent names, no cross-skill references
- No YAML frontmatter with agent/skill metadata beyond `name` and `description`

### Agent JD `## Mental Models` section contract

Each updated JD section must contain:
- 4 universal models: Circle of Competence, Inversion, Second-Order Thinking, Probabilistic Thinking
- 1 role-specific model (per D5 role assignments)
- For each model: a role-calibration paragraph explaining how it applies to that agent's specific work
- File path links to the corresponding model files

## MoSCoW

| Category | Items |
| -------- | ----- |
| **Must have** | SKILL.md catalog; 10 model files in correct category subfolders; 6-section schema per file; bottom-layer constraint enforced |
| **Should have** | 5 agent JD `## Mental Models` sections (Ron, Mark, Graeme, Peter, Matt) |
| **Could have** | `resolving-pr-issues` skill refactor (5-Whys pointer) |
| **Won't have (this time)** | Kabilan JD update; models beyond the 10 listed; automated enforcement hooks; model files for frameworks beyond Ron's 4+1 selection |

## Phased Delivery

### Phase 0: Skill library foundation

**Goal**: Create the `mental-models/` skill folder with `SKILL.md` and all 10 model files. The library is complete and self-contained — no agent JD changes yet.

**Deliverables**:

1. `.agents/skills/mental-models/SKILL.md` — pure catalog, 10 entries, no agent names
2. `.agents/skills/mental-models/general_thinking/circle-of-competence.md`
3. `.agents/skills/mental-models/general_thinking/inversion.md`
4. `.agents/skills/mental-models/general_thinking/second-order-thinking.md`
5. `.agents/skills/mental-models/general_thinking/probabilistic-thinking.md`
6. `.agents/skills/mental-models/root_cause_analysis/five-whys.md`
7. `.agents/skills/mental-models/strategic_decisions/reversible-vs-irreversible.md`
8. `.agents/skills/mental-models/strategic_decisions/ooda-loop.md`
9. `.agents/skills/mental-models/self_awareness/cognitive-biases.md`
10. `.agents/skills/mental-models/risk_analysis/black-swan.md`
11. `.agents/skills/mental-models/communication/third-story.md`

**Verification**:

```powershell
# All 10 model files exist
Get-ChildItem .agents/skills/mental-models/ -Recurse -Filter *.md | Where-Object { $_.Name -ne 'SKILL.md' } | Measure-Object
# Expected: Count = 10

# No agent names in any model file
Select-String -Path .agents/skills/mental-models/**/*.md -Pattern 'rl\.ron|rl\.mark|rl\.graeme|rl\.peter|rl\.matt|Kabilan|Harriet|Linda'
# Expected: no matches

# All 6 sections present in circle-of-competence.md (spot check)
Select-String -Path .agents/skills/mental-models/general_thinking/circle-of-competence.md -Pattern '## What it is|## Core principle|## When to invoke|## How to apply|## Anti-patterns|## Source'
# Expected: 6 matches
```

**Acceptance Gate** (both must pass before Phase 1 starts):
- [ ] 10 model files exist (11 including SKILL.md)
- [ ] Zero agent-name matches in model files

---

### Phase 1: Agent JD updates

**Goal**: Add `## Mental Models` section to each of the 5 advisory/expert agent JDs.

**Deliverables**:

1. `.github/agents/rl.ron.agent.md` — `## Mental Models` section with 4 universal + Reversible vs. Irreversible
2. `.github/agents/rl.mark.agent.md` — `## Mental Models` section with 4 universal + Cognitive Biases
3. `.github/agents/rl.graeme.agent.md` — `## Mental Models` section with 4 universal + Black Swan
4. `.github/agents/rl.peter.agent.md` — `## Mental Models` section with 4 universal + OODA Loop
5. `.github/agents/rl.matt.agent.md` — `## Mental Models` section with 4 universal + Third Story

**Verification**:

```powershell
# Spot check: Ron's JD has all 5 models
Select-String -Path .github/agents/rl.ron.agent.md -Pattern 'circle-of-competence|inversion|second-order-thinking|probabilistic-thinking|reversible-vs-irreversible'
# Expected: 5 matches

# All 5 JDs have the section header
Select-String -Path .github/agents/rl.*.agent.md -Pattern '## Mental Models'
# Expected: 5 matches (one per file)
```

**Acceptance Gate**:
- [ ] All 5 JDs contain `## Mental Models` with correct model references

---

### Phase 2: `resolving-pr-issues` refactor

**Goal**: Strip inline 5-Whys description from `resolving-pr-issues`; replace with pointer to `five-whys.md`.

**Deliverables**:

1. `.agents/skills/resolving-pr-issues/SKILL.md` — `5 Whys` references replaced with link
2. `.agents/skills/resolving-pr-issues/procedures/resolve-comments.md` — Step 5 updated

**Verification**:

```powershell
# Confirm reference link present
Select-String -Path .agents/skills/resolving-pr-issues/SKILL.md -Pattern 'five-whys'
# Expected: 1+ matches
```

**Acceptance Gate**:
- [ ] `resolving-pr-issues/SKILL.md` contains a link to `five-whys.md`

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
