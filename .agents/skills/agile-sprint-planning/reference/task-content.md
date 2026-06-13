# Reference: task content — what a board issue body must contain

Internal file of `agile-sprint-planning`, used by `procedures/commit.md` step 5b.
Also applies to ad-hoc task creation when the writer wants a context-complete issue.

**Why this exists.** Agile treats a story card as "a placeholder for a future
conversation" — details are negotiated verbally just before the work starts (*Clean
Agile*; XP). On this project the implementer is the founder days later, or an agent
with **no memory of the planning conversation** — that conversation never happens.
The card must therefore carry, in writing, what the conversation would have supplied:
the problem, the boundaries, and testable acceptance criteria. At the same time,
over-specifying makes a ticket "impenetrable and unusable" and removes the
implementer's judgment (*Sprint*; *Shape Up*) — state the problem and the bar, not
the keystrokes.

## Issue body template (level-1 parents and sub-issues alike)

```markdown
## Problem / Context
[1–3 sentences: the problem this task solves and why now — name the sprint goal,
bet, or blocking task it serves. Problem before solution (Shape Up: pitches open
with the problem, never the feature).]

## Solution outline
[The core elements of the intended approach — enough to start, loose enough to
leave judgment room. Name known prior art (template, ADR, research doc, notebook
finding) the implementer should start from. Never pixel-level prescription.]

## Acceptance criteria
[2–5 testable scenarios in Given / When / Then form (BDD — executable-specification
framing). Each observable in a browser, CLI, or document — "code merged" is not a
criterion. The first criterion is the task's done-when. Write a criterion only if
it can be stated genuinely — a vague bar dressed as Given/When/Then is worse than
naming the gap. Prefer criteria an agent can verify without human intervention
(CLI command, API request, MCP tool, file/exit-code check) and name the check
inline; tag the rest `[human-verify]` (e.g. visual confirmation inside Word).]
- Given …, when …, then … — verify: `<command or tool>`
- Given …, when …, then … `[human-verify]`

## Appetite
[N working days — must equal the board Start→Target span. Appetite is a budget,
not an estimate: when it runs out, surface the cut, don't extend silently.]

## Rabbit holes
[Known unknowns, edge cases, or traps to watch — anything the planning session
learned that the implementer can't see from the code. "None known" is a valid
entry; an empty section is not.]

## No-gos
[What THIS task explicitly does not do, with one-line reasons — the per-task
mirror of the sprint's out-of-scope list. Prevents local scope creep.]

## Agents
[Owner (domain expert accountable for the spec/decision) — implementer noted as
"X implements" per the assignment rule in `procedures/lead.md`.]

## Source
[Path to the sprint plan doc, spec, PRD, or ADR this task descends from.]
```

## Rules

- **Problem before solution.** A body that opens with implementation steps and
  never states why fails review — teams "jump straight to a solution assuming the
  underlying reason is obvious" (*Shape Up*).
- **Acceptance criteria are tests.** A specification is by nature a test
  (*Continuous Delivery*); Given/When/Then maps directly to test-first
  implementation and bounds the work — the implementer writes enough to make the
  criteria pass, nothing more.
- **Agent-verifiable first, honest always.** Prefer criteria checkable by an
  agent through a tool (CLI, API request, MCP) and state the check inline;
  mark genuinely human-only checks `[human-verify]`. Never invent a criterion
  to fill the section — a named verification gap beats a fabricated bar.
- **Context-complete, not exhaustive.** Include what the implementer cannot
  recover from the repo (planning-session findings, gaps, constraints); exclude
  what they can (code structure, existing docs — link instead).
- **Sub-issues carry their own body.** A sub-issue inheriting context "from the
  parent" still fails the no-shared-memory test — each body stands alone, with the
  parent linked for the wider arc.
- The auto-generated `create-task` body (`## Purpose` / `## Source` / `## Done
  when` / `## Agents`) is the floor, not the standard — pass `body=` explicitly
  (or edit after creation) to meet this template during the ceremony.

**Sources:** *Clean Agile* / XP (story-as-conversation, INVEST); *Shape Up*
(pitch structure: problem, appetite, solution, rabbit holes, no-gos); BDD
Given/When/Then (*Continuous Delivery*, *Modern Software Engineering*); notebook
research session 2026-06-13 (Software Development Methodology & Engineering
Organisation notebook).
