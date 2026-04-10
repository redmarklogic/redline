---
name: python-domain-modeling
description: Domain modeling conventions (value objects, Pandera/Pydantic, DataFrame-first APIs).
---

# Python Domain Modeling

This skill defines how to model domain data in this repo.

## Architectural stance

The domain layer contains core business logic and is structured as:

- **Entities**: identity-based objects that may be mutable.
- **Value objects**: immutable concepts identified by their data.
- **Aggregates**: consistency boundaries clustering entities/value objects.
- **Domain services**: domain logic that does not naturally belong to a single entity.

This repo uses a validation-first approach:

- **Pydantic** is the standard for entities and value objects.
- **Pandera** is the standard for validating complex DataFrame structures.
- Standard library `@dataclass` is deprecated for domain modeling in this repo (Pydantic/Pandera are treated as core language extensions for runtime safety).

## Tooling strategy (by layer)

- **Domain layer**: Pydantic `BaseModel` for entities/value objects; Pandera `DataFrameModel` for DataFrame-shaped domain contracts when justified.
- **Interface/web layer**: Pydantic models for DTOs (request/response parsing).
- **Infrastructure/adapters**: Pandera `DataFrameModel` (or `DataFrameSchema`) for boundary DataFrame validation.

## Non-negotiables

### Domain owns the canonical model

- The domain model is the source of truth.
- API DTOs and domain models must be separate classes (even if both are Pydantic).
- Dependencies point inward: interface/web depends on domain; domain must not depend on API DTO modules.

Mapping happens in the service/adapter layer (example pattern):

```python
domain_obj = DomainModel.model_validate(dto.model_dump())
```

### DataFrame-first (hybrid encapsulation)

- Treat raw DataFrames as primitives: do not pass raw DataFrames deep into domain logic by default.
- Prefer passing Pydantic-wrapped domain objects or typed wrappers.
- Restrict raw DataFrames + their Pandera schemas to adapters/boundaries.

Data science exception:

- Pandera `DataFrameModel` may enter the domain layer when the domain logic is fundamentally inseparable from the DataFrame structure (e.g., vectorized transformations).
- When allowed, the Pandera schema is the contract that protects invariants.

### Layered validation and invariants

- **Syntactic validation (the edge)**: use Pydantic/Pandera at I/O boundaries for shape, required fields, basic types.
- **Semantic validation (the core)**: enforce business invariants in the domain:
  - Pydantic `@field_validator` / `@model_validator` for per-field and cross-field rules.
  - Pandera checks (`@pa.check`, `@pa.dataframe_check`) for column-wise and dataframe-level invariants.

### Identifiers and entity-ness

- Prefer strongly typed ID value objects (Pydantic models with `ConfigDict(frozen=True)` + a `value` field).
- Entities compare by identity; value objects compare by value.

If you need identity semantics beyond default Pydantic behavior, implement them explicitly on the entity.

### Domain events (when used)

- Model domain events as Pydantic models with `ConfigDict(frozen=True)`.
- Aggregates may record events internally; downstream publication should happen after successful persistence (unit-of-work/message bus pattern).

### Repository pattern (aggregates, ports, adapters)

Use the repository pattern to decouple domain logic from persistence concerns.

- The domain (or service layer) defines the repository interface as a port.
- Infrastructure/adapters provide concrete implementations (SQL, blob storage, filesystem, etc.).
- Repositories should be defined for aggregates: one aggregate should have at most one repository.

Guiding principle: application code should read like it is interacting with an in-memory collection of
aggregates.

Minimal shape:

- `add(aggregate)` to persist a new or updated aggregate
- `get(id)` to load an aggregate by identity

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

Define the repository interface (port) near the consuming layer. Prefer `typing.Protocol` unless you need
runtime ABC checks:

```python
from typing import Protocol


class BatchRepository(Protocol):
    def add(self, batch: Batch) -> None: ...

    def get(self, reference: str) -> Batch: ...
```

Adapters implement the port and are responsible for mapping to and from persistence representations.

Testing benefit:

- Write unit tests for domain/service logic against a fake repository implementation that keeps aggregates in
  memory.
