---
name: customization-mechanism-triage
description: >
  Use before creating any VS Code Copilot customization artifact. Determines which
  mechanism — instruction, prompt file, custom agent, skill, VS Code hook, or plugin —
  best fits the stated need, and auto-corrects requests that name the wrong mechanism.
  Apply whenever someone asks to "add a skill for X", "create an agent for X", or
  "add a hook for X".
---

# Customization Mechanism Triage

## Boundary Contract

**Apply this skill before creating any VS Code Copilot customization artifact.**

| Input | A request to create any customization artifact |
|---|---|
| Output | Identified correct mechanism + correction statement if the wrong one was named |
| Out of scope | Writing the artifact itself (use `skills-create`, `writing-skills`, or `hiring-agent-management`) |

---

## The Six Mechanisms

| Mechanism | File | Invoked | Runs code? | Portable? |
|---|---|---|---|---|
| **Custom Instruction** | `AGENTS.md`, `.instructions.md`, `copilot-instructions.md` | Automatic, every chat | No | VS Code + GitHub only |
| **Prompt File** | `.github/prompts/*.prompt.md` | Manual (`/slash`) | No | VS Code only |
| **Custom Agent** | `.github/agents/*.agent.md` | Manual (agent picker) | Via hooks only | VS Code + GitHub |
| **Skill** | `.agents/skills/<name>/SKILL.md` | Auto (relevance) or `/slash` | Yes (linked scripts) | Open standard — VS Code, CLI, cloud |
| **VS Code Hook** | `.github/hooks/*.json` | Automatic (lifecycle event) | Yes — shell command | VS Code + Claude Code + CLI |
| **Plugin** | directory + `plugin.json` | Installed | Yes (bundles above) | Cross-tool |

### VS Code Hooks vs git pre-commit hooks

These are different systems. A common confusion documented in the RED phase baseline.

| | VS Code Hook | git pre-commit hook |
|---|---|---|
| **File** | `.github/hooks/*.json` | `.git/hooks/pre-commit` or `.pre-commit-config.yaml` |
| **Triggers** | Agent lifecycle events (SessionStart, PreToolUse, PostToolUse, Stop, …) | Before a git commit |
| **Scope** | Every agent session, any file edit | Only at commit time |
| **Use for** | "Run formatter after every agent edit", "Block dangerous commands" | "Run linter before committing", "Enforce commit message format" |

When someone says "add a hook to run X after file edits during an agent session" → **VS Code `PostToolUse` hook**.
When someone says "run X before committing" → **git pre-commit hook** (`hooks/` directory + `.pre-commit-config.yaml`).

---

## Triage Decision Tree

Apply in order. Stop at the first match.

### 1. Should this apply silently to every chat with no invocation?
→ **Custom Instruction**

- Passive rule: "always use X style", "never use Y library", "enforce naming convention Z"
- File-scoped: "apply only to `.py` files" → use `.instructions.md` with `applyTo` glob
- Project-wide: use `AGENTS.md` or `copilot-instructions.md`

**Key test**: Is this a *rule* (do/don't), not a *procedure* (how to)? → Instruction.

### 2. Should this fire automatically at a lifecycle point during an agent session?
→ **VS Code Hook** (`.github/hooks/*.json`)

Events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`,
`PreCompact`, `SubagentStart`, `SubagentStop`, `Stop`.

- "Run formatter after every file edit" → `PostToolUse`
- "Block dangerous terminal commands" → `PreToolUse`
- "Inject environment info at session start" → `SessionStart`
- "Force tests before the agent stops" → `Stop`

**Key test**: Would you write a shell script to enforce it during an active agent session, not at commit time? → VS Code Hook.

### 3. Is this a persistent persona — a named role with tool restrictions and/or handoffs?
→ **Custom Agent** (`.github/agents/*.agent.md`)

- Named roles: Harriet, Kabilan, a security reviewer, a read-only planner
- Needs tool restrictions (e.g., cannot edit files)
- Needs handoffs to other agents

**Key test**: Does it need an identity in the agent picker, tool restrictions, or handoffs? → Custom Agent.

### 4. Is this a reusable procedure with supporting scripts, examples, or resources?
→ **Skill** (`.agents/skills/<name>/SKILL.md`)

- Multi-step workflow with a procedure
- Needs supporting scripts, templates, or reference files
- Should be portable across VS Code, CLI, and cloud agent

**Key test**: Is it a *procedure* (how to do X) rather than a *rule* (do/don't)? Does it need more than text? → Skill.

### 5. Is this a one-off task invoked manually, with no scripts and no persistent persona?
→ **Prompt File** (`.github/prompts/*.prompt.md`)

- Single-purpose, invoked once per task
- No reuse across tools required

**Key test**: Would you invoke it exactly once per task with no cross-tool portability? → Prompt File.

### 6. Are you packaging multiple of the above for distribution?
→ **Plugin** (`plugin.json` bundle)

---

## Rule vs Procedure Test

The most common confusion is instruction vs skill. Apply this test:

| Question | If yes → | If no → |
|---|---|---|
| Is this a standard/convention? | Instruction | Maybe skill |
| Does it have steps to follow? | Skill | Maybe instruction |
| Does it need scripts or resources? | Skill | Instruction |
| Should it apply to all files of a type automatically? | Instruction (`applyTo`) | Maybe skill |
| Should it be available in Copilot CLI and cloud agent? | Skill | Instruction |

---

## Auto-Correction Rules

When a request names a mechanism, verify before proceeding. State the correction explicitly:

> "This is better served by a [correct mechanism], not a [requested mechanism], because [one-sentence reason]."

| Request says... | Need is... | Correct mechanism |
|---|---|---|
| "add a skill for always using X style" | Passive rule, no scripts | **Instruction** |
| "add a skill to run formatter after every agent edit" | Lifecycle automation in session | **VS Code Hook** (`PostToolUse`) |
| "add a hook to enforce commit message format" | Git commit gate | **git pre-commit hook** (not VS Code hook) |
| "add a skill for a planner/reviewer persona" | Persistent role with tool restrictions | **Custom Agent** |
| "add an agent to scaffold a component" | Single task, no persona or scripts | **Prompt File** |
| "add a skill for a debugging/ingestion workflow with scripts" | Multi-step, portable, needs scripts | **Skill** (correct) |
| "add a hook for a step-by-step testing procedure" | Reusable knowledge, no lifecycle trigger | **Skill** |

---

## Procedure

1. Read the request and identify the stated need.
2. Apply the decision tree above, stopping at the first match.
3. If the named mechanism differs from the triage result, state the correction before creating anything.
4. Hand off to the appropriate workflow:
   - **Instruction** → create `.instructions.md` with correct `applyTo` glob
   - **VS Code Hook** → create `.github/hooks/<name>.json` with correct lifecycle event
   - **Custom Agent** → draft in `docs/people/drafts/agents/` (Harriet's draft-first constraint applies)
   - **Skill** → use `skills-create` then `writing-skills`
   - **Prompt File** → create `.github/prompts/*.prompt.md`
   - **Plugin** → `plugin.json` bundle
