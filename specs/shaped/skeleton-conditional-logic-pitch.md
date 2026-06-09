# Pitch: Skeleton Conditional Section Logic — Input Model

**Shaped by**: Peter  
**Date**: 2026-06-09  
**Appetite**: Sprint 1 — fits inside the existing `POST /skeletons` scope. No new sprint.  
**Unblocks**: AC2f in `docs/product/prds/skeleton-generator-prd.md`  
**Branch**: `feature/51-platform-p-skeleton-endpoint-post-skeleton-returns-docx-behind-auth`  
**Primary reference**: ENZ/NZGS Geotechnical Reports Guideline and Template (August 2023)  
**Supporting reference**: `docs/knowledge/geotechnical/report-writing/engnz-nzgs-2023-guideline-structure-standards-conditional-logic.md`

---

## Diagnosis

Redline is pre-launch, NZ-only, Phase 1. The binding constraint is shipping a skeleton that
geotechnical engineers trust enough to use in one working session. The current `marker` stack
has no HTTP request body model — the skeleton builder takes hardcoded constants. The `POST
/skeletons` endpoint needs a Pydantic request schema in `src/rl/schemas/` before any
conditional logic can be tested.

The 2023 ENZ/NZGS guideline contains 8 conditional rules (CL-G1 through CL-G8). Five of them
have deterministic, checkable triggers. Three carry the phrase "as appropriate to the site and
development" without specifying which project inputs activate them. That phrase is practitioner
judgment in the guideline; it must become a concrete input field in our system. That product
decision is what this Pitch resolves.

**Surviving the Round test**: A skeleton that always includes all sections is structurally
wrong for low-risk residential projects — Section 8.2 Foundations appearing when foundation
design was not requested, or Section 7 hazard sub-sections appearing for a stable flat site,
signals to a practitioner that the tool does not understand the guideline. Conditional logic
is a short-runway requirement (3–6 months), not a long-runway aspiration. It ships in Sprint 1.

---

## Problem

The `POST /skeletons` request body has no input model. Without a defined schema, Kabilan
cannot implement conditional section logic — every rule degrades to "always include," which
produces structurally incorrect skeletons for a meaningful fraction of residential projects.

The design gate in the PRD (AC2f) is blocked on this Pitch existing. Nothing else is blocking.

The three ambiguous rules — CL-G1 (Hazards), CL-G3 (Foundations), CL-G4 (Earthworks) — need
concrete input parameters. The other five rules have clear, implementable triggers.

---

## Appetite

This is a scope boundary, not a time estimate. The conditional logic input model fits inside
Sprint 1. The appetite constraint is: **no new data storage, no LLM judgment calls for
section activation, no multi-phase input forms**. Every rule must be decidable from the
fields present in the request body using a deterministic function. No rule requires calling
an LLM to decide whether a section is included.

---

## Solution

### Part 1 — Request body schema

The `POST /skeletons` endpoint accepts a JSON body. The schema lives at
`src/rl/schemas/` as a Pydantic model. It is the authoritative input contract for skeleton
generation. The shape below is a breadboard — field names are indicative, not binding on
implementation details.

```
SkeletonRequest
  project_metadata:
    project_number: str (optional — blank if LOE extraction missed it)
    client_name:    str (optional)
    site_address:   str (optional)
    report_date:    date (optional — defaults to today if absent)

  report_context:
    jurisdiction:   enum { "NZ" }     — NZ-only in Sprint 1; AU deferred
    report_type:    enum { "GAR" }    — Geotechnical Assessment Report only
                                        (GBR out of scope; reject other values with 422)

  section_flags:   SectionFlags       — the conditional logic input model (see Part 2)
```

`report_context.report_type` is an enum with a single value in Sprint 1. This is deliberate:
the API shape is established now; new report types join the enum later. Receiving a value
outside the enum returns `422 Unprocessable Content` per ADR-018 decision 4. Do not silently
default to GAR — return an explicit error so the caller knows the value was unrecognised.

`project_metadata` fields are all optional. If the LOE extraction (Feature M) could not
populate a field, the caller sends `null` or omits the field. The skeleton generates with
blank placeholder tokens. No field in `project_metadata` gates section inclusion.

