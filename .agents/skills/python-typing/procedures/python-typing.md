# Python Typing — Detailed Reference

## Context & Guidelines

### Scope

Apply these rules whenever you add or refactor Python code in `src/`.

### Core Rules

- **Never** use `from __future__ import annotations`; the codebase targets Python 3.14+ where PEP 604 (`X | Y`) and built-in generics (`list[int]`) are native — no backport shim is needed.
- Type annotations are mandatory for function/method signatures (parameters and return type).
- Avoid `Any` unless absolutely necessary; prefer precise types or `TypeAlias`.
- Prefer narrow, intention-revealing types.
- Keep function signatures readable; extract complex types into a `TypeAlias`.
- Prefer built-in generics (e.g., `list[int]`, `dict[str, int]`) over `typing.List`/`typing.Dict`.
- Prefer unions using `X | Y` over `Union[X, Y]`.

### Ruff-Driven Typing Rules

- Avoid deprecated `typing` collection aliases like `typing.Dict` and `typing.List`; use built-in generics.
- Prefer Python 3.14 type parameters over `Generic[...]` base classes when writing generic code.

### Third-Party API Typing

- When using Google API clients, ensure resource objects are properly type-annotated (avoid untyped
  `dict`/`Any` for resources).

### Nullable Types

- Use `T | None` for optional values.
- Avoid using `None` to encode multiple behaviors. If there are multiple modes, model them
  explicitly (separate functions, strategy objects, or distinct types).

### Constrained Values

- Prefer `Literal[...]` when a value is one of a small set of known options.

### Context Managers

Type context manager methods explicitly.

- `__exit__` / `__aexit__` should include the exception triple:
  - `exc_type: type[BaseException] | None`
  - `exc_val: BaseException | None`
  - `exc_tb: TracebackType | None`

## Procedure

1. Add signature annotations for all parameters and return type.
2. If a parameter can be absent, use `T | None` and document the meaning.
3. If a type expression becomes hard to read, introduce a `TypeAlias`.
4. Prefer `Literal[...]` or dedicated value objects when values are constrained.

## Examples

### Good Example (TypeAlias for readability)

```python
from collections.abc import Callable
from typing import TypeAlias

Transformer: TypeAlias = Callable[[str], str]


def apply_transform(*, text: str, transform: Transformer) -> str:
    return transform(text)
```

### Good Example (Context manager typing)

```python
from types import TracebackType


class Resource:
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        return None

```

### Good Example (Python 3.14 type parameters)

```python
class Box[T]:
  def __init__(self, value: T) -> None:
    self.value = value
```
