# Initiative: Pre-Submission Council Compliance Checker

**Owner**: Mark (PM)
**Status**: Logged option (not yet prioritised)
**Strategic bet**: Extends Bet 2 (Pre-Review) as a freemium entry point
**Date logged**: 2026-05-13

---

## Opportunity

Council lodgement checklists (CERT 10a, Lodgement Checklist Commercial, Mason County) are
public, non-copyrighted documents that define the minimum bar for geotechnical report
submissions. Engineers submit reports that fail these basic checks, causing rejection and
rework delays.

A free/freemium Pre-Submission checker that validates against council-specific checklists would:

1. **Acquire users at zero CAC** -- engineers upload a report, get a pass/fail against their
   council's checklist
2. **Demonstrate product value** -- the free check proves Redline can parse and reason about
   geotechnical reports
3. **Upsell to Pre-Review** -- "Your report passes the council gate, but here are 12 quality
   issues a peer reviewer would find"

---

## Workflow Moment

**Pre-Submission**: The engineer has completed the report and is about to lodge it with the
council. The anxiety is "will it be rejected at the counter?" The audience is the filing
engineer (who may be junior) and the council processing officer.

---

## Scope

### In scope (Phase 2)

- Depth 1 checks only (section presence, deliverable presence)
- Council-specific rule configurations (CERT 10a, Lodgement Checklist, extensible)
- Simple pass/fail output with "missing items" list
- Free tier (limited checks per month) or freemium

### Out of scope

- Depth 2 or 3 checks (those belong to Pre-Review, Bet 2)
- Engineering judgment or technical validation
- Council-specific formatting requirements (page margins, font sizes)
- AGS4 data validation (different engine entirely)

---

## Rule Source

Council checklists are public documents. Copyright risk is minimal because:

1. The checklists are published for public use by local government
2. Redline encodes the *rules* (logical checks), not the document text
3. The rules are factual requirements, not creative expression

---

## Dependencies

- Shared taxonomy (ADR-007) must exist before council-specific overlays can be built
- Report parsing capability (from Bet 2 Pre-Review) is a prerequisite
- At least 3-5 council checklists should be encoded before launch to demonstrate breadth

---

## Architecture Decision

**Pre-Submission is a free mode within the Pre-Review product, not a standalone surface.**
Same web app, same URL, same parsing pipeline — Depth 1 rules only, zero cost until quota
exhaustion. This avoids a second codebase, keeps the upsell path frictionless, and presents
a single product to the market. The distinction is in rule depth and pricing tier, not in
product surface.

## Open Questions

1. How many NZ councils publish explicit geotechnical checklists? (CERT 10a is Western Bay of
   Plenty; how many others exist?)
2. Should the free tier be unlimited checks with limited depth, or limited checks with full
   depth?

---

## Provenance

Initiative derived from advisory board session (2026-05-13) analysing 10 geotechnical checklists.
See [research/20260513-checklist-collection-analysis.md](../../research/20260513-checklist-collection-analysis.md).
