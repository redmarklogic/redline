# Spec-Kit Extension Triage Procedure

Evaluate whether a skill (new or existing) or JD constraint should become a
spec-kit extension instead of (or in addition to) a standalone skill.

**Load this procedure** whenever creating a new skill, updating an existing skill,
or writing a JD constraint that interacts with the spec-kit workflow.

---

## When to Run This Triage

- Creating a new skill that mentions "before/after" a spec-kit phase
- Updating an existing skill whose language implies a lifecycle gate ("MUST run",
  "Iron Law", "NO X WITHOUT Y")
- Writing a JD constraint that references spec-kit phases (specify, plan, tasks,
  implement, analyze)
- Reviewing existing skills for extension migration candidates

---

## The Three-Question Test

All three must be YES for a spec-kit extension recommendation.

### Q1: Lifecycle Trigger — Does it fire at a specific spec-kit workflow event?

Spec-kit lifecycle points:

| Phase | Before Hook | After Hook |
|---|---|---|
| Constitution | `before_constitution` | `after_constitution` |
| Specify | `before_specify` | `after_specify` |
| Clarify | `before_clarify` | `after_clarify` |
| Plan | `before_plan` | `after_plan` |
| Tasks | `before_tasks` | `after_tasks` |
| Analyze | `before_analyze` | `after_analyze` |
| Implement | `before_implement` | `after_implement` |
| Checklist | `before_checklist` | `after_checklist` |
| Tasks to Issues | `before_taskstoissues` | `after_taskstoissues` |

**YES signals:**
- "Run X after implement completes" → `after_implement`
- "Verify Y before specify starts" → `before_specify`
- "Check Z after spec is written" → `after_specify`

**NO signals:**
- "Apply to all Python files" (no specific lifecycle event)
- "Use when debugging" (reactive, not lifecycle-bound)
- "Follow this pattern when writing classes" (coding convention)

### Q2: Structural Enforcement > Convention — Does the skill demand enforcement
      that convention cannot guarantee?

**YES signals:**
- Language like "Iron Law", "MUST", "NO X WITHOUT Y", "Gate", "mandatory"
- The skill describes itself as a quality gate or verification step
- The skill says "before claiming done" or "before proceeding"
- The JD constraint says "MUST run before considering any task complete"

**NO signals:**
- Language like "prefer", "consider", "when applicable"
- The skill provides guidance, not enforcement
- Compliance is valuable but not critical

### Q3: Sole Gate — Is this skill the only enforcement mechanism?

Reframed as a structural test (not historical anecdote): is there ANY other
enforcement mechanism that catches the same failure independently of this skill
being loaded?

**YES (this skill is the sole gate) signals:**
- No pre-commit hook, CI check, test, or instruction catches the same failure
- If an agent forgets to load this skill, the quality gate disappears silently
- No redundant enforcement exists anywhere in the pipeline

**NO (redundant enforcement exists) signals:**
- Pre-commit hooks or tests catch the same issue independently
- A `.instructions.md` file enforces the same rule passively
- Another skill or JD constraint provides equivalent coverage
- The skill provides design guidance, not a verification step

---

## Decision Matrix

| Q1 Lifecycle | Q2 Structural | Q3 Sole Gate | Recommendation |
|---|---|---|---|
| YES | YES | YES | **Spec-kit extension** — migrate or create as extension |
| YES | YES | NO | **Extension candidate** — evaluate ROI; redundant enforcement may suffice |
| YES | NO | * | **Skill with hook awareness** — keep as skill, document the lifecycle point for agent routing |
| NO | * | * | **Not an extension** — use skill, instruction, or other mechanism per main triage tree |

---

## Evaluation Template

Copy this template when evaluating a candidate:

```markdown
### [Skill/JD Constraint Name]

**Current form**: [Skill in `.agents/skills/` / JD bullet / prose in spec-kit SKILL.md]
**Proposed hook point**: [e.g., `after_implement`]

**Q1 — Lifecycle trigger**: [YES/NO] — [evidence]
**Q2 — Structural enforcement**: [YES/NO] — [evidence: quote the "MUST"/"Iron Law" language]
**Q3 — Sole gate**: [YES/NO] — [evidence: is there any other mechanism (pre-commit, CI, test, instruction) that catches this independently?]

**Decision**: [Extension / Extension candidate / Keep as skill / Not applicable]
**Hook type**: [mandatory / optional]
**Optional prompt**: [If optional: "Run X before proceeding?"]
```

---

## Extension Structure Reference

When the triage recommends a spec-kit extension:

```
.specify/extensions/<ext-id>/
  extension.yml          # Manifest: hooks, config, requirements
  README.md              # Usage docs
  commands/              # Extension commands (markdown)
    <command>.md
```

Register hooks in `.specify/extensions.yml` (project root):

```yaml
hooks:
  after_implement:
    - extension: "quality-gates"
      command: "speckit.quality-gates.verify"
      optional: false
      description: "Run static checks and verification"
  before_specify:
    - extension: "shaping-gate"
      command: "speckit.shaping-gate.check"
      optional: true
      prompt: "Check for shaped Pitch before specifying?"
      description: "Verify shaped work exists"
```

---

## Existing Skill Migration

When an existing skill is identified as an extension candidate:

1. Evaluate using the three-question test above
2. Document the evaluation using the template
3. Decide whether to **migrate** (replace skill with extension) or **augment**
   (keep skill for non-spec-kit contexts, add extension hook for spec-kit contexts)
4. If migrating: the extension command can reference the skill's content, but the
   hook fires automatically instead of requiring agent memory
5. If augmenting: the skill stays for general use; the extension hook calls the
   same verification logic during spec-kit workflows

**Augment** is the safer default for existing skills that have value outside spec-kit.
**Migrate** only when the skill is exclusively a spec-kit lifecycle gate.

---

## Relationship to Other Triage Steps

This procedure is step 6 in the `customization-mechanism-triage` decision tree.
It runs after checking: instruction (step 1), VS Code hook (step 2), custom agent
(step 3), skill (step 4), prompt file (step 5).

If a capability matches both "skill" (step 4) and "spec-kit extension" (step 6),
prefer the spec-kit extension when all three questions are YES. The skill form
provides convention-based enforcement; the extension form provides structural
enforcement. Structural wins when enforcement is critical.
