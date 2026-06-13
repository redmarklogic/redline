# Implementation Plan: Office.js Spike — Scan, Mark, Replace in Script Lab

**Date**: 2026-06-13 | **Spec**: [spec.md](spec.md)
**Status**: Draft

## Summary

This spike proves the three Word-document primitives the Sprint 4 proof of concept
depends on — find a word, mark it visibly, replace it — using the Office JavaScript
API (Office.js, Microsoft's JavaScript interface for manipulating open Office
documents) inside Script Lab (a free Microsoft add-in that runs JavaScript snippets
against the open document with no server, manifest, or certificates). The deliverable
is one Script Lab snippet with four buttons (Seed, Find, Mark, Replace) plus an
evidence file of console read-offs; each stage satisfies one child issue (issues
186, 187, 188). Nothing here touches the Python codebase: the spike is throwaway-grade
evidence generation whose value is de-risking the sprint's wiring task (#197) before
any infrastructure exists.

## Technical Context

> Preset defaults (Python 3.14, uv, pytest, import-linter) do **not** apply: this
> feature produces no code under `src/`, no package, and no Python. The fields below
> are restated for this spike's actual surface.

**Language**: JavaScript (TypeScript-flavored) inside a Script Lab snippet — no
local toolchain, no build step, no npm (Constitution XVII compliant: zero second
toolchain; the snippet lives in Script Lab and is exported as a YAML document)
**Package manager**: none (Script Lab supplies Office.js; no snippet libraries)
**Testing**: human read-off of structured console output per the spec's
`[human-verify]` acceptance scenarios — pytest N/A (no Python artifact)
**Project layout**: monorepo (`.specify/architecture.yml`) — untouched by this spike
**Runtime**: desktop Microsoft Word (Microsoft 365) on Windows, Script Lab add-in
**API floor**: WordApi 1.1 requirement set (primary path); WordApi 1.4 only if the
comments fallback is ever exercised
**Key platform APIs**: `body.search` + `SearchOptions`, `Range.insertContentControl`,
`ContentControl.{appearance,color,title,tag}`, `ContentControlCollection.getByTag`,
`Range.insertText`

## Constitution Check

| Principle | Assessment |
|---|---|
| XVII All-Python toolchain | PASS — snippet runs inside Script Lab; no Node/npm/compiler enters the repo; committed artifact is a YAML document + markdown evidence |
| VIII Determinism over LLM inference | PASS — word list is hard-coded placeholder data; the real registry arrives via #195 |
| II Hook-first enforcement | N/A — no new project rule introduced |
| XIV Platform obligation | N/A — artifact executes in desktop Word on the developer's Windows machine only |
| XVIII Stateless core | N/A — no `src/` code touched |
| Shaped Pitch before SpecKit | SATISFIED — issue #185 body is the shaped Pitch (problem, solution outline, appetite, rabbit holes, no-gos), supplied by founder via the /spec-kit invocation |
| **Accepted Risk** `[red-team-skipped]` | Red-team gate keyword scan matched category `contracts` on the words "interface" (spec assumption: console output is the operator interface) and "downstream" (issue cross-reference). Waived: the spike exposes no API boundary, payload, or schema — the API contract is #194, explicitly out of scope here. No findings report produced. |

## Design Decisions

| #  | Decision | Choice | Rationale |
| -- | -------- | ------ | --------- |
| D1 | Snippet structure | One snippet, four buttons (Seed / Find / Mark / Replace), `api_set: WordApi 1.1` | Children #187/#188 say "extend the snippet"; stages independently runnable per spec FR-013 ([research R8](research.md)) |
| D2 | Search | `body.search(word, {matchWholeWord: true, matchCase: false})` per listed word; no wildcards | WordApi 1.1; literal search avoids escaping; matches spec edge cases (R1) |
| D3 | Marking | Rich Text content control: `appearance "BoundingBox"`, distinct color, `title` = replacement, `tag` = `redline-taboo:<word>` | Grounded primary per #187; all WordApi 1.1; tag powers idempotency (R3, R5) |
| D4 | Idempotency | Detect existing marks via `getByTag` count; skip wrapped ranges; report `created/existing` | #187 AC2 "idempotent or detected"; tag persists in OOXML `<w:sdtPr><w:tag>` (R5) |
| D5 | Replace | `getByTag(...).getFirst()` → `insertText(replacement, "Replace")`; log before/after; report control state after replace | Notebook-grounded pattern; turns #188's rabbit hole into reported evidence (R6) |
| D6 | Seeding | Seed button inserts a known paragraph with exactly 3 occurrences (one word twice + a second word once) | Self-contained, repeatable baseline; repetition built in so US1 scenario 3 reads off the standard seed; spec FR-002 (R7) |
| D7 | Console schema | Stage-prefixed structured lines (see [contracts/console-output.md](contracts/console-output.md)) | Verification is read-off, not judgment (FR-011); child issues close by pointing at lines |
| D8 | Artifact home | `docs/research/20260622-185-officejs-spike/` — `snippet.yaml` + `evidence.md` | #174 precedent: spike outputs to `docs/research/` (R10) |
| D9 | Comments fallback | Build ONLY if content controls fail live in Word; requires WordApi 1.4 | #187 no-go: never build both (R3, R9) |

