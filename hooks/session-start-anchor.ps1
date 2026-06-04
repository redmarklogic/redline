# SessionStart hook (Copilot) / UserPromptSubmit hook (Claude Code).
# Writes HEAD SHA to .session/session-start.md to anchor the session boundary
# so session-handover can produce a bounded git log.
#
# Copilot: registered in .github/hooks/handover.json — fires once per session.
# Claude Code: registered in .claude/settings.json UserPromptSubmit — fires on every
# user message. The session-ID guard below makes it idempotent within a session
# and re-anchors automatically when a new session starts.

# --- Idempotent guard (Claude Code UserPromptSubmit) ---
# Copilot's SessionStart does not provide session_id, so $currentSessionId is $null
# and the guard is skipped — behaviour is unchanged for Copilot.
$raw = [Console]::In.ReadToEnd()
$inputData = try { $raw | ConvertFrom-Json } catch { $null }
$currentSessionId = if ($inputData -and $inputData.session_id) { $inputData.session_id } else { $null }

if ($currentSessionId) {
    $anchorPath = [System.IO.Path]::GetFullPath(
        (Join-Path $PSScriptRoot ".." ".session" "session-start.md")
    )
    if (Test-Path $anchorPath) {
        $existing = Get-Content $anchorPath -Raw -Encoding UTF8
        if ($existing -match "SESSION_ID: $([regex]::Escape($currentSessionId))") {
            exit 0  # Same session — anchor already written; skip
        }
    }
}
# -------------------------------------------------------

$sha = (git rev-parse HEAD 2>$null).Trim()
if (-not $sha) { $sha = "unknown" }

$sessionDir = Join-Path $PSScriptRoot ".." ".session"
$sessionDir = [System.IO.Path]::GetFullPath($sessionDir)
New-Item -ItemType Directory -Force -Path $sessionDir | Out-Null

$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
$content = "HEAD_SHA: $sha`nSESSION_ID: $currentSessionId`nwritten: $timestamp"
Set-Content -Path (Join-Path $sessionDir "session-start.md") -Value $content -Encoding UTF8

$output = @{
    hookSpecificOutput = @{
        hookEventName     = "SessionStart"
        additionalContext = "Session anchor written. HEAD SHA: $sha. Use this SHA in session-handover to bound the git log window."
    }
} | ConvertTo-Json -Compress -Depth 5

Write-Output $output
