---
name: eda-qa
description: Ingests an existing codebook + raw dataset, nominates data quality problems, validates hypotheses, and updates the codebook's Findings section with concrete findings. If no codebook exists, stops and directs the user to run eda-codebook first.
---

# EDA — Data Quality Assurance

Rigorously interrogate datasets against their existing codebook. Do not take data at face
value. Proactively nominate potential problems, validate those hypotheses against the data,
and update the target codebook with concrete, actionable findings.

Strictly use **UK English** spelling and grammar throughout (e.g. *analyse*, *colour*,
*organisation*).

## Boundary Contract

### Applies To
- Raw datasets with an existing codebook for data quality investigation

### Produces
- Updated codebook Findings section with validated data quality problems

### Does Not Cover
- Codebook creation (`eda-codebook`)
- Visual design (`eda-visual-design`)
- Pre-flight data screening (`eda-interpreting-data`)

## Context & Guidelines

- **Scope**: Apply whenever the user asks to "QA", "validate", "check", or "audit" a
  dataset, or asks to "update the codebook with quality findings".
- **Prerequisites**: A codebook **must** exist at `docs/codebooks/**/<name>.md` before
  any QA work begins. **BLOCKING RULE**: If no codebook is found, stop immediately, inform
  the user, and apply the `eda-codebook` skill to generate one first. Do not proceed with
  QA until the codebook exists and has been loaded.
- **Update, never overwrite**: Expand **Section 2 — Findings, Caveats & Limitations** of
  the existing codebook. Do not replace or reformat sections that are not affected.
- **Objectivity**: State findings as concrete observations with supporting counts or
  percentages. Never soften a genuine flaw.
- **Living QA rules**: The specific checks listed in the Procedure below will grow over
  time. When the user adds a new rule, append it to the "Specific Data Quality Checks"
  section of this skill file.

## Operational Workflow

### Step 1 — Locate and ingest codebook and data

1. **Check for an existing codebook** at `docs/codebooks/**/<name>.md`.
   - Derive the expected path from the dataset location: mirror the `data/` subdirectory
     hierarchy under `docs/codebooks/` and use the dataset filename in `snake_case`.
   - If the file **does not exist**: stop, tell the user the codebook is missing, and
     instruct them to create it first using the `eda-codebook` skill before re-running QA.
   - If the file **exists**: load and parse it fully before touching the dataset.
2. Read the expected schema from the codebook: column names, data types, coding schemes,
   allowed values, and any previously documented limitations.
3. Load the raw dataset. For Excel, enumerate all visible sheets and skip hidden ones.
   **Caution**: Two files with similar names (e.g. both containing "combined") can have
   opposite quality status. Do not assume completeness from filename similarity — always
   cross-check candidate files against upstream raw sources before selecting one.
4. Run `df.info()` and `df.describe(include="all")` immediately after loading to get a
   structural overview. Cross-check column names and dtypes against the codebook.

### Step 2 — Nominate potential problems (hypothesis generation)

Before writing any validation code, explicitly list every anomaly you suspect. Always
check for:

| Category | Examples to look for |
|---|---|
| **Logical contradictions** | End date before start date; total length smaller than a subcomponent; embedded depth greater than column length |
| **Implicit nulls** | Sentinel values masquerading as real data: `999`, `-1`, `0` in physical measurement columns, `1970-01-01`, `"Unknown"`, `"N/A"` as strings |
| **Formula vs static** | For Excel sources: load with `openpyxl data_only=False`. A computed-output column that returns only plain numbers (no `=` formula strings) has unknown provenance. Do not label it a formula error until this is confirmed. |
| **Cardinality clashes** | Boolean column with 3+ distinct values; categorical column with spelling/case variants (e.g. `Auckland` vs `auckland` vs `Auck.`) |
| **Outliers & impossible values** | Negative physical distances, currency, or areas; values outside physically plausible domain bounds |
| **Correlated missingness** | Is a column blank only when another column holds a specific value? |
| **Text formatting** | Leading/trailing whitespace in string columns |

Present nominated issues as a bulleted list before running any validation.

### Step 3 — Explore & validate

For each nominated issue:

1. Write and run the minimal pandas code required to confirm or refute the hypothesis.
2. Record the result: confirmed (with count/percentage), refuted, or inconclusive.
3. If confirmed, capture a representative sample (up to 5 rows) for the codebook update.

```python
# Example: check for sentinel zeros in physical measurement columns
physical_cols = ["retained_height_m", "embedment_m", "pole_diameter_mm"]
for col in physical_cols:
    zeros = df[df[col] == 0]
    if not zeros.empty:
        print(f"{col}: {len(zeros)} sentinel-zero rows")
        print(zeros[["wall_id", col]].head())
```

```python
# Example: check for correlated missingness
import pandas as pd
missing_mask = df["embedment_m"].isna()
print(df.loc[missing_mask, "temporary_works"].value_counts(dropna=False))
```

```python
# Example: check for leading/trailing whitespace
str_cols = df.select_dtypes(include="object").columns
for col in str_cols:
    dirty = df[col].dropna().str.strip() != df[col].dropna()
    if dirty.any():
        print(f"{col}: {dirty.sum()} rows with whitespace padding")
```

### Step 4 — Update the codebook

**Primary target — Section 2: Findings, Caveats & Limitations**

Add a dated sub-heading for this QA pass and document each confirmed anomaly:

```markdown
### QA Pass — [YYYY-MM-DD]

#### [Anomaly Title]
- **Affected column(s):** `column_name`
- **Finding:** [Plain English description with count/percentage.]
- **Recommendation:** [How future analysts should handle this.]
```

**Secondary target — Data Dictionary table**

If the QA pass reveals undocumented coding schemes, new null representations, or
incorrect data types, update the relevant row(s) in the dictionary table directly.
Note the change with `*(updated [YYYY-MM-DD])*` in the Description cell.

## Specific Data Quality Checks

This is the **living list** of checks. Append new rules here as the user defines them.

1. **Text whitespace**: Leading/trailing whitespace in all `object`/string columns.
2. **Correlated missingness**: For every column with > 10 % missing values, test whether
   the pattern is correlated with at least the two most likely explanatory columns
   (e.g. a flag column, a year column).
3. **Copy-paste contamination**: When a copy-paste or provenance error is confirmed in a
   source sheet, audit **every** column that originates from the affected sheet — not
   only the triggering column. Use a cross-round identity check
   (`df_a[col].equals(df_b[col])` for all shared columns) to detect silent contamination
   in fields that were not the focus of the original investigation.
4. **Formula vs static**: For Excel sources, load with `openpyxl data_only=False` and
   verify that computed output columns contain at least one formula string (starting
   with `=`). A column of all plain numbers in a computed-output role means the
   calculation provenance is outside the file and may be unrecoverable.

## Output Format

Structure every response under these three headings, in order:

```markdown
### Nominated Issues
- [Bulleted list of suspected anomalies, before any code is run]

### Exploration Results
- [Short summary per hypothesis: Confirmed (N rows) / Refuted / Inconclusive]

### Codebook Update
[Full updated codebook Markdown, maintaining exact original structure]
```

## Related Skills

- `eda-codebook` — the codebook format and structure that this skill reads and updates.
- `eda-interpreting-data` — anomaly screening conventions, sentinel-zero patterns, and
  axis-compression diagnosis that inform hypothesis generation.
- `python-data-ingestion` — pre-flight checks (sheet enumeration, formula vs static
  audit, non-zero guard) that apply before any QA analysis.
- `python-static-checks` — run ruff lint/format on any generated Python scripts.
