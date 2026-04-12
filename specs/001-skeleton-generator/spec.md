# Feature Specification: GIR Skeleton Generator (Phases 0-3)

**Branch**: `feature/map-doc-writing-process`
**Created**: 2026-04-12
**Status**: Draft

## Source Document Reconciliation

| Source | Authority | Status |
| --- | --- | --- |
| [skeleton-generator.md](../../docs/concepts/01-skeleton-generator/skeleton-generator.md) | Primary -- concept doc | Updated with canonical headings |
| [ADR-001](../../docs/adr/adr-001-docx-generation-engine-facade.md) | Binding -- facade pattern | No conflicts |
| [20260411-gir-skeleton-acceptance-criteria.md](../../docs/research/20260411-gir-skeleton-acceptance-criteria.md) | Supporting -- AC research | Integrated into concept doc ACs |
| [20260411-gir-skeleton-section-placeholders.md](../../docs/research/20260411-gir-skeleton-section-placeholders.md) | Supporting -- section content | Referenced for Phase 8 (deferred) |
| [incumbent-process.md](../../docs/concepts/01-skeleton-generator/incumbent-process.md) | Supporting -- current process | Heading discrepancies resolved |

### Resolved Conflicts

| Item | Concept doc (before) | Canonical source | Resolution |
| --- | --- | --- | --- |
| Section 2.1.1 heading | "Geology" | "Geology and faulting" | Updated concept doc |
| Section 2.1.2 heading | "Previous Investigations" | "Previous geotechnical investigations" | Updated concept doc |
| Section 2.1.3 heading | "Current Investigations" | "Current geotechnical investigations" | Updated concept doc |
| Section 2.2 heading | "Seismic Hazard" | "Seismic shaking hazard" | Updated concept doc |
| Appendix B name | "Previous Investigations" | "Previous ground investigation results" | Updated concept doc |
| Appendix C name | "Investigation Logs" | "Current geotechnical investigation logs" | Updated concept doc |
| Heading case | Title Case in places | Sentence case throughout | Updated concept doc |
| Section numbering gaps | Sections 4/5/6 hard-coded | Sequential renumbering when conditionals excluded | Updated concept doc |
| Slope stability heading | "Slope Stability" | "Slope stability assessment" | Updated concept doc |
| Fault rupture heading | "Fault Rupture Hazard" | "Fault rupture hazard assessment" | Updated concept doc |
| Section 3.2 heading | "Foundation Design Parameters" | "Foundation pile design parameters" | Updated concept doc |

## Scope

This spec covers **Phases 0-3 only** of the skeleton generator concept (Steps 0-3 in the
concept doc). These phases use pure DOCX generation with no LLM -- they produce a
structurally correct document from deterministic rules and metadata extraction.

Phases 4-8 (LLM-powered extraction, standards mapping, placeholder injection) are
deferred to a subsequent spec.

## Scenarios (mandatory)

### Scenario 1 -- Generate mandatory GIR section structure

An automation engineer runs the skeleton generator with a mock template and default flags.
The system produces a DOCX file with all mandatory GIR sections in the correct order,
using canonical sentence-case headings and sequential numbering. The Geotechnical Model
Table in Section 2.1.4 is present as an empty table with the six mandatory column headers.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 5     | 3              | 90             | 5                    | 27.0       |

**Independent test**: Open the generated DOCX in Word and verify all mandatory headings
are present, correctly numbered, and in sentence case.

**Acceptance criteria**:

1. **Given** a default configuration with no conditional flags enabled,
   **When** the skeleton is generated,
   **Then** the DOCX contains all mandatory sections (Document control through Appendix D)
   in the canonical order, with sequential numbering (no gaps), and no conditional sections.
2. **Given** a default configuration,
   **When** the skeleton is generated,
   **Then** Section 2.1.4 contains an empty table with headers: Layer/Unit, Description,
   Depth, RL, Thickness, Typical Test Values.
