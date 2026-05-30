# Quickstart: Mental Models Skill

**Feature**: 008-mental-models | **Date**: 2026-05-27

---

## Adding a new mental model

1. **Choose the right category subfolder** from the taxonomy in `data-model.md`. If none fits, add a new subfolder and update `SKILL.md`.

2. **Create the file** at `.agents/skills/mental-models/<category>/<slug>.md` using kebab-case slug. <!-- mental-model-link: allow -->

3. **Use the 6-section template**:

```markdown
# <Model Name>

## What it is
<1-2 sentence definition. No agent names.>

## Core principle
<Single most important insight, 1 paragraph.>

## When to invoke
- <Trigger condition 1>
- <Trigger condition 2>
- <Add more as needed>

## How to apply
1. <Step 1>
2. <Step 2>
3. <Step 3>

## Anti-patterns
- **<Misapplication name>**: <Brief explanation of why this is wrong and what to do instead.>
- **<Second misapplication>**: <Brief explanation.>

## Source
*<Book Title>* — <Author(s)>, <Chapter/Section if known>
```

4. **Add an entry to `SKILL.md`** in the correct category section:
```markdown
- [Model Name](<category>/<slug>.md) — <one-line trigger description>
```

5. **Verify** the file conforms to the schema contract (see `contracts/model-file-schema.md`):
```powershell
Select-String -Path .agents/skills/mental-models/<category>/<slug>.md `
  -Pattern '## What it is|## Core principle|## When to invoke|## How to apply|## Anti-patterns|## Source'
# Expected: 6 matches
```

---

## Adding a model to an agent JD

1. Locate the agent JD at `.github/agents/rl.<name>.agent.md`.

2. Add or update the `## Mental Models` section. It **must** include:
   - All 4 universal models (Circle of Competence, Inversion, Second-Order Thinking, Probabilistic Thinking)
   - The agent's assigned role-specific model (see `data-model.md` assignment table)
   - A calibration paragraph per model using a domain-specific example from that agent's work

3. Link each model to its file: `.agents/skills/mental-models/<category>/<slug>.md` <!-- mental-model-link: allow -->

4. Do **not** copy model definitions into the JD — only the calibration paragraph belongs there.

---

## Referencing a model from another skill

When another skill needs to reference a mental model (e.g., `resolving-pr-issues` referencing 5 Whys):

```markdown
Apply the [5 Whys](../../mental-models/root_cause_analysis/five-whys.md) root-cause method.
```

Use a relative path. Do not inline the model definition — the canonical text lives in the model file.

---

## Verification checklist (after any change)

```powershell
# 1. All model files exist
Get-ChildItem .agents/skills/mental-models/ -Recurse -Filter *.md |
  Where-Object { $_.Name -ne 'SKILL.md' } | Measure-Object
# Expected: Count matches number of entries in SKILL.md

# 2. No agent names in model files
Select-String -Path .agents/skills/mental-models/**/*.md `
  -Pattern 'rl\.ron|rl\.mark|rl\.graeme|rl\.peter|rl\.matt'
# Expected: no matches

# 3. All 6 sections present (spot check one file)
Select-String -Path .agents/skills/mental-models/general_thinking/circle-of-competence.md `
  -Pattern '## What it is|## Core principle|## When to invoke|## How to apply|## Anti-patterns|## Source'
# Expected: 6 matches
```
