# Design Type Taxonomy and Parameter Completeness Requirements

**Status**: validated (structure); draft (parameter sets)
**Owner**: Graeme (Principal Geotechnical Engineer)
**Last updated**: 2026-05-04
**Provenance**: Parameter completeness advisory session, 2026-05-04; original notebook
research 2026-05-04
**Sub-domain**: report-writing
**Confidence**: cross-referenced
**Sources**: Geotechnical Report Workflows, Engineering Standards, Ground Engineering Magazine,
Risk Assessment in Engineering

## Summary

Parameter completeness checking requires a taxonomy of geotechnical design types because
parameter requirements are non-overlapping across design categories and sub-types. The
notebook sources confirm eleven top-level design categories with approximately thirty
sub-types, each with distinct required parameters. Geographic variation (particularly
Canterbury vs the rest of NZ) adds a regional overlay of additional requirements driven
by local geology, seismicity, and post-earthquake regulatory frameworks (see
regional-parameter-overlays.md).

Five design types represent the Pareto 20% by report volume for a typical NZ/AU
geotechnical consultancy: shallow foundations, timber pole retaining walls, slope
stability, liquefaction assessment, and piled foundations. These are prioritised for
parameter set validation.

## The Common Kernel

All geotechnical design types share a small set of site-level parameters. These form
the common kernel that appears in every geotechnical report regardless of design type:

| Parameter | Notes |
| --- | --- |
| Groundwater level (and datum) | Measured or assumed; seasonal variation if relevant |
| Seismic hazard factor (Z) | Per NZS 1170.5 for site location |
| Site subsoil class | Per NZS 1170.5 (A through E) |
| Soil profile summary | Layer sequence, thicknesses, descriptions |
| Site location and coordinates | NZTM or lat/long |
| Topographic context | Slope, aspect, proximity to waterways or cliffs |

The common kernel is always required. Design-type-specific parameters are additional.

## Pareto 20% -- Priority Design Types

The following five design types are estimated to represent approximately 80% of report
volume for a typical NZ residential/light commercial geotechnical consultancy. These
are prioritised for parameter set development and validation. Marked with **(P)** in
the taxonomy below.

1. Shallow foundations (strip footings, pad footings)
2. Timber pole retaining walls
3. Slope stability assessment
4. Liquefaction assessment
5. Piled foundations (driven timber piles)

This estimate is practitioner-grounded and needs validation against actual firm
production data.

## Design Type Taxonomy

### 1. Foundations -- Shallow

| Sub-type | Pareto | Parameter set status |
| --- | --- | --- |
| Strip footings | **(P)** | draft |
| Pad footings | **(P)** | draft |
| Raft foundations | | not started |

**Draft parameter set (shallow foundations -- strip/pad footings):**

Inputs: applied loads (dead, live, seismic, wind), soil bearing parameters (cohesion,
friction angle or SPT/CPT correlation), groundwater level, foundation depth below
ground level, seismic hazard factor (Z), site subsoil class, soil profile (layer
thicknesses and properties), acceptable differential settlement limit.

Outputs: allowable bearing capacity (SLS and ULS), recommended footing dimensions,
expected settlement (total and differential), subgrade preparation requirements,
factor of safety against bearing failure.

### 2. Foundations -- Deep

| Sub-type | Pareto | Parameter set status |
| --- | --- | --- |
| Bored piles | | not started |
| Driven timber piles | **(P)** | draft |
| Screw piles | | not started |
| CFA (Continuous Flight Auger) piles | | not started |

**Draft parameter set (driven timber piles):**

Inputs: applied loads (axial, lateral), soil profile with layer properties, groundwater
level, seismic hazard factor (Z), site subsoil class, pile material grade,
target founding stratum.

Outputs: pile diameter, pile length, design capacity (axial and lateral), strength
reduction factor, stiffness, estimated settlement, set criteria (if driven),
minimum embedment into bearing stratum.

