---
applyTo: "docs/**"
---

# Visual Artifacts Policy (Markdown vs Miro)

Markdown is canonical for narrative and decision artifacts. Miro is canonical for relational
and spatial artifacts. PM skills declare which medium they own; `miro-mcp` is the rendering
toolset, not a skill that decides what to render.

| Artifact | Canonical medium | Owner |
|---|---|---|
| Strategic bets, OKRs, positioning, GTM plan | Markdown | Ron |
| PRDs, problem statements, hypotheses, decision logs | Markdown | Mark |
| Geotechnical domain knowledge | Markdown (`docs/knowledge/geotechnical/`) | Graeme |
| Roadmaps, opportunity solution trees, story maps, journey maps | **Miro** (Markdown synthesis optional) | Mark (Ron contributes strategic thread) |
| Customer archetypes / personas | **Hybrid**: Miro for collaborative drafting; Markdown canonical reference | Mark + Ron |
| Prioritization matrices (RICE / MoSCoW / Value-Effort) | **Miro** matrix or spreadsheet; Markdown table for the final ranking | Mark |
| Marketing campaigns, content briefs, signal reports, editorial calendar, style guide | Markdown (`docs/product/marketing/`) | John |
| Content Segmentation Grid (content x persona x buying-cycle stage) | **Miro** matrix; Markdown index in `docs/product/marketing/` | John |
| Design specifications, interaction pattern docs | Markdown (`docs/product/design/`) | Matt |
| Wireframes, user flows, annotated mockups | **Miro** (Markdown design spec canonical) | Matt |
| ADRs, architecture documents, shaped Pitches | Markdown | Peter |
| Evaluation rubric structures | Markdown (`docs/evaluation/`) | Peter (Graeme approves domain content) |
| Production code, tests, scripts | Code (`src/rl/`, `tests/`, `scripts/`) | Kabilan |

Do not auto-mirror every Markdown artifact to Miro -- mirror on demand. Drift starts when both
surfaces try to be canonical for the same content.
