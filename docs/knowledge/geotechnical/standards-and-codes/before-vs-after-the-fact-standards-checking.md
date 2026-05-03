# Before-the-Fact vs After-the-Fact Standards Checking

**Sub-domain**: standards-and-codes
**Last verified**: 2026-05-03
**Confidence**: cross-referenced
**Sources**: Geotechnical Report Workflows, Ground Engineering Magazine, Founder Memos

## Summary

Geotechnical engineers use standards in fundamentally different ways depending on whether
they are designing new infrastructure ("before the fact") or assessing/verifying existing
infrastructure ("after the fact"). The workflows, deliverables, applicable standards, and
risk profiles diverge significantly — but they share a common underlying need: identifying
which standards are relevant to a given project and checking compliance against them.

## Key Facts

### Design Phase — "Before the Fact"

1. The workflow is **forward-looking and strictly prescriptive**. Engineers select current,
   active codes (e.g. AS/NZS 1170.0, NZS 1170.5, NZS 3101) and mathematically test the
   proposed design against mandated load combinations (ULS and SLS) [GRW-6, GRW-13–17].

2. Deliverables include GFRs (Geotechnical Factual Reports), GIRs (Geotechnical Interpretive
   Reports), Detailed Design Reports, technical specifications, IFC drawings, and **Producer
   Statements (PS1 and PS2)** certifying compliance with the Building Code [GRW-2,3,5,7,9,18–21].

3. The design is subjected to formal **Design Peer Review** or **Regulatory Peer Review** —
   an independent engineer checks engineering rigour against selected regulations and codes
   [GRW-7,18].

4. Standards-checking for new designs requires checking current code clauses, current Factors
   of Safety, current seismic acceleration parameters, and active material standards
   [GRW-22–24].

5. New designs often result in "over-designing" to satisfy ULS requirements — structures are
   built significantly stronger than theoretically necessary [GE-3,4].

6. BIM and 3D ground modelling integration is a strong digitisation trend for new design
   workflows [GE-11–13].

7. AI parametric design tools (e.g. Artificial Neural Networks) are emerging to speed up
   preliminary design — predicting settlements and deflections in minutes [GE-14–16].

### Assessment Phase — "After the Fact"

8. The workflow is **backward-looking and diagnostic**. Engineers evaluate an asset's current
   condition, assess damage after events, or conduct forensic investigations [GRW].

9. Engineers often evaluate against the **standards that existed when the structure was built**,
   not current codes. Under the NHI Act, assessors must consider whether assets were
   "constructed to the standard considered appropriate at the time" [GRW-12].

10. Strictly following new-build codes for existing structures is often impractical,
    uneconomical, or impossible. Engineers rely on bespoke testing, monitoring, and advanced
    analysis [GE-7].

11. Deliverables include condition assessment reports, structural integrity reports, and
    **conceptual remediation strategies** (explicitly marked "conceptual only, not for
    construction") [GRW-26,27,30].

12. If failure has occurred, a **Forensic Review** determines liability and failure mechanisms —
    this may lead to expert witness roles in legal disputes [GRW-25].

13. For existing asset assessment, Network Rail uses a multi-level assessment framework
    (Level 0–3) ranging from rapid automated assessments to advanced numerical modelling,
    rather than standard new-build codes [GE-9,10].

14. The Shell Centre (Southbank Place) used ISO 2859 (a statistical sampling standard) to
    determine how many existing piles to investigate for reuse — a novel departure from
    standard geotechnical codes [GE-8].

15. Remote sensing (UAVs, LiDAR, InSAR) and Digital Twins are major digitisation trends
    for existing asset assessment [GE-18–27].

### Shared Engine — Founder's View

16. The founder believes both use cases can be powered by the same backend "standards engine"
    [FM-1,2].

17. The founder leans toward tackling "before the fact" first — this aligns with the skeleton
    document generation use case already in development [FM-2].

18. The founder wants a project-type taxonomy distinguishing new infrastructure, existing
    infrastructure, erection, demolition, and maintenance [FM-2].

## Standards Referenced

- AS/NZS 1170.0 — Structural design actions, general principles
- NZS 1170.5 — Earthquake actions
- NZS 3101 — Concrete structures
- Eurocode 7 (EC7) — Geotechnical design (European)
- ISO 2859 — Sampling procedures for inspection by attributes (used for foundation reuse)
- NHI Act — Natural Hazards Insurance Act (NZ)
- SNZ HB 8630 — Earthquake combination factors

## Open Questions

1. **Risk and liability**: The Risk Assessment in Engineering notebook returned "Not covered
   in sources" for the question of how professional liability differs between the two modes.
   This is a significant gap — the liability profile is arguably the biggest differentiator
   between the two workflows.

2. **Standards differentiation**: The Engineering Standards notebook returned "Not covered
   in sources" for the question of how NZ standards distinguish between new design vs
   assessment. This gap should be filled by reviewing NZS 3604, AS/NZS 2159, NZGS guidelines,
   and MBIE guidance on existing buildings (particularly earthquake-prone building legislation).

3. **Assessment-specific standards**: NZ has specific frameworks for assessing existing
   buildings (e.g. NZSEE assessment guidelines for earthquake-prone buildings, MBIE EPB
   methodology). These are not currently in the notebook corpus.

4. **Insurance and PI implications**: How do professional indemnity insurers view the
   liability difference between design sign-off (PS1/PS2) and condition assessment?

## Further Reading

> I have not verified these sources, but they may contain answers to the open questions:

- **NZSEE/MBIE "The Seismic Assessment of Existing Buildings"** (the "Red Book") — NZ's
  primary guidance for assessing existing buildings against seismic standards. Likely
  contains the clearest statement of how assessment standards differ from design standards.
- **MBIE Earthquake-Prone Buildings Methodology** — Defines percentage of New Building
  Standard (%NBS) for existing buildings, explicitly creating a different compliance
  threshold than new design.
- **NZGS "Geotechnical Earthquake Engineering Practice" Module Series** — May contain
  guidance on assessing existing geotechnical assets.
- **Engineering NZ Practice Note 19: Producer Statements** — Defines PS1/PS2/PS3/PS4
  and their legal standing, relevant to liability differentiation.
- **IPENZ/Engineering NZ guidance on Forensic Engineering** — Professional obligations
  when assessing failed or damaged infrastructure.

## Citation Key

- GRW = Geotechnical Report Workflows notebook
- GE = Ground Engineering Magazine notebook
- FM = Founder Memos notebook
- Numbers after the prefix correspond to the citation numbers returned by NotebookLM
