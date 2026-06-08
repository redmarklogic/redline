---
name: sync-agent-topology
description: Use when running a periodic Agent Topology Sync — triggered quarterly, on a new agent hire, a major strategy pivot, a significant product milestone, or a significant batch of client feedback. Facilitates a structured cross-agent session where each agent reflects using their assigned knowledge bases and proposes JD patches.
disable-model-invocation: true
---

# Agent Topology Sync

<!-- Manual-only: writes JD patches and org-chart updates — must not auto-invoke. -->

## Boundary Contract

## When to Use

Run a Topology Sync when **any** of the following is true:

- Quarterly cadence: 90 days have elapsed since the last sync
- A new agent has been hired and onboarded
- A major strategy pivot or new strategic bet has been approved by the advisory board
- A significant product milestone has been shipped
- A significant batch of client feedback has been processed by the advisory board

Do NOT run a Topology Sync for routine single-agent JD updates. Use the REFRESH mode of
`hr-hire-agent` for targeted, single-agent drift fixes.

## The Reflection Protocol — Non-Negotiable

Each reflecting agent MUST complete the Reflection Protocol before contributing to the
session. Skipping any step is a session violation.

> "JD review is not the same as knowledge review." — JD files encode past decisions.
> Knowledge bases encode current best practice. Both are required.

## Session Phases

Full step-by-step procedure: `procedures/run-topology-sync.md`

| Phase | Lead | Output |
|---|---|---|
| Pre-session prep | Facilitating agent | Drift Summary, agenda |
| Delta collection | All reflecting agents | Delta Statements (one per agent) |
| Gap & overlap analysis | Facilitating agent | Orphan list, conflict list |
| SRP Compliance Pass | Facilitating agent | `violations-list.md` |
| JD patch drafting | Facilitating agent | Draft patches in `docs/people/drafts/agents/` |
| Report publication | Facilitating agent | Topology Sync Report |

## Output Artifacts

| Artifact | Path | Owner | Required |
|---|---|---|---|
| Topology Sync Report | `docs/people/drafts/reports/topology-sync-YYYY-MM-DD.md` | Facilitating agent | Yes |
| Draft JD patches | `docs/people/drafts/agents/<agent>.agent.md` | Facilitating agent | Yes |
| Updated agent register | `docs/people/agent-register.md` | Facilitating agent | Yes |
| Updated org chart | `docs/people/org-chart.md` | Facilitating agent | Yes |
| Updated skills taxonomy | `docs/people/skills-taxonomy.md` | Facilitating agent | Yes |
| SRP violations list | `docs/people/drafts/reports/violations-list.md` | Facilitating agent | **Yes — sync cannot be marked complete without it** |


See `procedures/run-topology-sync.md` for the full step-by-step procedure.
See `procedures/srp-scan-procedure.md` for the SRP Compliance Pass algorithm.

## Common Mistakes

| Mistake | Correct behaviour |
|---|---|
| Agent reflects from JD memory only, skipping knowledge bases | Reflection Protocol Steps R1–R4 are mandatory — no exceptions |
| Online search skipped because "there's no specific problem" | Step R3 is a currency check, not a troubleshooting step; run it regardless |
| Facilitating agent writes JD patches without Delta Statements as input | Delta Statements from Steps R1–R4 are the required evidence base for every patch |
| Sync triggered by a single routine JD change | Use `hr-hire-agent` REFRESH mode instead |
| Advisory board agents omitted because "they don't have JDs to update" | Advisory board agents reflect on their knowledge bases and handoff definitions; they participate fully |
| Draft JD patches written directly to `.claude/agents/` | Draft-first constraint: all patches to `docs/people/drafts/agents/` until user promotes |
| SRP Compliance Pass skipped | The SRP Compliance Pass is mandatory — sync is incomplete without `violations-list.md` |
