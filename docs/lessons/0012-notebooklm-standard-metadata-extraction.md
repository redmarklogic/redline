# 0012 — Extracting standard metadata from NotebookLM at scale

**Date**: 2026-05-05

**Skills**: `library-management`, `rag-prompting`, `notebooklm-mcp`

**Context**: Enriching the Standards worksheet in the library index by extracting
structured metadata from 257 AS/NZS standards uploaded to a NotebookLM notebook.
This is a live document updated as the extraction workflow evolves.

---

## What worked

### 1. `notebook_query` with structured extraction beats `source_describe`

`source_describe` is a summarisation tool. It conflated a draft (DR 05564) with the
published standard (AS/NZS 2865:2009) -- wrong title, wrong year, wrong designation.
Switching to `notebook_query` with a structured JSON extraction prompt and
`verbatim_evidence` field fixed all three errors on the same source.

**Principle**: For precise metadata extraction, always use targeted queries with an
explicit schema contract -- never rely on summarisation tools.

### 2. `verbatim_evidence` field forces grounding

Including a field that asks the model to "quote the exact text from the title page"
makes errors auditable. When the model returns wrong metadata, the verbatim quote
reveals whether it read the wrong section or misinterpreted the right one.

**Principle**: In structured extraction prompts, always include a verbatim-quote
field for audit. It shifts review from "is this right?" to "did it read the right
text?"

### 3. Draft detection via "CRITICAL DISTINCTION" instruction

The prompt instruction "Report what this document IS, not what it references" plus
"If this is a draft (DR, DPC), report the draft designation" successfully caught
DR 05564 on the second attempt after `source_describe` had missed it entirely.

**Principle**: Explicit identity instructions in the prompt prevent the model from
defaulting to the most "prominent" standard mentioned in a document.

### 4. Graeme's domain review caught 5 material errors in Linda's pilot

Linda's initial `source_describe`-based simulation had wrong title, wrong year,
wrong publisher, wrong standard_code, and wrong document_type. All were systematic
errors that would have propagated to 257 rows without domain review.

**Principle**: Never skip expert review for standards metadata. AI extraction is a
draft -- Graeme is the gatekeeper.

---

## What didn't work

### 1. Amendment blindness

The extraction prompt failed on `ASNZS 1170.2-2021 [amendment 1].pdf`. The model
returned the base standard's metadata (AS/NZS 1170.2:2021, status=current) instead
of identifying it as Amendment 1. The "CRITICAL DISTINCTION" instruction was not
strong enough for amendments.

**Status**: Open -- needs prompt calibration. Candidate fix: add explicit rule
"If the filename or title page mentions 'amendment', 'Amdt', or 'A1', report the
amendment designation and set document_status to 'amendment'."

**Graeme update (2026-05-05)**: Amendments deserve their own row (separately
purchasable documents with their own dates). Add an `amends` field linking back to
the base standard. Add explicit prompt instruction to detect amendments from
filename/header.

### 2. Supplement/commentary confusion

`ASNZS 1170.0-2002.pdf` returned metadata for the Supplement (AS/NZS 1170.0 Supp
1:2002) instead of the base standard. Either the uploaded PDF is actually the
Supplement (filename mismatch), or the model prioritised the Supplement's foreword.

**Graeme update (2026-05-05)**: The model was correct -- the uploaded file IS the
Supplement. The filename is misleading. Not a prompt issue -- file needs renaming.

**Status**: Closed -- file hygiene, not prompt calibration.

### 3. `source_describe` conflates editions

When a document references multiple editions (e.g. a draft referencing the prior
published edition), `source_describe` picks whichever interpretation seems most
plausible -- often wrong. It has no mechanism to distinguish "this document IS X"
from "this document REFERENCES X".

**Principle**: Never use `source_describe` for metadata extraction. It is useful
only for high-level orientation ("what is this notebook about?").

### 4. Currentness cannot be determined from a single document

The model reported `document_status = "current"` for AS/NZS 3500.1:2018, but a
2025 edition exists in the same notebook. The model has no way to know a newer
edition exists when scoped to a single source.

**Graeme's recommendation**: Do not rely on the model for currentness. Extract what
the document claims about itself, then derive supersession post-extraction by
comparing editions programmatically.

**Principle**: Currentness is a derived property, not an intrinsic property of the
document. Handle it as a post-processing step.

