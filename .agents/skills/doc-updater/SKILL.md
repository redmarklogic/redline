---
name: doc-updater
description: Documentation and codemap specialist. Keeps codemaps and docs in sync with the Python codebase by scanning packages, FastAPI/MCP routes, and scripts; updates docs/CODEMAPS/*, README.md, and guides with verified paths and runnable commands.
---

# Documentation & Codemap Specialist

This skill is for updating documentation so it matches the current state of the codebase.

The priority is accuracy over prose: docs that mention files, endpoints, or commands must be verifiably correct.

## Context & Guidelines

- **Scope**: Apply when code changes impact architecture, public APIs, FastAPI routes, MCP tools, scripts, configuration, or directory structure.
- **Constraints**:
  - Prefer Python standard library for analysis (for example: `ast`, `pathlib`, `re`, `tomllib`).
  - Avoid adding new dependencies for doc generation unless clearly necessary; if needed, confirm APIs with Context7 before using.
  - Do not reference or import from `archive/`; it is reference-only.
  - Commands must respect repo conventions: PowerShell separators (`;`) and venv activation (`.\.venv\Scripts\activate; python -m ...`).
- **File Placement**:
  - Codemaps: `docs/CODEMAPS/` (create if missing).
  - Project overview/setup: `README.md`.
  - Deep dives: `docs/` (for this repo, ADRs live under `docs/adr/`).

## Procedure

1. **Identify what changed**
   - Scan the diff (or changed files) and classify changes:
     - New/removed modules/packages
     - Route changes (REST or MCP)
     - Config changes (YAML/TOML)
     - Script/task changes

2. **Map repository structure from source of truth**
   - Treat `src/` as the primary boundary for runtime code.
   - Record top-level packages (directories under `src/` that contain `__init__.py`).
   - Identify entry points and integration seams:
     - FastAPI app entry module(s)
     - REST router packages (commonly `.../api/.../routers`)
     - MCP server modules (commonly `.../mcp/...`)
     - Configuration directories (YAML/TOML)

3. **Generate/update codemaps**
   - Create or update `docs/CODEMAPS/INDEX.md` plus per-area maps.
   - Suggested codemap set for this repo’s layered architecture:
     - `docs/CODEMAPS/faultless.md`
     - `docs/CODEMAPS/marker.md`

     - `docs/CODEMAPS/base.md`

   - Each codemap should include:
     - **Last Updated** date
     - **Entry Points** (verified file paths)
     - **Key Modules** table (purpose, main exports, dependencies)
     - **Data Flow** narrative
     - **External Dependencies** (only if relevant and verified)

4. **Update README and guides**
   - Keep setup instructions runnable:
     - `uv sync`
     - venv activation and module execution with `python -m`
   - Ensure endpoints/tools tables match actual code (route paths, HTTP methods, tool names).
   - Cross-link codemaps from README (and vice versa).

5. **Validate documentation against the codebase**
   - Verify every mentioned path exists.
   - Validate internal Markdown links.
   - Sanity-check commands:
     - Prefer commands that don’t rely on unstated global state.
     - Avoid references to scripts that do not exist.

## Examples

### Good Example: build a package/module inventory (stdlib-only)

Use this to produce a quick, verifiable module list for codemaps.

```python
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PackageInfo:
    name: str
    path: Path


def discover_packages(src_dir: Path) -> list[PackageInfo]:
    packages: list[PackageInfo] = []
    for child in src_dir.iterdir():
        if not child.is_dir():
            continue
        if (child / "__init__.py").exists():
            packages.append(PackageInfo(name=child.name, path=child))
    return sorted(packages, key=lambda p: p.name)


src = Path("src")
for pkg in discover_packages(src):
    print(f"{pkg.name}: {pkg.path.as_posix()}")
```

### Good Example: find FastAPI router decorators via AST

This helps keep endpoint tables accurate without manual guessing.

```python
import ast
from collections.abc import Iterable
from pathlib import Path


HTTP_DECORATORS = {"get", "post", "put", "patch", "delete"}


def _format_expr(expr: ast.expr) -> str:
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        return f"{_format_expr(expr.value)}.{expr.attr}"
    return expr.__class__.__name__


def iter_python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        if "archive" in path.parts:
            continue
        yield path


def discover_router_decorators(py_file: Path) -> list[tuple[str, int]]:
    tree = ast.parse(py_file.read_text(encoding="utf-8"))
    found: list[tuple[str, int]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        for deco in node.decorator_list:
            if not isinstance(deco, ast.Call):
                continue
            if not isinstance(deco.func, ast.Attribute):
                continue
            if deco.func.attr in HTTP_DECORATORS:
                found.append((f"{_format_expr(deco.func.value)}.{deco.func.attr}", node.lineno))

    return found


for file in iter_python_files(Path("src")):
    decos = discover_router_decorators(file)
    if decos:
        print(file.as_posix())
        for name, lineno in decos:
            print(f"  - {name} at line {lineno}")
```

### Bad Example: unverified tooling and JS-first workflows

Avoid references like `npx`, `ts-morph`, or custom `/update-docs` commands unless the repo actually contains those scripts and they are part of the supported workflow.
