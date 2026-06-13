# Evidence: Office.js Spike — Scan, Mark, Replace in Script Lab (#185)

**Date run**: 2026-06-13
**Operator**: Harel Lustiger

This file holds the read-off evidence for the spike (spec FR-011). Each issue
section below is closed by pointing at its console transcript. Paste the Script
Lab console output verbatim into the fenced blocks; do not paraphrase. Acceptance
line shapes are defined in
[contracts/console-output.md](../../../specs/185-office-js-spike-scan-mark-replace-in-script-lab/contracts/console-output.md).

> Transcripts below are real Script Lab console output captured by the operator on
> the build named under Environment. All three child issues (#186, #187, #188) close
> against these read-offs. Three carry-forward findings are flagged inline (Design-Mode
> visibility, shared-tag replace reporting, control consumed on replace).

---

## Environment

- **Word build** (`File > Account > About Word`): Microsoft 365 MSO, Version 2605 (Build 16.0.20026.20166), 64-bit
- **Platform**: Windows desktop Word (Microsoft 365), Current Channel
- **Requirement sets relied on**: WordApi 1.1 only (content controls, search, font highlight; no 1.4 fallback needed)
- **Observed search semantics**: `matchWholeWord=true matchCase=false` confirmed — the two `utilise` occurrences each matched as whole words; no partial/substring hits reported.
- **Marking mechanism that worked**: content control (`insertContentControl` + `BoundingBox` + title) PAIRED with a text highlight (`font.highlightColor`). The highlight makes marks visible in normal reading view; the control carries the bounded box + replacement metadata. Comments fallback (T010) not needed.
- **Snippet version**: this evidence is the v2 (patched) run. The first run (v1) surfaced two findings — marks invisible outside Design Mode, and ambiguous post-replace state reporting from a word-level tag. Both were fixed in `snippet.yaml` (reading-view highlight + per-occurrence tags) and re-verified; the read-offs below are the patched run.

---

## Issue #186 — Find listed words (US1)

**Acceptance**: 3 match lines + `[find] total: 3` on the seeded doc; `[find] total: 0`
and no error on an unseeded doc; a repeated word reported once per occurrence.

### Scenario 1 — seeded document (expect 3 matches, total 3) — ✅ PASS

```text
[seed] inserted sample text with 3 occurrences (utilise x2, commence x1)
[find] options: matchWholeWord=true matchCase=false
[find] match 1: "utilise" (word: utilise)
[find] match 2: "utilise" (word: utilise)
[find] match 3: "commence" (word: commence)
[find] total: 3
```

### Scenario 2 — fresh unseeded document (expect total 0, no error) — ✅ PASS

Run on a fresh blank document (no Seed). `total: 0` and no `[find] ERROR` line — a
clean zero-match run is correctly not treated as an error (contract line 64).

```text
[find] options: matchWholeWord=true matchCase=false
[find] total: 0
```

### Scenario 3 — repeated word reported per occurrence — ✅ PASS

The repeated word `utilise` produced its own `[find] match` line for each of its two
occurrences (match 1 and match 2 above), not a single deduplicated line.

```text
[find] match 1: "utilise" (word: utilise)
[find] match 2: "utilise" (word: utilise)
```

---

## Issue #187 — Mark found occurrences (US2)

**Acceptance**: first run → 3 visible bounding boxes + `created: 3, existing: 0,
total marked: 3`; second run → `created: 0, existing: 3, total marked: 3` (total
unchanged); replacement readable on a mark's control header (title).

### Scenario 1 — first Mark run (expect created: 3) — ✅ PASS (visible in normal view)

```text
[mark] created: 3, existing: 0, total marked: 3
```

Console count correct (3 marks created). All three words (`utilise`, `commence`,
`utilise`) show a **yellow highlight in normal reading view — no Design Mode needed**
(screenshot evidence). Each is also wrapped in a BoundingBox content control carrying
its replacement as title (visible if Design Mode is toggled). The reading-view
highlight resolves the v1 visibility finding: marks no longer require Design Mode.

### Scenario 2 — re-run Mark (expect created: 0, total unchanged) — ✅ PASS (idempotency)

```text
[mark] created: 0, existing: 3, total marked: 3
```

Re-run created zero new marks; total unchanged at 3. The per-occurrence tag scan
correctly identifies every already-marked occurrence and skips it.

### Scenario 3 — replacement readable from mark metadata — ✅ PASS

The replacement is readable on each control's title in Design Mode (`commence` →
`start`, `utilise` → `use`), and each mark also carries a unique per-occurrence tag
(`redline-taboo:<word>:<index>`). Metadata is inspectable; no hover/inspector needed.

### Marking mechanism — RESOLVED

Marks now use a **paired mechanism**: a BoundingBox content control (bounded box +
title + per-occurrence tag metadata) AND a `font.highlightColor` text highlight
(always visible in normal reading view). WordApi 1.1 throughout; comments fallback
(T010, 1.4) NOT needed. The v1 constraint (controls invisible outside Design Mode)
is closed — the highlight gives the user-facing signal, the control carries the
structured metadata.

---

## Issue #188 — Replace a marked word (US3)

**Acceptance**: document shows the replacement text in place of the original word;
console shows the matching before/after pair plus the control-state note.

### Scenario 1 — replace one marked word — ✅ PASS (document text swapped, control consumed)

```text
[replace] before: "utilise" after: "use"
[replace] control state: control removed after replace (tag redline-taboo:utilise:0 gone)
```

**Document text after replace** (operator confirmed by reading the document, normal view):

> "The crew will **use** the new rig before they commence the survey and will
> utilise the same approach throughout the works."

The first `utilise` → `use` in the visible document; its highlight is gone, the other
two marks remain (screenshot evidence). **The replace primitive works.**

**Control state after replace** (the #188 rabbit hole — observed, not prescribed):

`insertText(after, "Replace")` on the targeted control's range replaces the document
text AND removes that control. Because Replace now targets a UNIQUE per-occurrence tag
(`redline-taboo:utilise:0`), the post-replace re-query reports that exact control's
true fate — `control removed after replace` — with no sibling ambiguity. This closes
the v1 reporting caveat (a word-level tag had returned a different occurrence's
still-live control, making it look like the replace hadn't taken).

Product carry-forward: a replace consumes its mark, so after replacing, the remaining
marks for that word are independent and individually addressable by their own tags.