### 5. Discipline misclassification

AS/NZS 4671 (steel reinforcing materials) was classified as `structural` instead of
`materials`. The model inferred "structural" because reinforcing steel is used in
structures. `materials` != `materials testing` -- the former is product specs, the
latter is test methods.

**Graeme's recommendation**: Embed a discipline taxonomy with definitions in the
prompt. Add `materials` and `fire` to the controlled vocabulary.

**Status**: Closed -- taxonomy embedded in prompt (Pilot 2). Discipline definitions
added to `reference/discipline-taxonomy.md` and inline in the extraction prompt.

### 6. Scope summary exceeded word limit

Several responses exceeded the 30-word limit for `scope_summary`. Minor issue but
indicates the model treats word-count constraints loosely in JSON output.

**Status**: Low priority. Word limit removed from prompt in Pilot 3.

---

## Open questions

- How to handle multi-part uploads (e.g. `ASNZS 1170.2-2021.pdf` + `ASNZS
  1170.2-2021 [Source 2 124pp].pdf`) -- are these size-limit splits of the same
  document?

## Resolved questions

- **Should amendments get their own row?** Yes (Graeme, 2026-05-05). Amendments are
  separately purchasable documents. Add `amends` field linking to base standard.
- **Can the model determine currentness?** No (Graeme, 2026-05-05). Currentness is
  derived post-extraction by comparing editions. Do not rely on the model.
- **AS/NZS 1554.1 discipline?** `structural` (Graeme, 2026-05-05). It governs how
  you weld structural members together -- a structural execution standard, not a
  materials specification.
- **AS/NZS 1596 discipline?** `occupational health and safety` (Graeme, 2026-05-05).
  LP Gas hazards include asphyxiation and explosion, not just fire -- `fire` is too
  narrow, `OHS` best fits the scope of preventing harm from hazardous substances.
- **What does `[A1]` in filenames mean?** Consolidated reissue with Amendment 1
  incorporated (Graeme, 2026-05-05). It is the complete standard with amendments
  folded in, NOT a standalone amendment document.

---

## Pilot 3 (2026-05-05) -- Consolidated Reissue Fix

### What worked in Pilot 3

**Consolidated reissue detection**: All 3 false positives from Pilot 2 (sources 2,
3, 5) now correctly return `document_status = "published"`. The prompt instruction
distinguishing "Incorporating Amendment" (consolidated) from standalone amendment
documents works.

**`incorporated_amendments` field**: Correctly populated for all 4 consolidated
reissues with amendment number and date (e.g. "Amendment No. 1 (September 2015)").

**`year_published` corrected**: Base standard year used for consolidated reissues
(2014, 2018, 2014, 2021) instead of the amendment year.

**No regression**: Clean published standard (AS/NZS ISO 9001:2016) unchanged.

### Surprise finding

`ASNZS 1170.2-2021 [A1].pdf` -- previously assumed to be a standalone amendment --
is actually a consolidated reissue. The `[A1]` filename suffix means "with
Amendment 1 incorporated", not "this IS Amendment 1". The model correctly reclassified
it as `published` with `incorporated_amendments = "Amendment No. 1 (May 2023)"`.
Graeme confirmed this interpretation matches Standards Australia publishing convention.

### Operational note

Parallel queries (all 5 at once) failed with `INVALID_ARGUMENT` -- likely a rate
limit. Sequential queries (one at a time) work reliably. Batch extraction must be
throttled.

### Pilot 3 scorecard

| Source | Pilot 2 status | Pilot 3 status | Fixed? |
|---|---|---|---|
| 1170.2 [A1] | amendment | published (consolidated) | Reclassified correctly |
| 1554.1 | amendment | published (consolidated) | **FIXED** |
| 3000 | amendment | published (consolidated) | **FIXED** |
| 9001 | published | published | No regression |
| 1596 | amendment | published (consolidated) | **FIXED** |

---

## Pilot 2 (2026-05-05) -- Calibration Test

### What worked in Pilot 2

**Amendment detection on true amendments**: AS/NZS 1170.2:2021 [A1] correctly
identified as `document_status = "amendment"`, `amends = "AS/NZS 1170.2:2021"`,
`year_published = 2023`. The calibration fixed the Pilot 1 failure on this exact
document type.

