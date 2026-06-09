<#
.SYNOPSIS
    PreToolUse hook: gates codebase-exploration tools on CCE engine health.

.DESCRIPTION
    Deterministic Swiss-Cheese layer enforcing the AGENTS.md mandate that CCE
    must be available before the agent explores the codebase. On a gated tool
    call it verifies the Code Context Engine is usable (binary resolvable +
    `cce status` exits 0).

    Anti-wedge design (a flaky/locked engine must never block the whole session):
    - Tools that do not consume CCE -- mutations and the human-escalation valve
      (Write/Edit/MultiEdit/NotebookEdit/TodoWrite/ExitPlanMode/AskUserQuestion)
      -- are ALWAYS allowed.
    - A failed health check escalates to `ask` (the user decides), never a hard
      `deny`, and is retried once because `cce status` is not safe under the
      concurrent invocation that parallel tool calls produce.
    - Only a positive `ok` verdict is ever cached (10 min). A failure is NEVER
      persisted, so a transient blip cannot poison subsequent calls.
    - The `ok` flag is written atomically (temp + move) so concurrent hook
      processes never read a half-written file.

    Escape hatch: repair/diagnostic commands (containing 'cce', 'setup-cce', or
    'mcp') are always allowed so the engine can be fixed from inside a session.

    Limitation: this checks the LOCAL engine/index health. It cannot observe
    whether the MCP server is connected inside the Claude session -- that is
    handled structurally by `enabledMcpjsonServers` in .claude/settings.json.

.NOTES
    Hook input  : JSON via stdin (hook_event_name, tool_name, tool_input, ...)
    Hook output : exit 0 with no output = allow; exit 0 with permissionDecision
                  JSON = deny/ask. Never exit 2 here (keep failures non-fatal).
    Doc: https://code.claude.com/docs/en/hooks (PreToolUse Decision Control)
#>
$ErrorActionPreference = 'Stop'

function Allow { exit 0 }  # no stdout => tool proceeds under normal permissions

function Decide([string]$decision, [string]$reason) {
    $out = @{
        hookSpecificOutput = @{
            hookEventName            = "PreToolUse"
            permissionDecision       = $decision
            permissionDecisionReason = $reason
        }
    } | ConvertTo-Json -Depth 4 -Compress
    Write-Output $out
    exit 0
}

# Tools that never touch CCE: mutations + the human-escalation valve. Gating
# these buys nothing, and a gated AskUserQuestion would remove the only way to
# recover from a wedged session.
$UNGATED = '^(Write|Edit|MultiEdit|NotebookEdit|TodoWrite|ExitPlanMode|AskUserQuestion)$'

try {
    $raw = [Console]::In.ReadToEnd()
    $evt = $null
    if ($raw) { try { $evt = $raw | ConvertFrom-Json } catch { } }

    # Never gate tools that do not consume CCE.
    if ($evt.tool_name -match $UNGATED) { Allow }

    # Escape hatch: let repair/diagnostic commands through so a gated session
    # can fix CCE itself.
    $cmdText = ""
    if ($evt.tool_input) {
        $cmdText = "$($evt.tool_input.command) $($evt.tool_input.file_path) $($evt.tool_input.description)"
    }
    if ($cmdText -match '(?i)\b(cce|setup-cce|mcp)\b') { Allow }

    # Positive-only cache: a fresh 'ok' verdict (10 min) short-circuits. A failed
    # verdict is NEVER cached, so a transient blip cannot poison later calls.
    # Scoped PER PROJECT so multiple clones never share a verdict; key off
    # CLAUDE_PROJECT_DIR (set by Claude Code for hook subprocesses).
    $projDir = $env:CLAUDE_PROJECT_DIR
    if (-not $projDir) { $projDir = (Get-Location).Path }
    $projKey = ([System.BitConverter]::ToString(
        [System.Security.Cryptography.MD5]::Create().ComputeHash(
            [System.Text.Encoding]::UTF8.GetBytes($projDir.ToLowerInvariant())))
        ).Replace('-', '').Substring(0, 12)
    $flag = Join-Path $env:TEMP "cce-health-$($env:USERNAME)-$projKey.flag"
    if (Test-Path $flag) {
        $age = (Get-Date) - (Get-Item $flag).LastWriteTime
        if ($age.TotalMinutes -lt 10 -and (Get-Content $flag -Raw).Trim() -eq 'ok') { Allow }
    }

    # Fresh health check.
    $cce = (Get-Command cce -ErrorAction SilentlyContinue).Source
    if (-not $cce) { $cce = Join-Path $env:USERPROFILE ".local\bin\cce.exe" }
    if (-not (Test-Path $cce)) {
        Decide 'ask' "CCE health check: 'cce' binary not found. Run tasks\setup-cce.ps1 to install the Code Context Engine, then approve to proceed."
    }

    # `cce status` is not safe under the concurrent invocation that parallel tool
    # calls produce -- retry once before escalating.
    & $cce status *> $null
    if ($LASTEXITCODE -ne 0) {
        Start-Sleep -Milliseconds 250
        & $cce status *> $null
    }
    if ($LASTEXITCODE -ne 0) {
        # Escalate to the user; do NOT cache a 'bad' verdict (no poison).
        Decide 'ask' "CCE health check failed (exit $LASTEXITCODE): the Code Context Engine is down or busy. Run tasks\setup-cce.ps1 or 'cce index' to repair, or approve to proceed."
    }

    # Cache the positive verdict atomically so concurrent readers never see a
    # half-written file.
    $tmp = "$flag.$PID.tmp"
    Set-Content -Path $tmp -Value 'ok'
    Move-Item -Path $tmp -Destination $flag -Force
    Allow
}
catch {
    # Fail OPEN: a broken gate must never wedge the whole session. Surface the
    # error to stderr (visible to the user) but allow the tool.
    Write-Error "cce-health-gate hook error (failing open): $_"
    exit 0
}
