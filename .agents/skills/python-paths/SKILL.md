---
name: python-paths
description: Use when resolving file paths in Python -- choosing between pathlib, importlib.resources, or repo_ helper, or identifying banned path patterns
paths: "src/**/*.py,tests/**/*.py"
---

# Python Paths

This skill defines how to resolve file and directory paths across the codebase.

## Boundary Contract

### Applies To
- File and directory path resolution across all Python code

### Produces
- Consistent path handling using `pathlib`, `importlib.resources`, and `repo_` helper

### Does Not Cover
- Data versioning paths (`python-pins-data-version-control`)
- General style (`python-style`)
- Lint rules for `os.path` ban (`python-linting`)

# Access a specific file inside the package (generally do this in a central config module,
# e.g. in a function like get_sites_config() that returns the config dict, rather than
# duplicating this pattern across multiple scripts/modules)
config_path = Path(str(files("<package>.config").joinpath("sites.yaml")))

# Resolve the project root via the package location
# Again, generally this should never be done in scripts, use a `src/repo_.py` module to
# do it once for your whole project repo.
ROOT = Path(__file__).parent.parent  # src/repo_.py -> src/ -> project root
```

## Banned Patterns

# BAD -- fragile, breaks when file moves
DATA_ROOT = Path("../../../data")

# GOOD -- use repo_ helper
from repo_ import DATA_DIR
```

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

# BAD -- in src/<package>/config/__init__.py
CONFIG_YAML_PATH = Path(__file__).parent / "config.yaml"

# GOOD
from importlib.resources import files
from pathlib import Path

CONFIG_YAML_PATH = Path(str(files("<package>.config").joinpath("config.yaml")))
```

# BAD -- in tests/<package>/test_loader.py
ASSETS = Path(__file__).parent / "assets"

# GOOD -- use the conftest fixture
def test_something(assets_dir):
    path = assets_dir / "sample.csv"
```

# BAD
import os
full = os.path.join(base, "subdir", "file.csv")

# GOOD
from pathlib import Path
full = base / "subdir" / "file.csv"
```

# BAD -- in a function body
df = pd.read_csv("T:/project/data/readings.csv")

# OK -- in a docstring for data provenance
"""Source: T:/corporate/raw/readings_2024.xlsx"""
```


See `procedures/python-paths.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using os.path.join instead of pathlib | Use Path objects and / operator throughout; avoid os.path in new code |
| Hardcoding an absolute path like `C:\Users\<user>\project` <!-- hook: allow --> | Use `pathlib.Path(__file__).resolve().parents[N]` or the `repo_` helper for scripts |
| Using __file__ in a package resource access | Use importlib.resources.files(<package>) for files inside installed packages |