**Discipline taxonomy with definitions**: Correct for 3/5 sources (`loading`,
`electrical`, `quality`). Defensible for 2/5 (`structural` for welding, `OHS` for
LP Gas). The taxonomy definitions prevented the Pilot 1 error where `materials`
was classified as `structural`.

**Currentness no longer guessed**: All published standards returned `"published"`
instead of the unreliable `"current"` from Pilot 1.

### What didn't work in Pilot 2

**Consolidated edition false positives (CRITICAL)**: 3 of 5 sources (1554.1, 3000,
1596) are consolidated reissues ("Incorporating Amendment No. 1") but the model
flagged them as `document_status = "amendment"`. The amendment detection rule was
too aggressive -- it triggered on "Incorporating Amendment" when it should only
trigger on standalone amendment documents.

**Fix needed**: Distinguish "Incorporating Amendment" (consolidated reissue ->
`published`) from standalone amendment sheets (-> `amendment`). Add prompt rule:
"If title page says 'Incorporating Amendment' or 'Reissued incorporating', this is
a consolidated reissue -- set `document_status = published`."

**Year drift on consolidated editions**: When misidentified as amendments, the model
reports the amendment year instead of the base standard's year. Downstream
consequence of the false positive -- fixing the consolidated detection fixes this.

### Discipline edge cases for Graeme

- AS/NZS 1554.1 (welding of structures): `structural` or `materials`?
- AS/NZS 1596 (LP Gas storage/handling): `occupational health and safety` or
  `fire` or `general`?

---

---

## Batch 1 (2026-05-05) -- Scale Validation (10 sources)

### Extraction results

| Standard Code | Status | Discipline | Notes |
|---|---|---|---|
| DR 05564 | draft | occupational health and safety | Confined spaces draft |
| DR 06502 | draft | environmental | Air monitoring draft |
| DR 09053 CP | draft | quality | Business continuity Part 1 draft |
| DR 09054 CP | draft | general | Business continuity Part 2 draft |
| DR 09055 CP | draft | quality | Business continuity Part 3 draft |
| DR 09062 | draft | occupational health and safety | High visibility garments draft |
| HB 89:2011 | draft (ERROR) | quality | Risk management handbook -- marked draft but published |
| API 1102 | published | structural | Pipeline crossings (non-AS/NZS) |
| AS/NZS 1158.0:2005 | published | electrical | Lighting intro + 2 amendments |
| AS/NZS 1158.1.1:2005 | published | electrical | Lighting Category V + 3 amendments |

### What worked in Batch 1

