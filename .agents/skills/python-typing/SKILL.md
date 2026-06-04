---
name: python-typing
description: Use when writing type hints in Python -- annotation style, generics, Optional, or fixing mypy type errors in this repo
paths: "src/**/*.py,tests/**/*.py"
---

# Python Typing

This skill defines how to write type hints that improve readability and correctness without
adding noise.

## Boundary Contract

### Applies To
- Type annotations across all Python modules under `src/` and `tests/`

### Produces
- Clear, consistent type hints that improve readability without noise

### Does Not Cover
- Docstring standards (`python-documentation`)
- Lint enforcement (`python-linting`)
- Domain model types (`python-domain-modeling`)


See `procedures/python-typing.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using List[str] instead of list[str] (Python 3.9+) | Use built-in generic types (list, dict, 	uple) directly; no need to import from 	yping |
| Annotating Optional[X] when X \| None is clearer | Prefer X \| None union syntax (Python 3.10+) over Optional[X] |
| Returning Any to suppress a type error | Define the correct return type; Any disables type checking for callers downstream |