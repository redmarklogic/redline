# Implementation Plan: GIR Skeleton Generator (Phases 0-3)

**Date**: 2026-04-12 | **Spec**: [spec.md](spec.md)
**Status**: Draft

## Summary

We are building the first four incremental delivery steps (Steps 0-3) of the GIR Skeleton
Generator: a deterministic Python pipeline that produces a structurally correct Word
document (.docx) from typed configuration objects. No LLM is involved in these phases.
The output is a DOCX file with all mandatory GIR (Geotechnical Interpretive Report)
sections, conditional section logic, empty structured tables, and project metadata -- ready
for an engineer to open and start editing.

The skeleton generator lives in a new `marker` sibling package under `src/`, accessed
through a `DocumentFacade` protocol (per ADR-001). The `marker` package handles all DOCX
generation concerns, while the `rl` hub package will later orchestrate it alongside other
tools.

## Technical Context

**Language**: Python 3.12
**Package manager**: uv
**Testing**: pytest (TDD workflow per `test-driven-development` skill)
**Project layout**: Monorepo (from `.specify/architecture.yml`)
**Architecture**: Sibling packages under `src/`: `rl` (hub, existing), `marker` (new --
DOCX generation). Each package applies its own internal layers: domain > functions.
**Dev OS**: Windows | **Deploy OS**: Linux
**Domain modeling**: Pydantic BaseModel for configuration objects
**Layer enforcement**: import-linter contracts in `pyproject.toml`
**Key dependencies**: python-docx (DOCX generation), pydantic (configuration models)

## Concept-to-Plan Phase Mapping

| Concept Step | Concept Name | Plan Phase | Notes |
| --- | --- | --- | --- |
| Step 0 | Template ingestion | Phase 0 | Foundation: facade protocol + python-docx implementation |
| Step 1 | Mandatory sections | Phase 1 | Section structure, conditional logic, tables |
| Step 2 | Project metadata | Phase 2 | Metadata model and population |
| Step 3 | Traceability matrix | Deferred | Requires LLM-based RFP/LOE parsing (out of scope for this spec) |

Note: Concept Step 3 (Traceability matrix) is deferred because it requires parsing
RFP/LOE documents to extract deliverables, which is an LLM task. The plan covers
Steps 0-2 in full and adds a "skeleton builder orchestrator" phase that wires the
pieces together.

## Design Decisions

| # | Decision | Choice | Rationale |
| --- | --- | --- | --- |
| D1 | Package location for skeleton generator | New `src/marker/` sibling package | Different bounded context (document generation vs. geotechnical analysis); changes at different rate; may graduate to standalone package. Supported by modularity research. |
| D2 | Internal layer structure for `marker` | `domain/` (models, protocols) and `functions/` (builders, facade impl) | Matches the project's existing layer convention. Keeps facade protocol in domain layer, implementation in functions layer. |
| D3 | Section numbering approach | Dynamic numbering at generation time | Sections are assigned numbers sequentially based on which conditionals are enabled, rather than using hard-coded numbers. Eliminates gap risk. |
| D4 | Conditional section representation | Boolean flags on a frozen Pydantic model | Simple, explicit, testable. Each flag maps to one conditional section group. Interaction rules (e.g., ground_improvement requires foundation_assessment) are validated in the model. |
| D5 | Heading text source | Canonical strings defined as constants in domain layer | Single source of truth for heading names. Prevents typos and ensures sentence case. |
| D6 | Template handling | Accept optional Path to `.docx` file; default to blank Document() | python-docx cannot open `.dotx` natively (ADR-001). Template integration is deferred to when a real template is available. |

## Domain Impact

**Modularity assessment**: New top-level package `src/marker/`. Signals from the decision
matrix: different bounded context (document generation vs. geotechnical analysis), different
rate of change (document format changes independently of analysis logic), potential future
extraction to standalone package, no shared domain objects with `rl`. The modularity
research document (20260412-modularity-vs-layering.md) strongly supports this choice.

**New packages**: `marker` -- new sibling package under `src/`.

**Bounded context changes**: New "Document Generation" bounded context alongside existing
"Geotechnical Analysis" context.

**Import-linter contract updates**:

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

**Subdomain classification**: Supporting -- template-driven output, no custom domain model
beyond configuration objects. Simpler patterns: thin domain layer with value objects and a
protocol, functions layer with builders.

**New domain terms**:

| Term | Definition |
| --- | --- |
| Skeleton | A structurally complete but content-empty GIR document with headings, tables, and metadata |
| DocumentFacade | Protocol abstracting DOCX engine operations (add_heading, add_table, save) |
| SkeletonConfig | Configuration object controlling which GIR sections to include |
| ProjectMetadata | Data object carrying project-level information (number, client, address, date) |
| Conditional section | A GIR section included or excluded based on project scope flags |
| Sequential renumbering | Assigning section numbers at generation time to avoid gaps when conditionals are excluded |

## Architecture

```
                  SkeletonConfig + ProjectMetadata
                           |
                           v
              +------------------------+
              |   build_skeleton()     |  <-- marker.functions.builders
              |   (orchestrator)       |
              +------------------------+
                   |            |
                   v            v
    +------------------+  +-------------------+
    | build_sections() |  | build_metadata()  |
    | (section logic)  |  | (metadata logic)  |
    +------------------+  +-------------------+
                   |            |
                   v            v
              +------------------------+
              |   DocumentFacade       |  <-- marker.domain.protocols
              |   (Protocol)           |
              +------------------------+
                        |
                        v
              +------------------------+
              |  PythonDocxFacade      |  <-- marker.functions.engines
              |  (python-docx impl)   |
              +------------------------+
                        |
                        v
                    .docx file
```

### Data flow

1. Caller creates `SkeletonConfig` (section flags) and `ProjectMetadata` (project info).
2. `build_skeleton(config, metadata, facade)` orchestrates the generation.
3. Section builder reads config flags, computes the ordered section list with dynamic
   numbering, and calls `facade.add_heading()` / `facade.add_table()` for each.
4. Metadata builder populates the Document Control block and cover page info.
5. `facade.save(path)` writes the DOCX file.

### Layer rules

```
marker/
    domain/         (lowest -- models, protocols, constants)
        protocols.py    DocumentFacade protocol
        models.py       SkeletonConfig, ProjectMetadata (frozen Pydantic)
        constants.py    Canonical heading strings, table headers
    functions/      (highest -- builders, facade implementations)
        engines.py      PythonDocxFacade
        builders.py     build_skeleton, build_sections, build_metadata
```

## Domain Models

### `marker.domain.models.SkeletonConfig`

```python
# src/marker/domain/models.py
from pydantic import BaseModel, model_validator

class SkeletonConfig(BaseModel, frozen=True):
    """Controls which GIR sections to include in the skeleton."""

    foundation_assessment: bool = False
    slope_stability: bool = False
    fault_rupture: bool = False
    ground_improvement: bool = False

    @model_validator(mode="after")
    def ground_improvement_requires_foundation(self) -> "SkeletonConfig":
        if self.ground_improvement and not self.foundation_assessment:
            msg = "ground_improvement requires foundation_assessment=True"
            raise ValueError(msg)
        return self
```

### `marker.domain.models.ProjectMetadata`

```python
# src/marker/domain/models.py
import datetime

class ProjectMetadata(BaseModel, frozen=True):
    """Project-level metadata for the skeleton."""

    project_number: str
    client_name: str
    site_address: str
    date: datetime.date
    document_code: str  # e.g., "1001234.1-RPT-GT-NRT-001"
```

### `marker.domain.protocols.DocumentFacade`

```python
# src/marker/domain/protocols.py
from typing import Protocol

class DocumentFacade(Protocol):
    """Uniform interface for DOCX generation engines (ADR-001)."""

    def add_heading(self, text: str, *, level: int) -> None: ...
    def add_paragraph(self, text: str, *, style: str | None = None) -> None: ...
    def add_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        *,
        style: str | None = None,
    ) -> None: ...
    def add_metadata_block(self, label: str, value: str) -> None: ...
    def save(self, path: str) -> None: ...
```

## MoSCoW

| Category | Items |
| --- | --- |
| **Must have** | DocumentFacade protocol and PythonDocxFacade implementation; SkeletonConfig and ProjectMetadata models with validation; all mandatory GIR sections with canonical headings; conditional section inclusion/exclusion with sequential renumbering; empty Geotechnical Model Table and Document Control table; metadata population in Document Control block |
| **Should have** | Version table with six mandatory columns pre-formatted; appendix headings in correct order |
| **Could have** | Distribution matrix placeholder in Document Control |
| **Won't have (this time)** | Real company template integration (mock only); LLM-based RFP/LOE parsing; traceability matrix generation; standards references per section; placeholder question injection; executive summary / client summary content; formatting compliance (font, sizes) beyond heading structure |

