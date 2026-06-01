# CCE MCP: Usage Examples, Installation & Savings

## Code Examples

```bash
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

## All 9 MCP Tools

| Tool | Purpose | When to call |
|---|---|---|
| `context_search` | Hybrid vector + BM25 search | Instead of reading a full file to find a function or pattern |
| `expand_chunk` | Full source for a single compressed result | When a chunk is truncated and you need the full body |
| `related_context` | Graph walk — follows CALLS/IMPORTS edges | When you need callers or dependencies of a found chunk |
| `record_decision` | Persist an architectural decision to SQLite | After resolving a non-obvious design choice |
| `session_recall` | Retrieve past decisions by keyword | At session start to reload relevant context |
| `record_code_area` | Mark which files were worked on | After each work session | <!-- hook: allow -->
| `index_status` | Check index freshness | Before a file-heavy task |
| `reindex` | Re-index a file or the full project | After adding a new file |
| `set_output_compression` | Adjust response verbosity (`off / lite / standard / max`) | When output tokens are the bottleneck |

## Docs vs Code

`context_search` and `session_recall` work for both code and `docs/`. The graph walk (`related_context`) follows CALLS/IMPORTS edges — code only, not useful on Markdown.

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
