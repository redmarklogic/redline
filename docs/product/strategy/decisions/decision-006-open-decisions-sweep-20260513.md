# Open Decisions — Document Sweep Findings (2026-05-13)

**Status**: All decided (2026-05-13).
**Raised by**: Document consistency sweep (2026-05-13).
**Deciders**: Mark (Issues 1, 2, 4), Ron (Issues 1, 3), Graeme (Issue 4).

---

## How to use this document

Each issue has a **Decision Required** section. The assigned decider adds their verdict,
updates status to Decided, and updates the downstream files listed under "Files to update."

---

## Issue 1 — Product Surfaces Count: 4 or 5?

**Status**: Pending. **Decider**: Mark (canonical source), Ron (GTM implications).

### Conflict

The agent register and AGENTS.md define Matt's scope as **four product surfaces**:
*web, Word documents, Word taskpane, email agent.*

The hiring report for Matt ([hire-ux-designer-2026-04-20.md](../../../people/drafts/reports/hire-ux-designer-2026-04-20.md))
states Mark defined **five product surfaces** and lists these as the priority surfaces for H2:

1. Skeleton Generator UI
2. Onboarding and SSO gate
3. Quota-exhaustion and conversion nudges
4. Pre-Review annotation UI
5. Impact communication surfaces

These two lists describe surfaces differently — one by delivery channel (web, Word, email),
one by product capability. They may be compatible rather than contradictory, but no canonical
list is on record.

### Decision Required

**Mark**: What is the canonical list of product surfaces, and how should they be named? Are
"onboarding / SSO gate" and "quota-exhaustion nudges" sub-surfaces of the web channel, or
standalone surfaces in their own right? Is "impact communication" the same as the email agent
surface?

**Ron**: Does the GTM motion depend on a specific surface count or ordering? Does calling
something a "surface" vs. a "mode within the web app" affect the positioning story?

### Options

| Option | Description | Implication |
|---|---|---|
| A | Keep four channels (web, Word docs, Word taskpane, email) — sub-divide within channels as needed | Simpler for external comms; internal design work is still grouped by product capability |
| B | Adopt five capability-based surfaces from Mark's hiring input as the canonical definition | More precise for design scoping; requires updating AGENTS.md, agent register, Matt's JD |
| C | Two-level taxonomy: four delivery channels, each with named capability surfaces | Most complete; adds complexity but resolves ambiguity permanently |

### Files to update after decision

- `docs/people/agent-register.md` (Matt row)
- `AGENTS.md` (Matt description)
- `.github/agents/rl.matt.agent.md` (if it exists)

---

## Issue 2 — Pre-Submission: Standalone Surface or Mode Within Pre-Review?

**Status**: Pending. **Decider**: Mark.

### Conflict

The [pre-submission initiative doc](../../initiatives/pre-submission-council-compliance-checker.md)
raises an open question: "Should the Pre-Submission checker need its own product surface, or
is it a mode within the Pre-Review product?"

The [checklist collection research doc](../../../research/20260513-checklist-collection-analysis.md)
lists "Three product surfaces: Pre-Submission (free/freemium), Pre-Review (paid, professional
quality), Pre-Investigation (Phase 3)." This implies Pre-Submission IS a standalone surface.

No PRD or strategy document has resolved this.

### Decision Required

**Mark**: Is Pre-Submission Council Compliance Checker:

(A) A standalone product surface with its own URL, branding, and entry point — a free tool
that lives independently of Pre-Review, acquired via SEO and council engineer referrals?

(B) A free tier or entry mode within the Pre-Review product — the same interface, lower
depth (Depth 1 only), zero cost until quota is hit?

### Options

| Option | Description | Pros | Cons |
|---|---|---|---|
| A | Standalone surface | Lower CAC (direct organic acquisition); cleaner positioning for council-specific users | More engineering work; two surfaces to maintain; brand fragmentation risk |
| B | Mode within Pre-Review | Single codebase; frictionless upsell path; one URL to rank for | Council users arrive in a "paid product" context; may feel bait-and-switch |
| C | Standalone MVP → merge into Pre-Review at scale | Test acquisition independently; absorb into main product if conversion is strong | More pivoting work later |