## Phased Delivery

### Phase 0: Foundation -- DocumentFacade and PythonDocxFacade

**Goal**: Establish the `marker` package with domain models, the `DocumentFacade` protocol,
and a working `PythonDocxFacade` implementation that can create a minimal DOCX file.

**TDD approach**: Write tests for `PythonDocxFacade` methods (`add_heading`, `add_paragraph`,
`add_table`, `save`) in `tests/marker/functions/test_engines.py`. Write tests for
`SkeletonConfig` validation in `tests/marker/domain/test_models.py`.

**Deliverables**:

1. `src/marker/__init__.py` -- package marker
2. `src/marker/py.typed` -- PEP 561 marker
3. `src/marker/domain/__init__.py`
4. `src/marker/domain/protocols.py` -- `DocumentFacade` protocol
5. `src/marker/domain/models.py` -- `SkeletonConfig`, `ProjectMetadata`
6. `src/marker/domain/constants.py` -- canonical heading strings, table headers
7. `src/marker/functions/__init__.py`
8. `src/marker/functions/engines.py` -- `PythonDocxFacade`
9. `tests/marker/__init__.py`, `tests/marker/domain/__init__.py`, `tests/marker/functions/__init__.py`
10. `tests/marker/domain/test_models.py` -- SkeletonConfig validation tests
11. `tests/marker/functions/test_engines.py` -- PythonDocxFacade tests
12. Updated `pyproject.toml` -- add python-docx dependency, marker to wheel packages,
    import-linter contracts

**Verification**:

```
.venv\Scripts\activate; python -m pytest tests/marker/ -v
```

**Acceptance Gate** (both must pass before Phase 1 starts):
- [ ] Working code: PythonDocxFacade produces a valid DOCX with headings and tables
- [ ] Run `.venv\Scripts\activate; python -m pytest tests/marker/ -v` -- all tests green

---

### Phase 1: Mandatory and Conditional GIR Sections

**Goal**: Build the section generation logic that takes a `SkeletonConfig` and calls the
facade to produce all mandatory sections with correct headings, plus conditional sections
based on flags, with sequential renumbering.

**TDD approach**: Write tests for section builder functions in
`tests/marker/functions/test_builders.py` using a `RecordingFacade` stub.
Test all 16 flag combinations for correct section ordering and numbering.

**Deliverables**:

1. `src/marker/functions/builders.py` -- `build_sections(config, facade)` and
   `build_tables(facade)` functions
2. `tests/marker/functions/test_builders.py` -- section builder tests with RecordingFacade
3. `tests/marker/conftest.py` -- `RecordingFacade` fixture

**Verification**:

```
.venv\Scripts\activate; python -m pytest tests/marker/functions/test_builders.py -v
```

**Acceptance Gate** (both must pass before Phase 2 starts):
- [ ] Working code: all 16 flag combinations produce correctly ordered, sequentially
  numbered sections
- [ ] Run `.venv\Scripts\activate; python -m pytest tests/marker/ -v` -- all tests green

---

### Phase 2: Project Metadata Population

**Goal**: Build the metadata population logic that takes a `ProjectMetadata` object and
populates the Document Control block (version table, metadata fields) in the skeleton.

**TDD approach**: Write tests for `build_metadata(metadata, facade)` in
`tests/marker/functions/test_builders.py` using `RecordingFacade`.

**Deliverables**:

1. Updated `src/marker/functions/builders.py` -- add `build_metadata(metadata, facade)`
2. Updated `tests/marker/functions/test_builders.py` -- metadata builder tests

**Verification**:

```
.venv\Scripts\activate; python -m pytest tests/marker/functions/test_builders.py -v
```

**Acceptance Gate** (both must pass before Phase 3 starts):
- [ ] Working code: Document Control block contains project metadata values
- [ ] Run `.venv\Scripts\activate; python -m pytest tests/marker/ -v` -- all tests green

---

### Phase 3: Orchestrator and End-to-End Validation

**Goal**: Wire the section builder, metadata builder, and facade together into a single
`build_skeleton()` entry point. Produce a complete DOCX file end-to-end and validate it
by reopening with python-docx.

**TDD approach**: Write integration tests in `tests/marker/test_integration.py` that
generate a real DOCX, reopen it, and assert on heading text and table structure.

**Deliverables**:

1. Updated `src/marker/functions/builders.py` -- add `build_skeleton(config, metadata, facade, path)` orchestrator
2. `tests/marker/test_integration.py` -- end-to-end DOCX generation and validation

