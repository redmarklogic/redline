# Agent Topology Sync Report

**Date:** 2026-05-23
**Previous sync:** 2026-05-17
**Trigger:** New agent hired and onboarded — Kabilan (Python Developer, 2026-05-22)
**Facilitating agent:** Harriet (Head of People & Agent Development)
**Participants:** All nine advisory/execution agents — Delta Statements compiled from repo artifact review (Steps R1–R3 in absentia; Step R4 synthesised from hire report evidence)

---

## 1. Session Summary

This sync was triggered six days after the May 17 DDD topology sync by Kabilan's hire and
onboarding on 2026-05-22. The scope is narrow: verify that all agent JDs are coherent
following the addition of a dedicated engineering execution agent, confirm that all May 17
skill patches were promoted, log new skill gaps surfaced during the hire consultation, and
flag stale draft files for cleanup.

**Key finding:** The topology is clean. All agent JDs were updated as part of the 2026-05-22
hire process. All May 17 DDD skill patches were promoted to live skill files before this sync.
No JD patches are needed from this session.

---

## 2. Trigger Validation

| Trigger criterion | Met? | Evidence |
|---|---|---|
| Quarterly cadence (90 days elapsed) | No | 6 days since last sync |
| New agent hired and onboarded | **Yes** | Kabilan hire approved and promoted 2026-05-22 |
| Major strategy pivot approved | No | No new bets; strategic-bets.md last updated 2026-05-09 |
| Significant product milestone shipped | No | No launch event since May 17 |
| Significant batch of client feedback | No | Pre-launch phase |

**Verdict:** Valid trigger.

---

## 3. Reflection Protocol — Delta Statements (Step R4)

> **Note:** Steps R1–R3 were conducted against repo artifacts (agent JDs, hire report, skill
> files, agent register). Online currency checks (Step R3) surfaced no framework changes
> affecting agent JDs within the 6-day window.

### Ron — Strategy & GTM Advisor

- **What I own today:** Strategic bets, OKRs, positioning, GTM motion. Proactive briefings to John and Peter.
- **What changed since May 17:** Kabilan hired. Ron has zero contact with Kabilan per the hire decision.
- **JD or skill drift:** None. Ron's JD does not reference Kabilan, which is correct.
- **Frameworks needing update:** None.
- **Delta: No drift.**

### Mark — Principal Product Manager

- **What I own today:** Problem statements, hypotheses, PRDs, decision logs.
- **What changed since May 17:** Kabilan hired. Mark's routing section already states "Mark does not hand off directly to Kabilan; work flows through Peter's shaping and SpecKit's task generation." This was present in the JD before this sync.
- **JD or skill drift:** None.
- **Delta: No drift.**

### Graeme — Principal Geotechnical Engineer

- **What I own today:** Domain knowledge documents, fact-checks, evaluation rubric domain content, three blocking gates (assertion sign-off, fixture sign-off, LLM explanation accuracy).
- **What changed since May 17:** Kabilan hired. Graeme's Team API already specifies "Kabilan's domain questions route through Peter; Graeme does not interact with Kabilan directly."
- **JD or skill drift:** None.
- **Delta: No drift.**

### John — Head of Marketing

- **What I own today:** Content marketing, SEO, social selling, monthly signal report, campaign briefs.
- **What changed since May 17:** Kabilan hired. Zero contact with Kabilan per hire decision.
- **JD or skill drift:** None.
- **Delta: No drift.**

### Peter — Principal Engineer

- **What I own today:** Architecture decisions, evaluation design, shaping, UL stewardship, EventStorming, model evolution governance, quality gate governance, improvement loop.
- **What changed since May 17:**
  - DDD responsibilities (UL stewardship, EventStorming, model evolution governance) added to JD — all confirmed live in `.github/agents/rl.peter.agent.md`.
  - Kabilan Team API row added: Kabilan escalates architectural boundary questions to Peter; Peter provides decisions.
  - Three skill extension requests raised during Kabilan hire consultation (see Skill Gap Triggers below).
