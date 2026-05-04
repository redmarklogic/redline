# Design Type Taxonomy and Parameter Completeness Requirements

**Sub-domain**: report-writing
**Last verified**: 2026-05-04
**Confidence**: cross-referenced
**Sources**: Geotechnical Report Workflows, Engineering Standards, Ground Engineering Magazine,
Risk Assessment in Engineering

## Summary

Parameter completeness checking requires a taxonomy of geotechnical design types because
parameter requirements are non-overlapping across design categories and sub-types. The
notebook sources confirm at least nine top-level design categories, each with distinct
required parameters. Geographic variation (particularly Canterbury vs the rest of NZ)
adds a regional overlay of additional requirements driven by local geology, seismicity,
and post-earthquake regulatory frameworks.

## Key Facts

### 1. Design type taxonomy — top-level categories from NZ practice

The following categories are confirmed in the Geotechnical Report Workflows notebook
as distinct design types with non-overlapping parameter sets:

1. **Foundations** — subdivides into shallow foundations (bearing capacity, settlement),
   bored piles, driven timber piles, screw piles [GRW: Source 1-4]
2. **Slope stability** — static, seismic, and temporary conditions with distinct
   geometry, material, and loading parameters [GRW: Source 12-19]
3. **Soil reinforcement and ground anchors** — soil nails, mechanical anchors, grouted
   anchors with pull-out, tensile, and bond parameters [GRW: Source 14, 20-26]
4. **Earthworks, landfills, stopbanks, and dams** — characterisation, compaction,
   seepage, filter compatibility [GRW: Source 27-35]
5. **Liquefaction assessment** — PGA, CRR, CSR, LPI, LSN [GRW: Source 36-39]
6. **Settlement analysis** — consolidation, compaction data, shear strength [GRW: Source 40-43]
7. **Retaining structures** — timber pole walls vs concrete abutments have completely
   different parameter sets [GRW: Source 44-53]
8. **Coastal protection** — RSLR, VLM, ARI/AEP, damage parameter, overtopping [GRW: Source 54-56]
9. **Ground improvement** — CFA grouting, stone columns, deep soil mixing, dynamic
   compaction [GRW: Source 57-59]

### 2. Sub-type differentiation — retaining walls example

Within "retaining structures," the sources confirm fundamentally different parameter sets:

- **Timber pole retaining wall**: length, retained height, pole embedment depth/size/centres,
  lagging size, drainage, anchors, total/damaged face area [GRW: Source 44, 46]
- **Concrete cantilever abutment**: toe thickness, base width, active and passive earth
  pressures, pressure coefficient at rest, sliding resistance, overturning moment,
  bearing pressures (maximum, minimum, average) [GRW: Source 45, 47-53]

These parameter sets share almost no overlap — confirming the founder's point that
even within a single category, sub-types require distinct parameter checklists.

### 3. Geographic variation — Canterbury vs rest of NZ

Canterbury imposes additional requirements not applicable elsewhere:

- **MBIE earthquake rebuild guidelines** — mandatory for Canterbury, not applicable
  nationally [Eng Stds: Source 1-2]
- **Liquefaction vulnerability mapping** — Canterbury uses a specific vulnerability map
  and Liquefaction Resistance (LR) Index zoning system (LR 0-4). LR zones 0-1 mandate
  polyethylene pipes; LR zones 0-2 require geotextile-wrapped haunching [Eng Stds: Source 5-11]
- **Subdivision on liquefaction-prone land** — MBIE Part D guidelines are
  Canterbury-specific [Eng Stds: Source 3-4]
- **Port Hills rockfall/cliff collapse** — Canterbury-specific GNS Science hazard
  reports, Canterbury-specific Producer Statement templates (PS1, PS2a, PS4) for
  rockfall protection design [Eng Stds: Source 17-20]
