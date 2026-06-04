# Ceremony Agent Topology Sync — Detailed Reference

### Inputs
- Agent files in `.claude/agents/`
- `docs/product/strategy/strategic-bets.md` and current roadmap
- New ADRs, specs, and PRDs created since the previous sync
- Client feedback signals (if available)
- Each agent's assigned NotebookLM notebooks and repo docs

### Outputs
- Topology Sync Report at `docs/people/drafts/reports/topology-sync-YYYY-MM-DD.md`
- Draft JD patches at `docs/people/drafts/agents/` for every agent with confirmed drift
- Orphan responsibility list (responsibilities with no owner)
- New hire trigger list (responsibilities that cannot be absorbed by any current agent)
- Updated `docs/people/agent-register.md`, `org-chart.md`, and `skills-taxonomy.md`

### Out of Scope
- Hiring decisions (`hiring-agent-management` → HIRE mode)
- Performance improvement (`hiring-agent-management` → AUDIT/PIP mode)
- Authoring domain content (geotechnical, PRDs, marketing copy)

### Step R1 — Repo Docs Scan
The reflecting agent reads:
- `docs/product/strategy/strategic-bets.md`
- All ADRs created since the previous sync
- All PRDs and specs merged since the previous sync
- Their own current JD in `.claude/agents/`

### Step R2 — Knowledge Base Query
The reflecting agent queries each of their assigned NotebookLM notebooks with:
1. "What frameworks, guidelines, or standards in my domain have been updated or superseded since [date of previous sync]?"
2. "Are there gaps between my current responsibilities and what best practice now recommends for this domain?"

Document findings verbatim. Do not summarise — raw notebook output is the evidence.

### Step R3 — Online Currency Check (when applicable)
If a knowledge base signals that a framework or standard may have been updated, or if the
agent has not had an online search opportunity since the previous sync, the reflecting
agent runs targeted online searches for:
- Updated editions of frameworks referenced in their skill files
- New industry guidelines relevant to their domain
- Deprecated tools, methods, or APIs they currently recommend

Record each finding as: `[Source] [Date] [Change] [Impact on current JD or skills]`.

### Step R4 — Delta Statement
Each reflecting agent produces a written Delta Statement before the facilitated session:
- "Here is what I own today."
- "Here is what has changed in my domain since the last sync (with evidence from Steps R1–R3)."
- "Here is where my current JD or skills may now be incorrect, incomplete, or outdated."
- "Here are the frameworks or guidelines I think need to be added or updated."

The Delta Statement is the input to the facilitated session. An agent without a Delta
Statement does not contribute to the session.
