---
name: python-class-design
description: Standards for designing maintainable Python classes (responsibilities, init, composition).
---

# Python Class Design

This skill defines how to design Python classes in this repo.

## Boundary Contract

### Applies To
- Python class definitions under `src/` and `tests/`

### Produces
- Classes with clear responsibilities, minimal init logic, and composition over inheritance

### Does Not Cover
- Function-level design (`python-function-design`)
- Domain value objects and Pydantic/Pandera models (`python-domain-modeling`)
- Type annotations (`python-typing`)

## Context & Guidelines

### Scope

Apply whenever you add or refactor classes under `src/`.

### Core Rules

- Keep classes focused on a single responsibility.
- Keep `__init__` simple; avoid complex logic in constructors.
- Prefer composition over inheritance.
- Use dataclasses for simple data containers.
- Use `@property` for computed attributes.

### Deep Modules over Shallow Modules

A class consists of an **interface** (what it promises) and an **implementation** (how it
delivers). A **deep module** provides powerful functionality behind a simple interface.
A **shallow module** exposes a complex interface for very little functionality.

- Aim for deep classes: hide complexity, expose minimal surface area.
- Avoid the "classitis" anti-pattern where excessive decomposition into tiny classes
  creates a large number of shallow modules. Each small class introduces its own
  interface; the accumulated interfaces create more total complexity than the
  monolithic code they replaced.
- If splitting a class does not meaningfully simplify the caller's experience, do not
  split it.

**Resolving the SRP vs Deep Modules tension**: the Single Responsibility rule ("keep
classes focused on a single responsibility") can push toward splitting, while the Deep
Modules heuristic pushes against unnecessary splitting. The tiebreaker is **information
hiding**: if the two responsibilities share the same internal knowledge (data format,
algorithm, invariant), keep them together -- splitting would leak that knowledge across
two interfaces. If they depend on genuinely independent knowledge, split them.

### Information Hiding and Leakage

Embed design decisions (data formats, algorithms, internal structures) inside a class's
implementation so they are invisible to the rest of the system.

**Information leakage** occurs when the same piece of knowledge (e.g., a file format,
a column name, a parsing rule) is reflected in multiple classes. This creates a hidden
dependency: changing that knowledge requires modifying all affected classes.

Common cause: **temporal decomposition** -- structuring classes by the chronological
order of operations (`ReadFile`, `ParseFile`, `WriteFile`) rather than by the knowledge
they encapsulate. If two classes share knowledge about the same file format, merge them
or extract the shared knowledge into its own class.

### Tell, Don't Ask

Applies to **objects with behavior** (services, domain entities, controllers) -- not
to plain data containers (dataclasses, Pydantic models, named tuples) whose purpose
is to carry and expose data.

For behavioral objects: do not query an object for its internal state, make a decision
based on that state, and then tell the object what to do. Instead, tell the object what
to accomplish and let it make the decision internally.

Bad:

```python
if report.status == "draft":
    report.status = "submitted"
    report.submitted_at = datetime.now()
```

Good:

```python
report.submit()  # encapsulates the status transition
```

### Law of Demeter

A method should only call methods on:

1. Its own object (`self`).
2. Objects passed as parameters.
3. Objects it creates.
4. Direct component objects it holds.

Do not reach through an object to access its internals:

Bad: `self.engine.session.query(User).filter(...)`

Good: `self.user_repository.find_active_users()`

Violating this rule tightly couples your code to the internal structure of another
object, making both fragile to change.

### Open-Closed Principle

Design classes so that new behavior can be added by writing new code (new subclasses,
new strategy functions, new configuration), not by editing existing code.

In Python, this is typically achieved via:

- **Protocol / ABC interfaces** that define extension points.
- **Strategy callables** passed into a class (composition over inheritance).
- **Registry patterns** where new handlers are registered without modifying the dispatcher.

### Dependency Inversion

High-level modules (business logic) must not depend on low-level modules (file I/O,
database, network). Both should depend on abstractions.

In Python, use `typing.Protocol` or `abc.ABC` to define the interface that the high-level
module expects. The low-level module implements that interface. The caller (script or
entrypoint) wires them together.

```python
from typing import Protocol


class SoilDataReader(Protocol):
    def read(self, path: Path) -> pd.DataFrame: ...


class ExcelSoilDataReader:
    def read(self, path: Path) -> pd.DataFrame:
        return pd.read_excel(path)


class SoilAnalyser:
    def __init__(self, reader: SoilDataReader) -> None:
        self._reader = reader
```

### Composition over Inheritance

Inheritance exposes a subclass to the internal details of its parent, breaking
encapsulation. Changes to the parent can silently break the subclass. Inheritance
is also static -- it cannot be changed at runtime.

Composition assembles separate objects via their public interfaces ("black-box reuse").
This keeps classes small, focused, and independently replaceable.

**When inheritance is acceptable:**

- Defining a `Protocol` or `ABC` that concrete classes implement.
- Inheriting from framework base classes where required (e.g., `BaseModel`,
  `DataFrameModel`).

**When to use composition:**

- Every other case. Inject collaborators through the constructor.

### Constructor Dependencies

- Never hardcode file paths as class-level or module-level defaults in library code under `src/<package>/`.
- Accept paths as required constructor parameters; let the caller (script/entrypoint) decide which paths to use.
- Library classes own "how to process"; scripts own "what to process" (which files, which rules, which prefixes).
- If you need a default for testing, define it in the test module or a test fixture, not in production code.

Good (library class):

```python
class DocumentProcessor:
    def __init__(self, *, input_file: Path, config: ProcessorConfig) -> None:
        self._input_file = input_file
        self._config = config
```

Bad (hardcoded default path in library):

```python
DEFAULT_INPUT = Path("assets/data/input.txt")  # Don't do this in library code

class DocumentProcessor:
    def __init__(self, *, input_file: Path = DEFAULT_INPUT) -> None:
        ...
```

### When Not to Use a Class

- If a feature can be expressed as a pure function with explicit inputs/outputs, prefer a function.
- Watch for **accidental complexity**: if the problem is simple but the class hierarchy is
  elaborate, you are adding complexity that does not serve the domain.

## Procedure

1. Start with a function-based design.
2. Introduce a class only if it improves clarity or models a domain concept.
3. Prefer deep classes with small interfaces over many shallow classes.
4. Apply Tell, Don't Ask -- keep decisions inside the object that owns the state.
5. Keep the public API small and document it.
6. Inject dependencies via the constructor; depend on abstractions, not concretions.
7. Add tests for non-trivial behavior.
