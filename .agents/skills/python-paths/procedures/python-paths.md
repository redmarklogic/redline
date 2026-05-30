# Python Paths — Detailed Reference

## Context & Guidelines

### Scope

Apply whenever code needs to reference a file path — whether reading data, loading
config, writing outputs, or resolving the project root.

### Always Use `pathlib.Path`

- Use `pathlib.Path` for all filesystem operations.
- Never use `os.path` functions (`os.path.join`, `os.path.dirname`, etc.).

### Data Location Decision Tree

Before writing a path, decide where the data belongs:

1. **Distributed with the package** (templates, config YAML, lookup tables baked into the
   installable package) -- use `importlib.resources` (see below).
2. **Git-tracked in `data/`** (small, nearly static reference files checked into the repo)
   -- use `repo_.DATA_DIR` / `repo_.PROCESSED_DATA_DIR`.
3. **Larger or evolving dataset** (pipeline outputs, analysis results, anything that
   changes between runs) -- use a `pins` board (use the `python-pins-data-version-control` skill).

### Package File Access (`importlib.resources`)

For files distributed inside the installed package, use `importlib.resources.files`.
This works consistently regardless of execution context (script, REPL, notebook,
`python -m`).

```python
from importlib.resources import files
from pathlib import Path

### Project Root Resolution by Context

| Context                                      | Pattern                                | Rationale                                                                            |
| -------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------ |
| Library code (`src/<package>/`)              | N/A                                    | Never access the project root from within a package. Packages must be self-contained |
| Scripts (`src/scripts/`)                     | `from repo_ import ROOT_DIR, DATA_DIR` | `src/repo_.py` is the single source for repo-root paths                              |
| Notebooks (`src/notebooks/`)                 | `from repo_ import ROOT_DIR, DATA_DIR` | Treated like scripts; import `repo_`                                                 |
| Tests (`tests/conftest.py` only)             | `Path(__file__).parent / "assets"`     | Acceptable as a pytest fixture definition                                            |
| Repo-specific config module (`src/repo_.py`) | `Path(__file__).parent.parent`         | The only place where `Path(__file__)` is acceptable outside of tests                 |

### Hardcoded Paths

- Hardcoded paths (string literals like `"data/processed/output.csv"`) are acceptable
  **only** in files under `src/**/scripts/` directories.
- **Never** hardcode paths in library packages (`src/<package>/` or any installable package).

### `Path(__file__)` — Restricted Use

`Path(__file__)` is acceptable in exactly two places:

1. `src/repo_.py` — the repo-root helper module consumed by scripts.
2. `tests/conftest.py` — for defining pytest fixtures that locate test assets.

Everywhere else, use `importlib.resources.files` or `repo_` imports instead.

### Multi-level relative paths

```python
### Attempting to access ROOT from within a package

```python
### `Path(__file__)` in library code

```python
### `Path(__file__)` in individual test files

```python
### `os.path` functions

```python
### Hardcoded drive letters in runtime code

```python
## Procedure

1. Determine which category the file belongs to (package resource, git-tracked data,
   or pins dataset).
2. Use the appropriate resolution pattern from the table above.
3. Never invent a new root-resolution mechanism; use `repo_` or `importlib.resources`.
4. If accessing parameterized or evolving data, set up a pins board (use the `python-pins-data-version-control` skill).
