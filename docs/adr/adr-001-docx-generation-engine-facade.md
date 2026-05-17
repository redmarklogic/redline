# ADR-001: DOCX Generation Engine Selection and Facade Abstraction

## Summary

python-docx is the accepted initial engine for skeleton DOCX generation, accessed exclusively through a `DocumentFacade` protocol (accepted 2026-04-12). The facade ensures no application code ever imports python-docx directly, keeping the engine swappable or composable with ONLYOFFICE document-builder and Quarto without touching business logic. The hard constraint: any code that reaches a python-docx type outside the facade implementation violates this ADR.

## Decision

Use python-docx as the initial DOCX generation engine for the skeleton generator,
accessed exclusively through a `DocumentFacade` protocol. All application code
interacts with the facade, never with python-docx directly. This allows swapping
or composing engines (python-docx, ONLYOFFICE document-builder, Quarto) without
propagating changes into the codebase.

## Status

Accepted -- 2026-04-12

## Context

The skeleton generator needs to produce structured DOCX files from typed Python
configuration objects. Three DOCX generation approaches were evaluated:

1. **python-docx** -- pure Python library for creating and editing .docx files
2. **Quarto (.qmd -> docx)** -- Pandoc-based publishing system rendering Markdown
   to DOCX
3. **ONLYOFFICE document-builder** -- Python wrapper around a C++ Office engine,
   already used in this project for comment-annotation workflows

The project already uses document-builder for a narrow but critical use case:
searching text with positional awareness and adding comments to exact ranges.
python-docx cannot replicate that capability. However, for skeleton generation
(creating documents from scratch), the requirements are different: headings,
tables, metadata blocks, and conditional sections.

Additionally, we anticipate that over time:

- The generation engine may change (e.g., adopting Quarto for narrative sections,
  or document-builder for pixel-perfect output with corporate templates).
- Multiple engines may coexist (python-docx for creation, document-builder for
  post-processing/commenting).
- Engine-specific quirks (OOXML repair, opaque error handling) should be
  encapsulated rather than leaked into business logic.

A facade pattern isolates the application from engine specifics, making the
choice reversible and engines composable.

## Options Considered

### Option A: python-docx (chosen for initial engine)

Pure Python, MIT-licensed, `pip install python-docx`. Creates and reads .docx
files with a Pythonic, typed API.

**Strengths**:

- Structural read/write -- can traverse paragraphs, runs, tables, styles
- MIT license -- no copyleft concerns
- Small footprint, pip-installable, no native dependencies
- Excellent testability -- generate in-memory, reload, assert on structure
- IDE autocomplete, type hints

**Weaknesses**:

- No comment-range API (cannot add comments to text ranges)
- No native .dotx support (must use .docx copy of template)
- No built-in TOC generation (requires Word to refresh fields)
- Table formatting is manual

### Option B: Quarto (.qmd -> docx)

Pandoc-based publishing. Markdown input, DOCX output via `quarto render`.
Supports `reference-doc` for template styling.

**Strengths**:

- Readable Markdown source, auto TOC and numbering
- Native template support via `reference-doc`
- Multi-format output (PDF, HTML, DOCX)

**Weaknesses**:

- One-way renderer -- cannot read or edit existing DOCX
- Requires Quarto CLI (system binary, not pip-installable)
- Limited table formatting from Markdown
- Wrong tool class: publishing system, not programmatic document construction
- Testing requires rendering then parsing output with another library

**Verdict**: Complementary tool for narrative-heavy generation (e.g., Client
Summary in Phase 6), not a replacement for programmatic construction. Could
be introduced behind the facade later.

### Option C: ONLYOFFICE document-builder

Python wrapper around C++ Office engine. JavaScript-like DOM API via `.Call()`.
Already used in this project.

**Strengths (confirmed from project usage)**:

- Pixel-perfect DOCX output, full rendering engine
- Rich API surface: charts, lists, tables, comments, images
- PyPI wheel (`pip install document-builder`, ~61-99 MB)
- Comment-range manipulation (our primary existing use case)

**Weaknesses (confirmed from project usage)**:

- AGPL-3.0 license -- requires legal analysis for distribution scenarios
- Call-string-based API (`table.Call('SetWidth', 'percent', 100)`) -- no type
  hints, no autocomplete
- Opaque error handling -- failed `.Call()` returns null `CDocBuilderValue` with
  no exception; must check `.IsNull()` manually
