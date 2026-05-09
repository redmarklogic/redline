# 0013 — SNZ scraper: parenthetical qualifiers, "Amd" suffix, and "Supp" abbreviation break matching

**Date**: 2026-05-06 (updated 2026-05-06 after second sample)

**Skill**: `python-testing-unit` (link: `.agents/skills/python-testing-unit/SKILL.md`)

**Context**: Live test-drive of `get_snz_metadata` (`.agents/tools/library/snz_scraper.py`)
against 10 NZ standards drawn from the library index
(`G:\My Drive\Library\library-index.xlsx`, Standards worksheet). Sample was deliberately
diverse: geotechnical, structural, OHS, environmental, ISO-prefixed, ISO/IEC-prefixed,
supplement, and amendment formats.

---

## Observation

7 of 10 queries returned correct `StandardRecord` objects. 3 failed:

| Query | Outcome | Root cause |
|---|---|---|
| `NZS 1170.5:2004` | `AmbiguousStandardError` | SNZ search result text includes `(Excludes Amdt 1)` appended to the number |
| `NZS 1170.5 Supp 1:2004` | `AmbiguousStandardError` | Two variants sold: `(Includes Amdt 1)` and `(Excludes Amdt 1)` |
| `AS/NZS 1269.1:2005 Amd 1:2005` | `StandardNotFoundError` | SNZ does not index amendments as separate search items |

Live inspection of the search parser (`_SearchPageParser`) for `NZS 1170.5:2004` revealed
the site returns these as the `<h5>` link texts:

```
'NZS 1170.5:2004 (Excludes Amdt 1)'     -> /shop/NZS-1170-52004-EXCLUDES-AMDT-1
'NZS 1170.5 Supp 1:2004 (Includes Amdt 1)' -> /shop/NZS-1170-5-SUPP-12004-INCLUDES-AMDT-1
'NZS 1170.5 Supp 1:2004 (Excludes Amdt 1)' -> /shop/NZS-1170-5-SUPP-12004-EXCLUDES-AMDT-1
'SNZ TS 1170.5 Supp 1:2025'             -> /shop/SNZ-TS-1170-5-SUPP-12025
'ISO/TR 25741-1:2025'                   -> (unrelated)
```

The parenthetical qualifier `(Excludes Amdt 1)` is part of the display text captured by
`_SearchPageParser` as the full `standard_number`. After `_normalize_query` strips the
prefix, the result becomes `"1170.5:2004 (Excludes Amdt 1)"`, which does not match the
normalised query `"1170.5:2004"` — neither exact equality nor the starts-with-boundary
test passes.

---

## Root Cause

**Issue 1 — parenthetical qualifiers in search result display text.**
The SNZ site appends amendment-variant descriptors in parentheses (e.g., `(Excludes Amdt 1)`,
`(Includes Amdt 1)`) directly to the standard number in the `<h5>` link text. These are
_display annotations_, not part of the standard designation. `_SearchPageParser` stores them
verbatim as the standard number, and `_query_matches` has no logic to strip or ignore them.

**Issue 2 — "Amd N:YEAR" suffix in library index codes.**
Some library index entries encode amendments as `AS/NZS 1269.1:2005 Amd 1:2005`. The SNZ
site does not surface amendments as separately discoverable products; searching for the full
string finds nothing. The scraper should either strip `\s+Amd\s+\d+[:\d]*$` from the query
before searching, or raise a clearer error explaining the format problem.

---

## Principle

**Strip parenthetical display annotations from search result numbers before comparison.**
In `_normalize_query` (or in a dedicated `_clean_result_number` helper called before
storing in `_SearchPageParser.results`), remove trailing `\s*\([^)]+\)\s*` patterns. This
is safe because no standard designation ever includes parentheses.

**Also strip amendment suffixes from incoming queries.**
Before passing the query to the search URL, strip `\s+Amd\s+[\d:.]+$` (case-insensitive).
The SNZ catalogue indexes the base standard, not individual amendments.

---

## Actionable test cases to add

1. `"NZS 1170.5:2004"` → should resolve to exactly the base edition (URL containing
   `NZS-1170-52004-EXCLUDES-AMDT-1` or `INCLUDES-AMDT-1`; either is acceptable; the tool
   should not raise `AmbiguousStandardError`). **Currently fails.**

2. `"NZS 1170.5 Supp 1:2004"` → should raise `AmbiguousStandardError` listing both
   `(Includes Amdt 1)` and `(Excludes Amdt 1)` variants. **Currently raises AMBIGUOUS but
   for the wrong reason** (parenthetical is included in the error message, making the
   options hard to read).

3. `"AS/NZS 1269.1:2005 Amd 1:2005"` → should either (a) strip the amendment suffix,
   search for `"AS/NZS 1269.1:2005"` and return the base standard, or (b) raise
   `StandardNotFoundError` with a message explaining that amendment suffixes are not
   supported. **Currently raises NOT_FOUND with no guidance.**

---

