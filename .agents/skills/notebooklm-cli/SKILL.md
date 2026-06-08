---
name: notebooklm-cli
description: Use when setting up, authenticating, or troubleshooting NotebookLM access via the nlm CLI — covers installation, login, available commands, and diagnostics. CLI-only; no MCP server.
---

## Boundary Contract


See `procedures/notebooklm-cli.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Reaching for an MCP tool | There is no NotebookLM MCP server — all access is via the `nlm` CLI (CLI-first, per ADR-016) |
| Skipping `nlm login --check` when queries fail | Always verify auth status first — expired cookies (2-4 week lifetime) are the most common cause |
| Guessing command flags | Confirm with `nlm <command> --help`; the published docs can lag the installed binary |