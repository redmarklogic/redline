<#
.SYNOPSIS
    PreToolUse hook: blocks tool execution when the CCE engine is unhealthy.

.DESCRIPTION
    Deterministic Swiss-Cheese layer enforcing the AGENTS.md mandate that CCE
    must be available before any agent does work. On every tool call it verifies
    the Code Context Engine is usable (binary resolvable + `cce status` exits 0 +
    an index exists for this project). If unhealthy, it DENIES the tool with a
    remediation message so work cannot proceed on a broken engine.

    Health is cached for 10 minutes in a per-project temp flag to keep the
    per-tool-call cost negligible.

    Escape hatch: repair/diagnostic commands (containing 'cce', 'setup-cce', or
    'mcp') are always allowed through so the engine can be fixed from inside a
    gated session.

    Limitation: this checks the LOCAL engine/index health. It cannot observe
    whether the MCP server is connected inside the Claude session — that is
    handled structurally by `enabledMcpjsonServers` in .claude/settings.json.

.NOTES
    Hook input  : JSON via stdin (hookEventName, tool_name, tool_input, ...)
    Hook output : exit 0 with no output = allow; exit 0 with permissionDecision
                  JSON = deny. Never exit 2 here (keep failures non-fatal/explicit).
    Doc: https://code.claude.com/docs/en/hooks (PreToolUse Decision Control)
#>
$ErrorActionPreference = 'Stop'

function Allow { exit 0 }  # no stdout => tool proceeds under normal permissions

function Deny([string]$reason) {
    $out = @{
        hookSpecificOutput = @{
            hookEventName          = "PreToolUse"
            permissionDecision     = "deny"
            permissionDecisionReason = $reason
        }
    } | ConvertTo-Json -Depth 4 -Compress
    Write-Output $out
    exit 0
}

try {
    $raw = [Console]::In.ReadToEnd()
    $evt = $null
    if ($raw) { try { $evt = $raw | ConvertFrom-Json } catch { } }

    # Escape hatch: let repair/diagnostic commands through so a gated session
    # can fix CCE itself.
    $cmdText = ""
    if ($evt.tool_input) {
        $cmdText = "$($evt.tool_input.command) $($evt.tool_input.file_path) $($evt.tool_input.description)"
    }
    if ($cmdText -match '(?i)\b(cce|setup-cce|mcp)\b') { Allow }

    # 10-minute cached health verdict, scoped PER PROJECT so multiple clones
    # (redline-1/2/3) never share a verdict. Key off CLAUDE_PROJECT_DIR (set by
    # Claude Code for hook subprocesses), falling back to the current dir.
    $projDir = $env:CLAUDE_PROJECT_DIR
    if (-not $projDir) { $projDir = (Get-Location).Path }
    $projKey = ([System.BitConverter]::ToString(
        [System.Security.Cryptography.MD5]::Create().ComputeHash(
            [System.Text.Encoding]::UTF8.GetBytes($projDir.ToLowerInvariant())))
        ).Replace('-', '').Substring(0, 12)
    $flag = Join-Path $env:TEMP "cce-health-$($env:USERNAME)-$projKey.flag"
    if (Test-Path $flag) {
        $age = (Get-Date) - (Get-Item $flag).LastWriteTime
        if ($age.TotalMinutes -lt 10) {
            if ((Get-Content $flag -Raw).Trim() -eq 'ok') { Allow }
            else { Deny ((Get-Content $flag -Raw).Trim() -replace '^bad:', '') }
        }
    }

    # Fresh health check
    $cce = (Get-Command cce -ErrorAction SilentlyContinue).Source
    if (-not $cce) { $cce = Join-Path $env:USERPROFILE ".local\bin\cce.exe" }
    if (-not (Test-Path $cce)) {
        $msg = "CCE blocked: cce binary not found. Run tasks\setup-cce.ps1 to install the Code Context Engine, then retry."
        Set-Content $flag "bad:$msg"
        Deny $msg
    }

    & $cce status *> $null
    if ($LASTEXITCODE -ne 0) {
        $msg = "CCE blocked: 'cce status' failed (exit $LASTEXITCODE). The Code Context Engine index is missing or corrupt. Run tasks\setup-cce.ps1 or 'cce index', then retry."
        Set-Content $flag "bad:$msg"
        Deny $msg
    }

    Set-Content $flag "ok"
    Allow
}
catch {
    # Fail OPEN: a broken gate must never wedge the whole session. Surface the
    # error to stderr (visible to the user) but allow the tool.
    Write-Error "cce-health-gate hook error (failing open): $_"
    exit 0
}
