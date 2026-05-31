---
name: mcp-cce
description: Use when discovering code or docs/ company memory, starting multi-phase work needing context persistence, or after creating a new file.
---

# Code Context Engine MCP

CCE indexes the project so the agent searches instead of reading files. 94% input-token savings. Indexes code, Markdown, YAML, JSON - including `docs/` (ADRs, research, strategy).

## Prerequisite

CCE tools are deferred. Call `tool_search("code context engine MCP")` before any CCE tool call. Without this step the tools are invisible and the agent falls back to `read_file`.

## Session Start

Before any file exploration, call `session_recall` to load prior decisions and active work areas. This prevents context compaction events and avoids re-explaining architecture every session.

## Boundary Contract

**Applies To:** Discovery, session continuity, file indexing | **Produces:** Indexed codebase via 9 MCP tools | **Does Not Cover:** Terminal compression (`rtk`), external knowledge (use NotebookLM)

## When to Use

- **Exploring/discovering** → `context_search` (not `read_file`)
- **Full file needed for editing** → `read_file`
- **Specific section** → `context_search` + `expand_chunk`
- **Session start** → `session_recall` | **New file** → `reindex`

Key tools: `context_search` (explore), `expand_chunk` (full body), `record_decision` (design choice), `session_recall` (session start), `reindex` (new file). See `procedures/cce-usage.md` for all 9 tools and examples.

## Common Mistakes

| Mistake | Fix |
|---|---|
| `read_file` to find a pattern | Use `context_search` first |
| `grep_search` for semantic queries | Use `context_search`; `grep_search` is for exact matches only |
| No `reindex` after creating a file | `reindex <file>` immediately after creation |

## Subagent Usage

Subagents need `context-engine/*` in their frontmatter `tools:` list. The server name must match the key in `.vscode/mcp.json` exactly — `context-engin/*` (missing trailing `e`) silently fails with "Unknown tool" warning.

Each agent JD's Session Discipline must instruct: `tool_search('code context engine MCP')` → `session_recall` → `context_search` for discovery.