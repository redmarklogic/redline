---
name: mcp-cce
description: Use when discovering code or docs/ company memory, starting multi-phase work needing context persistence, or after creating a new file.
---

# Code Context Engine MCP

CCE indexes the project so the agent searches instead of reading files. ~94% input-token savings per exploration query. Indexes code, Markdown, YAML, JSON - including `docs/` (ADRs, research, strategy).

## Prerequisite

CCE tools are deferred. Load them once before any CCE tool call:

```
ToolSearch query: "select:mcp__context-engine__context_search,mcp__context-engine__session_recall,mcp__context-engine__expand_chunk"
```

Without this step the tools are invisible and the agent falls back to Read/Grep/Glob sweeps.

## Session Start

Before any file exploration, call `mcp__context-engine__session_recall` to load prior decisions and active work areas. This prevents context compaction events and avoids re-explaining architecture every session.

## Boundary Contract

**Applies To:** Discovery, session continuity, file indexing | **Produces:** Indexed codebase via 11 MCP tools | **Does Not Cover:** Terminal compression (`rtk`), external knowledge (use NotebookLM)

## When to Use

- **Exploring/discovering** (where is X, how does Y work) → `context_search` (not Read/Glob sweeps)
- **Answering a question (no editing)** → `context_search` is the final source. If the returned chunks answer the question, respond directly. Do NOT follow up with Read, `expand_chunk`, or Glob on files CCE already covered.
- **Full file needed for editing** → Read
- **Specific section** → `context_search` + `expand_chunk`
- **Exact strings / symbol definitions / known paths** → Grep/Glob as usual
- **Session start** → `session_recall` | **New file** → `reindex`

### Stop Rule

After `context_search`, check: do chunks answer the question? If yes → respond directly. If no and it's a status/info query → answer from partial chunks (no Read). If no and you're writing an artifact → try `expand_chunk` first, then Read only if needed.

Key tools: `context_search` (explore), `expand_chunk` (full body), `record_decision` (design choice), `session_recall` (session start), `reindex` (new file). All names carry the `mcp__context-engine__` prefix in the tool list. See `procedures/cce-usage.md` for all tools and examples.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Read/Glob sweep for exploration | `context_search` first; Read only for edits |
| Skipping ToolSearch loading step | CCE tools are deferred - load them or they don't exist |
| `expand_chunk` fails → Read | For info queries, answer from partial chunks |
| Glob the tree after `context_search` | CCE indexes the full tree |
| No `reindex` after creating file | `reindex <file>` immediately |

## Subagent Usage

Subagents inherit MCP tools and load them the same way (ToolSearch). The SubagentStart hook (`.claude/hooks/cce-inject.ps1`) injects the loading incantation and recent decisions automatically. The server key in `.mcp.json` is exactly `context-engine` - tool names are `mcp__context-engine__<tool>` (a missing trailing `e` in the server name silently fails with "Unknown tool").
