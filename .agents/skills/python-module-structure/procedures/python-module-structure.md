# Python Module Structure — Detailed Reference

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
## Procedure

When adding or refactoring functions in any module:

1. **New function:** place it at the highest abstraction level it belongs to. If it
   is public, it goes above any private helpers it uses.
2. **New helper extracted from an existing function:** place it immediately **below**
   the function it was extracted from, not above it.
3. **Reordering after a refactor:** apply the violation checklist; move functions to
   satisfy caller-above-callee ordering.
4. Run `uv run prek run -a` to confirm no regressions.

---

## Examples

### Good: Public Callers Above Private Helpers

```python
### Bad: Private Helpers Above Their Callers

```python
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
