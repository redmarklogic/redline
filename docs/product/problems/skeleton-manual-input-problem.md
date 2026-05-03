> **Status: SUPERSEDED (2026-04-22).** The manual-input form approach was rejected by
> the founder. Sprint 1 uses one-click LOE upload with LLM metadata extraction. No
> manual form, no fallback form. If extraction cannot populate a metadata field, the
> skeleton generates with that field blank. See PRD decision log:
> `docs/product/prds/skeleton-generator-prd.md`.

# Problem Statement: Manual Parameter Input for Skeleton Generation (Document-Parser Scope Cut)

**Status**: Draft v1. **Owner**: Mark. **Date**: 2026-04-21.
**Strategic bet**: [Bet 1 — The Free Skeleton Wedge Beats Paid Acquisition](../strategy/strategic-bets.md)
**Parent problem**: [skeleton-wedge-problem.md](skeleton-wedge-problem.md)
**Trigger**: Ron's Sprint 1 pre-mortem (2026-04-21), Risk 1 mitigation Action A — cut the document parser from Sprint 1.

---

## Context: Why This Problem Exists

The original Sprint 1 plan included Feature M (Document Parser), which would extract project parameters from uploaded scope documents (RFPs, LOEs) to feed the skeleton generator. Ron's pre-mortem correctly identified this as an R&D-grade task disguised as a Sprint 1 deliverable: parsing unstructured geotechnical scope documents to extract jurisdiction, project type, conditional section flags, and metadata requires NLP or structured extraction from variable document formats. This is a research problem, not a defined implementation task.

The mitigation: replace the document parser with a manual-input form. The user selects jurisdiction, report type, and project parameters from structured form fields. This converts an uncertain R&D task into a well-defined UI problem.

The risk: if the manual form captures too little, the skeleton degenerates to "just headings" — the failure mode the pre-mortem identified. If the form captures too much, it becomes a friction barrier that users abandon before generating a skeleton. The form must thread the needle: fast enough to feel frictionless (under 2 minutes), specific enough to produce a genuinely useful skeleton.

---

## Target User

Intermediate civil/geotechnical engineer (3-7 years post-graduation), working inside a Small NZ consultancy (5-50 person firm) on residential or light-commercial GBR/GIR work. Same as [skeleton-wedge-problem.md](skeleton-wedge-problem.md).

This user knows what report type they need. They know what conditional sections apply. They know their project number and client name. What they do not know (or cannot confidently recall) is the complete list of mandatory sections, the correct heading conventions, which standards apply to each section, and what domain-specific questions the skeleton should prompt them to answer.

The form asks the user to provide what they already know. The skeleton generator provides what they do not.

---

## Core Pain

The skeleton generator requires project-specific parameters to produce useful output. Without these parameters, it can only produce a generic section structure — the same headings any engineer could type in Word in 10 minutes. The value proposition collapses.

Specifically, the skeleton's structural variation is driven by:

1. **Report type** — GIR and GBR have different section structures.
2. **Conditional section flags** — foundation assessment, slope stability, fault rupture, and ground improvement each add or remove entire sections, and the remaining sections must renumber sequentially.
3. **Regional jurisdiction** — Canterbury (NZ) has specific additional requirements (MBIE Part D, CCC IDS Part 4, Port Hills hazard assessment) that other NZ regions do not.
4. **Project type** — residential, commercial, and infrastructure projects reference different standards and trigger different placeholder content.
5. **Project metadata** — project number, client name, site address, and date populate the document control block, the Applicability boilerplate, and the document naming convention.

Without a document parser, the user must provide all of this. The question is: what is the minimum viable set of inputs that produces a skeleton worth generating?

---

## Desired Outcome

A user can generate a project-specific GIR skeleton by completing a structured form in under 2 minutes, without uploading any documents. The resulting skeleton includes the correct conditional sections, project-specific metadata, jurisdiction-appropriate standards references, and domain-specific placeholder prompts — enough structural scaffolding that the engineer's first action is editing and validating, not writing.

