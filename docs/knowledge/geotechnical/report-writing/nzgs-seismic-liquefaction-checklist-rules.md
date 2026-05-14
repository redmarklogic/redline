# NZGS 2016 Module 2 -- Seismic and Liquefaction Checklist Rules

**Sub-domain**: report-writing
**Last verified**: 2026-05-13
**Confidence**: cross-referenced
**Sources**: NZGS 2016 Earthquake Geotechnical Engineering Practice Module 2, via Geotechnical
Engineering Checklists notebook (58764ffc, source 400fdfc4)

---

## Summary

The NZGS 2016 Module 2 is the only external source in the checklist collection that reaches into
Layer 4 (technical method validation). It contains quantitative, method-specific investigation
requirements grounded in real-world failure data from the Canterbury 2010-2011 earthquake
sequence. These rules are mandatory for liquefaction assessment in New Zealand and represent
the highest-stakes domain in NZ geotechnical practice.

This document captures the automatable rules for inclusion in the NZ seismic configuration layer
of the Pre-Review engine.

---

## Quantitative Rules

### Investigation Depth Requirements

| Foundation Type | Minimum Depth for Liquefaction Assessment | Source |
|---|---|---|
| Shallow foundations (lightweight structures) | 10-15 m | NZGS 2016 M2 |
| Heavily loaded or pile foundations | 20 m or more | NZGS 2016 M2 |
| Shallow pad/strip foundations (general) | 2-4x foundation width | NZGS 2016 M2 |
| Pile foundations (general) | 5 pile diameters below tip, minimum 2 m below toe | NZGS 2016 M2 |

**Rule shape**: When report discusses liquefaction assessment, check whether investigation depth
is stated and whether it meets these thresholds. If investigation depth is not stated, flag as
MEDIUM severity: "Investigation depth not stated -- confirm adequacy for liquefaction assessment."

### Testing Method Requirements

| Rule | Requirement | Severity | Source |
|---|---|---|---|
| Primary methods for liquefaction triggering | CPT and SPT are the required primary tools | HIGH | NZGS 2016 M2 |
| Shear wave velocity (Vs) limitation | Vs must NOT be the sole method for liquefaction assessment | HIGH | NZGS 2016 M2 |
| SPT energy calibration | SPT hammer energy must be calibrated to N60 (60% efficiency ratio) | HIGH | NZGS 2016 M2 |
| CPT fines content cross-check | CPT data should be cross-checked with machine-drilled borehole samples for fines content | MEDIUM | NZGS 2016 M2 |
| Rotary wash drilling for loose soils | Rotary wash drilling strongly recommended for SPT in loose materials below groundwater | MEDIUM | NZGS 2016 M2 |
| Becker Penetration Test for gravels | BPT blowcounts should be converted to equivalent SPT N-values for gravel soils | MEDIUM | NZGS 2016 M2 |

**Christchurch evidence for Vs limitation**: A study in Christchurch showed that Vs-based
simplified procedures generally underestimated the triggering of liquefaction relative to CPT-
based procedures (Idriss and Boulanger 2008/2014) and did not fit well with field observations
of liquefaction/land performance during the 4 September 2010 and 22 February 2011 earthquakes.

### Liquefaction Failure Criteria

| Criterion | Definition | Source |
|---|---|---|
| Initial liquefaction | Excess pore pressure equals initial effective confining pressure | Seed and Lee (1966) via NZGS 2016 M2 |
| Strain-based liquefaction | 5% double amplitude axial strain (plus/minus 2.5%) | Ishihara (1993) via NZGS 2016 M2 |

**Caveat**: The 5% double amplitude strain criterion may not be appropriate for soils that
exhibit cyclic mobility rather than flow liquefaction.

### Laboratory Cross-Check Requirements

| Rule | Purpose | Source |
|---|---|---|
| Fines Content (FC) testing | Determine if soil behaves as "sand" or "clay" under seismic loading | NZGS 2016 M2 |
| Plasticity Index (PI) testing | Cross-check CPT data which can under-predict fines content in silty soils | NZGS 2016 M2 |

---

## Slope Stability Safety Factors (Mason County Comparison)

| Condition | Minimum Factor of Safety | Source |
|---|---|---|
| Static slope stability | 1.5 | Mason County / FHWA |
| Seismic slope stability | 1.1 | Mason County / FHWA |
| Quasi-static analysis coefficient | 0.15 | Mason County |
| Seismic bearing capacity (full PGA) | 1.0 | FHWA |
| Seismic bearing capacity (half PGA, strength-sensitive soil) | 1.1-1.15 | FHWA |

---

## Automatable Check Patterns

### Checks suitable for Pre-Review text analysis

1. **Vs-sole-method flag**: If the report states shear wave velocity as the only investigation
   method for liquefaction assessment, flag HIGH: "NZGS 2016 Module 2 does not recommend Vs-based
   simplified procedures as the sole method for liquefaction assessment."

2. **SPT energy calibration mention**: If SPT data is used for liquefaction assessment, check
   whether N60 or energy correction is mentioned. If absent, flag MEDIUM: "SPT hammer energy
   correction to N60 not stated -- required for NZGS 2016 liquefaction triggering procedures."

3. **Investigation depth statement**: If liquefaction assessment is performed, check whether
   investigation depth is stated. If absent, flag MEDIUM.

4. **Cross-check statement**: If CPT is the primary liquefaction investigation method, check
   whether cross-check with borehole sampling is mentioned. If absent, flag LOW.

### Checks NOT suitable for text analysis (Layer 4)

1. Whether the investigation depth is *sufficient* for the actual foundation type (requires
   knowing the foundation type and comparing against thresholds)
2. Whether the CPT data interpretation is technically correct
3. Whether the liquefaction triggering calculation uses an appropriate methodology
4. Whether the ground model is realistic for the Christchurch geologic setting

---

## Provenance

All rules sourced from NZGS 2016 Earthquake Geotechnical Engineering Practice Module 2
(November 2016, Revision 0). Queried via Geotechnical Engineering Checklists notebook,
source ID 400fdfc4.
