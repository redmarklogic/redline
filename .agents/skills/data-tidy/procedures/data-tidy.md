# Data Tidy — Detailed Reference

### Definitions

| Term                  | Definition                                                                                                                     |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Variable**    | A property of a unit of analysis that can take multiple values across observations (e.g.,`height`, `year`, `treatment`). |
| **Observation** | A unit of analysis measured at a point in time or context (e.g., one patient visit, one country-year combination).             |
| **Value**       | A single measurement: the intersection of one variable and one observation.                                                    |

**Identifying variables and observations is the critical first step.** When this is unclear, ask: "What is the unit of analysis for this table?" Variables describe properties; observations are instances of that unit.

---

## Context & Guidelines

- **Scope**: Apply when designing a new table/DataFrame, restructuring raw data, or defining Pandera/Pydantic schemas for tabular domain objects.
- **Language coverage**: Principles are language-agnostic. Tool references include Python (`pandas`, `polars`, `Pandera`) and R (`tidyr`, `dplyr`) as examples.
- **File placement**: Tidy schemas live in `src/<package>/domain/` (Pydantic value objects) or `src/<package>/functions/readers/` (Pandera DataFrameModels at boundaries).

---

### Pattern 1: Column names are values, not variable names

The variable is encoded in the column name itself. Each column represents a *value* of a variable (e.g., years, categories, time periods).

**Untidy** — year is spread across columns:

| country     | 1999  | 2000  |
| ----------- | ----- | ----- |
| Afghanistan | 745   | 2666  |
| Brazil      | 37737 | 80488 |

**Tidy** — year becomes a proper column:

| country     | year | cases |
| ----------- | ---- | ----- |
| Afghanistan | 1999 | 745   |
| Afghanistan | 2000 | 2666  |
| Brazil      | 1999 | 37737 |
| Brazil      | 2000 | 80488 |

**Remedy**: pivot (lengthen) — collapse the value-name columns into a single variable column and a single value column.

```python
### Pattern 2: One observation is scattered across multiple rows

Multiple rows in the table describe *the same* observation, with a type-indicator column splitting the values.

**Untidy** — one country-year observation across two rows:

| country     | year | type       | count    |
| ----------- | ---- | ---------- | -------- |
| Afghanistan | 1999 | cases      | 745      |
| Afghanistan | 1999 | population | 19987071 |

**Tidy** — each observation in one row:

| country     | year | cases | population |
| ----------- | ---- | ----- | ---------- |
| Afghanistan | 1999 | 745   | 19987071   |

**Remedy**: pivot (widen) — spread the type-indicator and its value column into separate variable columns.

```python
### Pattern 3: Multiple variables in one column

Two or more variables are concatenated into a single column, separated by a delimiter or positional encoding.

**Untidy** — `rate` encodes both `cases` and `population`:

| country     | year | rate         |
| ----------- | ---- | ------------ |
| Afghanistan | 1999 | 745/19987071 |

**Tidy** — each variable in its own column:

| country     | year | cases | population |
| ----------- | ---- | ----- | ---------- |
| Afghanistan | 1999 | 745   | 19987071   |

**Remedy**: split/separate the compound column into its constituent parts; validate types afterward.

```python
### Pattern 4: Multiple types of observational units in the same table

The table mixes rows from different units of analysis (e.g., song metadata and weekly chart positions in the same table). This violates the principle that each table captures one observational unit.

**Remedy**: split into separate, linked tables and join when needed. This mirrors third-normal-form (3NF) relational design.

---

### Rules for Schema Design

1. **One `DataFrameModel` per observational unit.** Do not build a schema that mixes two units of analysis.
2. **Each column maps to exactly one domain variable.** Reject compound columns (e.g., `age_sex`) at the schema level with a `@pa.parser` that splits them.
3. **Column names in the schema must match tidy column names** — they become the documented contract for downstream consumers.
4. **Enforce types strictly.** Avoid `object` dtype (Python) or character columns (R) when the domain type is numeric, date, or categorical.
5. **Declare nullable explicitly** — only allow `nullable=True` on a Pandera field when the column's NULL represents a genuine domain concept (e.g., "value not yet recorded"), not a data quality gap.
6. **Alias untidy source names at the boundary.** If raw data arrives with untidy column names (e.g., `2024`, `Type (A/B)`), rename at the ingestion boundary — never let untidy names survive into the domain schema.

### Example Schema (Python, Pandera)

See the `python-domain-modeling` skill for full field conventions. Key rules applied here:

- Add `description=` to every domain-relevant column (units and constraints included where meaningful).
- Use `alias=` at the boundary level to map untidy source column names to tidy Python identifiers; never let untidy names survive into the domain schema.

```python
import pandera.pandas as pa
from pandera.typing.pandas import Series
from typing import Optional


