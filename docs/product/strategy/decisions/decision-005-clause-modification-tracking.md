# Decision 005 — Clause Modification Tracking in OOXML Event Ledger

**Status**: Decided (design note). **Date**: 2026-05-10. **Deciders**: Founder, Mark.

---

## Context

The Sprint 1 OOXML Event Ledger (P-037) captures generation provenance: a write-only custom
XML part embedded in every generated DOCX recording the skeleton generation timestamp, template
version, and standards applied. Nothing reads the ledger yet — reading is Phase 2.

The full ledger schema design — covering extensibility model, all event types, and versioning
rules — is a Sprint 2 engineering design task per P-037.

A gap was identified: the ledger design does not currently account for whether mandatory clauses
have been modified after generation. If an engineer edits or deletes a mandatory limitation
clause (e.g., SCOPE-CLAUSE-01 or SCOPE-CLAUSE-05) before the document goes to a client, that
modification is currently undetectable and unlogged.

This is a design note to be incorporated into the Sprint 2 schema design. It does not add new
Sprint 1 scope.

## Decision

1. **Add `clause_modified` as a defined event type in the Sprint 2 ledger schema.**

   Event fields:
   - `clause_id`: identifier of the clause (e.g., `SCOPE-CLAUSE-01`)
   - `original_hash`: SHA-256 of the clause text at skeleton generation time
   - `current_hash`: SHA-256 of the clause text at the time of the Pre-Review run
   - `detected_at`: ISO 8601 timestamp of detection
   - `actor`: authenticated user ID if known; `null` if not available

2. **Detection mechanism: hash comparison on every Pre-Review run.** When Pre-Review
   runs, it reads the mandatory clause text from the DOCX and computes its SHA-256 hash.
   It compares this against the `original_hash` stored in the custom XML part at generation.
   If the hashes differ, a `clause_modified` event is written to the ledger.

3. **This is a Sprint 2 design task, not Sprint 1 scope.** The Sprint 1 ledger embeds
   the generation provenance event only (per P-037). The `clause_modified` event type
   is designed in Sprint 2 (as part of the full schema design) and implemented in Sprint 2-3
   when the Pre-Review engine is built.

4. **Content control locking is deferred.** The future Business tier state — principal
   engineer locks mandatory clauses as OOXML content controls; unlock events are logged —
   is deferred to Sprint 5+ when the Business tier PRD exists. It is not scoped now.

## Options Considered

| Option | Description | Verdict |
|---|---|---|
| A. No tracking — treat clause modifications as outside scope | Post-generation editing is the engineer's responsibility; Redline does not track it | Rejected — undetected clause modification of a mandatory liability-limitation clause is a material risk event; not tracking it undermines the audit trail value proposition |
| B. Content control locking (Sprint 1) | Lock mandatory clauses as OOXML content controls immediately | Rejected — over-engineering for Sprint 1; locks before a firm configures which clauses they want locked; requires Business tier PRD to define the unlock/override workflow |
| C. Hash-based detection on Pre-Review run (adopted) | Embed hashes at generation; compare on Pre-Review; write event if changed | **Adopted** — lightweight, audit-consistent, deferred to Sprint 2 schema design, compatible with the write-only Sprint 1 ledger |
| D. LLM-based clause comparison | Use the LLM to detect whether clause meaning has changed materially | Rejected — LLM comparison is non-deterministic and not auditable; hash comparison is deterministic and reproducible |

## Rationale

- **The audit trail is a core value proposition.** "Redline gives you the audit trail your
  insurer will ask for" is the GTM anchor (Bet 2). An audit trail that cannot detect
  post-generation clause modification of mandatory limitation clauses is incomplete for the
  insurance and liability use case.
- **Hash comparison is the correct mechanism.** SHA-256 of the clause text at generation
  is deterministic, reproducible, and requires no LLM at detection time. The hash is
  computed once at generation and stored; Pre-Review computes it again on the live text.
  This is low-cost and high-reliability.
- **Sprint 2 is the right timing.** The full ledger schema design is already a Sprint 2
  task (P-037). Adding `clause_modified` to that schema is a line-item addition, not a
  scope escalation. Implementing it alongside the Pre-Review engine (Sprint 2-3) means
  the event is detectable as soon as Pre-Review exists.
- **Content control locking is a Business tier concern.** The unlock mechanism and
  override workflow require firm-level configuration and a Business tier PRD. Designing
  it now, without that context, risks building the wrong locking model.

## Consequences

- The Sprint 2 ledger schema design task (P-037) must include `clause_modified` as a
  defined event type with the fields above.
- The mandatory clauses per Decision 004 are the initial set for which hashes are stored
  at generation time.
- Pre-Review engine implementation (Sprint 2-3) must include hash comparison against the
  stored originals as part of its run protocol.
- The content control locking design is deferred; it is not blocked by this decision.

## References

- `docs/product/strategy/decisions/parked-decisions.md` P-037 (OOXML Event Ledger)
- `docs/product/strategy/decisions/decision-004-mandatory-clause-boilerplate.md`
- `docs/product/prds/audit-trail-design-notes.md`
- `docs/product/prds/audit-trail-day1-requirement.md`
