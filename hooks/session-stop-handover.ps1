# Stop hook (Copilot agentStop / Claude Code Stop).
# Conditionally blocks the agent from finishing.
# Only blocks if session-track-writes.ps1 set .session/wrote-files.flag this session,
# indicating qualifying file writes occurred. Pure Q&A sessions exit 0 silently.
#
# Copilot: registered in agent frontmatter hooks.Stop — blocks via decision:"block" JSON.
# Claude Code: registered in .claude/settings.json Stop — blocks via exit code 2.
# Both mechanisms applied simultaneously; each tool reads what it understands.
#
# Copilot agent frontmatter: .github/agents/rl.kabilan.agent.md, rl.peter.agent.md.

$inputData = [Console]::In.ReadToEnd() | ConvertFrom-Json

$sessionDir = [System.IO.Path]::GetFullPath(
    (Join-Path $PSScriptRoot ".." ".session")
)
$flagPath = Join-Path $sessionDir "wrote-files.flag"
$hasWrites = Test-Path $flagPath

if ($inputData.stop_hook_active) {
    # Already in a stop-hook continuation — allow finishing and clean up flag.
    if ($hasWrites) { Remove-Item $flagPath -Force -ErrorAction SilentlyContinue }
    exit 0
}

if (-not $hasWrites) {
    # No qualifying file writes this session (e.g. Q&A only) — allow stopping silently.
    exit 0
}

# Qualifying writes detected — block and request handover.
$output = @{
    hookSpecificOutput = @{
        hookEventName = "Stop"
        decision      = "block"
        reason        = "File writes were made this session. Before finishing, invoke the session-handover skill: produce the four-section handover note (What shipped / In flight / Watch-outs / Open questions) and write load-bearing decisions to CCE."
    }
} | ConvertTo-Json -Compress -Depth 5

Write-Output $output
exit 2  # Claude Code Stop hook: exit 2 = block. Copilot reads decision:"block" above; exit code is irrelevant to Copilot.