**Measurable proxy**: Users generate 3-5 skeletons (quota burn) rather than generating one and abandoning the tool. If form completion takes longer than 2 minutes or if the resulting skeleton is too generic, users will not return.

---

## Strategic Link

Bet 1's kill criterion depends on quota exhaustion triggering outbound. Quota exhaustion requires users to generate 3-5 documents. Users will only generate multiple documents if each skeleton is project-specific and useful enough to be worth opening in Word. The manual-input form is the mechanism that makes each skeleton project-specific. If the form fails — either by being too burdensome (users abandon) or too shallow (skeletons are generic) — Bet 1 fails.

---

## Clarity Check

| Check | Status | Detail |
|---|---|---|
| Target user | Identified | Intermediate engineer, Small NZ firm, GBR/GIR work |
| Core pain | Identified | Skeleton generator needs project parameters; without them, output is generic and worthless |
| Desired outcome | Measurable | Form < 2 min, skeleton specific enough to drive 3-5 generations per user |
| Strategic link | Linked | Bet 1 — quota exhaustion depends on skeleton usefulness |
| Constraints | Stated | See below |

---

## Constraints

1. **Sprint 1 scope**: The form must be simple enough to build as HTML/CSS in days, not weeks. No NLP, ML, or document parsing capability. Standard web form controls only (dropdowns, toggles, text inputs, date pickers).
2. **GIR only in Sprint 1**: The spec (Phases 0-3) covers GIR section structure. GBR is deferred to a subsequent spec. The report-type selector should exist in the UI (showing future extensibility) but offer only GIR as a Sprint 1 option.
3. **NZ jurisdiction only**: Per Bet 5 (beachhead doctrine). The jurisdiction selector should exist but offer only NZ in Sprint 1.
4. **No document upload**: The entire point of this scope cut is eliminating the document parser. The form replaces it entirely.
5. **Switzerland-neutral**: The form collects structural parameters, not engineering opinions. It asks "do you need a foundation assessment section?" — it does not ask "what foundation type should be used?"

---

## Acceptance Criteria Affected by the Scope Cut

The document-parser scope cut affects three ACs from the concept doc:

| AC | Original Expectation | Sprint 1 Reality (with manual form) |
|---|---|---|
| AC5 (Project metadata) | Metadata "populated from the RFP/LOE" | Metadata entered manually by the user via form fields |
| AC6 (Traceability matrix) | "Maps every RFP/LOE deliverable to a report section" | **Deferred** — traceability requires document parsing. Sprint 1 skeleton has no traceability matrix. |
| AC15 (First action is editing) | Skeleton has enough structure "that an intermediate engineer can begin refining immediately" | Still achievable — the manual form captures enough to produce a project-specific skeleton. The user supplies what the parser would have extracted. |

AC6 deferral is acceptable for Bet 1 validation. The traceability matrix is valuable for workflow correctness, but it is not required for the "is this skeleton worth generating?" question that Bet 1 answers. It moves to Sprint 2 alongside the document parser.

---

## Manual-Input Form Field Specification

### Design Principles

1. **Required fields gate generation.** The user cannot generate a skeleton until all required fields are completed. This ensures every skeleton is project-specific.
2. **Smart defaults reduce friction.** Where a sensible default exists (e.g., date = today, jurisdiction = NZ, liquefaction = always included for NZ), use it.
3. **Progressive disclosure.** The form should group fields logically: metadata first, then structural choices. Conditional fields (e.g., ground improvement) should appear only when their parent is enabled.
4. **Under 2 minutes to complete.** The form targets 10-15 fields. Anything beyond 20 fields is a friction risk.

### Field Specification

#### Group 1: Project Metadata (Required)

These fields populate the Document Control block, cover page, Applicability boilerplate, and document naming convention.

