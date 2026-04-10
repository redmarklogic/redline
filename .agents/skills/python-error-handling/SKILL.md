---
name: python-error-handling
description: Standards for exception handling, error translation, and logging in this repo.
---

# Python Error Handling

This skill defines how to handle errors in a way that preserves tracebacks, keeps business
logic readable, and makes failures actionable.

## Context & Guidelines

### Scope

Apply these rules whenever you add or refactor Python code in `src/`.

### Prefer Exceptions to Error Codes

- Prefer raising exceptions over returning sentinel values or error codes.
- Return values should represent successful results.

### Separate Work from Error Translation

- Keep the happy path linear.
- Prefer a thin wrapper that catches and translates exceptions around a pure "do the work"
  function.
- Avoid mixing business logic with logging/translation when possible.

### try/except Patterns

- Do not silently swallow exceptions without logging or re-raising.
- Do not use bare `except:`.
- Catch specific exceptions rather than broad exception types (e.g., avoid `except Exception:`).
- **NEVER** use "greedy" exception handling (catching `Exception` just to log it and continue) in
  functions where failure should halt execution or be handled by the caller.
- Use bare `raise` inside `except` blocks to preserve tracebacks.
- When a return depends on the `try` succeeding, put the return in the `else` block.

### Logging

- Use `logging.exception(...)` inside `except` blocks when you want a stack trace.
- Do not include the exception object in `logging.exception(...)` calls.
- Provide meaningful error messages that explain context and next action.

## Procedure

1. Write the happy path first.
2. Add guard clauses for invalid input.
3. Catch only the exceptions you can handle meaningfully.
4. If you need to translate an exception type, do it in a thin wrapper.
5. Log only where it adds value (boundaries: APIs, jobs, scripts).

## Examples

### Good Example (thin wrapper)

```python
import logging

logger = logging.getLogger(__name__)


def load_config_text(*, path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def load_config_text_safe(*, path: str) -> str:
    try:
        return load_config_text(path=path)
    except OSError:
        logger.exception("Failed to read config")
        raise
```

### Good Example (`try` / `except` / `else`)

```python

def parse_positive_int(*, text: str) -> int:
    try:
        value = int(text)
    except ValueError:
        raise
    else:
        if value <= 0:
            raise ValueError("Expected a positive integer")
        return value
```
