# Python Domain Modeling — Detailed Reference

## Layer Architecture

This repo follows a strict layered architecture enforced by `import-linter`. Dependencies
point inward — outer layers depend on inner layers, never the reverse. Violations are
caught at pre-commit time and in CI.

### Current live layers (as of 2026-05-23)

| Layer | Location | Responsibility | Can import from |
|---|---|---|---|
| `functions` | `src/rl/functions/` | Stateless business operations, data transformations, file readers | `schemas`, `domain` |
| `schemas` | `src/rl/schemas/` | Shared data contracts — Pandera/Pydantic schemas used across layers | `domain` only |
| `domain` | `src/rl/domain/` | Core business logic: entities, value objects, aggregates, domain events | Nothing within `src/rl/` |

Layers not listed here (`adapters/`, `api/`, `web/`) **do not exist yet**. Do not create them without the Principal Engineer's approval.

### Machine enforcement

`import-linter` enforces the layer order via contracts in `pyproject.toml`:

```toml
[[tool.importlinter.contracts]]
name = "rl layers"
type = "layers"
layers = [ "functions", "schemas", "domain" ]
containers = [ "rl" ]
exhaustive = true   # no other top-level packages are permitted
```

`exhaustive = true` means the linter will **fail** if any package other than `functions`,
`schemas`, or `domain` appears directly under `src/rl/`. Adding a new top-level package
is an architectural decision — escalate to the Principal Engineer.

### Prohibited imports (enforced)

| This layer... | MUST NOT import from... |
|---|---|
| `domain` | `schemas`, `functions`, anything outside `src/rl/domain/` |
| `schemas` | `functions` |

Violations fail the `lint-imports` pre-commit hook. Do not suppress this hook.

### Scripts

`scripts/` sits outside `src/rl/` and is the thin orchestration layer. Scripts wire
layers together — they may import from any layer. Scripts must not contain business logic.

### When to escalate to the Principal Engineer

- Adding any new top-level package under `src/rl/` (e.g., `services/`, `adapters/`)
- Moving code between layers
- Updating the `import-linter` contracts in `pyproject.toml`
- Importing across a boundary that the linter currently prohibits

## Architectural Stance

The domain layer contains core business logic structured as:

- **Entities**: identity-based objects that may be mutable.
- **Value objects**: immutable concepts identified by their data.
- **Aggregates**: consistency boundaries clustering entities/value objects.
- **Domain services**: domain logic that does not naturally belong to a single entity.

This repo uses a validation-first approach:

- **Pydantic** is the standard for entities and value objects.
- **Pandera** is the standard for validating complex DataFrame structures.
- Standard library `@dataclass` is deprecated for domain modeling in this repo.

## Tooling Strategy (by layer)

- **Domain layer**: Pydantic `BaseModel` for entities/value objects; Pandera `DataFrameModel` for DataFrame-shaped domain contracts when justified.
- **Interface/web layer**: Pydantic models for DTOs (request/response parsing).
- **Infrastructure/adapters**: Pandera `DataFrameModel` (or `DataFrameSchema`) for boundary DataFrame validation.

## Non-Negotiables

### Domain owns the canonical model

- The domain model is the source of truth.
- API DTOs and domain models must be separate classes (even if both are Pydantic).
- Dependencies point inward: interface/web depends on domain; domain must not depend on API DTO modules.

Mapping happens in the service/adapter layer:

```python
domain_obj = DomainModel.model_validate(dto.model_dump())
```

### DataFrame-first (hybrid encapsulation)

- Treat raw DataFrames as primitives: do not pass raw DataFrames deep into domain logic by default.
- Prefer passing Pydantic-wrapped domain objects or typed wrappers.
- Restrict raw DataFrames + their Pandera schemas to adapters/boundaries.

Data science exception: Pandera `DataFrameModel` may enter the domain layer when the
domain logic is fundamentally inseparable from the DataFrame structure.

### Layered validation and invariants

- **Syntactic validation (the edge)**: use Pydantic/Pandera at I/O boundaries for shape, required fields, basic types.
- **Semantic validation (the core)**: enforce business invariants in the domain via `@field_validator` / `@model_validator` (Pydantic) or `@pa.check` / `@pa.dataframe_check` (Pandera).

### Identifiers and entity-ness

- Prefer strongly typed ID value objects (Pydantic models with `ConfigDict(frozen=True)` + a `value` field).
- Entities compare by identity; value objects compare by value.

### Domain events

- Model domain events as Pydantic models with `ConfigDict(frozen=True)`.
- Aggregates may record events internally; downstream publication happens after successful persistence.

