---
name: office-js-word-addin
description: Use when implementing or testing Office.js Word add-in behaviour — finding, marking, or replacing words in a Word document; wrapping ranges in content controls; making in-document marks visible; tagging marks for re-query; or proving add-in snippets work when no agent can drive the Word GUI. Covers Script Lab spikes and vendored JS served by the Python backend (WordApi 1.3 floor).
---

# Office.js Word Add-in (Find / Mark / Replace)

## Overview

Office.js is the JavaScript API that runs inside Microsoft Word and reads or
mutates the open document. This skill covers the three primitives behind the
Pre-Review product surface — **find** a listed word, **mark** it visibly, and
**replace** it — the two non-obvious gotchas a first implementation gets wrong,
and how an AI agent obtains trustworthy proof that add-in code worked when the
agent cannot touch the Word desktop graphical user interface (GUI).

Read the **Principles** section first. The gotchas and tables below are
applications of those principles; the principles are what transfer to the next
Office.js task.

## Principles (durable — these transfer)

1. **Proxy load/sync discipline.** The Word document is a proxy object model, not
   live state. You queue `load()` for each property you intend to read, call
   `await context.sync()` once, then read. Reading a proxy property before
   load+sync throws. Batch your loads; one sync per stage, not one per property.

2. **The requirement-set floor is a review contract the host does not enforce.**
   The declared `api_set` floor is a promise about which Word builds your code
   supports. The running host does **not** check it — your snippet runs against
   whatever API the *current* host happens to expose, which is usually far above
   your floor. A green run on your machine proves nothing about floor compliance.
   The floor is verified by humans reading the API reference, not by the runtime.

3. **Verification altitude — the console proves output, not floor compliance.**
   `console.log` evidence tells you *what the code produced* on the host that ran
   it. It cannot tell you the code stays within its declared floor, because the
   host silently offers higher API members. Keep these two questions separate:
   "did it produce the right output?" (console answers) and "does every call sit
   at or below the declared floor?" (only the API reference answers).

4. **Idempotency by persisted identity, not by position.** Re-running a stage must
   converge, not duplicate. Achieve this by tagging each mark with a stable
   identity persisted in the document, then skipping identities already present.
   **Caveat:** the identity we persist encodes a positional occurrence index
   (`:0`, `:1`, …). That index is only stable while upstream text is unchanged; an
   edit that inserts or deletes an earlier occurrence shifts every later index.
   Positional identity is good enough for a single scan/mark/replace pass; it is
   **not** a durable document-lifetime key. Treat the index as pass-local.

5. **A mark is a signal plus metadata, carried on two layers.** A complete mark is
   (a) a **reader-visible signal** — a text highlight a normal reader sees — and
   (b) **structured metadata** — a content control carrying the replacement and a
   machine-readable tag. The highlight is for the human; the control is for the
   code. One without the other is a half-mark (see Gotcha A).

6. **Target one exact occurrence, not one word.** A word repeats; an occurrence is
   unique. Every operation that mutates or re-queries a mark must address a single
   occurrence by a unique tag, never a word-level tag that matches all of them
   (see Gotcha B).

7. **Observe platform side-effects; do not prescribe them.** What `insertText(...,
   "Replace")` does to the wrapping content control, when chrome renders, what a
   re-query returns after a mutation — these are platform behaviours. Observe them
   on the running host and report what happened. Do not assert them from memory or
   from the docs as if they were guarantees.

8. **The human is the irreducible GUI bridge.** No AI agent can click "Run" in
   Script Lab, see the Word window, or read the rendered page. The agent authors
   the snippet *and* the verification protocol; a human operator performs the one
   action the agent cannot, and pastes the result back verbatim. Design every
   snippet to make that human step short and unambiguous.

## Requirement-Set Floor — WordApi 1.3

**Declare `WordApi 1.3`.** Most primitives in this skill are WordApi 1.1 (the
oldest supported requirement set), but **`ContentControl.getRange()` requires
WordApi 1.3**, and the find/mark/replace path uses it. The floor is set by the
single highest member you call, so the floor is **1.3**, not 1.1.

This raises the floor above Word 2016, which ships only WordApi 1.1. That trade
was made deliberately (see the floor-trap note below) — Word 2016 support is
dropped in exchange for using `getRange()`.