## What worked well

- `AS/NZS N.N:YYYY` format: all resolved correctly, including superseded standards.
- ISO cross-reference prefix (`AS/NZS ISO 14040:1998`): resolved correctly.
- ISO/IEC double prefix (`AS/NZS ISO/IEC 38500:2010`): resolved correctly.
- Recent 2025 standard (`AS/NZS 2312.3:2025`): resolved correctly.
- `_normalize_query` correctly handles `ASNZS`, `AS/NZS`, `AS`, `NZS` prefix variants.

---

**Source**: Live test-drive sessions, 2026-05-06 (two rounds: 10 + 10 standards).
Relevant files: `.agents/tools/library/snz_scraper.py`, `tests/test_snz_scraper.py`.

---

## Bug 3 (found in second sample): "Supp N" vs "Supplement N" abbreviation mismatch

### Observation

Two standards in the second sample of 10 failed with `AmbiguousStandardError: No result matches`:

| Query | Site returns |
|---|---|
| `AS/NZS 3725 Supp 1:2007` | `AS/NZS 3725 Supplement 1:2007` |
| `AS/NZS 1170.1 Supp 1:2002` | `AS/NZS 1170.1 Supplement 1:2002` |

The library index (and common usage) abbreviates "Supplement" as "Supp". The SNZ site consistently
uses the full word "Supplement" in its product titles. After prefix stripping, the normalised
query `"3725 Supp 1:2007"` never matches the normalised result `"3725 Supplement 1:2007"`.

### Root Cause

`_normalize_query` strips the AS/NZS prefix but does not expand "Supp" → "Supplement". The
mismatch is a vocabulary normalisation gap, not a parser bug.

### Fix

In `_normalize_query` (or in a dedicated `_expand_abbreviations` step applied to the query
before comparison), expand `\bSupp\b` → `Supplement` (case-insensitive). Since "Supp" never
appears in standard designations except as an abbreviation for "Supplement", this substitution
is safe.

Alternatively, apply normalisation symmetrically: collapse "Supplement" → "Supp" in both
query and result before comparing. Either direction works; expanding in the query is simpler
because it only touches one code path.

### Test case to add

`"AS/NZS 3725 Supp 1:2007"` → should resolve to a single URL containing `3725`. **Currently fails with AMBIGUOUS/no-match.**

### Second-sample summary (10 standards, 8 subdomains)

| Query | Outcome |
|---|---|
| `AS/NZS 3016:2002` | OK — Current |
| `AS/NZS 3580.10.1:2003` | OK — Superseded |
| `AS/NZS 1200:2000` | OK — Superseded |
| `AS/NZS 3725 Supp 1:2007` | **AMBIGUOUS** — Bug 3 |
| `AS/NZS 3582.3:2002` | OK — Superseded |
| `AS/NZS 3661.1:1993` | OK — Superseded |
| `AS/NZS 3833:1998` | OK — Superseded |
| `AS/NZS ISO 19011:2019` | OK — Current |
| `AS/NZS 1170.1 Supp 1:2002` | **AMBIGUOUS** — Bug 3 |
| `NZS 4600:2005` | OK — Superseded (resolved as `AS/NZS 4600:2005`; prefix stripping handled it correctly) |

---

## Third sample (30 unique NZS/ASNZS codes from index after normaliser, 2026-05-06)

**Context**: First live test-drive after `normalise_standard_code` was added to `naming_conventions.py`
and integrated into `get_snz_metadata`. 30 unique codes drawn from the Standards worksheet (deduped
by normalised query). **Result: OK=18 NOT\_FOUND=3 AMBIGUOUS=9.**

### OK (18/30)

| Raw index code | Resolved as | Status |
|---|---|---|
| `NZS 6807` | `NZS 6807:1994` | Current |
| `AS/NZS ISO 14040:1998` | `AS/NZS ISO 14040:1998` | Current |
| `AS/NZS 1546.3:2008` | `AS/NZS 1546.3:2008` | Current |
| `AS/NZS 1580.204.1:1998` | `AS/NZS 1580.204.1:1998` | Current |
| `AS/NZS 1576.5:1995` | `AS/NZS 1576.5:1995` | Current |
| `NZS 3112.2.86.A1` | `NZS 3112.2:1986` | Sponsored |
| `AS/NZS 1328.2:1998` | `AS/NZS 1328.2:1998` | Withdrawn |
| `NZS 3605` | `NZS 3605:2001` | Sponsored |
| `NZS 4608` | `NZS 4608:1992` | Sponsored |
| `AS/NZS 1576.3:1995` | `AS/NZS 1576.3:1995` | Superseded |
| `ASNZS 1170.0-2002 [Amdt 5]` | `AS/NZS 1170.0:2002` | Current |
| `NZS 4402.4.2.3` | `NZS 4402.4.2.3:1988` | Sponsored |
| `AS/NZS 3580.10.1:2003` | `AS/NZS 3580.10.1:2003` | Superseded |
| `AS/NZS 1170.1 Supp 1:2002` | `AS/NZS 1170.1 Supplement 1:2002` | Current |
| `NZS 3605-2001 [Source 2 26pp]` | `NZS 3605:2001` | Sponsored |
| `NZS 5262-2003 [Source 2 34pp]` | `NZS 5262:2003` | Sponsored |
| `ASNZS 1170.0 [Extract 11pp]` | `AS/NZS 1170.0:2002` | Current |
| `NZS 4411-2001 [Source 2 27pp]` | `NZS 4411:2001` | Current |

