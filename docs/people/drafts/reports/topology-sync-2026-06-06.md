# Agent Topology Sync Report

**Date:** 2026-06-06
**Previous sync:** 2026-05-23
**Trigger:** Pre-hire topology screen — DevOps/GCP agent ("Brent") proposed as a draft; ADR-016 (CLI-first tool selection) accepted and `tool-selection` skill rolled across all nine JDs.
**Facilitating agent:** Harriet (Head of People & Agent Development)
**Mode:** Proposal-screen only. Brent is **not** an approved hire. No live JD is modified by this sync. All Brent-contingent patches are drafts requiring hire approval before promotion.

> **Disclosure — Reflection Protocol conducted in absentia.** The named personas (Peter, Kabilan, Linda) are not dispatchable as subagents in the current Claude Code harness (their JDs use the VS Code Copilot custom-agent schema; only built-in subagent types resolve). Delta Statements and reciprocal-boundary recommendations below were synthesised from each agent's live JD, not from a live consult. **Every reciprocal patch must be validated by the affected agent at Brent hire-approval time.** Step R3 (online currency check) was not run this session.

---

## 1. Session Summary

Two topology events since the 2026-05-23 sync:

1. **A DevOps/GCP role ("Brent") has been drafted** at `docs/people/drafts/agents/brent.agent.md`, with two supporting NotebookLM register drafts (`register-devops-gcp-infrastructure.json`, `register-devops-gcp-tactical-playbook.json`). This is a substantial new execution role: it claims four new File Authority paths, two new notebooks, and sixteen skills (twelve of them new and unwritten).

2. **ADR-016 (CLI-first tool selection) was accepted 2026-06-06.** A live `tool-selection` skill now exists at `.agents/skills/tool-selection/`, `AGENTS.md` carries a CLI-first directive, and all nine agent JDs received staged edits adding `tool-selection` routing plus tightening.

**Key finding:** Brent's draft is internally coherent on its own terms but **disconnected from the existing topology** — its handoffs into Kabilan, Peter, and Linda are one-directional and unreciprocated, it contains one blocking internal contradiction (ADR authorship vs. read-only `docs/adr/`), it surfaces a latent infra-scope overlap with Kabilan, and it exposes one genuine orphan responsibility (cloud/DevOps source-currency triage). The `tool-selection` rollout is clean but is not yet recorded in the skills taxonomy.

---

## 2. Trigger Validation

| Trigger criterion | Met? | Evidence |
|---|---|---|
| Quarterly cadence (90 days) | No | 14 days since 2026-05-23 |
| New agent hired **and onboarded** | No | Brent is a draft; not approved, not onboarded |
| New agent **proposed** (pre-hire screen) | **Yes** | `brent.agent.md` draft; `hiring-agent-management` mandates a sync *before* finalising any hire |
| Major strategy pivot | No | No new strategic bet |
| Significant product milestone | No | Skeleton Generator not yet shipped |
| Significant topology change | **Yes** | ADR-016 + `tool-selection` across all nine JDs |

**Verdict:** Valid. This is a pre-hire topology screen, not a post-onboarding sync.

---

## 3. Drift Summary (per agent)

| Agent | Drift | Note |
|---|---|---|
| Ron | None | No Brent contact by design; `tool-selection` added |
| Mark | None | No Brent contact by design; `tool-selection` added |
| John | None | No Brent contact by design; `tool-selection` added |
| Graeme | None | Geotechnical domain; not a cloud-source triager (see §5 orphan) |
| Matt | None | No Brent contact by design |
| **Peter** | **Yes (omission)** | Brent escalates Tier-1 GCP + Cloud SQL ADR to Peter; Peter's JD does not reference Brent |
| **Kabilan** | **Yes (omission + overlap)** | Brent defines env-var/OAuth handoffs into Kabilan; Kabilan's JD does not reference Brent and still claims "infrastructure" in scope |
| **Linda** | **Yes (omission + orphan)** | Two new notebooks land in Linda's register; no reciprocal flow; cloud-source currency has no triager |
| Harriet | None | `ceremony-agent-topology-sync` live; running it now |

