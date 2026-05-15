---
name: mermaid-diagrams
description: Use when adding or reviewing a Mermaid diagram in any Markdown or Quarto document — covers diagram type selection, syntax constraints (v8.8.0 ceiling), when-to-diagram rules, and quality standards.
---

# Mermaid Diagrams

Governs all Mermaid diagram usage in this repo: type selection, v8.8.0 syntax constraints, and quality rules.

## Boundary Contract

### Applies To
- Any `.md` or `.qmd` document where a diagram aids comprehension
- Plans, research docs, PRDs, decision logs, architecture docs, codemaps

### Produces
- Mermaid code blocks that render in VS Code (Office Viewer plugin) and GitHub

### Does Not Cover
- Miro-based spatial artifacts — `miro-mcp` is canonical for roadmaps, story maps, journey maps
- Statistical plots — `eda-visual-design`, `python-plot-colors`
- Table rendering — `qmd-tables`
- Quarto narrative — `qmd-narrative-design`

## Version Ceiling: 8.8.0

The VS Code Office Viewer plugin supports Mermaid **<= 8.8.0**. All syntax must be valid
under this version. Hard dependency — not a preference.

## Quick Reference — Supported Types

**Load the relevant procedure file before drawing.** All types not listed here are
post-8.8.0 and will not render.

| Type | Keyword | Use when | Procedure |
|---|---|---|---|
| Flowchart | `flowchart` | Business process, decision tree, system flow | `procedures/flowchart.md` |
| Sequence | `sequenceDiagram` | Runtime interactions between actors | `procedures/sequence-class-state-erd.md` |
| Class | `classDiagram` | Code-level structure of a component | `procedures/sequence-class-state-erd.md` |
| State | `stateDiagram-v2` | Lifecycle states and transitions | `procedures/sequence-class-state-erd.md` |
| ER | `erDiagram` | Relational database schemas | `procedures/sequence-class-state-erd.md` |
| C4 | `flowchart` (approx.) | Software architecture levels | `procedures/c4-diagrams.md` |
| Gantt | `gantt` | Project timelines | — |
| Pie | `pie` | Proportional breakdown (≤5 categories) | — |
| User Journey | `journey` | UX flow with emotional arc | — |

**Banned (post-8.8.0):** `mindmap`, `timeline`, `quadrantChart`, `sankey`, `xychart`,
`block`, `kanban`, `architecture`, `zenuml`, `C4Context`, `requirementDiagram`, `gitGraph`.

## When to Diagram

**Use** when content involves: entity relationships, flows with branching, actor
interactions, state transitions, timelines, or decision trees.

**Do NOT use** when:
- A bullet list or table is more concise
- Fewer than 3 nodes
- Linear sequence, ≤5 steps, no branching
- Duplicates a canonical Miro artifact (see Visual Artifacts Policy in `AGENTS.md`)
- Purely decorative

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using a banned post-8.8.0 type | Check the Quick Reference table |
| Drawing a numbered list as a flowchart | No branching + ≤5 steps → use a list |
| Missing title heading above diagram block | Add a Markdown heading directly above stating context and type |
| Bi-directional arrows (`<-->`) | Model as two separate directed, labelled edges |
| Special characters in labels (`--`, `—`, `–`) | See `procedures/flowchart.md` and `procedures/syntax.md` |
| Colour without a legend | Add a Markdown bullet list below the block naming each colour |

Per-type mistakes: see the relevant procedure file. Cross-type syntax: `procedures/syntax.md`.
