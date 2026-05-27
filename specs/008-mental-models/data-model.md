# Data Model: Mental Models Skill

**Phase 1 output** | **Feature**: 008-mental-models | **Date**: 2026-05-27

---

## Entity 1 — Mental Model File

**Path pattern**: `.agents/skills/mental-models/<category>/<slug>.md`

**Required sections** (in this order):

| Section | Required | Content |
|---------|----------|---------|
| `## What it is` | Yes | 1-2 sentence definition. No agent names. |
| `## Core principle` | Yes | Single most important insight, 1 paragraph. |
| `## When to invoke` | Yes | Bullet list of trigger conditions. Min 2 triggers. |
| `## How to apply` | Yes | Numbered steps or structured guidance. |
| `## Anti-patterns` | Yes | 2+ common misapplications with brief explanation. |
| `## Source` | Yes | Book title, author, and relevant chapter/section if known. |

**Hard constraints**:
- No YAML frontmatter (plain Markdown)
- No agent names (Ron, Mark, Graeme, Peter, Matt, Kabilan, Harriet, Linda)
- No references to agent JD files (`rl.*.agent.md`)
- No references to other skill files (`resolving-pr-issues`, `systematic-debugging`, etc.)
- Cross-references to other mental model files: permitted in `## Anti-patterns` only, by filename

---

## Entity 2 — SKILL.md Catalog

**Path**: `.agents/skills/mental-models/SKILL.md`

**Required frontmatter**:
```yaml
---
name: mental-models
description: "..."
---
```

**Required body structure**:
```markdown
# Mental Models
<one-paragraph description of the library>

## <Category Name>
- [Model Name](<relative/path/to/file.md>) — <one-line trigger description>
```

**Hard constraints**:
- No agent names anywhere in the file
- No `applyTo` or agent-routing frontmatter fields
- No references to other skill files
- Every model file listed must exist at the stated path

---

## Entity 3 — Agent JD `## Mental Models` Section

**Applies to**: `rl.ron.agent.md`, `rl.mark.agent.md`, `rl.graeme.agent.md`, `rl.peter.agent.md`, `rl.matt.agent.md`

**Required structure**:
```markdown
## Mental Models

Load `.agents/skills/mental-models/SKILL.md` when applying these models.

### Universal Models (all advisory agents)

**[Model Name]** — [one-line description]. See [`<category>/<slug>.md`](.agents/skills/mental-models/<category>/<slug>.md).

> **[Agent role] calibration**: [1-2 sentences: how this model applies specifically to this agent's work, with a concrete example from their domain]

[Repeat for all 4 universal models]

### Role-Specific Model

**[Model Name]** — [one-line description]. See [`<category>/<slug>.md`](.agents/skills/mental-models/<category>/<slug>.md).

> **Calibration**: [1-2 sentences: why this model was assigned to this role; what failure mode it addresses]
```

**Hard constraints**:
- Must reference all 4 universal models: Circle of Competence, Inversion, Second-Order Thinking, Probabilistic Thinking
- Must include exactly 1 role-specific model per the D5 assignment table
- Each model must include a calibration paragraph with a domain-specific example
- Each model must link to its file in `.agents/skills/mental-models/`

---

## Entity 4 — Role-to-Model Assignment Table

| Agent | Role-specific model | Failure mode addressed |
|-------|--------------------|-----------------------|
| Ron | Reversible vs. Irreversible Decisions | Strategic bets accumulate without reversibility grading |
| Mark | Cognitive Biases (Confirmation + Sunk Cost) | PRD writing is most vulnerable to advocacy-over-evidence |
| Graeme | Black Swan | Geotechnical = tail-risk domain; past experience underweights extreme events |
| Peter | OODA Loop | Over-deliberation on architectural decisions; needs time-bounded decision cadence |
| Matt | Third Story | Design requires negotiating across user/founder/PM perspectives |

---

## Category Taxonomy

| Subfolder | Models |
|-----------|--------|
| `general_thinking/` | circle-of-competence, inversion, second-order-thinking, probabilistic-thinking |
| `root_cause_analysis/` | five-whys |
| `strategic_decisions/` | reversible-vs-irreversible, ooda-loop |
| `self_awareness/` | cognitive-biases |
| `risk_analysis/` | black-swan |
| `communication/` | third-story |
