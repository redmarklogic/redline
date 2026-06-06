# Agent Topology Sync Report

**Date:** 2026-06-07
**Previous sync:** 2026-06-06 (pre-hire screen)
**Trigger:** Full re-run requested by founder on branch `feature/47-onboarding-brent-devops-lead` (DevOps/GCP "Brent" onboarding intent). Founder also promoted Harriet to **Autonomous** this session.
**Facilitating agent:** Harriet (Head of People & Agent Development)
**Mode:** Full ceremony re-run. Brent remains a **draft proposal** — the onboarding branch signals hire intent but the hire is **not yet approved**. No Brent-contingent JD patch is promoted by this sync.

> **Correction (2026-06-07, post-publication):** The Harriet → Autonomous promotion described throughout this report was **reverted to Draft-first the same day at founder request.** Harriet's current maturity is **Draft-first**. The BOM dispatch fix (§3) stands — it was completed under the temporary Autonomous grant. Consequently the notes in §7 and §11 stating "Harriet can promote patches directly" **no longer apply**: patch and JD promotion revert to the Draft-first flow — Harriet stages in `docs/people/drafts/`, the founder promotes to `.claude/agents/`.

> **Disclosure — Reflection Protocol conducted in absentia (again, this session).** The named personas (Peter, Kabilan, Linda, etc.) are still not dispatchable as Claude Code subagents *in this running session*: the subagent registry loads at session start, and at this session's start all nine JDs still carried a UTF-8 BOM (Byte Order Mark) that breaks frontmatter parsing. This sync **fixed that blocker** (BOMs stripped — see §3), but the fix only takes effect after a **session restart**. Delta Statements below are therefore synthesised from each agent's live JD, not from a live consult. **The next sync can run live reflections.** Step R3 (online currency check) was not run this session.

---

## 1. Session Summary

Three facts define this sync:

1. **Nothing in the repository changed since the 2026-06-06 sync.** No new commits, ADRs (Architecture Decision Records), specs, or strategy documents. Git HEAD is unchanged. The 2026-06-06 working-tree changes (JD tools-format conversion + People-artifact updates) remain **uncommitted**.

2. **An onboarding branch now exists** — `feature/47-onboarding-brent-devops-lead`. This signals the founder's intent to hire Brent (DevOps Engineer, GCP), but the hire is not yet formally approved and Brent's JD is still a draft at `docs/people/drafts/agents/brent.agent.md`. The three contingent JD patches (Kabilan, Peter, Linda) from 2026-06-06 remain staged.

3. **The dispatch blocker was resolved this session.** All nine live JDs in `.claude/agents/` carried a UTF-8 BOM that prevented them registering as Claude Code subagents — the root cause of every "in absentia" reflection. Harriet was promoted to Autonomous and stripped the BOMs (§3). Effective next session restart, named agents become dispatchable.

**Net new value vs. the 2026-06-06 report:** the topology is now *coherent on the dispatch axis* (agents loadable) and Harriet is Autonomous. The Brent gap/overlap/orphan analysis is **unchanged** from 2026-06-06 because no underlying repo state changed — it is restated below for completeness, not re-derived.

---

## 2. Trigger Validation

| Trigger criterion | Met? | Evidence |
|---|---|---|
| Quarterly cadence (90 days) | No | 1 day since 2026-06-06 |
| New agent hired **and onboarded** | No | Brent draft; hire not approved; not onboarded |
| New agent **onboarding initiated** | **Partial** | Branch `feature/47-onboarding-brent-devops-lead` open; hire decision pending |
| Major strategy pivot | No | No new bet (strategic-bets.md unchanged) |
| Significant topology change | **Yes** | (a) Harriet promoted to Autonomous; (b) dispatch blocker resolved across all nine JDs |
| Founder explicitly requested a re-run | **Yes** | This session |

**Verdict:** Valid. Driven by the founder's explicit re-run request and two real topology changes (Harriet promotion, dispatch-blocker fix). The Brent hire trigger is *pending*, not met.

---

## 3. Dispatch Blocker — RESOLVED This Session [OK]

**Problem:** All nine live JDs (`graeme, harriet, john, kabilan, linda, mark, matt, peter, ron`) carried a UTF-8 BOM at byte 0. The Claude Code subagent loader does not tolerate a BOM before the frontmatter `---`, so none of the named personas resolved as dispatchable subagents — every Reflection Protocol since the schema migration has run in absentia as a result. The tools-format conversion (YAML list → comma-separated string) done 2026-06-04 was also still uncommitted.

