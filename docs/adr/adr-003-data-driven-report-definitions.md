# ADR-003: Data-Driven Report Definitions via ReportDefinition

## Summary

Report section structures, heading conventions, and conditional flags live in frozen `ReportDefinition` Pydantic objects — not in hard-coded builder constants or inline branching (accepted 2026-04-12). Each jurisdiction / report-type / company combination is a distinct instance in `definitions.py`; adding a new variant never requires touching builder code. Phase 0–3 ships a single `NZ_GIR` definition. The hard constraint: builder functions must contain no if/else branching on jurisdiction or report type — all such variation belongs in the `ReportDefinition`.

## Decision

Define report section structures, heading conventions, and conditional flags
in a `ReportDefinition` data object rather than as hard-coded constants or
inline logic in builder functions. Each combination of jurisdiction, report
type, and company convention produces a distinct `ReportDefinition` instance.
Phase 0-3 ships a single `NZ_GIR` definition.

## Status

Accepted -- 2026-04-12

## Context

The skeleton generator must produce structured DOCX reports. The first target
is a Geotechnical Investigation Report (GIR) for New Zealand. However, the
broader product vision includes:

- **Multiple report types**: GIR, GFR, environmental, structural.
- **Multiple jurisdictions**: NZ, AU, US, UK -- each with different standard
  section structures, naming conventions, and regulatory requirements.
- **Multiple company conventions**: Different companies use sentence-case or
  title-case headings, different appendix naming, and different section ordering.

If section names, ordering, and conditional logic are hard-coded in builder
functions or scattered across module-level constants, each new jurisdiction or
report type requires modifying builder code. This violates the open-closed
principle and creates a growing maintenance burden.

The key question is: where does the section structure live?

## Options Considered

### Option A: Module-level constants

Define heading strings and table headers as constants in a `constants.py`
module. Builder functions import and iterate over them.

```python
# constants.py
HEADING_GEOLOGY = "Geology and faulting"
HEADING_SEISMIC = "Seismic shaking hazard"
TABLE_GEO_MODEL_COLS = ["Layer", "Soil type", ...]
```

**Rejected because**:

- Adding a new report type means adding a parallel set of constants and
  branching in the builder.
- No structured way to express hierarchy (parent-child sections), conditionality,
  or metadata like heading case.
- Scales poorly: 10 report types across 4 jurisdictions = 40 constant sets.

### Option B: ReportDefinition data object (chosen)

Define a `ReportDefinition` Pydantic model that describes the full section tree,
heading conventions, and valid condition flags. Each report type/jurisdiction/company
combination is a single `ReportDefinition` instance defined in `definitions.py`.

```python
class ReportDefinition(BaseModel, frozen=True):
    report_type: str          # "GIR", "GFR", etc.
    jurisdiction: str         # "NZ", "AU", etc.
    heading_case: str         # "sentence" or "title"
    front_matter: list[SectionSpec]
    body_sections: list[SectionSpec]
    back_matter: list[SectionSpec]
    condition_flags: list[str]
```

### Option C: External configuration (YAML/JSON files)

Store report definitions in YAML or JSON files loaded at runtime.

**Rejected because**:

- Adds a file-loading layer and schema validation that Pydantic already
  provides when the definition is in Python.
- Definitions need to be version-controlled alongside code anyway.
- Loses IDE autocomplete and static analysis on the definition structure.
- Premature: if dozens of definitions accumulate, migration to external config
  is straightforward from the Pydantic model.

### Option D: Database-driven definitions

Store report structures in a database, editable via an admin UI.

**Rejected because**:

- Adds infrastructure complexity (database, migrations, admin UI) for a problem
  that currently has one instance (NZ GIR).
- Section structures change infrequently -- version-controlled Python objects
  are sufficient.
- Can be introduced later if the number of definitions grows beyond what code
  files can reasonably manage.

## Decision Rationale

**ReportDefinition as a data object** (Option B) because:

1. **Open-closed**: Adding AU GIR or NZ GFR means creating a new
   `ReportDefinition` instance in `definitions.py`, not modifying builder logic.
2. **Structured hierarchy**: `SectionSpec` models express parent-child
   relationships, conditionality (`condition_flag`), tables (`TableSpec`), and
   heading levels in a single tree structure.
3. **Convention-aware**: The `heading_case` field makes company-specific
   conventions data rather than branching logic.
4. **Validated**: `SkeletonConfig` flags are validated against the definition's
   `condition_flags` list, catching typos at construction time.
5. **Testable**: Each definition is a frozen Pydantic model that can be asserted
   on directly and used in parametrised tests.
6. **Migration path**: If definitions grow numerous, the Pydantic model
   serialises naturally to YAML/JSON (Option C) or database records (Option D)
   without changing the builder interface.

Phase 0-3 deliberately ships only `NZ_GIR` to avoid speculative generalisation.
The architecture supports growth without requiring it now.

## Consequences

**Positive**:

- Builder functions are parameterised by `ReportDefinition` and never hard-code
  section names, ordering, or heading conventions.
- Adding a new report type or jurisdiction is an additive change (new definition
  file), not a modification to existing code.
- The `condition_flags` mechanism validates `SkeletonConfig` inputs against what
  a given report type actually supports, preventing invalid flag combinations.
- Heading case, section ordering, and table schemas are all data-driven,
  reducing the surface area for bugs when conventions differ.

**Negative**:

- The `ReportDefinition` model is richer than a simple constants file -- more
  upfront modelling effort for the first (and currently only) report type.
- Risk of over-generalisation: if the `SectionSpec` model proves too rigid for
  some future report type, it may need restructuring. Mitigated by starting
  with one concrete instance and adapting the model to real needs.
- Developers must learn the `SectionSpec` tree structure to define new report
  types. Mitigated by the `NZ_GIR` definition serving as a reference example.

## References

- ADR-001: Single Source of Truth — foundational SSOT principle; this ADR records the authoritative location for report section structures and heading conventions
- [python-docx documentation](https://python-docx.readthedocs.io/)
- [Pydantic frozen models](https://docs.pydantic.dev/latest/concepts/models/#frozen)
- ADR-002: DOCX Generation Engine Selection and Facade Abstraction
