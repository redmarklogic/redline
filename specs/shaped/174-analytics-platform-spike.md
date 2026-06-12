# Pitch: Analytics Platform Spike (#174)

**Shaped by:** Peter (Principal Engineer)
**Date:** 2026-06-12
**Sprint:** 3 (Jun 15–21, 2026) — WBS item 5.1, ★d1 (starts Monday Jun 15)
**Serves:** Bet 1 (Free Skeleton Wedge) → KR1 (verified-email signups)
**Source:** `docs/product/tasks/sprint-3-goal.md` (founder-ratified 2026-06-12); GitHub issue #174
**Successor:** #175 "Wire chosen platform" (WBS 5.2 — *below the sprint cut line; may never run this sprint*)

> **Note on process:** No PRD exists for this item, and none is required. This is a
> one-day timeboxed spike shaped directly from the founder-ratified sprint plan,
> which serves as the discovery artifact. The deliverable being shaped is the
> *decision process* (shortlist → same-day founder pick → decision note), not an
> implementation. This Pitch does not enter SpecKit; Peter executes the spike directly.

---

## Diagnosis

- **Stage:** Pre-revenue proof of concept. First Django app deploying to staging this sprint. Phase-1 architecture is explicitly disposable (ADR-024), so vendor lock-in is a theoretical concern, not a binding one.
- **Binding constraints right now:**
  - **Appetite is one day** (Monday Jun 15), fixed by the founder. The successor wiring task (5.2 / #175) is below the cut line and yields first — so the spike's output must stand alone and survive into Sprint 4 if 5.2 never runs.
  - **Agent-operability hard filter:** the platform must expose a CLI (command-line interface), an MCP (Model Context Protocol) server, or an API (application programming interface). A dashboard-only product fails the filter regardless of other merits, because this team operates through agents.
  - **Cost ceiling:** total pre-revenue cloud spend is designed to $100/month (billing alert at $80, hard stop-and-talk at $150). In practice the platform must be free-tier or near-free.
  - **Data residency claim:** the founder has an approved commercial claim — "all data stays in Australia" — with infrastructure pinned to `australia-southeast1`. Analytics event rows contain email and name (personal data), so residency posture is decision-relevant. (Founder ruling 2026-06-12: *weighted column* — the claim binds primary product data only; residency posture is scored on the shortlist, not disqualifying.)
  - **The floor is non-negotiable:** the Cloud SQL append-only audit log (WBS 2.4 / #166) is the guaranteed landing place for events. Any external platform is additive, never a replacement.
  - **Founder same-day availability:** the spike's "done" includes a founder decision on the same day. Without a founder slot on Monday, the spike cannot close.
- **Theoretical-only constraints (explicitly not binding):** event volume and scale (a handful of founder-access users clicking three buttons), analytics sophistication (funnels, cohorts, retention), long-term vendor strategy, multi-region anything.

**Surviving the Round test:** Short-runway view (3–6 months): KR1 needs the team to *see* signups and clicks; the DB floor plus Django admin already delivers minimal visibility, so an external platform is a convenience purchase — justified only at one day of effort and ~zero dollars. Long-runway view (2+ years): a richer analytics stack would justify deeper evaluation, but that is exactly the justification we must refuse now. The one-day appetite and 5.2's below-the-line position are the correct expression of this. Anything heavier is descoped.

---

## Problem

Sprint 3's goal is an SSO-gated signal loop: the team must see who signed in and which buttons they clicked. The DB audit log guarantees the events exist, but reading raw rows in Django admin is the floor, not the intended end state — WBS 5.2 envisions an external product-analytics platform on top. Before anything can be wired, a platform must be chosen, and the choice has a hard, unusual filter (CLI/MCP/API for agent operation) that rules out default picks chosen on brand familiarity.

Left unshaped, this decision has two failure modes:

1. **Research-forever:** platform evaluation is a bottomless comparison exercise; without a timebox and a forced same-day decision, it eats the week that belongs to the SSO critical path.
2. **Decision-by-wiring:** skipping the spike and letting #175 "just pick something" embeds an unexamined choice into code, with residency and cost discovered after integration.

The spike exists to convert an open-ended evaluation into a one-day, founder-decided, documented choice — or an equally valid documented *deferral*.

## Appetite

**One day. Monday, June 15, 2026.** Fixed time, variable scope.

- If the candidate scan runs long, the shortlist shrinks — it does not spill into Tuesday.
- **Circuit breaker:** by end of Monday, the founder picks from whatever shortlist exists, or explicitly defers the external platform entirely (DB floor only). Either outcome closes the spike. "Still researching" is not a permitted end state.
- The spike's output must be self-contained enough that #175 can be picked up cold in Sprint 4, because 5.2 is below the cut line and is expected to yield.

## Solution Outline (breadboard — components and connections only)

```
[Hard Filter]
  criteria: agent surface (CLI/MCP/API) • residency posture •
            cost within $100/mo ceiling • additive to DB floor •
            server-side event emission from Django on Cloud Run
       |
       v
[Candidate Scan]  -- desk research only; no accounts, no SDKs, no test events
       |
       v
[Shortlist Table] -- one page, 2–4 candidates max
  columns: agent surface (CLI / MCP / API — which, and official vs community) |
           AU residency posture | free tier / monthly cost |
           server-side ingestion fit | wiring-effort estimate for #175 |
           trust-boundary impact (would wiring trigger a Tier-1 review?)
       |
       v
[Founder Decision] -- same-day, synchronous
  outcomes: (a) pick one candidate  (b) defer external platform, DB floor only
       |
       v
[Decision Note] -- short, written to docs/research/
  contents: chosen platform (or deferral) + the shortlist table +
            one-paragraph rationale + what #175 needs to know to start cold
       |
       v
[#175 unblocked] -- this sprint if capacity allows; Sprint 4 otherwise
```

Notes on the breadboard:

- **No platform is prescribed here.** The Pitch shapes the filter, the table, and the decision ritual. The founder makes the pick.
- The decision note lives in `docs/research/` as a spike artifact. It is deliberately *not* an ADR (Architecture Decision Record): the architectural moment is the *wiring* (#175), where a new data-egress path may expand the trust boundary. If it does, that triggers the existing Tier-1 approval route and an ADR at that point — not during this spike.
- "Server-side ingestion fit" matters because events originate from Django views on Cloud Run (the click handler that writes the audit row), not from browser JavaScript. A platform that only offers a browser snippet scores poorly.

## Rabbit Holes (identified and fenced)

1. **Hands-on trialing.** Signing up for accounts, installing SDKs (software development kits), or sending a single test event is wiring, not deciding. That is #175's job. The spike is desk research against documentation only.
2. **Residency redesign.** If candidates cannot pin analytics data to Australia, the temptation is to redesign the event schema (pseudonymise, strip email/name) to make the claim hold. That is a design exercise, not a spike. The fence: residency is a *column in the table*; if nothing passes, the founder's deferral option (DB floor only) is the designed escape hatch.
3. **Pricing-model spelunking.** No spreadsheets projecting event volumes against pricing tiers. The ceiling is $100/month total; one line per candidate ("free tier covers us" / "starts at $X") is sufficient at our event volume of approximately zero.
4. **MCP-quality evaluation.** Assessing the maturity, spec-compliance, or feature coverage of a candidate's MCP server is a checkbox, not an investigation: official / community / none.
5. **Self-hosting architecture.** Self-hostable platforms are seductive for residency (run it in `australia-southeast1` ourselves) but smuggle in infrastructure cost, Brent's time, and a Tier-1 trust-boundary review. A self-hosted candidate may appear on the shortlist only with an honest wiring-effort estimate that includes those costs. No deployment design happens in the spike.
6. **Decision drift.** "Let's sleep on it" converts a one-day spike into a week-long shadow. The circuit breaker above is the fence: end of Monday, pick or defer.

## No-Gos

- **No account creation, SDK installation, or event sent to any external platform.** That is #175.
- **No change to the DB audit-log floor** (2.4 / #166) — no schema edits, no "the platform replaces it" reasoning. Additive only.
- **No production code and no Django settings changes** during the spike.
- **No platform recommendation baked into this Pitch.** The shortlist informs; the founder decides.
- **No ADR required to close the spike.** Decision note in `docs/research/` suffices; the ADR trigger (if any) fires at wiring time when the trust boundary actually moves.
- **No paid-plan commitment** of any kind.
- **No shortlist longer than 4 candidates and no document longer than one page** (excluding the decision rationale paragraph).

## Done When (restated from #174, with the spike's own teeth)

- A shortlist (≤ 1 page, 2–4 candidates) exists, every candidate passing the CLI/MCP/API hard filter, with the six breadboard columns filled.
- The founder has made a same-day decision: a named platform, or an explicit deferral to DB-floor-only.
- A short decision note is written to `docs/research/`, self-contained for a cold Sprint-4 pickup of #175.
- The DB audit-log floor stands untouched.
- All of the above happened on Monday, June 15.

## Founder Rulings (2026-06-12 — all three open questions resolved at shaping)

1. **Founder decision slot: confirmed.** Founder is available Monday Jun 15 to review the shortlist and pick same-day.
2. **Residency: weighted column.** The "all data stays in Australia" claim binds primary product data only, not analytics event data. Residency posture is a scored column on the shortlist, not a disqualifying filter.
3. **Deferral pre-approved.** "Defer external platform, DB floor only" is a valid same-day spike outcome, not a failure. The sprint goal survives via 4.3's Django-admin viewer.

---

**Approval per shaping process:** Mark co-owns appetite. The one-day appetite is already founder-ratified in the sprint plan, so I treat business-appetite approval as given; Mark should flag within the trio if he disagrees before Monday.
