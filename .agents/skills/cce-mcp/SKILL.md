---
name: cce-mcp
description: Use when an AI agent is about to read source files or docs/ company memory for discovery, starting a new session on multi-phase work that needs context persistence, or creating a new file that subsequent queries should discover.
---

# Code Context Engine MCP

## Overview

CCE is a local MCP server that indexes the project so the agent searches instead of reading
entire files. Benchmarked at 94% input-token savings on Python codebases. Also indexes
Markdown, YAML, JSON, and all other text files via line-based fallback chunking — which
means `docs/` company memory (ADRs, research, strategy, knowledge docs) is fully searchable.

## Boundary Contract

### Inputs
- A project workspace to index
- An AI agent that supports MCP (GitHub Copilot, Claude Code, Cursor, Gemini CLI, Codex)

### Outputs
- Indexed codebase accessible via 9 MCP tools
- Token savings tracked via `cce savings`

### Out of Scope
- Terminal-output compression (use `rtk` — see `rtk.instructions.md`)
- General MCP server configuration unrelated to CCE

## When to Use

**Decision tree — follow before calling `read_file`:**

1. **Am I discovering or exploring?** (finding a function, pattern, or doc I haven't read yet)
   → Use `context_search`. Do NOT open files to browse.

2. **Do I know the exact file and need its full content for editing?**
   → Use `read_file` directly.

3. **Do I need a specific function or section from a known file?**
   → Use `context_search` to locate it, then `expand_chunk` for the full body.

**Additional triggers:**
- Starting a new session on multi-phase work → `session_recall` to reload prior decisions
- Just created a new file → `reindex` immediately
- Searching `docs/` company memory (ADRs, research, strategy, knowledge) → `context_search`

**Do not use when:**
- Compressing terminal output — use `rtk` instead
- Querying external knowledge (ebooks, PDFs, standards not authored by us) — use NotebookLM via `redline-research`

**Docs vs Code:**
`context_search` and `session_recall` work for both code and `docs/`. The graph walk
(`related_context`) follows CALLS/IMPORTS edges — code only, not useful on Markdown.

## Core Pattern / Quick Reference

### MCP Tools

| Tool | Purpose | When to call |
|---|---|---|
| `context_search` | Hybrid vector + BM25 search | Instead of reading a full file to find a function or pattern |
| `expand_chunk` | Full source for a single compressed result | When a chunk is truncated and you need the full body |
| `related_context` | Graph walk — follows CALLS/IMPORTS edges | When you need callers or dependencies of a found chunk |
| `record_decision` | Persist an architectural decision to SQLite | After resolving a non-obvious design choice |
| `session_recall` | Retrieve past decisions by keyword | At session start to reload relevant context |
| `record_code_area` | the Product Manager which files were worked on | After each work session |
| `index_status` | Check index freshness | Before a file-heavy task |
| `reindex` | Re-index a file or the full project | After adding a new file |
| `set_output_compression` | Adjust response verbosity (`off / lite / standard / max`) | When output tokens are the bottleneck |

### Search instead of read · Cross-session memory · Keep index current

```
# Code: instead of read_file to understand a pattern:
context_search "banned words hook argparse main return int"

# Docs: instead of reading every file to find relevant context:
context_search "hook enforcement ADR pre-commit"
context_search "skeleton generator acceptance criteria"

# End of phase — persist the canonical pattern:
record_decision "hook structure: module docstring + ADR ref + argparse + find_violations() + main()->int"

# Start of next session:
session_recall "hook structure pattern"

# Immediately after creating a new file:
reindex hooks/check-no-argparse.py
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| `read_file` to understand a pattern | Use `context_search` first; fall back to `expand_chunk` only for the full body |
| Reading every `docs/research/` file to find relevant context | Use `context_search` across docs/ instead |
| Using `grep_search` for semantic queries | Use `context_search` which combines vector + BM25; reserve `grep_search` for exact literal matches only |
| Using `related_context` on Markdown docs | It follows CALLS/IMPORTS edges — code only; skip for docs |
| Querying NotebookLM for company-authored `docs/` content | NotebookLM is for external knowledge (ebooks, PDFs, standards); use CCE for `docs/` |
| No `record_decision` after phase 1 | Record the canonical pattern before ending the phase |
| No `reindex` after file creation | Call `reindex <file>` immediately after creation |
| Skipping `session_recall` at session start | Always call `session_recall` at the start of multi-phase work |

## Installation

```bash
rtk uv tool install "code-context-engine[local]"
cce init --agent copilot   # or: claude | all
# Restart editor after init. Index builds automatically.
```

## Savings Tracking

```bash
cce savings        # Current project
cce savings --all  # All projects
```
