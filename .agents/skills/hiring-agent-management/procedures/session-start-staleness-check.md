# Session-Start Staleness Check

Run at the start of **every** session (regardless of mode) before proceeding with the requested task.

1. Run the check per agent (preferred): for each file in `.github/agents/`, get that file's last-updated date and run `git log --oneline --since="<date>" -- docs/product/strategy/ docs/adr/ specs/ AGENTS.md .github/agents/`. If a quick single cutoff is needed, use the **oldest** last-updated date among `.github/agents/` files, not the most recent.
2. If **no decision-bearing files changed** → proceed with the requested mode. No report needed.
3. If **decision-bearing files changed** → produce a one-paragraph staleness flag naming the changed files and which agents are likely affected. If `AGENTS.md` or any file in `.github/agents/` changed, flag all agents whose scope overlaps with the changed section and note that an organisational boundary may have shifted. Ask: "I noticed recent decision changes. Should I run a full REFRESH before proceeding, or continue with your request?"
4. If the user says continue → proceed with the requested mode. If the user says refresh → switch to REFRESH mode.
