---
name: python-mcp-tools
description: Guidance for using MCP tools and servers in this repo.
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
