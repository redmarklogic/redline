# PostToolUse hook: run prek pre-commit checks after writes to src/ or tests/
# Violations are surfaced as a systemMessage so the agent resolves them before continuing.

$json = $input | Out-String | ConvertFrom-Json
$filePath = $json.tool_input.file_path

if (-not $filePath) { exit 0 }
if (-not $filePath.EndsWith('.py')) { exit 0 }

$normalized = $filePath.Replace('\', '/')
if ($normalized -notmatch '/src/' -and $normalized -notmatch '/tests/') { exit 0 }

$lines = @()
& ".venv\Scripts\prek.exe" run --files $filePath --stage pre-commit --no-progress --color never 2>&1 |
    ForEach-Object { $lines += "$_" }
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    $output = $lines -join "`n"
    @{ systemMessage = "prek pre-commit violations in ${filePath} — resolve before continuing:`n`n$output" } |
        ConvertTo-Json -Compress
}
