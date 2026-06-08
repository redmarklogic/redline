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
- **Answering a question (no editing)** → `context_search` is the final source. If the returned chunks answer the question, respond directly. Do NOT follow up with `read_file`, `expand_chunk`, `file_search`, or `list_dir` on files CCE already covered.
- **Full file needed for editing** → `read_file`
- **Specific section** → `context_search` + `expand_chunk`
- **Session start** → `session_recall` | **New file** → `reindex`

### Stop Rule

After `context_search`, check: do chunks answer the question? If yes → respond directly. If no and it's a status/info query → answer from partial chunks (no `read_file`). If no and you're writing an artifact → try `expand_chunk` first, then `read_file` only if needed.

Never use `semantic_search` when CCE is available — `context_search` replaces it.

Key tools: `context_search` (explore), `expand_chunk` (full body), `record_decision` (design choice), `session_recall` (session start), `reindex` (new file). See `procedures/cce-usage.md` for all 9 tools and examples.

## Common Mistakes

| Mistake | Fix |
|---|---|
| `read_file` for exploration | `context_search` first; `read_file` only for edits |
| `semantic_search` when CCE loaded | `context_search` replaces it |
| `expand_chunk` fails → `read_file` | For info queries, answer from partial chunks |
| `file_search`/`list_dir` after `context_search` | CCE indexes full tree |
| No `reindex` after creating file | `reindex <file>` immediately |

## Subagent Usage

Subagents need `context-engine/*` in their frontmatter `tools:` list. The server name must match the key in `.mcp.json` exactly — `context-engin/*` (missing trailing `e`) silently fails with "Unknown tool" warning.

Each agent JD's Session Discipline must instruct: `tool_search('code context engine MCP')` → `session_recall` → `context_search` for discovery.