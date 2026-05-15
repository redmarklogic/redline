# Initiative Scope: NZ Civil Engineering Firmographic Spreadsheet

**Status**: Scoped. **Owner**: Mark (scope) / Founder (execution). **Date**: 2026-05-14.
**Strategic link**: [Bet 1](../strategy/strategic-bets.md) — Phase 1 LinkedIn outbound motion.
**Downstream consumer**: John — Tier 1 LinkedIn social selling targeting list.
**Source event**: CEAS/Aon "Insurance for Consulting Engineers" webinar, 14 May 2026 (~100 NZ civil engineering firm attendees).

---

## Purpose

Produce a tiered list of NZ civil engineering firms to serve two uses:

1. **Primary (Phase 1 — immediate)**: Unblock John's LinkedIn social selling motion by delivering a Tier 1 list of 10–15 active LinkedIn posters within the CEAS warm window (target: by 21 May 2026).
2. **Secondary (Phase 2+)**: Serve as the NZ market map for firmographic analysis, bowling-pin expansion planning, and ICP (Ideal Customer Profile) validation.

Ron has re-classified this as Phase 1 activity (not Phase 2+) because it directly feeds the immediate LinkedIn motion.

---

## MVP Definition — Tier 1 List (Phase 1, unblocks John)

The minimum viable output is not the full spreadsheet. It is:

> 10–15 named NZ civil engineering firm principals with confirmed active LinkedIn presence, sourced from the CEAS/Aon webinar participant list.

**MVP columns:**

| Column | Description | Source |
|---|---|---|
| Company name | Firm name as registered / trading | Webinar participant list |
| Principal name | Full name of 1–2 key principals | LinkedIn / firm website |
| LinkedIn profile URL | Direct URL to individual LinkedIn profile | LinkedIn manual lookup |
| LinkedIn activity level | Active poster / Passive / Not present | LinkedIn manual check |
| Tier | 1 = Active poster confirmed; 2 = Present, not active; 3 = Not on LinkedIn | Derived |

**Tier 1 threshold**: A principal qualifies as Tier 1 if they have posted or commented on LinkedIn within the last 30 days.

**MVP effort**: 3–5 hours of focused work (founder or structured agent workflow).

---

## Full Spreadsheet — Phase 1 Complete (target: by 4 June 2026)

All MVP columns plus:

| Column | Description | Source |
|---|---|---|
| Headcount band | 1–10 / 11–30 / 31–50 / 50+ | LinkedIn company page / NZ Companies Office |
| Service lines | Geotech / Civil / Structural / Environmental (multi-select) | Firm website |
| Location | City / region (Auckland, Wellington, Christchurch, Other) | Firm website / Companies Office |
| NZ Companies Office number | Registration number | companiesoffice.govt.nz |
| ACENZ member | Y / N | ACENZ public member list |
| Engineering NZ member | Y / N | engineeringnz.org public list |
| CEAS warm flag | Y = attended CEAS/Aon May 2026 webinar | Derived from participant list |
| Notes | Researcher observations | Researcher |

**Full effort**: 15–20 hours (founder part-time over 2–3 weeks, or agent-assisted batch workflow).

---

## Data Sources

| Source | Access | Legal status |
|---|---|---|
| CEAS/Aon webinar participant list | Founder-held | Legally clean — company names only extracted, no personal data from the event |
| NZ Companies Office | companiesoffice.govt.nz | Public registry, free |
| LinkedIn | linkedin.com | Public profiles — manual lookup only; no scraping or automated extraction |
| Engineering NZ member list | engineeringnz.org | Public facing |
| ACENZ member list | acenz.net.nz | Public facing |
| Firm websites | Various | Public |

**Data handling constraint**: No personal email addresses or phone numbers to be captured. Individual names are sourced only from public LinkedIn profiles and firm websites. The goal is LinkedIn profile URL + activity classification, not PII (Personally Identifiable Information) accumulation.

---

## Output Files

| Phase | File | Owner | Due |
|---|---|---|---|
| MVP (Tier 1 list) | `output/firmographic-nz-engineering-tier1.csv` | Founder | 21 May 2026 |
| Full spreadsheet | `output/firmographic-nz-engineering-full.csv` | Founder | 4 June 2026 |

---

## Handoff

When MVP is ready: Mark reviews → hands to John with the warm window context (see [hypothesis](../hypotheses/ceas-warm-window-linkedin-conversion.md)).

When full spreadsheet is ready: feeds into Phase 2 ICP validation and bowling-pin expansion planning (no separate initiative needed).

---

## Known Seed Firms — CEAS/Aon Webinar Attendees (14 May 2026)

The following firms sent representatives to the CAS "Insurance for Consulting Engineers"
webinar. All are confirmed CAS members and actively managing PI insurance risk.
**Individual names below are private/internal context only** — sourced from the webinar
participant list. Not for use in cold outreach. LinkedIn research uses publicly available
profiles only (consistent with the data handling constraint above).

| Firm | Individual(s) noted | Initial tier | Notes |
|---|---|---|---|
| Tonkin + Taylor | Harel Lustiger, Michelle Grant, Jonathan Shamrock | — | Large firm. Anti-target per GTM non-goals. Founder's current employer. Exclude from outreach. |
| Lewis Bradford Consulting Engineers | Craig Lewis, Ashley Wilson | TBD | Craig Lewis = CAS Chair. Key strategic contact. |
| LGE Consulting Ltd | Stefan Lanser, Michelle Grant | TBD | Michelle Grant may be webinar host. |
| Kirk Roberts Consulting | Nick Calvert | TBD | |
| Pedersen Read | Andrew Read | TBD | |
| Law Sue Davison Ltd | Charles Sue | TBD | |
| Northland Geotechnical Specialists Limited | Rebekah Buxton | TBD | |
| No 8 Engineering | Oisin Frost | TBD | |
| Powlesland Consulting Ltd | Ian Powlesland | TBD | |
| ETS Engineers Ltd | Emanuel Tsamandakis | TBD | |
| Lang Structural Consulting | Oliver Lang | TBD | |
| Malcolm Nielsen Consulting Engineer (MNCE) | Malcolm Nielsen | TBD | |
| Lyall Green Consultants Ltd | Lyall Green | TBD | |

**Tier classification** (1 = active LinkedIn poster, 2 = present/low activity, 3 = not
on LinkedIn) to be assigned during MVP research phase (target: 21 May 2026).

---

## Open Questions

1. **Participant list format**: RESOLVED — participant list contains both individual
   names and company names. Individual names are for private internal context only
   (see data handling constraint above). LinkedIn lookup proceeds from publicly available
   profiles.
2. **Agent workflow**: Can an agent (e.g., a CrewAI research agent) automate the LinkedIn lookup step, or is this fully manual? Manual is safe; automated scraping violates LinkedIn's ToS. Decision: manual lookup is the only compliant option.
