# PreToolUse guard: catches PowerShell patterns that silently break `gh api graphql`.
# 1. Hashtable/object member access inside -f/-F flag args  -> gh sends the literal
#    string "System.Collections.Hashtable.id" (verified live 2026-06-13, 26 failed calls).
# 2. PowerShell interpolation inside the query string        -> values parse as GraphQL
#    tokens (UNKNOWN_CHAR) or inject unquoted (26 more failed calls).
# 3. Destructive updateProjectV2Field mutations              -> option/iteration IDs
#    regenerate and assignments orphan; skill procedure is binding.
# Non-blocking: emits additionalContext so the agent can fix before running.

$payload = [Console]::In.ReadToEnd() | ConvertFrom-Json
$cmd = $payload.tool_input.command
if (-not $cmd) { exit 0 }
if ($cmd -notmatch 'gh\s+api\s+graphql') { exit 0 }

$warnings = @()

if ($cmd -match '-[fF]\s+\w+=\$\w+\.\w+') {
    $warnings += 'Member access in a -f/-F flag arg (e.g. -f itemId=$item.id) sends the literal string "Hashtable.id" - extract to a plain string variable first ($itemId = [string]$item.id).'
}

if ($cmd -match '-f\s+query=[^|;]*\$\(') {
    $warnings += 'PowerShell interpolation inside the GraphQL query string parses as GraphQL tokens (UNKNOWN_CHAR) - declare GraphQL variables and pass values via separate -f flags.'
}

if ($cmd -match 'updateProjectV2Field' -and $cmd -match 'iterationConfiguration|singleSelectOptions') {
    $warnings += 'DESTRUCTIVE: updateProjectV2Field replaces ALL option/iteration IDs and drops completed iterations - follow the snapshot-and-restore procedure in .agents/skills/github-projects/SKILL.md before running.'
}

if ($warnings.Count -eq 0) { exit 0 }

$out = @{
    hookSpecificOutput = @{
        hookEventName     = 'PreToolUse'
        additionalContext = ($warnings -join ' ')
    }
}
$out | ConvertTo-Json -Depth 5 -Compress | Write-Output
exit 0
