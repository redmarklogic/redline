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

IMPORTANT: You have CCE (Code Context Engine) tools available via context-engine/*.
For ANY workspace exploration or discovery, use context_search — NOT read_file, semantic_search, or list_dir.
read_file is ONLY for targeted edits when you already know the exact file path.

To load CCE tools: call tool_search('code context engine MCP') first.
Then call session_recall to load prior decisions.

Recent decisions and session context:
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
