# Decision 002 — "Before the Fact" First; "After the Fact" Phase 2

**Status**: Decided. **Date**: 2026-05-03. **Deciders**: Founder, Mark, Graeme.

---

## Context

A civil engineer (BMS specialist) uses Gemini to check designs against standards,
revealing two distinct use cases for the standards engine:

- **Before the fact** — awareness of relevant standards while designing new
  infrastructure (new build, greenfield).
- **After the fact** — verifying or expanding existing infrastructure (e.g. a dam,
  retaining wall) and checking compliance to suggest improvements or write a report.

The question: are these separate products or modes of one engine, and which ships first?

## Decision

1. **Architecture**: One standards engine, two separate product surfaces. The Standards
   Knowledge Store (Bet 3) is designed as a shared capability from Day 1 — no new-design
   assumptions hard-coded into the standards layer. Product surfaces (skeleton templates,
   rule sets, review workflows, deliverable types) are mode-specific.

2. **Sequencing**: "Before the fact" (new design) ships in H2 2026. "After the fact"
   (existing infrastructure assessment) is deferred to Phase 2.

3. **Taxonomy**: One project type exposed in H2: `New Build`. Stored as a metadata field
   for future routing. No project-type selector shown in the UI until a second real
   option exists behind it.

## Options Considered

| Option | Description | Verdict |
|---|---|---|
| A. Ship both modes in H2 | Build both product surfaces simultaneously | Rejected — violates focus, doubles scope, no validated demand for assessment mode |
| B. "Before the fact" first | Ship new-design mode in H2; defer assessment to Phase 2 | **Adopted** |
| C. "After the fact" first | Ship assessment mode first | Rejected — less structured, less frequent, requires historical standards lookup, episodic demand, misaligned with every active bet |
| D. Separate products | Treat as two independent products with no shared engine | Rejected — underlying standards capability is clearly shared; duplicating it wastes engineering effort |

## Rationale

### Domain evidence (Graeme)

- New design follows a prescriptive, linear workflow: Desktop Study, GFR, GIR,
  Preliminary Design, Detailed Design, IFC. More structured and codifiable.
  [Geotech Workflows GRW-6, GRW-7, GRW-18]
- New design always uses the current standard version — no ambiguity about which
  version applies. Assessment requires historical standards lookup and judgment calls
  about "the standard considered appropriate at the time." [GRW-12]
- Assessment deliverables require mandatory disclaimers ("conceptual only, not for
  construction") and different peer review types (forensic review, possible litigation).
  [GRW-25, GRW-26, GRW-27]
- "Modification of Existing" (expansion/alteration) is the hardest category — genuinely
  hybrid. Should be attempted last.

### Product evidence (Mark)

- Current product trajectory (Bet 1 Skeleton, Bet 2 Pre-Review) is entirely "before the
  fact." Switching orphans two active bets.
- New design reports are the core billable output for Small firms (5-50 staff). Reducing
  review rounds directly impacts utilisation, write-offs, and capacity.
- CEO Priority #1 for Small firms is Financial Performance — served by new-design
  efficiency, not episodic assessment work.
- "After the fact" requires encoding legislative definitions, historical compliance
  standards, and causation logic — a different knowledge domain from design-code
  compliance. [Geotech Workflows, NHI Act claims workflow]
- Product literature (Cagan, Spolsky) explicitly warns against serving two personas in
  one release. [Writing Specs d0fe6f0f, 81093ccc]
- Dependency chain: validate the engine on the simpler workflow before extending.
  [Product Roadmapping 13b0c35b]

### Strategic alignment

All six strategic bets reinforce "before the fact first":
- Bet 1 (Skeleton Wedge): generates new-design GBR/GIR
- Bet 2 (Pre-Review): checks new-design documents
- Bet 3 (Standards Store): corpus scoped for NZ GBR/GIR design standards
- Bet 4 (Switzerland-neutral): both modes preserve neutrality
- Bet 5 (NZ + AU beachhead): NHI Act claims are NZ-specific; new-design serves both
- Bet 6 (Nonconsumption): senior-review bottleneck is most acute on recurring new-design

## Consequences

- The Standards Knowledge Store data model must not embed new-design-only assumptions.
  Review the data model to confirm mode-neutrality.
- Project type is stored as a metadata field from Sprint 1, even though only one value
  exists in H2. This enables future routing without refactoring.
- Three knowledge gaps must be resolved before Phase 2 begins:
  1. Liability differentiation between design sign-off and condition assessment
  2. NZ-specific assessment standards (NZSEE "Red Book", EPB methodology) ingested into
     the Standards Knowledge Store
  3. PI insurance implications for each mode

## Phase 2 Trigger

Add "after the fact" when BOTH conditions are met:
1. Small-segment adoption validates the engine on new design
2. KR2 discovery conversations reveal demand for assessment-mode checking among
   beachhead customers

## Full Taxonomy (for future reference)

| Project Type | Standards Mode | Phase |
|---|---|---|
| New Build (greenfield) | Before the fact | H2 2026 |
| Assessment / Verification | After the fact | Phase 2 |
| Remediation / Repair | After the fact then Before the fact | Phase 2+ |
| Expansion / Alteration (brownfield) | Hybrid | Phase 2+ (last) |
| Demolition | After the fact (limited, H&S only) | Phase 2+ |
| Maintenance | After the fact (ongoing) | Phase 2+ |

## References

- `docs/product/strategy/strategic-bets.md` — Bets 1-6
- `docs/product/strategy/positioning.md` — CEO Priority Hierarchy
- `docs/research/20260503-firm-size-segmentation.md` — Firm size tiers
- `docs/adr/adr-006-standards-knowledge-store-citation-only-internal-architecture.md`