### Part 2 — The conditional logic input model (SectionFlags)

This is the core design decision this Pitch resolves.

The 8 rules split into two tiers by implementation complexity.

#### Tier A — Deterministic boolean flags (implement all five in Sprint 1)

These rules have explicit, checkable triggers. Each becomes a boolean field in
`SectionFlags`. Default is `false` when absent (safer — omit the section rather than include
it incorrectly).

| Flag name | Rule | Section affected | Default |
|---|---|---|---|
| `detailed_analysis_performed` | CL-G2 | Section 7 — full analysis detail | false |
| `retaining_walls_present` | CL-G5 | Section 8.4 (Retaining Walls) | false |
| `flooding_info_uncertain` | CL-G6 | Section 4.3 modification | false |
| `site_plan_footprint_available` | CL-G7a | Appendices — site plan footprint | false |
| `professional_opinion_required` | CL-G7b | Appendices — statement of professional opinion | false |

**CL-G8 (local regulatory additions):** Not a system flag. The guideline explicitly states
this is the author's responsibility. The skeleton generator must not prevent the user from
adding sections in Word after download. No flag, no logic, no implementation.

#### Tier B — The "as appropriate" trio (the design decision)

**CL-G1 — Section 7 (Geotechnical Hazards, sub-sections 7.1–7.15)**

The triggering input is a **hazard presence checklist** — a list of hazard categories the
engineer has identified as relevant to the site. Each item in the list activates the
corresponding sub-section in Section 7. The Section 7 heading itself is always included; the
sub-sections are driven by the list.

```
section_flags.hazards: list[HazardCategory]
```

Where `HazardCategory` is an enum:

```
HazardCategory {
  # Guideline 7.1–7.15 mapped values
  LIQUEFACTION,              # 7.1 — Liquefaction potential and effects
  LATERAL_SPREADING,         # 7.2 — Lateral spreading potential and effects
  EXPANSIVE_SOILS,           # 7.3 — Expansive soils
  COMPRESSIBLE_SOILS,        # 7.4 — Compressible soils (distinct from settlement outcome)
  SLOPE_INSTABILITY,         # 7.5 Mass movement / 7.7 Stability of slopes / 7.13 Slippage
  UNCONTROLLED_FILL,         # 7.6 — Uncontrolled fill (site condition; not reducible to
                             #        SETTLEMENT + SLOPE_INSTABILITY combo)
  EROSION_AND_DRAINAGE,      # 7.8 — Erosion and drainage (replaces COASTAL_EROSION;
                             #        coastal is a qualifier, not a separate category)
  SENSITIVE_AND_COLLAPSIBLE_SOILS, # 7.9 — Sensitive and collapsible soils (quick clays,
                             #        loess, metastable structure — distinct soil type)
  CONTAMINATION,             # 7.10 — Contamination
  FALLING_DEBRIS,            # 7.11 — Falling debris (rockfall/toppling; kinematically
                             #        distinct from slope mass movement)
  SUBSIDENCE,                # 7.12 — Subsidence
  FLOODING,                  # 7.14 — Inundation / flooding

  # NZ-specific extensions (no guideline sub-section; generate sub-sections 7.NZ-1–7.NZ-3)
  FAULT_RUPTURE,             # 7.NZ-1 — Active fault rupture (Hikurangi context)
  VOLCANIC,                  # 7.NZ-2 — Volcanic hazard
  TSUNAMI,                   # 7.NZ-3 — Tsunami inundation

  # Catch-all (practitioner-flagged only — see 7.15 note below)
  OTHER                      # 7.15 — Other relevant information
}
```

**Design decisions encoded in this enum (Graeme-consultation decisions, 2026-06-09):**

- **7.4 → `COMPRESSIBLE_SOILS`, not `SETTLEMENT`:** Compressible soils is a soil
  characterisation (cause); settlement is a predicted outcome. Conflating them would
  mislead practitioners assessing Holocene deposits or peat. They are distinct sub-sections
  with distinct mitigation logic.

- **7.6 → `UNCONTROLLED_FILL`:** Cannot be expressed as a `SETTLEMENT` + `SLOPE_INSTABILITY`
  combo. A site may have uncontrolled fill without exhibiting either of those as the
  primary concerns. Combo-activation would silently include 7.6 for practitioners who
  checked those values for unrelated reasons. Explicit enum value is unambiguous.

