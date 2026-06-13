# Research: Office.js Spike — Scan, Mark, Replace in Script Lab

**Date**: 2026-06-13 | **Spec**: [spec.md](spec.md)

Research sources (founder-directed for this run): NotebookLM "MS Word Taskpane Add-in
Development" notebook, NotebookLM "Office Open XML (OOXML) File Formats" notebook,
context7 (`/officedev/office-js-docs-reference`), and Microsoft Learn via web search.
Notebook answers are citation-backed; gaps the notebooks declared ("Not covered in
sources") were closed with context7/Microsoft Learn, per the issue's own instruction
to confirm the search API against Microsoft Learn.

## R1 — Document search mechanism

- **Decision**: Use the platform text search (`body.search(text, options)`) with
  `matchWholeWord: true`, `matchCase: false`, `matchWildcards: false` as the starting
  options; the find stage logs the semantics actually observed.
- **Rationale**: Closes the documented #186 knowledge gap. Confirmed present in
  WordApi 1.1 (every supported Word build). Full option set per context7/Microsoft
  Learn: `ignorePunct`, `ignoreSpace`, `matchCase`, `matchPrefix`, `matchSuffix`,
  `matchWholeWord`, `matchWildcards`. Literal (non-wildcard) search avoids the
  escaping rabbit hole entirely. Whole-word + case-insensitive matches the spec's
  edge-case decisions ("assess" must not match "assessment"; "Assess" must match).
- **Alternatives considered**: Client-side regex over `body.text` — rejected: #186
  no-go (real matching is the #196 endpoint's job) and it returns strings, not Range
  objects, so marking would need a second location pass. Paragraph iteration with
  manual splitting — rejected: reimplements search with more sync round-trips.

## R2 — Proxy-object batching (load/sync)

- **Decision**: Each stage queues `load()` for exactly the properties it will read
  (e.g., `text` on found ranges), then `await context.sync()` once, then reads.
- **Rationale**: Notebook-confirmed (cited): a Range is a proxy object; reading a
  property before load+sync throws an exception. Three steps: queue load → sync →
  read. One sync per batch keeps the same-word-multiple-occurrences case (#186
  rabbit hole) inside a single round-trip: load the collection's items, sync once,
  iterate.
- **Alternatives considered**: None viable — platform requirement.

## R3 — Marking mechanism

- **Decision**: Wrap each found range in a **Rich Text content control**
  (`range.insertContentControl()`), set `appearance: "BoundingBox"`, a distinct
  `color`, `title` = suggested replacement (visible on the control header), `tag` =
  machine-readable marker encoding the matched word (e.g., `redline-taboo:<word>`).
- **Rationale**: #187 fixes this as the grounded primary mechanism. All required
  properties are WordApi 1.1 — the requirement-set risk flagged in #185/#187 rabbit
  holes is effectively eliminated for the primary path (web-confirmed). The tag
  doubles as the idempotency marker (R5) and the title carries the replacement
  metadata demanded by the spec (FR-006).
- **Alternatives considered**: Comments API — WordApi 1.4, explicitly fallback-only
  per #187 no-go ("do not build both"); built only if content controls fail live.
  Font/style change — visible but carries no metadata and makes idempotency
  detection fragile; rejected.

## R4 — Content control appearance enum discrepancy

- **Decision**: Valid `appearance` values are `"BoundingBox" | "Tags" | "Hidden"`
  (Microsoft Learn). The notebook tutorial's mention of `"None"` is treated as
  stale/erroneous.
- **Rationale**: Microsoft Learn's enum reference is authoritative and current;
  source-conflict resolution recorded here per the source-reconciliation hook.
- **Alternatives considered**: Trusting the notebook text — rejected; it is tutorial
  prose, not the API reference.

## R5 — Idempotency on re-run (mark stage)

- **Decision**: Before creating marks, query
  `ContentControlCollection.getByTag(<tag>)`, load, sync, and count. Ranges already
  inside a tagged control are skipped; the console reports `created` vs `existing`
  so the re-run count is read-off-verifiable (unchanged total).
- **Rationale**: #187 AC2 accepts "idempotent or detected" — detection by tag is the
  cheapest grounded route. OOXML notebook confirms the tag persists in the document
  (`<w:sdtPr><w:tag>`), so detection survives across runs and document saves.
- **Alternatives considered**: Delete-all-then-remark — mutates more of the document
  and risks losing user content on a bug; rejected. In-memory tracking — lost
  between snippet runs; rejected.

## R6 — Replace semantics inside a marked range

- **Decision**: Target the marked control via `getByTag(...).getFirst()`, replace
  its content text with `insertText(replacement, "Replace")`, log the before/after
  pair, and additionally observe and report what happens to the control wrapper
  (kept with new text / cleared / removed) — that observation is itself spike
  evidence for #188's rabbit hole.
- **Rationale**: Notebook tutorial grounds the getByTag → getFirst → insert pattern
  and the "Replace" location semantics ("replaces the text of the existing range").
  The #188 rabbit hole (control may need removing/updating after replace) becomes
  an observed, reported outcome instead of an unknown.
- **Alternatives considered**: Replacing via a fresh search hit instead of the
  control — loses the connection to the mark and risks an orphaned wrapper around
  stale text; rejected as primary (kept as fallback observation if control-based
  replace misbehaves).

## R7 — Sample document seeding

- **Decision**: The snippet includes a setup action that inserts a known paragraph
  containing exactly 3 occurrences of listed words — one word twice and a second
  word once — into the open (blank) document, so the repeated-occurrence scenario
  (US1 scenario 3) is verifiable from the standard seed.
- **Rationale**: Spec FR-002/Assumption: self-contained, repeatable read-off
  baseline on any machine; no hand-prepared document to drift.
- **Alternatives considered**: Manual seeding instructions — error-prone, breaks
  the "read-off not judgment" verification mode; rejected.

## R8 — Snippet structure inside Script Lab

- **Decision**: ONE snippet with one button per stage — Seed, Find, Mark, Replace —
  each button bound to an async function wrapped in `tryCatch`, all output via
  `console.log` (renders in Script Lab's console section at the bottom of its task
  pane). Declared `api_set: WordApi 1.1`. No external libraries.
- **Rationale**: Children #187/#188 both say "extend the Script Lab snippet" —
  resolving #185's "one snippet (or three small ones)" to one snippet, staged.
  Script Lab style rules (notebook-cited): button → async function → tryCatch;
  snippets capped at a few hundred lines; hard-coded data of a few hundred
  characters is acceptable — the 3-5 word list is well inside that.
- **Alternatives considered**: Three separate snippets (one per child issue) —
  duplicates the word list and seed logic three times and triples drift risk;
  rejected by the children's own wording.

## R9 — Word build / requirement sets

- **Decision**: Primary path declares and needs only WordApi 1.1; the comments
  fallback would need WordApi 1.4. The run log records the Word build used.
- **Rationale**: Microsoft Learn requirement-set pages (web-confirmed): search,
  insertContentControl, appearance, color, getByTag, insertText are all 1.1;
  `Range.insertComment` is 1.4. Current Microsoft 365 desktop Word supports both.
- **Alternatives considered**: Feature-detecting at runtime — unnecessary ceremony
  for a one-day spike when the floor is 1.1; the recorded build covers the
  evidence need.

## R10 — Spike artifact location

- **Decision**: Committed spike outputs live at
  `docs/research/20260622-185-officejs-spike/` — `snippet.yaml` (Script Lab share
  export) and `evidence.md` (console transcripts + observations per child issue).
- **Rationale**: Follows the #174 precedent (spike outputs to `docs/research/`).
  The spec directory holds specification artifacts, not implementation evidence.
  Committing the YAML makes the snippet importable by anyone via Script Lab's
  import, feeding #197.
- **Alternatives considered**: New top-level `spikes/` directory — a structure
  decision with no second consumer yet; rejected. Issue comments only — not
  version-controlled alongside the repo; rejected as sole home (issue comments may
  still reference the files).
