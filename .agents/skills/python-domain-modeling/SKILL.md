---
name: python-domain-modeling
description: Use when modeling domain objects in Python -- value objects, Pandera/Pydantic contracts, or DataFrame-first API design
paths: "src/**/*.py,tests/**/*.py"
---

# Python Domain Modeling

Tactical DDD conventions for domain objects in this repo. For strategic DDD (subdomain classification, bounded contexts), use `ddd-strategic`.

## Boundary Contract

**Applies To:** Domain objects (Pydantic models, Pandera schemas, value objects) under `src/` | **Produces:** Tactical DDD artifacts following DataFrame-first API and value-object conventions | **Does Not Cover:** Strategic DDD (`ddd-strategic`), general class design (`python-class-design`), data ingestion (`python-data-ingestion`)

## Layer Architecture

| Layer | Location | Can Import From |
|---|---|---|
| `functions` | `src/rl/functions/` | `schemas`, `domain` |
| `schemas` | `src/rl/schemas/` | `domain` only |
| `domain` | `src/rl/domain/` | Nothing within `src/rl/` |

Enforced by `import-linter`. Escalate new top-level packages under `src/rl/` to Principal Engineer.

## Quick Reference

| Concern | Tool |
|---|---|
| Entities / value objects | Pydantic `BaseModel` with `frozen=True` |
| DataFrame contracts | Pandera `DataFrameModel` |
| API DTOs | Separate Pydantic models (never mix with domain) |
| Input validation | `@validate_call` on public functions only |
| Repository interfaces | `typing.Protocol` |

See `procedures/domain-modeling.md` for full rules: architectural stance, non-negotiables, file layout, testing expectations, schema evolution, and subdomain classification.

## Non-Negotiables

Every annotated attribute in a Pydantic model under `src/*/domain/` or `src/*/schemas/` **must** use `Field(description=..., alias=...)`:

```python
# Wrong
project_number: str

# Wrong
project_number: str = Field(...)

# Correct
project_number: str = Field(description="Client-assigned project number.", alias="Project Number")
```

`description` makes the model self-documenting. `alias` makes serialization explicit and decoupled from internal naming. The `check-pydantic-field-metadata` pre-commit hook enforces this at commit time.

**Alias rules:**

| Rule | Guidance |
|---|---|
| Format | Title Case with spaces: `project_number` → `"Project Number"` |
| Wording | Match UI Terminology Glossary exactly; unknown term → escalate to domain expert |
| Units | Append unit in parens when implicit: `"Depth (m)"`, `"Pressure (kPa)"` |
| Stability | Alias is a serialization contract; renaming breaks existing Excel/JSON output |
| Consistency | Same concept → same alias everywhere in the codebase |
| Abbreviations | Full term unless the abbreviation IS the standard: `"N60"`, `"qu"` |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using a plain dict to represent a domain concept | Define a Pydantic BaseModel or Pandera DataFrameModel; dicts have no contract |
| Putting I/O logic (file reads, API calls) inside a domain model | Domain models are pure; move I/O to a reader or service layer |
| Inheriting from pd.DataFrame to add domain behaviour | Use composition -- wrap a validated DataFrame in a value object, never subclass it |
| Declaring a field without `Field(description=..., alias=...)` | Every field needs both; the pre-commit hook blocks the commit otherwise |
