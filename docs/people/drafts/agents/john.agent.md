# Draft JD Patch — John (Head of Marketing)

**Status:** DRAFT — self-reported by John, drafted by Harriet; awaiting founder promotion (sync item A-20).
**Target file:** `.claude/agents/john.md`
**Drafted by:** Harriet (facilitating agent), Topology Sync 2026-06-10, from John's live Delta Statement (`docs/people/drafts/reports/delta-statements-2026-06-10/john.md`, §3.1, §3.2, §4.1–§4.2). Both patches are John's own proposals; no facilitator-invented changes.
**Root cause:**

1. The campaign gate cites `docs/product/personas/`, a directory that **does not exist** — verified on disk 2026-06-10. The persona artifact actually lives at `docs/product/strategy/personas.md`. As written, no campaign brief can ever satisfy John's own hard constraint (map-vs-territory defect: the JD encodes a path that was never materialised).
2. The signal-report constraint assumes live product instrumentation. Redline is pre-launch — ADR-022 ships a Bearer-token presence-only placeholder, and SSO/instrumentation work is deferred to issue #73 — so report sections 1–2 (conversion data) have no possible data source. The missed June 2026 report (due 2026-06-01, self-identified by John) was a structural breach, not a behavioural one.

---

## Patch 1 — Persona path correction (Outcome 6 + Session Discipline)

**REPLACE** Outcome 6:

> 6. **Campaigns link to a strategic bet and a validated persona.** No campaign brief is produced without references to both `docs/product/strategy/strategic-bets.md` and `docs/product/personas/`.

**WITH**:

> 6. **Campaigns link to a strategic bet and a validated persona.** No campaign brief is produced without references to both `docs/product/strategy/strategic-bets.md` and the persona artifact (currently `docs/product/strategy/personas.md`; personas are co-owned by Mark and Ron — if the canonical location changes, this gate follows the artifact).

**REPLACE** the Session Discipline bullet:

> - Always check `docs/product/strategy/strategic-bets.md` for bet alignment and `docs/product/personas/` for persona validation before writing a campaign brief.

**WITH**:

> - Always check `docs/product/strategy/strategic-bets.md` for bet alignment and `docs/product/strategy/personas.md` for persona validation before writing a campaign brief.

*Second-order note (not part of this patch):* Mark's JD claims `docs/product/personas/` as **direct write authority** (co-owned with Ron) — the same nonexistent directory. The canonical-location decision (materialise `docs/product/personas/` and move the artifact, or keep personas in Ron's strategy file and patch Mark's JD) is a founder + Ron + Mark decision, consolidated in the sync report §12 (item A-25). This patch points John's gate at the artifact's actual current location either way, so the gate is satisfiable regardless of the outcome.

## Patch 2 — Pre-launch signal-report mode (Hard Constraint + Monthly Ritual)

**REPLACE** the hard constraint:

> - I MUST file the monthly signal report by the first business day of each month.

**WITH**:

> - I MUST file the monthly signal report by the first business day of each month. **Pre-launch mode:** until product instrumentation is live (conversion events flowing — gated on the SSO/instrumentation work deferred to issue #73), sections 1–2 (What converted / What flopped) are not required and are marked "pre-launch — no instrumentation"; sections 3–6 (prospect questions, competitor moves, search trends, recommendations) are always due. Once instrumentation is live, all six sections are mandatory.

**ADD** to the "Monthly Ritual: Signal Report" section, after the numbered section list:

> **Pre-launch mode.** Until product instrumentation is live, sections 1–2 have no data source. File the report on schedule with sections 3–6 complete and an explicit "pre-launch — no instrumentation" marker on sections 1–2. The filing-date discipline (first business day of each month) applies in both modes — pre-launch status changes the report's scope, never its deadline.

---

## Items deliberately NOT in this patch (route elsewhere)

- **June 2026 remedy:** John retro-files a reduced-scope June report (sections 3–6) this week and files July's on 2026-07-01 under the amended rule — founder approval consolidated as sync item A-12. An action, not JD text.
- **Craig Lewis email publication status:** founder confirmation requested (sync item A-11). If sent without an AI-content-review log entry, that is a gate breach to record; if unsent, the seven artifacts in `docs/product/marketing/content/` are pre-publication drafts and no gate was breached.
- **Skill currency (`marketing-product-led-seo` AI-citation annex; `linkedin-social-selling` saves/dwell metrics):** conditional on primary-source corroboration — Linda to source one primary reference each (sync item A-26 / skill trigger S-9). John flagged his own R3 findings as directional secondary sources; no skill patch until corroborated.
- **"Files I Maintain" forward declarations** (editorial-calendar.md, signal-reports/, campaigns/, etc. not yet on disk): acceptable as forward declarations per John's own assessment; no JD change. The missing editorial calendar is a watch item against Outcome 1, not a patch.
