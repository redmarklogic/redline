# Feature Specification: Skeleton Conditional Section Logic — Input Model

**Feature Branch**: `feature/51-platform-p-skeleton-endpoint-post-skeleton-returns-docx-behind-auth`

**Created**: 2026-06-09

**Status**: Draft

**Input**: Shaped Pitch — [skeleton-conditional-logic-pitch.md](../../specs/shaped/skeleton-conditional-logic-pitch.md). Unblocks PRD AC2f ([skeleton-generator-prd.md](../../docs/product/prds/skeleton-generator-prd.md)).

## Overview

The skeleton endpoint currently generates a document with a fixed set of sections regardless of project context. This feature adds a structured input model that lets engineers describe their project's characteristics — site hazards, proposed earthworks, required analyses — so the generated skeleton includes exactly the sections the ENZ/NZGS 2023 guideline mandates for that project. Section inclusion is fully deterministic: the same input always produces the same output, with no probabilistic or model-inferred decisions.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Engineer generates a contextually accurate skeleton (Priority: P1)

An engineer submits a skeleton request that describes their project's site conditions. The generated Word document contains exactly the sections those conditions activate — no irrelevant sections appear, no relevant sections are missing.

**Why this priority**: A skeleton that always includes all sections is structurally wrong for the majority of residential projects. A practitioner who receives a Foundations section when foundation design was not requested, or a Slope Instability section for a flat site, recognises the tool does not understand the guideline. Practitioner trust requires conditional logic in Sprint 1 — it is not a future enhancement.

**Independent Test**: Submit a request with a specific set of section flags (e.g. two hazard categories and earthworks proposed). Confirm the generated skeleton contains exactly the sections those flags activate and no others.

**Acceptance Scenarios**:

1. **Given** a request with `hazards: [LIQUEFACTION, SLOPE_INSTABILITY]`, **When** a skeleton is generated, **Then** the document contains the Section 7 heading, Section 7.1 (Liquefaction), and Sections 7.5, 7.7, and 7.13 (the three sub-sections activated by Slope Instability) — and no other hazard sub-sections.
2. **Given** a request with `earthworks_proposed: true`, **When** a skeleton is generated, **Then** the document contains Section 8.3 (Filling and Earthworks).
3. **Given** a request with `foundation_recommendations_required: true`, **When** a skeleton is generated, **Then** the document contains Section 8.2 heading and sub-sections 8.2.1 through 8.2.9.
4. **Given** a request with `retaining_walls_present: true`, **When** a skeleton is generated, **Then** the document contains Section 8.4 (Retaining Walls).
5. **Given** a request with `hazards: [FLOODING]` and `flooding_info_uncertain: true`, **When** a skeleton is generated, **Then** the document contains both Section 7.14 (Inundation) and the Section 4.3 specialist recommendation modifier — these flags are orthogonal and both take effect independently.
6. **Given** a request with `hazards: [FAULT_RUPTURE]`, **When** a skeleton is generated, **Then** the document contains the NZ-specific extension sub-section 7.NZ-1 — not Section 7.15, not a no-op.
7. **Given** a request with `hazards: [SLOPE_INSTABILITY]` and no other flags, **When** the activated section set is examined, **Then** it contains exactly 7.5, 7.7, and 7.13 — the only one-to-many mapping in the activation rules.

---

### User Story 2 — Engineer generates a skeleton with no site-specific flags (Priority: P1)

An engineer submits a request with no section flags — or omits them entirely. The system accepts the request and produces a skeleton containing only the sections that are always structurally required by the guideline template. No conditional sections are incorrectly included by default.

**Why this priority**: Safe defaults are as important as correct conditionals. A practitioner who does not yet know the site's hazard profile must receive a skeleton they can complete — not one that preselects incorrect sections.

**Independent Test**: Submit a valid request body with no `section_flags` field. Confirm the response is 200 and the skeleton contains only mandatory sections (including the Section 7 heading, but no hazard sub-sections).

**Acceptance Scenarios**:

1. **Given** a request with no `section_flags` field, **When** a skeleton is generated, **Then** the response is `200 OK` and the skeleton contains only mandatory sections — including the Section 7 heading but no hazard sub-sections.
2. **Given** a request with `section_flags: null`, **When** a skeleton is generated, **Then** the behaviour is identical to the absent-flags case.
3. **Given** a request with `section_flags: {}` (all fields omitted), **When** a skeleton is generated, **Then** the behaviour is identical to the absent-flags case — all fields default to false / empty list.

---

### User Story 3 — Invalid input is rejected with a clear error (Priority: P1)

A caller that submits an unrecognised report type or hazard category receives a `422` error immediately. The system never silently defaults an unrecognised value.

**Why this priority**: Silently defaulting an unknown report type to GAR, or ignoring an unrecognised hazard category, would produce a document without signalling the input problem — a worse outcome than rejecting the request outright.