---

## 4. Gap & Overlap Analysis

### 4.1 File Authority — clean

Brent's claimed paths — `infra/`, `.github/workflows/`, `.env.example`, `docs/infrastructure/` — were checked against every existing JD. **No path overlap.** Kabilan (`src/rl/`, `tests/`, `scripts/`, `hooks/`, `output/`) and Peter (`docs/adr/`, `docs/architecture/`, `docs/evaluation/`, `specs/shaped/`) do not touch these. Brent reads `src/rl/settings.py` read-only — correct.

### 4.2 [BLOCKING] — internal contradiction in Brent's draft

Brent Outcome 4b requires a Cloud SQL connection-strategy **ADR to be written**; Brent's File Authority lists `docs/adr/` as **Read-only**. Brent cannot author it.

**Resolution (recommended):** **Peter authors the ADR**, with Brent supplying the connection-strategy analysis (Auth Proxy vs. direct, pooling) as input written to `docs/infrastructure/`. This fits Peter's existing constraint to "request and incorporate views from relevant agents before finalizing a decision" and keeps the ADR namespace single-owner. Brent's Outcome 4b must be reworded from "An ADR is written" to "Brent delivers the connection-strategy analysis to Peter, who authors the ADR."

### 4.3 [OVERLAP] — "infrastructure" scope, Kabilan vs. Brent

Kabilan's `description` and scope claim "infrastructure," and his Feature-Scope constraint *exempts* "infrastructure changes" from PRD review. If Brent owns cloud/deployment infra, this is now ambiguous.

**Resolution (recommended):** split the term explicitly —
- **Kabilan = application-level infrastructure:** scripts, data pipelines, hooks, infrastructure expressed *as Python code* inside `src/rl/`/`scripts/`.
- **Brent = cloud & deployment infrastructure:** GCP provisioning, CI/CD pipeline config, `.env.example`, container/runtime config.

### 4.4 [BLOCKING] Orphan handoffs — unreciprocated edges

Brent's Team API defines flows **into** Kabilan, Peter, and Founder, but none of those JDs reciprocate. Until reciprocated, the handoffs are incomplete. Draft patches produced (§6) for Kabilan, Peter, Linda.

### 4.5 [BLOCKING] Orphan responsibility — cloud/DevOps source-currency triage

Linda detects standards/source updates but routes domain triage to **Graeme (geotechnical only)**. Cloud/DevOps/SOC-2 source currency for the two new notebooks has **no triager**.

**Resolution (recommended):** if Brent is hired, **Brent** triages cloud/DevOps source currency (analogous to Graeme for geotechnical), routed via Linda's existing detect-and-route mechanism. Until hire, this responsibility is **unowned** — flagged as a hire-justifying orphan.

### 4.6 Team API friction — notebook metadata accuracy

The "GCP DevOps Tactical Playbook" register draft carries `"use cases to be confirmed"` and a DRAFT description. Linda's hard constraint requires accurate register metadata. **This notebook must not be promoted into `register.json` until its content and use-cases are confirmed.** The 8-book "DevOps & GCP Infrastructure" notebook draft is complete and promotable.

---

## 5. Skill Gap Triggers

| Gap | Status | Remediation |
|---|---|---|
| `tool-selection` (CLI-first routing; ADR-016) | **Live, untracked** | Add to `skills-taxonomy.md` (done this sync). Stale duplicate at `docs/people/drafts/skills/tool-selection/` — flag for deletion. |
| 12 GCP/DevOps skills (Cloud Run, CI/CD, IAM, Cloud SQL, IAP/OAuth, observability, cost controls, container tuning, WIF, multi-tenancy, Secret Manager, infra-boundary-contract) | **None exist** | Contingent on Brent hire. Grounding source = "DevOps & GCP Infrastructure" notebook (8 books) + tactical-playbook notebook (content pending). Logged in coverage gaps. |

