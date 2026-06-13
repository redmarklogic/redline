# Contract: Snippet Console Output

**Date**: 2026-06-13 | **Plan**: [plan.md](plan.md)

The snippet's only external interface is the structured text it prints to the
Script Lab console. Humans verify acceptance by reading these lines (spec FR-011);
child issues #186/#187/#188 close by pointing at them. Line shapes below are the
contract; exact wording may vary but every CAPITALIZED field MUST appear.

## Seed stage

```text
[seed] inserted sample text with OCCURRENCE_COUNT occurrences (WORD x N, ...)
```

- `OCCURRENCE_COUNT` MUST be 3.

## Find stage (#186)

```text
[find] match MATCH_INDEX: "MATCHED_TEXT" (word: LIST_WORD)
[find] total: TOTAL_COUNT
```

- One `match` line per found occurrence — multiple occurrences of one word each get
  their own line (US1 scenario 3).
- Seeded document: `TOTAL_COUNT` = 3 (US1 scenario 1).
- Document without listed words: no `match` lines, `total: 0`, and no error output
  (US1 scenario 2).
- SHOULD log observed match semantics once per run:
  `[find] options: matchWholeWord=true matchCase=false`.

## Mark stage (#187)

```text
[mark] created: CREATED_COUNT, existing: EXISTING_COUNT, total marked: TOTAL_MARKED
```

- First run on seeded doc: `created: 3, existing: 0, total marked: 3` (US2 scenario 1).
- Re-run: `created: 0, existing: 3, total marked: 3` — unchanged total proves
  idempotency (US2 scenario 2).
- Each mark carries `title` = replacement, `tag` = `redline-taboo:<word>` — metadata
  inspectability (US2 scenario 3) is verified on the control header in the document
  or via an optional `[mark] tagged: TAG title: REPLACEMENT` line.

## Replace stage (#188)

```text
[replace] before: "BEFORE_TEXT" after: "AFTER_TEXT"
[replace] control state: STATE_NOTE
```

- Exactly one replacement is performed (US3 scenario 1).
- `STATE_NOTE` reports what happened to the mark wrapper after replacement
  (kept with new text / cleared / removed) — observed evidence for #188's rabbit
  hole, no particular outcome prescribed.

## Error shape (all stages)

```text
[STAGE] ERROR: VERBATIM_PLATFORM_ERROR
```

- A clean 0-match Find run is NOT an error and MUST NOT print this line.
