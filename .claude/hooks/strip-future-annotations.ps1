$json = $input | Out-String | ConvertFrom-Json
$f = $json.tool_input.file_path
if (-not $f -or -not $f.EndsWith('.py')) { exit 0 }
if (-not (Test-Path $f)) { exit 0 }
$lines = Get-Content $f -Encoding UTF8
$filtered = $lines | Where-Object { $_ -notmatch '^from __future__ import annotations\s*$' }
if ($filtered.Count -lt $lines.Count) {
    $filtered | Set-Content $f -Encoding UTF8
}