### 3. Retaining Structures

| Sub-type | Pareto | Parameter set status |
| --- | --- | --- |
| Timber pole walls | **(P)** | validated |
| RC cantilever walls | | draft |
| Anchored sheet piles | | not started |
| MSE (Mechanically Stabilised Earth) walls | | not started |
| Crib walls | | not started |

**Validated parameter set (timber pole retaining walls):**

Inputs: retained height, soil unit weight, angle of internal friction, cohesion (if
applicable), groundwater level, surcharge loading, seismic acceleration coefficient,
backfill properties, slope above/below wall.

Outputs: pole diameter, pole embedment depth, pole spacing (centres), lagging type
and size, drainage specification (type, location, outlet), whether anchors are
required, anchor specification (if required), factor of safety (overturning), factor
of safety (sliding), total and damaged face area.

Source: [GRW: Source 44, 46]. This parameter set was confirmed against the
Geotechnical Report Workflows notebook.

**Draft parameter set (RC cantilever walls):**

Inputs: retained height, soil unit weight, angle of internal friction, cohesion,
groundwater level, surcharge loading, seismic acceleration coefficient, backfill
properties, allowable bearing pressure at toe, passive resistance at toe.

Outputs: base width, toe length, heel length, wall stem thickness, toe thickness,
active earth pressure, passive earth pressure, pressure coefficient at rest,
sliding resistance, overturning moment, bearing pressures (maximum, minimum,
average), factor of safety (sliding), factor of safety (overturning), factor of
safety (bearing), reinforcement schedule reference.

Source: [GRW: Source 45, 47-53]. Note: RC cantilever wall parameters share almost
no overlap with timber pole wall parameters, confirming that sub-type-level
parameter sets are essential.

### 4. Slope Stability

| Sub-type | Pareto | Parameter set status |
| --- | --- | --- |
| Natural slope assessment | **(P)** | draft |
| Cut slope design | **(P)** | draft |
| Fill slope design | | not started |
| Coastal cliff stability | | not started |

**Draft parameter set (slope stability -- general):**

Inputs: slope geometry (height, angle, benches, crest setback), geological unit
boundaries, shear strength parameters per unit (effective cohesion c', effective
friction angle phi', undrained shear strength Su), piezometric conditions (water
table, pore pressure distribution), surcharge loading, seismic acceleration
coefficient, rainfall/infiltration assumptions, slope material unit weights.

Outputs: factor of safety (static), factor of safety (seismic), factor of safety
(rapid drawdown, if applicable), critical failure surface location and type
(circular, non-circular, planar), remedial measures (if FoS inadequate), monitoring
requirements, acceptable building setback from crest/toe.

Source: [GRW: Source 12-19]. Confirmed against Stability Analysis Review Checklist.

### 5. Soil Reinforcement

| Sub-type | Pareto | Parameter set status |
| --- | --- | --- |
| Soil nails | | not started |
| Ground anchors (grouted) | | not started |
| Mechanical anchors | | not started |

Known parameters from notebooks: pull-out capacity, tensile capacity, bond strength,
anchor length, inclination, corrosion protection specification [GRW: Source 14, 20-26].
Full parameter sets not yet assembled.

### 6. Liquefaction Assessment

| Sub-type | Pareto | Parameter set status |
| --- | --- | --- |
| Triggering analysis | **(P)** | draft |
| Consequence assessment | **(P)** | draft |

**Draft parameter set (liquefaction triggering):**

Inputs: SPT N-values or CPT qc profiles, fines content, soil profile, groundwater
level, peak ground acceleration (PGA), earthquake magnitude, site subsoil class,
seismic hazard factor (Z), return period.

Outputs: cyclic resistance ratio (CRR), cyclic stress ratio (CSR), factor of safety
against liquefaction (per layer), Liquefaction Potential Index (LPI), Liquefaction
Severity Number (LSN), lateral spread potential, estimated settlement from
liquefaction.

