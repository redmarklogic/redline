---
name: python-paths
description: Conventions for resolving file paths in Python code — pathlib preference, importlib.resources for package files, repo_ helper for scripts, and banned patterns.
---

# Python Paths

This skill defines how to resolve file and directory paths across the codebase.

For related topics:

- Data versioning with pins: use the `python-pins-data-version-control` skill.
- General Python style: use the `python-style` skill.
- Lint rules (including `os.path` ban): use the `python-linting` skill.

## Boundary Contract

### Applies To
- File and directory path resolution across all Python code

### Produces
- Consistent path handling using `pathlib`, `importlib.resources`, and `repo_` helper

### Does Not Cover
- Data versioning paths (`python-pins-data-version-control`)
- General style (`python-style`)
- Lint rules for `os.path` ban (`python-linting`)

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

# Access a specific file inside the package (generally do this in a central config module,
# e.g. in a function like get_sites_config() that returns the config dict, rather than
# duplicating this pattern across multiple scripts/modules)
config_path = Path(str(files("<package>.config").joinpath("sites.yaml")))

# Resolve the project root via the package location
# Again, generally this should never be done in scripts, use a `src/repo_.py` module to
# do it once for your whole project repo.
ROOT = Path(__file__).parent.parent  # src/repo_.py -> src/ -> project root
```

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

## Banned Patterns

### Multi-level relative paths

```python
# BAD -- fragile, breaks when file moves
DATA_ROOT = Path("../../../data")

# GOOD -- use repo_ helper
from repo_ import DATA_DIR
```

### Attempting to access ROOT from within a package

```python
# BAD -- in src/<package>/functions/loader.py
ROOT = Path(__file__).resolve().parents[3]

# BAD -- in src/<package>/functions/loader.py
from importlib.resources import files
from pathlib import Path

ROOT = Path(str(files("<package>"))).parent.parent

# GOOD -- in src/repo_.py
# Not to be imported from within the package, only from scripts and notebooks
ROOT = Path(__file__).parent.parent
```

### `Path(__file__)` in library code

```python
# BAD -- in src/<package>/config/__init__.py
CONFIG_YAML_PATH = Path(__file__).parent / "config.yaml"

# GOOD
from importlib.resources import files
from pathlib import Path

CONFIG_YAML_PATH = Path(str(files("<package>.config").joinpath("config.yaml")))
```

### `Path(__file__)` in individual test files

```python
# BAD -- in tests/<package>/test_loader.py
ASSETS = Path(__file__).parent / "assets"

# GOOD -- use the conftest fixture
def test_something(assets_dir):
    path = assets_dir / "sample.csv"
```

### `os.path` functions

```python
# BAD
import os
full = os.path.join(base, "subdir", "file.csv")

# GOOD
from pathlib import Path
full = base / "subdir" / "file.csv"
```

### Hardcoded drive letters in runtime code

```python
# BAD -- in a function body
df = pd.read_csv("T:/project/data/readings.csv")

# OK -- in a docstring for data provenance
"""Source: T:/corporate/raw/readings_2024.xlsx"""
```

## Procedure

1. Determine which category the file belongs to (package resource, git-tracked data,
   or pins dataset).
2. Use the appropriate resolution pattern from the table above.
3. Never invent a new root-resolution mechanism; use `repo_` or `importlib.resources`.
4. If accessing parameterized or evolving data, set up a pins board (use the `python-pins-data-version-control` skill).
