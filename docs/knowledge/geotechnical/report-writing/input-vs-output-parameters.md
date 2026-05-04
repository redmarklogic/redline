# Input vs Output Parameters in Geotechnical Design Reports

**Status**: draft
**Owner**: Graeme (Principal Geotechnical Engineer)
**Last updated**: 2026-05-04
**Provenance**: Parameter completeness advisory session, 2026-05-04

**Sub-domain**: report-writing
**Confidence**: practitioner-grounded

## Summary

Geotechnical design parameters fall into two distinct categories: input parameters
(what the designer uses as inputs to the design calculation) and output parameters
(what the designer produces as results). Both categories require completeness checking
but serve fundamentally different purposes. Input completeness prevents errors from
wrong assumptions propagating through calculations. Output completeness prevents
ambiguity for downstream parties (structural engineers, builders, contractors) who
depend on the geotechnical report to proceed with their work.

## Definitions

**Input parameters** are the values the geotechnical designer uses as inputs to the
design process. These include measured or interpreted soil properties, geometric
constraints, applied loads, groundwater conditions, and regulatory values (such as
seismic hazard factors). The designer obtains these from ground investigation data,
project briefs, structural loads schedules, or standards.

**Output parameters** are the values the geotechnical designer produces as results of
the design calculation. These include bearing capacities, factors of safety, settlement
magnitudes, embedment depths, and recommended construction specifications. The output
parameters are what downstream parties (structural engineers, contractors, building
consent authorities) consume from the report.

## Why Both Matter

### Input completeness prevents error propagation

If a designer omits or uses an incorrect input parameter, every output that depends on
it is wrong. A missing groundwater level assumption can invalidate a bearing capacity
calculation, a slope stability factor of safety, and a retaining wall design
simultaneously. Checking that all required inputs are documented (and stated explicitly
rather than assumed implicitly) is the first line of defence against propagated errors.

### Output completeness prevents downstream ambiguity

A geotechnical report that calculates bearing capacity but omits the recommended
foundation depth, or that analyses slope stability but does not state the minimum
factor of safety achieved, forces the structural engineer or contractor to either
guess or come back and ask. Incomplete outputs cause project delays, rework, and
potential construction errors when downstream parties make assumptions the geotechnical
designer did not intend.

## Examples by Design Type

### Timber pole retaining wall

| Category | Parameter | Notes |
| --- | --- | --- |
| Input | Retained height | From architectural/civil drawings |
| Input | Soil unit weight | From ground investigation |
| Input | Angle of internal friction | From ground investigation or correlation |
| Input | Groundwater level | From ground investigation |
| Input | Surcharge loading | From project brief or standards |
| Input | Seismic acceleration coefficient | From NZS 1170.5 for site location |
| Output | Pole diameter | Design output |
| Output | Pole embedment depth | Design output |
| Output | Pole spacing (centres) | Design output |
| Output | Lagging type and size | Design output |
| Output | Drainage specification | Design output |
| Output | Factor of safety (overturning) | Design output |
| Output | Factor of safety (sliding) | Design output |
| Output | Whether anchors are required | Design output |

### Shallow foundation (pad footing)

| Category | Parameter | Notes |
| --- | --- | --- |
| Input | Applied column loads (dead, live, seismic) | From structural engineer |
| Input | Soil bearing parameters (cohesion, friction angle) | From ground investigation |
| Input | Groundwater level | From ground investigation |
| Input | Foundation depth below ground level | From architectural/structural drawings |
| Input | Seismic hazard factor (Z) | From NZS 1170.5 |
| Input | Soil profile (layer thicknesses, properties) | From ground investigation |
| Output | Allowable bearing capacity (SLS and ULS) | Design output |
| Output | Recommended footing dimensions | Design output |
| Output | Expected settlement (total and differential) | Design output |
| Output | Subgrade preparation requirements | Design output |
| Output | Factor of safety against bearing failure | Design output |

### Slope stability assessment

| Category | Parameter | Notes |
| --- | --- | --- |
| Input | Slope geometry (height, angle, benches) | From survey |
| Input | Geological unit boundaries | From ground investigation |
| Input | Shear strength parameters per unit (c', phi', Su) | From testing or correlation |
| Input | Piezometric conditions | From monitoring or assumption |
| Input | Surcharge loading | From project brief |
| Input | Seismic acceleration coefficient | From NZS 1170.5 |
| Input | Rainfall/infiltration assumptions | From hydrology or assumption |
| Output | Factor of safety (static) | Design output |
| Output | Factor of safety (seismic) | Design output |
| Output | Critical failure surface location | Design output |
| Output | Remedial measures (if FoS inadequate) | Design output |
| Output | Monitoring requirements | Design output |

## The Report Body vs Calculation File Distinction

Not all parameters appear in the report body. Corporate guidance in many firms
encourages engineers to keep reports concise by leaving detailed parameter derivations
in internal calculation files. The typical split is:

- **Report body**: key input assumptions, final output values, design recommendations
- **Calculation file (internal)**: intermediate calculations, sensitivity analyses,
  parameter derivation details, software input/output listings

A completeness check must be aware of this distinction. Checking the report body alone
may flag "missing" parameters that legitimately reside in the calculation file.
Checking the calculation file alone may miss parameters that should be visible to
downstream readers in the report.

## Open Questions

1. For each design type, which output parameters are mandatory in the report body
   versus acceptable in the calculation file only?
2. Should the completeness check flag parameters that are present in calculations
   but absent from the report, or only parameters absent from both?
3. How do different firms draw the line between report body content and calculation
   file content for the same design type?