**Action taken (Harriet, now Autonomous):** Stripped the three BOM bytes (`EF BB BF`) from all nine JDs via a byte-level rewrite. No other content changed; line endings preserved.

**Status after fix:**

| Item | State |
|---|---|
| BOM on 9 live JDs | Removed |
| Tools-format conversion (comma-separated) | Present in working tree (from 2026-06-04), still **uncommitted** |
| Brent draft frontmatter | Still old YAML-list `tools:` format — convert at hire time (it is a draft, not registered, so non-blocking) |
| Effect | Named agents dispatchable **after session restart** |

**Founder action required:** (1) restart the session to load the agents; (2) commit the JD conversion + BOM fix (Harriet does not commit without explicit instruction).

---

## 4. Drift Summary (per agent) — unchanged from 2026-06-06

| Agent | Drift | Note |
|---|---|---|
| Ron | None | No Brent contact by design; `tool-selection` added |
| Mark | None | No Brent contact by design; `tool-selection` added |
| John | None | No Brent contact by design; `tool-selection` added |
| Graeme | None | Geotechnical domain; not a cloud-source triager (see §6 orphan) |
| Matt | None | No Brent contact by design |
| **Peter** | **Yes (omission)** | Brent escalates Tier-1 GCP + Cloud SQL ADR to Peter; Peter's JD does not reference Brent. Contingent patch staged. |
| **Kabilan** | **Yes (omission + overlap)** | Brent defines env-var/OAuth handoffs into Kabilan; Kabilan's JD does not reference Brent and still claims "infrastructure" in scope. Contingent patch staged. |
| **Linda** | **Yes (omission + orphan)** | Two new notebooks land in Linda's register; no reciprocal flow; cloud-source currency has no triager. Contingent patch staged. |
| **Harriet** | **Updated this sync** | Promoted to Autonomous; JD maturity + Draft-first constraint amended; register row updated. |

---

## 5. Gap & Overlap Analysis (restated — no change in underlying state)

### 5.1 File Authority — clean
Brent's claimed paths (`infra/`, `.github/workflows/`, `.env.example`, `docs/infrastructure/`) do not overlap any existing JD. Kabilan (`src/rl/`, `tests/`, `scripts/`, `hooks/`, `output/`) and Peter (`docs/adr/`, `docs/architecture/`, `docs/evaluation/`, `specs/shaped/`) do not touch these. Brent reads `src/rl/settings.py` read-only — correct.

### 5.2 [BLOCKING] — internal contradiction in Brent's draft

Brent Outcome 4b requires a Cloud SQL connection-strategy **ADR to be written**; Brent's File Authority lists `docs/adr/` as **Read-only**. Brent cannot author it. **Resolution:** Peter authors the ADR from Brent's connection-strategy analysis (written to `docs/infrastructure/`). Peter's contingent patch encodes this. Brent's Outcome 4b must be reworded at hire time from "An ADR is written" to "Brent delivers the connection-strategy analysis to Peter, who authors the ADR." **Still uncorrected in the draft** (correct at hire).

### 5.3 [OVERLAP] — "infrastructure" scope, Kabilan vs. Brent

Kabilan's description/scope claims "infrastructure" and exempts "infrastructure changes" from PRD review. **Resolution:** split the term — Kabilan = application-level infra (Python code in `src/rl/`/`scripts/`); Brent = cloud & deployment infra (GCP provisioning, CI/CD config, `.env.example`, runtime config). Kabilan's contingent patch encodes this.

### 5.4 [BLOCKING] Orphan handoffs — unreciprocated edges

Brent's Team API defines flows into Kabilan, Peter, and Founder; none reciprocate. Contingent patches (§7) reciprocate Kabilan, Peter, Linda.

### 5.5 [BLOCKING] Orphan responsibility — cloud/DevOps source-currency triage

Linda routes domain source-currency triage to Graeme (geotechnical only). Cloud/DevOps/SOC-2 source currency for the two new GCP notebooks has **no triager**. **Resolution:** on hire, Brent triages cloud/DevOps source currency (analogous to Graeme for geotechnical), via Linda's existing detect-and-route mechanism. **Until hire, this responsibility is unowned** — the strategic justification for the hire (§8).

### 5.6 Team API friction — notebook metadata accuracy

The "GCP DevOps Tactical Playbook" register draft carries `"use cases to be confirmed"` and a DRAFT description. Linda's hard constraint requires accurate register metadata — **do not promote into `register.json` until content and use-cases confirmed.** The 8-book "DevOps & GCP Infrastructure" notebook draft is complete and promotable.

