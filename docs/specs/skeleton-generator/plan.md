# Skeleton Generator — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> to implement this plan task-by-task.
> Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an incremental pipeline that ingests contractual documents (RFP, LOE) and
produces a structured Word document skeleton ready for an engineer to edit, not write from
scratch.

**Architecture:** Pure DOCX-generation first (Phases 0–3, no LLM). LLM extraction enters
only at Phase 4, against the simplest possible input. Each phase produces a DOCX artifact
that can be opened in Word and self-validated in under a minute.

**Tech Stack:** `python-docx`, `pydantic`, `pytest`. LLM client (Phase 4+): TBD.

---

## MoSCoW scope for this plan

| Category | Scope |
|---|---|
| **Must Have** | Phases 0–3: DOCX generation, mandatory structure, empty tables, conditional toggle, static metadata |
| **Should Have** | Phase 4: First LLM step — metadata extraction from a real PDF |
| **Could Have** | Phase 5: Traceability matrix. Phase 6: Client Summary draft |
| **Won't Have** | Standards registry integration, Canterbury-specific sections, GFR skeleton, feedback mechanism |

Phases 4+ are **outlined** at the end of this plan. They will be fully task-decomposed after
Phases 0–3 are complete and validated.

---

## File Structure

```
src/rl/skeleton/
    __init__.py         # Public exports: build_skeleton
    builder.py          # Orchestrates the full DOCX build from config + metadata
    config.py           # SectionConfig: boolean flags for conditional sections
    metadata.py         # ProjectMetadata: typed fields extracted from RFP/LOE
    tables.py           # Table builders: document_control_table, geotech_model_table
tests/skeleton/
    __init__.py
    test_builder.py     # Integration: open DOCX, assert headings and tables present
    test_config.py      # Unit: SectionConfig flag behaviour
    test_tables.py      # Unit: table column headers
```

---

## Phase 0 — Bootstrap: prove you can write any DOCX from Python

**New question answered:** Can I install python-docx and save a file that Word can open?

**Self-validation:** The file opens in Word without errors.

---

### Task 0.1: Add python-docx dependency

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Add the dependency**

```powershell
.\.venv\Scripts\activate; uv add python-docx
```

Expected output: `Added python-docx ...` and `pyproject.toml` updated.

- [ ] **Step 2: Verify import works**

```powershell
.\.venv\Scripts\activate; python -c "import docx; print('ok')"
```

Expected: `ok`

- [ ] **Step 3: Commit**

```powershell
git add pyproject.toml uv.lock; git commit -m "deps: add python-docx"
```

---

### Task 0.2: Write a Hello World DOCX with no template

**Files:**
- Create: `src/rl/skeleton/__init__.py`
- Create: `src/rl/skeleton/builder.py`
- Create: `tests/skeleton/__init__.py`
- Create: `tests/skeleton/test_builder.py`

- [ ] **Step 1: Write the failing test**

`tests/skeleton/test_builder.py`:

```python
from pathlib import Path
import docx
from rl.skeleton import build_skeleton


def test_build_skeleton_creates_a_docx_file(tmp_path: Path) -> None:
    output = tmp_path / "skeleton.docx"
    build_skeleton(output_path=output)
    assert output.exists()
    doc = docx.Document(str(output))
    assert doc is not None
```

- [ ] **Step 2: Run test to verify it fails**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/test_builder.py -v
```

Expected: `FAILED` — `ImportError: cannot import name 'build_skeleton'`

- [ ] **Step 3: Write minimal implementation**

`src/rl/skeleton/__init__.py`:

```python
from rl.skeleton.builder import build_skeleton

__all__ = ["build_skeleton"]
```

`src/rl/skeleton/builder.py`:

```python
from pathlib import Path
import docx


def build_skeleton(output_path: Path) -> None:
    doc = docx.Document()
    doc.add_paragraph("Hello World")
    doc.save(str(output_path))
```

- [ ] **Step 4: Run test to verify it passes**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/test_builder.py -v
```

Expected: `PASSED`

- [ ] **Step 5: Open the file in Word manually and confirm it opens**

```powershell
.\.venv\Scripts\activate; python -c "
from pathlib import Path
from rl.skeleton import build_skeleton
build_skeleton(Path('output/hello.docx'))
print('Written to output/hello.docx')
"
```

Open `output/hello.docx` in Word. Confirm it opens without repair prompts.

- [ ] **Step 6: Commit**