## Domain Impact

**Modularity assessment**: N/A — no package under `src/` is created or modified.
**New packages**: None.
**Bounded context changes**: None.
**Import-linter contract updates**: None.
**Subdomain classification**: Generic (platform-capability evidence; no domain model).
**New domain terms**: taboo word: a word the product flags for replacement in a
geotechnical report; mark: a visible bounded annotation wrapping a flagged word and
carrying its suggested replacement.

## Architecture

Stage flow (each button = one `Word.run` batch; every read follows load → sync → read
per the proxy-object rule, [research R2](research.md)):

```text
[Seed]    insert known paragraph (3 occurrences of listed words)
   |
[Find]    for each of 3-5 listed words:
            body.search(word, {matchWholeWord, !matchCase})
          load found ranges' text -> ONE context.sync()
          log each match text + running total        --> closes #186
   |
[Mark]    existing = getByTag count (idempotency guard)
          wrap each unwrapped found range:
            insertContentControl(); appearance=BoundingBox;
            color; title=replacement; tag=redline-taboo:<word>
          log created / existing / total             --> closes #187
   |
[Replace] control = getByTag(tag).getFirst()
          before = control text; insertText(replacement, "Replace")
          log before/after + control state           --> closes #188
```

Failure path: if content-control creation throws on the installed Word build, stop,
log the error verbatim, and only then implement the comments fallback (D9). "Any
visible marking" is acceptable per founder ruling; the evidence file records which
mechanism worked.

## Domain Models

No Pydantic/Pandera models — the only data shape is the hard-coded snippet constant:

```js
// word -> suggested replacement (placeholder pairs; real dictionary = #195)
const TABOO = [
  { word: "...", replacement: "..." },  // 3-5 entries, Graeme-agnostic placeholders
];
const TAG_PREFIX = "redline-taboo:";
```

## MoSCoW

| Category | Items |
| -------- | ----- |
| **Must have** | Seed action (exactly 3 occurrences); Find: per-match text + total, 0-match clean exit; Mark: bounding-box+color controls with replacement in title/tag, created-count log, idempotent re-run; Replace: one marked word swapped with before/after log; single snippet, zero infrastructure; evidence.md read-offs per child issue |
| **Should have** | Log observed match semantics (case/whole-word behavior); log Word build + requirement-set availability; report control state after replace |
| **Could have** | Reset action (remove marks/seed for clean demo re-runs); comments-fallback probe — only on primary-path failure |
| **Won't have (this time)** | Served taskpane/manifest/certs (#189-#193); API endpoint or network calls (#194/#196/#197); real dictionary (#195); client-side regex; Fluent UI; wired Fix button; both marking mechanisms built together |

## Phased Delivery

> Appetite: all three phases inside ONE working day (Mon Jun 22), per issue/children.
> "TDD approach" for this spike = acceptance-by-console: each phase's acceptance
> scenarios are read off the Script Lab console and captured into `evidence.md`.
> pytest gates are N/A (no Python artifact; nothing under `src/` or `tests/`).

### Phase 0: Snippet skeleton + Seed + Find (US1, #186)

**Goal**: Running snippet in Script Lab that seeds the sample text and reports every
occurrence of listed words with a total count — the load/sync pattern proven.

**Verification approach**: Console read-off vs US1 scenarios 1-3 (3 matches with
texts; 0-match clean; per-occurrence reporting).

**Deliverables**:

1. `docs/research/20260622-185-officejs-spike/snippet.yaml` — Seed + Find buttons,
   TABOO constant, tryCatch wrapper, `api_set: WordApi 1.1`
2. `docs/research/20260622-185-officejs-spike/evidence.md` — section "#186" with
   console transcript (3-match run and 0-match run)

**Verification**:

```text
In Word: Script Lab > import snippet > Seed > Find
Console shows: [find] lines for each occurrence + "[find] total: 3"
New blank doc (no seed): Find shows "[find] total: 0" and no error
```

**Acceptance Gate** (must pass before Phase 1):

- [ ] US1 scenarios 1-3 read off the console and pasted into evidence.md

---

### Phase 1: Mark (US2, #187)

**Goal**: Found ranges visibly marked with bounded, colored controls carrying the
replacement metadata; re-run provably creates no duplicates.

