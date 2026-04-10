---
name: python-data-ingestion
description: Standard Operating Procedure for data ingestion and validation. Defines the import/process/read function pattern in functions/readers/<entity>.py, Pandera DataFrameModel contracts, schema reuse across sources, multi-worksheet handling, TDD workflow, and module exposure conventions. domain/ is reserved for pure model objects (classifiers, value objects, constants).
---

# Python Data Ingestion & Validation

Modular **ETL** pipeline using the **Functional Core / Imperative Shell** pattern, with
each domain entry point exposed as a **Facade**.

| Layer                | Prefix      | Role                                                             |
| -------------------- | ----------- | ---------------------------------------------------------------- |
| **Imperative Shell** | `import_*`  | I/O only. File reads, `skiprows`, `sheet_name`. Side-effectful.  |
| **Functional Core**  | `process_*` | Pure function. Rename, cast, fill, validate. No side effects.    |
| **Facade**           | `read_*`    | Only function pipeline code should call. Composes the two above. |

Related skills: `python-domain-modeling`, `test-driven-development`, `python-testing-unit`,
`python-function-design`, `python-typing`.

## Rules

- **pandera >= 0.30.0** — use `pa.DataFrameModel`, not the legacy `pa.SchemaModel`.
- **Module naming** — each reader module is named after its entity (e.g. `customers.py`,
  `sales.py`) and lives flat inside `functions/readers/`. Never use `readers.py` as the
  module name; never shadow a stdlib module.
- **Dependency direction** — `functions/readers/<entity>.py` imports from `schemas/<entity>.py`
  and may import utilities from `domain/utils/`; never the reverse. Cross-domain: a reader may
  import another entity's schema from `schemas/`; must never import another entity's reader module.
- **`domain/` is model-objects only** — `domain/` holds classifiers, value objects, constants,
  and shared utilities. No `import_*`, `process_*`, or `read_*` functions belong there.
- **Schema reuse** — before creating a new `DataFrameModel`, check whether the logical
  entity is already modelled. Reuse or subclass. Duplication drifts silently.
- **`__init__.py`** — expose only `read_*` wrappers. `import_*` and `process_*` are
  implementation details.

## Directory Structure

```
src/<pkg_name>/
├── schemas/
│   ├── __init__.py           # re-exports all DataFrameModel classes
│   ├── customers.py          # CustomerModel
│   └── sales.py              # RetailModel, WholesaleModel
├── functions/
│   ├── __init__.py
│   └── readers/
│       ├── __init__.py         # re-exports all read_* facades
│       ├── customers.py        # import_*, process_*, read_customers
│       └── sales.py            # import_*, process_*, read_sales_retail, read_sales_wholesale
└── domain/
    ├── constants/            # pure constants
    ├── models/               # value objects, domain models
    ├── site_classification/  # classifiers
    └── utils/                # shared utilities (e.g. excel.py)
```

Schemas live in the shared `schemas/` package. Reader modules live flat inside
`functions/readers/<entity>.py` — one file per logical entity. They import from
`schemas/` and may import utilities from `domain/utils/`.

`domain/` contains only pure model objects — it must not contain `import_*`, `process_*`,
or `read_*` functions.

## Procedure

### Step 0 — Pre-flight checks (workbooks only)

Run these **before writing any reader**. Never skip based on a filename or verbal
description.

**1. Enumerate all sheets**

```python
pd.ExcelFile("path/to/file.xlsx").sheet_names
```

Print the full list. If a sheet contains wrong data for its label (e.g. April dates in a
July-labelled sheet), that is a copy-paste error — the correct data may be in another
sheet of the same workbook. Exhaust the full sheet inventory before escalating.

**2. Formula vs static audit**

Load with `openpyxl data_only=False`. Columns that should be computed must contain at
least one formula string (starts with `=`). A column of plain numbers in a
computed-output role has unknown provenance — treat the file as suspect.

```python
import openpyxl
wb = openpyxl.load_workbook(path, data_only=False)
print(wb["Sheet1"]["B2"].value)  # formula string → live; number → static (unknown origin)
```

**3. Anomaly screen**

Run `df.describe()` on all numeric columns immediately after loading. Hard stops:

- Values outside physically plausible bounds (e.g. temperature > 100 °C for liquid water).
- `std = 0` or all values zero — `pd.read_excel` silently returns all-zero DataFrames when
  openpyxl's formula cache is stale (common on master/summary sheets). Raise immediately.
- Sentinel zeros: rows where **all** measurement columns are exactly `0.0` but structural
  columns (site ID, timestamp) are non-null. Replace with `NaN` and document.

**4. Cross-source spot-check**

If two or more files claim to cover the same observations, join on (survey, site) for a
sample of rows and compare key values. A discrepancy > ~10% means at least one source is
wrong. The more processed a file appears, the higher the risk — consolidated workbooks
have had more opportunities to carry untracked errors than the raw upstream CSVs they were
derived from.

**Sheets to skip**

| Type                 | Action                                                              |
| -------------------- | ------------------------------------------------------------------- |
| Hidden               | Skip — off-contract, content may be unstable.                       |
| Empty                | Skip — returns an empty DataFrame that will fail schema validation. |
| Scratchpad / working | Skip — irregular layout, merged cells, free-form notes.             |
| Lookup / reference   | Skip unless required by downstream logic.                           |

Document every skipped sheet with a comment above the first reader:

```python
# Sheet "Scratch" skipped — unstructured working notes, no stable schema.
```

### Step 1 — Schema first

Create `schemas/<entity>.py` before any reader code.

- One `pa.DataFrameModel` per logical table.
- Internal names: `snake_case`. Business alias: `alias="Title Case"`.
- `Config.strict = True` — reject unexpected columns.
- `@pa.check` for domain constraints (plausible ranges, non-empty strings, etc.).

```python
# schemas/customers.py
import pandera as pa

class MeasurementModel(pa.DataFrameModel):
    site_id: str = pa.Field(alias="Site ID")
    flux_ch4: float = pa.Field(ge=0.0, alias="CH4 Flux (g/m²/d)")

    class Config:
        strict = True
```

### Step 2 --- TDD (see `test-driven-development` and `python-testing-unit`)

1. Fixture file under `tests/assets/<domain>/` — include edge cases (empty rows, offset headers).
2. **Red** `test_import_*` — assert raw shape and columns only.
3. **Green** `import_*` — tune `skiprows`, `sheet_name`, `header`. Add non-zero guard on key columns.
4. **Red** `test_process_*` — assert result validates against schema.
5. **Green** `process_*` — rename, cast, fill, `Model.validate(df)`.
6. `read_*` — thin wrapper; one integration test against the fixture file.

### Step 3 — Single-table reader

```python
# functions/readers/customers.py
from pathlib import Path

import pandas as pd
from pandera.typing import DataFrame

from <pkg_name>.schemas.customers import CustomerModel


def import_customers(path: str | Path) -> pd.DataFrame:
    """Imperative shell (Extract): read raw file."""
    df = pd.read_csv(path, skiprows=2)
    zero_cols = [c for c in ("revenue", "quantity") if c in df and df[c].dropna().eq(0).all()]
    if zero_cols:
        raise ValueError(f"All values zero in {zero_cols} from {path} — check formula cache.")
    return df


def process_customers(df: pd.DataFrame) -> DataFrame[CustomerModel]:
    """Functional core (Transform): pure — rename, cast, fill, validate."""
    df = df.copy()
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df["is_active"] = df["is_active"].fillna(False)
    return CustomerModel.validate(df)


def read_customers(path: str | Path) -> DataFrame[CustomerModel]:
    """Facade: single entry point."""
    return process_customers(import_customers(path))
```

### Step 4 — Multi-worksheet reader

After Step 0, create distinct `import_<sheet>_sheet` / `process_<sheet>_sheet` pairs and
flat `read_*` wrappers:

```python
# functions/readers/sales.py
from .schema import RetailModel, WholesaleModel

# Sheet "Admin" skipped — internal lookup table, not required by this pipeline.

# --- Worksheet: Retail ---
def import_retail_sheet(path: str | Path) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name="Retail", skiprows=1)

def process_retail_sheet(df: pd.DataFrame) -> DataFrame[RetailModel]:
    return RetailModel.validate(df)

# --- Worksheet: Wholesale ---
def import_wholesale_sheet(path: str | Path) -> pd.DataFrame:
    return pd.read_excel(path, sheet_name="Wholesale", skiprows=4)

def process_wholesale_sheet(df: pd.DataFrame) -> DataFrame[WholesaleModel]:
    return WholesaleModel.validate(df)

def read_sales_retail(path: str | Path) -> DataFrame[RetailModel]:
    """Facade."""
    return process_retail_sheet(import_retail_sheet(path))

def read_sales_wholesale(path: str | Path) -> DataFrame[WholesaleModel]:
    """Facade."""
    return process_wholesale_sheet(import_wholesale_sheet(path))
```

### Step 5 — Expose via `__init__.py`

```python
# functions/readers/__init__.py
from .customers import read_customers
from .sales import read_sales_retail, read_sales_wholesale
__all__ = ["read_customers", "read_sales_retail", "read_sales_wholesale"]
```

## Schema Reuse

When two sources describe the same logical entity, import the owning domain's schema:

```python
# functions/readers/discrete_surveys.py
from <pkg_name>.schemas.continuous_monitoring import MeasurementModel
```

For a superset source, subclass:

```python
class MeasurementWithDepthModel(MeasurementModel):
    depth_m: float = pa.Field(ge=0.0, alias="Depth (m)")
```

## Anti-patterns

```python
# NEVER — mix schema constants and reader functions in one module
# enrichment/spatial.py
ENRICHMENT_COLUMNS = [...]          # schema constant — belongs in schemas/
def build_base_enrichment(...): ... # reader — belongs in functions/readers/
# Even when "all related to the same entity", keep the layers separate.
# A component/feature name (e.g. enrichment/) is not a substitute for the
# internal schemas/ + functions/readers/ + domain/ split.

# NEVER — circular import
# schemas/customers.py
from ghgmod.functions.readers.customers import import_customers

# NEVER — readers nested as entity subdirectories
# functions/customers/readers.py  ← belongs in functions/readers/customers.py

# NEVER — readers in domain/
# domain/customers/readers.py  ← belongs in functions/readers/customers.py

# NEVER — transformation inside the imperative shell
def import_customers(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()  # belongs in process_*
    return df

# NEVER — duplicate schema
# discrete_surveys/schema.py
class MeasurementModel(pa.DataFrameModel):  # already exists in continuous_monitoring
    ...

# NEVER — shadow stdlib
# functions/readers/os.py  ← name after the entity, e.g. scada_telemetry.py
```
