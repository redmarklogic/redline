# Python Patterns — Detailed Reference

## Context & Guidelines

### Scope

Apply when:

- Writing or refactoring Python under `src/` or `tests/`
- Reviewing code for readability / maintainability
- Choosing between competing Python idioms (EAFP vs LBYL, comprehension vs loop, etc.)

### Non-goals (avoid conflicts)

This skill does **not** define:

- Type hint standards (use the typing skill)
- Exception policy / logging strategy (use the error-handling skill)
- Formatting/lint configuration or suppressions (use the linting skill)
- Domain modeling rules (use the domain-modeling skill)

If guidance here appears to contradict another skill, the more specific skill wins.

## Procedure

1. Start with the simplest readable code that matches intent.
2. Pick the idiom that reduces branching and nesting _without_ becoming clever.
3. Keep patterns small and local; avoid introducing “frameworky” helpers unless repeated.
4. Re-check against the relevant canonical skill (typing, error handling, domain modeling, linting).

### EAFP vs LBYL (choose deliberately)

Prefer EAFP when the exceptional case is truly exceptional and the operation is atomic.
Prefer LBYL when you need to avoid side effects or when exceptions are expected in normal flow.

Good (EAFP for mapping lookup):

```python
from collections.abc import Mapping


def get_required_value(mapping: Mapping[str, str], key: str) -> str:
    try:
        return mapping[key]
    except KeyError as exc:
        message = f"Missing required key: {key}"
        raise KeyError(message) from exc
```

Good (LBYL when you need custom branching and it’s expected):

```python
from collections.abc import Sequence


def first_or_none(items: Sequence[str]) -> str | None:
    if not items:
        return None
    return items[0]
```

### `try/except/else` for “happy-path” clarity

Use `else` when the return depends on the `try` succeeding.

```python

def parse_positive_int(text: str) -> int:
    try:
        value = int(text)
    except ValueError as exc:
        message = f"Not an integer: {text}"
        raise ValueError(message) from exc
    else:
        if value <= 0:
            message = "Expected a positive integer"
            raise ValueError(message)
        return value
```

### Comprehension vs loop (readability threshold)

- Use comprehensions for **simple** filter/map.
- Use a loop when conditions or transformations become multi-step.

Good (simple):

```python
active_names = [user.name for user in users if user.is_active]
```

Good (multi-step logic stays explicit):

```python
names: list[str] = []
for user in users:
    if not user.is_active:
        continue
    names.append(user.name.strip())
```

### Prefer generators for streaming / large inputs

```python

def total_size(paths: list[str]) -> int:
    return sum(len(path) for path in paths)
```

### Context managers for resource lifetime

Use `with` for anything that must be closed/released.

```python

def read_text(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()
```

### No CLI Output in Library Code

Library code under `src/<package>/` must not call `print()` or CLI formatting tools (like `ruru.cli.bullets`).

**Rule:**

- Library functions **return data**; they do not display it.
- Scripts under `src/scripts/` handle all user-facing output (printing, CLI formatting, progress bars).
- Exception: Proper logging via `logging` module is acceptable in library code.
- This rule targets **presentation** side effects (stdout, CLI formatting), not all
  side effects. Library code that writes to files or databases (e.g., a Repository)
  is fine -- it is the *intended* purpose of those classes.

Good (library returns data):

```python
### Data containers: dataclasses vs domain objects

- For small internal data containers, prefer dataclasses (see class design skill).
- For _domain_ value objects and validated data, use the `python-domain-modeling` skill
  (Pandera/Pydantic over `@dataclass` for domain types).

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetryBudget:
    attempts: int
    backoff_seconds: float
```

### Decorators (use sparingly, keep transparent)

- Always preserve function metadata with `functools.wraps`.
- Avoid decorators that hide I/O, global state, or error swallowing.

```python
import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar


P = ParamSpec("P")
R = TypeVar("R")


def traced(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    return wrapper
```

### Pragmatic concurrency choices

- I/O-bound work:
  - Prefer `asyncio` if you are already in async code.
  - Otherwise, prefer `ThreadPoolExecutor` for a small number of blocking calls.
- CPU-bound work:
  - Prefer `ProcessPoolExecutor` for expensive pure computations.

Keep concurrency at the boundary; keep the core logic pure and testable.

### Strategy pattern (function-based)

When a function contains branching logic (`if/elif`) to select different algorithms,
consider the Strategy pattern. In Python, you rarely need a class hierarchy for this --
pass a callable (a first-class function) as a parameter instead.

Bad (branching on a flag):

```python
def calculate_pressure(method: str, depth: float) -> float:
    if method == "rankine":
        return _rankine(depth)
    elif method == "coulomb":
        return _coulomb(depth)
    ...
```

Good (strategy as a callable):

```python
from collections.abc import Callable

PressureStrategy = Callable[[float], float]

def calculate_pressure(strategy: PressureStrategy, depth: float) -> float:
    return strategy(depth)

### Functional core, imperative shell

Separate your code into two layers:

- **Functional core**: pure functions that contain business logic and decision-making.
  They depend only on the data passed in and produce no side effects. This core is
  fast to test without mocks or I/O setup.
- **Imperative shell**: thin orchestration that gathers inputs from the outside world
  (files, databases, APIs), feeds them into the functional core, and applies the
  resulting outputs (writes, network calls).

This is the Python translation of the Onion / Hexagonal architecture. The critical
rule is **dependency direction**: the shell depends on the core, but the core knows
nothing about the shell.

```python
### Repository pattern (protocol-based)

When domain logic needs to read or write persistent data, abstract the data access
behind a `Protocol` interface. The domain code calls `repository.get()` or
`repository.add()` without knowing whether the backing store is a database, a file,
or an in-memory dict.

This pattern makes domain logic trivially testable -- swap the real repository for
a fake in-memory one in tests.

```python
from typing import Protocol


class BoreholeRepository(Protocol):
    def get(self, borehole_id: str) -> Borehole: ...
    def add(self, borehole: Borehole) -> None: ...


class InMemoryBoreholeRepository:
    """Fake for tests."""
    def __init__(self) -> None:
        self._store: dict[str, Borehole] = {}

    def get(self, borehole_id: str) -> Borehole:
        return self._store[borehole_id]

    def add(self, borehole: Borehole) -> None:
        self._store[borehole.id] = borehole
```

### Matplotlib: use mathtext for chemical/subscript notation

DejaVu Sans (matplotlib's default font) lacks Unicode subscript characters such as
₂ (U+2082) and ₄ (U+2084). Using them in axis labels, titles, or annotations
produces empty boxes in rendered output.

**Rule:** always use matplotlib's mathtext syntax for chemical formulae and subscript
notation in chart strings. Keep Unicode versions only for non-matplotlib output
(print, tables, Quarto prose).

```python
## Anti-patterns to avoid (quick reminders)

- Mutable default arguments
- Hidden side effects in imports
- Bare `except:` or swallowing exceptions
- Overly clever one-liners that obscure intent
- **Connascence of meaning**: relying on magic values (`1` for True, `"A"` for active)
  instead of named constants or enums
- **Connascence of position**: fragile tuple unpacking or positional-only arguments
  where keyword arguments would be clearer

(For the repo-specific rules and lint constraints, use the `python-style` and `python-linting` skills.)