- **7.8 → `EROSION_AND_DRAINAGE`:** Renamed from `COASTAL_EROSION`. The guideline heading
  covers inland gully erosion, streambank erosion, and drainage — coastal is one instance,
  not the category. If coastal distinction is needed later it becomes a qualifier field,
  not a new enum value.

- **7.9 → `SENSITIVE_AND_COLLAPSIBLE_SOILS`:** Quick clays, loess, and metastable soils
  have no existing enum match. This is a distinct soil type requiring its own sub-section.

- **7.11 → `FALLING_DEBRIS`:** Rockfall and toppling failure are kinematically distinct
  from slope mass movement (`SLOPE_INSTABILITY`). A practitioner assessing a stable slope
  with rockfall hazard above would not tick `SLOPE_INSTABILITY`; keeping 7.11 under that
  enum value would cause the sub-section to be omitted.

- **7.15 → `OTHER`, practitioner-flagged only:** Section 7.15 is not an always-on
  placeholder. An engineer ticks `OTHER` when site-specific information does not fit
  7.1–7.14. Always generating 7.15 adds noise to skeletons where there is nothing else.
  `OTHER` maps to 7.15 only when explicitly included in the hazards list.

- **`FAULT_RUPTURE`, `VOLCANIC`, `TSUNAMI` → NZ-specific extensions (7.NZ-1, 7.NZ-2,
  7.NZ-3):** These are real NZ residential hazards (Hikurangi subduction zone context).
  Routing to 7.15 conflates distinct hazards into a catch-all; deferring to v2 creates
  dead enum values that accept input but produce no output. Instead, these generate
  sub-sections outside the guideline's 15-point list, clearly labelled as NZ-specific
  template extensions. Sub-section IDs use the `7.NZ-x` namespace to signal they extend
  (not interpolate into) the guideline numbering. Heading text for these sub-sections is
  Graeme's domain — placeholder text until Graeme provides content.

Rationale: For NZ residential sites, hazard categories are known at LOE stage (the engineer
has visited the site or reviewed NZGD records before commissioning). Presenting a checklist
of hazard categories is consistent with how practitioners think — they do not think "include
Section 7.3"; they think "this site has a liquefaction risk." The enum maps practitioner
vocabulary to section numbers.