3. **Given** a default configuration,
   **When** the skeleton is generated,
   **Then** all headings use sentence case (only first word and proper nouns capitalised).

---

### Scenario 2 -- Conditional section inclusion and exclusion

An automation engineer generates a skeleton with various combinations of conditional flags
(`foundation_assessment`, `slope_stability`, `fault_rupture`, `ground_improvement`). The
system includes or excludes sections based on the flags and renumbers remaining sections
sequentially.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 5     | 2.5            | 85             | 4                    | 26.6       |

**Independent test**: Generate skeletons with several flag combinations and verify section
presence/absence and numbering.

**Acceptance criteria**:

1. **Given** `foundation_assessment=True`,
   **When** the skeleton is generated,
   **Then** Section 3 ("Foundation assessment") with subsections 3.1 and 3.2 is present,
   and Residual geotechnical risk, Further work, and Applicability are numbered 4, 5, 6.
2. **Given** `foundation_assessment=False`,
   **When** the skeleton is generated,
   **Then** Section 3 is absent, and the sections after Section 2 are numbered 3, 4, 5
   (Residual geotechnical risk, Further work, Applicability).
3. **Given** `slope_stability=True` and `fault_rupture=False`,
   **When** the skeleton is generated,
   **Then** Section 2.4 is present with heading "Slope stability assessment"
   (no parent "Other geotechnical hazards" wrapper when only one child).
4. **Given** `slope_stability=True` and `fault_rupture=True`,
   **When** the skeleton is generated,
   **Then** Section 2.4 has heading "Other geotechnical hazards" with subsections
   2.4.1 "Slope stability assessment" and 2.4.2 "Fault rupture hazard assessment".
5. **Given** `ground_improvement=True` and `foundation_assessment=False`,
   **When** the skeleton is generated,
   **Then** no ground improvement section appears (ground_improvement is ignored when
   foundation_assessment is False).
6. **Given** `ground_improvement=True` and `foundation_assessment=True`,
   **When** the skeleton is generated,
   **Then** a ground improvement subsection appears within Section 3.

---

### Scenario 3 -- Document facade abstraction

The skeleton builder accepts any `DocumentFacade` implementation. Tests use a recording
stub to verify the correct sequence of facade calls without producing a real DOCX.
Production code uses `PythonDocxFacade`.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 3     | 2              | 95             | 3                    | 19.0       |

**Independent test**: Run the skeleton builder with a `RecordingFacade` stub and assert
the call sequence matches expectations.

**Acceptance criteria**:

1. **Given** a `RecordingFacade` stub,
   **When** the skeleton builder runs with default configuration,
   **Then** the recorded calls include `add_heading` for every mandatory section
   and `add_table` for the Geotechnical Model Table and Document Control table.
2. **Given** a `PythonDocxFacade` with no template,
   **When** the skeleton builder runs,
   **Then** a valid DOCX file is produced that can be opened by python-docx's `Document()`.

---

### Scenario 4 -- Project metadata population

An automation engineer provides a `ProjectMetadata` configuration object (project number,
client name, site address, date, document code). The skeleton populates the Document
Control block and cover page metadata from this object.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 5     | 2              | 80             | 3                    | 26.7       |

**Independent test**: Generate a skeleton with metadata, reopen with python-docx, and
verify the metadata values appear in the document text.

**Acceptance criteria**:

1. **Given** a `ProjectMetadata` with project_number="1001234.1", client_name="Acme Ltd",
   **When** the skeleton is generated,
   **Then** the Document Control section contains the project number and client name.
2. **Given** a `ProjectMetadata` with all fields populated,
   **When** the skeleton is generated,
   **Then** the document naming follows the convention `[JobNo]-RPT-GT-[Element]-[Seq]`.

---

### Edge Cases

- What happens when all conditional flags are False? Only mandatory sections appear.
- What happens when `ground_improvement=True` but `foundation_assessment=False`? Ground
  improvement is silently ignored (documented behaviour).
