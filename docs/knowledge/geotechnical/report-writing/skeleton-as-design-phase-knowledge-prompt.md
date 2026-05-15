# Skeleton Generator as Design-Phase Knowledge Prompt

**Sub-domain**: report-writing
**Last verified**: 2026-05-14
**Confidence**: cross-referenced
**Sources**: Geotechnical Engineering Checklists notebook, Engineering Standards notebook,
Geotechnical Report Workflows notebook, practitioner judgment (Graeme)

## Summary

The report skeleton generator currently produces document structure. The founder proposed
extending it to nominate applicable standards, generate pre-investigation checklists, and
flag mandatory report clauses for a given project type. This document assesses the domain
validity of that proposal and provides a concrete example for a residential earthworks GIR.
The extension is valid, well-grounded in existing NZ practice tools (NZGS 0200 Volume 2,
CERT 10a, TDOT 1GT2), and would close the largest class of documentation failure seen in
both engineer-authored and AI-generated reports.

---

## Key Facts

### 1. Senior engineers already carry this mental model

1. A senior geotechnical engineer who has written fifty residential earthworks GIRs
   knows immediately which standards apply. This knowledge is externalised in large firms
   through two channels: firm template libraries with embedded standard references, and the
   Project Director's skeleton approval gate (sense check). Neither channel exists reliably
   in small firms without a senior engineer layer.

2. The NZGS provides a "Volume 2 – Project Specific Requirements" template completed by
   the client and geotechnical professional before a project begins, defining which aspects
   of the specification apply and mandating additions [Checklists-1]. This is the NZGS's
   own formalisation of the same mental model.

3. The TDOT (Tennessee DOT) uses a pre-investigation checklist called "1GT2 Develop
   Geotechnical Work Plan" that verifies: design plans gathered, land use history checked,
   initial field visit done, seismic information assessed, project type and mitigation
   strategies identified [Checklists-2,3,4]. This confirms the design-phase checklist
   pattern is standard practice in mature geotechnical organisations.

4. For NZ residential and commercial investigations, NZGS 0200 mandates a formal desktop
   study stage — collecting hazard maps, liquefaction maps, national fault database, well
   records, historical aerial photographs — before any fieldwork [Checklists-5,6,7]. This
   is a codified pre-investigation checklist, though not labelled as such.

### 2. Mandatory standards for a residential earthworks GIR (NZ)

The following standards are mandatory (not optional) for a residential earthworks GIR in NZ.
They must be cited in the report:

| Standard | What it governs | Status |
|---|---|---|
| NZS 4431:2022 | Code of practice for earth fill for residential development — fill quality, compaction levels, inspection, Statement of Suitability | **Mandatory**. No exceptions |
| NZS 3604:2011 | Timber-framed buildings — foundation types and bearing requirements | **Mandatory** if residential buildings included |
| NZS 4404:2010 | Land development and subdivision infrastructure | **Mandatory** for subdivision |
| NZS 4402:1986 | Soil testing methods — **testing methodology only, NOT the compliance framework** | **Mandatory as method reference. Must NOT be cited as compliance standard** |
| NZGS 0200 | Ground investigations specification | **Mandatory** — governs SI conduct |
| NZS 1170.5:2004 | Earthquake actions — seismic hazard factor Z and site subsoil class | **Mandatory** for all NZ sites with seismic considerations |
| NZGS Module 3 | Liquefaction hazard identification, assessment, and mitigation | **Mandatory** where liquefaction screening is required |

Regional additions:
- **MBIE Canterbury Part D** — mandatory if site is in Canterbury
- **Auckland Council Earthworks and Geotechnical Code of Practice Chapter 2** — mandatory
  if site is in Auckland [Engineering Standards-13]

Sources: Engineering Standards notebook [citations 1–4]; Geotechnical Engineering Checklists
notebook [citation 12].

### 3. Design-phase checks the skeleton should prompt (residential earthworks)

These are work items, not report sections. The skeleton prompts them before fieldwork begins:

1. **Desktop study** — existing borehole/CPT data (NZGD), hazard maps (liquefaction, flood,
   tsunami, landslide), national fault database, well records, historical aerial photographs,
   HAIL (Hazardous Activities and Industries List) records [Checklists-5,6,7]
2. **Site walkover** — topographic assessment, surface drainage, existing fill identification,
   slope angles, access constraints [Checklists-7,8]
3. **Liquefaction screening** — CPT or SPT programme, groundwater depth, NZGS Module 3
   methodology application
4. **Slope stability check** — required if terrain > 3° or retaining walls > 1.5 m
5. **Existing fill identification** — engineered vs non-engineered; extent, nature, suitability
   [Checklists-9]
6. **Bearing capacity assessment** — ULS and SLS bearing pressures for proposed foundation
7. **Site subsoil class determination** — per NZS 1170.5 Table 3.1

### 4. Mandatory report clauses (residential earthworks GIR)

These clauses must appear regardless of project specifics, per IDS Clause 4.3.4 and 4.3.5:

1. Liquefaction and lateral spread assessment — explicit analysis, not a dismissal
2. Rockfall, cliff collapse, landslide hazard assessment — even if result is "no hazard"
3. Slope stability assessment confirming building site suitability
4. Ground bearing capacity with documented factors of safety
5. Design assumptions and factors of safety, explicitly listed [Engineering Standards-6]
6. Statement of Professional Opinion on Suitability for Subdivision — signed, per IDS
   Appendix I [Engineering Standards-6]
7. Earthworks specification — fill materials, compaction criteria, site preparation, fill
   drawings [Checklists-9,10]
8. Compaction testing methodology with correct NZS 4402 clause reference
   (NZS 4402.4.1.1 standard compaction; NZS 4402.4.1.3 vibrating hammer)
9. Reference to future Geotechnical Completion Report deliverable (IDS Clause 4.3.6)
   [Engineering Standards-7,8,9]

### 5. Gap closure — Case 2 (good engineering, wrong documentation)

5. A skeleton-generated standards list prevents the largest class of documentation error:
   omission of a mandatory standard. If "NZS 4431:2022" is pre-populated in the skeleton's
   earthworks section, the engineer must actively delete it to miss it. The Claude demo's
   most serious error — complete absence of NZS 4431 from a residential earthworks report —
   is structurally prevented.

6. The skeleton prevents omissions. Redline's citation checker (CITE-EXIST-01) catches
   transcription and hallucination errors within citations. These are complementary, not
   overlapping functions.

### 6. Gap closure — Case 1 (AI-generated report, wrong citations)

7. When the skeleton's standards list is injected as a constraint into the AI prompt, Claude's
   output is bounded. It cannot omit NZS 4431. It cannot cite NZS 4402 as a compliance
   framework if the skeleton explicitly labels it as "testing methodology only". The risk of
   hallucinating irrelevant standards (e.g., NZS 4407 for SPT testing) drops because the
   correct standard space has been defined.

8. Constraint injection via skeleton reduces Claude's degrees of freedom in the domain where
   unlimited degrees of freedom produce wrong answers. It does not prevent hallucination of
   clause numbers *within* a nominated standard.

### 7. What the skeleton cannot do (hard boundary)

9. The skeleton nominates standards. It cannot verify that the engineer applied them correctly:
   - Cannot verify that the FS calculation used correct shear strength parameters
   - Cannot verify that NZS 1170.5 site subsoil class is correct for the actual site
   - Cannot verify that compaction tests were actually run or results are genuine
   - Cannot verify that the signing engineer is an Approved Geoprofessional

10. The skeleton and citation checker together enforce structural completeness and citation
    integrity. They do not enforce engineering correctness. Engineering correctness requires
    a human reviewer — either a senior engineer or a Regulatory Peer Review for high-risk
    projects.

11. Redline's value is raising the floor of documentation quality so the human reviewer can
    spend their time on engineering correctness rather than hunting for missing clauses and
    wrong standard numbers. That is a real and large value. It is also a finite one.

---

## Standards Referenced

- NZS 4431:2022 — Code of practice for earth fill for residential development
- NZS 4431:1989 — Superseded edition (pre-2022 projects)
- NZS 3604:2011 — Timber-framed buildings
- NZS 4404:2010 — Land development and subdivision infrastructure
- NZS 4402:1986 — Methods of testing soils for civil engineering purposes
- NZS 1170.5:2004 — Structural design actions — earthquake actions
- NZGS 0200 — Ground investigations specification (3 volumes)
- NZGS Module 3 — Guideline for identification, assessment and mitigation of liquefaction hazards
- MBIE Canterbury Part D — Guidelines for geotechnical investigation of subdivisions in Canterbury
- Auckland Council Earthworks and Geotechnical Code of Practice Chapter 2
- IDS (Christchurch City Council Infrastructure Design Standard) Clauses 4.3.4, 4.3.5, 4.3.6

---

## Open Questions

1. **Clause-level hallucination within nominated standards** — the skeleton prevents standard
   omission and standard confusion, but does not prevent Claude from fabricating clause numbers
   within a correctly nominated standard. Whether Redline's citation checker can catch this
   depends on whether clause-level verification is feasible against the standards corpus.

2. **Regional overlays at scale** — the mandatory standard set varies by territorial authority
   (Auckland, Canterbury, GWRC, etc.). The skeleton must know the project location to apply
   the correct regional overlay. This requires the location to be a dropdown input parameter
   at skeleton generation time.

3. **NZS 4431:2022 clause coverage** — the notebook sources confirm NZS 4431:2022 is the
   current edition and the governing framework. The specific internal clause structure of
   the 2022 edition (what changed from 1989) is not fully covered in sources. Needs
   ingestion into the Engineering Standards notebook.

---

## Further Reading

- NZGS 0200 Volume 2 (Project Specific Requirements template) — available from NZGS website
- CERT 10a Guide for Geotechnical Report (New Zealand) — present in Checklists notebook
- TDOT 1GT2 Develop Geotechnical Work Plan checklist — present in Checklists notebook
- IDS (Christchurch City Council Infrastructure Design Standard) Clauses 4.3.4–4.3.6 —
  present in Engineering Standards notebook
