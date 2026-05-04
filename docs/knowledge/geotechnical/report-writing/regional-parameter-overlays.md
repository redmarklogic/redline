# Regional Parameter Overlays

**Status**: draft
**Owner**: Graeme (Principal Geotechnical Engineer)
**Last updated**: 2026-05-04
**Provenance**: Parameter completeness advisory session, 2026-05-04

**Sub-domain**: report-writing
**Confidence**: practitioner-grounded

## Summary

Regional variation in geotechnical parameter requirements is an overlay on the
design-type taxonomy, not the primary axis. The correct sequencing is: identify the
design type first, assemble the base parameter set, then apply regional modifiers
required by local regulatory frameworks, council standards, and geological conditions.
This document captures the known regional overlays for New Zealand, starting with
Canterbury (the best-documented region) and identifying gaps for Auckland and Wellington.

## Principle: Overlay, Not Primary Axis

Regional variation modifies parameter requirements but does not define them. A timber
pole retaining wall in Canterbury requires the same core structural and geotechnical
parameters as one in Auckland. Canterbury adds liquefaction zoning and specific Producer
Statement requirements. Auckland may add volcanic terrain considerations. But the
starting point is always the design type, not the region.

This means the data model should be: `base_parameters(design_type) + overlay(region)`,
not `parameters(region, design_type)`.

## Canterbury / Christchurch

Canterbury is the most heavily regulated region for geotechnical practice in New Zealand,
driven by the 2010-2011 Canterbury Earthquake Sequence and the subsequent rebuild
programme. The following regional requirements are confirmed in the Engineering Standards
and Geotechnical Report Workflows notebooks.

### Liquefaction zoning

Canterbury uses a Liquefaction Resistance (LR) Index zoning system with values 0 through 4:

- **LR 0**: No liquefaction vulnerability. Standard design applies.
- **LR 1**: Low liquefaction vulnerability. Polyethylene pipes mandatory for buried
  services (LR 0 and LR 1).
- **LR 2**: Moderate liquefaction vulnerability. Geotextile-wrapped haunching required
  for drainage (LR 0, 1, and 2).
- **LR 3**: High liquefaction vulnerability. Full liquefaction assessment required.
- **LR 4**: Very high liquefaction vulnerability. Detailed ground improvement or
  avoidance strategies required.

The LR Index is derived from the Canterbury liquefaction vulnerability maps and is
mandatory for all geotechnical design in the region.

### MBIE earthquake rebuild guidelines

The Ministry of Business, Innovation and Employment (MBIE) published Canterbury-specific
guidance for repairing and rebuilding houses affected by the earthquakes (Parts A-D).
These guidelines are mandatory for Canterbury but do not apply nationally. They impose
additional documentation requirements for foundation design, ground improvement, and
land damage assessment.

### Port Hills specific requirements

- **Rockfall hazard**: GNS Science rockfall and cliff collapse reports are required for
  sites in the Port Hills. These define run-out distances and boulder kinetic energies
  that feed into rockfall protection design.
- **Producer Statements**: Canterbury uses specific Producer Statement templates:
  - PS1 (Producer Statement -- Design) for rockfall protection design
  - PS2a (Producer Statement -- Design Review)
  - PS4 (Producer Statement -- Construction Review)
- **Loess soils**: The Port Hills contain dispersive volcanic loess soils that require
  lime treatment for stabilisation. A winter earthworks ban applies from 1 May to
  31 August due to moisture sensitivity.

### Christchurch Drainage Datum (CDD)

Christchurch uses a unique local elevation datum (Christchurch Drainage Datum) instead
of the national LINZ datum for stormwater and drainage design levels. Any geotechnical
report addressing groundwater or drainage levels in Christchurch must specify which
datum is used.

### Seismic hazard factor

Canterbury has a higher seismic hazard factor (Z value per NZS 1170.5) than many other
New Zealand regions. This affects all seismic design parameters including liquefaction
triggering analysis, slope stability under seismic loading, and retaining wall design
for earthquake conditions.

## Auckland

**Status: gap -- needs research.**

Auckland has a fundamentally different geological setting from Canterbury:

- **Volcanic terrain**: Auckland sits on the Auckland Volcanic Field with basalt lava
  flows, scoria cones, and tuff deposits. Foundation design in volcanic ground requires
  different investigation and parameter considerations compared to the alluvial and
  marine sediments of Canterbury.
- **Auckland Council engineering standards**: Auckland Council publishes its own
  engineering standards and Code of Practice for Land Development and Subdivision, which
  may impose region-specific geotechnical documentation requirements.
- **Auckland Transport requirements**: Infrastructure projects under Auckland Transport
  jurisdiction may have additional geotechnical reporting requirements.

The notebooks do not currently contain Auckland-specific geotechnical standards.
This is a known gap requiring research.

## Wellington

**Status: gap -- needs research.**

Wellington presents a distinct set of regional considerations:

- **High seismicity**: Wellington has some of the highest seismic hazard factors (Z values)
  in New Zealand.
- **Active faults**: The Wellington Fault and other active faults impose additional
  requirements for fault avoidance, fault rupture assessment, and setback distances.
- **Different geology**: Wellington's greywacke rock, colluvium, and harbour sediments
  differ from both Canterbury and Auckland, affecting parameter selection for foundation
  and slope stability design.

The notebooks do not currently contain Wellington-specific geotechnical standards.
This is a known gap requiring research.

## National

- **NZS 1170.5 seismic hazard factor (Z)**: Varies nationally by location. Every
  seismic design parameter set must include the site-specific Z value. This is a
  national requirement but the value itself is region-dependent.
- **NZ Building Code**: National baseline, but territorial authorities may impose
  additional requirements through district plans and council engineering standards.

## Open Questions

1. What specific Auckland Council engineering standards affect geotechnical parameter
   requirements? Are there volcanic-terrain-specific requirements?
2. What Wellington-specific geotechnical requirements exist beyond the national seismic
   code (e.g., Wellington City Council fault setback rules)?
3. How do Australian state-level variations (e.g., Queensland vs Victoria vs NSW)
   compare to the NZ regional variation pattern?
4. Are there other NZ regions with significant overlays beyond Canterbury, Auckland,
   and Wellington (e.g., Hawke's Bay post-Cyclone Gabrielle)?

## Further Reading

- MBIE, *Repairing and rebuilding houses affected by the Canterbury earthquakes*,
  Parts A-D -- Canterbury-specific geotechnical guidance
- Auckland Council, *Code of Practice for Land Development and Subdivision* -- I have
  not verified whether this contains geotechnical parameter requirements
- Wellington City Council, *District Plan fault hazard provisions* -- I have not
  verified the current content or applicability
- GNS Science, Port Hills rockfall and cliff collapse reports -- Canterbury-specific
  hazard assessment documentation
