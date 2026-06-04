---
name: mcp-notebooklm
description: Use when setting up, configuring, or troubleshooting the NotebookLM MCP server in VS Code — covers installation, authentication, allowed/forbidden tools, and MCP config.
---

## Boundary Contract


See `procedures/notebooklm-mcp.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Duplicating the MCP server config in both user-level and workspace-level mcp.json | Configure only at the user level (%APPDATA%\Code\User\mcp.json); workspace config causes conflicts |
| Skipping 
lm login --check when queries fail | Always verify auth status before debugging MCP connectivity — expired tokens are the most common cause |
| Using a forbidden tool from the list | Only the 10 allowed tools may be used; all other 25 MCP tools are out of scope for this server |