If `hazards` is empty or absent: Section 7 heading is present (always structurally required
per the guideline's template), but no sub-sections are generated. This is the correct output
for a hypothetical site with no identified hazards.

Note: `FLOODING` in the hazard list activates Section 7.x (hazard sub-section); the
`flooding_info_uncertain` flag (Tier A) separately controls the Section 4.3 modification.
These are orthogonal — a site can have identified flooding as a hazard (include 7.x) without
the available information being uncertain (modify 4.3).

**CL-G3 — Section 8.2 (Foundations, sub-sections 8.2.1–8.2.9)**

This is the same signal as the existing CL-04 from prior research: "LOE requires foundation
design or engineering parameters." These are the same rule. Unify them into one flag.

```
section_flags.foundation_recommendations_required: bool
```

Default: `false`. When `true`, Section 8.2 and its sub-sections (8.2.1–8.2.9) are included.

Note from guideline (CL-G3): "detailed foundation design is flagged as likely outside scope
and to be provided in a separate report." The skeleton generates the Section 8.2 heading and
sub-section headings with placeholder text — it does not generate foundation design content.
The flag means "include the structural scaffold for foundation recommendations"; the engineer
fills the content.

**CL-G4 — Section 8.3 (Filling and Earthworks)**

The trigger is whether the proposed development includes filling, cutting, or earthworks.
This is a project characteristic known at LOE stage.

```
section_flags.earthworks_proposed: bool
```

Default: `false`. When `true`, Section 8.3 is included.

Rationale: "Earthworks proposed" is a clean binary. A flat residential lot with a standard
house does not involve earthworks; a hillside section or a lot requiring fill absolutely
does. The practitioner knows this when uploading the LOE.

#### Complete SectionFlags breadboard

```
SectionFlags:
  # Tier A — deterministic
  detailed_analysis_performed:      bool  (default: false)
  retaining_walls_present:          bool  (default: false)
  flooding_info_uncertain:          bool  (default: false)
  site_plan_footprint_available:    bool  (default: false)
  professional_opinion_required:    bool  (default: false)

  # Tier B — "as appropriate" trio, now made concrete
  hazards:                          list[HazardCategory]  (default: [])
  foundation_recommendations_required: bool              (default: false)
  earthworks_proposed:              bool                  (default: false)
```

All fields optional at the HTTP level — absent means `false` / empty list. This allows the
LOE extraction (Feature M) to populate only the fields it can confidently extract, with the
remainder defaulting safely.

### Part 3 — Section activation rules (deterministic mapping)

This table is the implementation contract. Kabilan implements this as a pure function:
`SectionFlags -> set[SectionID]`. No LLM involvement. No judgment calls. No external calls.

| Section / Element | Included when | Rule | Notes |
| --- | --- | --- | --- |
| Section 4.3 (Flooding) — specialist recommendation modifier | `flooding_info_uncertain == true` | CL-G6 | |
| Section 7 heading | Always | Template structure | |
| Section 7.1 (Liquefaction) | `LIQUEFACTION` in hazards | CL-G1 | |
| Section 7.2 (Lateral spreading) | `LATERAL_SPREADING` in hazards | CL-G1 | |
| Section 7.3 (Expansive soils) | `EXPANSIVE_SOILS` in hazards | CL-G1 | |
| Section 7.4 (Compressible soils) | `COMPRESSIBLE_SOILS` in hazards | CL-G1 | Distinct from settlement outcome |
| Section 7.5 (Mass movement) | `SLOPE_INSTABILITY` in hazards | CL-G1 | Also activates 7.7, 7.13 (same enum) |
| Section 7.6 (Uncontrolled fill) | `UNCONTROLLED_FILL` in hazards | CL-G1 | |
| Section 7.7 (Stability of existing slopes) | `SLOPE_INSTABILITY` in hazards | CL-G1 | Same enum as 7.5 and 7.13 |
| Section 7.8 (Erosion and drainage) | `EROSION_AND_DRAINAGE` in hazards | CL-G1 | Replaces COASTAL_EROSION |
| Section 7.9 (Sensitive and collapsible soils) | `SENSITIVE_AND_COLLAPSIBLE_SOILS` in hazards | CL-G1 | |
| Section 7.10 (Contamination) | `CONTAMINATION` in hazards | CL-G1 | |
| Section 7.11 (Falling debris) | `FALLING_DEBRIS` in hazards | CL-G1 | Kinematically distinct from SLOPE_INSTABILITY |
| Section 7.12 (Subsidence) | `SUBSIDENCE` in hazards | CL-G1 | |
| Section 7.13 (Slippage) | `SLOPE_INSTABILITY` in hazards | CL-G1 | Same enum as 7.5 and 7.7 |
| Section 7.14 (Inundation) | `FLOODING` in hazards | CL-G1 | |
| Section 7.15 (Other relevant information) | `OTHER` in hazards (practitioner-flagged only) | CL-G1 | Not always-on; only when explicitly selected |
| Section 7.NZ-1 (Fault rupture) | `FAULT_RUPTURE` in hazards | CL-G1 | NZ-specific extension; heading text from Graeme |
| Section 7.NZ-2 (Volcanic) | `VOLCANIC` in hazards | CL-G1 | NZ-specific extension; heading text from Graeme |
| Section 7.NZ-3 (Tsunami) | `TSUNAMI` in hazards | CL-G1 | NZ-specific extension; heading text from Graeme |
| Section 7 full analysis detail | `detailed_analysis_performed == true` | CL-G2 | |
| Section 8.2 (Foundations) heading + sub-sections 8.2.1–8.2.9 | `foundation_recommendations_required == true` | CL-G3 / CL-04 unified | |
| Section 8.3 (Filling and Earthworks) | `earthworks_proposed == true` | CL-G4 | |
| Section 8.4 (Retaining Walls) | `retaining_walls_present == true` | CL-G5 | |
| Appendix — site plan footprint | `site_plan_footprint_available == true` | CL-G7a | |
| Appendix — statement of professional opinion | `professional_opinion_required == true` | CL-G7b | |
| SCOPE-CLAUSE-03 (Groundwater fluctuation clause) | Groundwater section present in skeleton | CL-08 (existing rule, not new) | |

**`SLOPE_INSTABILITY` activates three sub-sections (7.5, 7.7, 7.13).** These are structurally
distinct headings in the document; they share one enum value because they share one practitioner
trigger ("slope instability is relevant to this site"). The activation function maps one enum
value to multiple section IDs for this case only. This is the only multi-section mapping in
the table.

The activation function is pure: given a `SectionFlags` value object, it returns the set of
section identifiers to include. It has no side effects and no I/O. Every conditional
inclusion/exclusion decision is logged in the generation audit trail (per AC2d).

### Part 4 — LOE extraction integration

Feature M (Document Parser, metadata extraction) populates `project_metadata` fields. It
should also attempt to populate `section_flags`. The confidence bar for flag extraction is
higher than for metadata extraction — a wrong flag produces a structurally wrong skeleton,
not just a blank token.

**LOE extraction behaviour for flags:**
- Flags that can be extracted with high confidence (>90%) from explicit LOE language
  (e.g., "earthworks are proposed", "retaining wall to be designed") are populated by the
  extractor and passed in the request body.
- Flags that cannot be extracted with high confidence are left absent (default = false).
- The LOE extraction does not attempt to infer hazard categories from site address alone —
  that requires NZGD lookup, which is out of scope for Sprint 1.

The engineer reviews the extracted flags before submission. The UI layer (Matt's domain)
decides how to surface this review step — this Pitch does not prescribe the UX.

### Part 5 — Sections 8.5 and 8.6

Graeme flagged that Sections 8.5 (Slope design) and 8.6 (Other engineering considerations)
have uncertain conditional status — the guideline does not carry the "as appropriate" tag
explicitly on these, but Graeme infers they are conditional.

**Decision**: Do not include 8.5 or 8.6 in Sprint 1 conditional logic. Treat both as always
present in the skeleton structure (like the Section 7 heading — scaffold is present, content
is placeholder). This is the safe default: a practitioner who does not need these sections
deletes the heading in Word; a practitioner who needs them has the scaffold. No flag is
added until Graeme confirms the rule from the guideline. This is explicitly deferred, not
forgotten.

---

## Rabbit Holes

### Rabbit hole 1 — LLM-inferred hazard categories from site address

It is technically possible to have the LLM look up the site address against NZGD
(NZ Geotechnical Database) records and infer hazard categories. This is a different feature
— geospatial hazard lookup — not part of the skeleton generator. Do not implement it in
Sprint 1. The engineer provides the hazard list explicitly.

### Rabbit hole 2 — Graduated hazard severity per sub-section

The hazard checklist could carry a severity level (low/medium/high) to control sub-section
depth. This is unnecessary complexity for Sprint 1. The flag is binary: the hazard is
relevant to the site or it is not. Severity is editorial content — the engineer adds it in Word.

### Rabbit hole 3 — Validation that the flag combination is geotechnically coherent

For example: `earthworks_proposed = true` but `hazards = []` could indicate an incomplete
input (earthworks without slope stability assessment). Adding cross-field validation rules
that encode geotechnical judgment is a domain correctness problem, not a structural problem.
The skeleton generator is Switzerland-neutral — it does not make engineering judgments. Do
not add cross-field geotechnical validation. Validate schema shape and type only.

### Rabbit hole 4 — Sections 8.5 and 8.6 flag design

Graeme's uncertainty about 8.5 and 8.6 is an open domain question. Do not design a flag for
these sections until Graeme confirms the activation rule from the guideline. Building a flag
now that turns out to be wrong requires a schema change and a migration. Deferring costs
nothing in Sprint 1.

### Rabbit hole 5 — Multi-jurisdiction flag behaviour

The `jurisdiction` enum currently has one value (`"NZ"`). AU has different hazard categories
and different standards references. Do not design AU flag behaviour now. When AU is added,
the `SectionFlags` model will need AU-specific extension. The enum is the seam; keep it.

### Rabbit hole 6 — CL-G1 / CL-G3 / CL-G4 "as appropriate" re-interpretation

The guideline says "as appropriate to the site and development." Someone will argue this
means the system should decide appropriateness rather than asking the engineer. For Sprint 1:
the engineer decides. The skeleton generator does not claim to know the site — only the
engineer standing on the ground knows. Switzerland-neutral applies.

---

## No-Gos

- No LLM calls to decide which sections to include. Section activation is a deterministic
  function of the request body. This is testable and auditable. An LLM decision is neither.
- No geospatial lookup in Sprint 1. NZGD integration is a separate feature.
- No cross-field geotechnical validation. The system validates schema, not engineering logic.
- No manual input form as a fallback (PRD Decision Log 2026-04-22). If LOE extraction
  cannot populate a flag, the flag defaults to false.
- No AU section logic in Sprint 1. The `jurisdiction` enum enforces this boundary.
- Do not rename the `SectionFlags` fields to match the guideline's section numbers
  (e.g., `section_7_hazards`). Field names should reflect practitioner concepts
  (`hazards`, `foundation_recommendations_required`) not document navigation. The mapping
  to section numbers is the activation function's job.
- No GBR report type in Sprint 1. The `report_type` enum enforces this. Receiving
  `report_type: "GBR"` returns `422`. It does not silently generate a GAR.

---

## Architectural constraints (testable)

These constraints are expressible as automated tests. Kabilan implements them; they are
not optional.

1. **Section activation is a pure function.** Given the same `SectionFlags`, the activation
   function always returns the same set of section IDs. No randomness, no external I/O.
   Test: assert output stability across N calls with the same input.

2. **Every conditional inclusion/exclusion is logged in the audit trail.** The audit log
   entry for a skeleton generation event must include the `SectionFlags` value and the
   resulting set of included sections. Test: parse the audit log entry, assert both fields
   are present and non-empty.

3. **Unknown `report_type` returns 422.** Sending any value outside the `report_type`
   enum returns `422 Unprocessable Content` with the standard error envelope (ADR-018 §3).
   Test: POST with `report_type: "GBR"`, assert 422.

4. **Unknown `HazardCategory` value returns 422.** Sending a hazard string not in the
   `HazardCategory` enum returns `422`. Test: POST with `hazards: ["VOLCANO"]`, assert 422.

5. **Absent `section_flags` is valid.** A request body with no `section_flags` field (or
   `section_flags: null`) succeeds and produces a skeleton containing only mandatory sections
   plus default-false sections excluded. Test: POST with no `section_flags`, assert 200 and
   skeleton contains mandatory sections only.

6. **`retaining_walls_present: true` produces Section 8.4 in the skeleton.** Test: POST
   with `retaining_walls_present: true`, assert the docx contains a Section 8.4 heading.

---

## Layer placement

The `SectionFlags` Pydantic model belongs in `src/rl/schemas/`. It is an HTTP API input
schema, not a domain model. It does not belong in `src/marker/domain/models.py`.

The activation function (SectionFlags -> set[SectionID]) belongs in the domain layer,
possibly in a new `src/rl/domain/` module or extending `src/marker/domain/`. It takes a
value object and returns a value object. It has no knowledge of HTTP, Pydantic, or docx.

The section identifier type (SectionID) is a domain concept. It maps to heading strings in
the builder layer. The builder layer (`src/marker/functions/builders.py`) remains unchanged
in its core function; the activation function's output drives which sections are passed to
`build_sections`.

This maintains the existing layer boundary: HTTP schema -> domain logic -> document builder.
No layer is asked to do work outside its responsibility.

---

## Open question for Mark (not blocking this Pitch)

The LOE extraction currently extracts `project_number`, `client_name`, `site_address`,
`date`, `report_type`, and `conditional section flags` (per PRD Decision Log 2026-04-22).
The `SectionFlags` model above defines what those "conditional section flags" are. Mark
should confirm whether the LOE extraction UX should show the extracted flags to the engineer
for review before submission, or whether flags should silently default and the engineer
corrects the output in Word. This is a UX decision — it belongs in Matt's design phase, not
this Pitch. It does not block Sprint 1 implementation.

---

## What this Pitch does not decide

- The UI for presenting `SectionFlags` to the engineer (Matt's domain, Touch 1 constraints
  memo delivered separately).
- The exact sub-section heading text for Section 7 hazard sub-sections (Graeme's domain —
  the activation function produces section IDs; the heading text comes from the Standards
  Knowledge Store, not from this Pitch).
- The exact sub-section heading text for Section 7 hazard sub-sections (Graeme's domain —
  the activation function produces section IDs; the heading text comes from the Standards
  Knowledge Store, not from this Pitch). Partially unblocked: heading text for 7.1–7.15
  (guideline-defined sub-sections) is Graeme's to confirm. Heading text for 7.NZ-1, 7.NZ-2,
  and 7.NZ-3 (NZ-specific extensions) is Graeme's to provide before these sub-sections can
  carry anything other than placeholder text.

**Previously blocking gate — now resolved (2026-06-09):**
The Section 7 sub-section list (7.1–7.15), the `HazardCategory` enum definition, and the
complete hazard-to-sub-section mapping are all decided in this Pitch. Kabilan can implement
the activation function without further consultation. The only remaining Graeme dependency
is canonical heading text for the three NZ-specific extension sub-sections (7.NZ-1, 7.NZ-2,
7.NZ-3), which does not block coding or testing — use placeholder strings.

---

## Summary: what Kabilan builds

1. `src/rl/schemas/skeleton_request.py` — Pydantic `SkeletonRequest` model containing
   `ProjectMetadata`, `ReportContext`, and `SectionFlags` as defined in Part 1 and Part 2.
   `HazardCategory` enum lives here.

2. `src/rl/domain/section_activation.py` (or equivalent) — pure function
   `activate_sections(flags: SectionFlags) -> frozenset[SectionID]` per the activation table
   in Part 3. No I/O, no LLM calls, fully unit-testable.

   The Section 7 hazard-to-sub-section mapping is now fully resolved and unambiguous.
   Implement the lookup table exactly as the activation table specifies. Key implementation
   notes for this function:

   - `SLOPE_INSTABILITY` maps to three section IDs: `7.5`, `7.7`, and `7.13`. This is the
     only one-to-many mapping in the table.
   - `OTHER` maps to `7.15` only when explicitly present in the hazards list. It is not
     auto-included.
   - `FAULT_RUPTURE`, `VOLCANIC`, and `TSUNAMI` map to `7.NZ-1`, `7.NZ-2`, and `7.NZ-3`
     respectively. These are NZ-specific extensions to the guideline template. The section
     ID namespace `7.NZ-x` signals they are extensions, not interpolations into the
     guideline's numbering. Placeholder heading text is used until Graeme provides canonical
     heading strings for these three sub-sections.
   - All other enum values are one-to-one mappings per the activation table.

   **Graeme consultation still required for one item only:** Canonical heading text for
   `7.NZ-1` (Fault Rupture), `7.NZ-2` (Volcanic), and `7.NZ-3` (Tsunami). Use placeholder
   text for these three headings in Sprint 1. The structural scaffold and section IDs are
   unblocked; only the heading strings await Graeme. This does not block item 2 from being
   coded and tested — use placeholder strings.

3. Wiring in the `POST /skeletons` FastAPI route: parse `SkeletonRequest`, call
   `activate_sections`, pass result to `build_skeleton` via the existing builder chain.

4. Audit log extension: include `section_flags` and `activated_sections` in the generation
   audit log entry (per AC2d).

5. Tests for all 6 architectural constraints listed above, plus at least one happy-path
   integration test covering a full request body. Additional test cases required for the
   resolved mapping decisions:
   - Assert `SLOPE_INSTABILITY` produces section IDs `7.5`, `7.7`, and `7.13`.
   - Assert `OTHER` absent from hazards list produces no `7.15` sub-section.
   - Assert `FAULT_RUPTURE` produces `7.NZ-1` (not routed to `7.15`, not a no-op).
   - Assert `COMPRESSIBLE_SOILS` produces `7.4` (not `7.12` Subsidence).
   - Assert `FALLING_DEBRIS` produces `7.11` independently of `SLOPE_INSTABILITY`.
