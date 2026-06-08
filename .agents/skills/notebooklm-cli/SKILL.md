---
name: notebooklm-cli
description: Use when setting up, authenticating, or troubleshooting NotebookLM access via the nlm CLI — covers installation, login, available commands, and diagnostics. CLI-only; no MCP server.
---

## Boundary Contract

All NotebookLM access in this project is via the `nlm` CLI. There is no MCP server (removed per ADR-016, CLI-first policy). Do not search the web for `nlm` syntax — the complete command reference is below.

See `procedures/notebooklm-cli.md` for extended reference including notebook registration (Steps R1–R4), the post-source-change rule, and troubleshooting.

## Quick-Start (do this before anything else)

```powershell
# 1. Verify installation
nlm --version

# 2. Verify authentication (cookies expire every 2-4 weeks)
nlm login --check

# 3. List notebooks and find IDs
nlm notebook list --json

# 4. Query a notebook
nlm notebook query <notebook_id> "<your question>"
```

If `nlm` is not installed: `rtk uv tool install notebooklm-mcp-cli`
If not authenticated: run `nlm login` (opens browser), sign in with Google, then re-run `nlm login --check`.

## Command Reference

| Command | Purpose |
|---|---|
| `nlm notebook query <id> "<question>"` | Query a notebook — primary use case. Scope with `--source-ids <id,id>`. Add `--json` for parseable output. |
| `nlm notebook list --json` | List all notebooks (find notebook IDs) |
| `nlm notebook get <id>` | Get notebook details and source list |
| `nlm notebook describe <id>` | AI-generated summary and suggested topics |
| `nlm source list <notebook>` | List sources in a notebook |
| `nlm source describe <source-id>` | AI-generated per-source summary and keywords |
| `nlm notebook create "<title>"` | Create a notebook — **Knowledge Operator only** |
| `nlm source add <notebook> --url/--text/--file/--youtube/--drive` | Add a source — **Knowledge Operator only**. Verified types: PDF, TXT, audio (MP3/M4A/WAV), video (MP4) |
| `nlm source delete <source-id> --confirm` | Remove a source — **Knowledge Operator only** |
| `nlm source rename <source-id> "<name>"` | Rename a source — **Knowledge Operator only** |
| `nlm source stale <notebook>` / `nlm source sync <notebook> --confirm` | List / refresh stale Drive-linked sources |
| `nlm login --check` | Verify auth status |
| `nlm login` | Authenticate (opens browser) |
| `nlm doctor` | Version, auth, and config diagnostics |

> Use `--json` on read commands when parsing output programmatically.
> `create`, `add`, `delete`, `rename`, and `sync` are restricted to the Knowledge Operator.

## Notebook IDs

Notebook IDs are not human-readable strings. Always run `nlm notebook list --json` first and match by name. The canonical notebook register is `.agents/skills/redline-research/register.json`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Reaching for an MCP tool or web search | There is no NotebookLM MCP server — all access is via the `nlm` CLI (CLI-first, per ADR-016). CLI commands are in this file. |
| Skipping `nlm login --check` when queries fail | Always verify auth status first — expired cookies (2-4 week lifetime) are the most common failure cause |
| Guessing command flags | Confirm with `nlm <command> --help`; the published docs can lag the installed binary |
| Hardcoding a notebook ID | IDs change between accounts. Resolve via `nlm notebook list --json` or `register.json`. |
