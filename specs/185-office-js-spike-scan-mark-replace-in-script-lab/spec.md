# Feature Specification: Office.js Spike — Scan, Mark, Replace in Script Lab

**Feature Branch**: `feature/185-office-js-spike-scan-mark-replace-in-script-lab`

**Created**: 2026-06-13

**Status**: Draft

**Input**: GitHub issue [#185](https://github.com/redmarklogic/redline/issues/185) "Office.js spike: scan, mark, replace in Script Lab" (parent of [#186](https://github.com/redmarklogic/redline/issues/186), [#187](https://github.com/redmarklogic/redline/issues/187), [#188](https://github.com/redmarklogic/redline/issues/188)); sprint context `docs/product/tasks/sprint-4-goal.md`

## Purpose

Sprint 4's goal (Word taskpane PoC, Bet 2 — Pre-Review) depends on the ability to find,
mark, and replace words inside an open Word document. This spike proves those three
primitives inside Word using the Script Lab add-in — with no server, no manifest, no
certificates, and no API calls — so that the later wiring task (#197) builds on proven
ground instead of discovering platform limitations mid-sprint. The spike's output is
evidence: structured console reports and visible document changes that a human can
verify by read-off, not judgment.

## User Scenarios & Testing *(mandatory)*

The "user" throughout is the spike operator: the engineer running the snippet in
Script Lab inside desktop Word (Peter owns; Kabilan implements).

### User Story 1 - Find listed words in the document body (Priority: P1)

The operator opens a sample document seeded with exactly 3 occurrences of words from a
hard-coded list of 3-5 taboo-word/replacement pairs, runs the snippet's find stage in
Script Lab, and reads from the console the text of each found occurrence and a total
count — without inspecting the document manually. (Child issue #186.)

**Why this priority**: Every later primitive operates on found ranges. If locating
words fails, marking and replacing are unreachable, and the sprint's wiring plan (#197)
loses its foundation. This is also the stage that closes the known knowledge gap around
the document-search capability, which our notebook sources did not cover.

**Independent Test**: Run the find stage alone against the seeded sample document and
compare the console report (occurrence texts + total) against the known seeded content.
Delivers standalone value: proof that word location works inside Word.

**Acceptance Scenarios**:

1. **Given** a sample document seeded with exactly 3 occurrences of listed words,
   **When** the find stage runs, **Then** the console lists each found occurrence's
   text and reports a total count of 3 `[human-verify: read Script Lab console in Word]`
2. **Given** a document containing none of the listed words, **When** the find stage
   runs, **Then** the console reports 0 matches and no error is raised `[human-verify]`
3. **Given** a document where one listed word appears more than once, **When** the find
   stage runs, **Then** every occurrence is reported individually (no collapsing to one
   match per word) `[human-verify]`

---

### User Story 2 - Mark each found occurrence visibly (Priority: P2)

After the find stage, the operator runs the mark stage. Each found occurrence becomes
visibly marked in the document body — a bounded, colored highlight around the word —
and each mark carries the word's suggested replacement as inspectable metadata. The
console reports how many marks were created. (Child issue #187.)

**Why this priority**: Visible in-document marking is the core user-facing behavior of
the future Pre-Review product (flagged words appear in the document). It depends on
find (P1) but replace does not depend on it being perfect — hence second.

**Independent Test**: With found occurrences available, run the mark stage and visually
confirm 3 distinct marks in the document plus a console count of 3. Delivers standalone
value: proof that in-document visual annotation works.

**Acceptance Scenarios**:

1. **Given** the 3 found occurrences from the find stage, **When** the mark stage runs,
   **Then** 3 bounded, visibly distinct marks appear in the document and the console
   logs that 3 marks were created `[human-verify]`
2. **Given** an already-marked document, **When** the mark stage re-runs, **Then** no
   duplicate marks are created (the run is idempotent or existing marks are detected)
   and the console count is unchanged `[human-verify: console count unchanged]`
3. **Given** a created mark, **When** the operator inspects it, **Then** the suggested
   replacement for that word is readable from the mark's metadata `[human-verify]`

---

### User Story 3 - Replace a marked word with its suggestion (Priority: P3)

The operator runs the replace stage against one marked occurrence. The document text
changes from the taboo word to its suggested replacement, and the console logs the
before/after text pair. (Child issue #188.)

**Why this priority**: Replace backs the future "Fix" button, which is a should-have
for the sprint (a stretch goal after #197). Proving it now makes that wiring optional
rather than exploratory, but the PoC demo succeeds without it.

**Independent Test**: Run the replace stage on one marked word and confirm the document
shows the replacement text while the console shows the before/after pair. Delivers
standalone value: proof that programmatic text substitution works.

**Acceptance Scenarios**:

1. **Given** a marked taboo word, **When** the replace stage runs, **Then** the document
   shows the replacement text in place of the original word and the console logs the
   before/after text pair `[human-verify]`

---

### Edge Cases

- A listed word appears inside a longer word (e.g., a list word "assess" inside
  "assessment"): matching is whole-word, so the longer word is not reported or marked.
- A listed word appears with different letter casing than the list entry: matching is
  case-insensitive, so the occurrence is still found (see Assumptions).
- The document contains none of the listed words: the find stage reports 0 and exits
  cleanly (no error state).
- The mark stage re-runs on an already-marked document: no duplicate marks accumulate
  (idempotent or detected — either satisfies acceptance).
- The replace target is wrapped in a mark: the document must show the replacement
  text; what happens to the mark wrapper (kept, cleared, or removed) is observed and
  reported as spike evidence — no particular wrapper outcome is prescribed (source
  issue #188 flags this as the open question the spike answers).
- The installed Word build does not support the chosen marking mechanism: any visible
  marking is acceptable as fallback (founder ruling, sprint-4 risk register); the spike
  reports which mechanism worked.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The snippet MUST carry a hard-coded list of 3-5 taboo-word/replacement
  pairs (placeholder data; the real dictionary arrives via #195).
- **FR-002**: The snippet MUST provide a setup step that seeds the open document with
  sample text containing exactly 3 occurrences of listed words — one listed word
  appearing twice and a second listed word once — so verification is repeatable on
  any machine and word repetition is part of the standard baseline.
- **FR-003**: The find stage MUST locate every occurrence of every listed word in the
  document body and report each occurrence's text plus a total count to the console.
- **FR-004**: The find stage MUST report a count of 0 and complete without error when
  no listed word is present.
- **FR-005**: The mark stage MUST visibly mark each found occurrence in the document
  with a bounded, colored highlight distinct from normal text.
- **FR-006**: Each mark MUST carry the occurrence's suggested replacement as
  inspectable metadata attached to the mark.
- **FR-007**: The mark stage MUST report the number of marks created to the console.
- **FR-008**: Re-running the mark stage MUST NOT create duplicate marks; the console
  count MUST make this verifiable (idempotent re-run or detection of existing marks).
- **FR-009**: The replace stage MUST replace the text of one marked occurrence with its
  suggested replacement so the change is visible in the document.
- **FR-010**: The replace stage MUST log the before/after text pair to the console.
- **FR-011**: Every acceptance check MUST be verifiable by reading structured console
  output or directly observing the document — read-off, not judgment.
- **FR-012**: The entire spike MUST run inside Script Lab in desktop Word with zero
  infrastructure: no served taskpane, no manifest, no certificates, no network or API
  calls.
- **FR-013**: The spike MUST be delivered as one snippet extended in stages (find,
  mark, replace), each stage runnable and verifiable on its own.

### Key Entities

- **Word list entry**: A taboo word paired with its suggested replacement; 3-5 entries
  hard-coded in the snippet.
- **Sample document content**: Seeded text containing exactly 3 occurrences of listed
  words; the known baseline every console report is compared against.
- **Found occurrence**: One located instance of a listed word in the document body —
  its text and position; input to marking.
- **Mark**: A visible, bounded, colored annotation wrapping one found occurrence,
  carrying the suggested replacement as metadata; detectable on re-run.
- **Console report**: Structured per-stage output (occurrence texts, counts,
  before/after pairs) that a human verifies by read-off.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An operator on a machine with only Word and Script Lab installed runs all
  three stages and verifies every acceptance scenario the same day — total effort within
  the 1-working-day appetite (Mon Jun 22).
- **SC-002**: The find stage's console report matches the seeded baseline exactly: 3
  occurrence texts and total count 3, with zero manual document inspection required.
- **SC-003**: 3 visible marks appear in the document after the mark stage; console
  count equals 3; a second run leaves the count at 3.
- **SC-004**: After the replace stage, the document shows the replacement text and the
  console shows the matching before/after pair — 1 successful replacement.
- **SC-005**: Zero infrastructure components exist at spike end: no server process, no
  manifest file, no certificate, no network call made.
- **SC-006**: Each child issue (#186, #187, #188) can be closed by pointing at its
  console read-off — no additional evidence gathering needed.

## Assumptions

- **Seeding**: The snippet itself seeds the sample text (setup step) rather than
  requiring a hand-prepared document — keeps verification self-contained and
  repeatable. Source issues say "a sample document seeded with 3 known taboo words"
  without fixing who seeds; self-seeding is the chosen default.
- **Match semantics**: Whole-word and case-insensitive matching are the chosen defaults
  (taboo scanning should flag "Assess" as well as "assess", but not "assessment").
  Child issue #186 lists case/whole-word handling as an open rabbit hole; the find
  stage verifies and reports the actual semantics achieved.
- **Marking mechanism**: Sources fix the primary mechanism as a rich-text wrapper with
  a bounding-box appearance and a distinct color, with the replacement stored in the
  mark's title/tag metadata; an in-document comment is the fallback only if the primary
  fails — never both (#187 no-go). Mechanism details live in the plan, not this spec.
- **Environment**: Current Microsoft 365 desktop Word on Windows; Script Lab is
  installable from the Office Store on the operator's machine (organization policy
  permits add-in installation). Research confirms all required platform capabilities
  exist in the oldest supported API level, so the installed Word build is not expected
  to be a constraint for the primary path.
- **Operator**: A developer-profile user; raw console output is an acceptable
  interface. No end-user UX is in scope.
- **Replacement metadata inspection** (US2 scenario 3) may use any read-off mechanism
  available in the environment (mark metadata display or console log).

## Out of Scope

- Served taskpane, manifest, certificates, sideloading — issue #189/#190-#193.
- Any API endpoint or network call — issues #194/#196/#197.
- Real taboo dictionary — issue #195 delivers it; this spike hard-codes 3-5 pairs.
- Client-side regex or matching logic beyond locating listed words — real matching
  lives in the scan endpoint (#196).
- Visual design, Fluent UI, polished UX — add-in epic; founder ruling accepts any
  visible marking.
- A wired "Fix" button in a served pane — Sprint 4 stretch, after #197.
- Building both marking mechanisms (primary and fallback) — fallback only on primary
  failure.

## Dependencies

- Script Lab add-in installable from the Office Store on the operator's machine.
- Desktop Word (Microsoft 365) available to the operator.
- Downstream consumers: #197 (wiring) builds on the proven primitives; #37 (Inline
  Annotation Engine PRD) cites this spike as evidence. Neither blocks this spike.
