---
name: python-class-design
description: Standards for designing maintainable Python classes (responsibilities, init, composition).
---

# Python Class Design

This skill defines how to design Python classes in this repo.

## Context & Guidelines

### Scope

Apply whenever you add or refactor classes under `src/`.

### Core Rules

- Keep classes focused on a single responsibility.
- Keep `__init__` simple; avoid complex logic in constructors.
- Prefer composition over inheritance.
- Use dataclasses for simple data containers.
- Use `@property` for computed attributes.

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

## Procedure

1. Start with a function-based design.
2. Introduce a class only if it improves clarity or models a domain concept.
3. Keep the public API small and document it.
4. Add tests for non-trivial behavior.
