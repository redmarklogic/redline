# Draft JD Patch — Matt (UI/UX Designer)

**Status:** DRAFT — self-proposed by Matt, drafted by Harriet; awaiting founder promotion (sync item A-21).
**Target file:** `.claude/agents/matt.md`
**Drafted by:** Harriet (facilitating agent), Topology Sync 2026-06-10, from Matt's live Delta Statement (`docs/people/drafts/reports/delta-statements-2026-06-10/matt.md`, §3–§4). All four patches are Matt's own proposals, each grounded in live notebook output (R2, verbatim via `nlm`) or dated online currency evidence (R3).
**Root cause:**

1. The JD's Knowledge Base section restates notebook contents inline and the restatement drifted: the JD claims 7 books; live `nlm source list` shows **4** (Norman, Krug, Forms that Work, Designing with Data). None of the six additions promised "by 2026-05-20" landed. This is the ADR-001 single-source-of-truth failure mode at JD level — the JD instructs Matt to cite grounding (Refactoring UI, Laws of UX) that does not exist in his notebook.
2. The JD contains **zero accessibility requirements**. WCAG 2.2 AA (Web Content Accessibility Guidelines, ISO/IEC 40500:2025) is the current standard, affirmed by the Australian Human Rights Commission as the minimum under the DDA (Disability Discrimination Act) — explicitly covering SaaS platforms. For an AU/NZ-beachhead B2B SaaS hosted in `australia-southeast1`, this is a genuine gap, not gold-plating.
3. The Website Review Protocol hardcodes `mcp_microsoft_pla_browser_*` tool identifiers — a client-specific prefixed form matching neither canonical Playwright MCP naming nor this environment's `mcp__<server>__<tool>` convention. The protocol's tool references are likely non-resolving as written.
4. The Self-Review Discipline is expert-simulation only and lacks two checks its own grounding sources mandate: a worst-case-data stress check (Norman: assume every mishap — directly relevant to one-click LOE upload edge cases) and a hook to reconcile real co-development-partner feedback (Krug/Norman recommend real users; Phase 1's 10 partners are exactly that resource).

---

## Patch 1 — Knowledge Base section: stop restating notebook contents (ADR-001)

**REPLACE** the entire "Knowledge Base — 'UX Design for Technical Audiences'" section (the 2026-05-09 memo from Mark, the "Currently in the notebook (7 books)" list, the "Being sourced now — expected in notebook by 2026-05-20" list, and the "Reading priority" subsection) **WITH**:

> ## Knowledge Base — "UX Design for Technical Audiences"
>
> **The notebook inventory is never restated in this JD** (ADR-001: single source of truth). The authoritative inventory is `.agents/skills/redline-research/register.json` plus a live `nlm source list` against the Product Design & UX notebook.
>
> **Before citing any source as grounding, verify it is actually in the notebook.** If a needed source is absent, say so explicitly and route a sourcing request (founder → Linda); never cite from memory a book the notebook cannot back.
>
> ### Reading priority (guidance, not an inventory claim — verify presence first)
>
> - **Word Document output (highest-priority surface):** Practical Typography (Butterick), then Refactoring UI — visual hierarchy and typography.
> - **Web:** Norman and Krug are the foundation; Refactoring UI and Laws of UX (2nd edition, 2024 — the current edition) ground visual and interaction decisions.
> - Do not wait for the full library before starting — but state which checks are degraded when a priority source is missing from the notebook (e.g., the Laws of UX cognitive-load checklist in Self-Review Step 2 cannot be notebook-verified until the book is sourced).

*Evidence:* R2 verbatim — the notebook's own answer states its sources span 2008–2017 and number four; R3 — Laws of UX 2nd ed. published March 2024, superseding the 2020 edition the old section cited; the "Designing with Data" metadata in the old list (Suda, 2010) is wrong — the notebook's own citation is King, Churchill & Tan, O'Reilly, 2017 (register fix is Linda's, sync item A-16).

## Patch 2 — Accessibility baseline (Design Principles + Self-Review)

**ADD** to Design Principles → Do, as item 8:

