# FHWA Reviewer Checklist -- Rule Vocabulary for Pre-Review Engine

**Sub-domain**: report-writing
**Last verified**: 2026-05-13
**Confidence**: cross-referenced
**Sources**: FHWA Checklist and Guidelines for Review of Geotechnical Reports (1988),
via Geotechnical Engineering Checklists notebook (58764ffc)

---

## Summary

The FHWA 1988 reviewer checklists contain approximately 120 discrete yes/no items across 10
topic sections. These are written from the reviewer's perspective (not the author's), making
them the single best external source for Redline's Pre-Review rule vocabulary. The checklist
is divided into Geotechnical Report (GTR) review items and Plans, Specifications & Estimate
(PS&E) review items. For Redline Phase 1, only GTR review items are relevant.

The 1988 taxonomy structure remains durable -- the same sections appear in 2025 TDOT checklists.
Specific threshold values (factors of safety, test methods) require updating to current
standards, but the checklist vocabulary is still valid.

---

## Candidate Seed Set for Pre-Review Rule Library

The following FHWA items are assessable against a report's text using Layers 1-3 analysis
(structural presence, content completeness, and linguistic checks) without requiring Layer 4
engineering judgment. These form the candidate seed set for the Pre-Review 20-30 rule library.

### Tier 1 -- High Confidence (presence checks, binary)

These items can be checked with high reliability and minimal false-positive risk.

| # | FHWA Item | Taxonomy Node | Check Type |
|---|---|---|---|
| 1 | Is the general location described / vicinity map included? | 1. Site Context | Presence |
| 2 | Is the scope and purpose summarised? | 1. Site Context | Presence |
| 3 | Is a concise description of geologic setting and topography given? | 3. Geology | Presence |
| 4 | Are field explorations and lab tests listed? | 4. Field Investigation | Presence |
| 5 | Is a general description of subsurface conditions given? | 5. Subsurface Conditions | Presence |
| 6 | Are test hole logs included? | 10. Deliverables | Presence |
| 7 | Is a plan and subsurface profile provided? | 10. Deliverables | Presence |
| 8 | Are field explorations located on the plan view? | 10. Deliverables | Cross-reference |
| 9 | Are groundwater levels and date measured shown? | 5. Subsurface Conditions | Presence |
| 10 | Are sample types and depths recorded? | 4. Field Investigation | Presence |
| 11 | Are SPT blow count, core recovery, and RQD values shown? | 4. Field Investigation | Presence |
| 12 | Are laboratory test results included or summarised? | 6. Laboratory Testing | Presence |
| 13 | Is recommended cut slope design provided? | 7. Engineering Analysis | Presence |
| 14 | Is recommended fill slope design provided? | 7. Engineering Analysis | Presence |
| 15 | Are estimated shrink-swell factors provided? | 8. Earthworks | Presence |
| 16 | Is estimated settlement and time given? | 7. Engineering Analysis | Presence |
| 17 | Is recommended allowable bearing pressure given? | 7. Engineering Analysis | Presence |
| 18 | Are soil strength parameters provided for retaining wall design? | 7. Engineering Analysis | Presence |
| 19 | Are wall drainage details provided? | 9. Drainage/Environment | Presence |
| 20 | Are excavation requirements covered? | 8. Earthworks | Presence |

### Tier 2 -- Medium Confidence (content completeness, requires section parsing)

These items require examining section content, not just presence. Suitable for LLM-assisted
checks with human-review framing.

| # | FHWA Item | Taxonomy Node | Check Type |
|---|---|---|---|
| 21 | Has the use of "subjective" subsurface terminology been avoided? | 5. Subsurface Conditions | Language quality |
| 22 | Are station-to-station descriptions included for drainage, wet areas, slides? | 7. Engineering Analysis | Content completeness |
| 23 | Has the use of "template" designs been avoided (designing based on actual conditions)? | 7. Engineering Analysis | Content quality |
| 24 | Have effects of blast-induced vibrations on adjacent structures been evaluated? | 7. Engineering Analysis | Content completeness |
| 25 | Are cost comparisons of treatment alternates given? | 7. Engineering Analysis | Content completeness |
| 26 | Is a specific correction alternative recommended? | 7. Engineering Analysis | Content completeness |
| 27 | Has seasonal fluctuation of groundwater table been considered? | 5. Subsurface Conditions | Content completeness |
| 28 | Has pile group settlement been estimated? | 7. Engineering Analysis | Content completeness |
| 29 | Has abutment downdrag load been estimated? | 7. Engineering Analysis | Content completeness |
| 30 | For major structure in high seismic risk area, has liquefaction potential been assessed? | 7. Engineering Analysis | Content completeness |

### Tier 3 -- Low Confidence (requires engineering judgment, not for Phase 1)

These items require Layer 4 domain judgment and are not suitable for automated checking.

| # | FHWA Item | Reason for exclusion |
|---|---|---|
| 31 | Are clay cut slopes designed for minimum F.S. = 1.50? | Requires reading and evaluating FoS values |
| 32 | Will fill slope design provide minimum F.S. = 1.25? | Requires reading and evaluating FoS values |
| 33 | Do you consider the recommended pile type to be the most suitable and economical? | Professional judgment |
| 34 | Do you consider the recommended design loads to be reasonable? | Professional judgment |
| 35 | Does the conducted site investigation meet minimum criteria? | Requires comparison against Table 2 |
| 36 | Has field investigation confirmed toe of slide does not extend beyond counterberm? | Site-specific technical judgment |

---

## FHWA Critical Items (Starred)

The FHWA checklist marks certain items with an asterisk (*), indicating that a response other
than "Yes" or "N/A" is cause to contact the appropriate geotechnical engineer for clarification.
These starred items represent the highest-priority checks. In the candidate seed set above,
items 6-11 (site investigation information) and items 13-14 (slope design) are starred in the
original FHWA document.

---

## Architecture Notes

1. **GTR vs PS&E split**: The FHWA checklist has parallel GTR and PS&E sections. Only GTR items
   are relevant for Pre-Review Phase 1. PS&E items (verifying report recommendations are
   incorporated into construction documents) are a future "Pre-Construction" workflow moment.

2. **Reviewer voice**: Every FHWA item is phrased as a question from the reviewer's perspective
   ("Is X provided?", "Has Y been evaluated?"). This is the correct voice for Pre-Review flags.
   Redline's Pre-Review output should adopt the same questioning voice, not the author's
   declarative voice.

3. **The "common pitfalls" sub-checklist**: Section A PS&E item 5 lists explicit common pitfalls
   including "Has the use of subjective subsurface terminology been avoided?" This is directly
   analogous to the taboo word detection rule family already in the Pre-Review rule set. The FHWA
   document calls out "relatively soft rock" and "gravel with occasional boulders" as examples of
   subjective terminology. These should be added to the taboo/vague word detection list.

---

## Provenance

All items sourced from FHWA-TS-88-003 "Checklist and Guidelines for Review of Geotechnical
Reports and Preliminary Plans and Specifications" (1988). Queried via Geotechnical Engineering
Checklists notebook, source IDs 0ee5ffe3 and 91dd4604.
