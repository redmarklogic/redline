# Feature Specification: GIR Skeleton Generator (Phases 0-3)

**Branch**: `feature/4-gir-skeleton-generator-phases-0-3`
**Created**: 2026-04-12
**Status**: Draft

## Pre-Execution Gate (Peter)

Before Kabilan starts Phase 0, Peter produces a short go/no-go memo confirming:

- ADR-002 is still current and the facade pattern is unchanged
- No open rabbit holes in the risk register block execution
- All acceptance gates are testable as written
- No escalation-requiring dependencies (new packages, layer changes) are unresolved

This is a currency check, not a reshaping session. Peter does not rewrite specs or resequence tasks.

## Source Document Reconciliation

| Source                                                                                                          | Authority                     | Status                            |
| --------------------------------------------------------------------------------------------------------------- | ----------------------------- | --------------------------------- |
| [skeleton-generator.md](../../docs/concepts/01-skeleton-generator/skeleton-generator.md)                           | Primary -- concept doc        | Updated with canonical headings   |
| [ADR-002](../../docs/adr/adr-002-docx-generation-engine-facade.md)                                                 | Binding -- facade pattern     | No conflicts                      |
| [20260411-gir-skeleton-acceptance-criteria.md](../../docs/research/20260411-gir-skeleton-acceptance-criteria.md)   | Supporting -- AC research     | Integrated into concept doc ACs   |
| [20260411-gir-skeleton-section-placeholders.md](../../docs/research/20260411-gir-skeleton-section-placeholders.md) | Supporting -- section content | Referenced for Phase 8 (deferred) |
| [incumbent-process.md](../../docs/concepts/01-skeleton-generator/incumbent-process.md)                             | Supporting -- current process | Heading discrepancies resolved    |

### Resolved Conflicts

| Item                    | Concept doc (before)           | Canonical source                                  | Resolution          |
| ----------------------- | ------------------------------ | ------------------------------------------------- | ------------------- |
| Section 2.1.1 heading   | "Geology"                      | "Geology and faulting"                            | Updated concept doc |
| Section 2.1.2 heading   | "Previous Investigations"      | "Previous geotechnical investigations"            | Updated concept doc |
| Section 2.1.3 heading   | "Current Investigations"       | "Current geotechnical investigations"             | Updated concept doc |
| Section 2.2 heading     | "Seismic Hazard"               | "Seismic shaking hazard"                          | Updated concept doc |
| Appendix B name         | "Previous Investigations"      | "Previous ground investigation results"           | Updated concept doc |
| Appendix C name         | "Investigation Logs"           | "Current geotechnical investigation logs"         | Updated concept doc |
| Heading case            | Title Case in places           | Sentence case throughout                          | Updated concept doc |
| Section numbering gaps  | Sections 4/5/6 hard-coded      | Sequential renumbering when conditionals excluded | Updated concept doc |
| Slope stability heading | "Slope Stability"              | "Slope stability assessment"                      | Updated concept doc |
| Fault rupture heading   | "Fault Rupture Hazard"         | "Fault rupture hazard assessment"                 | Updated concept doc |
| Section 3.2 heading     | "Foundation Design Parameters" | "Foundation pile design parameters"               | Updated concept doc |

## Scope

Phases 0-3 only. Pure DOCX generation, no LLM. The function accepts:

1. `structure: ReportStructure` — ordered, non-empty value object wrapping a sequence of `SectionHeading` items (each carrying a heading string). Flat for Phases 0-3; hierarchy extensible without breaking the API. No duplicate top-level headings.
2. `metadata: ProjectMetadata` — typed value object with project-level fields (project number, client, site address, date); full field list subject to Graeme design session
3. `output_path: Path` — where to write the output DOCX

The function returns `None` on success and raises on failure (see pending ADR).

**Design principle (applied here and to all core functions):** function signatures prefer named value objects over raw collections. A `list[str]` becomes `ReportStructure`; a plain string address would become `SiteLocation`. This keeps the API stable while the domain model evolves.

**Deferred to future specs:**

- Geotechnical-specific section tree and conditional flags (foundation_assessment, slope_stability, etc.)
- Metadata table layout and field set (pending Graeme design session)
- Phases 4-8 (LLM-powered extraction, standards mapping, placeholder injection)
- Fork of python-docx to internal GitHub org (separate feature, out of scope)

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

- **FR-001**: System MUST generate a DOCX file with sections defined by a `ReportStructure`
  value object. The builder MUST NOT hard-code any section names, ordering, or heading
  conventions. (Addresses AC2, AC11. Enables multi-jurisdiction and multi-report-type
  evolution.)
- **FR-002**: System MUST include or exclude conditional sections based on boolean flags
  in `SkeletonConfig`, validated against the `ReportDefinition`'s allowed flags,
  and renumber remaining sections sequentially. (Addresses AC3.)
- **FR-003**: System MUST insert mandatory tables (e.g., Geotechnical Model Table) as
  defined by `TableSpec` objects within the `ReportDefinition`. (Addresses AC4.)
- **FR-004**: System MUST insert a Document Control version table with columns
  defined by the report definition. (Addresses AC2.)
- **FR-005**: System MUST populate project metadata (project number, client name, site
  address, date, document code) from a typed `ProjectMetadata` object. (Addresses AC5.)
- **FR-006**: System MUST access the DOCX engine exclusively through the `DocumentFacade`
  protocol defined in ADR-002. The facade MUST accept only primitive types (`str`, `int`,
  `list[str]`). No domain value objects, Pydantic models, or enums may cross the facade
  boundary. (Addresses architectural constraint.)
