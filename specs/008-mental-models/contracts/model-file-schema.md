# Model File Schema Contract

**Contract type**: Structural schema — every mental model file must conform to this.
**Enforced by**: Manual review + grep verification (SC-001, SC-006)

---

## Required sections

Every file at `.agents/skills/mental-models/<category>/<slug>.md` must contain
these six H2 headings in this exact order:

```
## What it is
## Core principle
## When to invoke
## How to apply
## Anti-patterns
## Source
```

Verification command:
```powershell
Select-String -Path .agents/skills/mental-models/**/*.md `
  -Pattern '## What it is|## Core principle|## When to invoke|## How to apply|## Anti-patterns|## Source'
# Each file must produce 6 matches
```

---

## Forbidden content

| Pattern | Reason |
|---------|--------|
| Agent names (`Ron`, `Mark`, `Graeme`, `Peter`, `Matt`, `Kabilan`, `Harriet`, `Linda`) | Bottom-layer constraint — model files must not know about agents |
| Agent JD file references (`rl.*.agent.md`) | Same reason |
| Skill file references (e.g., `resolving-pr-issues`, `systematic-debugging`) | Same reason; cross-references only via Anti-patterns section by filename |
| YAML frontmatter | Model files are plain Markdown; no frontmatter |

Verification command:
```powershell
Select-String -Path .agents/skills/mental-models/**/*.md `
  -Pattern 'rl\.ron|rl\.mark|rl\.graeme|rl\.peter|rl\.matt|rl\.kabilan|rl\.harriet|rl\.linda'
# Expected: no matches
```

---

## SKILL.md catalog contract

`SKILL.md` must pass all of the following:

1. Contains YAML frontmatter with `name: mental-models` and a non-empty `description`
2. Every model file listed in `SKILL.md` exists at the stated relative path
3. Every model file in the folder tree is listed in `SKILL.md` (no orphans)
4. No agent names in body text
5. No references to other skill SKILL.md files
