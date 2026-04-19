# 3-Month Roadmap — June–August 2026

> **Miro is canonical for this artifact.**
> This file is the synthesis layer only — it captures the decisions visible on the board but
> is not the source of truth for layout, status, or visual relationships.
>
> **Miro board**: [Redline — Product Management](https://miro.com/app/board/uXjVGgXTnIY=/?moveToWidget=3458764668404106570)
> (direct link to the roadmap table)

---

## Context

The founder's first official day is **2026-06-01**. This roadmap covers the first 90 days —
the period in which Bet 1's kill criterion must either pass or trip.

**Kill criterion for Bet 1**: By 2026-09-01, Redline must have ≥ 50 verified-email signups
and ≥ 5% outbound response rate from quota-exhausted users. Missing either number kills
the Free Skeleton Wedge without revival. See [strategic-bets.md](strategic-bets.md).

---

## Roadmap Table

| Milestone / Feature | Bet | Month 1 — June 2026 | Month 2 — July 2026 | Month 3 — Aug 2026 | Kill / Gate |
|---|---|---|---|---|---|
| **[M1] Skeleton Generator live** | [Bet 1](strategic-bets.md) | Ship | — | — | First verified signups (Jun 30) |
| A — GBR Skeleton Generator | [Bet 1](strategic-bets.md) | Ship | — | — | Quota exhaustion → outbound |
| M — Document Parser | [Bet 1](strategic-bets.md) | Ship | — | — | Infra dependency of A |
| N — Standards Knowledge Store (MVP) | [Bet 3](strategic-bets.md) | Ship | — | — | NZ-only subset |
| **[M2] 60-day warning check** | [Bet 1](strategic-bets.md) | — | Ship | — | KR1 ≥ 30 signups by Day 60 (Jul 31) |
| G — Justification Email Generator | [Bet 2](strategic-bets.md) | — | Discovery | Ship | Bottoms-up conversion |
| **[M3] 90-day kill criterion** | [Bet 1](strategic-bets.md) | — | — | Gate | 50 signups + 5% outbound → continue (Sep 1) |
| D — Inline Annotation Engine | [Bet 2](strategic-bets.md) | Parked | Discovery | Discovery | **P-030 decomposition required first** |
| **[M4] Pre-Review sprint kick-off** | [Bet 2](strategic-bets.md) | — | — | Ship | D decomposition session complete |

**Status key**: Ship = committed delivery · Discovery = design/research only · Parked = blocked (see below) · Gate = must-pass milestone · — = out of scope that month

---

## Milestone Definitions

| ID | Date | Meaning |
|---|---|---|
| M1 | 2026-06-30 | Skeleton Generator live, SSO-gated, first verified signups received |
| M2 | 2026-07-31 | 60-day warning-signal checkpoint — KR1 signup count must be ≥ 30 to stay on track |
| M3 | 2026-09-01 | Kill-criterion deadline — 50 signups + 5% outbound response rate required to continue Bet 1 |
| M4 | 2026-08 | Pre-Review sprint kick-off — conditional on P-030 decomposition session being complete |

---

## Parked Items

**D — Inline Annotation Engine (P-030)**

Feature D cannot begin construction until:
1. Feature A (GBR Skeleton Generator) has shipped its first iteration, and
2. A dedicated decomposition session (decision parked as P-030) has been completed.

Month 2 and Month 3 entries for D are Discovery only — no production build is committed.
The P-030 session is a prerequisite gate; until it passes, D has no sprint commitment.

See [parked-decisions.md](decisions/parked-decisions.md) for the full P-030 record.

**Items not on this roadmap**: B, C (rejected/deferred); H, I (Phase 2, not in H2 2026 scope).

---

## Strategic Bet Coverage

| Bet | Coverage in this roadmap |
|---|---|
| Bet 1 — Free Skeleton Wedge | A, M, M1, M2, M3 (primary bet; kill criterion is the 90-day horizon) |
| Bet 2 — Pre-Review is Day-1 paid | G (discovery + ship), D (parked → discovery), M4 (sprint gate) |
| Bet 3 — Standards Knowledge Store is the moat | N (MVP ship in Month 1) |

Bets 4–6 are not surfaced in this horizon — they fall beyond the 90-day kill window.

---

> *Miro is canonical for this artifact. This file is the synthesis.*
> Last updated: 2026-04-19. Owner: Mark.