### Repository pattern

Use the repository pattern to decouple domain logic from persistence:

```python
from typing import Protocol

class BatchRepository(Protocol):
    def add(self, batch: Batch) -> None: ...
    def get(self, reference: str) -> Batch: ...
```

Minimal shape: `add(aggregate)` to persist, `get(id)` to load.

Example domain types (Pydantic v2):

```python
from pydantic import BaseModel, ConfigDict, Field

class OrderLine(BaseModel):
    model_config = ConfigDict(frozen=True)
    order_id: str
    sku: str
    qty: int = Field(gt=0)

class Batch(BaseModel):
    reference: str
    sku: str
    purchased_quantity: int
    allocations: set[OrderLine] = Field(default_factory=set)

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self.allocations.add(line)

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

    @property
    def available_quantity(self) -> int:
        return self.purchased_quantity - sum(line.qty for line in self.allocations)
```

## File / Module Layout

Organize domain code by bounded context / aggregate (vertical slicing):

- `src/<package>/domain/<aggregate_name>.py` grouping entity, value objects, and aggregate-specific exceptions.
- `src/<package>/domain/events.py` for domain events.
- Value objects must live in `src/<package>/domain/value_objects/<value_object_name>.py` and be re-exported from `src/<package>/domain/value_objects/__init__.py`.
- Value object class names should be domain-oriented nouns; avoid implementation terms like `Schema` or `DataFrame` or `Table`.
- When re-exporting, export only the primary value object models; do not export supporting enums/constants.
- Do not add standalone validation helper functions for value objects. Call `model_validate(...)` / Pandera `.validate(...)` from boundary or service code.
- **NEVER create direct unit tests for value objects.** No `tests/*/domain/value_objects/test_*.py` files.
- **Minimalist implementation**: Do not create adapters, schemas, validator functions or tests for a value object unless explicitly requested.
- **Column aliases**: Keep aliases as string literals directly in the field definition, not as constants.
- When a value object will map to CSV/Excel/SQL columns, define Pydantic `Field` aliases using column names.

API schemas (DTOs) belong in the interface/entrypoint layer.

## Documentation Requirements

- For Pandera `pa.Field(...)`: include `description=` for every domain-relevant column; include units/constraints when meaningful.
- Prefer snake_case field/column names in domain.
- If source data is messy (e.g., CamelCase), map it at the adapter boundary, not in the domain.

## Inheritance When Extending Value Objects

When adding a new value object that extends an existing one:

- Subclass the existing value object and add only the new fields.
- Do not redeclare fields already defined on the parent.
- Name the subclass to reflect the extended concept (e.g. `ConsolidationFinding(ReviewFinding)`).

## Schema Evolution & Compatibility

- **No default backward compatibility**: Do not maintain backward compatibility with external systems during refactors.
- **De-clutter immediately**: Delete deprecated shims, old constants, and retired types immediately.
- **Self-contained focus**: Assume internal consistency is the goal, not support for unnamed external callers.

## Pre-Commit Hook Enforcement

The rule against stdlib `@dataclass` in `src/rl/` is enforced by `hooks/check-no-dataclass-in-domain.py`.
Any `from dataclasses import` or `@dataclass` in `src/rl/**/*.py` will fail the commit.

For rules specific to Pydantic models used as `output_pydantic` in CrewAI tasks, use the `python-crewai` skill.

## Procedure

1. Model core entities and value objects with Pydantic and/or Pandera in the domain layer.
2. Validate DataFrame-shaped boundaries with Pandera where DataFrame contracts are required.
3. Keep API DTOs separate from domain models and perform mapping in services/adapters.
4. Enforce semantic invariants in model validators/checks.
5. Add focused tests for domain invariants and boundary mappings.

## Testing Expectations

- Unit tests covering happy-path invariants in the domain (pure logic; no I/O).
- Boundary tests validating mapping from external DTOs/inputs to domain models.

For baseline unit test conventions, use the `python-testing-unit` skill.

## Subdomain Classification

| Classification | Pattern choice | Example |
|---|---|---|
| **Core** | Full DDD: aggregates, domain events, rich model | Geotechnical analysis engine |
| **Supporting** | Simpler: transaction scripts, thin domain layer | Report formatting, data ingestion |
| **Generic** | Off-the-shelf libraries, no custom domain model | Authentication, email delivery |

The `ddd-strategic` skill's `procedures/subdomain-classification.md` covers when and how to classify subdomains.

## Imports

When importing internal modules, do not include the `src` folder in the import path.
