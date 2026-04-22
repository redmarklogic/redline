# Initiative: Maker-Checker UX Concept (Phase 2)

**Status**: Draft v1. **Owner**: Mark. **Date**: 2026-04-20.
**Strategic bet**: [Bet 2 — Pre-Review Is the Paid Product Day-1](../strategy/strategic-bets.md)
**Sequence**: Design thinking starts now. Build starts after skeleton ships (Sprint 2+).
**Architecture reference**: [ai-maker-checker-pattern.md](../../architecture/ai-maker-checker-pattern.md)

## What This Document Is

A lightweight UX concept for how the Maker-Checker pattern surfaces in the user's
workflow. This is not a full PRD — it is design thinking captured early so the skeleton
and audit trail are built with this future workflow in mind. The full PRD will be drafted
when Pre-Review enters Sprint 2-3 scope.

## The Analogy

GitHub Copilot writes code. A second AI (Copilot code review) reviews the code and
leaves comments. The human developer has final authority — they accept, reject, or modify
each suggestion. Neither AI has the authority to merge. The human is the decision-maker
at every step.

Redline's Maker-Checker works the same way for geotechnical reports. The AI that
generates content is not the same agent that reviews it. The reviewer AI's job is to
direct human attention, not to rubber-stamp the generator's output.

This is not a conflict of interest — it is an attention-directing mechanism. The Checker
does not approve or reject on behalf of the engineer. It enumerates what it checked and
flags where the engineer should look harder.

## The Flow

```
1. Skeleton + client materials
        |
        v
2. AI Draft Generation (Maker)
   - Fills skeleton sections with draft content
   - Draws on Standards Knowledge Store + client scope documents
   - Higher temperature (creative, task-oriented)
        |
        v
3. AI Review (Checker)
   - Evaluates draft against standards rubric, completeness checklist,
     and firm-specific House Rules (when available)
   - Lower temperature (deterministic, critical)
   - Produces enumerated Word comments anchored to specific sections
        |
        v
4. Human Reviewer
   - Receives .docx with visible Word comments from the Checker
   - Each comment says what was checked: "I checked clause X against
     NZS 3910 s4.2 — this section does not address [specific gap]"
   - Engineer focuses attention on flagged items
   - Engineer accepts, rejects, or modifies each comment
   - Every resolution is logged in the audit trail
```

## How Word Comments Surface AI Review

The Checker produces its output as standard Word revision comments (not tracked changes).
Each comment is:

- **Anchored** to a specific paragraph or sentence in the draft.
- **Enumerated** with a sequential reference number for traceability.
- **Attributed** to "Redline Pre-Review" (not a human name — maintains
  Switzerland-neutral positioning).
- **Specific** about what was checked: "Checked against NZGS Module 2, Clause 3.4.
  This section omits the recommended baseline statement for groundwater regime."
- **Actionable**: tells the engineer what to do, not just what is wrong.

The engineer's workflow is familiar — they already review Word documents with tracked
changes and comments from senior reviewers. The difference is that the first pass of
comments comes from the AI Checker, compressing the time the senior reviewer spends on
structural and standards-compliance issues.

## Trust Mechanism

The Checker does not say "this section is fine." It says "I checked clauses X, Y, Z
against standards A, B, C. Here is what I found." The enumeration is the trust signal.

When the Checker finds nothing wrong in a section, it still reports what it checked:
"Reviewed against NZS 3910 s4.2, s5.1, and NZGS Module 2 Clause 3.4. No issues
identified." This gives the engineer confidence that the section was examined, not
skipped.

The senior reviewer's role shifts from first-pass structural markup to second-pass
engineering judgment on the items the AI flagged plus their own domain expertise.
The senior is not replaced — their time is redirected to higher-value review.

## What This Means for Sprint 1

The skeleton and audit trail must be architected with this downstream flow in mind:

- The .docx output format must support Word comments (not just content).
- The audit trail must support review-comment events (even if those events are not
  logged until Sprint 2-3).
- The Standards Knowledge Store must be queryable by the Checker agent, not just the
  Maker (both agents need access to the same clause references).

## Open Questions

1. Should the Checker operate on the full document or section-by-section? Full-document
   review is more coherent but slower and more expensive (token cost).
2. How many review iterations before the Checker stops? Per the
   [Maker-Checker architecture doc](../../architecture/ai-maker-checker-pattern.md),
   a circuit breaker (MAX_RETRIES = 3) is required.
3. Does the engineer see the Maker's raw draft before the Checker's comments, or only
   the commented version? Showing both might reduce trust ("why show me something the
   AI itself thinks is wrong?"). Showing only the commented version is cleaner.
4. How does the Checker handle firm-specific House Rules that are not yet configured?
   Graceful degradation: Checker runs standards-only review when no House Rules exist.

## Risks

| Risk | Mitigation |
|---|---|
| Engineers perceive AI-reviewing-AI as circular or untrustworthy | Enumeration of what was checked makes the review transparent. Copilot analogy normalises the pattern. |
| Comment volume overwhelms the engineer | Severity ranking on comments (critical / advisory / informational). Engineer can filter. |
| Token cost doubles or triples per document | Use cheaper model for Maker, more capable model for Checker. Accept cost as a pricing input for Pre-Review tier. |
| Senior reviewers feel displaced | Positioning: "compresses your first pass, does not replace your judgment." |

## Next Step

Full PRD for Pre-Review (Feature D) is drafted when the D decomposition session (P-030)
completes, per [roadmap.md](../strategy/roadmap.md). This concept informs that PRD.
