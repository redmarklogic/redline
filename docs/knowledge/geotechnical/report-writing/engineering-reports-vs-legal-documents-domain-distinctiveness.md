# Engineering Reports vs Legal Documents — Domain Distinctiveness

**Sub-domain**: report-writing
**Last verified**: 2026-05-04
**Confidence**: cross-referenced
**Sources**: Geotechnical Report Workflows, Risk Assessment in Engineering, Engineering Standards,
Ground Engineering Magazine, parameter-completeness-checking-standard-of-care.md,
design-type-taxonomy-and-parameter-completeness.md, practice-vs-business-of-engineering.md

## Summary

Engineering reports are structurally, technically, and legally distinct from legal
documents. While both carry legal weight, the knowledge required to review an engineering
report for completeness is fundamentally different from legal-document review. A legal
document review checks clauses against codified law and contract terms. An engineering
report review requires the reviewer to evaluate tacit interpretive decisions, run parallel
calculations, verify design-type-specific parameter completeness, and assess whether the
physical model accurately represents site-specific geology and loading conditions. No
generalist AI tool — and no legal-document AI tool — possesses the curated domain knowledge
needed to perform these checks.

## Key Facts

### 1. Engineering reports require mathematical and physical verification

1. Engineering report review requires "parallel simplified calculations" to verify inputs
   and arithmetic — a step that has no analogue in legal document review [GRW: Table 5.1].

2. A technical reviewer must verify that computational models are physically sound: that
   critical slip surfaces do not contact model boundaries, that interslice forces are
   positive, that m-alpha values exceed 0.5, that piezometric conditions are correctly
   applied [GRW: Stability Analysis Review Checklist].

3. A legal contract reviewer checks clauses against codified law. A geotechnical reviewer
   must "evaluate tacit, interpretive engineering decisions — such as whether a low-strength
   shear surface was appropriately modelled, or if soil anisotropy is applicable to the
   specific site — which cannot simply be cross-referenced against a static rulebook"
   [GRW: Source 6].

### 2. Parameter completeness is design-type-specific and non-transferable

4. A timber pole retaining wall requires: length, retained height, pole embedment
   depth/size/centres, lagging size, drainage, anchors, total/damaged face area [GRW].
   A concrete cantilever abutment requires: toe thickness, base width, active and passive
   earth pressures, pressure coefficient at rest, sliding resistance, overturning moment,
   bearing pressures (max, min, average) [GRW]. These parameter sets share almost no
   overlap.

5. Canterbury imposes additional parameters not required elsewhere: MBIE earthquake
   rebuild guidelines, Liquefaction Resistance Index zoning (LR 0-4), Port Hills rockfall
   energy derivations, Christchurch Drainage Datum, and a winter earthworks ban for loess
   soils [Engineering Standards].

6. A generalist AI would not know that "embedment depth" and "pole centres" are required
   parameters for a timber pole retaining wall in Canterbury, because this knowledge
   derives from firm-specific templates, regional council requirements, and NZ-specific
   MBIE guidance — not from public general knowledge.

### 3. Engineering reports are legally binding in ways that require domain expertise

7. Producer Statements (PS1, PS2, PS4) constitute formal certifications that are "relied
   upon both by the municipalities concerned and by the engineer's own clients." Signing
   one without adequate inspection "could be characterized as fraud, or at best,
   professional negligence" [Risk Assessment: Source 6].

8. Courts have held engineers 75% liable for omitting soils reports and groundwater data
   from tender packages (Brown & Huston Ltd v City of York) [Risk Assessment: Source 10-11].

9. An engineer was found negligent for failing to note a missing rebar schedule — "the
   structural-steel components and requirements vital to the integrity of the cement wall
   were missing" — and for calling deficient plans "good plans" [Risk Assessment: Source 12].

10. The legal test is whether the engineer met the "standard of care": the level of skill,
    care, and diligence ordinarily exercised by members of the profession under similar
    conditions. A legal-document AI does not know what this standard requires for a
    specific geotechnical design type.

### 4. Review requires multi-tiered domain-specialist independence

11. Engineering firms mandate structural independence between: the originating engineer,
    the technical reviewer (who must have "equal or above" expertise), the calculations
    checker, the formatting/copy editor, and the project director (who manages commercial
    liability) [GRW: Table 5.1, Six Key Business Rules].

12. The technical reviewer must answer a question no legal-document tool can answer: "has
    the right answer been given to the right question?" based on the specific geotechnical
    context [GRW: Source 5].

### 5. What a generalist AI would and would not catch

13. A generalist AI (ChatGPT, Claude, Copilot) could reasonably catch:
    - Grammar, spelling, and style issues
    - Structural completeness at a high level (e.g., "this report has no conclusions section")
    - Generic professional document checks (e.g., "no limitation of liability clause")
    - Some standards references if explicitly prompted ("does this mention NZS 1170.5?")

14. A generalist AI would NOT catch:
    - Missing design-type-specific parameters (e.g., embedment depth for timber pole walls)
    - Incorrect application of earth pressure coefficients ($k_a$, $k_p$, $k_o$)
    - Piezometric conditions inconsistent with the reported geology
    - Whether the chosen Factor of Safety is appropriate for the specific failure mode
    - Canterbury-specific requirements (MBIE guidelines, LR zoning, CDD datum)
    - Whether the report body and calculation files have the right split of content
    - Whether a Producer Statement's scope matches the actual field services rendered
    - Whether the geological model is consistent with the reported investigation data

## Standards Referenced

- NZS 1170.5 — Structural Design Actions (seismic)
- Eurocode 7 (EC7) — Geotechnical design
- Christchurch IDS — Infrastructure Design Standard
- MBIE Part D — Guidelines for geotechnical investigation (Canterbury)
- Building Act 2004 (NZ) — Producer Statement framework

## Open Questions

1. Has any AI vendor (legal or otherwise) claimed capability for engineering report
   review? If so, what domain-specific knowledge do they claim to encode?

2. How do international engineering jurisdictions (UK ICE, US ASCE, Australian EA)
   compare in terms of the domain-specificity required for report review?

3. Would a two-layer approach (generalist AI for structure/grammar + specialist AI for
   domain parameters) be viable, or does domain context need to permeate the entire review?

## Further Reading

- I have not verified these sources, but they may contain relevant material:
  - ACENZ, *Guide to Engagement of Consulting Engineers* — NZ-specific contractual and
    certification requirements
  - Engineering NZ Practice Note 19 (Engineers and the Law)
  - ICE, *Guidelines for the Preparation of Ground Reports* — UK equivalent of NZ
    geotechnical report standards
