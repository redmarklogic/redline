# Tasks: Office.js Spike — Scan, Mark, Replace in Script Lab

**Input**: [plan.md](plan.md)
**Prerequisites**: spec.md, research.md, data-model.md, contracts/console-output.md,
quickstart.md, version-guard-report.md (compatibility rules are binding)

<!-- Task sizing rule: each task is a VERTICAL SLICE -- front-to-back, one complete
     new behaviour, nothing left dangling. Split by user-visible behaviour.
     Appetite for the whole list: ONE working day (Mon Jun 22). -->

> Spike-specific note: there is no `src/` code and no pytest surface. The preset's
> pytest gates are conditional ("if function files modified") — the condition is
> never met here; each phase gate instead verifies the spec's `[human-verify]`
> read-offs and that the diff stays inside `docs/research/` + `specs/`. Execution is
> human-in-the-loop (Word GUI + Script Lab); tasks are sequential within one snippet
> file except where marked [P].

## Phase 0: Snippet skeleton + Seed + Find (US1, closes #186)

**Purpose**: A running Script Lab snippet that seeds the sample text and reports
every listed-word occurrence with a total — the load/sync pattern proven live.

- [x] T001 [Phase 0] Install Script Lab from the Office Store in desktop Word and confirm the console section renders (quickstart.md prerequisites + step 1); if org policy blocks install, escalate immediately (plan Risk Register) and fall back to Word on the web
- [x] T002 [P] [Phase 0] Create `docs/research/20260622-185-officejs-spike/evidence.md` skeleton with headings: Environment, Issue #186, Issue #187, Issue #188
- [x] T003 [Phase 0] Build the snippet skeleton in Script Lab — four buttons (Seed, Find, Mark, Replace) each wired to an async function in a tryCatch wrapper, `api_set: WordApi 1.1`, `TABOO` constant (3-5 word/replacement pairs) and `TAG_PREFIX = "redline-taboo:"` — and export via Share > Copy to `docs/research/20260622-185-officejs-spike/snippet.yaml`
- [x] T004 [Phase 0] Implement Seed in `docs/research/20260622-185-officejs-spike/snippet.yaml`: insert one plain-prose paragraph containing exactly 3 occurrences of listed words (one word twice + a second word once, per spec FR-002); log the `[seed]` line per contracts/console-output.md
- [x] T005 [Phase 0] Implement Find in `docs/research/20260622-185-officejs-spike/snippet.yaml`: for each TABOO word run `body.search(word, {matchWholeWord: true, matchCase: false})`, load `items/text`, ONE `context.sync()`, then log one `[find] match` line per occurrence, the `[find] options` line, and `[find] total` per contract; a 0-match run must end cleanly with `total: 0` and no error line

### Acceptance Gate (hard stop — do not start Phase 1 until green)

- [x] T006 [Phase 0] Verify read-offs in Word and paste transcripts into evidence.md section "Issue #186": (a) seeded doc → 3 match lines + `total: 3`; (b) fresh unseeded doc → `total: 0`, no error; (c) a repeated word reported once per occurrence
- [x] T007 [Phase 0] Pytest gate not triggered — confirm the working-tree diff touches only `docs/research/` and `specs/` (zero-infrastructure check, spec FR-012)

---

## Phase 1: Mark found ranges (US2, closes #187)

**Purpose**: Every found occurrence visibly marked with a bounded, colored control
carrying its replacement; re-runs provably create no duplicates.