---

## 6. Draft JD Patches Produced (CONTINGENT — do not promote until Brent hire approved)

| Patch | Path | Addresses |
|---|---|---|
| Kabilan | `docs/people/drafts/agents/kabilan.agent-patch.md` | Brent handoff row; infra-scope split (§4.3); env-var + OAuth boundary |
| Peter | `docs/people/drafts/agents/peter.agent-patch.md` | Brent Tier-1 GCP approval gate; Cloud SQL ADR authorship (§4.2) |
| Linda | `docs/people/drafts/agents/linda.agent-patch.md` | Two new notebooks; tactical-playbook accuracy hold; cloud-source-currency routing gap (§4.5) |

> Brent's own JD (`brent.agent.md`) is **not** patched this session — it remains a screen-only proposal. Its Outcome 4b contradiction (§4.2) is logged for correction at hire time.

---

## 7. People Artifact Updates (this session)

| Artifact | Change |
|---|---|
| `skills-taxonomy.md` | Added `tool-selection`; fixed stale `.github/agents/rl.matt.agent.md` reference; logged 12 GCP/DevOps gaps + `tool-selection`; updated date |
| `agent-register.md` | Added Brent to Open Headcount; updated date |
| `org-chart.md` | Added Brent to Open Headcount; updated date |

---

## 8. Housekeeping Flags (user action)

- **Stale promoted drafts (carried from 2026-05-23, never cleaned):** `docs/people/drafts/skills/*-patch.md` (engineering-architecture, miro-mcp, python-domain-modeling, python-domain-modeling-layer-arch, dev-environment, version-control-pr-discipline), `docs/people/drafts/skills/ddd-strategic/`. Confirm deletion.
- **Stale `tool-selection` duplicate:** `docs/people/drafts/skills/tool-selection/` (live at `.agents/skills/tool-selection/`). Confirm deletion.
- **Stale path references project-wide:** People artifacts and the 2026-05-23 report still cite `.github/agents/rl.<name>.agent.md`. Agents migrated to `.claude/agents/<name>.md` on 2026-06-04.

---

## 9. New Hire Triggers

**One.** The cloud/DevOps execution + source-currency responsibility (§4.5) is currently orphaned and cannot be absorbed by any existing agent (Kabilan writes no infra config; Peter does not execute; Linda makes no domain judgments; Graeme is geotechnical-only). **This is the strategic justification for the Brent hire.** Recommend Harriet run `hiring-agent-management` HIRE mode to formally screen Brent against strategy and cognitive-load criteria before approval.

---

## 10. User Approvals Required

| Item | Action | Owner |
|---|---|---|
| Brent hire decision | Approve / defer / reject the DevOps/GCP role | User |
| ADR-authorship resolution (§4.2) | Confirm Peter authors Cloud SQL ADR from Brent input | User + Peter |
| Infra-scope split (§4.3) | Confirm Kabilan = app-infra, Brent = cloud-infra | User + Kabilan |
| Contingent JD patches (§6) | Approve for promotion **if** Brent hired | User |
| Notebook intake (§4.6) | Approve "DevOps & GCP Infrastructure"; hold tactical-playbook | User + Linda |
| Housekeeping deletions (§8) | Confirm stale drafts can be deleted | User |

---

## 11. Next Sync Eligibility

| Trigger | Earliest date |
|---|---|
| Quarterly cadence | 2026-08-22 (90 days from 2026-05-23 baseline) |
| New hire onboarded | On Brent (or next agent) approval + onboarding |
| Major product milestone | On Skeleton Generator ship (target 2026-06-30) |

**Next action:** User decides on the Brent hire (§9–10). If approved, Harriet promotes the three contingent patches and corrects Brent's Outcome 4b. If deferred, the cloud/DevOps orphan (§4.5) remains logged and unowned.