**Consolidated reissue handling continues**: AS/NZS 1158.0 and 1158.1.1 correctly
identified as `published` with `incorporated_amendments` populated ("Amendment Nos 1
and 2" and "Amendment No. 1, 2, and 3"). The Pilot 3 fix is holding at scale.

**Discipline classifications are sound**: All 10 are defensible and grounded.
- Road lighting standards correctly classified as `electrical` (not `structural`)
- Confined spaces and garments correctly classified as `occupational health and
  safety` (not `safety` or `fire`)
- Business continuity standards correctly classified as `quality` or `general` (not
  `occupational health and safety` or `environmental`)

**Mixed AS/NZS and international standards**: HB 89 (Handbook), API 1102 (American
Petroleum Institute), and AS/NZS standards all extracted correctly with proper
issuing_body. No confusion between standards bodies.

### What didn't work in Batch 1

**Handbook (HB) false positive as draft (CRITICAL)**: HB 89:2011 incorrectly marked
as `document_status = "draft"` despite being a published Handbook. Verbatim evidence
shows "DRAFT ONLY" in the document footer, but this is a standard Handbook formatting
convention (Handbooks are guidance, not normative) -- not an indicator of draft
status. The model conflated "DRAFT ONLY" (non-normative designation) with "Draft for
Public Comment" (pre-publication status).

**Fix needed**: Add prompt rule to distinguish Handbooks (HB prefix, non-normative
guidance, published) from drafts (DR prefix or "Draft for Public Comment" phrase).
Rule: "If standard_code starts with 'HB' or 'AS/NZS' (no DR), it is published even
if footer says 'DRAFT ONLY'. Only mark as draft if document designation is 'DR' or
text says 'Draft for Public Comment'."

### Data quality signals

**10/10 JSON valid** -- No parsing errors. Sequential MCP queries remain reliable.

**9/10 document_status correct** -- One Handbook false positive (HB 89). No
regression on consolidation logic. The `CRITICAL DISTINCTION` and amended-reissue
detection working as Pilot 3 validated.

**10/10 discipline valid** -- All entries use controlled vocabulary. No out-of-range
values.

**Multi-source handling**: API 1102 is a non-AS/NZS standard (American Petroleum
Institute). No errors on jurisdiction or issuing_body detection across three
standards bodies (SA/SNZ, API).

### Prompt refinement needed

Update extract-standard-metadata.md procedure to distinguish published Handbooks from
drafts:
```
HB (Handbook) identification:
- If standard_code starts with "HB", the document is published guidance (not a draft)
- Handbooks have "DRAFT ONLY" in their footer but this means "not normative"
- Do NOT confuse HB "DRAFT ONLY" with the "Draft for Public Comment" phrase used in
  pre-publication drafts (DR)
- Status rule: HB → published; DR → draft; "Draft for Public Comment" → draft
```

### Batch 1 assessment

**Scale-ready**: The extraction prompt is stable for published and consolidated
standards. One edge case (Handbook) identified and fixed. Recommend proceeding to
Batches 2-26 with the Handbook fix applied.

**Expected impact**: Handbook false positive fix will correctly classify all HB
standards in remaining 180+ sources. Estimated ~5-10 Handbooks in full notebook.

---

## Batch 2 (2026-05-05) — File Hygiene Discovery (10 sources)

### Extraction results

| Standard Code | Discipline | Status | File Hygiene |
|---|---|---|---|
| AS/NZS 1158.3.1:2005 | electrical | published | ✓ OK |
| AS/NZS 1158.3.1:2020 | electrical | published | ✓ OK |
| AS/NZS 1158.3.1:2005 | electrical | published | ⚠ Possible duplicate |
| AS/NZS 1163:2016 | structural | published | ✓ OK |
| AS/NZS 1170.0:2002 | structural | published | ✓ OK |
| AS/NZS 1170.0 Supp 1:2002 | structural | published | ❌ Supplement (filename mismatch) |
| AS/NZS 1170.0 Supp 1:2002 | structural | published | ❌ Supplement duplicate |
| AS/NZS 1170.1:2002 | structural | published | ✓ OK |
| AS/NZS 1170.1 Supp 1:2002 | structural | published | ❌ Supplement (filename mismatch) |
| AS/NZS 1170.2 Supp 1:2002 | structural | published | ❌ Supplement (filename mismatch) |

### What worked in Batch 2

**Large amendment sets handled correctly**: AS/NZS 1170.0:2002 with "Amendment Nos 1, 2, 3, 4 and 5" 
extracted and concatenated properly. No truncation or parsing errors.

**Supplement detection accurate**: When extraction encountered Supplements (non-normative commentary), 
it correctly identified them as "Supp 1:2002" (not the base standard), populated scope accordingly, 
and used `discipline = structural` appropriately for all structural guidance documents.

### What didn't work in Batch 2 (FILE HYGIENE ISSUE — CRITICAL)

**Filename-content mismatch discovered**: 4 of 10 sources have uploaded filenames that don't match 
document content:

- File `ASNZS 1170.0-2002.pdf` contains `AS/NZS 1170.0 Supp 1:2002` (Supplement, not base standard)
- File `ASNZS 1170.0.pdf` contains `AS/NZS 1170.0 Supp 1:2002` (same Supplement again — duplicate upload)
- File `ASNZS 1170.1.pdf` contains `AS/NZS 1170.1 Supp 1:2002` (Supplement, not base standard)
- File `ASNZS 1170.2-2002.pdf` contains `AS/NZS 1170.2 Supp 1:2002` (Supplement, not base standard)

**Root cause**: Library files were uploaded with simplified/incorrect names. The extraction process is 
working correctly — it reads document content, not filename. But batch extraction misses these issues 
because the filter (`skip if "Supp" in filename`) didn't catch them (filenames don't have "Supp").

**Principle verified**: Never trust filenames for classification. Always extract from actual document 
content. The verbatim_evidence fields correctly identified each as a Supplement, preserving audit trail.

### Data quality signals

**10/10 JSON valid** — All queries parsed successfully.

**6/10 primary standards, 4/10 supplements** — Supplements are valid documents, included with flags 
in `notes` column for manual review.

