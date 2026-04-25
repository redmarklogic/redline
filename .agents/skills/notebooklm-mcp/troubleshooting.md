# NotebookLM MCP Troubleshooting

Running log of issues encountered and fixes applied during setup and usage of
the `notebooklm-mcp-cli` MCP server.

---

## 2026-04-25: Initial setup — Chrome not found

**Symptom**: `nlm doctor` reports `Chrome: not found` on Windows even though
Chrome is installed.

**Root cause**: Chrome was installed at the **user level**
(`%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe`), not the system level
(`C:\Program Files\Google\Chrome\Application\chrome.exe`). The `nlm doctor`
check only scans system-level paths.

**Fix**: Configured Edge as the auth browser instead:

```powershell
nlm config set auth.browser edge
```

Edge is always available on Windows at
`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`.

**Alternative**: Could also point nlm at the user-level Chrome install, but
using Edge avoids the path detection issue entirely.

---

## 2026-04-25: Tool names differ from MCP_GUIDE.md

**Symptom**: The skill originally documented tools as `notebook_query`,
`notebook_list`, etc. But in VS Code, the MCP tools are prefixed by the server
name from `mcp.json`, resulting in `mcp_notebooklm_notebook_query`,
`mcp_notebooklm_notebook_list`, etc.

**Root cause**: VS Code automatically prefixes MCP tool names with
`mcp_{server_name}_` where `server_name` comes from the key in `mcp.json`.
Our server is keyed as `"notebooklm"`, so all tools get the
`mcp_notebooklm_` prefix.

**Fix**: The skill documents the **base** tool names (e.g., `notebook_query`)
which is the correct convention — skills should be agnostic of the VS Code
prefix. Agents calling tools use the prefixed form automatically.

---

## 2026-04-25: `notebooklm-mcp --version` hangs

**Symptom**: Running `notebooklm-mcp --version` in the terminal hangs
indefinitely.

**Root cause**: The `notebooklm-mcp` executable is the MCP server, which runs
in stdio mode waiting for JSON-RPC input. It does not support `--version`.
Use `nlm --version` instead (the CLI companion).

**Fix**: Use `nlm --version` to check the installed version. Use `nlm doctor`
for full diagnostics.

---

## 2026-04-25: Auth required before any MCP tool call

**Symptom**: All MCP tool calls (`notebook_list`, `notebook_query`, etc.)
return `"No authentication found"` error.

**Root cause**: The `notebooklm-mcp-cli` package requires CLI-based
authentication (`nlm login`) before the MCP server can function. Unlike the
old `PleasePrompto/notebooklm-mcp` which had in-MCP auth tools
(`setup_auth`, `re_auth`), the new server delegates auth entirely to the CLI.

**Fix**: Run `nlm login` in a terminal. This opens a browser window for
Google sign-in and saves cookies locally at `~/.notebooklm-mcp-cli/`.

---

## 2026-04-25: Workspace mcp.json conflicts with user-level config

**Symptom**: Created `.vscode/mcp.json` in the workspace, but the user-level
config at `%APPDATA%\Code\User\mcp.json` already had a `notebooklm` server
entry.

**Root cause**: Both files define a server with the same key (`notebooklm`).
VS Code may load both, causing conflicts or duplicate tool registrations.

**Fix**: The user-level config is authoritative (it has the `NOTEBOOKLM_QUERY_TIMEOUT`
env var set). The workspace-level `.vscode/mcp.json` should either be removed
or should NOT duplicate the `notebooklm` entry. If the workspace file exists
for other project-specific MCP servers, keep it but omit the `notebooklm` key.

**Action taken**: Removed the `notebooklm` entry from workspace-level mcp.json
since user-level config handles it.

---

## 2026-04-25: Auth browser fallback to Edge

**Symptom**: `nlm login` fails because Chrome is not detected at the system level.

**Fix**: Configure Edge as the auth browser:

```powershell
nlm config set auth.browser edge
```

Then run `nlm login` — Edge opens for Google sign-in.

---

## 2026-04-25: Successful test-drive query

**Verification**: After auth setup, a medium-complexity query against the
"Software Architecture & DDD" notebook returned a well-structured answer with
21 citations across 4 sources, including a `conversation_id` for follow-ups.

**Tools used**: `mcp_notebooklm_notebook_list` (to find notebook IDs) then
`mcp_notebooklm_notebook_query` (the actual query). Both worked on first attempt.

**VS Code tool naming**: The MCP tools appear in VS Code with the prefix
`mcp_notebooklm_` (derived from the server key `"notebooklm"` in mcp.json).
The base names from the MCP_GUIDE.md (`notebook_query`, `notebook_list`) get
this prefix automatically.