### Files to update after decision

- [pre-submission-council-compliance-checker.md](../../initiatives/pre-submission-council-compliance-checker.md) — resolve open question on line ~78
- [20260513-checklist-collection-analysis.md](../../../research/20260513-checklist-collection-analysis.md) — update product surfaces description
- [day-in-the-life-author-td-pd.md](../../marketing/day-in-the-life-author-td-pd.md) — update product surfaces diagram
- [strategic-bets.md](../strategic-bets.md) — update Pre-Submission note under Bet 2

---

## Issue 3 — KR1 Deadline Ambiguity: Warning vs. Kill Criterion

**Status**: Clarification needed (not a contradiction). **Decider**: Ron.

### Conflict

Multiple documents use the phrase "KR1: 50 signups in 60 days" as if it is the kill criterion.
The OKR doc ([2026-h2.md](../okrs/2026-h2.md)) correctly explains that:
- **Aug 1 (day 60)**: 50 signups = *warning signal*, triggers founder review
- **Sep 1 (day 90)**: 50 signups = *authoritative kill criterion* for Bet 1

However, the parked decisions ([parked-decisions.md](../decisions/parked-decisions.md)) and the
launch plan ([2026-launch-plan.md](../gtm/2026-launch-plan.md)) say "KR1 fails (< 50 signups in
60 days)" — language that implies 60 days is the kill criterion, not Sep 1.

This is not a factual contradiction. The OKR doc's explanation is correct. The problem is that
downstream documents have not been updated with the two-threshold model.

### Decision Required

**Ron**: Confirm that the two-threshold model (60-day warning, 90-day kill) is the intended
design and should be propagated to all downstream references. OR simplify to a single date.

### Recommendation

Propagate the two-threshold model. Add a one-line clarification in parked-decisions.md and
the launch plan distinguishing the warning from the kill criterion. No strategy change.

### Files to update after decision

- [parked-decisions.md](../decisions/parked-decisions.md) — entries P-016 and P-021: add "(60-day warning only; authoritative kill criterion is Sep 1)"
- [2026-launch-plan.md](../gtm/2026-launch-plan.md) — update KR1 language in the contingency section

---

## Issue 4 — Rule Schema: Are Severity and Depth Level Independent Dimensions?

**Status**: Pending. **Decider**: Mark, with Graeme confirming domain validity.

### Conflict

The Pre-Review rule validation document and the FHWA vocabulary document both use `severity`
(HIGH / MEDIUM / LOW) and `depth_level` (1 / 2 / 3) as rule properties. ADR-006 defines
`depth_level` as part of the canonical rule schema. But neither document explicitly states
whether severity and depth are *orthogonal* (independent) or *correlated* (depth 1 always
HIGH because presence is critical).

Current rules suggest they are orthogonal: SCOPE-LIM-01 is HIGH severity at Depth 1 (presence
of scope limitation clause is critical). But a Depth 1 check for "are photographs included?"
(FHWA item, Tier 1) would be LOW severity. So HIGH is not implied by Depth 1 alone.

If they are not explicitly declared orthogonal, future rule authors may conflate them.

### Decision Required

**Mark**: Confirm that `severity` and `depth_level` are orthogonal dimensions, both required
on every rule. Update the rule schema in ADR-006 to make this explicit.

**Graeme**: Validate that the proposed 2x3 matrix (3 severities x 3 depths) makes domain sense.
Are there cells that should never exist (e.g., Depth 3 / LOW severity — a method validation
check that is unimportant)?

### Proposed Rule Schema (for Mark's review)