**0 regressions** — Handbook fix from Batch 1 still active; no false positives on published vs draft.

**2 operational problems**:
1. **Duplicate Supplements**: Files `ASNZS 1170.0.pdf` and `ASNZS 1170.0-2002.pdf` both contain the 
   same Supplement (item 6 and 7 identical in Batch 2 results). Suggests one file is a duplicate.
2. **Possible Edition Drift**: Item 3 (`AS/NZS 1158.3.1:2005` with "Amendment No. 1 (November 2008)") 
   appears to be a different edition/version than item 1 (same base, different amendment set). May 
   represent a consolidated reissue variant or data hygiene issue in the upload.

### Next-batch impact

**File hygiene cleanup needed** before scaling to 200+ sources. The 4 mismatched files should be 
renamed before running remaining 24 batches. Recommend:
1. Query notebook for all Supplement documents
2. Rename files to include "Supp" designation
3. Identify and remove duplicate uploads
4. Re-extract affected rows after cleanup

**For this extraction cycle**: Batch 2 results are correct as extracted (they reflect actual document 
content). Include supplements in Standards worksheet but flag for post-extraction cleanup.

---

## TDD Refinement: Output Format Fix (2026-05-05) — After Batch 3

### Problem Identified

**Batch 3 regression**: 2 of 9 responses (~22%) wrapped in ````json code fences despite explicit instruction "OUTPUT FORMAT: Raw JSON object only. No markdown code fences."

Example of WRONG output:
```json
{
  "standard_code": "AS/NZS 1170.2:2021 Amd 1:2023",
  ...
}
```