class TbCasesSchema(pa.DataFrameModel):
    """One row = one country-year-sex-age-type observation of TB cases."""

    country: str = pa.Field(
        nullable=False,
        description="ISO country name as reported by WHO.",
    )
    year: int = pa.Field(
        ge=1980,
        le=2030,
        description="Calendar year of the TB case count.",
    )
    sex: str = pa.Field(
        isin=["m", "f"],
        description="Sex of patients: 'm' = male, 'f' = female.",
    )
    age_group: str = pa.Field(
        isin=["0-14", "15-24", "25-34", "35-44", "45-54", "55-64", "65+"],
        description="Age band of patients (years).",
        # alias maps the raw source column name to this tidy field name
        alias="age_band",
    )
    diagnosis_type: str = pa.Field(
        isin=["sp", "sn", "ep", "rel"],
        description=(
            "TB diagnosis method: sp=smear-positive, sn=smear-negative, "
            "ep=extrapulmonary, rel=relapse."
        ),
    )
    cases: Optional[int] = pa.Field(
        ge=0,
        nullable=True,
        description="Number of TB cases. NULL means count was not recorded for this stratum.",
    )

    class Config:
        name = "TbCasesSchema"
        strict = True   # reject extra columns — the schema is the contract
        coerce = False  # fail loudly on wrong types; do not silently cast
```

### Example Schema (R, equivalent intent)

```r
## References

