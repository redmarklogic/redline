# Import-Linter Reference

Authoritative source: `pyproject.toml` under `[tool.importlinter]`.
Pre-commit enforcement: `uv run --frozen --offline lint-imports` (always_run, priority 3).

## Purpose

Import-linter enforces **architectural dependency direction** at the module level.
It builds a full import graph (via Grimp) and checks every import — including indirect,
transitive chains — against declared contracts. A violation in `lint-imports` means the
layered architecture has been broken.

This is the **executable documentation** of the project's layered architecture. If the
contracts pass, the dependency direction is proven correct — not just hoped for.

## Contract Types

### Layers (primary — used in this repo)

Enforces a top-to-bottom dependency flow: higher layers may import lower ones, never
the reverse. Indirect imports (A -> B -> C) are also checked.

```toml
[[tool.importlinter.contracts]]
name = "<package> layers"
type = "layers"
layers = ["functions", "schemas", "domain"]
containers = ["<package>"]
exhaustive = true
```

The generic baseline layers are `domain` (lowest), `schemas`, and `functions` (highest).
Add project-specific higher layers above `functions` when the project warrants them
(e.g., `scripts`, `cli`, `api`). Do not add layers speculatively.

**Key options:**

| Option               | Purpose                                                                 |
| -------------------- | ----------------------------------------------------------------------- |
| `layers`             | Ordered list, highest first. `functions` may import `schemas`, etc.     |
| `containers`         | The parent package(s). Layers are resolved relative to each container.  |
| `exhaustive`         | Every sibling subpackage must appear in `layers`. New packages FAIL.    |
| `exhaustive_ignores` | Exempt specific siblings from `exhaustive` (e.g. `utils`, `_internal`). |

**Optional layers** — wrap in parentheses: `"(medium)"`. Missing optional layers don't
trigger exhaustive failures.

**Multi-item layers** — siblings that are independent of each other within the same
tier. Separated by pipes:

```toml
layers = ["high", "blue | green | yellow", "low"]
```

This means `blue`, `green`, and `yellow` are peers that **cannot import each other**
but can all import from `low`.

**Non-independent siblings** — separated by colons if they *should* be allowed to
import each other:

```toml
layers = ["high", "blue : green : yellow", "low"]
```

### Nested / per-subpackage contracts

Each subpackage can have its own contract. This repo already does this:

```toml
[[tool.importlinter.contracts]]
name = "rl.functions layers"
type = "layers"
layers = ["readers"]
containers = ["rl.functions"]
exhaustive = true
```

**When to add a nested contract:** Any time a subpackage grows its own internal
hierarchy (e.g. `rl.functions.readers` has multiple reader subpackages that should
not import each other), add a new `[[tool.importlinter.contracts]]` block.

### Forbidden

Prevents specific modules from importing specific other modules. Useful for hard
boundaries (e.g. domain must never import from infrastructure).

```toml
[[tool.importlinter.contracts]]
name = "domain isolation"
type = "forbidden"
source_modules = ["rl.domain"]
forbidden_modules = ["rl.functions", "rl.schemas"]
```

### Independence

Ensures listed modules have zero imports between them (useful for bounded contexts
that must stay decoupled).

```toml
[[tool.importlinter.contracts]]
name = "reader independence"
type = "independence"
modules = [
    "rl.functions.readers.foundation",
]
```

### Protected

Restricts who can import a module. The inverse of Forbidden — instead of "X cannot
import Y", it says "only A and B may import Y."

```toml
[[tool.importlinter.contracts]]
name = "domain only via functions"
type = "protected"
protected_modules = ["rl.domain"]
allowed_importers = ["rl.functions", "rl.schemas"]
```

### Acyclic Siblings

Ensures sibling subpackages under a common ancestor have no circular dependencies.

```toml
[[tool.importlinter.contracts]]
name = "no cycles in rl"
type = "acyclic_siblings"
ancestors = ["rl"]
```

## Configuration Options

| Option                           | Scope      | Purpose                                                            |
| -------------------------------- | ---------- | ------------------------------------------------------------------ |
| `root_packages`                  | Top-level  | Which packages to scan. Currently `["rl"]`.                        |
| `include_external_packages`      | Top-level  | Include third-party packages in the graph (needed for `forbidden`).     |
| `exclude_type_checking_imports`  | Top-level  | Exclude `if TYPE_CHECKING:` imports from the graph.                |
| `ignore_imports`                 | Per-contract | Whitelist specific import paths (escape hatch).                  |

## When to Update Contracts

Update `pyproject.toml` import-linter contracts when:

1. **Adding a new subpackage** under an `exhaustive = true` container — it must be
   placed in the `layers` list or added to `exhaustive_ignores`.
2. **Adding a new bounded context** (e.g. a second reader domain like `foundation`) —
   add an `independence` contract if the contexts must stay decoupled.
3. **Splitting a layer** into sub-layers — add a nested contract for the sub-hierarchy.
4. **Introducing a shared utility package** (e.g. `rl._internal`) — add it to
   `exhaustive_ignores` if it is cross-cutting, or place it as the lowest layer.
5. **Creating a new top-level package** (e.g. `src/base/`) — add it to `root_packages`
   and create its own contracts.

## Common Failure Scenarios

| Symptom                                       | Cause                                               | Fix                                                       |
| --------------------------------------------- | --------------------------------------------------- | --------------------------------------------------------- |
| `Module rl.X is not in any layer`              | New subpackage not listed in exhaustive contract     | Add to `layers` or `exhaustive_ignores`                   |
| `rl.domain imports rl.functions`               | Domain layer importing a higher layer                | Move shared code down or restructure the dependency       |
| `Could not find package rl`                    | Package not importable from working directory        | Run from repo root; ensure `uv sync` has been run         |
| Contract passes but architecture still wrong   | Missing contract for a sub-hierarchy                 | Add a nested contract for the subpackage                  |

## Integration with Spec-Kit Planning

During the `plan` phase, the plan template includes a **Domain Impact** section.
When a feature introduces a new package or layer:

1. State which import-linter contract is affected.
2. Show the proposed `layers` list change.
3. If a new contract type is needed (independence, forbidden), declare it.

This catches architectural drift at design-time, not at pre-commit-time.

## Running Locally

```powershell
# Full check (same as pre-commit)
uv run lint-imports

# Verbose output (shows import chains)
uv run lint-imports --verbose
```
