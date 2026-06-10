<#
.SYNOPSIS
    SubagentStart hook: injects CCE workspace context into subagent conversations.

.DESCRIPTION
    Exports recent decisions from CCE session memory and returns them as
    additionalContext, together with the exact (Claude Code) incantation for
    loading the deferred CCE MCP tools. Tool names here MUST be names that
    exist in Claude Code sessions — mcp__context-engine__* and ToolSearch —
    or the instructions are unfollowable (the pre-2026-06 version used
    VS Code Copilot names and was ignored by every subagent).

.NOTES
    Hook input: JSON via stdin (hookEventName, agent_id, agent_type, etc.)
    Hook output: JSON via stdout with hookSpecificOutput.additionalContext
#>
$ErrorActionPreference = 'Stop'

$null = [Console]::In.ReadToEnd()  # drain stdin; payload not needed

try {
    # Export recent decisions from CCE session memory (last 7 days)
    $since = (Get-Date).AddDays(-7).ToString('yyyy-MM-dd')
    $decisions = & cce sessions export --since $since --format markdown 2>$null

    if (-not $decisions) {
        $decisions = "No recent CCE session decisions found."
    }
    if ($decisions.Length -gt 4000) {
        $decisions = $decisions.Substring(0, 4000) + "`n... (truncated)"
    }

    $context = @"
[CCE Session Context - injected by SubagentStart hook]

This project has an indexed Code Context Engine (MCP server "context-engine").
Its tools are DEFERRED - load them once before exploring:

  ToolSearch query: "select:mcp__context-engine__context_search,mcp__context-engine__session_recall,mcp__context-engine__expand_chunk"

Routing rule:
- Conceptual codebase questions (where is X, how does Y work) -> mcp__context-engine__context_search FIRST, not Grep/Glob/Read sweeps.
- Exact strings, symbol definitions, known file paths -> Grep/Glob as usual.
- Editing a file -> Read it in full as usual.
- Stop rule: if context_search chunks answer the question, respond directly; use mcp__context-engine__expand_chunk for a full section; fall back to Read only if that fails.

## Recent CCE Decisions
$decisions
"@

    @{ hookSpecificOutput = @{
            hookEventName     = 'SubagentStart'
            additionalContext = $context
        } } | ConvertTo-Json -Depth 3 | Write-Output
    exit 0
}
catch {
    # Non-blocking: warn but don't stop the subagent
    Write-Error "CCE inject hook failed: $_"
    exit 1
}