Regional overlay: Canterbury requires LR Index zone classification and
MBIE-specific assessment methodology (see regional-parameter-overlays.md).

### 7. Settlement Analysis

| Sub-type | Pareto | Parameter set status |
| --- | --- | --- |
| Elastic (immediate) settlement | | not started |
| Consolidation settlement | | not started |
| Secondary compression (creep) | | not started |

Known parameters from notebooks: consolidation parameters (Cc, Cr, Cv, e0),
preconsolidation pressure, layer thicknesses, drainage path lengths, applied stress
increment, compressibility modulus [GRW: Source 40-43]. Full parameter sets not yet
assembled.

### 8. Earthworks

| Sub-type | Pareto | Parameter set status |
| --- | --- | --- |
| Engineered fill | | not started |
| Stopbanks / levees | | not started |
| Landfill cells | | not started |

Known parameters from notebooks: compaction specification (MDD, OMC, % compaction),
fill material classification, seepage analysis parameters, filter compatibility
criteria [GRW: Source 27-35]. Full parameter sets not yet assembled.

### 9. Coastal Protection

| Sub-type | Pareto | Parameter set status |
| --- | --- | --- |
| Rock revetments | | not started |
| Gravel beaches | | not started |
| Sea walls | | not started |

Known parameters from notebooks: relative sea level rise (RSLR), vertical land
movement (VLM), Average Recurrence Interval / Annual Exceedance Probability
(ARI/AEP), damage parameter (Sd), overtopping rate [GRW: Source 54-56]. Full
parameter sets not yet assembled.

### 10. Ground Improvement

| Sub-type | Pareto | Parameter set status |
| --- | --- | --- |
| Stone columns | | not started |
| Deep soil mixing | | not started |
| Dynamic compaction | | not started |
| Grouting | | not started |

Known parameters from notebooks: treatment depth, column diameter and spacing,
area replacement ratio, target post-improvement soil properties [GRW: Source 57-59].
Full parameter sets not yet assembled.

### 11. Rockfall / Mass Movement

| Sub-type | Pareto | Parameter set status |
| --- | --- | --- |
| Boulder roll | | not started |
| Cliff collapse | | not started |
| Landslip | | not started |

Known parameters from notebooks: run-out distance, boulder kinetic energy, block
size, slope angle, barrier requirements [Eng Stds: Source 9, 11, 17-20].
Full parameter sets not yet assembled.

Canterbury-specific: GNS Science hazard reports required for Port Hills sites.
PS1/PS2a/PS4 Producer Statements for rockfall protection design.

## Design Types Missing from Notebooks but Present in Practice

The following design types are commonly encountered in NZ/AU geotechnical practice but
are not represented in the current notebook corpus:

- **Dewatering design**: temporary and permanent dewatering systems, pump rates, drawdown
  calculations, settlement from dewatering
- **Retaining wall drainage design**: subsoil drainage behind walls, weep holes,
  drainage blankets -- often treated as part of retaining wall design but has its own
  parameter set
- **Pavement subgrade assessment**: CBR, subgrade modulus, pavement design inputs for
  roading projects
- **Contaminated land assessment**: not strictly geotechnical design but frequently
  addressed in the same reports, with its own parameter requirements (NES-CS, CLMG
  guidelines)

These represent gaps in the taxonomy that should be filled from firm procedures or
standards research.

## Key Facts (Contextual)

### EC7 Part 2 -- parameter-orientated restructuring

The second generation of Eurocode 7 restructures the standard from two parts to three:

- Part 1: General rules (basis of design)
- Part 2: renamed from "Ground investigation and testing" to "Ground properties" --
  now orientated towards obtaining parameters rather than describing investigation
  methods [Ground Eng: Source 1-5]
- Part 3: Geotechnical structures (new) -- specific design rules for slopes, spread and
  piled foundations, retaining structures, anchors, reinforced fill [Ground Eng: Source 6]

