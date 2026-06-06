# Implementation Plan: GIR Skeleton Generator (Phases 0-3)

**Date**: 2026-04-12 (revised 2026-06-05) | **Spec**: [spec.md](spec.md)
**Status**: Draft (revised)

## Summary

Building `build_skeleton()` — a Python function that accepts a `ReportStructure` value object
(ordered section headings), a `ProjectMetadata` value object, and an output path, then produces
a structurally correct DOCX file. No LLM involved. Four phases, each ending with working code
the founder can review.

| Phase | Goal | Deliverable |
| --- | --- | --- |
| 0 | Value objects | `ProjectMetadata` Pydantic model (fields confirmed with Graeme) |
| 1 | Function contract | `build_skeleton()` signature + failing tests (TDD) |
| 2 | Section generation | DOCX with correct headings from `list[str]` |
| 3 | Metadata table | Deferred — pending Graeme design session on required fields and table placement |

## Technical Context

**Language**: Python 3.14
**Package manager**: uv
**Testing**: pytest (TDD; behavior-focused, equivalence classes, protocol-conforming fakes)
**Project layout**: Monorepo — sibling packages under `src/`
**Architecture**: New `marker` package under `src/`. Internal layers: `domain/` (models, protocols) and `functions/` (builders, facade impl).
**Dev OS**: Windows | **Deploy OS**: Linux
**Domain modeling**: Pydantic BaseModel (frozen)
**Layer enforcement**: import-linter contracts in `pyproject.toml`
**Key dependencies**: python-docx (DOCX generation), pydantic (value objects)

## Function Signature

```python
def build_skeleton(
    structure: ReportStructure,
    metadata: ProjectMetadata,
    output_path: Path,
) -> None:
    ...
```

- `structure` — `ReportStructure` value object wrapping an ordered, non-empty sequence of `SectionHeading` items. Each `SectionHeading` wraps a heading string. No hierarchy in Phases 0-3; extensible to carry level/flags later without changing this signature.
- `metadata` — typed value object. Required fields TBD with Graeme. Starting set: `project_number`, `client_name`, `site_address`, `date`.
- `output_path` — where to write the `.docx` file.
- Returns `None` on success. Raises on failure (see Error Handling Policy below).

**Design principle:** core function signatures use named value objects, not raw collections. `list[str]` → `ReportStructure`; plain string fields that carry domain meaning (e.g. site address) are candidates for typed value objects in future phases.

## Error Handling Policy (pending ADR)

**Decision: raise exceptions (punitive).** Functions return `None` on success; raise on failure.

| Failure type | Exception |
| --- | --- |
| Invalid input (empty sections, missing required metadata field) | `ValueError` |
| File I/O failure (unwritable path, missing directory) | `OSError` |
| Internal build failure | `SkeletonError` (thin domain base, subclasses as needed) |

Rationale: Pythonic (EAFP); consistent with python-docx's own API; forces caller to handle failures; full stack trace on failure. Forgiving returns (None/False) are easy to ignore and lose context. See ADR to be written.

## Design Decisions

| # | Decision | Choice | Rationale |
| --- | --- | --- | --- |
| D1 | Package location | New `src/marker/` sibling package | Different bounded context (document generation vs. geotechnical analysis). |
| D2 | Internal layer structure | `domain/` (models, protocols) and `functions/` (builders, facade impl) | Matches project convention. Facade protocol in domain layer, implementation in functions layer. |
| D3 | Sections input type | `ReportStructure` wrapping `list[SectionHeading]` | Named value object at the API boundary. Wrapping a `list[str]` in `SectionHeading`/`ReportStructure` now keeps the signature stable as the domain model evolves (hierarchy, flags, validation). Thin wrappers now; extensible without a breaking change. Principle: core APIs prefer value objects over raw collections. (Graeme design session 2026-06-05 confirmed `ReportStructure` as the right domain term.) |
| D4 | Metadata input type | `ProjectMetadata` (frozen Pydantic model) | Typed, validated, immutable. Fields confirmed with Graeme before Phase 0 ships. |
| D5 | DOCX engine access | `DocumentFacade` protocol (ADR-002) | Keeps builder independent of engine. `PythonDocxFacade` is the concrete implementation. Allows future engine swap (e.g. internal fork) without changing builder code. |
| D6 | Template handling | Optional `Path` to `.docx`; default to blank `Document()`. Styles-only strategy: clear content, keep styles. | python-docx cannot open `.dotx` natively (ADR-002). |
| D7 | Facade boundary | `DocumentFacade` accepts only primitive types (`str`, `int`, `list[str]`). No Pydantic models cross the boundary. | Builder layer translates domain objects into facade calls. Keeps facade reusable. |
| D8 | Error handling | Raise, don't return sentinel. `None` on success. | See Error Handling Policy above. |
| D9 | NZ GIR section tree | Deferred. `list[str]` decouples the builder from the report definition. | Start simple. The geotechnical-specific section tree, conditional flags, and sequential renumbering are a later phase after the builder is validated. |