- **JD or skill drift:** None. All May 17 patches and Kabilan row are live.
- **Delta: No drift. Skill gap triggers outstanding (see Section 6).**

### Matt — UI/UX Designer

- **What I own today:** Design specs, wireframes, component inventories, user flows across four surfaces.
- **What changed since May 17:** Kabilan hired. Matt's Team API already specifies "Interaction mode with Kabilan | X-as-a-Service. Kabilan consults Matt's design specs before implementing any user-facing component. If a spec is missing, Kabilan asks Matt before proceeding."
- **JD or skill drift:** None.
- **Delta: No drift.**

### Linda — Knowledge Infrastructure Operator

- **What I own today:** Digital library, NotebookLM notebook maintenance, register.json, standards monitoring.
- **What changed since May 17:** Kabilan hired. Linda has no interaction with Kabilan.
- **JD or skill drift:** None.
- **Delta: No drift.**

### Harriet — Head of People & Agent Development

- **What I own today:** Hiring, audits, PIPs, agent register, org chart, skills taxonomy, topology syncs.
- **What changed since May 17:** Kabilan hired. Agent register, org chart, and skills taxonomy updated 2026-05-22. `ceremony-agent-topology-sync` skill live and registered.
- **JD or skill drift:** None. Skills table already includes `ceremony-agent-topology-sync`.
- **Delta: No drift.**

### Kabilan — Python Developer (Senior Software Engineer) *(new agent)*

- **What I own today:** Full-stack Python engineering — implementation, testing, debugging, data pipelines, scripts, infrastructure. No push to origin without founder instruction. Founder reviews all code.
- **What changed since May 17:** N/A (new agent).
- **JD currency:** JD created 2026-05-22 and immediately promoted to `.github/agents/rl.kabilan.agent.md`.
- **Skill base:** 39 Python/engineering skills, loaded on demand.
- **Delta: Current (new agent). Three skill extensions outstanding — see Section 6.**

---

## 4. Gap and Overlap Analysis

### 4.1 Orphan Responsibilities