Industry leaders describe this as "a really positive change" because "focusing on the
parameters engineers actually need is much more logical from a designer's perspective"
[Ground Eng: Source 1, 5].

Supporting technical guidelines have been published including "Assembling the ground model
and the derived values" [Ground Eng: Source 7].

The AGSi digital format now enables transfer of interpreted ground models and design
parameters electronically [Ground Eng: Source 8-10].

### Where parameter checklists actually come from

Sources confirm a three-layer structure (see also parameter-completeness-checking-standard-of-care.md):

1. **Standards and codes** (NZS, EC7, IDS): high-level requirements, not exhaustive lists
2. **Firm procedures and templates**: GIR templates, stability analysis checklists,
   review checksheets -- closest to codifiable parameter lists
3. **Professional judgment**: the designer selects which parameters are relevant to the
   specific project context, soil conditions, and design method

### Over-inclusion is a documented failure mode

Corporate guidance explicitly states: "many of our reports are too wordy and complex"
and include "information which is not relevant to the reader" [GRW: Source 4]. The
preferred approach is to exclude detailed parameter derivations from the report body and
ensure they are "well documented in calculations on [firm] files" [GRW: Source 6, 7].

## Standards Referenced

- Eurocode 7 (EC7) -- current and second generation (EN 1997-1, -2, -3)
- Christchurch IDS -- Infrastructure Design Standard (geotechnical sections)
- MBIE Part D -- Guidelines for geotechnical investigation of subdivisions in Canterbury
- NZS 1170.5 -- Structural Design Actions (seismic)
- AS 2159-2009 -- Piling -- Design and Installation
- GNS Science rockfall/cliff collapse reports (Canterbury-specific)
- NES-CS -- National Environmental Standard for Assessing and Managing Contaminants
  in Soil to Protect Human Health (for contaminated land gap)

## Open Questions

1. Which design types represent the Pareto 20% by report volume? The current estimate
   (shallow foundations, timber pole retaining walls, slope stability, liquefaction
   assessment, piled foundations) is practitioner-grounded but needs validation against
   actual firm production data.

2. Beyond Canterbury, what Auckland-specific or Wellington-specific geotechnical
   requirements exist? (See regional-parameter-overlays.md for current state of this gap.)

3. Does the second-generation EC7 Part 2 provide a usable, codifiable structure for
   building design-type-specific parameter checklists?

4. How do Australian state-level variations (e.g., Queensland vs Victoria vs NSW)
   compare to the NZ regional variation pattern?

5. For design types marked "not started", which should be prioritised next after the
   Pareto five? Likely candidates: RC cantilever walls (already draft), raft foundations,
   bored piles, ground anchors.

6. Should dewatering, pavement subgrade, and contaminated land be added as top-level
   categories or as sub-types within existing categories?

## Further Reading

- MBIE, *Repairing and rebuilding houses affected by the Canterbury earthquakes*,
  Parts A-D -- Canterbury-specific geotechnical guidance
- AGS/FPS, *Effective Procurement of Ground Investigations* -- parameter requirements
  from the client/procurement perspective
- CIRIA C760, *Guidance on embedded retaining wall design* -- may contain parameter
  checklists for retaining wall design documentation
- EC7 second generation supporting technical reports -- "Assembling the ground model
  and the derived values" (published by TC250/SC7)
- FPS guidance on minimum site investigation information for piling (forthcoming)

## Related Documents

- [regional-parameter-overlays.md](regional-parameter-overlays.md) -- regional modifiers
  layered on top of design-type parameter sets
- [input-vs-output-parameters.md](input-vs-output-parameters.md) -- input/output
  classification of parameters
- [parameter-completeness-scope-statement.md](parameter-completeness-scope-statement.md) --
  canonical scope statement for parameter completeness checking
- [parameter-completeness-checking-standard-of-care.md](parameter-completeness-checking-standard-of-care.md) --
  legal and professional basis for checking