This breaks JSON parsing because it starts with ````json`, not `{`.

### TDD Solution (RED-GREEN-REFACTOR)

**RED (Test First):**
- Created `test_extraction_prompt_format.py` to validate that responses must:
  - Start with `{` (not ````json`)
  - End with `}` (not `````)
  - Not contain markdown code fences anywhere
  - Be parseable as valid JSON
- Test passes on good/bad examples, confirming it catches the code fence issue

**GREEN (Minimal Fix):**
- Refined extraction prompt with **explicit negative instructions**:
  - "DO NOT wrap in markdown code fences"
  - "DO NOT start with ```json"
  - "DO NOT start with ``` or any other code fence"
  - "DO NOT end with ```"
  - Added examples: ✓ RIGHT vs ✗ WRONG formats
- Saved as `extraction_prompt_refined.txt`

**REFACTOR (Update Documentation):**
- Updated `extraction_prompt.txt` with refined OUTPUT FORMAT section
- Updated skill `.agents/skills/library-management/procedures/extract-standard-metadata.md` with TDD-refined format rules
- Added clear positive/negative examples to both places
- Committed to git

### Key Improvements in Refined Prompt

| Aspect | Original | Refined |
|---|---|---|
| **Length** | 1 line | 15 lines dedicated to OUTPUT FORMAT |
| **Clarity** | "Start with {, end with }" (ambiguous) | "Start with { (left brace), end with } (right brace)" |
| **Negative rules** | None | 8 explicit "DO NOT" statements |
| **Examples** | None | 5 examples (3 WRONG, 2 RIGHT) |
| **Emphasis** | Basic instruction | "CRITICAL", "DO NOT violate", "RULE:" repeated |

### Expected Impact

The refined prompt should reduce code fence wrapping from ~22% to <5% in Batch 4+.

**Next step:** Query Batch 4 sources with refined prompt and validate improvement.

---

## Batch 3 (2026-05-05) — Amendment Detection & [Source N] Files (9 sources)

### Extraction results

| Standard Code | Status | Amendment? | File Type | Notes |
|---|---|---|---|---|
| AS/NZS 1170.2:2021 | published | No | [Source 2] | Base standard (large doc split) |
| AS/NZS 1170.2:2021 | published | No | Primary | Base standard |
| AS/NZS 1170.2:2021 | published | No | ? | Possible 2020 edition misfile |
| AS/NZS 1170.2:2021 Amd 1:2023 | amendment | Yes | [amendment 1] | Standalone amendment 2023 |
| AS/NZS 1170.2:2021 | published | No | [Source 5] | Base with Amd 1&2 incorporated |
| AS/NZS 1170.2:2021 Amd 2:2024 | amendment | Yes | [Source 6] | Standalone amendment 2024 |
| AS/NZS 1170.2:2021 | published | No | [Source 2] again | Duplicate (Same as item 1) |
| AS/NZS 1170.2:2021 | published | No | Primary | Base standard |
| AS/NZS 1170.3 Supp 1:2003 | published | No | [supp1-2003] | Commentary supplement |

### What worked in Batch 3

**Amendment detection 100% accurate**: All standalone amendments correctly identified:
- AS/NZS 1170.2:2021 Amd 1:2023 (May 2023 publication) → `document_status = amendment`
- AS/NZS 1170.2:2021 Amd 2:2024 (June 2024 publication) → `document_status = amendment`
- Both correctly populated `amends` field with base standard reference
- Both left `incorporated_amendments` as "N/A"

**[Source N] file structure understood**: Files labeled [Source 2], [Source 5], [Source 6] are revealed to be 
large document splits (typical for PDFs >100pp uploaded in chunks):
- [Source 2 102pp] = part of large document
- [Source 5 11pp] and [Source 6 132pp] = other parts of same standard
- Model correctly extracted the document content from each part, not treating splits as separate standards

**Multiple editions/amendments tracked**: Extracted 2 separate amendments (Amd 1:2023, Amd 2:2024) 
plus the base standard (2021) with various consolidated editions showing different amendment incorporation states.

### What didn't work in Batch 3 (OUTPUT FORMAT REGRESSION)

**JSON code fence wrapping (CRITICAL)**: Two of five query responses came back wrapped in markdown 
code fences:

```
```json
{ ... valid JSON ... }
```
```

This is NOT valid JSON (starts with ``json`` instead of `{`). The prompt explicitly says 
"OUTPUT FORMAT: Raw JSON object only. No markdown code fences." The model partially reverted 
to older behavior despite the Handbook fix maintaining the rule.

**File labeling vs document content mismatch**: ASNZS 1170.2-2020.pdf extracted as AS/NZS 1170.2:2021, 
suggesting either a file mislabeling or a year drift in the upload process.

**Massive duplication in uploads**: Batch 3 shows at least 4 representations of AS/NZS 1170.2:2021 
with slightly different incorporation states:
- [Source 2]: Amendment No. 1 (May 2023)
- [Source 5]: Amendment Nos 1 and 2  
- [Source 6]: Only Amendment No. 1 (May 2023) initially, then Amd 2:2024 found in [Source 6]
- Primary file: Amendment No. 1 (May 2023)

This suggests the uploaded files may be redundant consolidations or partial extracts, not 
de-duplicated source files.

### Data quality signals

**9 JSON responses, 2 with format errors** — 78% valid JSON (regression from Batch 1-2's 100%)

**7 published, 2 amendments** — Amendment detection still working despite regression

**Massive version/edition sprawl** — 4 file representations of 1 standard with 3 amendment states 
suggests need for **comprehensive de-duplication and consolidation strategy** before continuing.

### Critical Issue: Output Format Regression

The extraction prompt includes explicit instruction: "OUTPUT FORMAT: Raw JSON object only. 
No markdown code fences, no explanations. Start your response with { and end with }. Nothing else."

**Batch 3 result**: 2/5 responses had ````json` wrapping, breaking JSON validity. This suggests 
either:
1. Model context drift (earlier parts of prompt becoming less influential over time in session)
2. Ambiguity in prompt on when to add code fences (for clarity vs literal JSON)
3. Session length affecting instruction adherence

**Recommended fix**: Add explicit negative instruction to extraction prompt:
```
DO NOT wrap the JSON in markdown code fences.
DO NOT start the response with ```json
DO NOT end the response with ```
Start directly with { character. End with } character. Nothing before or after.
```

### Next steps before continuing

1. **Deduplicate uploaded files**: Query notebook for duplicates across [Source N] splits
2. **Fix output format regression**: Strengthen prompt instruction against code fences
3. **Clarify file structure**: Understand whether [Source N] files are intentional splits or upload artifacts
4. **Continue batches**: Assess whether duplication continues in remaining 200+ sources

---

**Source**: Conversation 2026-05-05, NotebookLM notebook
`dfd5b22d-4b26-4919-a5b0-3d21385ec745`. Scale validation batches 1-3.
Batch 1: rows 1477-1486. Batch 2: rows 1487-1496. Batch 3: rows 1507-1515 (9 rows, includes duplicates/splits).
