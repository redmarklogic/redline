# VS Code SessionStart hook — writes the HEAD SHA to .session/session-start.md.
# This anchors the session boundary so session-handover can produce a bounded git log.
#
# Registered in .github/hooks/handover.json (applies to all agents).

$sha = (git rev-parse HEAD 2>$null).Trim()
if (-not $sha) { $sha = "unknown" }

$sessionDir = Join-Path $PSScriptRoot ".." ".session"
$sessionDir = [System.IO.Path]::GetFullPath($sessionDir)
New-Item -ItemType Directory -Force -Path $sessionDir | Out-Null

$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
$content = "HEAD_SHA: $sha`nwritten: $timestamp"
Set-Content -Path (Join-Path $sessionDir "session-start.md") -Value $content -Encoding UTF8

$output = @{
    hookSpecificOutput = @{
        hookEventName    = "SessionStart"
        additionalContext = "Session anchor written. HEAD SHA: $sha. Use this SHA in session-handover to bound the git log window."
    }
} | ConvertTo-Json -Compress -Depth 5

Write-Output $output
