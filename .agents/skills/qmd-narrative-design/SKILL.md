---
name: qmd-narrative-design
description: Use when designing Quarto reports or presentations -- Hook-Problem-Insight-Proof-Action arc, slide composition, speaker notes, or writing quality for revealjs or HTML/PDF output
---

# QMD Narrative Design

## Boundary Contract

### Applies To
- Quarto `.qmd` documents for external audiences (presentations, reports, memos)

### Produces
- Narrative structure following Hook-Problem-Insight-Proof-Action arc

### Does Not Cover
- Table rendering (`qmd-tables`)
- Plot construction (`eda-visual-design`)
- Data quality screening (`eda-interpreting-data`)

## 1. Ask Before You Generate

Before generating any content, ask up to three clarifying questions. Do not produce
slides, sections, or narrative until you have the answers. Enumerate options where
the choice is not obvious.

**Always ask:**

| #   | Question                                                                                                                            | Why it matters                                                                      | Default if not answered       |
| --- | ----------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------- |
| 1   | **Who is the audience?** General (non-specialist), technically informed (domain practitioner), or highly specialised (expert peer)? | Controls jargon level, definition density, and how much technical detail to include | Assume technically informed   |
| 2   | **What is the single key message?** One plain-English sentence the audience should be able to repeat after leaving the room.        | Everything in the document must serve this message. If it doesn't, cut it.          | Ask — do not assume           |
| 3   | **What is the format and length constraint?** (e.g., 20-minute talk, 15-slide deck, 4-page memo, open-ended report)                 | Governs slide count, section depth, and how much evidence to include                | Ask — do not assume           |
| 4   | **What type of presentation?** Client progress update, conference/technical, or general briefing? _(Presentations only)_            | Selects the structural template from Rule 3.6                                       | Assume client progress update |

Do not ask all four if context already provides the answer. Use the codebook,
spec, or existing document structure to resolve any question you can answer yourself.

---

## 2. Shared Principles (Presentation and Report)

These rules apply regardless of output format.

## 3. Presentation Mode (revealjs)

Apply these rules in addition to the shared principles for any revealjs deck.

## 4. Report Mode (HTML / PDF / typst)

Apply these rules in addition to the shared principles for narrative reports,
technical memos, and EDA documents.

## Quick Checklist


See `procedures/qmd-narrative-design.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Opening a presentation with an agenda slide | Lead with the hook (the problem or surprising insight); agendas kill engagement before it starts |
| Putting too many bullets on a slide | Maximum 3 bullet points per slide; move detail to speaker notes |
| Writing all sections before asking the clarifying questions | Run the intake questions first; generating content without audience context produces the wrong narrative |