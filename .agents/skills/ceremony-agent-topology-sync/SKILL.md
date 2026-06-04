---
name: ceremony-agent-topology-sync
description: Use when running a periodic Agent Topology Sync — triggered quarterly, on a new agent hire, a major strategy pivot, a significant product milestone, or a significant batch of client feedback. Facilitates a structured cross-agent session where each agent reflects using their assigned knowledge bases and proposes JD patches.
---

# Agent Topology Sync

## Boundary Contract

## When to Use

Run a Topology Sync when **any** of the following is true:

- Quarterly cadence: 90 days have elapsed since the last sync
- A new agent has been hired and onboarded
- A major strategy pivot or new strategic bet has been approved by the advisory board
- A significant product milestone has been shipped
- A significant batch of client feedback has been processed by the advisory board

Do NOT run a Topology Sync for routine single-agent JD updates. Use the REFRESH mode of
`hiring-agent-management` for targeted, single-agent drift fixes.

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
| JD patch drafting | Facilitating agent | Draft patches in `docs/people/drafts/agents/` |
| Report publication | Facilitating agent | Topology Sync Report |

## Output Artifacts

| Artifact | Path | Owner |
|---|---|---|
| Topology Sync Report | `docs/people/drafts/reports/topology-sync-YYYY-MM-DD.md` | Facilitating agent |
| Draft JD patches | `docs/people/drafts/agents/<agent>.agent.md` | Facilitating agent |
| Updated agent register | `docs/people/agent-register.md` | Facilitating agent |
| Updated org chart | `docs/people/org-chart.md` | Facilitating agent |
| Updated skills taxonomy | `docs/people/skills-taxonomy.md` | Facilitating agent |


See `procedures/ceremony-agent-topology-sync.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Correct behaviour |
|---|---|
| Agent reflects from JD memory only, skipping knowledge bases | Reflection Protocol Steps R1–R4 are mandatory — no exceptions |
| Online search skipped because "there's no specific problem" | Step R3 is a currency check, not a troubleshooting step; run it regardless |
| Facilitating agent writes JD patches without Delta Statements as input | Delta Statements from Steps R1–R4 are the required evidence base for every patch |
| Sync triggered by a single routine JD change | Use `hiring-agent-management` REFRESH mode instead |
| Advisory board agents omitted because "they don't have JDs to update" | Advisory board agents reflect on their knowledge bases and handoff definitions; they participate fully |
| Draft JD patches written directly to `.claude/agents/` | Draft-first constraint: all patches to `docs/people/drafts/agents/` until user promotes |
