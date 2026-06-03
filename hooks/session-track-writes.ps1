# VS Code PostToolUse hook — writes a session flag when file-editing tools target paths
# matching WRITE_PATTERN. The session-stop-handover.ps1 Stop hook reads this flag to
# decide whether a handover is needed. If no flag exists, Stop allows the session to
# end silently (Q&A sessions never trigger handover).
#
# Environment variables (set in agent frontmatter hooks config):
#   WRITE_PATTERN  Substring to match against filePath. Use "src/" to require src/ writes.
#                  Use "any" to flag on any file write regardless of path.
#                  Default: "src/"
#
# File-writing tool names (VS Code camelCase — see VS Code hooks FAQ):
#   create_file, replace_string_in_file, multi_replace_string_in_file, edit_notebook_file

param()

$FILE_WRITING_TOOLS = @(
    "create_file",
    "replace_string_in_file",
    "multi_replace_string_in_file",
    "edit_notebook_file"
)

$writePattern = if ($env:WRITE_PATTERN) { $env:WRITE_PATTERN } else { "src/" }

$raw = [Console]::In.ReadToEnd()
try {
    $inputData = $raw | ConvertFrom-Json
} catch {
    exit 0  # Malformed input — non-blocking, do not interfere
}

$toolName = $inputData.tool_name
$filePath = $inputData.tool_input.filePath

if (-not $toolName -or -not $filePath) { exit 0 }

$isWriteTool = $toolName -in $FILE_WRITING_TOOLS

$pathMatches = if ($writePattern -eq "any") {
    $true  # Match any path
} else {
    $filePath -like "*$writePattern*"
}

if ($isWriteTool -and $pathMatches) {
    $sessionDir = [System.IO.Path]::GetFullPath(
        (Join-Path $PSScriptRoot ".." ".session")
    )
    New-Item -ItemType Directory -Force -Path $sessionDir | Out-Null
    $flagPath = Join-Path $sessionDir "wrote-files.flag"
    # Append so multiple writes accumulate (useful for debugging)
    Add-Content -Path $flagPath -Value "$toolName : $filePath" -Encoding UTF8
}

# Always non-blocking — PostToolUse must not interfere with tool execution
exit 0
