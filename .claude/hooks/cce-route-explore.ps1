<#
.SYNOPSIS
    Routing hook: steer codebase exploration through CCE context_search.
    Wired to UserPromptSubmit (primary - lands BEFORE the model plans) and
    PreToolUse Grep|Glob (fallback reminder if the first prompt needed none).

.DESCRIPTION
    CCE MCP tools are deferred — they are invisible until loaded via
    ToolSearch, so the model defaults to Grep/Glob and the index never gets
    used. This injects the exact loading incantation and routing rule as
    additionalContext, once per session (flag file keyed by session_id);
    every later invocation is a fast flag check.

    Never blocks: additionalContext only, exit 0 on every path.
#>
$ErrorActionPreference = 'Stop'

try {
    $raw = [Console]::In.ReadToEnd()
    $evt = $null
    if ($raw) { try { $evt = $raw | ConvertFrom-Json } catch { } }

    $sid = if ($evt -and $evt.session_id) { $evt.session_id } else { 'unknown' }
    $evtName = if ($evt -and $evt.hook_event_name) { $evt.hook_event_name } else { 'UserPromptSubmit' }
    $flag = Join-Path $env:TEMP "cce-route-$sid.flag"
    if (Test-Path $flag) { exit 0 }
    Set-Content -Path $flag -Value '1'

    $ctx = @"
CCE routing rule for this project: an indexed Code Context Engine answers questions about this codebase in ~300 tokens instead of multi-file Glob/Grep/Read sweeps. For ANY question about where/how something is configured, defined, or works in this repo, your FIRST exploration step is:
1. Load the deferred tools once: ToolSearch query "select:mcp__context-engine__context_search,mcp__context-engine__session_recall,mcp__context-engine__expand_chunk"
2. Call mcp__context-engine__context_search with the question.
3. If the chunks answer it, respond directly - do not re-read the files. Use mcp__context-engine__expand_chunk for a full section.
Grep/Glob remain correct for exact strings, symbol definitions, and already-known paths. Read remains correct for files you are about to edit.
"@

    @{ hookSpecificOutput = @{
            hookEventName     = $evtName
            additionalContext = $ctx
        } } | ConvertTo-Json -Depth 4 -Compress | Write-Output
    exit 0
}
catch {
    exit 0  # fail open, never block exploration
}
