> DRAFT — pending user approval. Do not promote to production.

# Hire Report: UI/UX Designer (Matt)

**Date:** 2026-04-20
**Requested by:** Founder
**Agent file:** `rl.matt.agent.md`
**Mode:** HIRE
**Conducted by:** Harriet (Head of People & Agent Development)

## Step 0 — Screening: When NOT to Hire

I screened this hire against Team Topologies' four "do not create a new team" patterns.

| Pattern | Result | Reasoning |
|---|---|---|
| Reactive / ad-hoc creation | **Pass** | This role is tied to four active strategic bets and addresses a genuine capability gap (no agent currently holds design capability). It is not a reaction to a single failure. |
| Single-function silo | **Pass** | Matt would own four product delivery surfaces (web app, Word document output, Word taskpane, email agent) with end-to-end design responsibility across each. This is not a single-function overlay applied to everyone else's output. |
| Complicated-subsystem without cognitive-load justification | **Pass** | No existing agent holds design capability. Mark handles product management (problem framing, PRDs, decisions). John handles marketing content and brand voice. Neither has the skills or cognitive bandwidth for interaction design, wireframing, or component specification. This is a new capability, not a split of an existing agent's domain. |
| No active strategic bet pulls on this role | **Pass** | Four active bets require UX design work: Bet 1 (Skeleton Wedge UI, ships Jun 30), Bet 2 (Pre-Review annotation UI), Bet 4 (Switzerland-neutral positioning expressed in product surfaces), and Bet 6 (impact communication surfaces). Bet 1 has a hard kill criterion deadline (90 days from launch). |

**Screening verdict:** Hire is justified. Proceed.

## Step 1 — Work Deconstruction (Jesuthasan & Boudreau Four-Step Framework)

### Elemental Task List

| # | Task | Repetitive / Variable | Independent / Interactive | Deterministic / Judgment | ROIP | Disposition |
|---|---|---|---|---|---|---|
| 1 | Design the Skeleton Generator UI (wireframes, interaction flows, component specs) | Variable | Interactive (with Mark for PRD, Graeme for domain terms) | Judgment | Exponential — directly enables Bet 1 ship date | **Create** |
| 2 | Design the onboarding and SSO gate flow | Variable | Interactive (with Mark, John for funnel continuity) | Judgment | High — signup abandonment reduces Bet 1 kill criterion metric | **Create** |
| 3 | Design quota-exhaustion and conversion nudge interfaces | Variable | Interactive (with John for messaging, Mark for triggers) | Judgment | Exponential — the highest-leverage design decision for the Bet 1 kill criterion (outbound response rate) | **Create** |
| 4 | Design the Pre-Review annotation UI | Variable | Interactive (with Mark for PRD, Graeme for domain review) | High judgment | Exponential — the core paid product surface for Bet 2 | **Create** |
| 5 | Design impact communication surfaces (post-session summaries) | Variable | Interactive (with Mark, John) | Judgment | High — retention mechanism for Bet 6 | **Create** |
| 6 | Define interaction patterns and component library for the platform | Variable | Independent | Judgment | High — consistency reduces future design cost and engineering rework | **Create** |
| 7 | Specify PostHog instrumentation points in design specs | Repetitive | Independent | Low judgment | Moderate — ensures telemetry coverage without engineering guesswork | **Augment** (embedded in design workflow, not a standalone task) |
| 8 | Review designs for domain terminology accuracy with Graeme | Variable | Interactive | Judgment | High — prevents domain errors reaching users | **Augment** (Matt + Graeme) |
| 9 | Review designs for positioning alignment with John | Variable | Interactive | Judgment | High — prevents marketing/product visual disconnect | **Augment** (Matt + John) |
| 10 | Produce design specifications for engineering handoff | Variable | Independent | Judgment | High — reduces engineering interpretation errors | **Substitute** (Matt fully owns) |

### Disposition Summary

- 6 tasks are "Create new work" — capabilities that do not exist today.
- 3 tasks are "Augment" — Matt collaborates with existing agents (Graeme, John) or embeds a lightweight procedure in a broader task.
- 1 task is "Substitute" — Matt fully owns the output with no dependency.

Most tasks are **Variable + Interactive + Judgment-based**. This profile requires a dedicated agent, not a skill bolted onto an existing agent. If the majority had been Repetitive + Independent + Low-judgment, I would have recommended writing a skill for Mark instead. That is not the case.

**Conclusion:** The work profile justifies a standalone agent. Proceed to JD drafting.

