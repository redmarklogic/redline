Review the entire conversation history from this session and produce a retrospective report.

## Section 1 — What Worked

Identify:
- Problem-solving patterns that resolved on the first or second attempt
- Tools or commands that returned accurate, complete results
- Correct assumptions that needed no course-correction
- Skill invocations that matched the task cleanly

Concise bullet list. No padding.

## Section 2 — What Didn't Work

Identify friction points:
- **Hallucinations**: wrong file paths, non-existent functions, invented flags
- **Syntax errors**: shell/language errors caused by wrong platform syntax
- **Tool failures**: repeated retries of the same tool call
- **Manual corrections**: places where you had to correct Claude directly
- **Wrong assumptions**: misread task scope, wrong technology branch
- **Over-explanation**: responses that buried signal in prose

For each item: what happened, cost (turns lost, user effort), root cause.

## Section 3 — Actionable Updates (Proposals Only — no files written yet)

Based on sections 1 and 2, propose updates in three categories:

**A. CLAUDE.md / AGENTS.md additions** — only if the session revealed a persistent gap not already covered.
Format:
> Proposed addition to [file, section]:
> `[exact text]`
> Reason: [one sentence]

**B. New Skill** — only if a multi-step workflow was repeated or is likely to recur.
Provide the full draft command content inline.

**C. New Hook** — only if a recurring syntax or style check was missed that a hook could catch automatically.
Format:
> Hook: [event] → [shell command]
> Reason: [what this prevents]

## Section 4 — Session Time Profiler

Reconstruct a time profile of the session by scanning conversation turns, tool calls, and task boundaries.

**Step 1 — Identify tasks.** Group the session into discrete tasks (numbered T01, T02, …). A task is a distinct goal the user asked for, not individual tool calls. Estimate relative time spent on each task based on: number of turns, retries, tool calls, and apparent complexity. Express each as a percentage of total session time.

**Step 2 — Render a Gantt chart.** Produce an ASCII Gantt chart with this layout:

```
SESSION TIME PROFILER
=====================
Total tasks: N  |  Longest: T0X (name)  |  Most retries: T0X (name)

ID   │ Task Name (truncated to 30 chars) │ Timeline (% of session)          │  Time%
─────┼───────────────────────────────────┼──────────────────────────────────┼───────
T01  │ Setup / orientation               │ ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │  12%
T02  │ Implement feature X               │ ░░░░████████████░░░░░░░░░░░░░░░░ │  38%
T03  │ Debug failing test                │ ░░░░░░░░░░░░░░░░████████░░░░░░░░ │  25%
T04  │ Code review / retro               │ ░░░░░░░░░░░░░░░░░░░░░░░░████████ │  25%
─────┴───────────────────────────────────┴──────────────────────────────────┴───────
     0%                                                                      100%

LEGEND
══════
T01  Setup / orientation          — Initial file reads, context loading, task scoping
T02  Implement feature X          — [brief description of what was done]
T03  Debug failing test           — [brief description, including retry count if > 1]
T04  Code review / retro          — [brief description]

KEY OBSERVATIONS
════════════════
• Biggest time sink: T0X — [reason, e.g. "3 retry loops due to wrong shell syntax"]
• Quick wins: T0X, T0X — completed in < 5% each
• Optimisation target: T0X — [what change would cut this time, e.g. "a hook or memory entry"]
```

Rules for the chart:
- Use `█` for active periods and `░` for inactive periods. The timeline column is 32 chars wide (each `█` = ~3%).
- Tasks are sequential — no overlap unless genuinely parallel tool calls.
- If a task had > 1 retry loop, append `(×N retries)` to the task name in the legend.
- If the session was short (< 5 tasks), merge micro-tasks rather than listing one-liners.

**Step 3 — Optimisation table.** After the chart, add a compact table:

```
OPTIMISATION TARGETS (ranked by impact)
════════════════════════════════════════
Rank │ Task │ Time% │ Root cause              │ Suggested fix
─────┼──────┼───────┼─────────────────────────┼──────────────────────────────────
  1  │ T03  │  25%  │ Wrong shell syntax       │ Add PowerShell hook
  2  │ T02  │  38%  │ Large scope, unavoidable │ —
```

## Presentation Rules

- Present all three sections before asking for confirmation
- After presenting, list each proposed change as **[A/B/C][number] — [one-line description]**
- Ask: "Which of these should I write? (list numbers, or 'none')"
- Write only confirmed items, one file at a time
- Section 4 (Time Profiler) is always rendered — no confirmation needed