**Independent Test**: Submit a request with `report_type: "GBR"`. Confirm `422`. Submit a request with `hazards: ["VOLCANO"]` (not a valid category). Confirm `422`.

**Acceptance Scenarios**:

1. **Given** a request with an unrecognised `report_type` value, **When** the caller submits the request, **Then** they receive `422 Unprocessable Content` and no document is generated.
2. **Given** a request with an unrecognised hazard category string in the `hazards` list, **When** the caller submits the request, **Then** they receive `422`.
3. **Given** a request with `report_type` absent from the request body, **When** the caller submits the request, **Then** they receive `422` — the report type is required and must be explicit; no silent default to GAR.

---

### User Story 4 — Generation events are auditable (Priority: P2)

A reviewer can inspect the audit record for any skeleton generation event and determine exactly which flags were submitted and which sections were included as a result.

**Why this priority**: Deterministic section selection is only trustworthy if the selection event is traceable. An engineer incorporating the skeleton into a professional report needs confidence that the sections reflect the flags they submitted; an auditor needs a verifiable record.

**Independent Test**: Generate a skeleton with specific flags. Read the audit entry for that event. Confirm it contains both the submitted flags and the resulting section identifiers.

**Acceptance Scenarios**:

1. **Given** a skeleton is generated, **When** the audit log entry for that event is read, **Then** it contains the full section flags submitted in the request.
2. **Given** a skeleton is generated, **When** the audit log entry for that event is read, **Then** it contains the set of section identifiers that were activated for that generation.

---

### Edge Cases

- `hazards: []` — Section 7 heading is present; no hazard sub-sections are generated.
- `SLOPE_INSTABILITY` in hazards — activates 7.5, 7.7, and 7.13 together (the only one-to-many activation mapping).
- `OTHER` absent from hazards — Section 7.15 is not generated (it is not an always-on placeholder; it requires explicit selection).
- `FLOODING` in hazards activates Section 7.14; `flooding_info_uncertain: true` activates the Section 4.3 modifier. Both may be present simultaneously; neither implies the other.
- `FAULT_RUPTURE`, `VOLCANIC`, `TSUNAMI` activate NZ-specific extension sub-sections (7.NZ-1, 7.NZ-2, 7.NZ-3 respectively) — not routed to Section 7.15.
- Sections 8.5 and 8.6 are always present in the skeleton structure (headings with placeholder content); no flag governs their inclusion in Sprint 1.
- `COMPRESSIBLE_SOILS` activates Section 7.4 (compressible soils as a soil characterisation) — distinct from `SUBSIDENCE` (Section 7.12), which activates based on predicted outcome, not soil type.
- `FALLING_DEBRIS` activates Section 7.11 independently of `SLOPE_INSTABILITY` — they are kinematically distinct hazards; selecting one does not imply the other.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The skeleton endpoint MUST accept an optional `section_flags` block in the request body alongside project metadata. Absent or null `section_flags` MUST be valid and treated as all flags defaulting to false / empty list.
- **FR-002**: The system MUST determine section inclusion from `section_flags` using a deterministic rule: the same flags always produce the same section set. No probabilistic or LLM-inferred section selection is permitted.
- **FR-003**: The `hazards` field MUST accept a list of values drawn from the supported hazard category set. Each value in the list MUST activate the corresponding guideline section(s). An absent or empty list MUST produce the Section 7 heading with no sub-sections.
- **FR-004**: The `SLOPE_INSTABILITY` hazard category MUST activate exactly three sub-sections: 7.5, 7.7, and 7.13.
- **FR-005**: The `OTHER` hazard category MUST activate Section 7.15 only when explicitly present in the hazards list — it MUST NOT be auto-included when absent.
- **FR-006**: `FAULT_RUPTURE`, `VOLCANIC`, and `TSUNAMI` MUST each activate a dedicated NZ-specific extension sub-section (7.NZ-1, 7.NZ-2, 7.NZ-3 respectively). They MUST NOT be silently routed to Section 7.15 or produce no output.
- **FR-007**: The five Tier A boolean flags MUST each independently control a specific section or section modifier per the activation rules: `detailed_analysis_performed` → Section 7 full analysis detail; `retaining_walls_present` → Section 8.4; `flooding_info_uncertain` → Section 4.3 specialist recommendation modifier; `site_plan_footprint_available` → site plan appendix; `professional_opinion_required` → statement of professional opinion appendix. Each defaults to false when absent.
- **FR-008**: `foundation_recommendations_required: true` MUST include Section 8.2 and its sub-sections 8.2.1–8.2.9 in the generated skeleton.
- **FR-009**: `earthworks_proposed: true` MUST include Section 8.3 in the generated skeleton.
- **FR-010**: The `report_type` field MUST be required. Absent or unrecognised `report_type` values MUST be rejected with `422`. The system MUST NOT silently default to any report type.
- **FR-011**: Unrecognised hazard category values in the `hazards` list MUST be rejected with `422`.
- **FR-012**: The `flooding_info_uncertain` flag and the `FLOODING` hazard category MUST be treated as orthogonal inputs — each activates a different section element independently.
- **FR-013**: Every skeleton generation event MUST produce an audit record containing: (a) the full `section_flags` value submitted, and (b) the set of section identifiers included in the output.
- **FR-014**: Sections 8.5 and 8.6 MUST always be present in the skeleton as headings with placeholder content. No flag governs their inclusion in Sprint 1.

