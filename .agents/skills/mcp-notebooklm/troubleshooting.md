# NotebookLM MCP Troubleshooting

Known failure modes for the `notebooklm-mcp-cli` MCP server on Windows.
Organised by symptom for fast lookup.

## Chrome / Edge detection

| Symptom | Cause | Fix |
|---------|-------|-----|
| `nlm doctor` reports `Chrome: not found` | Chrome installed at user level (`%LOCALAPPDATA%\...`); `nlm` only scans system-level paths | `nlm config set auth.browser edge` |
| `nlm login` fails with browser not found | Same as above | Same as above |

Edge is always present on Windows at
`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`.

## Authentication

| Symptom | Cause | Fix |
| --- | --- | --- |
| MCP tools return `"No authentication found"` | CLI auth (`nlm login`) not completed | Run `nlm login` in a terminal |
| Tool returns `status: error`, `error_reason: "expired"` | Auth cookies fully expired | Re-run `nlm login` |
| Tool returns `status: error`, `error_reason: "stale_heuristic"` | Cookies likely expired based on age heuristic | Re-run `nlm login` |
| Tool returns `status: error`, `error_reason: "no_tokens"` | No credentials stored at all | Run `nlm login` (first-time setup) |
| Queries fail after weeks of working | Auth cookies expired (2-4 week lifetime) | Re-run `nlm login` |

Cookies are stored locally at `~/.notebooklm-mcp-cli/`. Never commit them.
Since v0.6.14, a running MCP server watches auth files on disk — re-running `nlm login` takes effect immediately without restarting the server.

## Server & CLI

| Symptom | Cause | Fix |
|---------|-------|-----|
| `notebooklm-mcp --version` hangs | That executable is the MCP server (stdio mode); it does not support `--version` | Use `nlm --version` instead |
| General diagnostics needed | -- | Run `nlm doctor` |

## Claude Code configuration

| Symptom | Cause | Fix |
| --- | --- | --- |
| Server not listed in Claude Code MCP tools | `.mcp.json` entry missing or not reloaded | Add `"notebooklm-mcp"` entry to `.mcp.json` at repo root; restart Claude Code or use `/mcp` to reconnect |
| Env vars set in terminal have no effect | MCP server is a child of Claude Code, not the shell | Set env vars in the `"env"` block inside `.mcp.json` |
