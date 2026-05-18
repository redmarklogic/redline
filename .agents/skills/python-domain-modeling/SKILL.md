---
name: python-domain-modeling
description: Domain modeling conventions (value objects, Pandera/Pydantic, DataFrame-first APIs).
---

# Python Domain Modeling

This skill defines **tactical DDD** conventions: how to implement domain objects in
Python. For **strategic DDD** decisions (subdomain classification, bounded context
identification, EventStorming, context maps, anti-corruption layers, model evolution
governance), use the `ddd-strategic` skill.

## Boundary Contract

### Applies To
- Domain objects (Pydantic models, Pandera schemas, value objects) under `src/`

### Produces
- Tactical DDD artifacts following DataFrame-first API and value-object conventions

### Does Not Cover
- Strategic DDD decisions and bounded context identification (`spec-kit` plan phase)
- General class design patterns (`python-class-design`)
- Data ingestion pipelines (`python-data-ingestion`)

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

## Subdomain classification

Not every domain area needs full DDD treatment. Classify each subdomain before choosing
tactical patterns:

| Classification | Pattern choice                                      | Example                           |
| -------------- | --------------------------------------------------- | --------------------------------- |
| **Core**       | Full DDD: aggregates, domain events, rich model     | Geotechnical analysis engine      |
| **Supporting** | Simpler: transaction scripts, thin domain layer     | Report formatting, data ingestion |
| **Generic**    | Off-the-shelf libraries, no custom domain model     | Authentication, email delivery    |

The `ddd-strategic` skill's `procedures/subdomain-classification.md` covers when and
how to classify subdomains. The `spec-kit` skill's plan phase includes a Domain Impact
section where subdomain classification is recorded for each feature.

## Model evolution governance

Domain models must evolve as understanding deepens. Follow these tactical rules when
changing domain objects:

- **Value Objects:** Replace entirely. Value objects are immutable -- create a new type
  rather than mutating an existing one.
- **Entities:** Update attributes while maintaining identity. Entity refactors must
  preserve the identity mechanism.
- **Aggregates:** Keep small. One transaction per aggregate. Use eventual consistency
  between aggregates.
- When a model change affects the Ubiquitous Language, update the UL table in
  `docs/architecture/domain-model.md` first, then refactor the code.
- When a model change affects multiple bounded contexts, update the Context Map
  (see `ddd-strategic` `procedures/context-mapping.md`) before propagating changes.

For the full strategic governance framework, use the `ddd-strategic` skill.

## Modularity vs. layering

Modularity and layering are orthogonal architectural tools that complement each other:

- **Layering** enforces dependency direction *within* a component (higher layers depend
  on lower layers, never the reverse). It answers: "who can import whom inside this
  boundary?"
- **Modularity** decomposes the system into independent, replaceable components at the
  *package* level. It answers: "what are the independently evolvable units?"

Each top-level package under `src/` is a modular component. Each component may apply its
own internal layered architecture. The integration hub (`src/rl/`) composes the
independent components but does not own them.

For the full research and citations, see `docs/research/20260412-modularity-vs-layering.md`.

## Bounded contexts

A bounded context is a boundary within which a domain model is consistent and terms
have a single meaning. In DDD, bounded contexts map to **top-level packages**, not
subpackages:

- Each bounded context gets its own top-level package under `src/`.
- Bounded contexts must not import from each other directly. Use an
  `independence` contract in `pyproject.toml` to enforce this.
- The integration hub (`src/rl/`) may import from bounded context packages, but they
  must not import from `rl` or from each other.

### Deciding: new top-level package vs. subpackage

Use this decision matrix when introducing a new capability:

| # | Signal | New top-level package | Keep as subpackage |
|---|--------|-----------------------|--------------------|
| 1 | **Language boundary** | Introduces new domain vocabulary or existing terms take on different meanings | Intrinsic part of existing Ubiquitous Language |
| 2 | **Conceptual cohesion** | Does not share data or concepts with existing package | Shares information and is frequently used together with existing code |
| 3 | **General vs. special** | Existing package is general-purpose; new capability is special-purpose application | Combining simplifies the overall interface |
| 4 | **Rate of change** | New capability changes at a different rate or for different reasons | Both change at similar rates for similar reasons |
| 5 | **Future extraction** | May graduate to a standalone PyPI package | Will always live in this repo |

If the majority of signals point to "new top-level package", create a sibling under
`src/`. If signals are mixed or point to subpackage, add a subpackage to the existing
package and update its layer contract.

### Context mapping between packages

When bounded context packages need to share domain concepts:

- **Shared kernel**: A small, stable shared package (`src/<shared>/`) that both contexts
  import. Acceptable in this repo because all code is deployed together and retest cost
  is minimal. Use for highly stable types shared across multiple contexts.
- **Anti-Corruption Layer**: A translation layer built by the consuming context. Use
  when the upstream model is volatile or when protecting a Core Domain from foreign
  concepts.
- **Duplication**: Accept that the same real-world concept means something slightly
  different in each context and model it separately. Use when the concept genuinely
  diverges across contexts.

**Monorepo tradeoff**: In a monorepo with single-command deployment and minimal
compilation time, the "retested and redeployed" argument against shared packages does
not apply. A shared kernel is a reasonable default when types are stable and genuinely
identical across contexts.

See `.agents/skills/spec-kit/references/import-linter.md` for contract examples.

## Ubiquitous Language

Domain terms must be used consistently in code, docs, and conversation:

- Class names, method names, and variable names use domain terms, not technical terms.
- New domain terms introduced during planning should be added to
  `docs/architecture/domain-model.md` under the Ubiquitous Language section.
- When domain terms conflict with Python builtins or stdlib names (e.g., `statistics`),
  suppress `A005` and document the reason inline.
- **Language change = code refactor.** When the team discovers a better domain term,
  the code changes immediately. Code and speech are the two enduring expressions of
  the model; documents go stale. This rule is non-negotiable -- see `ddd-strategic`
  skill, UL Rules.

## Multi-package layout

This repo contains multiple top-level packages under `src/`, one per bounded context:

- `src/rl/` -- integration hub (thin orchestrator that composes tools)
- Additional packages (e.g., `src/skeleton/`, `src/reviewer/`) are added as sibling
  top-level packages when a new bounded context is identified.

When adding a new top-level package:

1. Add it to `root_packages` in the import-linter config.
2. Create its own layer contracts (if it has internal layers).
3. Add an `independence` contract between it and other bounded context packages.
4. Add it to `build.targets.wheel.packages` in `pyproject.toml`.

See the import-linter reference for details.

## Layer enforcement

Import-linter contracts in `pyproject.toml` enforce the dependency direction at the
module level. When adding a new subpackage under an `exhaustive = true` container:

1. Add it to the `layers` list in the corresponding contract.
2. Or add it to `exhaustive_ignores` if it is cross-cutting.

See `.agents/skills/spec-kit/references/import-linter.md` for the full reference.