### Key Entities

- **SkeletonRequest**: the complete request body — comprises project metadata (optional identification fields), report context (jurisdiction, report type), and section flags.
- **SectionFlags**: the conditional logic input block — five Tier A boolean flags plus three Tier B fields (hazard list, foundation flag, earthworks flag). All fields optional at the request level; absent fields default to false / empty.
- **HazardCategory**: an enumerated set of geotechnical hazard types; each value maps to one or more guideline sub-sections in Section 7.
- **SectionID**: an identifier for a specific section or sub-section in the generated document. The activation mapping translates a `SectionFlags` value into a set of `SectionID`s.
- **GenerationAuditEntry**: a record produced for every skeleton generation event — contains the submitted `SectionFlags` and the resulting set of activated `SectionID`s.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Given any valid combination of section flags, the generated skeleton contains exactly the sections those flags activate — no extra sections, no missing sections — verified independently for each of the 7 implemented conditional rules (CL-G1 through CL-G7).
- **SC-002**: Given the same section flags on repeated calls, the system produces a skeleton with the same section set every time (determinism verified across N calls with the same input).
- **SC-003**: A request with no section flags produces a skeleton with mandatory sections only — no conditional sections incorrectly included by default.
- **SC-004**: 100% of unrecognised `report_type` values are rejected with 422 and produce no document.
- **SC-005**: 100% of unrecognised hazard category values are rejected with 422 and produce no document.
- **SC-006**: 100% of skeleton generation events produce an audit record containing both the submitted flags and the resulting section set.

## Assumptions

- Engineers know their site's hazard profile before submitting the request. The system does not infer hazard categories from site address or geospatial records — that is a separate, deferred feature.
- The UI for presenting section flags to the engineer before submission is out of scope for this feature (Matt's design domain).
- Canonical heading text for NZ-specific extension sub-sections (7.NZ-1 Fault Rupture, 7.NZ-2 Volcanic, 7.NZ-3 Tsunami) is Graeme's to provide. Placeholder text is used in Sprint 1; this does not block implementation or testing of the structural logic.
- Sections 8.5 and 8.6 conditional status is uncertain pending Graeme's guideline confirmation; they are treated as always-present in Sprint 1.
- All `project_metadata` fields are optional. Absent fields produce blank placeholder tokens in the generated document; no `project_metadata` field controls section inclusion.
- Cross-field geotechnical validation (e.g. flagging earthworks without a slope stability hazard) is deliberately out of scope. The system validates input shape and permitted values only — it does not make engineering judgments.

## Out of Scope

- LLM-inferred or geospatial-lookup-driven hazard category pre-population (Rabbit Hole 1 in the Pitch).
- Graduated hazard severity per sub-section — the hazard flag is binary (Rabbit Hole 2).
- Cross-field geotechnical coherence validation (Rabbit Hole 3).
- Section 8.5 and 8.6 conditional flags (Rabbit Hole 4 — deferred pending Graeme's confirmation).
- AU jurisdiction section logic — the jurisdiction field enforces this boundary (Rabbit Hole 5).
- GBR report type — `report_type: "GBR"` returns 422; no GBR skeleton is generated.
- CL-G8 (local regulatory additions) — this is the practitioner's responsibility, not a system flag.
- LOE extraction of section flags — that is Feature M (Document Parser); the extraction behaviour is specified in the Pitch but the implementation belongs to that feature.
- Manual fallback input form (excluded per PRD Decision Log 2026-04-22).

## Dependencies

- **Pitch**: `specs/shaped/skeleton-conditional-logic-pitch.md` — primary scope authority.
- **PRD AC2f**: `docs/product/prds/skeleton-generator-prd.md` — the acceptance criterion this feature unblocks.
- **ENZ/NZGS 2023 guideline**: `docs/knowledge/geotechnical/report-writing/engnz-nzgs-2023-guideline-structure-standards-conditional-logic.md` — authoritative source for conditional rules CL-G1 through CL-G8.
- **Base skeleton endpoint**: `specs/001-skeleton-endpoint/` — this feature extends the request model introduced there. The `project_metadata` entity in 001's spec is carried forward; the request is enriched with `report_context` and `section_flags`.
- **Graeme**: heading text for 7.NZ-1, 7.NZ-2, 7.NZ-3 (non-blocking for Sprint 1 implementation).