- This keeps tests fast and independent from database/network I/O.

## File/module layout

Organize domain code by bounded context / aggregate (vertical slicing). Allowed layouts:

- `src/<package>/domain/<aggregate_name>.py` (or a subpackage) grouping: entity, value objects, and aggregate-specific exceptions.
- `src/<package>/domain/events.py` for domain events.
- Value objects must live in `src/<package>/domain/value_objects/<value_object_name>.py` and be re-exported from `src/<package>/domain/value_objects/__init__.py`.
- Value object class names should be domain-oriented nouns; avoid implementation terms like `Schema` or `DataFrame` or 'Table' (prefer names like `RulebankMetadata`).
- When re-exporting from `src/<package>/domain/value_objects/__init__.py`, export only the primary value object models; do not export supporting enums/constants.
- Do not add standalone validation helper functions for value objects (e.g., `validate_*` wrappers). Call `model_validate(...)` / Pandera `.validate(...)` from the boundary or service code that owns the workflow.
- **NEVER create direct unit tests for value objects.** There must be no `tests/*/domain/value_objects/test_*.py` file. Value objects are exercised indirectly through the services and functions that use them.
- **Minimalist implementation**: Do not create adapters, schemas, validator functions or tests for a value object unless explicitly requested.
- **Column aliases**: When using `pa.Field(alias="...")` or Pydantic aliases, keep the alias as a string literal directly in the field definition for clarity, even if repeated across the module. Do not define constants for these.
- When a value object will later map to CSV, Excel or SQL database table columns, define Pydantic `Field` aliases using the CSV column names and enable alias-based validation/serialization.

API schemas (DTOs) belong in the interface/entrypoint layer (keep them distinct from domain types).

## Documentation requirements

- For Pandera `pa.Field(...)`: include `description=` for every domain-relevant column; include units/constraints when meaningful.
- Prefer snake_case field/column names in domain.
- If source data is messy (e.g., CamelCase), map it at the adapter boundary using aliases (Pydantic) or column renaming, not in the domain.

## Inheritance when extending value objects

When adding a new value object that extends an existing one (e.g. adding fields to a base concept), **prefer inheritance over duplication**:

- Subclass the existing value object and add only the new fields.
- Do not redeclare fields already defined on the parent.
- Name the subclass to reflect the extended concept (e.g. `ConsolidationFinding(ReviewFinding)` not a flat copy).

## Schema evolution & compatibility

When changing domain schemas (Pydantic or Pandera):

- **No default backward compatibility**: Unless explicitly instructed, do not maintain backward compatibility with external systems (APIs, legacy files, databases) during refactors or renames.
- **De-clutter immediately**: Delete deprecated shims, old constants, and retired types immediately as part of the refactor.
- **Self-contained focus**: Assume the goal is technical debt reduction and internal consistency, not support for unnamed external callers.

Do not hardcode library version numbers in this skill; the authoritative pins are in `uv.lock`.

## Pre-commit hook enforcement

The rule against stdlib `@dataclass` in `src/rl/` is enforced at commit time by
`hooks/check-no-dataclass-in-domain.py`. Any `from dataclasses import` or `@dataclass`
statement in `src/rl/**/*.py` will fail the commit with an actionable error message.

For rules specific to Pydantic models used as `output_pydantic` in CrewAI tasks (collection field typing, defensive validators, `expected_output` wording), use the `python-crewai` skill.

## Procedure

1. Model core entities and value objects with Pydantic and/or Pandera in the domain layer.
2. Validate DataFrame-shaped boundaries with Pandera where DataFrame contracts are required.
3. Keep API DTOs separate from domain models and perform mapping in services/adapters.
4. Enforce semantic invariants in model validators/checks.
5. Add focused tests for domain invariants and boundary mappings.

## Testing expectations

Minimum expectations when introducing/changing a domain model:

- Unit tests covering happy-path invariants in the domain (pure logic; no I/O).
- Boundary tests that validate mapping from external DTOs/inputs to domain models (anti-corruption layer behavior).

For baseline unit test conventions, use the `python-testing-unit` skill.

## Imports

- When importing internal modules, do not include the `src` folder in the import path.
