---
name: ceremony-monthly-editorial-session
description: Use when running the monthly editorial session triggered by a new Ground Engineering magazine issue, or when the user asks to process the latest Ground Engineering issue for content and product signals.
---

# Monthly Editorial Session

## Boundary Contract

### Inputs

- Latest Ground Engineering magazine issue
- Access to `ground-engineering-magazine` NotebookLM notebook
- Current Dream 100 target list
- Current editorial calendar (`docs/product/marketing/editorial-calendar.md`) — created by this ceremony if absent

### Outputs

- 2-3 approved post angles queued in `docs/product/marketing/editorial-calendar.md`
- Each post angle tagged with its Big 5 category
- 1-paragraph product signal note filed to Mark
- Updated Dream 100 commenting notes
- Session date and issue reference logged

### Out of Scope

- Content writing (`marketing-content-big-5`)
- Strategy decisions (`pm-product-strategist`)
- Code implementation

## Procedure

This ceremony is a multi-agent orchestration workflow. The full procedure lives in a
prompt file that can be invoked directly.

**To run:** type `/monthly-editorial-session` in chat.
