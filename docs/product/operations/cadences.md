# Standard Operating Cadences

**Status**: Active. **Owner**: Founder.

This document is the canonical schedule of all recurring operational rituals for Redline
in H2 2026. Each entry includes the purpose, attendees, timing, duration, inputs, and
outputs — enough to create a calendar event.

> **Calendar tip:** Each recurring event below lists a `Calendar` field specifying the
> recurrence pattern and timing. The founder can schedule these directly; the timings
> are chosen to be compatible with a solo-founder pre-employment-exit preparation
> period (Apr 18 – May 31) and a full-time product period from June 2.

---

## Daily — LinkedIn Channel (Founder Solo)

| Field | Detail |
|---|---|
| **Purpose** | Maintain the 10:1 commenting rule; respond to DMs; advance Dream 100 outreach |
| **Attendees** | Founder only |
| **Calendar** | Daily, Mon–Fri |
| **Duration** | 30–60 min total (15 min morning commenting; 15–30 min afternoon DMs) |
| **Inputs** | LinkedIn feed; Dream 100 target list |
| **Outputs** | 10 substantive comments per 1 original post; DM replies; connection requests |
| **Reference** | `docs/product/strategy/gtm/content-engine.md` → Cadence |

---

## Weekly — Content Batching Session (Founder Solo)

| Field | Detail |
|---|---|
| **Purpose** | Draft, review, and queue 2–3 LinkedIn posts for the coming week; stage Graeme's review queue |
| **Attendees** | Founder (drafts); Graeme (async review of any technical claims) |
| **Calendar** | Weekly, Sunday |
| **Duration** | ~60 min |
| **Inputs** | Editorial calendar (`docs/product/marketing/editorial-calendar.md`); approved post angles from latest editorial session |
| **Outputs** | 2–3 scheduled LinkedIn posts; any technical claims queued for Graeme async review |
| **Reference** | `docs/product/strategy/gtm/content-engine.md` → Cadence |

---

## Monthly — Editorial Session

| Field | Detail |
|---|---|
| **Purpose** | Process the latest Ground Engineering issue; surface post angles and product signals using the archive intelligence layer |
| **Attendees** | Founder (leads queries), Graeme (NZ/AU filter), John (Big 5 mapping and post angles), Mark (product signal extraction); Ron joins only if a strategic bet is touched |
| **Calendar** | Monthly, within 5 business days of each new Ground Engineering issue dropping |
| **Duration** | 60–90 min |
| **Inputs** | New Ground Engineering issue; NotebookLM `ground-engineering-magazine` notebook; Dream 100 target list |
| **Outputs** | 2–3 approved post angles queued in `editorial-calendar.md`; 1-paragraph product signal note filed to Mark |
| **Reference** | `docs/product/marketing/archive-intelligence.md` → Query Track A |

### Agenda template

1. Read the new issue (founder, before the session). Identify 3–5 notable topics.
2. Run resonance query against the archive: "What topics in this issue have appeared
   before? How has the framing changed?"
3. Run novelty query: "What topics have NOT appeared in any previous issue?"
4. Run Dream 100 commenting query for any active targets.
5. Map every surfaced topic to a Big 5 category. Discard anything that does not map.
6. Draft 2–3 post angles. Assign to Graeme for technical review if needed.
7. File 1-paragraph product signal note to Mark (email or async message).

---

## Monthly — Signal Report Filing (John)

| Field | Detail |
|---|---|
| **Purpose** | John files the monthly market-signal report to Ron and Mark |
| **Attendees** | John (authors); Ron and Mark (recipients) |
| **Calendar** | Monthly, first business day of each month |
| **Duration** | John's output; no meeting required |
| **Inputs** | Editorial session outputs; Dream 100 engagement data; any trend shifts flagged |
| **Outputs** | Signal report filed to `docs/product/marketing/signal-reports/YYYY-MM.md` |
| **Reference** | `docs/product/marketing/README.md` Hard Rule 5 |

---

## Quarterly — Product Intelligence Extraction

| Field | Detail |
|---|---|
| **Purpose** | Extract product signals from the Ground Engineering archive; identify recurring quality problems, standards-evolution patterns, and competitive intelligence |
| **Attendees** | Mark (leads queries); Graeme (NZ/AU applicability filter) |
| **Calendar** | Quarterly — September 2026, December 2026 (first extraction) |
| **Duration** | 2–3 hours (async query + sync discussion) |
| **Inputs** | NotebookLM `ground-engineering-magazine` notebook; current Pre-Review rule library; Standards Knowledge Store roadmap |
| **Outputs** | Filtered recurring-problem list → Mark creates product hypotheses; standards-coverage gaps → roadmap input; any bet-level insight → `parked-decisions.md` |
| **Reference** | `docs/product/marketing/archive-intelligence.md` → Query Track B |

### Agenda template

1. Run recurring-problem extraction query.
2. Run standards-evolution mapping query for priority standards (NZS 3910, AS 4000,
   Eurocode 7, BS 5930, NZGS guidance).
3. Run technology adoption history query.
4. Run dispute and failure pattern extraction query.
5. Graeme reviews all outputs for NZ/AU applicability.
6. Mark converts confirmed signals to product hypotheses; files any bet-level insight to
   `parked-decisions.md`.

---

## Quarterly — Strategy Refresh Review

| Field | Detail |
|---|---|
| **Purpose** | Ron-led review of bets, OKRs, and kill criteria; unfreeze any parked decisions whose triggers have fired |
| **Attendees** | Founder + Ron (mandatory); Mark and John join if relevant decisions surface |
| **Calendar** | Quarterly — September 2026, December 2026 |
| **Duration** | 60–90 min |
| **Inputs** | `docs/product/strategy/strategic-bets.md`; `docs/product/strategy/okrs/`; `docs/deferred/_index.md` |
| **Outputs** | Updated bets (revisions, kills, new bets); OKR progress note; unfrozen decisions resolved; next quarter's kill-criterion checkpoints confirmed |
| **Reference** | `docs/product/strategy/strategic-bets.md`; `docs/deferred/_index.md` |

---

## H2 2026 Calendar at a Glance

| Date | Event |
|---|---|
| 2026-06-01 | Founder's first official day. All KR and sprint clocks start. |
| 2026-07-01 | Monthly signal report (July) |
| Monthly (rolling) | Editorial session — within 5 days of each Ground Engineering issue |
| 2026-08-01 | Monthly signal report (August) |
| 2026-09-01 | Bet 1 kill-criterion checkpoint (90 days post-launch) |
| 2026-09-01 | Monthly signal report (September) |
| September 2026 | Quarterly product intelligence extraction |
| September 2026 | Quarterly strategy refresh review |
| 2026-10-01 | Monthly signal report (October) |
| 2026-11-01 | Monthly signal report (November) |
| December 2026 | Quarterly product intelligence extraction |
| December 2026 | Quarterly strategy refresh review / H2 retrospective |

---

## Provenance

Cadences derived from `docs/product/strategy/gtm/content-engine.md` (daily, weekly),
`docs/product/marketing/README.md` Hard Rule 5 (monthly signal report),
`docs/product/marketing/archive-intelligence.md` (editorial session, product intelligence
extraction), and the founder + Ron + John advisory session of 2026-04-19.
