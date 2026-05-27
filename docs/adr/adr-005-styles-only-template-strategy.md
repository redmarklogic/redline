# ADR-005: Styles-Only Template Strategy with Jinja Deferral

## Summary

Company DOCX templates are treated as style sources only: all body content is cleared and the document is rebuilt from scratch using `DocumentFacade` primitives, preserving only style definitions, page layout, headers, and footers (accepted 2026-04-12). Jinja-based template rendering (`python-docx-template`) is deferred until a concrete placeholder-injection need arises beyond Phase 3. The hard constraint: the generator must never append content to an existing template body — it clears first, then builds.

## Decision

Company DOCX templates are treated as style sources only. The skeleton
generator clears all content from the template and rebuilds the document from
scratch, preserving only the template's style definitions. Jinja-based
template rendering (e.g., via `python-docx-template`) is deferred until a
concrete need for placeholder injection arises beyond Phase 3.

## Status

Accepted -- 2026-04-12

## Context

Company reports are produced from branded DOCX templates that define heading
styles, fonts, colours, page layouts, headers/footers, and watermarks. The
skeleton generator must produce output that matches the company's visual
identity.

Two concerns are in tension:

1. **Template content**: Templates may contain sample headings, placeholder
   text, or example tables that conflict with generated content. If the
   generator appends to a template, leftover content creates duplicates or
   misorderings.
2. **Template styles**: The generator must use the template's style definitions
   (Heading 1 font, Body Text spacing, Table Grid borders) so the output
   matches the company brand.

Additionally, the `python-docx-template` library (Jinja2 integration for
DOCX) is a natural candidate for placeholder injection (e.g., `{{ client_name }}`
in headers, `{% for section in sections %}` loops). However, introducing Jinja
at this stage adds complexity:

- Template syntax collisions with existing DOCX content.
- Additional dependency and learning curve.
- Phases 0-3 generate content programmatically; there is no template with
  placeholders to render.

## Options Considered

### Option A: Merge strategy

Append generated content after existing template content. Rely on the template
author to leave the body empty or mark insertion points.

**Rejected because**:

- Fragile: if the template contains any body content (sample headings, example
  sections, boilerplate paragraphs), duplicates appear in the output.
- Requires coordination with template authors to ensure the template body is
  always empty -- an implicit contract that is not version-controlled or
  validated.
- Insertion point detection (where to start appending) is heuristic and
  error-prone.

### Option B: Styles-only strategy (chosen)

Clear all body content from the loaded template `Document`, keeping only style
definitions, page layout, headers, and footers. Then build the document from
scratch using `DocumentFacade` methods.

```python
class PythonDocxFacade:
    def __init__(self, template_path: str | None = None) -> None:
        if template_path:
            self._doc = Document(template_path)
            self._clear_body()  # remove all paragraphs and tables
        else:
            self._doc = Document()

    def _clear_body(self) -> None:
        for element in list(self._doc.element.body):
            if element.tag.endswith(("p", "tbl")):
                self._doc.element.body.remove(element)
```

### Option C: Jinja templating (python-docx-template)

Use Jinja2 syntax inside DOCX templates. The template contains
`{{ project_number }}`, `{% for section in sections %}`, etc. The generator
renders the template with context data.

**Deferred (not rejected) because**:

- Phases 0-3 generate all content programmatically. There is no existing
  template with Jinja placeholders to render.
- Jinja introduces template syntax (`{{ }}`, `{% %}`) that may collide with
  existing content in company templates not designed for Jinja.
- The `DocumentFacade` protocol (ADR-002) already allows introducing a
  `JinjaDocxFacade` behind the same interface when placeholder injection is
  needed (e.g., Phase 6+ narrative sections).
- Keeping Phases 0-3 Jinja-free simplifies testing and reduces the dependency
  surface.

### Option D: .dotx template format

Use DOCX template files (.dotx) natively.

**Rejected because**:

- python-docx cannot open `.dotx` files natively (documented limitation).
- Workaround (rename `.dotx` to `.docx`) works but adds a fragile build step.
- The `.docx` copy-of-template approach is simpler and equally effective for
  style extraction.

## Decision Rationale

**Styles-only** (Option B) because:

1. **Deterministic output**: Clearing the body and rebuilding guarantees that
   the output contains exactly what the generator produced, with no leftover
   template content.
2. **Template independence**: Templates can contain any content (examples,
   instructions, sample sections) without affecting generator output. Template
   authors do not need to coordinate with the generator.
3. **Style preservation**: python-docx preserves all style definitions, page
   layout, headers, and footers when body content is removed. The generated
   document inherits the company brand automatically.
4. **Simplicity**: No Jinja dependency, no placeholder syntax, no template
   rendering step. The facade's `add_heading`/`add_paragraph` calls use named
   styles that are defined in the template.

**Jinja deferral** because:

5. **YAGNI**: Phases 0-3 do not have a use case for Jinja. Programmatic
   building via the facade is sufficient.
6. **Reversible**: The facade protocol allows introducing Jinja later without
   changing builder code. A `JinjaDocxFacade` can render a Jinja template
   and expose the same `add_heading`/`add_table` interface.
7. **Risk reduction**: Avoiding Jinja now eliminates template syntax collision
   risks and reduces the testing surface.

## Consequences

**Positive**:

- Templates are pure style sources. Any company template works without
  modification.
- No Jinja dependency in Phases 0-3. Smaller attack surface, simpler tests.
- The `_clear_body()` approach is self-contained within `PythonDocxFacade` and
  does not affect the facade protocol.
- When Jinja is needed later, it enters behind the existing facade protocol --
  no architectural disruption.

**Negative**:

- If a template has intentional body content that should be preserved (e.g.,
  a pre-written executive summary), the styles-only strategy discards it.
  Mitigated: this is not a current requirement, and a future "merge" strategy
  can be added as a facade option.
- Jinja deferral means Phase 6+ (narrative placeholder injection) will need
  its own implementation decision. Mitigated: the facade protocol already
  supports this extension point, and the decision can be made with Phase 6
  context.

## References

- ADR-001: Single Source of Truth — foundational SSOT principle; this ADR records the authoritative location for DOCX output visual formatting
- ADR-002: DOCX Generation Engine Selection and Facade Abstraction
- [python-docx template handling](https://python-docx.readthedocs.io/en/latest/user/documents.html)
- [python-docx-template (Jinja)](https://docxtpl.readthedocs.io/)
