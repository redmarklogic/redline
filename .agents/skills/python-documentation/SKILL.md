---
name: python-documentation
description: Use when writing Python docstrings or documentation -- Google Style, type hint integration, or fixing missing or incorrect documentation
paths: "src/**/*.py,tests/**/*.py"
---

# Python Documentation Standards

This skill defines the standards for documenting Python code, following the Google Python Style Guide with specific adaptations for type-annotated code.

## Boundary Contract

### Applies To
- Docstrings in all Python modules, classes, and functions under `src/` and `tests/`

### Produces
- Google Style docstrings that complement type annotations without redundancy

### Does Not Cover
- Type hint standards (`python-typing`)
- Lint rule enforcement (`python-linting`)
- README and architecture docs (`doc-updater`)

## Core Rules

1. **Mandatory Documentation**: Public functions, classes, and methods must have docstrings.
2. **Parameters**: Document all function parameters.
3. **Returns**: Document return values.
4. **Exceptions**: Document exceptions raised.
5. **Maintainability**: Keep comments up-to-date with code changes.
6. **Examples**: Include examples for complex functions.

## Docstring Structure and Section Order

According to the Google Python Style Guide, docstring fields should appear in a specific order.

The docstring must start with a summary line, followed by a blank line, and then the extended description (optional) and specific sections.

## Type Hint Integration

Since the codebase uses Python 3.14+ with type hints, documentation should obey the following rules to avoid redundancy:

- **Do not** include type information in the docstring (args or returns) if it is already present in the function signature.
- **Do** describe the _purpose_ of the argument or return value.

If a function raises an exception as part of its normal contract, document it in a `Raises:`
section.

## Styling

- Follow the **Google Python Style Guide**.


See `procedures/python-documentation.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Writing Args: with positional-only descriptions and no type hint | Type hints belong in the signature; Args: should describe intent, not type |
| Documenting self in the Args: section | Never document self or cls — they are implicit |
| Putting implementation details in the docstring summary line | Summary is the what, not the how; move implementation notes to the body or inline comments |