| # | Field | Type | Required | Default | Justification |
|---|---|---|---|---|---|
| 1 | **Project number** | Text input | Yes | — | Populates Document Control table and document naming (`[JobNo]-RPT-GT-[Element]-[Seq]`). Every firm uses project numbers; the user knows this. |
| 2 | **Client name** | Text input | Yes | — | Populates Document Control, Applicability boilerplate (Exclusive Use clause names the client as the legal entity), and Client Summary references. Critical for legal boilerplate personalisation — without it, the Applicability section is generic. |
| 3 | **Site address** | Text input | Yes | — | Populates Introduction (Section 1.0) and Site Description (Section 1.2). Anchors the skeleton to a physical location. |
| 4 | **Report date** | Date picker | Yes | Today | Populates Document Control. Defaulting to today reduces friction. |

#### Group 2: Report Configuration (Required)

These fields determine the skeleton's section structure and standards context.

| # | Field | Type | Required | Default | Justification |
|---|---|---|---|---|---|
| 5 | **Jurisdiction** | Dropdown | Yes | New Zealand | Determines which standards corpus applies. Sprint 1: NZ only. The field exists for future AU expansion (Bet 5). |
| 6 | **Report type** | Dropdown | Yes | GIR | Determines section structure. Sprint 1: GIR only. The field exists for future GBR support. Showing a single-option dropdown signals "more coming" without over-building. |
| 7 | **Region** | Dropdown | Yes | — (must select) | Options: `Auckland / Waikato / Bay of Plenty / Hawke's Bay / Wellington / Canterbury / Otago-Southland / Other NZ`. Canterbury triggers additional standards references (MBIE Part D, CCC IDS Part 4) and, if Port Hills sub-region is selected, GNS Science Stage 1 hazard content. **This field is the primary jurisdiction-mapping mechanism in the absence of a document parser.** |
| 8 | **Project type** | Dropdown | Yes | — (must select) | Options: `Residential / Light Commercial / Heavy Commercial-Industrial / Infrastructure / Subdivision`. Affects standards references: residential triggers NZS 3604 (Good Ground), subdivision triggers additional council requirements, infrastructure triggers different seismic design cases. |

#### Group 3: Conditional Sections (Required)

These toggles control which optional sections the skeleton includes. They directly map to the `SkeletonConfig` flags in the spec.

