---
name: ceremony-monthly-editorial-session
description: Use when running the monthly editorial session triggered by a new Ground Engineering magazine issue, or when the user asks to process the latest Ground Engineering issue for content and product signals.
---

# Monthly Editorial Session

## Boundary Contract

### Inputs
- Latest Ground Engineering magazine issue

### Outputs
- Content signals at `docs/product/marketing/`
- Product signals routed to Ron and Mark

### Out of Scope
- Content writing (`marketing-content-big-5`)
- Strategy decisions (`pm-product-strategist`)
- Code implementation

## Overview

A structured ceremony that processes each new Ground Engineering magazine issue through
the advisory board to produce LinkedIn post angles, product signal notes, and Dream 100
commenting intelligence. The founder drives the session; each advisory board member
contributes within their lane.

## When to Use

- A new Ground Engineering issue has dropped and needs processing.
- The user asks to "run the editorial session" or "process the latest issue."
- It is time for the monthly editorial cadence (within 5 business days of a new issue).

## Inputs

Before the session starts, the founder must have:

1. Read the new Ground Engineering issue and identified 3-5 notable topics.
2. Access to the `ground-engineering-magazine` NotebookLM notebook.
3. The current Dream 100 target list.
4. The current editorial calendar (`docs/product/marketing/editorial-calendar.md`).
   If this file does not yet exist, the first session creates it.

## Session Flow

The session runs in five phases. Each phase has a designated lead and clear handoff.

### Phase 1 -- Archive Queries (Founder-led, via NotebookLM)

The founder runs Track A queries from `docs/product/marketing/archive-intelligence.md`
against the `ground-engineering-magazine` notebook. Use the `redline-research` skill to
query the notebook.

**Query sequence (run in order):**

1. **Resonance query:** "What topics in this issue have appeared in previous issues?
   How has the framing or proposed solution changed over time?"
2. **Novelty query:** "What topics in this issue have NOT appeared in any previous issue?"
3. **Dream 100 commenting query:** For each active Dream 100 target's recent posts,
   query: "What has Ground Engineering published about [this topic] across the archive?"

Collect all query results before proceeding to Phase 2.

### Phase 2 -- Technical Validation (Graeme)

Hand the query results to Graeme. Graeme's job in this phase:

- **NZ/AU applicability filter:** Ground Engineering is UK-focused. Graeme confirms
  which surfaced topics are relevant to NZ/AU practice. Topics that fail this filter
  are discarded -- they do not proceed to Phase 3.
- **Technical accuracy check:** Flag any claims or framings that are technically
  inaccurate or misleading for the NZ/AU market.
- **Standards mapping:** Note which NZ/AU standards (NZS 3910, AS 4000, NZGS guidance)
  connect to the surviving topics.

**Invoke:** "Graeme, review these Ground Engineering topics for NZ/AU relevance."

### Phase 3 -- Big 5 Mapping and Post Angle Drafting (John)

Hand Graeme's filtered topics to John. John's job:

- **Map every surviving topic to a Big 5 category.** The five categories are: Pricing
  and Costs, Problems, Versus and Comparisons, Reviews, Best in Class. Topics that do
  not map to any Big 5 category are discarded. No exceptions.
- **Draft 2-3 post angles** from the mapped topics.
- **Tag any post angle that contains a technical claim** for Graeme's async review.
- **Update Dream 100 commenting notes** with commenting intelligence from Phase 1.

**Invoke:** "John, map these topics to Big 5 and draft post angles."

### Phase 4 -- Product Signal Extraction (Mark)

From the same session material, Mark extracts product signals:

- Write a **1-paragraph product signal note** capturing any insight relevant to
  Pre-Review rules, Standards Knowledge Store, or user workflow.
- If a signal is bet-level (affects strategic bets), flag it for
  `docs/product/strategy/decisions/parked-decisions.md`.

**Invoke:** "Mark, extract product signals from this editorial session."

### Phase 5 -- Strategic Check (Ron, only if needed)

Ron is invoked only if:

- A product signal from Phase 4 touches a strategic bet or kill criterion.
- A topic surfaces a potential new bet or contradicts an existing one.
- The founder wants a positioning check on a post angle.

**Invoke:** "Ron, review this signal against our strategic bets."

If none of these conditions apply, skip Phase 5.

## Outputs Checklist

Every editorial session must produce all of the following before closing:

- [ ] 2-3 approved post angles queued in `docs/product/marketing/editorial-calendar.md`
- [ ] Each post angle tagged with its Big 5 category
- [ ] Any technical claims tagged for Graeme's async review
- [ ] 1-paragraph product signal note filed to Mark
- [ ] Updated Dream 100 commenting notes
- [ ] Session date and Ground Engineering issue reference logged

If any output is missing, the session is not complete.

## Invisibility Protocol (Binding)

The Ground Engineering archive is **never** cited as a personal corpus on any external
surface. This is a hard rule from `docs/product/marketing/archive-intelligence.md`.

During the session, agents may freely reference the archive internally. But every
external-facing output (post angles, LinkedIn drafts) must:

- Frame insights as **pattern observations**, not archive citations.
- Never say "I read in Ground Engineering that..." or "according to a 2016 article..."
- Let Graeme be the credibility source for technical claims.

**Test before publishing:** "Could a senior NZ geotech engineer who reads Ground
Engineering conclude the founder holds 15 years of systematic coverage?" If yes,
rewrite the angle.

## Handoff Summary

```
Founder (reads issue, runs archive queries)
    |
    v
Graeme (NZ/AU filter, technical validation)
    |
    v
John (Big 5 mapping, post angles, Dream 100 notes)
    |
    v
Mark (product signal extraction)
    |
    v
Ron (strategic check -- only if triggered)
```

## Reference Documents

- `docs/product/operations/cadences.md` -- Monthly Editorial Session entry
- `docs/product/marketing/archive-intelligence.md` -- Track A query sequence
- `docs/product/strategy/gtm/content-engine.md` -- Big 5 rubric, voice constraints
- `docs/product/marketing/README.md` -- Hard rules (especially rule 6: invisibility)
- `redline-research` skill -- NotebookLM query procedure

## Common Mistakes

| Mistake | Fix |
|---|---|
| Skipping Graeme's NZ/AU filter | UK topics served to NZ/AU audience. Always run Phase 2. |
| Posting angles that do not map to Big 5 | Kill gate is absolute. No Big 5 category = discard. |
| Citing Ground Engineering as a corpus externally | Invisibility protocol violation. Rewrite as pattern observation. |
| John querying geotechnical notebooks directly | John is forbidden from querying engineering notebooks. Founder runs queries; Graeme validates. |
| Skipping the product signal note to Mark | Track A feeds Track B. Missing signal = missing product intelligence. |
| Running the session without reading the issue first | Founder must pre-read and identify 3-5 topics before the session starts. |
