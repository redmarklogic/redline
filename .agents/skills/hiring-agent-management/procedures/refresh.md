# REFRESH Workflow

Detect and resolve drift between business decisions and agent definitions. Business decisions evolve continuously; agent JDs and skills are point-in-time artifacts that go stale.

## Step 1 — Gather the decision delta

1. For each agent in `.github/agents/`, read the file's last-modified date from git: `git log -1 --format="%ai" -- .github/agents/<file>`.
2. Collect all commits to decision-bearing paths since that date:
   - `docs/product/strategy/` (strategic bets, OKRs, positioning, GTM, non-goals)
   - `docs/adr/` (architecture decision records)
   - `specs/` (feature specs, plans, tasks)
   - `docs/product/operations/` (cadences, pricing)
   - `docs/research/` (research findings that inform constraints)
   - `AGENTS.md` and `.github/agents/` (organisational boundaries, handoff chains, agent scope)
3. Read each changed file. Extract the concrete decisions: what was added, changed, or parked.

## Step 2 — Classify impact per agent

For each decision, determine which agents are affected and how:

| Impact type | Description | Example |
|---|---|---|
| **New constraint** | A decision introduces a boundary the agent's JD does not yet reflect | "Word task pane parked" → Matt's JD should state "web only" |
| **Removed scope** | Something the agent was responsible for is now out of scope or parked | A parked feature means the agent no longer needs to design for it |
| **New responsibility** | A decision creates work that falls within an existing agent's domain | A new strategic bet adds a surface the agent should own |
| **Skill gap** | A decision requires knowledge the agent does not have a skill for | A new technology choice creates a skill gap |
| **No impact** | The decision does not affect this agent | Strategy change to a domain another agent owns |

Produce a **staleness table**:

| Agent | Last updated | Decisions since | Impact type | Proposed action |
|---|---|---|---|---|

## Step 3 — Scope the refresh (advisory board vs. non-advisory)

- **Non-advisory-board agents** (Matt, future hires, Harriet herself): draft JD patches directly. Apply the Prompt Rewriting Rules from the main SKILL.md.
- **Advisory-board agents** (Ron, Mark, John, Graeme): flag the drift and route the update to the agent themselves. Example: "Ron, your JD still references [X] — that has been parked per ADR-006. Please update your constraints." Advisory board members maintain their own JDs; this role flags, it does not rewrite.

## Step 4 — Check skills for staleness

For each affected agent, check whether their skills need updating:

1. Read each skill the agent uses (from `agent-register.md`).
2. If a decision changes a domain rule the skill encodes, flag the skill as stale.
3. For stale skills: draft a skill patch (if within this role's capability) or route to the skill's primary user for update.

## Step 5 — Output

- Staleness report → `docs/people/drafts/reports/refresh-<YYYY-MM-DD>.md`
- Draft JD patches for non-advisory agents → `docs/people/drafts/agents/<agent>.agent.md` (include a diff-style summary of what changed and why)
- Routing messages for advisory-board agents → listed in the report with the exact message to send

## Step 6 — After user approval

Apply the patches. Update `docs/people/agent-register.md` with the new "Last updated" date for each refreshed agent.
