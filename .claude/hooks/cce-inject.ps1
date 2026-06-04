<#
.SYNOPSIS
    SubagentStart hook: injects CCE workspace context into subagent conversations.

.DESCRIPTION
    Calls `cce sessions export` to load recent decisions and returns them as
    additionalContext JSON so subagents start pre-loaded with workspace state.
    This is a Swiss Cheese defence layer — deterministic code enforcement
    complementing advisory JD text constraints.

.NOTES
    Hook input: JSON via stdin (hookEventName, agent_id, agent_type, etc.)
    Hook output: JSON via stdout with hookSpecificOutput.additionalContext
    Exit 0 = success, exit 2 = blocking error.
#>
$ErrorActionPreference = 'Stop'

# Read hook input from stdin
$input_json = [Console]::In.ReadToEnd()

try {
    # Export recent decisions from CCE session memory (last 7 days)
    $since = (Get-Date).AddDays(-7).ToString('yyyy-MM-dd')
    $decisions = & cce sessions export --since $since --format markdown 2>$null

    if (-not $decisions) {
        $decisions = "No recent CCE session decisions found."
    }

    # Truncate to avoid blowing the context window
    if ($decisions.Length -gt 4000) {
        $decisions = $decisions.Substring(0, 4000) + "`n... (truncated)"
    }

    $context = @"
[CCE Session Context - Auto-injected by SubagentStart hook]

## MANDATORY TOOL LOADING — DO THIS FIRST

You have deferred MCP tools from the 'context-engine' server that are NOT yet loaded.
They will NOT appear in your tool list until you load them.

Step 1: Call the tool literally named "tool_search" with query "context engine MCP session recall"
        — this is NOT semantic_search. tool_search is a SEPARATE tool that loads deferred tools.
Step 2: After tool_search returns tool names, call "mcp_context-engin_session_recall" with topic relevant to user request.
Step 3: Use "mcp_context-engin_context_search" for workspace discovery instead of read_file/semantic_search/list_dir.

WARNING: "semantic_search" searches FILE CONTENTS — it cannot access CCE memory.
         "tool_search" LOADS DEFERRED TOOLS — it makes new tools callable. They are different tools.

DO NOT use semantic_search, read_file, or list_dir for workspace exploration.
DO NOT skip tool_search — CCE tools are invisible until loaded.
DO NOT read files that CCE already returned chunks for — apply the Stop Rule: if CCE output answers the question, respond directly.

## STOP RULE

After context_search returns results, check: do the chunks answer the user's question?
- YES → respond directly. Do NOT follow up with read_file, file_search, or list_dir.
- NO (status/priority question) → answer from partial chunks. Do not fall back to read_file.
- NO (writing an artifact like PRD/hypothesis) → use expand_chunk first, then read_file only if expand_chunk fails.

## INFORMATION QUERY BUDGET

For status checks, weekly priorities, and "what should we focus on" questions:
Use at most 1 session_recall + 1 context_search, then respond.
Do NOT expand scope by reading individual spec/task/plan files.

## Recent CCE Decisions
$decisions
"@

    $output = @{
        hookSpecificOutput = @{
            hookEventName = "SubagentStart"
            additionalContext = $context
        }
    } | ConvertTo-Json -Depth 3

    Write-Output $output
    exit 0
}
catch {
    # Non-blocking: warn but don't stop the subagent
    Write-Error "CCE inject hook failed: $_"
    exit 1
}