## Step 2 — Domain Agent Consultation

### Mark's Input (Principal Product Manager)

Mark defined the four product delivery surfaces, their H2 priority capability areas, the skills Matt needs, and file authority. Key points:

- **H2 priority capabilities (within web app surface):** Skeleton Generator UI, onboarding and SSO gate, quota-exhaustion and conversion nudges.
- **Post-launch capability (web app surface):** Pre-Review annotation UI (highest-complexity surface).
- **Cross-cutting (email agent surface):** Impact communication surfaces.
- **Exclusions:** Settings/admin, marketing website, API docs.
- **Interaction mode:** Collaboration. Matt is downstream of PRDs (Mark's output), upstream of engineering (speckit).

### John's Input (Head of Marketing)

John defined the marketing-product boundary and interaction modes. Key points:

- **Collaboration surfaces:** Landing pages, pricing page, onboarding, impact summaries.
- **X-as-a-Service:** Email templates, blog page template (Matt designs, John commissions).
- **Autonomous surfaces:** In-app product UI (John retains micro-copy review rights).
- **Anti-patterns to encode:** Marketing/product visual disconnect, gating information behind clicks, chatbot popups, stock hard-hat photos.
- **Patterns to encode:** Show the output not the feature, institutional trust signals, dense information hierarchy.
- **Persona caveat:** P-029 (personas not yet validated) means Matt should treat all layout decisions as draft until personas are canonical.
- **Notebook access request:** Product Design & UX (direct read), Digital Marketing & Social Selling (scoped read via John).

### Graeme (not directly consulted)

Graeme was not invoked directly in this session, but the JD encodes a mandatory handoff to Graeme for domain terminology review on every design that touches geotechnical concepts. This is consistent with the established handoff chain.

## Step 3 — Career-Ladder Style JD

The full JD is in `.github/agents/rl.matt.agent.md`.

Design choices applied:

- **Outcomes, not task lists.** Responsibilities are framed as outcomes Matt is accountable for, not a fixed list of design deliverables (per Jesuthasan & Boudreau's warning against rigid JDs that trap work in a title).
- **Testable hard constraints.** Every constraint uses "MUST" or "MUST NOT" with a concrete boundary (per prompt rewriting rules).
- **Crisp boundaries.** The JD explicitly states what Matt does not do, matching the Larson career-ladder pattern.
- **Team API published.** Inputs, outputs, interaction modes, handoff partners all declared.
- **Draft-first maturity.** Matt starts in Draft-first mode (writes to `docs/product/design/drafts/` first, promoted to `docs/product/design/` after user approval).

## Step 4 — Team API and File Authority Check

### Matt's File Authority

| Path | Mode |
|---|---|
| `docs/product/design/` | Write (new directory, Matt is sole owner) |
| `specs/` | Read |
| `docs/product/` | Read (except `design/`, where Matt has write) |
| `docs/knowledge/geotechnical/` | Read |
| `docs/research/` | Read |

### Overlap Check

| Existing Agent | Their Write Authority | Overlap with Matt? |
|---|---|---|
| Ron | `docs/product/strategy/`, `docs/research/`, `specs/` | No — Matt reads these, does not write to them |
| Mark | `docs/product/`, `specs/`, `docs/research/` | Mark writes to `prds/`, `problems/`, `hypotheses/`, `decisions/`, `operations/`, `personas/`. Matt writes to `design/` (new subdirectory). No overlap. |
| John | `docs/product/marketing/` | No — `marketing/` and `design/` are disjoint directories |
| Graeme | `docs/knowledge/geotechnical/` | No — Matt reads only |
| Harriet | `docs/people/` | No overlap |

**File Authority verdict:** No overlaps detected. Step 4 passes.

## Step 5 — Skill Gap Check

### Skills Matt Would Use (Existing)

| Skill | Status | Notes |
|---|---|---|
| `notebooklm-mcp` | Exists | Matt queries notebooks for design grounding |
| `miro-mcp` | Exists | Matt renders wireframes and user flows on Miro |
| `pm-personas` | Exists | Matt reads persona definitions (does not author them) |
| `pm-structural-integrity-auditor` | Exists | Matt can `/challenge` his own designs |

### Skills Matt Needs (Missing)

| Proposed Skill Name | Domain | Grounding Source | Status |
|---|---|---|---|
| `ux-professional-software` | Information-dense UI design for professional/technical software, document-centric interaction patterns, annotation overlays | `Product Design & UX` notebook (Norman, Krug, Designing with Data, Forms that Work) + `Information Architecture and Knowledge Management` notebook | **Gap — needs creation** |
| `ux-conversion-design` | Conversion UX for warm-handoff B2B SaaS (quota exhaustion nudges, SSO gate design, pricing page layout, onboarding friction reduction) | `Product Design & UX` notebook + `Monetizing & Scaling Innovation` notebook (route through John for advisory-board notebook) + `Digital Marketing & Social Selling` (route through John) | **Gap — needs creation** |

### Skills Taxonomy Gap Entry (Existing)

The skills taxonomy already records a related gap: "UX for technical professional software" with proposed remediation to install `frontend-design` from `anthropics/skills` and commission `rl-ux-for-engineers` from the `Product Design & UX` notebook. I am refining this into the two concrete skills above, which are agent-agnostic (no personal names).

### Recommended Actions

1. **`ux-professional-software`**: Query the `Product Design & UX` notebook and the `Information Architecture and Knowledge Management` notebook to draft this skill using the `writing-skills` TDD cycle. No additional sourcing needed — notebooks are already loaded with relevant content.
2. **`ux-conversion-design`**: Route through John to query `Monetizing & Scaling Innovation` and `Digital Marketing & Social Selling` for conversion UX principles. Combine with `Product Design & UX` notebook for the interaction design layer. Then draft using `writing-skills` TDD cycle.
3. **Accessibility and geo-localisation awareness**: Not a standalone skill. Encode as a JD constraint for now. If the domain grows complex enough to warrant a skill, revisit. A resource for future grounding: W3C WCAG 2.2 guidelines (freely available, current, stack-agnostic).

## Step 6 — Notebook Check

### Notebooks Matt Needs

| Notebook | Exists in `register.json`? | Access Level | Matt's Access |
|---|---|---|---|
| Product Design & UX | Yes | Open | Direct query |
| Information Architecture and Knowledge Management | Yes | Open | Direct query |
| Digital Marketing & Social Selling | Yes | Advisory-board-only | Route through John (scoped read) |
| Monetizing & Scaling Innovation | Yes | Advisory-board-only | Route through John (for conversion UX grounding only) |

### Missing Notebooks

None. All required notebooks are loaded. The two advisory-board-only notebooks are accessible through John as the established routing pattern.

## Step 7 — Summary and Next Actions

### Deliverables Produced

1. **This hire report** — `docs/people/drafts/reports/hire-ux-designer-2026-04-20.md`
2. **Production JD** — `.github/agents/rl.matt.agent.md`

### Updates Required (pending user approval)

1. **`docs/people/agent-register.md`** — Add Matt's row.
2. **`docs/people/org-chart.md`** — Add Matt to the org structure.
3. **`docs/people/skills-taxonomy.md`** — Add UX/Design skill category with the two proposed skills; update gap log.

### Open Items

| Item | Owner | Action |
|---|---|---|
| Approve the hire and promote JD to `.github/agents/rl.matt.agent.md` | User | Review this report, then instruct Harriet to promote |
| Create `docs/product/design/` directory | Engineering | After JD promotion |
| Draft `ux-professional-software` skill | Harriet | Query `Product Design & UX` and `Information Architecture and Knowledge Management` notebooks, then apply `writing-skills` TDD cycle |
| Draft `ux-conversion-design` skill | Harriet (with John) | Route through John for advisory-board notebook queries, then apply `writing-skills` TDD cycle |
| Validate personas (P-029) | Mark | Until personas are canonical, Matt treats all layout decisions as draft |

### Framework Citations

| Decision | Framework | Citation |
|---|---|---|
| Step 0 screening (four "do not hire" patterns) | Team Topologies (Skeleton & Pais) | Chapter on team-first boundaries; "do not create a new team" anti-patterns |
| Step 1 work deconstruction (elemental tasks, three continuums, ROIP) | Work Without Jobs / Reinventing Jobs (Jesuthasan & Boudreau) | Four-step work-deconstruction framework |
| Step 3 JD design (outcomes not tasks, crisp boundaries) | An Elegant Puzzle (Larson) | Career-ladder design; gap-less ownership map |
| Step 4 Team API (inputs, outputs, interaction modes) | Team Topologies (Skeleton & Pais) | Team API pattern; three interaction modes |
| File Authority overlap check | An Elegant Puzzle (Larson) | Gap-less ownership map — every responsibility maps to exactly one agent |
| Skill naming (agent-agnostic, no personal names) | `hiring-agent-management` skill | Skill Naming Rules section |
