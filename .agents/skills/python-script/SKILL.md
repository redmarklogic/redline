---
name: python-script
description: Conventions for Python scripts in src/scripts/ -- thin orchestration, Spyder-style cell structure, and keeping reusable logic in the package
---

# Python Script Conventions

This skill defines how scripts under `src/scripts/` should be structured.

For related topics:

- Script naming and execution order: use the `python-script-numbering` skill.
- Function design (decomposition, signatures): use the `python-function-design` skill.
- General Python style: use the `python-style` skill.
- Function ordering within any module (step-down rule, public-before-private): use the `python-module-structure` skill.

## Boundary Contract

### Applies To
- Python scripts under `src/scripts/` using Spyder-style cell structure

### Produces
- Thin orchestration scripts with reusable logic kept in the package

### Does Not Cover
- Script naming and ordering (`python-script-numbering`)
- Function design (`python-function-design`)
- Module ordering (`python-module-structure`)

## Context & Guidelines

### Scope

Apply whenever you add, review, or refactor a Python script under `src/scripts/`.

### Scripts Are Thin Orchestrators

A script's job is to **wire together** package-level functions, not to contain
domain logic.

- **Reusable code belongs in the package** (`src/<package>/`, where `<package>` is
  the installable package name declared in `pyproject.toml`). If a function could be
  called from two scripts, a notebook, or a test, it must not live in `src/scripts/`.
- **Scripts should import and call**, not implement. The body of a script is
  typically: read config, call package functions, write output, print summary.
- **Tests follow the code**: when logic moves into the package, unit tests are
  written in `tests/` for that package module. Scripts themselves are not unit
  tested -- the package functions they call are.

### What May Stay in a Script

Not everything needs to move to the package. These are acceptable in a script:

- **Glue code**: wiring inputs to outputs, calling package functions in sequence.
- **Output formatting**: `print_summary`, progress messages, CSV writes.
- **Script-specific constants**: file paths, output directories, CLI-like
  configuration that only this script uses.
- **Thin wrappers**: a one-liner that adapts a package function's signature for
  the script's specific context (e.g., hardcoding a config value).

### The Stepdown Rule

Organise functions within a script so that the file reads **top-to-bottom like a
newspaper article**: high-level orchestration first, supporting details later.

1. **Module docstring** at the very top.
2. **`# %%` (no comment)**: imports and module-level constants/configuration (paths,
   dataclass configs, column-name mappings).
3. **`# %%` / `# Definitions`**: classes and all helper functions in stepdown order
   (public/high-level first, private helpers last).
4. **`# %%` / `# <description>`**: one cell per logical execution step
   (build data, QC checks, write output, etc.).
5. **Trailing `# %%`** with a blank line — always the last line of the file.

**Why**: A new reader should be able to stop reading after the Definitions cell and
already understand the script's purpose from the function names alone. Details they
can skip are at the bottom of the Definitions cell.

**Caveat**: Python requires names to be defined before module-level _use_ (e.g., a
constant that calls a function, or a default argument value). Function definitions do
not have this constraint — a function body can reference names defined later because
Python resolves them at call time, not definition time. So function ordering within
the Definitions cell is free to follow the stepdown rule.

### Detecting Stepdown Violations

A violation exists when:

- A private helper (`_foo`) is defined **above** the public function that calls it.
- The script's main public functions appear near the **bottom** of the Definitions
  cell, buried under implementation details.
- A reader must scroll past helper functions to discover what the script actually does.

### Fixing Stepdown Violations

1. Identify the highest-level functions (the ones called directly from the execution
   cells, or decorated with `@check_types`).
2. Move them to the **top** of the Definitions cell.
3. Move the functions they call below them, in rough call-order.
4. Push private helpers (`_prefixed`) to the **bottom** of the Definitions cell.
5. Run tests and linters to verify nothing broke.

### Spyder-Style Cell Conventions

- **Never use `if __name__ == "__main__":`** unless the script uses multiprocessing
  or another special circumstance. Scripts are executed directly; the guard adds noise.
- The description comment for a cell goes on the **next line after `# %%`**, never on
  the same line. VS Code's Interactive Terminal hides the `# %%` line and shows the
  following line as the cell preview — the comment is what the developer sees.
- The **first cell** (imports + constants) has `# %%` with **no comment** on the next
  line.
- **Never use decorative `print("=== Section ===")` calls** to mark sections. The <!-- hook: allow -->
  `# %%` cell comment is the section label. Plain `print()` calls are for data output
  only.
- **Don't over-functionalize bespoke orchestration**. If logic is called only once,
  is highly script-specific, and would not be unit-tested, it belongs in a `# %%` cell,
  not wrapped in a named function. Named functions belong in the package when they are
  mature enough to be reused and tested.
- **Output-only functions are always candidates for inlining.** If a function body
  consists entirely of `print()` calls (i.e. it only formats and displays data), it adds
  no reuse value. The `# %%` cell comment is a strictly better label — remove the
  function and inline the prints as a cell.
- **When removing a function, audit its imports.** Type annotations in function
  signatures can be the sole consumer of an import. After deleting a function, check
  whether any of its parameter or return type imports are now unused and remove them.

## Procedure

When creating or reviewing a script:

1. Check that domain logic lives in the package, not the script.
2. Verify the stepdown rule: high-level functions first, helpers last.
3. Ensure the script is documented in `src/scripts/README.md` per the `python-script-numbering` skill.
4. Run `uv run prek run scripts-in-readme` to verify registration.

## Examples

### Good: Cell-Based Structure

```python
"""Build tidy emissions dataset from raw CSVs."""

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

### Bad: `if __name__` Guard and Decorative Print Headers

```python
"""Build tidy emissions dataset from raw CSVs."""

import pandas as pd

OUTPUT_FILE = "emissions.csv"


def ingest_all() -> pd.DataFrame:
    raw = pd.read_csv("raw.csv")
    return raw.dropna()


def print_summary(df: pd.DataFrame) -> None:
    print("\n=== Summary ===")   # bad: decorative section header
    print(df.describe())


if __name__ == "__main__":     # bad: unnecessary guard
    df = ingest_all()
    print_summary(df)
```
