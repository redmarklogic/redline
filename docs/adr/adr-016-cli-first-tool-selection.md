# ADR-016 — CLI-First Tool Selection

## Summary

When an agent can accomplish an operation via a CLI tool (`gh`, `gws`, `gcloud`), an MCP server, or a direct API call, the CLI is the preferred mechanism. This decision establishes a project-wide routing policy for external tool use, documented in `.agents/skills/tool-selection/SKILL.md` and enforced via the `AGENTS.md` convention layer. The primary constraint it imposes: agents must not reach for MCP servers or raw API calls when an installed CLI covers the operation.

## Decision

Agents select the narrowest available CLI tool for any external operation. Direct API calls are a fallback used only when no CLI covers the operation, the CLI is unavailable in the environment, or batching requirements exceed CLI ergonomics.

## Status

Accepted — 2026-06-06

## Context

The project uses three CLIs covering the majority of external operations:
- `gh` — GitHub (repos, PRs, issues, Actions, Projects)
- `gws` — Google Workspace (Gmail, Drive, Calendar, Sheets, Docs, Chat)
- `gcloud` — GCP infrastructure (Cloud SQL, Compute, Cloud Run, IAM, Cloud Storage)

Without a stated policy, agents default to whichever tool they encountered most in training — typically direct API calls or MCP servers — rather than the installed CLIs. This produces inconsistent behaviour, harder-to-audit logs, and token waste from custom HTTP client setup.

`gws` was released in March 2026 and is absent from most LLM training data, making an explicit routing rule especially important: agents otherwise reach for `gcloud` (wrong) or direct Gmail API calls (unnecessary).

## Options Considered

- **CLI-first (selected):** CLIs as the default; MCP and direct API as explicit fallbacks.
- **MCP-first:** MCP servers as the default integration layer. Rejected — MCP servers require server process setup and are less auditable in agent logs than shell commands.
- **Direct API-first:** Raw REST/GraphQL calls. Rejected — highest setup cost, no shared auth state, least readable in logs.
- **No policy:** Leave tool selection to agent discretion. Rejected — produces inconsistent behaviour and re-explanation overhead every session.

## Decision Rationale

CLIs provide three advantages over the alternatives:

1. **Auditability** — shell commands appear verbatim in agent transcripts; MCP calls and API requests require log reconstruction.
2. **Auth reuse** — CLIs maintain their own credential stores (`gh auth`, `gws auth`, `gcloud auth`); direct API calls require credential injection per request.
3. **Token efficiency** — a single CLI invocation replaces multi-step HTTP client setup, response parsing, and error handling in agent context.

The "narrowest tool" sub-rule (gh for GitHub, gws for Workspace, gcloud for GCP infrastructure) prevents category errors — notably using `gcloud` for Gmail, which has no Gmail surface.

## Consequences

**Positive:**
- Consistent, auditable agent behaviour across sessions.
- Reduced token overhead — agents skip HTTP client setup.
- Single routing document (`.agents/skills/tool-selection/SKILL.md`) as SSOT for command patterns.

**Negative:**
- Agents running in environments without CLIs installed must fall back to direct API calls — the skill documents this escape hatch.
- `gws --params` requires Bash, not PowerShell (PS5.1 JSON quoting incompatibility) — noted in the skill.
- CLI coverage is not exhaustive; some operations (e.g., GitHub Projects custom field types) still require direct GraphQL calls — also noted in the skill.

## References

- `.agents/skills/tool-selection/SKILL.md` — routing table and command patterns
- ADR-001 — Single Source of Truth (routing table as SSOT for tool selection)
- ADR-013 — Defence-in-Depth (AGENTS.md as convention layer)
