---
name: eda-codebook
description: Generates and updates comprehensive Markdown codebooks (data dictionary + statistical profile) for CSV and Excel datasets. Covers output path logic, update-not-overwrite rules, statistical conventions, and the required document structure including a layperson glossary.
---

# EDA Codebook

Produce and maintain professional **Quantitative Codebooks** — structured Markdown documents
that combine a Data Dictionary with a Point-in-Time Data Profile — for any CSV or Excel
dataset in this project.

## Context & Guidelines

- **Scope**: Apply whenever the user asks to "create", "generate", or "update" a codebook,
  or asks to "profile" or "document" a dataset.
- **Audience**: Write for a non-technical reader. Use plain English column descriptions.
  Strictly use **UK English** spelling and grammar throughout (e.g. *analyse*, *colour*,
  *organisation*).
- **Inference**: If a column's meaning must be inferred, do so logically and note the
  inference. If the purpose is entirely ambiguous, write
  `"Requires clarification from data owner"`. Never hallucinate definitions.
- **Update, never overwrite**: If a codebook already exists for the dataset, append new
  findings, add new columns, and refresh statistics rather than replacing the file.
- **Hidden sheets**: Ignore and exclude any worksheet marked as hidden in Excel workbooks.

## Output Path Logic

The output file must be saved to:

```
docs/codebooks/**/<database_name_in_snakecase>.md
```

The `**` represents the directory hierarchy mirroring the dataset's location inside
`data/`. If the dataset lives outside the project, substitute the dataset's thematic
category for `**` (e.g. `engineering`, `environmental`, `financial`). Deduce the category
from project documentation; if it cannot be determined, present the user with logical
options and wait for confirmation.

**Example:**  
Dataset at `data/database/timber_pole_walls.xlsx` → output at
`docs/codebooks/database/timber_pole_walls.md`.

## Statistical Conventions

- **% Missing**: `ceil(missing_rows / total_rows * 100, 1)` — apply the ceiling function,
  rounded to exactly 1 decimal place. Include `NULL`, `NA`, and completely blank cells.
- **Numerical summaries**: Mean and Five-Number Summary (Min, Q1, Median, Q3, Max) must
  **exclude** all null/NA/blank values.
- **Cardinality**: Count exact unique values for all categorical, boolean, and string columns.
- **Most common value**: Report the mode for categorical/string columns. If the mode is a
  tie, list the tied values separated by ` / `.

### Semantic Type Override — Identifier Columns

Columns are classified as **Categorical** (factor) — regardless of their pandas dtype —
when their name (case-insensitive, word-boundary match) contains any of the following
identifier keywords:

| Keyword | Example column names |
|---|---|
| `ID` | `Wall ID`, `Project ID` |
| `UID` / `UUID` | `Survey UUID`, `Record UID` |
| `Number` | `Project Number`, `Reference Number` |
| `No` / `No.` | `Wall No`, `Sheet No.` |
| `Code` | `Site Code`, `Job Code` |
| `Ref` | `Project Ref`, `Drawing Ref` |
| `Key` | `Record Key` |

These columns **must** appear in the **Categorical & Factor Cardinality** profile table,
not in Numerical Summary Statistics, even when pandas reads them as `float64` or `int64`.
Record their Data Type as `Categorical` in the dictionary.

Apply this override in Python scripts via a helper and pattern constant:

```python
import re

_IDENTIFIER_RE = re.compile(
    r"\b(ID|UID|UUID|Number|No\.?|Code|Ref|Key)\b", re.IGNORECASE
)

def _is_identifier_col(name: str) -> bool:
    return bool(_IDENTIFIER_RE.search(name))
```

Then guard the two profile functions:

```python
# _cat_profile_rows — skip only truly numeric, non-identifier columns
if pd.api.types.is_numeric_dtype(df[col]) and not _is_identifier_col(col):
    continue

# _num_profile_rows — skip non-numeric AND identifier columns
if not pd.api.types.is_numeric_dtype(df[col]) or _is_identifier_col(col):
    continue
```

## File Type Logic