- What happens when `slope_stability=True` is the only hazard? The parent heading
  "Other geotechnical hazards" is replaced by the specific hazard heading.
- What happens when no template path is provided? A blank Document is created (no styles).
- What happens when an invalid heading level is requested? python-docx raises ValueError
  for levels outside 0-9 (handled by the facade).

## Requirements (mandatory)

### Functional Requirements

- **FR-001**: System MUST generate a DOCX file with all mandatory GIR sections in the
  canonical order using sentence-case headings. (Addresses AC2, AC11.)
- **FR-002**: System MUST include or exclude conditional sections based on boolean flags
  and renumber remaining sections sequentially. (Addresses AC3.)
- **FR-003**: System MUST insert an empty Geotechnical Model Table in Section 2.1.4 with
  six mandatory column headers. (Addresses AC4.)
- **FR-004**: System MUST insert a Document Control version table with six mandatory
  columns (Date, Version, Description, Prepared by, Reviewed by, Authorised by).
  (Addresses AC2.)
- **FR-005**: System MUST populate project metadata (project number, client name, site
  address, date, document code) from a typed configuration object. (Addresses AC5.)
- **FR-006**: System MUST access the DOCX engine exclusively through the `DocumentFacade`
  protocol defined in ADR-001. (Addresses architectural constraint.)
- **FR-007**: System MUST use a `.docx` copy of the company template when one is provided,
  or create a blank document when none is provided. (Addresses AC14.)
- **FR-008**: System MUST insert empty appendix headings (A through D) in the standard
  order. (Addresses AC13.)

### Key Entities (if data is involved)

- **SkeletonConfig**: Configuration object controlling which sections to include.
  Key attributes: `foundation_assessment` (bool), `slope_stability` (bool),
  `fault_rupture` (bool), `ground_improvement` (bool).
- **ProjectMetadata**: Data object for project-level metadata. Key attributes:
  `project_number` (str), `client_name` (str), `site_address` (str), `date` (date),
  `document_code` (str).
- **DocumentFacade**: Protocol for DOCX engine abstraction (from ADR-001).
  Key methods: `add_heading`, `add_paragraph`, `add_table`, `add_metadata_block`, `save`.
- **PythonDocxFacade**: Concrete implementation of `DocumentFacade` using python-docx.

## Success Criteria (mandatory)

- **SC-001**: A DOCX generated with default config passes automated heading-order
  validation against the canonical section list.
- **SC-002**: All 16 flag combinations (4 boolean flags) produce structurally valid,
  sequentially numbered DOCX files.
- **SC-003**: The skeleton builder can be tested entirely with a recording stub --
  no DOCX engine required for unit tests.

## Assumptions

- The company Word template is not available yet. The initial implementation uses a blank
  `Document()` or a mock `.docx` file. Real template integration is deferred. If the
  template introduces style names that conflict with python-docx defaults, the facade
  implementation will need updating.
- Section 1.1 (Scope of work) is always included by default. The concept doc resolved
  this open question explicitly.
- Liquefaction assessment (Section 2.3) is always included for NZ sites. It is treated
  as mandatory, not conditional.
- Steps 4-8 of the concept doc (LLM extraction, standards mapping, placeholders) are
  out of scope for this spec and will be covered in a future iteration.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| python-docx heading styles don't match corporate template styles | Generated headings render without formatting in the real template | Facade encapsulates style mapping; test with real template early |
| Sequential renumbering logic has off-by-one errors with nested conditionals | Incorrectly numbered sections undermine trust | Exhaustive flag-combination tests (16 combinations) |
| DocumentFacade protocol grows too large as features are added | Facade becomes a leaky abstraction | Keep facade minimal; add methods only when needed by a concrete scenario |
| Template `.dotx` format not supported by python-docx | Cannot use the corporate template directly | ADR-001 documents this: use a `.docx` copy of the template |