- **Port Hills loess soils** — dispersive volcanic soils requiring lime treatment;
  winter earthworks ban (1 May - 31 August) [Eng Stds: Source 12-16]
- **Christchurch Drainage Datum (CDD)** — unique local elevation datum instead of
  national LINZ datum [Eng Stds: Source 21]
- **Council-specific requirements** — "Specific requirements of each Council may differ"
  [GRW: Source 1]

### 4. EC7 Part 2 — parameter-orientated restructuring

The second generation of Eurocode 7 restructures the standard from two parts to three:

- Part 1: General rules (basis of design)
- Part 2: renamed from "Ground investigation and testing" to "Ground properties" —
  now orientated towards obtaining parameters rather than describing investigation
  methods [Ground Eng: Source 1-5]
- Part 3: Geotechnical structures (new) — specific design rules for slopes, spread and
  piled foundations, retaining structures, anchors, reinforced fill [Ground Eng: Source 6]

Industry leaders describe this as "a really positive change" because "focusing on the
parameters engineers actually need is much more logical from a designer's perspective"
[Ground Eng: Source 1, 5].

Supporting technical guidelines have been published including "Assembling the ground model
and the derived values" [Ground Eng: Source 7].

The AGSi digital format now enables transfer of interpreted ground models and design
parameters electronically [Ground Eng: Source 8-10].

### 5. Where parameter checklists actually come from

Sources confirm a three-layer structure (see also parameter-completeness-checking-standard-of-care.md):

1. **Standards and codes** (NZS, EC7, IDS): high-level requirements, not exhaustive lists
2. **Firm procedures and templates**: GIR templates, stability analysis checklists,
   review checksheets — closest to codifiable parameter lists
3. **Professional judgment**: the designer selects which parameters are relevant to the
   specific project context, soil conditions, and design method

### 6. Over-inclusion is a documented failure mode

Corporate guidance explicitly states: "many of our reports are too wordy and complex"
and include "information which is not relevant to the reader" [GRW: Source 4]. The
preferred approach is to exclude detailed parameter derivations from the report body and
ensure they are "well documented in calculations on [firm] files" [GRW: Source 6, 7].

## Standards Referenced

- Eurocode 7 (EC7) — current and second generation (EN 1997-1, -2, -3)
- Christchurch IDS — Infrastructure Design Standard (geotechnical sections)
- MBIE Part D — Guidelines for geotechnical investigation of subdivisions in Canterbury
- NZS 1170.5 — Structural Design Actions (seismic)
- AS 2159-2009 — Piling — Design and Installation
- GNS Science rockfall/cliff collapse reports (Canterbury-specific)

## Open Questions

1. Which design types represent the Pareto 20% by report volume for a typical NZ/AU
   geotechnical consultancy? (Practitioner judgment suggests: shallow foundations,
   retaining walls, slope stability, liquefaction assessment, piled foundations — but
   this needs validation against actual firm production data.)

2. Beyond Canterbury, what Auckland-specific or Wellington-specific geotechnical
   requirements exist? (Auckland has volcanic soils and different seismicity;
   Wellington has active faults and high seismic hazard factors — but the notebooks
   do not contain Auckland or Wellington council-specific standards.)

3. Does the second-generation EC7 Part 2 provide a usable, codifiable structure for
   building design-type-specific parameter checklists?

4. How do Australian state-level variations (e.g., Queensland vs Victoria vs NSW)
   compare to the NZ regional variation pattern?

## Further Reading

- MBIE, *Repairing and rebuilding houses affected by the Canterbury earthquakes*,
  Parts A-D — Canterbury-specific geotechnical guidance
- AGS/FPS, *Effective Procurement of Ground Investigations* — parameter requirements
  from the client/procurement perspective
- CIRIA C760, *Guidance on embedded retaining wall design* — may contain parameter
  checklists for retaining wall design documentation
- EC7 second generation supporting technical reports — "Assembling the ground model
  and the derived values" (published by TC250/SC7)