- **FR-007**: System MUST use a `.docx` copy of the company template when one is provided
  (clearing all content, keeping styles only), or create a blank document when none is
  provided. (Addresses AC14.)
- **FR-008**: System MUST insert appendix headings as defined by the report definition's
  back matter section. (Addresses AC13.)

### Key Entities (if data is involved)

**Phases 0-3 (this spec):**

- **SectionHeading**: Thin value object wrapping a single heading string. No hierarchy in Phases 0-3; designed to carry `level`, `key`, and `condition_flag` in future phases without changing the `ReportStructure` API. Key attribute: `heading` (str).
- **ReportStructure**: Ordered, non-empty value object wrapping `list[SectionHeading]`. Represents the *resolved* section list — mandatory/conditional decisions already made upstream. Validates: non-empty, no duplicate top-level headings. Replaces `list[str]` as the first argument to `build_skeleton()`. (Graeme design session 2026-06-05.)
- **ProjectMetadata**: Data object for project-level metadata. Key attributes:
  `project_number` (str), `client_name` (str), `site_address` (str), `date` (date),
  `document_code` (str).
- **DocumentFacade**: Protocol for DOCX engine abstraction (from ADR-002).
  Key methods: `add_heading`, `add_paragraph`, `add_table`, `add_metadata_block`, `save`.
  **Boundary rule**: accepts only primitive types.
- **PythonDocxFacade**: Concrete implementation of `DocumentFacade` using python-docx.

**Future phases (identified, not in scope):**

- **ReportDefinition**: Policy object describing a report type's section structure (mandatory sections, conditional flags, jurisdiction rules). Produces a `ReportStructure` as output via a `resolve_structure()` step. Key attributes: `report_type`, `jurisdiction`, `heading_case`, `front_matter`, `body_sections`, `back_matter`, `condition_flags`.
- **SectionSpec**: Richer per-section model used inside `ReportDefinition`. Key attributes: `key`, `heading`, `level`, `mandatory`, `condition_flag`, `children`, `table`. Distinct from `SectionHeading` — carries policy, not just text.
- **SkeletonConfig**: Configuration controlling which conditional sections to include. Key attribute: `flags` (dict[str, bool]).
- **GIRTemplate**: Policy object encoding standard section sets for a given investigation type and jurisdiction. Input to `resolve_structure()`; produces a `ReportStructure`.
- **InvestigationScope**: What fieldwork was done (borehole count/type, lab programme, in situ tests). Drives conditional section inclusion. Distinct from `ProjectMetadata`.
- **SiteLocation**: Coordinates, legal description, regional council jurisdiction. Drives seismic/liquefaction zone defaults. Candidate for extraction from `ProjectMetadata`.

## Success Criteria (mandatory)

- **SC-001**: A DOCX generated with default config passes automated heading-order
  validation against the canonical section list.
- **SC-002**: All 16 flag combinations (4 boolean flags) produce structurally valid,
  sequentially numbered DOCX files.
- **SC-003**: The skeleton builder can be tested entirely with a recording stub --
  no DOCX engine required for unit tests.

## Assumptions

- The company Word template is not available yet. The initial implementation uses a blank
  `Document()` or a mock `.docx` file. When a template is provided, the "styles only"
  strategy applies: clear all content, keep style definitions. Real template integration
  is deferred.
- Section 1.1 (Scope of work) is always included by default. The concept doc resolved
  this open question explicitly.
- Liquefaction assessment (Section 2.3) is always included for NZ sites. It is treated
  as mandatory in the NZ_GIR report definition.
- Steps 4-8 of the concept doc (LLM extraction, standards mapping, placeholders) are
  out of scope for this spec and will be covered in a future iteration.
- Only one `ReportDefinition` instance (NZ_GIR) is shipped. AU, US, UK, and other report
  types are deferred but the architecture supports them without builder code changes.
- Only "sentence" heading case is exercised. "title" case support is deferred but the
  `heading_case` field on `ReportDefinition` ensures the architecture supports it.
- Jinja templating for placeholder population is deferred. The facade pattern allows
  introducing a `JinjaDocxFacade` later without changing builder code.

## Risks

| Risk                                                                        | Impact                                                            | Mitigation                                                                        |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| python-docx heading styles don't match corporate template styles            | Generated headings render without formatting in the real template | Facade encapsulates style mapping; test with real template early                  |
| Sequential renumbering logic has off-by-one errors with nested conditionals | Incorrectly numbered sections undermine trust                     | Exhaustive flag-combination tests (16 combinations)                               |
| DocumentFacade protocol grows too large as features are added               | Facade becomes a leaky abstraction                                | Keep facade minimal; add methods only when needed by a concrete scenario          |
| Template `.dotx` format not supported by python-docx                      | Cannot use the corporate template directly                        | ADR-002 documents this: use a `.docx` copy of the template                      |
| ReportDefinition model may not generalise well to non-geotechnical reports  | Architecture rework needed when environmental reports are added    | Validate model shape with 2-3 hypothetical definitions before committing          |
| Company template has existing content that conflicts with generated sections | Merge logic would be complex and error-prone                      | "Styles only" strategy: clear all content, keep styles. Defer merge scenario.   |
| Jinja placeholder syntax in template collides with user template content    | Template rendering errors                                         | Defer Jinja entirely; use programmatic building for Phases 0-3                    |
