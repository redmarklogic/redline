# Daily Standup — Morning Brief

Generate a morning brief for today's work using live GitHub Projects board state.

## What to do

Load and follow the `agile-daily-standup` skill at `.agents/skills/agile-daily-standup/SKILL.md`.
Run the full workflow (Steps 1–8). Write the brief to file — do not render it in the
conversation.

Use today's date from the session context. Do not ask for clarification — read the
board, read the sprint context, and write the brief immediately.

## Preflight checks (abort with clear error if either fails)

1. `gh auth status` — must list `project` in scopes
2. `.agents/tools/github_projects/project_config.json` must exist and be ≤ 24 h old

If `docs/product/tasks/this-week.md` is absent or older than today, run
`sync-this-week` (procedure 10 in `.agents/skills/github-projects/SKILL.md`) before
generating the brief.

## Output

Write the full brief to `docs/standups/YYYY-MM-DD.md` (use today's date).
Do not summarise, truncate, or skip any section — even empty ones need their
"✓ Nothing here" confirmation so the founder knows the board was checked.

Add one line at the end of the file:
> Next: [the single most important thing to do right now, from the execution plan]

After writing the file, confirm in conversation with a single line:
`Brief written to docs/standups/YYYY-MM-DD.md`

Do not render the brief content in the chat.
