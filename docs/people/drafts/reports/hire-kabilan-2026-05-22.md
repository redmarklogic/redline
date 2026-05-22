# Hire Report: Kabilan — Python Developer (Senior Software Engineer)

**Date:** 2026-05-22
**Drafted by:** Harriet (Head of People & Agent Development)
**Status:** Draft — awaiting founder approval

---

## Step 0 — "When NOT to hire" Screening

| Screen | Result | Reasoning |
|---|---|---|
| Expansion-first (Parsimony) | PASS | Nearest agent is `speckit.implement` — vendor-managed, cannot expand. 39 Python skills exist with no assigned agent. |
| Reactive / ad-hoc | PASS | Not a response to failure. Filling a structural vacancy in the handoff chain. |
| Single-function silo | PASS | Full-stack Python engineering is broad, not a narrow slice. |
| Cognitive-load justification | PASS | Founder holds strategy + product + domain + marketing + architecture + design + people + knowledge + ALL coding. Engineering is the largest cognitive load bucket by volume. |
| Active strategic bet | PASS | Bet 1 (Skeleton Generator), Bet 2 (Pre-Review), Bet 3 (Standards Knowledge Store) all require Python engineering. |

**Verdict: PASS.**

---

## Step 1 — Task Deconstruction

| Task | Rep/Var | Ind/Int | Det/Judg | ROIP | Disposition |
|---|---|---|---|---|---|
| Implement features from SpecKit tasks | Variable | Interactive | Judgment | Exponential | Substitute |
| Write and maintain unit/API tests | Repetitive | Independent | Mixed | Reduce mistakes | Substitute |
| Debug failing tests and runtime errors | Variable | Independent | Judgment | Reduce mistakes | Substitute |
| Write data ingestion pipelines | Variable | Interactive | Mixed | Incremental | Substitute |
| Write and maintain scripts | Variable | Independent | Mixed | Incremental | Substitute |
| Create/update FastAPI endpoints | Variable | Interactive | Judgment | Exponential | Substitute |
| Refactor and maintain `src/rl/` | Variable | Independent | Judgment | Incremental | Substitute |
| Ad-hoc engineering outside SpecKit | Variable | Interactive | Judgment | Varies | Substitute |
| Run static checks | Repetitive | Independent | Deterministic | Reduce variance | Skill (exists) |
| Manage dev environment | Repetitive | Independent | Deterministic | Reduce variance | Skill (exists) |
| Commit code | Repetitive | Independent | Low judgment | Reduce variance | Skill (exists) |

---

## Step 2 — Advisory Board Consultation Summary

All six agents consulted. Full transcripts in the chat session dated 2026-05-22.

### Interaction Map

| Agent | Interaction with Kabilan | Mode |
|---|---|---|
| Ron | Zero contact. Fully shielded by Peter and Mark. | None |
| Mark | X-as-a-Service. Kabilan reads PRDs for context. | On-demand |
| Graeme | Indirect only. Kabilan reads knowledge store. Domain ambiguity routes through Peter. Graeme reviews domain test fixtures (blocking gate). | Mediated by Peter |
| John | Zero contact. Matt's gate covers user-facing copy. | None |
| Peter | X-as-a-Service. Kabilan reads ADRs + Pitches. Escalates architectural boundary crossings. Peter does Touch 2 at PR review. | Structured escalation |
| Matt | Closest partner. Kabilan reads design specs before user-facing work. Matt reviews before user-facing features ship. | Collaboration |

### Constraints Raised by the Team (all incorporated in JD)

15 hard constraints from the team + 2 founder requirements (no push to origin, founder reviews all code). See agent file for full list.

### Skill Gaps Identified by Peter (minor — no new skill files)

| Gap | Proposed fix | Owner |
|---|---|---|
| Dependency management guidance | Extend `dev-environment` skill | Peter |
| Layer architecture explanation | Extend `python-domain-modeling` skill | Peter |
| PR discipline thresholds | Extend `version-control` skill | Peter |

---

## Step 3-4 — Agent Design

| Field | Value |
|---|---|
| **Agent name** | `kabilan` |
| **Role** | Python Developer (Senior Software Engineer) |
| **Domain** | Full-stack Python engineering |
| **File Authority (write)** | `src/rl/`, `tests/`, `scripts/` (modify only), `hooks/` (bug fixes only), `output/` |
| **File Authority (read)** | `docs/adr/`, `docs/architecture/`, `docs/knowledge/geotechnical/`, `docs/product/prds/`, `docs/product/hypotheses/`, `docs/product/problems/`, `docs/product/design/`, `specs/` |
| **Explicit exclusions** | MUST NOT write to `docs/`, `specs/`, `.github/agents/`, `.agents/skills/` |
| **Maturity** | Autonomous (with mandatory founder code review and no-push-without-permission constraint) |
| **Skills** | 39 existing Python/engineering skills — loaded on demand |
| **New skills needed** | None (3 minor extensions to existing skills — Peter's responsibility) |
| **Notebooks** | None required |

### Founder Requirements (binding)

1. **No push to origin.** Kabilan MUST NOT push to remote under any circumstances unless the founder explicitly instructs it in the same session.
2. **Founder reviews all code.** All code Kabilan produces is subject to founder review before merge/push.

---

## Steps 5-6 — Skill and Notebook Gap Check

**Skills:** All 39 engineering skills exist. No new skills required. Three minor extensions identified (Peter will draft).

**Notebooks:** No new notebooks required. Engineering notebooks are accessible via Peter.

---

## Sunset Clause

Kabilan covers Python surfaces only. When a non-Python frontend surface is introduced (e.g., TypeScript/React), the role splits. This is a planned evolution, not a failure.

---

## Next Actions

| Action | Owner | Status |
|---|---|---|
| Approve this hire report and the agent file | Founder | Done (2026-05-22) |
| After approval: promote `rl.kabilan.agent.md` to `.github/agents/` | Founder | Done (2026-05-22) |
| After approval: update agent-register.md | Harriet | Done (2026-05-22) |
| After approval: update org-chart.md | Harriet | Done (2026-05-22) |
| After approval: update skills-taxonomy.md | Harriet | Done (2026-05-22) |
| Draft skill extensions (dependency mgmt, layer arch, PR discipline) | Peter | Done (2026-05-22) |

---

## Framework Citations

| Decision | Framework | Source |
|---|---|---|
| Step 0 screening | Team Topologies anti-patterns | Skelton & Pais |
| Task deconstruction | Four-step work-deconstruction | Jesuthasan & Boudreau |
| JD as outcomes not tasks | Work Without Jobs | Jesuthasan & Boudreau |
| Team API | Team Topologies | Skelton & Pais |
| Cognitive load justification | Team Topologies | Skelton & Pais |
| Maturity level | Career ladders | Larson |