### NOT\_FOUND (3/30) — genuinely absent from SNZ catalogue

| Raw index code | Normalised query | Real standard | Diagnosis |
|---|---|---|---|
| `ASNZS 56674` | `AS/NZS 56674` | **AS/NZS 5667.4:1998** | Missing decimal: `5667` + `.` + `4` run together |
| `ASNZS 56676` | `AS/NZS 56676` | **AS/NZS 5667.6:1998** | Missing decimal: `5667` + `.` + `6` run together |
| `ASNZS 566711` | `AS/NZS 566711` | **AS/NZS 5667.11:1998** | Missing decimal: `5667` + `.` + `11` run together |

All three are from the **AS/NZS 5667 — Water Quality — Sampling** series. The decimal
point between the series number (`5667`) and the part number was dropped when the files were
originally named and indexed. The files exist and are in the correct folder
(`G:\My Drive\Library\Engineering Standards\AS-NZS\`); no move is needed.

Confirmed by: sibling files `ASNZS 56671-1998.pdf` (part 1), `ASNZS 566712-1999.pdf`
(part 12), and `ASNZS 5667.12.pdf` (same series, correctly notated) all present in the same
folder. Earlier IEC 60567 / IEC 60335 hypotheses were incorrect.

**Action**: Update library index entries to `AS/NZS 5667.4:1998`, `AS/NZS 5667.6:1998`,
`AS/NZS 5667.11:1998`. Rename the three PDF files to use the canonical dot-separator
convention (`ASNZS 5667.4-1998.pdf`, etc.) consistent with `ASNZS 5667.12.pdf`.
The SNZ scraper should find them once the index codes are corrected. Graeme to confirm
exact part titles before finalising the index entries.

### AMBIGUOUS (9/30) — classified by root cause

**Root cause A — year stripped by amendment normaliser, multiple editions exist on SNZ (4 cases):**
These codes had `.AN` or `[Amdt N]` suffix which the normaliser stripped, leaving a year-less
base number that matches multiple editions on SNZ.

| Raw | Normalised query | SNZ editions found |
|---|---|---|
| `ASNZS 4911` | `AS/NZS 4911` | 2003, 1998 |
| `ASNZS 4671.A1` | `AS/NZS 4671` | 2019, 2001 |
| `NZS 3104.A2` | `NZS 3104` | 2021, 1991, 2003, 1983 |
| `AS/NZS 3500.3/Amdt 3` | `AS/NZS 3500.3` | 2025, 2021, 2003, 2018, 2015, + sub-part |

Conclusion: the amendment suffix encoding in the library filename *did* contain version
information, but we lost it because `.A2` tells us the amendment number not the base year.
These codes need manual year lookup.

**Root cause B — no year in index code at all, multiple editions exist (4 cases):**

| Raw | Normalised query | SNZ editions found |
|---|---|---|
| `ASNZS 4602` | `AS/NZS 4602` | NZS 4602:1988, AS/NZS 4602.2:2013, AS/NZS 4602.1:2011, AS/NZS 4602:1999 |
| `NZS 5262` | `NZS 5262` | 1997, 2003 |
| `NZS 4509` | `NZS 4509` | (now AS/NZS 4509.1 and 4509.2 — series split) |
| `NZS 4411` | `NZS 4411` | 2001, AS/NZS 4411:2015, AS/NZS 4411:1996 |

These are expected: no year was ever in the index for these codes. They require manual resolution.

**Root cause C — Bug 4: `AS/NZS 9001` became `AS/NZS ISO 9001` on SNZ (1 case):**

| Raw | Normalised query | SNZ returns |
|---|---|---|
| `ASNZS 9001-2008 [Amdt 1]` | `AS/NZS 9001:2008` | `AS/NZS ISO 9001:2008` |

SNZ re-designated `AS/NZS 9001` as `AS/NZS ISO 9001` when it was aligned to the ISO standard.
`normalise_snz_query` strips `AS/NZS` leaving `9001:2008`, but the result has `ISO 9001:2008`
after stripping. The `ISO` infix breaks the match.

**Fix required**: `normalise_snz_query` must also strip an optional `ISO` or `ISO/IEC` infix
that can appear between the `AS/NZS` prefix and the number. Apply symmetrically to both
query and result.

Test case to add:
```python
("ASNZS 9001-2008 [Amdt 1]", "AS/NZS ISO 9001:2008")  # should resolve, not fail
```