---

## 6. Strategic Grounding for the Brent Hire

Re-confirmed against `docs/product/strategy/strategic-bets.md` (unchanged since 2026-06-06):

- **Bet 1 (Free Skeleton Wedge):** requires an SSO-gated Skeleton Generator deployed on GCP Cloud Run. Cloud deployment + OAuth/IAP wiring is Brent's domain. The org chart marks this hire as "blocks Skeleton Generator deploy."
- **Bet 2 / Bet 4 (Pre-Review paid product / Switzerland-neutral positioning):** both depend on surviving enterprise IT review and on an audit trail; SOC 2 technical controls (encryption, audit sink, IAM least-privilege) are Brent's domain.

The cloud/DevOps execution + source-currency responsibility cannot be absorbed by any existing agent (Kabilan writes no infra config; Peter does not execute; Linda makes no domain judgments; Graeme is geotechnical-only). The hire is strategy-justified and the orphan is real.

---

## 7. Contingent JD Patches (CONTINGENT — not promoted; await Brent hire approval)

| Patch | Path | Addresses |
|---|---|---|
| Kabilan | `docs/people/drafts/agents/kabilan.agent-patch.md` | Brent handoff row; infra-scope split (§5.3); env-var + OAuth boundary |
| Peter | `docs/people/drafts/agents/peter.agent-patch.md` | Brent Tier-1 GCP approval gate; Cloud SQL ADR authorship (§5.2) |
| Linda | `docs/people/drafts/agents/linda.agent-patch.md` | Two new notebooks; tactical-playbook accuracy hold; cloud-source-currency routing gap (§5.5) |

> Brent's own JD remains a screen-only proposal. Its Outcome 4b contradiction (§5.2) is logged for correction at hire time. **Now that Harriet is Autonomous, on hire approval Harriet can promote these patches and Brent's JD directly into `.claude/agents/` — no separate draft-promotion step needed.**

---

## 8. New Hire Trigger

**One.** The cloud/DevOps execution + source-currency responsibility (§5.5) is orphaned and unabsorbable by any existing agent. **This is the strategic justification for the Brent hire.** The onboarding branch indicates founder intent; the formal hire decision is still pending.

---

## 9. People Artifact Updates (this session)

| Artifact | Change |
|---|---|
| `agent-register.md` | Harriet row → **Autonomous** (file authority + maturity); added 2026-06-07 sync note; date updated |
| `org-chart.md` | Open Headcount row updated (onboarding branch open, hire pending, 3 contingent patches noted); date updated |
| `skills-taxonomy.md` | Date updated (content already carries `tool-selection` + 12 GCP/DevOps gaps from 2026-06-06) |
| `.claude/agents/harriet.md` | Maturity → Autonomous; Draft-first constraint relaxed; promotion actions recorded |
| `.claude/agents/*.md` (all 9) | UTF-8 BOM stripped (dispatch fix) |

---

## 10. User Approvals / Actions Required

| Item | Action | Owner |
|---|---|---|
| Session restart | Restart to load now-dispatchable agents | User |
| Commit | Commit JD conversion + BOM fix + People-artifact updates (Harriet does not commit unprompted) | User |
| Brent hire decision | Approve / defer / reject the DevOps/GCP role | User |
| ADR-authorship resolution (§5.2) | Confirm Peter authors Cloud SQL ADR from Brent input | User + Peter |
| Infra-scope split (§5.3) | Confirm Kabilan = app-infra, Brent = cloud-infra | User + Kabilan |
| Contingent JD patches (§7) | Approve for promotion **if** Brent hired (Harriet can now promote directly) | User |
| Notebook intake (§5.6) | Approve "DevOps & GCP Infrastructure"; hold tactical-playbook | User + Linda |
| Housekeeping deletions (carried from 2026-06-06 §8) | Confirm stale draft skills + `tool-selection` duplicate can be deleted | User |

---

## 11. Next Sync Eligibility

| Trigger | Earliest date |
|---|---|
| Quarterly cadence | 2026-08-22 (90 days from 2026-05-23 baseline) |
| New hire onboarded | On Brent hire approval + onboarding |
| Major product milestone | On Skeleton Generator ship (target 2026-06-30) |

**Next action:** User decides on the Brent hire (§8, §10) and restarts + commits to lock in the dispatch fix. If Brent is approved, Harriet (now Autonomous) promotes the three contingent patches and Brent's JD directly into `.claude/agents/`, correcting Outcome 4b in the process. The first sync after restart can run the Reflection Protocol **live** for the first time.
