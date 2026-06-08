# JD Frontmatter Governance

When drafting, updating, auditing, or refreshing `.claude/agents/*.md`, follow the Claude Code subagent format. Person agent JDs live in `.claude/agents/`; vendor-generated SpecKit agents remain in `.github/agents/`.

Every Redline-owned custom agent must declare these YAML frontmatter fields explicitly:

| Field | Rule |
|---|---|
| `name` | Use the identifier that handoffs and subagent lists reference. |
| `description` | Keep the invocation and role summary concise. |
| `tools` | List the Claude Code tools available to the agent (Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, Agent, etc.). |

Vendor-generated agents, including `speckit.*`, must not be manually edited. If they violate this governance, report the drift and fix it through the vendor generation path rather than patching the generated file.

## Description Field Rules

Frontmatter `description` fields describe only the agent's own scope. No other agent name, boundary allocation ("belongs to X"), or adjacent-role negation ("X's domain") appears in a `description` field. This field drives Claude Code dispatch routing — pollution causes mis-routing.
