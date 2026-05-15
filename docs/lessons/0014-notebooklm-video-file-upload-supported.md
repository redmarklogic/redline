# 0014 — NotebookLM source_add accepts video (MP4) files

**Date**: 2026-05-14

**Skill**: `notebooklm-mcp` (link: `.agents/skills/notebooklm-mcp/SKILL.md`)

**Context**: User asked to upload 12 MP4 video part files to a new NotebookLM notebook
("Webinar - Insurance for Consulting Engineers") after splitting a 1.2 GB screen recording.

**Observation**: Agent refused to attempt the upload, citing the MCP tool's description
text — `"Local file upload (PDF, text, audio)"` — and concluded that MP4 was unsupported.
The user then manually uploaded the same files successfully via the NotebookLM web UI,
proving the assumption wrong.

**Root Cause**: The agent treated the tool's description string as an exhaustive allow-list
rather than as a summary. Tool descriptions written by third parties are often incomplete;
they document common cases, not all supported cases.

**Principle**: Never refuse a file operation based on tool description text alone. When in
doubt, attempt the operation and let the system reject it. Silence in documentation is not
prohibition.

**Source**: Conversation on 2026-05-14; notebook at
`https://notebooklm.google.com/notebook/12dc5e06-4f77-4577-abca-758017e26675`.
