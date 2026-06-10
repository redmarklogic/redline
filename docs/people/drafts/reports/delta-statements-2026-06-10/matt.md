# Delta Statement — Matt (UI/UX Designer) — Topology Sync 2026-06-10

**Reflection windows used:** R1 = 2026-06-07 → 2026-06-10 (facilitator's enumerated changes, verified directly). R2/R3 = **widened to 2026-05-09 → 2026-06-10** (date of my JD's knowledge-base memo) because my live reflection has never happened — syncs 05-17, 05-23, 06-06, and 06-07 all synthesized my deltas in absentia, and the earlier 06-10 run deferred me. This is my first live R2 and R3.

## 1. Here is what I own today

- Design specifications across four surfaces: web application and Word document output (active), Word taskpane and email agent (deferred, not foreclosed). Sole write owner of `docs/product/design/`. Maturity: Draft-first.
- Owner of the **Product Design & UX** notebook; consumer on geotechnical-report-workflows, technical-communication, and django-application-development (per `register.json`).
- H2 priority outcome: Skeleton Generator UI designed and spec'd for the **2026-06-30** ship date, supporting SSO gate, quota cap, and quota-exhaustion trigger (Bet 1 kill criterion).
- **Honest state of my domain:** `docs/product/design/` contains only two reference docs (`house-rules-design-references.md`, `pre-review-ux-references.md`). **No Skeleton Generator design spec exists.** The PRD exists (`docs/product/prds/skeleton-generator-prd.md`), but `specs/shaped/` is **empty** — no Touch 1 constraints memo from Peter. Under the Two-Touch model I cannot begin wireframes without it. With the ship date 20 days out and the deploy chain now live (PR #97, ADR-022), the design-spec critical path is the most decision-relevant fact in this statement. **Ask for the session:** Peter to deliver the Touch 1 memo (Mark to confirm PRD readiness) so design can start this week.

## 2. Here is what has changed in my domain since the last sync (evidence R1–R3)

- **R1, confirmed:** the facilitator's drift note holds. ADR-019 (platform boundary), ADR-020 (Terraform), ADR-021 (env config), and specs 004/005/005-gcp/006/70 contain no user-facing surface content — verified by reading the ADRs and grepping all spec bodies (only matches: developer-facing Swagger UI and Docker onboarding).
- **R1, one design-adjacent item:** ADR-022 defers SSO/IdP wiring to **B-1b scope (issue #73)** with a Bearer-presence placeholder, and PR #97 stands up staging+prod on Cloud Run (australia-southeast1). Implications: (a) my SSO gate / onboarding design must exist before B-1b implementation starts — a concrete sequencing hook for Outcome 2; (b) a live staging URL will soon exist, making my Website Review Protocol executable against real deploys. No JD change required.
- **R1, Brent onboarded:** zero handoff edges to or from me in `brent.md` — "no Brent contact by design" still holds. No JD change.
- **R1, F-2 noted:** AGENTS.md epistemic-honesty clause omits me from its agent list. Awareness only (owner: founder); my JD carries the clause inline, so my behaviour is unaffected.
- **R2, verbatim core finding:** my owned notebook "cannot answer questions about events after their publication dates… publication date range of the sources provided is between 2008 and 2017." Consumer notebooks likewise (technical-communication sources 2000–2014; report-workflows newest source is the EnggNZ/NZGS Guideline, August 2023, with no supersession information). My knowledge base has no currency mechanism — R3 is load-bearing for me every sync.

## 3. Here is where my current JD or skills may now be incorrect, incomplete, or outdated

1. **JD Knowledge Base section is factually false.** It claims 7 books currently in the notebook; `nlm source list` shows **4** (Norman, Krug, Forms that Work, Designing with Data). Refactoring UI, Laws of UX, and About Face are absent. None of the six additions promised "by 2026-05-20" ever landed — including **Practical Typography, named "the single most important resource" for my highest-priority surface, now 3 weeks overdue.** Downstream defect: my Self-Review Discipline Step 2 mandates "the 8-item cognitive load checklist from Laws of UX" — a source I cannot query; my JD instructs me to cite Refactoring UI and Laws of UX as sufficient grounding for web work — half of that grounding does not exist in my notebook. This is the ADR-001 SSOT failure mode in miniature: the JD restates notebook contents inline, and the restatement drifted.
2. **Source metadata wrong in both JD and register:** "Designing with Data — Suda (2010)" is actually King, Churchill & Tan, O'Reilly, **2017** (verbatim from the notebook's own citation). Register correction is Linda's; JD correction is a patch item.
3. **R3 finding:** [Jon Yablonski / O'Reilly] [March 2024] [Laws of UX **2nd edition** published — same 11 chapters, updated examples, deeper psychology, new AI-era context] [Impact: JD cites the superseded 2020 edition — and the book is absent from the notebook entirely].
4. **R3 finding:** [microsoft/playwright-mcp, playwright.dev] [current] [Canonical Playwright MCP tool names are `browser_navigate`, `browser_snapshot`, `browser_click`, etc.] [Impact: my Website Review Protocol hardcodes `mcp_microsoft_pla_browser_*` — a client-specific prefixed form that matches neither canonical naming nor this environment's `mcp__<server>__<tool>` convention; the protocol's tool references are likely non-resolving as written].
5. **R3 finding:** [W3C; AHRC via Deque/OZeWAI] [2023–2026] [WCAG 2.2 AA is the current standard (ISO/IEC 40500:2025); the Australian Human Rights Commission affirmed WCAG 2.2 Level AA as the minimum under the DDA, explicitly covering **SaaS platforms**; NZ Web Accessibility Standard 1.1 sits at WCAG 2.1 AA] [Impact: my JD contains **zero accessibility requirements** — no design principle, no Self-Review step, no viewport/AT check. For an AU/NZ-beachhead B2B SaaS hosted in australia-southeast1, this is a genuine JD gap, not gold-plating].
6. **R2 Q2 gaps, filtered through Redline constraints as my JD requires:** (a) my Self-Review Discipline is expert-simulation only (heuristics + persona walk-through); the sources (Krug: "three users, one morning a month"; Norman: iterative HCD) recommend testing with real users — Phase 1's 10 co-development partners are exactly that resource, and my JD has no hook into that loop (discovery is Mark's domain; the hook should be a handoff, not a new Matt responsibility); (b) no worst-case-data stress check in Self-Review (Norman: assume every mishap; directly relevant to one-click LOE upload — malformed PDFs, 100-page-cap edges); (c) the sources' A/B testing recommendation is **flagged inapplicable** at current scale — n=10 partners cannot power an experiment; the applicable lightweight version is a stated behavioural hypothesis per design spec alongside the existing PostHog instrumentation points.

## 4. Here are the frameworks or guidelines I think need to be added or updated

1. **Sourcing request to Linda (via the founder/facilitator — not a dispatch I hold):** add Laws of UX **2nd ed. (2024)**, Refactoring UI, About Face, and Practical Typography (URL source) to the Product Design & UX notebook; then the remaining promised titles (Strategic Writing for UX, Writing Is Designing, Articulating Design Decisions, Continuous Discovery Habits, Design That Scales). Correct the register's Designing with Data metadata (King/Churchill/Tan, 2017).
2. **JD patch — Knowledge Base section:** stop restating notebook contents inline (ADR-001); point to `register.json` and `nlm source list` as the authoritative inventory, keep only the reading-priority guidance.
3. **JD patch — accessibility baseline:** add WCAG 2.2 AA as a Design Principle (Do #8) and a Self-Review step (keyboard reachability, contrast, focus order, target size at minimum), with the NZ 2.1-AA note for government-adjacent users.
4. **JD patch — Website Review Protocol:** replace hardcoded `mcp_microsoft_pla_browser_*` identifiers with canonical tool names (`browser_navigate`, `browser_snapshot`, `browser_take_screenshot`, `browser_console_messages`, `browser_network_requests`), environment prefix left to the runtime.
5. **JD patch — Self-Review Discipline:** add a worst-case-data stress check (Step 2b), and a Step 6 hook: when co-development partner feedback exists (Mark's discovery loop), reconcile it against the persona walk-through before handoff.
6. **No change** to surface priorities, Two-Touch model, dispatch edges, or design hard rules — R1 confirmed none of the window's decisions touch them.

---

## Evidence & gaps

- **R1 — COMPLETE.** Read: `strategic-bets.md`, ADR-019/020/021/022, sync reports 2026-06-07 and 2026-06-10, my JD, `register.json`; verified spec bodies via grep; verified `docs/product/design/`, `docs/product/prds/`, `specs/shaped/` state; verified `brent.md` has no Matt edges.
- **R2 — COMPLETE for my owned notebook** (both mandated questions, verbatim output captured via `nlm`, auth verified) **plus** the currency question on two of three consumer notebooks (geotechnical-report-workflows, technical-communication). **Scoping decision:** I did not query `django-application-development` — it is Kabilan-owned implementation-framework material where my access is capability-checking during design; its currency reflection belongs to its owner. Recorded as proportionality, not an access failure.
- **R3 — COMPLETE.** Three targeted searches (Laws of UX edition, Playwright MCP tool names, accessibility baseline). Notebook-first order honoured: every searched topic was first put to the notebooks, which confirmed inability to answer.
- **Gap — CCE:** `session_recall`/`context_search` were not available in this thread's toolset (no MCP tools loaded for a dispatched agent); discovery fell back to Glob/Grep/Read. No findings fabricated to cover the gap.
- **Gap — Miro MCP:** not exercised; no visual artifact was required for this reflection.

Sources:
- [Laws of UX Book, 2nd Edition — Jon Yablonski](https://jonyablonski.com/articles/2024/laws-of-ux-the-2nd-edition/)
- [Laws of UX, 2nd Edition — O'Reilly](https://www.oreilly.com/library/view/laws-of-ux/9781098146955/)
- [microsoft/playwright-mcp — GitHub](https://github.com/microsoft/playwright-mcp)
- [Playwright MCP — playwright.dev](https://playwright.dev/docs/getting-started-mcp)
- [WCAG 2 Overview — W3C WAI](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [Three major accessibility updates in Australia — Deque](https://www.deque.com/blog/accessibility-updates-in-australia-in-2026/)
- [Three major accessibility updates in Australia — OZeWAI](https://ozewai.org/blog/standards/three-major-accessibility-updates-in-australia/)
- [Web Accessibility laws in Australia & New Zealand — Siteimprove](https://www.siteimprove.com/blog/web-accessibility-laws-in-australia-new-zealand/)

**Next action:** facilitated session input delivered. After the session, my first move is the Skeleton Generator design spec — gated on Peter's Touch 1 constraints memo, which I am formally requesting through this sync.