| Input type | Output structure |
|---|---|
| CSV | Exactly one Data Dictionary table + one set of statistical profile tables. |
| Excel workbook | One Data Dictionary **and** one statistical profile **per visible worksheet**, all within the single output file. |

## Procedure

### Step 0 — Pre-flight

1. Enumerate all sheets: `pd.ExcelFile(path).sheet_names`. Print the full list.
   **Never conclude a sheet is absent until every name in the full inventory has been
   inspected.** If a sheet's data looks wrong (e.g. wrong date range, duplicated rows),
   treat it as a copy-paste error and exhaust all remaining sheets in the same workbook
   before escalating to an external source.
2. Identify hidden sheets via openpyxl: exclude any sheet where `ws.sheet_state != "visible"`.
3. **Source-file acceptance checks** — before committing to a candidate source workbook,
   run all four checks:
   1. **Date audit**: For each sheet, compare `min()`/`max()` of date columns against the
      sheet name. Any mismatch is a hard stop.
   2. **Formula vs static audit**: Load with `openpyxl.load_workbook(..., data_only=False)`.
      For every column that should be computed, verify that at least one cell is a formula
      string (starts with `=`). A column of all plain numbers in a computed-output role
      means provenance is unknown — do not write a formula-error hypothesis until this
      check is run. If a cell returns a number, the value is hard-coded; look upstream
      for where the wrong number was introduced.
   3. **Inter-sheet distribution**: For key numeric columns, compute per-sheet IQR or
      range. Values ≥10× the cross-sheet range are red flags even without an external
      reference.
   4. **Cross-source spot-check**: If ≥2 files cover the same observations, join on
      (survey, site) for a sample of rows and compare key values. A discrepancy >10%
      means at least one source is wrong. The more processed a file appears, the more
      important these checks become — a merged workbook has had more opportunities to
      accumulate untracked errors than the raw upstream files it was derived from.
4. Run `df.describe()` on all numeric columns immediately after loading. For any
   column with `std == 0` or all-zero values, verify formula vs static (see check 3.2
   above) before proceeding. Raise an error rather than silently continuing:
   ```python
   zero_cols = [col for col in key_cols if df[col].dropna().eq(0).all()]
   if zero_cols:
       raise ValueError(f"All values are zero in {zero_cols} — check for stale formula cache.")
   ```
5. **Anomaly screening** — run domain-plausible range checks across all numeric columns
   (e.g. temperature: 0–100 °C for liquid water; pH: 0–14; DO: 0–20 ppm). Anomaly
   screening is an onboarding step, not a plot-debugging reaction. For each anomaly
   found, classify it as one of:
   - **(a)** Confirmed transcription/instrument error with recoverable true value.
   - **(b)** Suspected error; true value unknown.
   - **(c)** Genuine extreme observation.
   Record all three classes in the codebook regardless of whether the value is corrected.
6. Check the existing `docs/codebooks/` path — if a codebook file already exists, load
   it and update rather than creating from scratch.

### Step 1 — Build column labels

For Excel files with multi-row merged-cell headers, use openpyxl merged-cell ranges to
expand group labels correctly. **Do not use pandas `ffill()` on header rows** — it bleeds
group labels past their actual column span. See `python-data-ingestion` for the standard
`_expand_merged_row` pattern.

### Step 2 — Generate the document

Produce the Markdown file following the structure below, in strict order.

### Step 3 — Static checks

Run `uv run ruff check` and `uv run ruff format` on any Python script used to generate
the codebook before considering the task complete. See `python-static-checks`.

## Required Document Structure

Output must follow this exact sequential structure:

---

### 1  Document Header & Overview

```markdown
# [Dataset Name] — Data Codebook

## Overview

[2–3 sentences describing what the dataset represents.]

**File structure:** [Single-table CSV | Multi-sheet Excel workbook (sheets: Sheet1, Sheet2, …)]  
**Source file:** `[relative path to the source file]`  
**Codebook path:** `docs/codebooks/[category]/[name].md`  
**Profile date:** [YYYY-MM-DD]  
**Rows:** [n]  **Columns:** [n]
```

---

