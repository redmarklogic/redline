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
|---------|-------|-----|
| MCP tools return `"No authentication found"` | CLI auth (`nlm login`) not completed | Run `nlm login` in a terminal |
| Queries fail after weeks of working | Auth cookies expired (2-4 week lifetime) | Re-run `nlm login` |

Cookies are stored locally at `~/.notebooklm-mcp-cli/`. Never commit them.

## Server & CLI

| Symptom | Cause | Fix |
|---------|-------|-----|
| `notebooklm-mcp --version` hangs | That executable is the MCP server (stdio mode); it does not support `--version` | Use `nlm --version` instead |
| General diagnostics needed | -- | Run `nlm doctor` |

## VS Code configuration

| Symptom | Cause | Fix |
|---------|-------|-----|
| Server not listed in Copilot tools | MCP config missing or not reloaded | Add entry to `%APPDATA%\Code\User\mcp.json`; reload VS Code window |
| Duplicate tool registrations or conflicts | Both workspace `.vscode/mcp.json` and user-level `mcp.json` define `"notebooklm"` | Keep the entry in **user-level** config only; remove from workspace config |
| Env vars set in terminal have no effect | MCP server is a child of VS Code, not the shell | Set env vars in the `"env"` block of `mcp.json` |
