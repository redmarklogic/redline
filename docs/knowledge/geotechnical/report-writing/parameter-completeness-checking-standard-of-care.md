# Parameter Completeness Checking and Standard of Care

**Status**: validated
**Owner**: Graeme (Principal Geotechnical Engineer)
**Last updated**: 2026-05-04
**Provenance**: Original notebook research 2026-05-04; confirmed in parameter
completeness advisory session, 2026-05-04
**Sub-domain**: report-writing
**Confidence**: cross-referenced
**Sources**: Geotechnical Report Workflows, Risk Assessment in Engineering, Engineering Standards, Ground Engineering Magazine

## Summary

Checking that a geotechnical design report mentions all required input and output
parameters (without validating their numeric values) is a legitimate quality-assurance
concern that contributes to meeting the engineering standard of care. However, the problem
is nuanced: standards mandate documentation of key assumptions and design parameters, but
do not provide exhaustive per-design-type checklists of individual parameters. The
parameter lists are partially codifiable from standards, but require firm-specific and
project-specific augmentation. Incomplete documentation is a known source of professional
liability.

## Key Facts

### 1. Parameter completeness contributes to standard of care

1. The standard of care is the legal benchmark for measuring negligence: providing the
   level of skill, care, and diligence ordinarily exercised by members of the engineering
   profession currently practising under similar conditions [Risk Assessment: Source 1, 2].
   It does not require perfection, but failure to conform to generally accepted professional
   standards is strong evidence of negligence [Risk Assessment: Source 8].

2. While exhaustive completeness of every possible parameter is not required (and is
   actively discouraged in some contexts like GBRs), the omission of "vital" or
   "necessary" information does constitute a breach of standard of care. Courts have
   ruled that it is the duty of an engineer to note when components "vital to the
   integrity" of a structure are absent [Risk Assessment: Source 11].

3. The IDS (Christchurch Infrastructure Design Standard) requires that the Design Report
   include "the constraints, parameters, assumptions and raw data on which the design is
   based" [Engineering Standards: Source 10]. Design records must "enable the process to
   be followed easily and should allow for replication of the results" [Engineering
   Standards: Source 12].

### 2. Engineers do miss parameters — and the consequences are real

4. Case law demonstrates clear liability from omitted information:
   - *Unit Farm Concrete Products Ltd v Eckerlea Acres Ltd*: An engineer failed to note
     the complete absence of a rebar schedule — a component vital to wall integrity. Found
     negligent [Risk Assessment: Source 11].
   - *Brown & Huston Ltd v City of York*: Consulting engineers were held 75% liable for
     omitting a soils report and groundwater level information from a tender package [Risk
     Assessment: Source 12, 17].
   - *Mawson Gage Associates Ltd v R*: Missing pages of specifications from tender details
     led to a successful tort claim for negligent misrepresentation [Risk Assessment:
     Source 18].

5. However, the Geotechnical Report Workflows notebook notes the opposite problem is also
   common: "many of our reports are too wordy and complex" and include "information which
   is not relevant to the reader" [GRW: Source 4]. Over-inclusion and under-inclusion are
   both failure modes.

### 3. Parameter lists are partially codifiable

6. The Stability Analysis Review Checklist requires checking: slope geometry, geological
   unit boundaries, material parameters (cohesion, friction angle, undrained shear
   strength), piezometric conditions, surcharge loading, and seismic accelerations [GRW:
   Source 1].

7. For retaining walls (NHI Act context), required parameters include: length, retained
   height, pole embedment depth/size/centres, lagging size, drainage, anchors, and safety
   barriers [GRW: Source 3].

8. For foundation piles, the GIR template prompts: bearing capacity, strength reduction
   factor, and stiffness [GRW: Source 6].

9. For rockfall mitigation, the IDS requires: run-out distances and kinetic energy of
   boulders at the site [Engineering Standards: Source 9].

10. The PS1 (Producer Statement — Design) template for rockfall protection requires
    explicit listing of "Inputs to the Design (Standards and codes used)" and "Rockfall
    Energy used and its derivation/supply" [Engineering Standards: Source 11].

### 4. But no universal checklist exists in standards

11. NZ standards do not provide an exhaustive, itemised list of exact parameters that must
    be documented for common geotechnical designs. They mandate high-level requirements
    like "key achievement criteria and assumptions... such as the chosen factors of safety"
    [Engineering Standards: Source 5].

12. Eurocode 7 does not currently prescribe parameter checklists either, but the
    forthcoming second generation of EC7 will restructure Part 2 to be "orientated towards
    parameters" rather than investigation methods — which industry leaders consider "much
    more logical from a designer's point of view" [Ground Eng: Source 3].

13. The Federation of Piling Specialists (FPS) is actively working to produce "clear,
    concise guidance on minimum site investigation information required for effective
    piling solutions" [Ground Eng: Source 4].

14. The AGS (Association of Geotechnical and Geoenvironmental Specialists) published
    *Effective Procurement of Ground Investigations* to ensure "the required data is
    obtained to meet project objectives" [Ground Eng: Source 5].

### 5. Where parameter checklists come from in practice

15. Sources for parameter checklists are layered:
    - **Standards and codes** (NZS, EC7, IDS): high-level requirements, not exhaustive lists
    - **Firm procedures and templates**: GIR templates, stability analysis checklists,
      review checksheets — these are the closest to codifiable parameter lists
    - **Professional judgment**: the designer selects which parameters are relevant to the
      specific project context, soil conditions, and design method

### 6. Critical nuance: where parameters live in the report

16. Corporate guidance actively encourages engineers to keep reports concise by leaving
    detailed parameter derivations out of the main text. The preferred approach is:
    "Exclude and ensure well documented in calculations on [firm] files" [GRW: Source 6, 7].
    A "complete" design deliverable often splits the final outputs (which go in the report)
    from the detailed inputs (which remain in internal calculation files).

## Standards Referenced

- Eurocode 7 (EC7) — Geotechnical design (current and forthcoming second generation)
- Christchurch IDS — Infrastructure Design Standard (geotechnical sections)
- NHI Act — Natural Hazards Insurance Act (NZ)
- Various NZ Producer Statement (PS1) templates

## Open Questions

1. What would a "minimum viable" parameter checklist look like for the five most common
   residential geotechnical designs in NZ (timber pole retaining walls, concrete
   cantilever walls, shallow foundations, piled foundations, slope stability assessments)?

2. How do other NZ/AU firms structure their internal QA checksheets for parameter
   completeness — is there convergence or divergence in what they check?

3. Should the completeness check distinguish between parameters that must appear in the
   report body versus parameters that may legitimately reside only in calculation files?

4. Does the forthcoming EC7 Part 2 (parameter-orientated) provide a usable structure for
   codifying parameter checklists?

## Further Reading

- AGS et al., *Effective Procurement of Ground Investigations* (Emerald Publishing) —
  I have not verified this source, but it may contain parameter completeness guidance
  from the client's perspective.
- FPS guidance on minimum site investigation information for piling (forthcoming) —
  I have not verified whether this has been published yet.
- CIRIA C760, *Guidance on embedded retaining wall design* — may contain parameter
  checklists for retaining wall design documentation.
- Eurocode 7 second generation (EN 1997, next edition) — the restructured Part 2
  orientated towards parameters may provide a codifiable framework.