- Wickham, H. (2014). *Tidy Data*. Journal of Statistical Software, 59(10). [https://www.jstatsoft.org/v59/i10/paper](https://www.jstatsoft.org/v59/i10/paper)
- Wickham, H. & Grolemund, G. (2017). *R for Data Science*, Chapter 12: Tidy Data. [https://r4ds.had.co.nz/tidy-data.html](https://r4ds.had.co.nz/tidy-data.html)
- For Python DataFrame validation, use the `python-domain-modeling` skill for Pandera/Pydantic patterns.
- For ingestion at the boundary, use the `python-data-ingestion` skill.

# Tidy Data

This skill defines the structural principles of tidy data (Wickham, 2014) and
provides guidelines for applying them when designing tables, DataFrame schemas, and
value-object/model contracts — regardless of programming language.

> "Tidy datasets are all alike, but every messy dataset is messy in its own way."
> — Hadley Wickham, *R for Data Science*

## Core Tidy Data Rules

Three interrelated rules define a tidy dataset:

1. **Each variable has its own column.**
2. **Each observation has its own row.**
3. **Each value has its own cell.**

These three rules reduce to two practical instructions:

- Put each dataset in a single rectangular table.
- Put each variable in a column.

## Common Untidy Patterns and Remedies

# Python (pandas)
df.melt(id_vars=["country"], var_name="year", value_name="cases")

# Python (polars)
df.unpivot(index="country", variable_name="year", value_name="cases")
```

```r
# R (tidyr)
table4a |> pivot_longer(c(`1999`, `2000`), names_to = "year", values_to = "cases")
```

---

# Python (pandas)
df.pivot_table(index=["country", "year"], columns="type", values="count").reset_index()

# Python (polars)
df.pivot(index=["country", "year"], on="type", values="count")
```

```r
# R (tidyr)
table2 |> pivot_wider(names_from = type, values_from = count)
```

---

# Python (pandas)
df[["cases", "population"]] = df["rate"].str.split("/", expand=True).astype(int)
df = df.drop(columns="rate")
```

```r
# R (tidyr)
table3 |> separate(rate, into = c("cases", "population"), convert = TRUE)
```

---

## Column Naming Conventions

- **Use `snake_case` for all column names** (applies to both Python and R). Never use spaces, dots, or CamelCase in column names.
- **Name columns after the variable, not the encoding** — `year` not `y`, `treatment_group` not `grp1`.
- **Avoid abbreviations** unless the domain justifies them (e.g., `iso2`, established by a standard).
- **Type suffixes** where disambiguation is essential: `start_date`, `end_date`; `kg_weight`, `lb_weight`.
- **Never encode values in column names** (see Pattern 1). If you name a column `2024_revenue`, admit it is untidy.
- **Boolean columns**: prefix with `is_`, `has_`, or `was_` — `is_treated`, `has_missing_data`.
- **Identifier columns**: suffix with `_id` for surrogate keys, use the entity noun for natural keys — `patient_id`, `iso3`.

---

## Missing Values

A value can be missing in two ways:

- **Explicit**: present as `NA` / `None` / `NaN` — the absence is marked.
- **Implicit**: the row simply does not exist — the absence is invisible.

**Rule**: make implicit missing values explicit before analysis. Use `complete()` (R) or an explicit cross-join / `reindex` (Python) to fill the Cartesian product of key dimensions.

```python
# Python (pandas): expose implicit gaps in a time series
full_index = pd.MultiIndex.from_product(
    [df["country"].unique(), df["year"].unique()], names=["country", "year"]
)
df = df.set_index(["country", "year"]).reindex(full_index).reset_index()
```

```r
# R (tidyr)
stocks |> complete(year, qtr)
```

**Do not drop NA rows prematurely** — distinguish between "not recorded" (true NA), "not applicable" (structural NA), and "zero" (a real observation).

---

## DataFrame Schema Design (Tidy-First Contracts)

When designing a Pandera `DataFrameModel` or an equivalent typed schema, apply the tidy rules to the contract itself:

# Express constraints with pointblank
agent <- pointblank::create_agent(tbl = tb_cases) |>
  pointblank::col_is_character(columns = c(country, sex, age_group, diagnosis_type)) |>
  pointblank::col_is_integer(columns = c(year, cases)) |>
  pointblank::col_vals_in_set(columns = sex, set = c("m", "f")) |>
  pointblank::col_vals_gte(columns = year, value = 1980) |>
  pointblank::col_vals_gte(columns = cases, value = 0, na_pass = TRUE) |>
  pointblank::interrogate()
```

---

## Value-Object Design for Tidy Data

When wrapping a tidy row as a typed value object (Pydantic), the same rules apply:

- **One class = one observational unit.** The class name names the unit, e.g., `TbObservation`, `WallSegment`.
- **Each field = one variable.** Never use `dict` or `str` fields that smuggle multiple values.
- **Use narrow types.** Prefer `Literal["m", "f"]` over `str`; `date` over `str` for dates.
- **Forbid compound fields.** A field named `age_sex` is untidy — split it.
- **Frozen for value semantics.** When the object represents a measured observation (not an entity), use `ConfigDict(frozen=True)`.

```python
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class TbObservation(BaseModel):
    """One tidy row: a TB case count for a specific country-year-sex-age-type."""

    model_config = ConfigDict(frozen=True)

    country: str
    year: int = Field(ge=1980, le=2030)
    sex: Literal["m", "f"]
    age_group: Literal["0-14", "15-24", "25-34", "35-44", "45-54", "55-64", "65+"]
    diagnosis_type: Literal["sp", "sn", "ep", "rel"]
    cases: int | None = Field(default=None, ge=0)
```

---

## When NOT to Use Tidy Format

Tidy is the safe default for analysis. Legitimate reasons to deviate:

| Situation                                       | Why wide/non-tidy may be justified                                                                                               |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Machine learning feature matrices**     | Algorithms expect one-row-per-sample, one-column-per-feature; tidy "long" format would require pivoting before every fit.        |
| **Reporting / pivot tables**              | Human-readable tables are often deliberately wide (e.g., years as columns, countries as rows). Store tidy; display wide.         |
| **Performance-critical joins**            | Wide tables avoid joins; acceptable in data warehousing (star-schema fact tables are tidy; dimension tables are naturally wide). |
| **Sparse data**                           | When most cells are empty, a long table with an index is more efficient than a wide matrix of NAs.                               |
| **Time-series with aligned observations** | Financial tick data, sensor arrays — same timestamp for all channels; a matrix format is natural and efficient.                 |

**Rule**: store data tidy; reshape for the consumer (report, model, chart). Never let display format infect the stored or intermediate representation.

---

## Quick Diagnostic Checklist

Before finalising a table design or schema, verify:

- [ ] I can name the **unit of analysis** for this table in one noun phrase.
- [ ] Every column name is a **variable**, not a value.
- [ ] Every row is a **single observation** of the unit of analysis.
- [ ] Every cell holds **exactly one value** (no slashes, commas, or concatenation).
- [ ] Column names are `snake_case` and carry no encoded values.
- [ ] Missing values are `NULL`/`NA`/`None`; implicit gaps are made explicit before analysis.
- [ ] The schema or model contract rejects untidy column names at the boundary.

---
