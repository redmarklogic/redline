# Version Guard Report — Skipped

Generated: 2026-06-13T00:00:00+12:00 (session date; clock not sampled)

No dependency sources found (no lockfile, package.json, or tech stack decision record).

This feature is a Script Lab snippet spike: it has no package manifest by design
(zero infrastructure is FR-012). The npm-oriented steps of version guard therefore
skip. The platform version surface that DOES constrain this feature is recorded
below so that `speckit.version-guard.load` has real constraints to re-load before
tasks and implementation.

## Supplemental Platform Constraints (authoritative for this feature)

| Capability | Minimum requirement set | Status on current Microsoft 365 Word |
|---|---|---|
| Document body text search (`body.search` + `SearchOptions`) | WordApi 1.1 | Available |
| Wrap range in rich text content control (`insertContentControl`) | WordApi 1.1 | Available |
| Content control `appearance` ("BoundingBox") and `color` | WordApi 1.1 | Available |
| Content control retrieval by tag (`getByTag`) | WordApi 1.1 | Available |
| Text replacement (`Range.insertText` location "Replace") | WordApi 1.1 | Available |
| Comments API (`Range.insertComment`) — fallback path only | WordApi 1.4 | Available |

## Compatibility Rules (mandatory)

| # | DON'T | DO instead |
|---|-------|------------|
| 1 | Read any proxy-object property (e.g., `range.text`) before it is loaded | Queue `load()` for the needed properties, `await context.sync()`, then read |
| 2 | Use content control appearance value `"None"` (notebook tutorial text; not in the current enum) | Use `"BoundingBox"`, `"Tags"`, or `"Hidden"` per Microsoft Learn |
| 3 | Enable `matchWildcards` and pass unescaped user text | Keep `matchWildcards` false; search literal words |
| 4 | Declare the snippet `api_set` higher than needed | Declare `WordApi 1.1` for the primary path (comments fallback would raise it to 1.4) |
| 5 | Pull libraries into the snippet without pinned versions | Pin exact versions in the Script Lab libraries pane (Script Lab style rule); none are expected to be needed |

## Migration References

- WordApi 1.1 requirement set: https://learn.microsoft.com/en-us/javascript/api/requirement-sets/word/word-api-1-1-requirement-set
- ContentControlAppearance enum: https://learn.microsoft.com/en-us/javascript/api/word/word.contentcontrolappearance
- Script Lab overview: https://learn.microsoft.com/en-us/office/dev/add-ins/overview/explore-with-script-lab
