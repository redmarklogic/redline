---
name: python-script
description: Use when writing Python scripts in src/scripts/ -- thin orchestration, Spyder-style cell structure, or keeping reusable logic in the package
paths: "src/**/*.py,tests/**/*.py"
---

# Python Script Conventions

This skill defines how scripts under `src/scripts/` should be structured.

For related topics:

- General Python style: use the `python-style` skill.

## Boundary Contract

### Applies To
- Python scripts under `src/scripts/` using Spyder-style cell structure

### Produces
- Thin orchestration scripts with reusable logic kept in the package

### Does Not Cover
- Script naming and ordering (`python-script-numbering`)
- Function design (`python-function-design`)
- Module ordering (`python-module-structure`)

# %%
import pandas as pd
from <package>.<module> import read_raw, apply_qc  # replace <package> with the package name
from repo_ import DATA_DIR

OUTPUT_FILE = DATA_DIR / "processed" / "emissions.csv"

# %%
# Definitions
def _format_row_count(n: int) -> str:
    return f"{n:,} rows"

# %%
# Read and QC-filter the raw data
df = read_raw()
df = apply_qc(df)

# %%
# Print summary statistics
print(df.describe().to_string())

# %%
# Write output CSV
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)
print(f"Wrote {_format_row_count(len(df))} -> {OUTPUT_FILE}")

# %%
```


See `procedures/python-script.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Putting reusable logic directly in the script instead of the package | Move functions to src/rl/ and import them; scripts should be thin orchestration only |
| Using argparse in a script | Configure via env vars or module-level constants; never import argparse |
| Running a script without activating the virtual environment | Always activate .venv first: .\.venv\Scripts\activate then python -m scripts.<name> |