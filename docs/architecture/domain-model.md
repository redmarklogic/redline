# Domain Model

Living document capturing the strategic domain architecture of the Redline project.
Updated during the `spec-kit` plan phase whenever a feature introduces new domain
concepts, packages, or bounded contexts.

Authoritative layer enforcement: `pyproject.toml` under `[tool.importlinter]`.

## Domain Vision

Redline is a geotechnical engineering analysis platform that automates residential
foundation and retaining wall assessments for New Zealand council compliance.

## Subdomain Classification

| Subdomain         | Classification | Package            | Tactical Pattern                 |
| ----------------- | -------------- | ------------------ | -------------------------------- |
| Geotechnical core | Core           | `src/rl/domain/`   | Full DDD: aggregates, events     |
| Data ingestion    | Supporting     | `src/rl/functions/` | Transaction scripts, readers    |
| Report generation | Supporting     | TBD                | Template-driven output           |

## Bounded Contexts

<!-- Each bounded context maps to a package. Add new contexts as the domain grows. -->

| Context            | Package                        | Independence Contract |
| ------------------ | ------------------------------ | --------------------- |
| Retaining wall     | `rl.functions.readers.retaining_wall` | N/A (single context)  |

## Layer Architecture

```
calculators    (highest -- orchestration, scripts)
    |
functions      (business logic, readers)
    |
schemas        (Pandera DataFrameModels for boundaries)
    |
enrichment     (data enrichment, transformations)
    |
domain         (lowest -- entities, value objects, events)
```

Enforced by import-linter contracts in `pyproject.toml`. See
`.agents/skills/spec-kit/references/import-linter.md` for the full reference.

## Ubiquitous Language

<!-- Add domain terms with clear definitions. Use these terms consistently in
     code (class/method/variable names), documentation, and conversation. -->

| Term               | Definition                                                    |
| ------------------ | ------------------------------------------------------------- |
| <!-- Example -->   |                                                               |

## Entity and Value Object Registry

<!-- Track key domain objects, their type, and location. -->

| Name               | Type         | Module Path                              |
| ------------------ | ------------ | ---------------------------------------- |
| <!-- Example -->   |              |                                          |

## Context Map

<!-- Document relationships between bounded contexts as the system grows.
     Relationship types: Shared Kernel, Customer-Supplier, Conformist,
     Anti-Corruption Layer, Open Host Service, Published Language. -->

No inter-context relationships yet (single bounded context).