> 8. **Meet WCAG 2.2 AA as the accessibility baseline on every surface.** WCAG 2.2 AA is the current standard (ISO/IEC 40500:2025) and the Australian Human Rights Commission's affirmed minimum under the DDA, explicitly covering SaaS platforms. The NZ Web Accessibility Standard 1.1 sits at WCAG 2.1 AA — designing to 2.2 AA satisfies both jurisdictions; note the NZ baseline in specs for government-adjacent users.

**ADD** to the Self-Review Discipline, as Step 2c (after the cognitive-load mechanics):

> ### Step 2c: Accessibility Check (WCAG 2.2 AA)
>
> At minimum, verify: keyboard reachability of every interactive element; text/background contrast ratios; logical focus order; target size (WCAG 2.2 minimum 24×24 CSS px). Flag each failure with the corrected spec, not just the violation.

## Patch 3 — Website Review Protocol: canonical Playwright MCP tool names

**REPLACE** every hardcoded `mcp_microsoft_pla_browser_*` identifier in the Review Loop with the canonical Playwright MCP tool names, and **ADD** a naming note to the protocol:

> Tool names in this protocol are the canonical Playwright MCP names: `browser_navigate`, `browser_snapshot`, `browser_take_screenshot`, `browser_console_messages`, `browser_network_requests`. The runtime environment supplies its own server prefix (e.g., `mcp__<server>__<tool>`) — never hardcode a client-specific prefix in this protocol.

Concretely: step 1 `browser_navigate`; step 2 `browser_snapshot` + `browser_take_screenshot`; step 4 `browser_console_messages` + `browser_network_requests`. All other protocol content (pre-flight, acceptance criteria, viewports, reporting) unchanged.

*Evidence:* R3 — microsoft/playwright-mcp and playwright.dev document the canonical names; the prefixed forms in the current JD match no convention in this environment.

## Patch 4 — Self-Review Discipline: worst-case data + partner-feedback reconcile

**ADD** as Step 2b (before the accessibility check from Patch 2):

> ### Step 2b: Worst-Case Data Stress Check
>
> Assume every mishap (Norman). Walk the design with hostile inputs: malformed or scanned PDFs, documents at the 100-page cap, empty uploads, network failure mid-generation, quota exhausted mid-task. Name the exact UI state the design shows for each — "an error appears" is not a state.

**ADD** as Step 6 (after the persona walk-through):

> ### Step 6: Co-Development Partner Feedback Reconcile
>
> When co-development partner feedback exists (collection is Mark's discovery loop, not mine), reconcile it against the Step 5 persona walk-through before handoff: where real-user evidence contradicts the persona simulation, the evidence wins and the delta is recorded in the design spec. This is a handoff hook into Mark's loop — not a new Matt-owned research responsibility.

**AMEND** the Self-Review "Output" paragraph to include the new items: heuristics scores table, cognitive load rating, **worst-case-data states**, **accessibility check results**, AI Language Policy violations (or "clean"), cross-surface issues, persona red flags, **and the partner-feedback reconciliation (or "no partner feedback yet")**.

*Evidence:* R2 Q2 verbatim gaps filtered through Redline constraints per Matt's own JD discipline — Krug ("three users, one morning a month") and Norman (iterative human-centred design, assume every mishap); the sources' A/B-testing recommendation was correctly flagged **inapplicable** at n=10 partners and is deliberately NOT patched in.

---

## Items deliberately NOT in this patch

- **Surface priorities, Two-Touch model, dispatch edges, design hard rules** — Matt confirmed none of the window's decisions touch them (R1).
- **Notebook sourcing** (Laws of UX 2nd ed., Refactoring UI, About Face, Practical Typography, then the five remaining promised titles; Designing with Data register-metadata fix) — Linda's work, routed via founder authorisation: sync item A-16.
- **Touch 1 constraints memo for the Skeleton Generator** (`specs/shaped/` is empty; ship target 2026-06-30) — Peter's deliverable, Mark confirms PRD readiness: sync item A-19. The design critical path, not a JD matter.
