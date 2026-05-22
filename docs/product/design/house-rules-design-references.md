# House Rules — Design References

**Status**: Forward reference (Phase 2 input). Not active work.
**Created**: 2026-05-22. **Owner**: Mark.
**Source**: Ron's competitor analysis of Microsoft Legal Agent ([competitor profile](../../research/competitors/microsoft-legal-agent.md)).

This note captures design patterns from the Microsoft Legal Agent (Word Frontier programme) that should inform House Rules design when Phase 2 begins. It does not change H2 scope or Pre-Review Sprint 1 commitments.

---

## 1. Playbook-to-Skill Conversion (Interaction Pattern Reference)

The Legal Agent's playbook review workflow is the strongest public reference implementation of what Redline's House Rules engine should look like. The interaction pattern:

1. User uploads a `.docx` playbook (internal standards document).
2. Agent converts the playbook into a "skill" — an AI-readable instruction set broken down by categorised topics with extracted rules and example clauses.
3. User reviews, adjusts, and saves the skill for reuse.
4. User clicks "Start Review" — agent scans the active document against the saved skill.
5. Colour-coded compliance report generated (Green = compliant, Red = requires changes).
6. User resolves issues individually or clicks "Accept All."

The key design insight is the intermediate review step (step 3): the user sees what the AI extracted from their playbook before it is applied. This builds trust and catches extraction errors before they propagate into false flags.

When House Rules design begins, this upload-extract-review-save-apply pattern should be the starting point for UX exploration. Evidence quality: `[Vendor]` per the competitor profile.

## 2. Colour-Coded Compliance Report (UX Reference for Pre-Review Output)

The Legal Agent's compliance report uses a simple Green/Red colour coding with per-topic drill-down. This is scannable, professional-grade output that a senior reviewer can triage in seconds.

Pre-Review output (Bet 2, Sprint 1 onwards) should be at least this clear. The colour-coded report is not a House Rules feature — it is a baseline output quality standard that applies to any review mode. When designing Pre-Review's annotation summary view, use this as the floor, not the ceiling.

## 3. Clickable Source Citations (Non-Negotiable for Pre-Review Sprint 1)

The Legal Agent provides clickable numbered citations linking each flag to the exact source text in the document. Ron's recommendation: this is non-negotiable for Pre-Review Sprint 1.

Every Pre-Review flag must link to the specific standard clause, house rule, or structural expectation that triggered it. "Your report has an issue" is not useful. "Section 4.2 is missing a scope limitation statement — see NZS 4402:2015 clause 3.1.2" is useful. The citation must be clickable and navigate to the source.

This is not a House Rules dependency. It is a Pre-Review quality requirement that happens to be validated by Microsoft's implementation.

## 4. Scope Boundary

This document is a Phase 2 design input. It does not:

- Change H2 scope or strategic bets.
- Constitute a PRD or feature commitment.
- Alter Pre-Review Sprint 1 priorities (except to reinforce that clickable citations are non-negotiable, which was already the intent per Bet 2's rule taxonomy).

When House Rules work begins, this note should be loaded alongside the competitor profile and any updated intelligence on the Legal Agent's general availability rollout.
