---
name: python-module-structure
description: How to order functions within a Python module — the step-down rule, public-before-private ordering, helper extraction, and separating executable code from implementation.
---

# Python Module Structure

This skill governs the internal organisation of Python modules: how functions are
ordered, when to extract helpers, and what code may appear at module level.

For related topics:

- Function design (signatures, parameters, side effects): use the `python-function-design` skill.
- Script cell structure and Spyder conventions: use the `python-script` skill.
- Cognitive complexity reduction through helper extraction: use the `python-function-design` skill.

## Boundary Contract

### Applies To
- Function and definition ordering within any Python module under `src/` and `tests/`

### Produces
- Modules following the step-down rule with public-before-private ordering

### Does Not Cover
- Function design and signatures (`python-function-design`)
- Script cell structure (`python-script`)
- General style (`python-style`)

## Context & Guidelines

### Scope

Apply these rules whenever you add, reorder, or refactor functions in **any Python
module** — both package modules (`src/ghgmod/**`) and scripts (`src/scripts/**`).

---

### The Step-Down Rule

Organise functions so the file reads **top-to-bottom like a newspaper article**:
high-level concepts first, implementation details lower down.

- **Public functions appear before the private functions they use.**
- **Callers appear above callees** — a function body may call names defined later in
  the same file; Python resolves function names at call time, not definition time.
- **Private helpers (`_prefixed`) sit below the first public function that calls
  them**, ordered from higher to lower level of abstraction.

**Why:** A reader scanning from the top should understand _what_ the module does
before encountering _how_. Private helpers are details that can be skipped on a
first read.

**Caveat:** Module-level constants and class definitions that are referenced at
import time (e.g., as default argument values or class-level attributes) must be
defined before their first use. Function ordering is not constrained in this way.

#### Violation Checklist

A step-down violation exists when:

- A `_private` helper is defined **above** the public function that calls it.
- A low-level utility appears near the **top** of the module, above the callers
  that give it context.
- A reader must scroll past implementation details to find the entry-point functions.

#### Fixing a Violation

1. Identify the highest-level functions (public, or decorated with `@validate_call` /
   `@pa.check_types`).
2. Move them to the **top** of the function block.
3. Move functions they call immediately below, preserving rough call-order.
4. Push all `_private` helpers to the **bottom** of the function block.
5. Run tests and linters to verify nothing broke.

**Critical:** when extracting a new helper during a refactor, the instinct is to
insert it just **above** the call site. Always resist this — insert it just **below**
the calling function's closing line.

---

### Public Before Private

After module-level constants and imports, functions follow this order:

1. Public functions (no leading underscore) — ordered from highest to lowest
   abstraction level.
2. Private functions (`_prefixed`) — ordered from highest to lowest abstraction
   level, each following the public function it primarily supports.

This mirrors the Stepdown Rule at the visibility level: readers see the contract
(public API) before the implementation (private helpers).

---

### Extract Bodies of Conditionals and Loops

When a conditional branch or loop body grows complex, extract it into a named
helper. This keeps high-level functions readable and pushes detail downward —
consistent with the step-down rule.

**Signals that extraction is warranted:**

- A loop body contains multiple branches that perform the same conceptual operation
  on different inputs (duplicate structural branches).
- A branch body is longer than ~5 lines and has a name that can be stated clearly.
- Cognitive complexity (SonarQube) of the containing function exceeds 15.

For the full cognitive-complexity pattern (before/after code blocks), see the
`python-function-design` skill.

---

### Separation of Implementation and Execution

Executable module-level code (code that runs on import) must not appear in package
modules. Package modules define behaviour; scripts and notebooks trigger it.

**Acceptable** (package module — definitions only):

```python
# src/ghgmod/functions/loaders.py
def load_daily_pond_readings(path: Path) -> pd.DataFrame:
    ...
```

**Not acceptable** (execution in a package module):

```python
# src/ghgmod/functions/loaders.py  ← WRONG
df = load_daily_pond_readings(Path("data/..."))  # runs on import
print(df.head())
```

**Acceptable** (execution lives in a script):

```python
# src/scripts/build_pond_dataset.py
from ghgmod.functions.loaders import load_daily_pond_readings

df = load_daily_pond_readings(DATA_DIR / "wastewater_process/daily_pond_readings/...")
```

---

## Procedure

When adding or refactoring functions in any module:

1. **New function:** place it at the highest abstraction level it belongs to. If it
   is public, it goes above any private helpers it uses.
2. **New helper extracted from an existing function:** place it immediately **below**
   the function it was extracted from, not above it.
3. **Reordering after a refactor:** apply the violation checklist; move functions to
   satisfy caller-above-callee ordering.
4. Run `uv run pre-commit run -a` to confirm no regressions.

---

## Examples

### Good: Public Callers Above Private Helpers

```python
# Public function to add a task
def add_task(task: str) -> None:
    if _validate_task(task):
        tasks.append(task)
        _log_action(f"Task added: {task}")
    else:
        print("Task validation failed.")


# Public function to complete a task
def complete_task(task: str) -> None:
    if task in tasks:
        tasks.remove(task)
        completed_tasks.append(task)
        _log_action(f"Task completed: {task}")
    else:
        print("Task not found.")


# Private helper: validate a task (follows the public functions it supports)
def _validate_task(task: str) -> bool:
    return isinstance(task, str) and bool(task.strip())


# Private helper: log an action
def _log_action(action: str) -> None:
    print(f"Action: {action}")
```

### Bad: Private Helpers Above Their Callers

```python
# Private function to validate a task  ← helper defined before its caller
def _validate_task(task):
    return isinstance(task, str) and bool(task.strip())


# Private function to log actions      ← helper defined before its caller
def _log_action(action):
    print(f"Action: {action}")


# Public function to add a task        ← caller buried below its helpers
def add_task(task):
    if _validate_task(task):
        tasks.append(task)
        _log_action(f"Task added: {task}")
```

### Good: Helper Inserted Below Its Caller After Extraction

```python
def _parse_daily_pond_sheet(ws: object) -> list[dict[str, object]]:
    """Caller — higher-level function."""
    for row_vals in ws.iter_rows(values_only=True):
        detected = _detect_temp_col(row_vals)   # calls helper defined below
        ...
    return records


def _detect_temp_col(row_vals: tuple) -> int | None:
    """Helper — placed BELOW its caller, not above."""
    if _cell(row_vals, 8) == "Temp":
        return 8
    if _cell(row_vals, 7) == "Temp":
        return 7
    return None
```
