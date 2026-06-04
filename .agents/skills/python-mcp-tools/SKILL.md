---
name: python-mcp-tools
description: Use when calling MCP tools or servers from Python code in this repo
paths: "src/**/*.py,tests/**/*.py"
---

# Python MCP Tools

This skill describes how to work with MCP-related tooling in this repo.

## Boundary Contract

### Applies To
- MCP server and tool implementations under `src/`

### Produces
- Code following repo conventions for MCP tool registration and usage

### Does Not Cover
- General style (`python-style`)
- Class design (`python-class-design`)
- NotebookLM MCP setup (`notebooklm-mcp`)

## Context & Guidelines

### Scope

Apply these rules when working on MCP servers, transports, or integrations.

### Core Rules

- Prefer minimal, explicit interfaces.
- Keep error handling at boundaries (API layer) where possible.
- Preserve existing transport/security constraints.

## Procedure

1. Identify the MCP entrypoint and transport used.
2. Implement changes with clear request/response structures.
3. Add/adjust tests where appropriate.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Calling a deferred MCP tool without loading it first via 	ool_search | Always run 	ool_search for the capability before invoking a deferred tool |
| Passing a workspace-relative path where an absolute URI is expected | Use absolute paths with the ile:// scheme or the tool's documented path format |
| Ignoring an MCP tool error and retrying with the same arguments | Change the argument (e.g. use absolute path, fix a missing field) before retrying |