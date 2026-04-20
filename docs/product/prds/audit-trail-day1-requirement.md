# PRD: Audit Trail as Day-1 Product Requirement

**Status**: Draft v1. **Owner**: Mark. **Date**: 2026-04-20.
**Target reader**: Engineering.
**Strategic bet**: [Bet 1](../strategy/strategic-bets.md) (ships with skeleton),
[Bet 4](../strategy/strategic-bets.md) (Switzerland-neutral trust posture).
**Problem statement**: [skeleton-wedge-problem.md](../problems/skeleton-wedge-problem.md)

## Why Day-1, Not Phase-2

Feature L (Audit Log + Reviewer Sign-off) in
[feature-backlog.md](../strategy/feature-backlog.md) is currently scored for Sprint 5+.
This PRD elevates the core audit trail to Sprint 1 based on the insurance bifurcation
finding from the Archie competitive intelligence session (2026-04-20).

The finding: NZ insurers are diverging. Some are offering affirmative AI policies that
cover AI-assisted professional work. Others are inserting absolute exclusion clauses that
void coverage entirely when AI is used in the delivery of professional services. A firm
using AI to draft geotechnical reports without a demonstrable audit trail of human
oversight is potentially uninsurable under the exclusion-clause regime.

This makes the audit trail a market-access requirement, not a nice-to-have. Firms cannot
adopt Redline if doing so jeopardises their professional indemnity insurance. The audit
trail is the mechanism that proves human oversight occurred.

Engineering NZ guidance is clear: a Chartered Professional Engineer (CPEng) retains full
personal liability for any work product, regardless of the tools used to produce it. AI
cannot sign off work. The audit trail must demonstrate that a human engineer reviewed,
accepted, modified, or rejected every AI-generated element.

GTM framing: "Your AI wrote it. Who checked it? Redline gives you the audit trail your
insurer will ask for."

## What Is Logged

Every interaction between the AI system and the user's document is recorded:

| Event type | What is captured |
|---|---|
| **AI generation** | Timestamp, user ID, model version, input parameters (report type, jurisdiction, project parameters), output document hash, generation duration. | **Sprint 1** |
| **Human edit** | Timestamp, user ID, section modified, nature of change (addition, deletion, modification). Content diffs are stored but not the full document text at each step. | Sprint 5+ |
| **Review comment** | Timestamp, reviewer ID, comment text, target section, comment type (suggestion, flag, question). | Sprint 2–3 (ships with Pre-Review) |
| **Comment resolution** | Timestamp, resolver ID, resolution action (accepted, rejected, modified), modification summary if modified. | Sprint 2–3 (ships with Pre-Review) |

All timestamps are UTC. All user IDs are authenticated via SSO.

## What Is Surfaced to the User

The audit trail is not a hidden log — it is a visible trust mechanism in the output
document.

- **Structured diff trail**: the output .docx includes a metadata section (or appendix)
  listing: which sections were AI-generated, which were human-authored, which were
  AI-generated-then-human-edited, and the timestamp of each transition.
- **Generation provenance badge**: each AI-generated section carries a visible marker
  indicating it was machine-generated and the date/time of generation. This marker
  persists in the document even after human editing — the edit is recorded as a
  separate event on top of the generation event.
- **Review summary**: when the document passes through Pre-Review (Phase 2), the
  audit trail records which comments were raised, how each was resolved, and by whom.

## What an Insurer Needs

An insurer evaluating a claim involving an AI-assisted engineering report needs to
establish that human professional oversight occurred. The audit trail must provide:

1. **Attribution**: who generated each element (AI or human) and who reviewed it.
2. **Timestamp chain**: a chronological record proving that review happened after
   generation, not simultaneously or retroactively.
3. **Decision record**: for each AI-generated element, evidence that a qualified
   engineer accepted, modified, or rejected it — not that it passed through
   unexamined.
4. **Completeness**: no gap in the chain. Every AI-generated section has a
   corresponding human-review event.

This does not require the insurer to access the system directly. The structured metadata
embedded in the output document is the portable evidence artifact.

## Scope for Sprint 1

The full Feature L (Audit Log + Reviewer Sign-off) as described in the backlog includes
reviewer sign-off workflows, firm-level audit dashboards, and exportable compliance
reports. That full scope remains Sprint 5+.

What ships in Sprint 1 with the skeleton:

- Generation event logging (every skeleton generation is recorded).
- Output document metadata section listing AI-generated sections with timestamps.
- Generation provenance markers in the .docx output.
- Immutable log storage (append-only; no retroactive editing of audit records).

What ships later (Sprint 5+ per Feature L):

- Human edit tracking at the section level.
- Review comment and resolution logging (ships with Pre-Review in Sprint 2-3).
- Reviewer sign-off workflow.
- Firm-level audit dashboard.
- Exportable compliance report for insurers.

## Acceptance Criteria (Sprint 1 Subset)

1. Every skeleton generation event is logged with: timestamp (UTC), authenticated user
   ID, report type, jurisdiction, input parameters, output document hash, model version.
2. The output .docx includes a metadata section identifying all AI-generated content
   with generation timestamps.
3. Audit log is append-only — no mechanism exists to delete or modify historical
   entries.
4. Audit log is queryable by user ID and date range (internal use; no user-facing
   dashboard in Sprint 1).
5. The audit trail infrastructure supports extension to edit-tracking and review-comment
   logging without architectural rework.

## Open Questions

1. Where does the audit log live? Options: application database, dedicated append-only
   store, or blockchain-adjacent immutable log. Recommend application database with
   append-only constraints for Sprint 1; evaluate dedicated store for Sprint 5+.
2. What is the retention period? Insurers may need records for the statute of
   limitations on professional negligence claims (6-15 years depending on
   jurisdiction). Storage cost implications need scoping.
3. Should the .docx metadata section be a visible appendix or hidden document
   properties? Visible appendix is more transparent but adds pages. Recommend visible
   appendix for trust signalling.

## Risks

| Risk | Mitigation |
|---|---|
| Audit trail adds Sprint 1 scope and delays skeleton ship date | Sprint 1 subset is deliberately minimal: generation logging + output metadata. No edit-tracking or review workflows. |
| Retention period creates storage cost at scale | Defer retention policy decision to Sprint 5. Sprint 1 stores indefinitely; revisit when user count is meaningful. |
| Insurer requirements vary by jurisdiction | Start with NZ (Engineering NZ guidance is well-documented). AU requirements are similar but not identical — validate during beachhead. |

## References

- [feature-backlog.md](../strategy/feature-backlog.md) — Feature L (Audit Log + Reviewer Sign-off), Sprint 5+
- [strategic-bets.md](../strategy/strategic-bets.md) — Bet 1 (skeleton wedge), Bet 4 (Switzerland-neutral)
- [non-goals.md](../strategy/non-goals.md) — Redline does not attest to compliance
- [positioning.md](../strategy/positioning.md) — Switzerland-neutral quality layer
- Archie competitive intelligence session (2026-04-20) — insurance bifurcation finding
