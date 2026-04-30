# Forbidden Tools Reference

The `notebooklm-mcp-cli` MCP server exposes 35 tools. **Only the tools listed in
Allowed Tools in [SKILL.md](SKILL.md) may be called.** All others listed below are
forbidden to prevent context-window pollution and unintended side effects.

## Context-pollution risk

These return massive, unbounded responses:

| Tool | Why forbidden |
|------|---------------|
| `cross_notebook_query` | Aggregates responses from multiple notebooks; can return tens of thousands of tokens |
| `batch` | Batch operations across notebooks; `action="query"` queries all matching notebooks at once |
| `source_get_content` | Dumps raw source text; a single source can be megabytes |
| `pipeline` | Multi-step automated workflows generating unbounded output |
| `research_start` / `research_status` / `research_import` | Web/Drive research importing unbounded content |

## Out-of-scope

These create, modify, or delete resources without explicit user intent:

| Tool | Why forbidden |
|------|---------------|
| `notebook_create` / `notebook_delete` / `notebook_rename` | Destructive notebook management |
| `source_add` / `source_delete` / `source_list_drive` / `source_sync_drive` / `source_rename` | Source management |
| `studio_create` / `studio_status` / `studio_delete` / `studio_revise` | Content generation (audio, video, reports) |
| `download_artifact` / `export_artifact` | File downloads and exports |
| `notebook_share_status` / `notebook_share_public` / `notebook_share_invite` / `notebook_share_batch` | Sharing management |
| `note` | Note management inside notebooks |
| `chat_configure` | Changes chat settings |
| `save_auth_tokens` | Fallback auth (use `nlm login` CLI instead) |
| `tag` | Notebook tagging (manage tags via CLI instead) |
| `notebook_query_start` / `notebook_query_status` | Async query variants (use `notebook_query` instead) |