### 2  Findings, Caveats & Limitations

```markdown
## Findings, Caveats & Limitations

### Data Collection
[How the data was gathered, if known or clearly inferred.]

### Data Quality Issues
[Anomalies, high missingness, formatting inconsistencies, suspicious patterns.]

### Limitations
[Caveats a user must understand before modelling or statistical analysis.]
```

---

### 3  Data Dictionary (repeat per visible worksheet)

```markdown
### Worksheet / Table: [Name] — Dictionary

[One sentence describing what this sheet contains.]

| Variable Name | Description | Data Type | Coding Scheme / Allowed Values | Missing Data Handling |
| :--- | :--- | :--- | :--- | :--- |
| column_name | Plain English explanation. | Float | Metres above sea level; ≥ 0 | Left blank |
```

**Data Type values:** `String`, `Integer`, `Float`, `Boolean`, `Categorical`.

---

### 4  Data Profile (repeat per visible worksheet, immediately after its dictionary)

```markdown
#### Worksheet / Table: [Name] — Data Profile

**Categorical & Factor Cardinality**

| Variable Name | % Missing (Est.) | Cardinality (Unique Values) | Most Common Value (Sample) |
| :--- | :--- | :--- | :--- |
| column_name | 4.2% | 6 | Auckland |

**Numerical Summary Statistics (Excluding Nulls)**

| Variable Name | % Missing (Est.) | Mean | Min | Q1 (25%) | Median (50%) | Q3 (75%) | Max |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| column_name | 0.0% | 3.25 | 0.75 | 1.55 | 2.63 | 4.05 | 8.55 |
```

---

### 5  Glossary (domain terms only; omit section if none apply)

Include this section only when the dataset contains terms that a non-technical reader
would not know from general knowledge — for example:

- Acronyms and abbreviations specific to the project domain (e.g. `WGS84`, `DO`)
- Engineering or scientific method names (e.g. Nominatim geocoding, city-default coordinate)
- Domain jargon that appears as data values (e.g. `deadman anchor`, `waler beam`, `lagging`)

**Do NOT include** statistical or codebook meta-terms such as Cardinality, % Missing,
Five-Number Summary, Variable Name, Data Type, Coding Scheme, or Null / Missing Value.
Those describe the codebook format, not the dataset domain, and clutter the glossary for
subject-matter readers.

If the dataset has no domain-specific terms to explain, **omit this section entirely**.

```markdown
## Glossary

**[Term]:** [Plain-English definition in one or two sentences.]
```

---

## Codebook Content Rules

Codebooks document **data**, not code. They must be understandable by someone who has
never seen the codebase — a data reviewer, an auditor, or a future team inheriting the
dataset. The following content is **banned** from codebook files:

1. **No script, module, or notebook paths** — replace with a description of the data
   behaviour (e.g. "All Survey 1 N2O rows carry `qc_passed=False`" rather than
   "applied in `extract_n2o_rows()` in `ingest_lws_flux.py`").
2. **No code samples** — if a loading recipe is useful, put it in a developer guide or
   README alongside the code, not in the codebook.
3. **Discovery dates without notebook citations** — when documenting a data quality issue
   found during analysis, record "Discovered YYYY-MM-DD" without naming the notebook or
   script.
4. **ADR and data-inventory references are allowed** — these are decision/governance
   documents, not code artefacts.

## Python Script Conventions

When generating the codebook via a Python script, follow the `python-script` skill:

- Script lives at `src/scripts/create_<name>_codebook.py`.
- Spyder-style `# %%` cell structure; thin orchestration only.
- Use openpyxl for header/merge introspection; pandas for statistics.
- Write output with `Path.write_text(..., encoding="utf-8")`.
- Apply ceiling to % missing: `import math; math.ceil(pct * 10) / 10`.

## Related Skills

- `python-data-ingestion` — multi-row merged-cell header handling (`_expand_merged_row` pattern).
- `python-script` — script structure and cell conventions.
- `python-static-checks` — ruff lint/format checks before finishing.
- `eda-interpreting-data` — anomaly screening and insight writing for EDA plots.