## Architecture

```text
     ReportStructure + ProjectMetadata + Path
                    |
                    v
       +---------------------------+
       |   build_skeleton()        |  <-- marker.functions.builders
       +---------------------------+
            |              |
            v              v
  build_sections()   build_metadata()   (Phase 2 / Phase 3)
            |              |
            | primitives only (str, int, list)
            v
       +---------------------------+
       |   DocumentFacade          |  <-- marker.domain.protocols
       |   (Protocol)              |
       +---------------------------+
                    |
                    v
       +---------------------------+
       |   PythonDocxFacade        |  <-- marker.functions.engines
       +---------------------------+
                    |
                    v
               .docx file
```

## Layer Rules

```text
marker/
    domain/             lowest — models, protocols
        protocols.py    DocumentFacade protocol
        models.py       ProjectMetadata (Phase 0)
    functions/          highest — builders, facade implementations
        engines.py      PythonDocxFacade
        builders.py     build_skeleton, build_sections, build_metadata
```

## Import-Linter Contracts

```toml
[[tool.importlinter.contracts]]
name = "marker layers"
type = "layers"
layers = ["functions", "domain"]
containers = ["marker"]
exhaustive = true

[[tool.importlinter.contracts]]
name = "marker independence"
type = "independence"
modules = ["marker", "rl"]
```

## Phased Delivery

### Phase 0: Value Objects

**Goal**: Define `SectionHeading`, `ReportStructure`, and `ProjectMetadata`. Consult Graeme for `ProjectMetadata` required fields before finalising. Starting set: `project_number`, `client_name`, `site_address`, `date`.

**Deliverables**:

1. `src/marker/__init__.py`
2. `src/marker/py.typed`
3. `src/marker/domain/__init__.py`
4. `src/marker/domain/models.py` — `SectionHeading`, `ReportStructure`, `ProjectMetadata` (all frozen Pydantic)
5. `tests/marker/__init__.py`, `tests/marker/domain/__init__.py`
6. `tests/marker/domain/test_models.py` — validation tests for all three value objects
7. Updated `pyproject.toml` — pydantic dependency, marker package, import-linter contracts

`SectionHeading`: frozen Pydantic, single `heading: str` field, validates non-empty/non-whitespace.
`ReportStructure`: frozen Pydantic, `sections: tuple[SectionHeading, ...]`, validates non-empty, no duplicate headings.

**Acceptance Gate**:

- [x] `SectionHeading` rejects empty/whitespace strings
- [x] `ReportStructure` rejects empty section list and duplicate headings
- [x] `ProjectMetadata` is instantiable with valid fields
- [x] `ProjectMetadata` raises `ValidationError` on missing required fields
- [x] `.venv\Scripts\activate; python -m pytest tests/marker/ -v` — all green

---

### Phase 1: Function Contract + Tests

**Goal**: Establish `DocumentFacade` protocol, `PythonDocxFacade` implementation, and `build_skeleton()` signature with failing tests. TDD: tests exist and fail before implementation.

**Deliverables**:

1. `src/marker/domain/protocols.py` — `DocumentFacade` protocol
2. `src/marker/functions/__init__.py`
3. `src/marker/functions/engines.py` — `PythonDocxFacade`
4. `src/marker/functions/builders.py` — `build_skeleton()` stub (signature only, raises `NotImplementedError`)
5. `tests/marker/functions/__init__.py`
6. `tests/marker/conftest.py` — `RecordingFacade` (protocol-conforming fake, not a mock)
7. `tests/marker/functions/test_engines.py` — `PythonDocxFacade` tests
8. `tests/marker/functions/test_builders.py` — failing `build_skeleton()` contract tests

**Acceptance Gate**:

- [x] `PythonDocxFacade` produces a valid DOCX with headings and a table (use `tmp_path`)
- [x] `build_skeleton()` tests exist and fail (Red phase confirmed)
- [x] `.venv\Scripts\activate; python -m pytest tests/marker/ -v` — engine tests green, builder tests red (expected)

---

### Phase 2: Section Generation

**Goal**: Implement `build_skeleton()` to produce a DOCX with sections from `list[str]`.
All sections rendered as level-1 headings in order. No conditional logic yet.

**Deliverables**:

1. Updated `src/marker/functions/builders.py` — full `build_skeleton()` and `build_sections()` implementation
2. Updated `tests/marker/functions/test_builders.py` — tests now green

**Test strategy** (equivalence classes):

- Happy path: `["Introduction", "Methodology", "Conclusion"]` → DOCX with three headings in order
- Empty list: `[]` → raises `ValueError`
- Single section: `["Executive Summary"]` → DOCX with one heading
- Sections with special characters → headings rendered as provided (no transformation)

**Verification**:

```shell
.venv\Scripts\activate; python -m pytest tests/marker/ -v
```

**Acceptance Gate**:

- [x] All builder tests green
- [x] DOCX opened with python-docx shows headings in correct order
- [x] `.venv\Scripts\activate; python -m pytest tests/marker/ -v` — all green

---

### Phase 3: Metadata Table

**Status**: Deferred — requires two design inputs before work begins:

1. **Graeme design session**: Which fields are required in the metadata table? What is the canonical order?
2. **Table placement decision**: Where does the metadata table live in the document? (Document Control block, cover page, or both?)

When unblocked, this phase adds `build_metadata(metadata, facade)` and integrates it into `build_skeleton()`.

---

### Phase Z: Polish

After all preceding phases pass:

- Run full project test suite: `.venv\Scripts\activate; python -m pytest -v`
- Ruff format: `.venv\Scripts\activate; python -m ruff format src/marker/ tests/marker/`
- Full static checks: `.venv\Scripts\activate; python -m ruff check src/; python -m importlinter; python -m deptry src/`
- Update `docs/architecture/domain-model.md`: add marker bounded context, new domain terms
- Write ADR for error handling policy (raise vs. return)

## Library Notes

### python-docx

- Import: `from docx import Document`
- `.dotx` files cannot be opened natively — use a `.docx` copy of the template
- `add_heading(text, level)` — level 0 = Title style, level 1-9 = Heading N
- `add_table(rows, cols)` — first row is data, not header by default
- Table styles: names with spaces removed, e.g. `'LightShading-Accent1'`
- No native TOC generation
- Confirmed pattern:

  ```python
  doc = Document()
  doc.add_heading("Introduction", level=1)
  doc.save("output.docx")
  ```

### pydantic

- Import: `from pydantic import BaseModel`
- `model_validator(mode="after")` returns `self`
- Frozen models:

  ```python
  class ProjectMetadata(BaseModel, frozen=True):
      project_number: str
      client_name: str
      site_address: str
      date: datetime.date
  ```

## Risk Register

| Risk | Mitigation |
| --- | --- |
| Graeme design session delayed, blocking Phase 3 | Phases 0-2 are independent; Phase 3 is explicitly gated on that session |
| `list[str]` too simple when NZ GIR section tree needs hierarchy | Architecture supports evolution to `list[tuple[str, int]]`; facade boundary isolates the change |
| python-docx heading levels don't map to corporate template styles | Facade encapsulates style mapping; test with real template when available |
| `marker` package name conflicts with a PyPI package | Internal monorepo; rename only if extracting to PyPI later |
| Pydantic version mismatch between marker and rl | Single `pyproject.toml` — no divergence possible in monorepo |

## Glossary

| Term | Definition |
| --- | --- |
| Skeleton | A structurally complete but content-empty report document |
| DocumentFacade | Protocol abstracting DOCX engine operations. Accepts only primitive types |
| ProjectMetadata | Frozen Pydantic value object carrying project-level fields |
| SectionHeading | Thin value object wrapping a single heading string. Extensible to carry level/flags in future phases |
| ReportStructure | Ordered, non-empty value object wrapping `tuple[SectionHeading, ...]`. The resolved section list passed to `build_skeleton()` |
| Mandatory section | Always present regardless of project scope |
| Conditional section | Deferred — included or excluded based on project flags (future phase) |
| GIRTemplate | Future policy object encoding standard section sets per investigation type and jurisdiction. Produces a `ReportStructure` |