| # | Field | Type | Required | Default | Justification |
|---|---|---|---|---|---|
| 9 | **Include foundation assessment?** | Toggle (Yes/No) | Yes | No | When Yes, adds Section 3 (Foundation Assessment) with subsections for foundation options and design parameters. Per spec Scenario 2, this is the primary structural branching point. |
| 10 | **Include slope stability assessment?** | Toggle (Yes/No) | Yes | No | When Yes, adds a slope stability section under Other Geotechnical Hazards (or as a standalone section if no other hazards apply). Triggers NZS 4431 and NZGS slope guidance references. |
| 11 | **Include fault rupture assessment?** | Toggle (Yes/No) | Yes | No | When Yes, adds a fault rupture section under Other Geotechnical Hazards. Triggers NZS 1170.5 Table 3.6 and GNS Active Faults Database references. Relevant primarily for Wellington, Canterbury, and sites near known active faults. |
| 12 | **Include ground improvement?** | Toggle (Yes/No) | Yes (when #9 = Yes) | No | **Conditionally visible** — only shown when foundation assessment (#9) is Yes. Per spec, ground improvement is silently ignored when foundation assessment is False. UI should enforce this dependency. |

#### Group 4: Report Context (Recommended)

These fields materially improve skeleton quality but are not strictly required for section structure generation. They should be presented as a clearly labelled "optional" group that the user can skip.

| # | Field | Type | Required | Default | Justification |
|---|---|---|---|---|---|
| 13 | **Report supports a consent application?** | Toggle (Yes/No) | No | No | When Yes, adds the Council/Regulatory Authority clause to the Applicability section (Section 6). Affects legal boilerplate. Defaulting to No is safe — the user can add the clause manually. |
| 14 | **Separate GFR being produced?** | Toggle (Yes/No) | No | No | When Yes, appendices B/C/D contain cross-references to the GFR rather than placeholder content for raw investigation data. Affects appendix structure. Defaulting to No (include placeholders) is the safe option. |
| 15 | **Heading preference** | Dropdown | No | Client Summary | Options: `Client Summary / Executive Summary`. Per research, Client Summary is the safe default ("executive summaries carry a high risk of contradicting the main report"). Executive Summary should only be used when the client's LOE explicitly requests it. |

#### Group 5: Document Control (Optional)

These fields pre-populate the Document Control version table. They are convenience fields — the user can always edit them in Word.

| # | Field | Type | Required | Default | Justification |
|---|---|---|---|---|---|
| 16 | **Prepared by** | Text input | No | — | Author name for the Document Control table. Optional because the user will edit the document anyway. |
| 17 | **Reviewed by** | Text input | No | — | Technical reviewer name. Optional for the same reason. |
| 18 | **Authorised by** | Text input | No | — | Project Director name. Optional for the same reason. |

### Field Count Summary

| Group | Fields | Required | Time estimate |
|---|---|---|---|
| Project Metadata | 4 | 4 | 30 sec |
| Report Configuration | 4 | 4 | 15 sec |
| Conditional Sections | 4 | 4 (toggles, fast) | 10 sec |
| Report Context | 3 | 0 | 10 sec (if used) |
| Document Control | 3 | 0 | 15 sec (if used) |
| **Total** | **18** | **12** | **~60-80 sec** |

Twelve required fields, six optional. A user who fills only the required fields completes the form in under a minute. A user who fills everything completes it in under 90 seconds. This is well within the 2-minute target.

---

## Essential vs Deferrable: Reasoning

### Essential (Ships in Sprint 1)

**Project metadata (fields 1-4)** is essential because without it, the skeleton has no Document Control, no Applicability boilerplate personalisation, and no document naming. The output would look like a template, not a project document. This is the "just headings" failure mode.

**Report configuration (fields 5-8)** is essential because these fields drive the skeleton's structural variation and standards references. Jurisdiction and region determine which standards corpus applies. Project type determines which NZS/NZGS references are injected per section. Without these, every skeleton is identical — the tool adds no value beyond what the user's firm template already provides.

**Conditional section toggles (fields 9-12)** are essential because they are the primary input to the skeleton generator's section inclusion/exclusion logic (spec Scenario 2). Without them, the skeleton either includes everything (generating unnecessary sections the user must delete) or includes nothing conditional (producing a minimal skeleton the user must extend). Both options degrade the user experience below the "worth generating" threshold.

### Recommended but Deferrable

**Report context (fields 13-15)** improves skeleton quality but the defaults are safe. If the consent-application toggle is missing, the user gets a skeleton without the regulatory clause — they can add it in Word. If the GFR toggle is missing, appendices include investigation data placeholders — harmless if a GFR also exists. The heading preference defaults to the safer option (Client Summary).

These fields should ship in Sprint 1 because they are trivial to implement (three more toggles/dropdowns) and meaningfully improve skeleton quality. But if build time is critically tight, they can be cut without breaking the core value proposition.

### Optional and Safely Deferrable

**Document Control names (fields 16-18)** are pure convenience. The user will open the skeleton in Word and edit the Document Control table regardless. Pre-populating author/reviewer/authoriser names saves 30 seconds of typing. Worth including if time permits, but zero impact on skeleton usefulness if omitted.

### Deferred to Sprint 2+ (Requires Document Parser)

The following capabilities are explicitly out of scope for the manual-input form and will return with the document parser (Feature M) in a later sprint:

| Capability | Why deferred | Sprint 2 dependency |
|---|---|---|
| Auto-extraction of project metadata from RFP/LOE | Requires document parsing (the exact R&D task we cut) | Feature M |
| Traceability matrix (RFP deliverables mapped to report sections) | Requires understanding the RFP's deliverable list (AC6) | Feature M |
| Auto-detection of conditional section flags from scope document | Requires NLP to infer "does this project need foundation assessment?" from prose | Feature M |
| Client Summary / Introduction drafting from RFP content | Requires extraction and summarisation of client brief (Phases 4-8 in concept doc) | Feature M + LLM integration |
| Scope of Work extraction from LOE | Requires document parsing and semantic understanding | Feature M |

---

## Items Requiring Graeme's Confirmation

Ron's pre-mortem instruction explicitly asks to "confirm with Graeme that dropdown-based parameter selection is sufficient for NZ GBR/GIR jurisdiction mapping." The following specific questions need Graeme's sign-off before the form design is finalised:

### Q1: Are the four conditional section toggles sufficient?

The form offers four toggles: foundation assessment, slope stability, fault rupture, and ground improvement. Are there other conditional sections that an intermediate NZ engineer would expect to toggle on/off for a GIR skeleton? Specifically:

- Is "geotechnical issues identified" (Section 2.5 in the research) a section the user should control, or should it always be included when foundation assessment is Yes?
- Are there Canterbury-specific conditional sections beyond what the region selector triggers?

### Q2: Is the region dropdown granular enough?

The form proposes eight NZ regions. Canterbury triggers additional MBIE Part D and CCC IDS Part 4 references. Is this sufficient, or does Canterbury need a sub-region selector (e.g., Port Hills vs Canterbury Plains vs Waimakariri) to capture the GNS Science Stage 1 hazard requirements that apply only to Port Hills?

### Q3: Is the project-type dropdown granular enough?

The form proposes five project types (Residential, Light Commercial, Heavy Commercial/Industrial, Infrastructure, Subdivision). Do these categories adequately capture the standards-mapping differences? For example, does "Residential" need to distinguish between single-dwelling and multi-unit? Does "Infrastructure" need sub-categories (roading, water, retaining)?

### Q4: Does NZS 3604 "Good Ground" assessment need a dedicated toggle?

For residential projects, NZS 3604 Section 3.1.2 defines "Good Ground" (300 kPa bearing capacity). Does the skeleton need a toggle like "Site meets Good Ground criteria?" to vary the content of the foundation assessment section, or is this an engineering interpretation that belongs in the authored content, not the skeleton structure?

---

## Structural Gaps

**Gap 1: GBR section structure is undefined.** The Sprint 1 spec and all supporting research cover GIR only. If GBR is added to the report-type selector in a future sprint, a separate section-structure specification is needed. This is a product decision, not a Graeme question.

**Gap 2: Canterbury sub-region handling is unresolved.** Open Question OQ4 from the section-placeholders research asks whether Canterbury should be a separate configuration or conditional flags within the standard template. The manual form's region selector partially addresses this (Canterbury triggers additional standards), but Graeme's input is needed on whether sub-regions (Port Hills) require distinct skeleton content.

**Gap 3: Liquefaction reporting path is not captured by the form.** The research identifies three liquefaction reporting paths (does not dictate design / limited impact / important issue). The current form does not ask the user to select a path because liquefaction is always included for NZ sites. However, the placeholder content could vary by path. This is a Sprint 1 "nice-to-have" — the skeleton can include the three-path prompt and let the user choose while authoring.

---

## Next Step

1. **Graeme confirmation**: Route Q1-Q4 above to Graeme for domain validation. If Graeme identifies additional toggles or finer-grained region handling, update this form spec before build begins.
2. **Engineering handoff**: Once Graeme confirms, this problem statement and form spec feed into a PRD for the manual-input form, which then feeds into `speckit` for engineering execution.
3. **Ron alignment**: Confirm with Ron that the AC6 (traceability matrix) deferral is acceptable for Bet 1 validation. I believe it is — the traceability matrix is a workflow-correctness feature, not a skeleton-usefulness feature — but Ron should sign off on the scope change.
