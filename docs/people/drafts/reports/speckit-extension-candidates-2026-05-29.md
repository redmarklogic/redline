# Spec-Kit Extension Candidates — Evaluation Report

**Date**: 2026-05-29
**Evaluator**: Harriet (Head of People & Agent Development)
**Procedure**: `customization-mechanism-triage/procedures/speckit-extension-triage.md`

---

## Tier 1 — Strong Candidates (All Three Questions = YES)

### verification-before-completion

**Current form**: Skill in `.agents/skills/verification-before-completion/SKILL.md`
**Proposed hook point**: `after_implement`

**Q1 — Lifecycle trigger**: YES — fires after spec-kit implement phase completes.
The skill's stated purpose is "before claiming work is complete" which maps directly
to the end of the implement phase.

**Q2 — Structural enforcement**: YES — the skill uses "Iron Law" language:
"NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE." It demands a gate,
not guidance.

**Q3 — Forgetting = failure**: YES — if an agent forgets to load this skill after
implement, the verification gate disappears silently. No pre-commit hook or test
catches "claiming done without running tests." Kabilan's JD says "MUST load" this
skill, confirming it has been a convention-enforcement problem.

**Decision**: **Extension** — `after_implement` mandatory hook
**Hook type**: mandatory (`optional: false`)
**Recommendation**: Augment (keep skill for non-spec-kit contexts; extension hook
for spec-kit workflows)

---

### python-static-checks

**Current form**: Skill in `.agents/skills/python-static-checks/SKILL.md`
**Proposed hook point**: `after_implement`

**Q1 — Lifecycle trigger**: YES — fires after implement phase. Kabilan's JD:
"MUST run python-static-checks before considering any task complete."

**Q2 — Structural enforcement**: YES — Kabilan's JD uses "MUST" language.
AGENTS.md says "Always finish by using the python-static-checks skill."
Convention-only enforcement.

**Q3 — Forgetting = failure**: YES — if skipped, lint/type errors ship silently.
Pre-commit hooks catch some issues at commit time, but the spec-kit implement
phase can produce multiple commits — the gate should fire after the full phase,
not per-commit.

**Decision**: **Extension** — `after_implement` mandatory hook
**Hook type**: mandatory (`optional: false`)
**Recommendation**: Augment (keep skill; add extension hook). Can combine with
verification-before-completion into a single `quality-gates` extension.

---

### brainstorming

**Current form**: Skill in `.agents/skills/brainstorming/SKILL.md`
**Proposed hook point**: `before_specify` (optional)

**Q1 — Lifecycle trigger**: YES — the spec-kit skill documents brainstorming as
"transitions to spec-kit as terminal state." It runs before specify starts.

**Q2 — Structural enforcement**: YES — the skill has a HARD-GATE: "Do NOT invoke
any implementation skill... until you have presented a design and the user has
approved it."

**Q3 — Forgetting = failure**: YES — if skipped, features enter the spec-kit
pipeline without exploration. The brainstorming skill's anti-pattern section
("This Is Too Simple To Need A Design") documents this failure mode explicitly.

**Decision**: **Extension** — `before_specify` optional hook
**Hook type**: optional (`optional: true`)
**Optional prompt**: "Run brainstorming session before specifying? (Recommended
for new features; skip for well-defined tasks.)"
**Recommendation**: Augment (keep skill for standalone use; extension hook
prompts before specify)

---

### requesting-code-review

**Current form**: Skill in `.agents/skills/requesting-code-review/SKILL.md`
**Proposed hook point**: `after_implement`

**Q1 — Lifecycle trigger**: YES — fires after implementation completes.
The subagent-driven-development skill mandates "two-stage review after each task."

**Q2 — Structural enforcement**: YES — the skill says review is "Mandatory"
after completing major features and before merge.

**Q3 — Forgetting = failure**: YES — without review, code ships unreviewed.
Currently depends on agent discipline to dispatch the review subagent.

**Decision**: **Extension** — `after_implement` optional hook
**Hook type**: optional (`optional: true`)
**Optional prompt**: "Dispatch code review before finalizing?"
**Recommendation**: Augment. Can bundle into the `quality-gates` extension
alongside static checks and verification.

---

## Tier 2 — Good Candidates (Embedded Logic or Gate Enforcement)

### Source Document Reconciliation (spec-kit SKILL.md §)

**Current form**: 40+ lines of prose inside `spec-kit/SKILL.md`
**Proposed hook point**: `before_specify`

**Q1 — Lifecycle trigger**: YES — explicitly runs "before specify."
**Q2 — Structural enforcement**: YES — "run a reconciliation pass BEFORE
writing any spec content."
**Q3 — Forgetting = failure**: PARTIAL — reconciliation is valuable but
the specify agent can still produce a spec without it. Drift is introduced
silently, but not always caught.

**Decision**: **Extension candidate** — `before_specify` mandatory hook
**Recommendation**: Extract from skill prose into a standalone extension
command. Lower priority than Tier 1.

---

### shaping (gate enforcement)

**Current form**: Skill in `.agents/skills/shaping/SKILL.md` + Peter's JD
constraint: "No unshaped work enters SpecKit"
**Proposed hook point**: `before_specify` (mandatory, blocking)

**Q1 — Lifecycle trigger**: YES — runs before specify. The two-touch model
explicitly gates specify on a shaped Pitch existing.
**Q2 — Structural enforcement**: YES — Peter's JD says "no unshaped work
enters SpecKit." Currently a JD bullet, not a structural gate.
**Q3 — Forgetting = failure**: YES — if the gate is skipped, unscoped
features enter the pipeline, causing mid-sprint scope explosions.

