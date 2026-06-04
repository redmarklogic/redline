# Claude Code Migration Audit

**Date:** 2026-06-04
**Branch:** feature/migration-to-claude
**Scope:** `.agents/`, `.github/`, `.vscode/`, `hooks/`, `AGENTS.md`

---

## Summary

The project is configured exclusively for GitHub Copilot. No `.claude/` project directory exists. Key incompatibilities are in the hook system (different event names and registration format) and the instructions/prompts auto-loading mechanism. Skill and agent body content is largely compatible — it's markdown that Claude can read. The main migration work is plumbing (hook registration, MCP config location, instruction inclusion).

---

## Compatibility Table

### Configuration Files

| File | Copilot | Claude Code | Issue | Required Adjustment |
|------|:-------:|:-----------:|-------|---------------------|
| `.vscode/settings.json` | OK | NO | Contains `github.copilot.*` and `chat.*` settings; `.claude/settings.json` explicitly commented out under `chat.hookFilesLocations` | Uncomment Claude Code entries OR remove them (they're VSCode Copilot settings, not Claude Code config) |
| `.vscode/mcp.json` | OK | NO | Claude Code reads MCP config from `.claude/mcp.json`, not `.vscode/mcp.json` | Copy/symlink content to `.claude/mcp.json` |
| `.claude/settings.json` | N/A | NO **Missing** | No `.claude/` directory exists; no hooks registered for Claude Code | Create `.claude/settings.json` with hook registrations (see below) |

---

### Hook System

#### Hook Registration Files (`.github/hooks/`)

| File | Copilot | Claude Code | Issue | Required Adjustment |
|------|:-------:|:-----------:|-------|---------------------|
| `.github/hooks/rtk-rewrite.json` | OK | NO | Copilot hook registration format; references `rtk hook copilot` | Migrate to `.claude/settings.json` `PreToolUse` entry; change command to `rtk hook claude` |
| `.github/hooks/cce-subagent.json` | OK | NO | Uses `SubagentStart` event — does not exist in Claude Code | No direct equivalent; closest approximation is `UserPromptSubmit` or static inclusion in CLAUDE.md |
| `.github/hooks/handover.json` | OK | NO | Uses `SessionStart` event — does not exist in Claude Code | No direct equivalent; session anchoring needs a different mechanism (e.g., a startup script or manual trigger) |

#### Hook Scripts

| File | Copilot | Claude Code | Issue | Required Adjustment |
|------|:-------:|:-----------:|-------|---------------------|
| `.github/hooks/cce-inject.ps1` | OK | PARTIAL | Script is reusable; invocation mechanism missing | Decide whether to invoke via `UserPromptSubmit` hook or embed CCE context differently |
| `hooks/session-start-anchor.ps1` | OK | NO | Called by `SessionStart` which Claude Code lacks | Needs alternative trigger (e.g., a git post-checkout hook, or manual `session-handover` skill invocation) |
| `hooks/session-stop-handover.ps1` | OK | PARTIAL | Claude Code has a `Stop` hook; format/capabilities differ slightly | Migrate to `.claude/settings.json` `Stop` hook; verify script exit-code semantics work with Claude Code |
| `hooks/session-track-writes.ps1` | OK | PARTIAL | Claude Code has `PostToolUse`; per-agent scoping (Kabilan only) is not supported — hooks are global | Migrate to `.claude/settings.json` `PostToolUse` with a `matcher` filter on Write/Edit tools; accept global scope |
| `hooks/*.py` (24 pre-commit scripts) | OK | OK | Pre-commit hooks are git-level, AI-agnostic | No change needed |

---

### Agent Definitions (`.github/agents/`)

| Aspect | Copilot | Claude Code | Issue | Required Adjustment |
|--------|:-------:|:-----------:|-------|---------------------|
| YAML frontmatter (`name`, `description`) | OK | NO not parsed | Claude Code does not auto-load `.github/agents/*.agent.md` files | No action needed for content; ensure agent personas are reachable via AGENTS.md references |
| `tools:` field (e.g., `search`, `web/fetch`, `context-engine/*`) | OK | NO | Copilot-specific tool identifiers; meaningless to Claude Code | Remove or leave as documentation only; does not affect Claude Code behaviour |
| `hooks:` field in agent frontmatter (e.g., Kabilan's `PostToolUse`, `Stop`) | OK | NO | Per-agent hooks in agent files are a Copilot feature; Claude Code hooks are global | Move desired hook behaviours to `.claude/settings.json`; accept global (not per-agent) scope |
| `agents:` field | OK | NO | Copilot agent composition field; no equivalent | Leave as documentation only |
| Body content (persona, constraints, skill tables) | OK | OK | Plain markdown; Claude reads it when referenced | No change; content remains usable |

---

### Prompts (`.github/prompts/`)

| File | Copilot | Claude Code | Issue | Required Adjustment |
|------|:-------:|:-----------:|-------|---------------------|
| `speckit.*.prompt.md` (16 files) | OK | NO not auto-loaded | Copilot auto-loads `.github/prompts/` files; `agent:` frontmatter routes them to specific agents | Content is compatible markdown; not auto-discovered by Claude Code. Reference needed from AGENTS.md or create `.agents/skills/` entries |
| `evaluation-workflow.prompt.md` | OK | NO not auto-loaded | Same issue | Same fix |
| `monthly-editorial-session.prompt.md` | OK | NO not auto-loaded | Same issue | Same fix |

---

### Instructions (`.github/instructions/`)

| File | Copilot | Claude Code | Issue | Required Adjustment |
|------|:-------:|:-----------:|-------|---------------------|
| `rtk.instructions.md` | OK | NO not auto-loaded | Copilot auto-loads via `applyTo: "**"` glob; Claude Code doesn't read `.github/instructions/` | Content already partially covered by global `RTK.md` in `~/.claude/`. Verify overlap; add missing rules to CLAUDE.md if needed |
| `mental-models-protocol.instructions.md` | OK | NO not auto-loaded | Same | Add `@.github/instructions/mental-models-protocol.instructions.md` to AGENTS.md or CLAUDE.md |
| `visual-artifacts.instructions.md` | OK | NO not auto-loaded | Copilot loads this for `docs/**` via `applyTo`; Claude Code has no equivalent scoped loading | Add reference to AGENTS.md with a note that it applies to `docs/**` work |
| `skills-reporting.instructions.md` | OK | NO not auto-loaded | Same | Same fix |

---

### Skill Files (`.agents/skills/`)

| Aspect | Copilot | Claude Code | Issue | Required Adjustment |
|--------|:-------:|:-----------:|-------|---------------------|
| Skill file content (`SKILL.md`) | OK | OK | Plain markdown; readable by Claude Code on demand | No change to content |
| Skill discovery | OK auto-routed via agent JD | PARTIAL manual | Copilot agents load skills via routing tables in JDs; Claude Code reads when told to | AGENTS.md already instructs Claude to load skills from `.agents/skills/` — this works, but requires the agent to follow the instruction |
| `session-handover` skill | OK | PARTIAL | Depends on `.session/session-start.md` written by `SessionStart` hook (missing in Claude Code) | Skill partially broken until session anchoring is solved; fallback procedure in `procedures/session-handover.md` needed |

---

### GitHub Workflows (`.github/workflows/`)

| File | Copilot | Claude Code | Issue | Required Adjustment |
|------|:-------:|:-----------:|-------|---------------------|
| `copilot-setup-steps.yml` | OK | NO | Installs Copilot agent skills and `prek` hooks; no Claude Code equivalent | Leave as-is (runs in CI for Copilot); optionally add a parallel `claude-setup-steps.yml` if Claude Code CI integration is needed |
| `static-checks.yml` | OK | OK | Generic Python CI; AI-agnostic | No change |
| `tests.yml` | OK | OK | Generic Python CI; AI-agnostic | No change |
| `topology-sync.yml` | OK | OK | Generic CI; AI-agnostic | No change |

---

## Migration Checklist

### Must-do (blocking)

- [ ] Create `.claude/mcp.json` — copy CCE server config from `.vscode/mcp.json`
- [ ] Create `.claude/settings.json` with:
  - `PreToolUse` hook → `rtk hook claude` (replaces `rtk hook copilot`)
  - `PostToolUse` hook → `hooks/session-track-writes.ps1` (global; Kabilan-scoping lost)
  - `Stop` hook → `hooks/session-stop-handover.ps1`
- [ ] Update `rtk-rewrite.json` or note that it's Copilot-only and parallel `.claude/` config handles Claude Code

### Should-do (functionality gaps)

- [ ] Decide CCE injection strategy — `SubagentStart` has no Claude Code equivalent. Options:
  - A) Add CCE `session_recall` instruction to AGENTS.md (static, always on)
  - B) Use `UserPromptSubmit` hook to run `cce-inject.ps1` on every user message (dynamic, closer to current behaviour)
- [ ] Session anchoring — `SessionStart` has no Claude Code equivalent. Options:
  - A) Write `.session/session-start.md` manually at session start (poor ergonomics)
  - B) Use a `UserPromptSubmit` hook that writes the SHA once if file doesn't exist
- [ ] Reference `.github/instructions/*.instructions.md` from AGENTS.md so Claude Code picks them up
- [ ] Audit `speckit.*.prompt.md` files — determine if they should become Claude Code skills in `.agents/skills/` or stay Copilot-only

### Won't-do / accept as-is

- `.github/agents/*.agent.md` frontmatter (`tools:`, `hooks:`, `agents:`) — leave in place; harmless to Claude Code, required for Copilot
- Pre-commit hook scripts (`hooks/*.py`) — fully compatible, no change needed
- CI workflows (`static-checks.yml`, `tests.yml`, `topology-sync.yml`) — no change needed
- Skill file content (`.agents/skills/*/SKILL.md`) — no change needed