```powershell
git add src/rl/skeleton/ tests/skeleton/; git commit -m "feat(skeleton): hello world DOCX generation"
```

---

## Phase 1 — Mandatory structure: headings and empty tables (no LLM)

**New questions answered:**
- Can I insert headings at the right hierarchy and order?
- Can I insert empty tables with the right column headers?

**Self-validation:** Open the DOCX. The headings appear in this exact order at the right
level. The tables have the specified columns.

---

### Task 1.1: Define mandatory sections as a data structure

**Files:**
- Create: `src/rl/skeleton/config.py`
- Create: `tests/skeleton/test_config.py`

- [ ] **Step 1: Write the failing test**

`tests/skeleton/test_config.py`:

```python
from rl.skeleton.config import SectionConfig, mandatory_sections


def test_mandatory_sections_are_defined() -> None:
    sections = mandatory_sections()
    titles = [s.title for s in sections]
    assert "Introduction" in titles
    assert "Assessment and Interpretation of Site Conditions" in titles
    assert "Residual Geotechnical Risk" in titles
    assert "Further Work" in titles
    assert "Applicability" in titles


def test_mandatory_sections_have_correct_levels() -> None:
    sections = mandatory_sections()
    intro = next(s for s in sections if s.title == "Introduction")
    assert intro.level == 1
    scope = next(s for s in sections if s.title == "Scope of Work")
    assert scope.level == 2
```

- [ ] **Step 2: Run test to verify it fails**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/test_config.py -v
```

Expected: `FAILED` — `ImportError`

- [ ] **Step 3: Write the implementation**

`src/rl/skeleton/config.py`:

```python
from dataclasses import dataclass, field


@dataclass(frozen=True)
class SectionConfig:
    title: str
    level: int  # 1 = Heading 1, 2 = Heading 2, 3 = Heading 3


@dataclass
class SkeletonConfig:
    slope_stability: bool = False
    fault_rupture: bool = False
    liquefaction: bool = True   # mandatory by default for NZ sites
    ground_improvement: bool = False
    foundation_assessment: bool = False


def mandatory_sections() -> list[SectionConfig]:
    return [
        SectionConfig("Introduction", 1),
        SectionConfig("Scope of Work", 2),
        SectionConfig("Site Description", 2),
        SectionConfig("Proposed Development", 2),
        SectionConfig("Assessment and Interpretation of Site Conditions", 1),
        SectionConfig("Ground and Groundwater Conditions", 2),
        SectionConfig("Geology", 3),
        SectionConfig("Previous Investigations", 3),
        SectionConfig("Current Investigations", 3),
        SectionConfig("Geotechnical Model", 3),
        SectionConfig("Groundwater", 3),
        SectionConfig("Seismic Hazard", 2),
        SectionConfig("Seismic Site Subsoil Class", 3),
        SectionConfig("Ground Shaking Hazard", 3),
        SectionConfig("Liquefaction Assessment", 2),
        SectionConfig("Residual Geotechnical Risk", 1),
        SectionConfig("Further Work", 1),
        SectionConfig("Applicability", 1),
    ]
```

- [ ] **Step 4: Run test to verify it passes**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/test_config.py -v
```

Expected: `PASSED`

- [ ] **Step 5: Commit**

```powershell
git add src/rl/skeleton/config.py tests/skeleton/test_config.py
git commit -m "feat(skeleton): define mandatory section structure"
```

---

### Task 1.2: Insert mandatory headings into the DOCX

**Files:**
- Modify: `src/rl/skeleton/builder.py`
- Modify: `tests/skeleton/test_builder.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/skeleton/test_builder.py`:

```python
def test_mandatory_headings_are_present(tmp_path: Path) -> None:
    output = tmp_path / "skeleton.docx"
    build_skeleton(output_path=output)
    doc = docx.Document(str(output))
    headings = [
        p.text for p in doc.paragraphs if p.style.name.startswith("Heading")
    ]
    assert "Introduction" in headings
    assert "Assessment and Interpretation of Site Conditions" in headings
    assert "Residual Geotechnical Risk" in headings
    assert "Applicability" in headings


def test_mandatory_heading_levels_are_correct(tmp_path: Path) -> None:
    output = tmp_path / "skeleton.docx"
    build_skeleton(output_path=output)
    doc = docx.Document(str(output))
    heading_map = {
        p.text: p.style.name
        for p in doc.paragraphs
        if p.style.name.startswith("Heading")
    }
    assert heading_map.get("Introduction") == "Heading 1"
    assert heading_map.get("Scope of Work") == "Heading 2"
    assert heading_map.get("Geology") == "Heading 3"
```

