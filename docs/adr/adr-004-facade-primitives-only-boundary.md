# ADR-004: DocumentFacade Primitives-Only Boundary

## Summary

`DocumentFacade` method signatures accept only primitive types — `str`, `int`, `list[str]`, `list[list[str]]` — and no domain objects cross the facade boundary (accepted 2026-04-12). The builder layer is responsible for translating `ReportDefinition`, `SectionSpec`, and other domain types into facade primitive calls before passing them across. The hard constraint: no Pydantic model, enum, or value object may appear in a `DocumentFacade` method signature; if it does, the facade is coupled to the domain and cannot be reused or tested independently.

## Decision

The `DocumentFacade` protocol accepts only primitive types (`str`, `int`,
`list[str]`, `list[list[str]]`) as method parameters. No Pydantic models,
domain value objects, or enums cross the facade boundary. The builder layer
is responsible for translating domain objects into facade calls.

## Status

Accepted -- 2026-04-12

## Context

ADR-002 established the `DocumentFacade` protocol as the abstraction boundary
between skeleton builder logic and the DOCX generation engine. The protocol
defines methods like `add_heading(text, level)`, `add_table(headers, rows)`,
and `save(path)`.

The question is: what types should these methods accept?

The builder operates on domain models (`ReportDefinition`, `SectionSpec`,
`SkeletonConfig`, `ProjectMetadata`). The facade operates on document
primitives (strings to write, integers for heading levels, lists for table
data). If domain types leak into the facade signature, the facade becomes
coupled to the domain model and cannot be reused or tested independently.

This decision clarifies the boundary that ADR-002 implied but did not
explicitly state.

## Options Considered

### Option A: Domain-aware facade

Facade methods accept domain objects directly:

```python
class DocumentFacade(Protocol):
    def add_section(self, spec: SectionSpec) -> None: ...
    def add_metadata(self, meta: ProjectMetadata) -> None: ...
```

**Rejected because**:

- Couples the facade protocol to `marker.domain.models`, making it impossible
  to use the facade in a context that does not have the domain package.
- Facade implementations must import and understand domain models, violating
  the layered architecture (engines should not depend on domain).
- Adding a new domain model field forces facade interface changes even when the
  document output is unchanged.
- Multiple facade implementations (production, test stub, future Quarto-based)
  all must understand domain types.

### Option B: Primitives-only facade (chosen)

Facade methods accept only built-in types:

```python
class DocumentFacade(Protocol):
    def add_heading(self, text: str, *, level: int) -> None: ...
    def add_table(
        self, headers: list[str], rows: list[list[str]], *,
        style: str | None = None,
    ) -> None: ...
    def save(self, path: str) -> None: ...
```

The builder translates domain objects:

```python
def build_sections(
    definition: ReportDefinition,
    config: SkeletonConfig,
    facade: DocumentFacade,
) -> None:
    for section in definition.body_sections:
        if section.mandatory or config.is_enabled(section.condition_flag):
            facade.add_heading(section.heading, level=section.level)
```

### Option C: DTO layer between domain and facade

Introduce intermediate data transfer objects that the builder creates and the
facade consumes.

**Rejected because**:

- Primitives already serve as the DTO. Adding a formal DTO layer creates
  another mapping step without meaningful benefit.
- The facade's method signatures are already a contract; wrapping them in
  dedicated DTOs adds boilerplate without added safety.

## Decision Rationale

**Primitives-only** (Option B) because:

1. **Independence**: The facade protocol has zero imports from `marker.domain`.
   It can be defined in its own module and implemented by any engine without
   pulling in domain dependencies.
2. **Testability**: A `RecordingFacade` test stub records `(method, args)`
   tuples of primitives. Tests assert on strings and integers, not on domain
   model serialisation.
3. **Stability**: Facade methods change only when the document structure
   changes (new element types), not when domain models evolve (new fields on
   `ProjectMetadata`, new attributes on `SectionSpec`).
4. **Composability**: Future engines (Quarto, document-builder) implement the
   same primitive interface without knowing about the domain layer.
5. **Clarity**: The builder is the translation layer. It owns the mapping from
   domain intent to document actions. This responsibility is explicit and
   testable.

## Consequences

**Positive**:

- `marker.domain.protocols` has no dependency on `marker.domain.models` --
  clean layer separation enforced by import-linter.
- Facade implementations are engine-only code with no domain coupling.
- Test stubs are trivial: record primitive calls, assert on them.
- Adding domain model fields (e.g., a new `SectionSpec.footnote` attribute)
  requires changes only in the builder, not in the facade protocol.

**Negative**:

- The builder must manually decompose domain objects into primitive calls. This
  is deliberate (the builder is the translation layer), but it means builder
  functions grow as the domain model grows.
- Some complex document operations (e.g., nested tables, merged cells) may
  require multiple primitive calls where a single domain-aware method could be
  more expressive. Mitigated by adding targeted facade methods when a clear
  pattern emerges.

## References

- ADR-001: Single Source of Truth — foundational SSOT principle; this ADR records the authoritative location for DocumentFacade method signatures
- ADR-002: DOCX Generation Engine Selection and Facade Abstraction
- [Protocol classes (PEP 544)](https://peps.python.org/pep-0544/)
- **External validation (2026-05-22)**: Microsoft's Legal Agent in Word uses a "purpose-built insertion algorithm" and a "deterministic resolution layer" for document editing rather than relying on an LLM to generate OOXML directly -- confirming the primitives-only boundary principle independently. See the competitor profile in `docs/research/competitors/`.