```
rule_id: str
statement: str           # The check question (reviewer voice)
taxonomy_node: str       # Which of the 10 nodes this attaches to
workflow_moment: str     # pre-investigation | during-drafting | pre-review | pre-submission
depth_level: int         # 1=presence, 2=content-quality, 3=method-validation
jurisdiction: list[str]  # ["universal"] or ["nz", "au"] etc.
source_standard: str     # Document reference
severity: str            # high | medium | low  (INDEPENDENT of depth_level)
configurable: bool       # Can a firm override via House Rules?
```

### Files to update after decision

- [adr-006-shared-taxonomy-skeleton-checklist-prereview.md](../../../adr/adr-006-shared-taxonomy-skeleton-checklist-prereview.md) — add explicit schema definition with orthogonality note
- [fhwa-reviewer-checklist-rule-vocabulary.md](../../../knowledge/geotechnical/report-writing/fhwa-reviewer-checklist-rule-vocabulary.md) — update tables to include both `severity` and `depth_level` columns explicitly
- [pre-review-rule-validation-scope-and-language-checks.md](../../../knowledge/geotechnical/report-writing/pre-review-rule-validation-scope-and-language-checks.md) — add schema reference

---

## Issue 5 — 10-Node Taxonomy: Duplicate Table in Two Documents

**Status**: Low priority / maintenance risk. **Decider**: Mark.

### Conflict

The 10-node taxonomy table appears identically in:
1. [checklist-taxonomy-cross-jurisdiction.md](../../../knowledge/geotechnical/report-writing/checklist-taxonomy-cross-jurisdiction.md)
2. [adr-006-shared-taxonomy-skeleton-checklist-prereview.md](../../../adr/adr-006-shared-taxonomy-skeleton-checklist-prereview.md)

If a node name is updated in one, the other silently diverges.

### Decision Required

**Mark**: Should the 10-node taxonomy be extracted to a single canonical reference file
(`docs/knowledge/geotechnical/report-writing/canonical-taxonomy.md`) and both ADR-006
and the cross-jurisdiction analysis link to it? Or is the duplication acceptable given that
ADRs are typically immutable after acceptance?

### Options

| Option | Description |
|---|---|
| A | Extract to `canonical-taxonomy.md`; both documents link to it | Single source of truth; any change is visible in both contexts |
| B | ADR-006 is immutable (by ADR convention); only the knowledge doc is the live reference; ADR-006 is explicitly marked "taxonomy defined at 2026-05-13; see knowledge doc for current version" | Respects ADR immutability; adds a clarifying note |
| C | Accept duplication; low-risk given stable taxonomy | No effort now; risk of silent drift over time |

**Recommended**: Option B. ADRs should not be mutated; adding a note that the knowledge doc
is the live reference respects that convention while directing readers to the right place.

### Files to update after decision

- [adr-006-shared-taxonomy-skeleton-checklist-prereview.md](../../../adr/adr-006-shared-taxonomy-skeleton-checklist-prereview.md) — add note under taxonomy table pointing to knowledge doc as live reference

---

## Decisions Log

| Issue | Decider | Status | Decision | Date |
|---|---|---|---|---|
| 1 — Product surfaces count | Mark, Ron | Decided | Four delivery channels (web, Word docs, Word taskpane, email). Capability areas are sub-surfaces of channels. Hiring draft corrected. | 2026-05-13 |
| 2 — Pre-Submission scope | Mark | Decided | Mode within Pre-Review (Option B). Same codebase, Depth 1 rules, free tier. Initiative doc, research doc, day-in-the-life updated. | 2026-05-13 |
| 3 — KR1 deadline ambiguity | Ron | Decided | Two-threshold model confirmed. Aug 1 = warning (founder review triggered, bet continues). Sep 1 = authoritative kill criterion. Parked-decisions P-016, P-021 and launch plan updated. | 2026-05-13 |
| 4 — Rule schema orthogonality | Mark, Graeme | Decided | `severity` and `depth_level` are orthogonal. Full schema with code block added to ADR-006. | 2026-05-13 |
| 5 — Taxonomy duplication | Mark | Decided | ADR-006 is immutable (snapshot). Pointer note added in ADR-006 directing to knowledge doc as live reference. | 2026-05-13 |