**Client-version mapping** (Microsoft official requirement-set table, verified
2026-04-21): WordApi 1.1 = Word 2016; **WordApi 1.3 = Word 2019**. So a 1.3 floor
means the **minimum supported client is Word 2019** (or any Microsoft 365
subscription, which is evergreen); Word 2016 / 2013 / 2010 are unsupported. This is
a **client-facing minimum requirement** that must reach the contract / terms of use /
website copy before launch — it is owned as a product decision (see
`docs/product/decisions/minimum-client-requirements-by-surface.md`), not just an
engineering detail.

| Member used | Requirement set |
|---|---|
| `Body.search(...)` | WordApi 1.1 |
| `Range.insertContentControl()` | WordApi 1.1 |
| `ContentControl.appearance` / `.color` / `.title` / `.tag` | WordApi 1.1 |
| `Range.font.highlightColor` | WordApi 1.1 |
| `ContentControlCollection.getByTag(...)` | WordApi 1.1 |
| `Range.insertText(text, "Replace")` | WordApi 1.1 |
| **`ContentControl.getRange()`** | **WordApi 1.3** ← sets the floor |

> **The floor trap (why this matters — the whole point of this skill).**
> The first cut of this snippet was assumed to be WordApi 1.1 because every
> *visible* primitive is 1.1, and it **ran green** on the dev host. A green
> console can never catch a floor violation — see Principle 3 — because the host
> silently offered every member the code asked for, including `getRange()`. The
> 1.3 dependency was discovered only by a human reading the Microsoft Learn
> requirement-set reference member-by-member. Once found, the team chose to
> **raise the declared floor to 1.3 to match the code** (accepting the loss of
> Word 2016) rather than rewrite `getRange()` away.
>
> The durable lesson is not "remember that `getRange()` is 1.3." It is: **the
> requirement-set floor is a review contract the host doesn't enforce, and a
> green run can't prove floor compliance.** Verify the floor by reading the API
> reference, every member, every time — the runtime will never tell you.

## When to Use