- [x] T008 [Phase 1] Implement Mark in `docs/research/20260622-185-officejs-spike/snippet.yaml`: idempotency guard first (`getByTag` count per word, load + sync), then for each unwrapped found range `insertContentControl()` with `appearance = "BoundingBox"`, distinct `color`, `title` = replacement, `tag` = `TAG_PREFIX + word`; log `[mark] created/existing/total marked` per contract (plan D3/D4) — implemented with a refinement found at verify: per-occurrence tags (`TAG_PREFIX + word + ":" + index`) + a paired `font.highlightColor` for reading-view visibility (see evidence.md #187)
- [x] T009 [Phase 1] Verify in Word and paste into evidence.md section "Issue #187": first run → 3 visible bounding boxes + `created: 3, existing: 0`; second run → `created: 0, existing: 3`, total unchanged; replacement readable on a control header (title)
- [ ] T010 [Phase 1] Contingency — ONLY if T009 fails on control creation: log the verbatim platform error, implement the comments fallback (`Range.insertComment`, WordApi 1.4) per plan D9, and record which mechanism worked in evidence.md "Issue #187" — SKIPPED: content-control mechanism worked (paired with a text highlight), so the WordApi 1.4 comments fallback was not needed

### Acceptance Gate (hard stop)

- [x] T011 [Phase 1] US2 scenarios 1-3 transcripts present in evidence.md; the marking mechanism that worked is named; `snippet.yaml` re-exported with the Mark stage

---

## Phase 2: Replace one marked word (US3, closes #188)

**Purpose**: One marked taboo word swapped for its suggestion with the change
visible in the document and the before/after pair logged.

- [x] T012 [Phase 2] Implement Replace in `docs/research/20260622-185-officejs-spike/snippet.yaml`: `getByTag(...).getFirst()`, load + sync the control text as `before`, `insertText(replacement, "Replace")`, sync, then log `[replace] before/after` and the `[replace] control state` observation per contract (plan D5) — Replace targets a unique per-occurrence tag so the post-replace state line reports the exact control's fate
- [x] T013 [Phase 2] Verify in Word and paste into evidence.md section "Issue #188": document shows the replacement text; console shows the matching before/after pair plus the control-state note; `snippet.yaml` re-exported

### Acceptance Gate (hard stop)

- [x] T014 [Phase 2] evidence.md now has one closable read-off section per child issue (#186, #187, #188)

---

## Phase Z: Polish & evidence filing

- [x] T015 [P] [Phase Z] Fill evidence.md "Environment": Word build (`File > Account > About Word`), requirement sets relied on (WordApi 1.1; 1.4 only if fallback used), and observed search semantics (case/whole-word behavior)
- [x] T016 [Phase Z] Run the quickstart.md verification checklist end-to-end on a clean document — all 7 boxes checked
- [ ] T017 [Phase Z] Comment evidence links on #186, #187, #188 and a summary on #185 via `gh issue comment` (founder review precedes any push, per repo policy)

### Acceptance Gate

- [ ] T018 [Phase Z] All quickstart boxes checked; `snippet.yaml` + `evidence.md` committed on this feature branch

---

## Dependencies & Execution Order

- Phases are strictly sequential: 0 → 1 → 2 → Z (each stage operates on the prior
  stage's document state; the Acceptance Gate is a hard stop).
- Within Phase 0, T001 and T002 are parallel; T003 → T004 → T005 are sequential
  (same snippet file).
- Story independence: each story remains independently RE-verifiable at any time by
  opening a fresh document and pressing Seed + the prior stage buttons — the
  buttons, not other engineers, provide the prerequisite state. MVP = Phase 0
  (US1/#186) alone.
- T010 is conditional; skip it entirely when T009 passes.

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies)
- `[Phase N]` = plan phase the task belongs to (Phase 0 = US1, Phase 1 = US2, Phase 2 = US3)
- TDD note: no function files are created, so the pytest Red/Green cycle does not
  apply; the contract file (contracts/console-output.md) plays the "failing test"
  role — each verify task checks console output against it
- The version-guard-report.md Compatibility Rules are mandatory while writing the
  snippet (load/sync before reads; appearance enum BoundingBox|Tags|Hidden; no
  wildcards; api_set WordApi 1.1)
- Commit after each phase gate passes
- Human-in-the-loop: snippet runs and read-offs happen in the Word GUI —
  `subagent-driven-development` does not apply
- Use `/make-pr` to complete the work after Phase Z