**Decision**: **Extension** — `before_specify` mandatory hook
**Hook type**: mandatory (`optional: false`)
**Recommendation**: Extension checks for a shaped Pitch in `specs/shaped/`
before allowing specify to proceed. The shaping skill itself stays
(it teaches how to shape); the extension enforces that shaping happened.

---

### Concept-to-Plan Phase Mapping (spec-kit SKILL.md §)

**Current form**: Prose in `spec-kit/SKILL.md`
**Proposed hook point**: `after_plan`

**Q1 — Lifecycle trigger**: YES — fires after plan generation.
**Q2 — Structural enforcement**: PARTIAL — "the plan MUST start with an
explicit mapping table" but no gate enforces this.
**Q3 — Forgetting = failure**: PARTIAL — missing mapping causes confusion
but does not break the pipeline.

**Decision**: **Extension candidate** — lower priority
**Recommendation**: Keep as prose for now. Revisit after Tier 1 extensions
prove the pattern.

---

## Tier 3 — Keep as Skills

### finishing-a-development-branch

**Q1**: YES (after implement). **Q2**: Moderate. **Q3**: NO — it is the
natural next step and rarely forgotten. Other mechanisms (branch hygiene)
catch issues.
**Decision**: Keep as skill.

### systematic-debugging

**Q1**: NO — reactive, triggered by failures, not lifecycle events.
**Decision**: Keep as skill.

### subagent-driven-development

**Q1**: NO — this IS the execution engine, not a gate or check.
**Decision**: Keep as skill.

### test-driven-development

**Q1**: NO — methodology embedded in how code is written, not a lifecycle event.
Enforced through task ordering in templates (already handled by preset).
**Decision**: Keep as skill.

### python-* coding skills

**Q1**: NO — coding conventions, no lifecycle trigger.
**Decision**: Keep as skills.

---

## JD Constraints That Could Become Extension Hooks

| Agent | JD Constraint | Hook Point | Type |
|---|---|---|---|
| Kabilan | "Read all ADRs before starting cycle work" | `before_plan` | Mandatory |
| Kabilan | "Consult UI Terminology Glossary before using geotechnical terms" | `after_specify` | Mandatory |
| Kabilan | "Check docs/product/design/ for relevant design spec" | `before_implement` | Mandatory |

These are lower priority than the skill-level candidates above. They would
require extracting JD bullets into extension commands that scan specific
directories, which adds complexity.

---

## Recommended Implementation Order

1. **`quality-gates` extension** — combines `verification-before-completion`,
   `python-static-checks`, and `requesting-code-review` as `after_implement`
   hooks. One extension, three checks. Low risk, high value.

2. **`brainstorming` extension** — `before_specify` optional hook. Prompts
   before every new spec.

3. **`shaping-gate` extension** — `before_specify` mandatory hook. Checks
   for shaped Pitch existence.

4. **`source-reconciliation` extension** — `before_specify` mandatory hook.
   Extracted from spec-kit SKILL.md prose.

---

## Next Step

Awaiting Peter's architectural review of these recommendations before
drafting `extension.yml` manifests.

---

## Peter's Architectural Review (2026-05-29)

### Verdicts

| Candidate | Peter's Verdict |
|---|---|
| `verification-before-completion` | **Approved** — strongest candidate |
| `python-static-checks` | **Approved** |
| `brainstorming` | **Rejected as extension** — redundant with shaping gate; no useful firing window at `before_specify` |
| `requesting-code-review` | **Downgraded to Tier 2** — already embedded in `subagent-driven-development` execution model |
| `shaping-gate` | **Approved with conditions** — ship as optional initially, needs manual Pitch mapping + small-task bypass, flip mandatory after 3+ Pitches exist |
| Source Reconciliation | **Approved** — clean migrate from prose |
| JD constraints (ADRs, glossary, design specs) | **Rejected** — agent-specific workflow steps, not pipeline-universal gates |

### Bundling Decision

**Split, not bundle.** Peter rejects the `quality-gates` mega-extension. Reasons:
1. Mixed enforcement levels (mandatory + optional in one extension)
2. Internal ordering dependency (static checks must pass before verification)
3. Single Responsibility — each check answers a different question

Revised structure:

| Extension | Hook | Type | Order |
|---|---|---|---|
| `static-checks` | `after_implement` | mandatory | Runs first |
| `verification-gate` | `after_implement` | mandatory | Runs second |

### Shaping Gate Design Constraints (Peter)

Three problems Peter identified:
1. **Pitch-to-spec mapping undefined** — start with manual assertion (user confirms which Pitch), automate later
2. **Small task bypass essential** — must include documented exemption with rationale logging
3. **Cold start** — `specs/shaped/` is currently empty; mandatory gate blocks all work. Ship optional, flip mandatory after 3+ Pitches

### Triage Procedure Fixes Applied

1. Step 4 cross-check added: "If this procedure fires at a spec-kit lifecycle point, also evaluate step 6"
2. Q3 reframed from "forgetting = failure" (subjective) to "sole gate" (structurally testable)

### Revised Implementation Order

1. `static-checks` extension — `after_implement`, mandatory
2. `verification-gate` extension — `after_implement`, mandatory (after static-checks)
3. `shaping-gate` extension — `before_specify`, optional (upgrade after 3+ Pitches)
4. `source-reconciliation` extension — `before_specify`, mandatory (migrate from prose)
