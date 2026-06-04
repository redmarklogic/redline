---
name: python-testing-unit
description: Use when writing unit tests in this repo -- test structure, fixtures, mocking, or coverage patterns
paths: "src/**/*.py,tests/**/*.py"
---

## Boundary Contract

### Applies To
- Unit tests under `tests/` using pytest

### Produces
- Tests following Arrange/Act/Assert, equivalence classes, and parametrize conventions

### Does Not Cover
- API endpoint testing (`python-testing-api`)
- TDD workflow (`test-driven-development`)
- General style (`python-style`)


See `procedures/python-testing-unit.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Testing multiple behaviours in one test function | One assertion of intent per test; use separate functions with descriptive names |
| Patching at the wrong scope (patching origin instead of usage) | Patch where the name is looked up (the module under test), not where it is defined |
| Writing tests that rely on execution order between test functions | Each test must be fully self-contained with its own setup; never share mutable state |