| Responsibility | Status |
|---|---|
| Python engineering implementation | Assigned → Kabilan |
| Architectural escalation from engineering | Assigned → Peter |
| Design spec consumption by engineering | Assigned → Kabilan (reads Matt's specs) |
| Domain accuracy of test fixtures | Assigned → Graeme (blocking gate) |
| Static check execution (ruff, mypy, deptry) | Covered by `python-static-checks` skill, Kabilan owns execution |

**No orphan responsibilities found.**

### 4.2 Overlaps

| Potential overlap | Assessment |
|---|---|
| SpecKit.implement vs Kabilan | No overlap. SpecKit generates structured task plans; Kabilan is a chat-session engineering agent consuming those plans or acting on direct founder requests. They are parallel workflows, not competing. |
| Peter (architectural decisions) vs Kabilan (implementation) | No overlap. Escalation protocol is explicit: Kabilan escalates, Peter decides. |
| Matt (design specs) vs Kabilan (implementation) | No overlap. Matt produces, Kabilan consumes. Collaboration only when a spec is missing. |

**No overlaps found.**

### 4.3 Team API Friction

| Potential friction | Assessment |
|---|---|
| Kabilan's `agents: []` in JD frontmatter | Correct. Kabilan escalates to Peter via the chat interface, not via agent handoff. No change needed. |
| Kabilan cannot write to `.agents/skills/` | Correct by design. Skill updates route through Peter (identification) → Harriet (drafting) → founder (approval and promotion). |

**No Team API friction found.**

---

## 5. Stale Draft Cleanup Flags

The following draft files have been promoted to production and are now stale. They should
be cleaned up at the user's discretion.

| Draft file | Promoted artifact | Promotion status |
|---|---|---|
| `docs/people/drafts/agents/rl.peter.agent-patch.md` | `.github/agents/rl.peter.agent.md` | Confirmed live (UL stewardship, EventStorming, model evolution governance all present) |
| `docs/people/drafts/agents/rl.kabilan.agent.md` | `.github/agents/rl.kabilan.agent.md` | Confirmed live |
| `docs/people/drafts/skills/ddd-strategic/` | `.agents/skills/ddd-strategic/SKILL.md` + `procedures/` | Confirmed live |
| `docs/people/drafts/skills/engineering-architecture-patch.md` | `.agents/skills/engineering-architecture/SKILL.md` | Confirmed live (Strategic DDD cross-reference present) |
| `docs/people/drafts/skills/python-domain-modeling-patch.md` | `.agents/skills/python-domain-modeling/SKILL.md` | Confirmed live ("Language change = code refactor" rule present) |
| `docs/people/drafts/skills/miro-mcp-patch.md` | `.agents/skills/miro-mcp/SKILL.md` | Confirmed live (`board_create` and new tools present) |

> **Note:** The drafts in `docs/people/drafts/` should be deleted or archived after user review. Retaining them creates a false signal that promotion is still pending.

---

## 6. Skill Gap Triggers (New — from Kabilan Hire Consultation)

Three skill extensions were identified by Peter during the 2026-05-22 hire consultation.
These are outstanding and must be added to `skills-taxonomy.md` → Skills Coverage Gaps.

| Gap | Identified by | Skill to extend | Proposed content | Owner |
|---|---|---|---|---|
| Dependency management guidance | Peter (2026-05-22 hire consultation) | `dev-environment` | How to add, remove, and audit dependencies via `uv add` / `uv remove`; `pyproject.toml` dependency declarations; when to escalate to Peter | Peter (identifies content) → Harriet (drafts) |
| Layer architecture explanation | Peter (2026-05-22 hire consultation) | `python-domain-modeling` | Visual reference for Redline's layer architecture (`domain/`, `functions/`, `api/`); what belongs in each layer; prohibited imports across layers; escalation triggers when a layer change is needed | Peter (identifies content) → Harriet (drafts) |
| PR discipline thresholds | Peter (2026-05-22 hire consultation) | `version-control` | Maximum PR size (lines/files); what constitutes "one logical change"; when to split a PR; how to detect oversized PRs via SonarQube/Copilot; author-side AI feedback window | Peter (identifies content) → Harriet (drafts) |

> **Note:** These are extensions to existing live skills. No new skill files are needed.
> Harriet will draft the extension patches after Peter provides content.

---

## 7. JD Patches Produced

**None.** All agent JDs are current. No patches were drafted in this session.

---

## 8. People Artifact Status

| Artifact | Last updated | Status |
|---|---|---|
| `docs/people/agent-register.md` | 2026-05-22 | Current — Kabilan added |
| `docs/people/org-chart.md` | 2026-05-22 | Current — Kabilan added |
| `docs/people/skills-taxonomy.md` | 2026-05-22 | Requires update: add 3 new skill gaps (Section 6) |

---

## 9. New Hire Triggers

None. All responsibilities map to existing agents.

---

## 10. User Approvals Required

| Item | Action required | Owner |
|---|---|---|
| Stale draft cleanup | Confirm drafts in `docs/people/drafts/agents/` and `docs/people/drafts/skills/` can be deleted | User |
| Skill gap logging | Approve additions to `skills-taxonomy.md` → Skills Coverage Gaps (Section 6) | User (then Harriet applies) |
| Skill extension patches | After Peter provides content, Harriet will draft patches. User approves before promotion to `.agents/skills/` | User (future session) |

---

## 11. Next Sync Eligibility

| Trigger | Earliest date |
|---|---|
| Quarterly cadence | 2026-08-22 (90 days from 2026-05-23) |
| New hire | On onboarding of next agent |
| Strategy pivot | On approval of a new or substantially revised strategic bet |
| Major product milestone | On launch of Skeleton Generator (target: 2026-06-30) or other significant ship event |
| Significant client feedback batch | On processing of first co-development partner feedback batch (Phase 1) |

> **Recommendation:** The next scheduled trigger after today is the Skeleton Generator
> launch (target 2026-06-30). That milestone qualifies as a significant product milestone
> and should initiate the next topology sync within one week of ship.