- OOXML output sometimes requires repair (watermark removal, comments XML
  rewriting, destructive OOXML repair pipeline)
- API fragility across versions -- method signatures change without deprecation
- "Read" capability is text-only, not structural (no paragraph/run/style traversal)
- Single-threaded in practice despite documentation claims

**Verdict**: Remains the right tool for comment-annotation workflows. Not
suitable as the skeleton generation engine due to licensing, error handling, and
OOXML repair overhead.

### Option D: Direct usage (no facade)

Use python-docx directly in builder modules. Simplest approach.

**Rejected because**:

- Couples business logic to one library's API
- Engine swap requires rewriting every call site
- Cannot compose engines (e.g., python-docx for structure + document-builder for
  post-processing) behind a uniform interface
- Engine-specific quirks (OOXML repair, error handling patterns) leak into
  business logic

## Decision Rationale

**Engine choice**: python-docx for skeleton generation. It is the only option that
provides structural read/write with a Pythonic API, MIT license, and pip-only
installation. document-builder remains in use for comment-annotation but is not
involved in skeleton generation.

**Facade pattern**: All document operations go through a `DocumentFacade` protocol
that exposes domain-meaningful methods (`add_heading`, `add_table`,
`add_metadata_block`, `save`) rather than python-docx primitives. This:

1. **Makes the engine choice reversible** -- swapping python-docx for
   document-builder or Quarto requires implementing a new facade, not rewriting
   callers.
2. **Enables engine composition** -- a future facade implementation could delegate
   heading/table creation to python-docx and post-processing to
   document-builder, behind one interface.
3. **Encapsulates engine quirks** -- OOXML repair, error handling patterns, and
   API workarounds live in the facade implementation, not in business logic.
4. **Improves testability** -- tests can use a stub facade that records calls
   without producing a real DOCX, or use the real facade and verify output.

### Facade design sketch

```python
from typing import Protocol

class DocumentFacade(Protocol):
    """Uniform interface for DOCX generation engines."""

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

```python
from docx import Document

class PythonDocxFacade:
    """DocumentFacade implementation backed by python-docx."""

    def __init__(self, template_path: str | None = None) -> None:
        self._doc = Document(template_path) if template_path else Document()

    def add_heading(self, text: str, *, level: int) -> None:
        self._doc.add_heading(text, level=level)

    def add_paragraph(self, text: str, *, style: str | None = None) -> None:
        self._doc.add_paragraph(text, style=style)

    def add_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        *,
        style: str | None = None,
    ) -> None:
        table = self._doc.add_table(rows=1, cols=len(headers))
        if style:
            table.style = style
        for i, header in enumerate(headers):
            table.rows[0].cells[i].text = header
        for row_data in rows:
            cells = table.add_row().cells
            for i, value in enumerate(row_data):
                cells[i].text = value

    def add_metadata_block(self, label: str, value: str) -> None:
        self._doc.add_paragraph(f"{label}: {value}", style="Body Text")

    def save(self, path: str) -> None:
        self._doc.save(path)
```

The `build_skeleton()` function accepts a `DocumentFacade` parameter. Production
code passes `PythonDocxFacade()`; tests can pass a recording stub or the real
implementation.

## Consequences

**Positive**:

- Engine choice is decoupled from business logic -- can be changed in one place
- Comment-annotation pipeline (document-builder) and skeleton generator
  (python-docx) coexist cleanly, each behind its own facade
- Quarto can be introduced for narrative generation later without architectural
  disruption
- Engine-specific workarounds (OOXML repair, `.IsNull()` checks) are contained
  within facade implementations
- Tests can verify skeleton structure without depending on a specific engine

**Negative**:

- One additional abstraction layer (protocol + implementation class)
- Facade methods may need to grow as document features are added (e.g., images,
  page breaks, headers/footers) -- but this growth is incremental and bounded by
  actual need
- Some python-docx power features (direct style manipulation, run-level
  formatting) are not exposed through the facade initially -- available via
  escape hatch if needed

## References

- [python-docx documentation](https://python-docx.readthedocs.io/)
- [ONLYOFFICE Document Builder API](https://api.onlyoffice.com/docs/document-builder/get-started/overview/)
- [Quarto Word output](https://quarto.org/docs/output-formats/ms-word.html)
- [Quarto Word templates](https://quarto.org/docs/output-formats/ms-word-templates.html)
