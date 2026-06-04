---
name: python-class-design
description: Use when designing Python classes -- structuring responsibilities, init patterns, or choosing composition over inheritance
paths: "src/**/*.py,tests/**/*.py"
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


See `procedures/python-class-design.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Putting business logic in __init__ | Move logic to a dedicated method; keep __init__ to assignment only |
| Inheriting to reuse implementation | Prefer composition — inherit only for true is-a relationships |
| Single class doing data loading, validation, and transformation | Split into focused classes with one responsibility each |