- [ ] **Step 2: Run test to verify it fails**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/test_builder.py::test_mandatory_headings_are_present -v
```

Expected: `FAILED` — headings not found

- [ ] **Step 3: Update the builder**

`src/rl/skeleton/builder.py`:

```python
from pathlib import Path
import docx
from rl.skeleton.config import SkeletonConfig, mandatory_sections


def build_skeleton(
    output_path: Path,
    config: SkeletonConfig | None = None,
) -> None:
    if config is None:
        config = SkeletonConfig()
    doc = docx.Document()
    _insert_mandatory_headings(doc)
    doc.save(str(output_path))


def _insert_mandatory_headings(doc: docx.Document) -> None:
    for section in mandatory_sections():
        doc.add_heading(section.title, level=section.level)
```

- [ ] **Step 4: Run tests to verify they pass**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/test_builder.py -v
```

Expected: all `PASSED`

- [ ] **Step 5: Open in Word and verify visually**

```powershell
.\.venv\Scripts\activate; python -c "
from pathlib import Path
from rl.skeleton import build_skeleton
build_skeleton(Path('output/headings.docx'))
print('Written to output/headings.docx')
"
```

Open `output/headings.docx`. Confirm:
- All mandatory section names are present
- Introduction = large heading, Scope of Work = smaller, Geology = smaller still

- [ ] **Step 6: Commit**

```powershell
git add src/rl/skeleton/builder.py tests/skeleton/test_builder.py
git commit -m "feat(skeleton): insert mandatory headings at correct hierarchy"
```

---

### Task 1.3: Insert mandatory empty tables

**Files:**
- Create: `src/rl/skeleton/tables.py`
- Create: `tests/skeleton/test_tables.py`
- Modify: `src/rl/skeleton/builder.py`
- Modify: `tests/skeleton/test_builder.py`

- [ ] **Step 1: Write the failing tests**

`tests/skeleton/test_tables.py`:

```python
import docx
from pathlib import Path
from rl.skeleton.tables import document_control_table, geotech_model_table


def test_document_control_table_has_correct_columns(tmp_path: Path) -> None:
    doc = docx.Document()
    document_control_table(doc)
    table = doc.tables[0]
    headers = [cell.text for cell in table.rows[0].cells]
    assert headers == [
        "Date", "Version", "Description",
        "Prepared by", "Reviewed by", "Authorised by",
    ]


def test_geotech_model_table_has_correct_columns(tmp_path: Path) -> None:
    doc = docx.Document()
    geotech_model_table(doc)
    table = doc.tables[0]
    headers = [cell.text for cell in table.rows[0].cells]
    assert headers == [
        "Layer / Unit", "Description", "Depth (m)",
        "RL (m)", "Thickness (m)", "Typical Test Values",
    ]
```

- [ ] **Step 2: Run tests to verify they fail**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/test_tables.py -v
```

Expected: `FAILED` — `ImportError`

- [ ] **Step 3: Write the tables module**

`src/rl/skeleton/tables.py`:

```python
import docx


_DOCUMENT_CONTROL_HEADERS = [
    "Date", "Version", "Description",
    "Prepared by", "Reviewed by", "Authorised by",
]

_GEOTECH_MODEL_HEADERS = [
    "Layer / Unit", "Description", "Depth (m)",
    "RL (m)", "Thickness (m)", "Typical Test Values",
]


def document_control_table(doc: docx.Document) -> docx.table.Table:
    return _add_header_table(doc, _DOCUMENT_CONTROL_HEADERS)


def geotech_model_table(doc: docx.Document) -> docx.table.Table:
    return _add_header_table(doc, _GEOTECH_MODEL_HEADERS)


def _add_header_table(doc: docx.Document, headers: list[str]) -> docx.table.Table:
    table = doc.add_table(rows=1, cols=len(headers))
    for i, header in enumerate(headers):
        table.rows[0].cells[i].text = header
    return table
```

- [ ] **Step 4: Run tests to verify they pass**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/test_tables.py -v
```

Expected: `PASSED`

- [ ] **Step 5: Wire tables into the builder**

Update the `_insert_mandatory_headings` call order in `builder.py` so that the Document Control table is inserted at the top, and the Geotechnical Model table is inserted after the "Geotechnical Model" heading:

```python
from rl.skeleton.tables import document_control_table, geotech_model_table


def build_skeleton(
    output_path: Path,
    config: SkeletonConfig | None = None,
) -> None:
    if config is None:
        config = SkeletonConfig()
    doc = docx.Document()
    document_control_table(doc)
    _insert_mandatory_headings(doc, config)
    doc.save(str(output_path))


def _insert_mandatory_headings(doc: docx.Document, config: SkeletonConfig) -> None:
    for section in mandatory_sections():
        doc.add_heading(section.title, level=section.level)
        if section.title == "Geotechnical Model":
            geotech_model_table(doc)
```

- [ ] **Step 6: Add integration test for table presence in full skeleton**

Add to `tests/skeleton/test_builder.py`:

```python
def test_skeleton_contains_document_control_table(tmp_path: Path) -> None:
    output = tmp_path / "skeleton.docx"
    build_skeleton(output_path=output)
    doc = docx.Document(str(output))
    assert len(doc.tables) >= 2  # document control + geotech model


def test_skeleton_document_control_table_headers(tmp_path: Path) -> None:
    output = tmp_path / "skeleton.docx"
    build_skeleton(output_path=output)
    doc = docx.Document(str(output))
    headers = [cell.text for cell in doc.tables[0].rows[0].cells]
    assert "Prepared by" in headers
    assert "Authorised by" in headers
```

- [ ] **Step 7: Run all skeleton tests**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/ -v
```

Expected: all `PASSED`

- [ ] **Step 8: Open in Word and verify tables visually**

```powershell
.\.venv\Scripts\activate; python -c "
from pathlib import Path
from rl.skeleton import build_skeleton
build_skeleton(Path('output/with_tables.docx'))
print('Written to output/with_tables.docx')
"
```

Open `output/with_tables.docx`. Confirm:
- First element is a 6-column table with header row (Date, Version, ...)
- "Geotechnical Model" heading is followed immediately by a 6-column table

- [ ] **Step 9: Commit**

```powershell
git add src/rl/skeleton/tables.py tests/skeleton/test_tables.py src/rl/skeleton/builder.py tests/skeleton/test_builder.py
git commit -m "feat(skeleton): insert mandatory empty tables"
```

---

## Phase 2 — Conditional section toggling (no LLM)

**New question answered:** Can I include or exclude a heading based on a boolean flag, and
verify the toggle works?

**Self-validation:** Set `slope_stability=True` → heading appears in DOCX. Set `False` →
heading absent. Verifiable by opening the file or running a test.

---

### Task 2.1: Wire SkeletonConfig flags to conditional heading insertion

**Files:**
- Modify: `src/rl/skeleton/config.py`
- Modify: `src/rl/skeleton/builder.py`
- Modify: `tests/skeleton/test_builder.py`

- [ ] **Step 1: Write the failing tests**

Add to `tests/skeleton/test_builder.py`:

```python
def test_slope_stability_heading_absent_by_default(tmp_path: Path) -> None:
    output = tmp_path / "skeleton.docx"
    build_skeleton(output_path=output)
    doc = docx.Document(str(output))
    headings = [p.text for p in doc.paragraphs if p.style.name.startswith("Heading")]
    assert "Slope Stability" not in headings


def test_slope_stability_heading_present_when_enabled(tmp_path: Path) -> None:
    from rl.skeleton.config import SkeletonConfig
    output = tmp_path / "skeleton.docx"
    build_skeleton(output_path=output, config=SkeletonConfig(slope_stability=True))
    doc = docx.Document(str(output))
    headings = [p.text for p in doc.paragraphs if p.style.name.startswith("Heading")]
    assert "Slope Stability" in headings


def test_foundation_assessment_absent_by_default(tmp_path: Path) -> None:
    output = tmp_path / "skeleton.docx"
    build_skeleton(output_path=output)
    doc = docx.Document(str(output))
    headings = [p.text for p in doc.paragraphs if p.style.name.startswith("Heading")]
    assert "Foundation Assessment" not in headings
```

- [ ] **Step 2: Run tests to verify they fail**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/test_builder.py::test_slope_stability_heading_present_when_enabled -v
```

Expected: `FAILED`

- [ ] **Step 3: Add conditional sections to config.py**

Add to `src/rl/skeleton/config.py`:

```python
def conditional_sections(config: SkeletonConfig) -> list[SectionConfig]:
    sections = []
    if config.slope_stability:
        sections.append(SectionConfig("Slope Stability", 3))
    if config.fault_rupture:
        sections.append(SectionConfig("Fault Rupture Hazard", 3))
    if config.foundation_assessment:
        sections.append(SectionConfig("Foundation Assessment", 1))
        sections.append(SectionConfig("Foundation Options", 2))
        sections.append(SectionConfig("Foundation Design Parameters", 2))
        if config.ground_improvement:
            sections.append(SectionConfig("Ground Improvement", 2))
    return sections
```

- [ ] **Step 4: Update builder to insert conditional sections**

In `builder.py`, after the mandatory headings loop, add:

```python
from rl.skeleton.config import SkeletonConfig, mandatory_sections, conditional_sections


def _insert_mandatory_headings(doc: docx.Document, config: SkeletonConfig) -> None:
    for section in mandatory_sections():
        doc.add_heading(section.title, level=section.level)
        if section.title == "Geotechnical Model":
            geotech_model_table(doc)
        if section.title == "Liquefaction Assessment":
            for cond in conditional_sections(config):
                doc.add_heading(cond.title, level=cond.level)
```

- [ ] **Step 5: Run all tests**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/ -v
```

Expected: all `PASSED`

- [ ] **Step 6: Open in Word and verify toggle visually**

```powershell
.\.venv\Scripts\activate; python -c "
from pathlib import Path
from rl.skeleton import build_skeleton
from rl.skeleton.config import SkeletonConfig
build_skeleton(Path('output/with_slope.docx'), config=SkeletonConfig(slope_stability=True))
build_skeleton(Path('output/without_slope.docx'))
print('Done')
"
```

Open both files. Confirm "Slope Stability" appears in one and not the other.

- [ ] **Step 7: Commit**

```powershell
git add src/rl/skeleton/config.py src/rl/skeleton/builder.py tests/skeleton/test_builder.py
git commit -m "feat(skeleton): conditional section toggling via SkeletonConfig flags"
```

---

## Phase 3 — Static metadata injection (no LLM)

**New question answered:** Can I populate named placeholders in the DOCX from a Python dict?

**Self-validation:** Project name, number, and address appear in the document in the
expected locations. Verifiable by opening the file.

---

### Task 3.1: Define ProjectMetadata model

**Files:**
- Create: `src/rl/skeleton/metadata.py`
- Create: `tests/skeleton/test_metadata.py`

- [ ] **Step 1: Write the failing test**

`tests/skeleton/test_metadata.py`:

```python
from rl.skeleton.metadata import ProjectMetadata


def test_project_metadata_has_required_fields() -> None:
    meta = ProjectMetadata(
        project_number="12345",
        client_name="Acme Corp",
        site_address="1 Main Street, Christchurch",
        report_date="April 2026",
    )
    assert meta.project_number == "12345"
    assert meta.document_name == "12345-RPT-GT-001"


def test_document_name_follows_naming_convention() -> None:
    meta = ProjectMetadata(
        project_number="98765",
        client_name="Test Client",
        site_address="10 Test Road",
        report_date="January 2026",
    )
    assert meta.document_name.startswith("98765-RPT-GT-")
```

- [ ] **Step 2: Run to verify failure**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/test_metadata.py -v
```

Expected: `FAILED` — `ImportError`

- [ ] **Step 3: Write the metadata model**

`src/rl/skeleton/metadata.py`:

```python
from pydantic import BaseModel, computed_field


class ProjectMetadata(BaseModel):
    project_number: str
    client_name: str
    site_address: str
    report_date: str
    sequence: str = "001"

    @computed_field
    @property
    def document_name(self) -> str:
        return f"{self.project_number}-RPT-GT-{self.sequence}"
```

- [ ] **Step 4: Run to verify pass**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/test_metadata.py -v
```

Expected: `PASSED`

- [ ] **Step 5: Add pydantic dependency**

```powershell
.\.venv\Scripts\activate; uv add pydantic
```

- [ ] **Step 6: Commit**

```powershell
git add src/rl/skeleton/metadata.py tests/skeleton/test_metadata.py pyproject.toml uv.lock
git commit -m "feat(skeleton): ProjectMetadata model with document naming convention"
```

---

### Task 3.2: Inject metadata into the DOCX

**Files:**
- Modify: `src/rl/skeleton/builder.py`
- Modify: `tests/skeleton/test_builder.py`

- [ ] **Step 1: Write the failing test**

Add to `tests/skeleton/test_builder.py`:

```python
from rl.skeleton.metadata import ProjectMetadata


