# Quickstart: Running the Spike

**Date**: 2026-06-13 | **Plan**: [plan.md](plan.md)

Operator manual for executing the spike on Mon Jun 22 (appetite: 1 working day).

## Prerequisites

- Desktop Microsoft Word (Microsoft 365) on Windows.
- Permission to install add-ins from the Office Store (if blocked, this is the
  day's first escalation — see plan Risk Register; Word on the web is the fallback
  surface).

## Steps

1. **Install Script Lab** (one-time): in Word, `Home > Add-ins` (or `Insert >
   Get Add-ins`), search "Script Lab", install. Entry point: `aka.ms/getscriptlab`.
2. **Import the snippet**: open the Script Lab pane, `Import`, paste the contents
   of `docs/research/20260622-185-officejs-spike/snippet.yaml` (or build it there
   and export to that path when done — the committed YAML is the deliverable).
3. **Open a blank document**, then in the Script Lab Run pane press the buttons in
   order, reading the console section at the bottom of the pane after each:
   1. `Seed` — inserts the sample paragraph (3 known occurrences: one word twice,
      a second word once).
   2. `Find` — expect 3 match lines (two of them for the repeated word) +
      `total: 3` (issue #186).
   3. `Mark` — expect 3 bounding boxes in the document + `created: 3`; press again
      and expect `created: 0, existing: 3` (issue #187).
   4. `Replace` — expect the document text to change + a before/after console pair
      (issue #188).
4. **Negative case**: open a fresh blank document (do NOT seed), run `Find`, expect
   `total: 0` and no error.
5. **Capture evidence**: paste each stage's console output into
   `docs/research/20260622-185-officejs-spike/evidence.md` under the matching issue
   heading; note the Word build (`File > Account > About Word`) and which marking
   mechanism worked.

## Verification checklist (read-off)

- [ ] `[find] total: 3` with 3 match lines (US1-1)
- [ ] `[find] total: 0`, no error, on unseeded doc (US1-2)
- [ ] Repeated word reported per occurrence (US1-3)
- [ ] 3 visible bounding boxes + `created: 3` (US2-1)
- [ ] Re-run: `created: 0`, total unchanged (US2-2)
- [ ] Replacement readable on mark (control header title) (US2-3)
- [ ] Document text changed + before/after pair logged (US3-1)

All seven boxes checked = spike complete; children #186/#187/#188 close by linking
their evidence sections.