**Verification approach**: Visual check (3 bounding boxes) + console read-off vs US2
scenarios 1-3; re-run count unchanged.

**Deliverables**:

1. `snippet.yaml` extended — Mark button with idempotency guard (D3, D4)
2. `evidence.md` section "#187" — created/existing counts for first and second run;
   note on metadata visibility (title on control header)

**Verification**:

```text
Mark once: 3 boxes visible; console "[mark] created: 3, existing: 0, total: 3"
Mark again: console "[mark] created: 0, existing: 3, total: 3" (count unchanged)
```

**Acceptance Gate** (must pass before Phase 2):

- [ ] US2 scenarios 1-3 read off and captured; marking mechanism that worked is named

---

### Phase 2: Replace (US3, #188)

**Goal**: One marked word replaced with its suggestion; document text visibly
changed; before/after pair logged; control-state-after-replace observed.

**Verification approach**: Console read-off vs US3 scenario 1 + document observation.

**Deliverables**:

1. `snippet.yaml` extended — Replace button (D5)
2. `evidence.md` section "#188" — before/after pair + control state note; closing
   summary listing Word build and requirement sets observed

**Verification**:

```text
Replace: document shows replacement text;
console "[replace] before: "<taboo>" after: "<replacement>"" + control state line
```

**Acceptance Gate** (spike complete):

- [ ] US3 scenario 1 read off and captured
- [ ] evidence.md has one closable read-off section per child issue (#186/#187/#188)

## File Inventory

| Phase | New Files | Count |
| ----- | --------- | ----- |
| 0 | `docs/research/20260622-185-officejs-spike/snippet.yaml`, `.../evidence.md` | 2 |
| 1 | (extends both) | 0 |
| 2 | (extends both) | 0 |

**Total new**: 2 | **Total deleted**: 0

## Library Best Practices

<!-- Populated from Context7 + Microsoft Learn review (see research.md) -->

### office.js (Script Lab-provided; WordApi 1.1 floor)

- **Import path**: none — Script Lab injects Office.js; snippet declares
  `api_set: WordApi 1.1`
- **API gotchas**:
  - Proxy objects: reading `range.text` before `load()` + `await context.sync()`
    throws — queue loads, sync once, then read (notebook-cited)
  - `ContentControlAppearance` enum is `BoundingBox | Tags | Hidden` — the value
    `"None"` from older tutorial text is not valid (Microsoft Learn authoritative)
  - `body.insert*` methods lack "Before"/"After" locations (cannot insert outside
    body); Range.insertText supports `Replace | Start | End | Before | After`
  - `SearchOptions`: `ignorePunct, ignoreSpace, matchCase, matchPrefix, matchSuffix,
    matchWholeWord, matchWildcards` — leave `matchWildcards` false for literal terms
- **Confirmed pattern** (find→mark core):

  ```js
  const results = body.search(word, { matchWholeWord: true, matchCase: false });
  results.load("items/text");
  await context.sync();
  results.items.forEach(r => {
    const cc = r.insertContentControl();
    cc.appearance = "BoundingBox"; cc.color = "red";
    cc.title = replacement; cc.tag = TAG_PREFIX + word;
  });
  await context.sync();
  ```

## Risk Register

| Risk | Mitigation |
| ---- | ---------- |
| Script Lab install blocked by org add-in policy | Check first thing Monday (store install is the spike's step 1); Script Lab also runs in Word on the web as a same-day fallback surface |
| `body.search` semantics surprise (punctuation, smart quotes in seed text) | Seed text is snippet-controlled plain prose; observed semantics logged as a Should-have; options documented in research R1 |
| Marking API unsupported/odd on installed build | Primary path is WordApi 1.1 (floor for every supported build); founder ruling accepts any visible marking; fallback = comments (1.4), built only on failure (D9) |
| Multiple occurrences of one word mishandled across sync | Load collection items once, single sync, iterate (R2); US1 scenario 3 verifies |
| Replace leaves orphaned/odd control wrapper | Explicitly observed and reported as evidence (D5); any clean visible result acceptable |
| Snippet outgrows Script Lab size limits | Stages share helpers; word list is tiny; Script Lab cap is a few hundred lines (notebook-cited) — well clear |

## Glossary

| Term | Definition |
| ---- | ---------- |
| taboo word | A word the product flags in a geotechnical report as needing replacement. |
| suggested replacement | The preferred wording paired with a taboo word. |
| mark | A visible bounded annotation wrapping a flagged word in the document, carrying its replacement. |
| seed text | Snippet-inserted sample prose containing exactly 3 known taboo-word occurrences. |
| read-off verification | Accepting a check by reading structured console output, not by judgment. |
| spike | A timeboxed throwaway-grade experiment that buys knowledge, not production code. |
| appetite | The fixed time budget for the work (here: 1 working day, Mon Jun 22). |