def test_metadata_appears_in_document(tmp_path: Path) -> None:
    output = tmp_path / "skeleton.docx"
    meta = ProjectMetadata(
        project_number="12345",
        client_name="Acme Corp",
        site_address="1 Main Street",
        report_date="April 2026",
    )
    build_skeleton(output_path=output, metadata=meta)
    doc = docx.Document(str(output))
    full_text = "\n".join(p.text for p in doc.paragraphs)
    assert "12345" in full_text
    assert "Acme Corp" in full_text
    assert "1 Main Street" in full_text
```

- [ ] **Step 2: Run to verify failure**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/test_builder.py::test_metadata_appears_in_document -v
```

Expected: `FAILED`

- [ ] **Step 3: Update build_skeleton signature and inject metadata**

```python
from rl.skeleton.metadata import ProjectMetadata


def build_skeleton(
    output_path: Path,
    config: SkeletonConfig | None = None,
    metadata: ProjectMetadata | None = None,
) -> None:
    if config is None:
        config = SkeletonConfig()
    doc = docx.Document()
    if metadata:
        _insert_metadata_block(doc, metadata)
    document_control_table(doc)
    _insert_mandatory_headings(doc, config)
    doc.save(str(output_path))


def _insert_metadata_block(doc: docx.Document, metadata: ProjectMetadata) -> None:
    doc.add_paragraph(f"Project: {metadata.project_number}")
    doc.add_paragraph(f"Client: {metadata.client_name}")
    doc.add_paragraph(f"Site: {metadata.site_address}")
    doc.add_paragraph(f"Date: {metadata.report_date}")
    doc.add_paragraph(f"Document: {metadata.document_name}")
```

- [ ] **Step 4: Run all tests**

```powershell
.\.venv\Scripts\activate; python -m pytest tests/skeleton/ -v
```

Expected: all `PASSED`

- [ ] **Step 5: Open in Word and verify**

```powershell
.\.venv\Scripts\activate; python -c "
from pathlib import Path
from rl.skeleton import build_skeleton
from rl.skeleton.metadata import ProjectMetadata
meta = ProjectMetadata(
    project_number='12345',
    client_name='Acme Corp',
    site_address='1 Main Street, Christchurch',
    report_date='April 2026',
)
build_skeleton(Path('output/with_metadata.docx'), metadata=meta)
print('Written to output/with_metadata.docx')
"
```

Open `output/with_metadata.docx`. Confirm project number, client name, and site address
are visible in the document.

- [ ] **Step 6: Commit**

```powershell
git add src/rl/skeleton/builder.py tests/skeleton/test_builder.py
git commit -m "feat(skeleton): inject project metadata into DOCX"
```

---

## Phase 4 — First LLM step: extract metadata from a real PDF (outline)

> **Status:** Not yet task-decomposed. Begin after Phase 3 is complete and
> self-validated.

**New question answered:** Can an LLM reliably extract project number, client name, and
site address from a real RFP PDF, and does the output match what I can verify by eye?

**Input:** A single clean PDF (one RFP you have on hand). No ambiguous documents yet.

**Rabbit holes to avoid:**
- Do not use a scanned PDF for the first test — use a text-based PDF.
- Do not attempt multi-document extraction in this phase. One document, one call.
- Do not validate with an SME. Read the PDF yourself and compare the extracted values.

**Won't Have in Phase 4:** MSG/EML parsing, multi-document merging,
confidence scoring.

**Tasks to plan when ready:**
1. Choose and set up LLM client (OpenAI or Anthropic SDK)
2. Build a PDF text extractor (pdfplumber or pypdf)
3. Write an extraction prompt that returns structured JSON
4. Bind extracted JSON to `ProjectMetadata`
5. Run against one known RFP; verify by hand in 60 seconds

---

## Phase 5 — Traceability matrix (outline)

> **Status:** Not yet task-decomposed. Begin after Phase 4 is complete.

**New question answered:** Can the LLM parse deliverables from an LOE and map them to
report sections?

---

## Phase 6 — Client Summary draft (outline)

> **Status:** Not yet task-decomposed. Begin after Phase 5 is complete.

**New question answered:** Can the LLM produce a one-page Client Summary in plain
language from RFP/LOE content?