- Implementing or testing find / mark / replace inside a Word document via Office.js.
- Wrapping a found range in a content control and needing the mark **visible to a normal reader**.
- Tagging marks so later code can query, re-query, or replace **one exact occurrence**.
- Building a Script Lab spike (zero infrastructure: no manifest, no server, no certificate).
- Writing the **vendored JavaScript** the Python backend serves to a Word taskpane (per the all-Python rule's "vendored JS permitted" carve-out — this JS is implementation code, owned by the Python developer).
- Needing to **prove** an add-in snippet works when no agent can click "Run" in Word.

**When NOT to use:** server-side DOCX generation (OOXML / python-docx — a
different surface); manifest / sideloading / certificate work (a separate epic);
the real taboo dictionary or scan endpoint (backend concerns, not the Office.js
layer).

## Quick Reference

| Operation | API | Notes |
|---|---|---|
| Find a word | `body.search(word, {matchWholeWord:true, matchCase:false, matchWildcards:false})` | WordApi 1.1. Literal search; whole-word stops "assess" matching "assessment"; case-insensitive matches "Assess". Returns a Range collection — load `items/text` then sync. |
| Mark — bounded box | `range.insertContentControl()` then `cc.appearance="BoundingBox"`, `cc.color="red"`, `cc.title=<replacement>` | WordApi 1.1. Box + title chrome render **only in Design Mode** — see Gotcha A. |
| Mark — reader-visible | `range.font.highlightColor = "Yellow"` | WordApi 1.1. Visible in normal reading/editing view. **Pair this with the content control** — see Gotcha A. |
| Tag a mark | `cc.tag = "redline-taboo:" + word + ":" + occurrenceIndex` | WordApi 1.1. **Per-occurrence**, not per-word — see Gotcha B. |
| Get a control's range | `cc.getRange()` | **WordApi 1.3 — sets the floor.** Use to read/operate on the wrapped text. |
| Re-query a mark | `document.contentControls.getByTag(tag)` → load `items` → sync | WordApi 1.1. Tag persists in the saved document (`<w:sdtPr><w:tag>`), so detection survives runs. |
| Replace in place | `range.insertText(replacement, "Replace")` | WordApi 1.1. Replaces the range text; observe what happens to the wrapping control (see Gotcha B, Principle 7). |

## Gotcha A — A content-control BoundingBox is invisible to a normal reader

**Symptom:** you wrap the word in a content control with `appearance="BoundingBox"`
and a colour, the console says the mark was created, but the user reading the
document sees nothing flagged.

**Why:** the bounding-box chrome (the shaded rectangle and the title header)
renders **only when Word is in Design Mode** (Developer tab → Design Mode). In
normal reading/editing view the chrome is suppressed, so the mark carries metadata
but gives the reader no signal. (This is Principle 5: a mark needs both layers.)

**Fix:** pair the content control with a text highlight on the same range:

```js
range.font.highlightColor = "Yellow";    // WordApi 1.1 — visible in normal reading view
const cc = range.insertContentControl(); // WordApi 1.1
cc.appearance = "BoundingBox";            // bounded box + title — visible only in Design Mode
cc.color = "red";
cc.title = replacement;                   // metadata, readable on the control header
cc.tag = occurrenceTag(word, index);      // see Gotcha B
const ccRange = cc.getRange();            // WordApi 1.3 — the call that sets the floor
```

The **highlight is the user-facing signal**; the **control carries the structured
metadata** (replacement + machine-readable tag). One without the other is a
half-mark. (Spike #185 evidence, issue #187 finding: marks were invisible outside
Design Mode until the highlight was added.)

## Gotcha B — A word-level tag is ambiguous when a word repeats

**Symptom:** "utilise" appears twice. Both marks share the tag
`redline-taboo:utilise`. You replace the first occurrence, then re-query
`getByTag("redline-taboo:utilise")` to confirm the control was consumed — and the
query still returns a control, so you wrongly conclude the replace did not take.
The control you got back is the *second* occurrence's still-live mark.

**Why:** `getByTag` returns *every* control with that tag. A shared, word-level tag
cannot distinguish one occurrence from another. Post-replace state queries become
unreliable exactly when a word repeats — the common case for taboo scanning. (This
is Principle 6: address an occurrence, not a word.)

**Fix:** give every mark a **unique per-occurrence tag** encoding the occurrence
index:

```js
function occurrenceTag(word, index) {
  return "redline-taboo:" + word + ":" + index;   // e.g. redline-taboo:utilise:0
}
```

Now Replace targets one exact tag (`redline-taboo:utilise:0`), and the post-replace
re-query reads **that control's true fate** with no sibling ambiguity:

```js
const targetTag = occurrenceTag(word, 0);
const cc = context.document.contentControls.getByTag(targetTag).getFirst();
const range = cc.getRange();                     // WordApi 1.3
range.load("text");
await context.sync();
const before = range.text;                       // loaded above

range.insertText(replacement, "Replace");        // WordApi 1.1
await context.sync();

const stillThere = context.document.contentControls.getByTag(targetTag);
stillThere.load("items");
await context.sync();
// items.length === 0  →  "control removed after replace (tag ... gone)"  — unambiguous
```

> **Positional-identity caveat (Principle 4).** The `:index` suffix is a *pass-local*
> identity. It is stable only while earlier occurrences are not inserted or deleted;
> any upstream edit reshuffles later indexes. It is sufficient for one
> scan→mark→replace pass; do not treat it as a durable document-lifetime key.

**Observed behaviour (spike #185, #188 — observation, not an API guarantee):**
`insertText(..., "Replace")` on the targeted control's range replaced the document
text **and consumed (removed) that control**, so the unique-tag re-query returned
zero items on **Build 16.0.20026**. Remaining marks for the same word are
independent and individually addressable by their own tags. Per Principle 7, do not
prescribe the wrapper's fate from memory — observe and report it on the host that
ran.

> **Idempotency note (Principle 4):** on the mark stage, read existing controls'
> tags first and skip occurrence indexes already taken, so re-running mark reports
> `created: 0, existing: N` and the total stays stable. A word-level `getByTag`
> cannot see the per-occurrence suffix — read tags directly off `contentControls`.

## Human-in-the-Loop Verification (no agent can drive the Word GUI)

**The hard constraint (Principle 8):** no AI agent can click "Run" in Script Lab,
see the Word window, or read the rendered document. The agent authors the snippet
and the verification protocol; a **human operator** is the irreducible bridge for
the manual steps.

**The pattern (grounded in spike #185, FR-011 read-off-not-judgment):**

1. **Instrument the snippet to self-report.** Every stage emits structured,
   contract-shaped lines via `console.log` (e.g. `[find] total: 3`,
   `[mark] created: 3, existing: 0, total marked: 3`,
   `[replace] before: "utilise" after: "use"`). The console output is the
   machine-readable evidence surface.
2. **Human runs each stage** in Script Lab (the one action the agent cannot do)
   and **reads the result two ways:** the console transcript, and the on-screen
   document (the highlight is visible in normal view — that is why Gotcha A's
   highlight matters for verification, not just UX).
3. **Human pastes the console transcript back verbatim** — not paraphrased. The
   agent verifies each line against the expected contract shape.

**What counts as proof vs. what does not** (calibrated for a **zero-infrastructure
Script Lab spike** — do not over-engineer). Note the altitude split from Principle
3: this table verifies **output**, not floor compliance — the floor is verified
separately against the API reference.

| Evidence | Trust | Why |
|---|---|---|
| Verbatim console transcript matching the contract lines | Strong | Structured, read-off-verifiable, agent can check each line |
| Human read-off of the on-screen highlight in normal view | Acceptable corroboration | The reader-visible mark (Gotcha A) is the user-facing signal |
| Re-query read-back via `getByTag` printed to console | Strong | API read of the document model, not a screen artifact |
| "It ran, no error" with no transcript | Insufficient | No error ≠ correct output; Office.js fails silently |
| A green run as evidence of floor compliance | Reject | Principle 3 — the host offers members above your floor; only the API reference proves the floor |
| Paraphrased / summarised console output | Reject | Must be verbatim; paraphrase hides contract mismatches |

> **Do not** reach for `document.save()` + cold-reopen + raw-XML inspection as the
> default proof. That is a heavier protocol for a different context; a Script Lab
> spike has zero infrastructure by design (FR-012). The verbatim console transcript
> plus the reader-visible highlight is the canonical proof here.

## Snippet Structure (Script Lab)

One snippet, one button per stage (Seed → Find → Mark → Replace), each button bound
to an async function wrapped in a `tryCatch` that surfaces platform errors verbatim.
Declare `api_set: WordApi 1.3` (the floor — see the Requirement-Set Floor section).
No external libraries beyond `office.js` itself. Hard-coded placeholder data (a 3–5
word taboo/replacement list) is acceptable; the real dictionary arrives from the
backend, not the snippet.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Marking with a content control alone | Pair with `font.highlightColor` — the box is Design-Mode-only (Gotcha A, Principle 5). |
| Tagging all occurrences of a word with one tag | Use a per-occurrence tag `redline-taboo:<word>:<index>` (Gotcha B, Principle 6). |
| Reading `range.text` before load+sync | Queue `load("text")`, `await context.sync()`, then read (Principle 1). |
| Declaring `api_set: WordApi 1.1` because the visible primitives are 1.1 | `getRange()` is 1.3 and sets the floor; declare `WordApi 1.3` (Principle 2). |
| Treating a green run as proof of floor compliance | The host offers members above your floor; verify the floor against the API reference (Principle 3). |
| Treating the `:index` tag suffix as a durable document key | It is pass-local; an upstream edit reshuffles indexes (Principle 4). |
| `matchWildcards: true` with raw user text | Keep it false; search literal words (avoids escaping bugs). |
| Treating "no error" as success | Demand the verbatim console transcript; verify each contract line (Principle 8). |
| Prescribing the post-replace wrapper state from memory | Observe via a unique-tag re-query and report what actually happened (Principle 7). |

## Grounding Sources

- Spike #185 evidence (patched run, floor raised to WordApi 1.3): `docs/research/20260622-185-officejs-spike/evidence.md`
- Snippet (per-occurrence tags + paired highlight, `api_set: WordApi 1.3`): `docs/research/20260622-185-officejs-spike/snippet.yaml`
- Spec / research / version-guard: `specs/185-office-js-spike-scan-mark-replace-in-script-lab/{spec.md,research.md,version-guard-report.md}`
- Microsoft Learn requirement-set reference (live; verify member-by-member, current as of 2026-05): `ContentControl.getRange` (**WordApi 1.3**), `ContentControlCollection.getByTag`, `Range.insertText` ("Replace"), `Range.font.highlightColor`, `ContentControlAppearance` — confirm each member's requirement set against this reference, never against a green run.

### Provenance and confidence (Peter's labels — do not strip)

- **OOXML tag persistence** (the claim that `cc.tag` survives in `<w:sdtPr><w:tag>`
  across save/reopen) is grounded in the **issue #185 research notebook (finding
  R5)**. It is **not independently XML-verified** in this spike — we read it from
  the research source, we did not crack the .docx and inspect the XML ourselves.
- **Post-replace control consumption** (the claim that `insertText(..., "Replace")`
  removes the wrapping control) is an **observation on Build 16.0.20026**, not a
  documented API guarantee. Re-observe it on the target host before relying on it.
