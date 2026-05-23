# Initiative: Pre-Investigation Scope Check

**Owner**: Mark (PM)
**Status**: Logged option (not yet prioritised)
**Strategic bet**: Potential future Bet (Phase 3)
**Date logged**: 2026-05-13

---

## Opportunity

The Pre-Investigation workflow moment occurs before field work begins. The lead engineer or
project manager defines the investigation scope: which tests to run, how deep to drill, how
many boreholes. Getting this wrong is expensive (wasted mobilisation costs, insufficient data
requiring re-investigation).

Investigation scoping checklists exist (USACE 2001, NZGS 2022 Ground Investigations
Specification) that define minimum investigation requirements by project type and ground
conditions. A scope-checking tool could validate a proposed investigation plan against these
requirements.

---

## Workflow Moment

**Pre-Investigation**: Before the drill rig arrives on site. The anxiety is "have we specified
enough investigation for this project?" The audience is the lead geotechnical engineer and the
project manager.

---

## Scope

### In scope (Phase 3, future)

- Validation of proposed investigation scope against minimum requirements
- Project-type-specific rules (residential, commercial, infrastructure, seismic)
- Jurisdiction-specific rules (NZGS for NZ, FHWA for US)
- Output: "Your proposed investigation may be insufficient because..."

### Out of scope

- Investigation design (choosing borehole locations, test types)
- Cost estimation
- Scheduling or logistics

---

## Why Phase 3

1. **Different buyer anxiety**: Pre-Investigation serves "am I doing enough?" not "is my report
   good enough?" This is a different value proposition than Bet 2.
2. **Different data input**: Input is a scope document or investigation plan, not a completed
   report. Different parsing requirements.
3. **Smaller addressable market**: Only lead engineers scope investigations, whereas all
   engineers write and review reports.
4. **Same buyer**: Despite different anxiety, the buyer is the same engineering consultancy.
   Phase 3 expands the product offering without changing the buyer relationship.

---

## Dependencies

- Shared taxonomy (ADR-007) must exist
- Investigation scoping standards must be encoded (USACE 2001, NZGS 2022)
- Pre-Review engine maturity (Phase 1) proves the NLP pipeline works

---

## Open Questions

1. Is the investigation plan a document (DOCX/PDF) or structured data? If structured, the
   parsing problem is simpler.
2. Does NZGS 2022 provide explicit minimum investigation requirements by project type, or only
   guidance?
3. Would this tool be used by the engineer (self-check) or by the client (verification)?

---

## Provenance

Initiative derived from advisory board session (2026-05-13) analysing 10 geotechnical checklists.
See [research/20260513-checklist-collection-analysis.md](../../research/20260513-checklist-collection-analysis.md).