**Verification**:

```
.venv\Scripts\activate; python -m pytest tests/marker/ -v
```

**Acceptance Gate** (both must pass before declaring this iteration complete):
- [ ] Working code: end-to-end skeleton generation produces a valid DOCX with correct
  sections, tables, and metadata
- [ ] Run `.venv\Scripts\activate; python -m pytest tests/marker/ -v` -- all tests green
- [ ] Run `.venv\Scripts\activate; python -m ruff check src/marker/` -- no lint errors

## File Inventory

| Phase | New Files | Count |
| --- | --- | --- |
| 0 | `src/marker/__init__.py`, `src/marker/py.typed`, `src/marker/domain/__init__.py`, `src/marker/domain/protocols.py`, `src/marker/domain/models.py`, `src/marker/domain/constants.py`, `src/marker/functions/__init__.py`, `src/marker/functions/engines.py`, `tests/marker/__init__.py`, `tests/marker/domain/__init__.py`, `tests/marker/domain/test_models.py`, `tests/marker/functions/__init__.py`, `tests/marker/functions/test_engines.py` | 13 |
| 1 | `src/marker/functions/builders.py`, `tests/marker/functions/test_builders.py`, `tests/marker/conftest.py` | 3 |
| 2 | (updates only -- no new files) | 0 |
| 3 | `tests/marker/test_integration.py` | 1 |

**Total new**: ~17 | **Total deleted**: 0

## Library Best Practices

### python-docx

- **Import path**: `from docx import Document` (not `from python_docx`)
- **API gotchas**:
  - `.dotx` files cannot be opened natively; use a `.docx` copy of the template
  - `add_heading(text, level)` -- level 0 = "Title" style, level 1-9 = "Heading N"
  - `add_table(rows, cols)` creates a table; first row is data, not header by default
  - Table styles use names with spaces removed: `'LightShading-Accent1'`
  - No native TOC generation; requires Word to refresh fields
  - No comment-range API (comments cannot be added to text ranges)
- **Confirmed pattern**: Create document, add headings/paragraphs/tables, save:
  ```python
  doc = Document()
  doc.add_heading("Introduction", level=1)
  doc.add_paragraph("Content here.", style="Body Text")
  table = doc.add_table(rows=1, cols=3)
  table.rows[0].cells[0].text = "Header 1"
  doc.save("output.docx")
  ```

### pydantic

- **Import path**: `from pydantic import BaseModel`
- **API gotchas**: `model_validator(mode="after")` returns `self`, not a dict
- **Confirmed pattern**: Frozen models with validation:
  ```python
  class Config(BaseModel, frozen=True):
      flag: bool = False

      @model_validator(mode="after")
      def validate_flags(self) -> "Config":
          ...
          return self
  ```

## Risk Register

| Risk | Mitigation |
| --- | --- |
| python-docx heading levels don't map to corporate template styles | Facade encapsulates style mapping; test with real template when available |
| Sequential renumbering has edge cases with nested conditionals under Section 2.4 | Exhaustive flag-combination tests cover all 16 combinations |
| `marker` package name conflicts with an existing PyPI package | No conflict found; name is internal to the monorepo. If extracting later, rename. |
| Pydantic version mismatch between marker and rl packages | Both use the same dependency from pyproject.toml; no version divergence possible in monorepo |

## Glossary

| Term | Definition |
| --- | --- |
| GIR | Geotechnical Interpretive Report -- the primary engineering deliverable interpreting ground conditions and providing design recommendations |
| Skeleton | A structurally complete but content-empty GIR document with headings, empty tables, and project metadata |
| DocumentFacade | Protocol abstracting DOCX engine operations so the engine can be swapped without changing business logic |
| Mandatory section | A GIR section that is always present regardless of project scope (e.g., Introduction, Seismic shaking hazard) |
| Conditional section | A GIR section included or excluded based on boolean flags tied to project scope |
| Sequential renumbering | Assigning section numbers dynamically at generation time so excluded sections don't leave gaps |
| Sentence case | Capitalisation rule: only the first word and proper nouns are capitalised (enterprise standard for all headings) |
| Front matter | Document sections before the main numbered body: Document control, Table of contents, Client summary |
| Applicability | Legal boilerplate section containing mandatory liability clauses |
| LOE | Letter of Engagement -- the binding contract between the engineering firm and the client |
| RFP | Request for Proposal -- the client's formal invitation defining project requirements |
