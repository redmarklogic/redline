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

## Presentation Rules

- Present all three sections before asking for confirmation
- After presenting, list each proposed change as **[A/B/C][number] — [one-line description]**
- Ask: "Which of these should I write? (list numbers, or 'none')"
- Write only confirmed items, one file at a time
