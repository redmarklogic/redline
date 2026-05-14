---
name: notebooklm-mcp
description: Use when setting up, configuring, or troubleshooting the NotebookLM MCP server in VS Code — covers installation, authentication, allowed/forbidden tools, and MCP config.
---

# NotebookLM MCP

How to connect GitHub Copilot (Agent mode) to Google NotebookLM via the
[`notebooklm-mcp-cli`](https://github.com/jacob-bd/notebooklm-mcp-cli) MCP server.

## Boundary Contract

### Inputs
- VS Code environment requiring NotebookLM access

### Outputs
- Configured, authenticated MCP connection to NotebookLM

### Out of Scope
- Query writing and prompt design (`rag-prompting`)
- Research workflow orchestration (`redline-research`)
- Notebook registry (`.agents/skills/redline-research/register.json`)

## Allowed Tools

| Tool | Purpose |
|------|---------|
| `notebook_query` | Query a notebook (primary use case) |
| `notebook_list` | List all notebooks (find notebook IDs) |
| `notebook_get` | Get notebook details and sources |
| `notebook_describe` | Get AI-generated notebook summary and suggested topics |
| `source_describe` | Get AI-generated per-source summary and keywords |
| `source_add` | Upload a new source to a notebook — **Linda only** (library ingestion workflow). Verified file types: PDF, TXT, audio (MP3/M4A/WAV), **video (MP4)** |
| `source_delete` | Remove a source from a notebook — **Linda only** (deduplication / file hygiene) |
| `source_rename` | Rename a source in a notebook — **Linda only** (canonical naming enforcement) |
| `refresh_auth` | Refresh auth tokens when expired |
| `server_info` | Check version and diagnostics |

### File Upload Rule

> **Never refuse a file upload based on assumed format limitations.**
> The `source_add` `file` type accepts at minimum: PDF, TXT, audio, and **video (MP4)**.
> When asked to upload any file, attempt the upload and let NotebookLM reject it if
> the format is truly unsupported. Do not pre-emptively block the user.

All other tools (27 of 35) are **forbidden**. See
[`forbidden-tools.md`](forbidden-tools.md) for the full list and rationale.

## Post-Source-Change Rule (mandatory)

After **any** operation that adds, removes, or renames a source in a notebook
(`source_add`, `source_delete`, `source_rename`), Linda **must** update
`G:\My Drive\Library\index-notebooklm.xlsx` before the task is considered done.

Trigger: load the `notebooklm-index` skill and run the **single-notebook upsert**
for the affected notebook using its UUID. Do not run a full sync — upsert only the
notebook that changed.

This rule applies even when the source operation was part of a larger task
(e.g. library ingestion). The index update is the final step, not optional.

## Procedure

### Step 1 — Install

Check whether `nlm` is available:

```powershell
nlm --version
```

If not installed:

```powershell
uv tool install notebooklm-mcp-cli
```

This installs two executables: `nlm` (CLI) and `notebooklm-mcp` (MCP server).

### Step 2 — Configure VS Code

The server is configured at the **user level** in
`%APPDATA%\Code\User\mcp.json` (not workspace-level `.vscode/mcp.json`):

```json
{
  "servers": {
    "notebooklm": {
      "command": "notebooklm-mcp",
      "type": "stdio",
      "env": {
        "NOTEBOOKLM_QUERY_TIMEOUT": "300"
      }
    }
  }
}
```

If missing, add it and reload the VS Code window (**Developer: Reload Window**).
Do **not** duplicate in workspace-level `.vscode/mcp.json`.

### Step 3 — Authenticate

```powershell
nlm login --check
```

If not authenticated:

1. User runs `nlm login` in a terminal (opens browser).
2. User signs in to Google. Cookies saved locally (never committed to VCS).
3. Confirm: `nlm login --check` returns success.

Named profiles: `nlm login --profile work`. Diagnostics: `nlm doctor`.

### Step 4 — Query

Use `notebook_list` to find notebook IDs, then `notebook_query` to query.

**REQUIRED SUB-SKILL:** Load `rag-prompting` before writing any query.

## Troubleshooting

See [`troubleshooting.md`](troubleshooting.md) for known failure modes
and fixes (symptom-based lookup).

## Add Notebook to Register

When the user provides a NotebookLM URL and asks to add it to the register or knowledge base,
follow this four-step workflow in order. Do **not** skip steps or ask for metadata — discover
it from the notebook itself.

The canonical register is `.agents/skills/redline-research/register.json`. Every
notebook used by any skill (including `redline-research`) is listed there.

### Step R1 — Check the register

Read `.agents/skills/redline-research/register.json` and check if any entry's `url` field matches the provided URL.
Also call `notebook_list` to verify the notebook exists in the user's NotebookLM account. If
the notebook is already registered, report that it exists and stop.

### Step R2 — Find the notebook ID and query for purpose

Call `notebook_list` to find the notebook. Match by URL or name. Note the `notebook_id`.

Then call `notebook_query` with that `notebook_id`. Use the following question template:

```
Explain for the uninitiated. Define any specialist term or acronym the
first time it appears. Keep citations. Avoid ambiguity.

What is the purpose of this notebook? What topics does it cover, what
kind of knowledge or documents does it contain, and when would someone
consult it?
```

From the answer extract: an `id` (kebab-case slug), a `name`, a one-paragraph `description`,
a `topic_area` (match an existing area from `register.json` or propose a new one), a flat
`topics` list (5-10), `content_types`, and 3-5 `use_cases`. Set `access` to `"open"` unless
the user specifies otherwise (e.g. `"advisory-board-only"`).

### Step R3 — Append to `.agents/skills/redline-research/register.json`

Append a new JSON object to the array in `.agents/skills/redline-research/register.json` with all fields from Step R2 plus
`"added": "YYYY-MM-DD"`. Ensure the JSON remains valid.

### Step R4 — Confirm

Report to the user:
- Notebook name and ID assigned.
- A one-sentence purpose summary.
- Confirmation that the entry was added to `.agents/skills/redline-research/register.json`.

Do **not** ask the user to provide any metadata — derive everything from the notebook query.

## Tips

- Notebook names are case-sensitive; match names exactly when querying.
- The first query per session may take a few seconds while the server initialises.
- Authentication cookies expire every 2-4 weeks. Re-run `nlm login` when queries fail.
- Use `nlm doctor` to diagnose installation, auth, and config issues.
- Free-tier rate limit is ~50 queries/day.
- Environment variables set in a terminal have **no effect** on the MCP server — it is a
  child process of VS Code, not the shell. All env overrides must be placed in
  `%APPDATA%\Code\User\mcp.json` under the server's `"env"` block.

## References

- [notebooklm-mcp-cli GitHub repo](https://github.com/jacob-bd/notebooklm-mcp-cli)
- [MCP Guide (all 35 tools)](https://github.com/jacob-bd/notebooklm-mcp-cli/blob/main/docs/MCP_GUIDE.md)
- [Authentication guide](https://github.com/jacob-bd/notebooklm-mcp-cli/blob/main/docs/AUTHENTICATION.md)
- [CLI Guide](https://github.com/jacob-bd/notebooklm-mcp-cli/blob/main/docs/CLI_GUIDE.md)
- [VS Code MCP server configuration docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
