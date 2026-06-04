# PostToolUse hook (Copilot / Claude Code) — writes a session flag when file-editing tools
# target paths matching WRITE_PATTERN. The session-stop-handover.ps1 Stop hook reads this
# flag to decide whether a handover is needed. If no flag exists, Stop exits silently.
#
# Environment variables:
#   WRITE_PATTERN  Substring to match against the file path. Default: "src/"
#                  Use "any" to flag on any file write regardless of path.
#
# Copilot: registered in agent frontmatter hooks.PostToolUse (WRITE_PATTERN set there).
# Claude Code: registered in .claude/settings.json PostToolUse matcher Write|Edit|MultiEdit.
#
# Tool name reference:
#   Copilot/VS Code: create_file, replace_string_in_file, multi_replace_string_in_file, edit_notebook_file
#   Claude Code:     Write, Edit, MultiEdit, NotebookEdit

param()

$FILE_WRITING_TOOLS = @(
    # Copilot / VS Code tool names
    "create_file",
    "replace_string_in_file",
    "multi_replace_string_in_file",
    "edit_notebook_file",
    # Claude Code tool names
    "Write",
    "Edit",
    "MultiEdit",
    "NotebookEdit"
)

$writePattern = if ($env:WRITE_PATTERN) { $env:WRITE_PATTERN } else { "src/" }

$raw = [Console]::In.ReadToEnd()
try {
    $inputData = $raw | ConvertFrom-Json
} catch {
    exit 0  # Malformed input — non-blocking, do not interfere
}

$toolName = $inputData.tool_name
# Copilot uses camelCase filePath; Claude Code uses snake_case file_path.
$filePath = if ($inputData.tool_input.filePath) { $inputData.tool_input.filePath }
            elseif ($inputData.tool_input.file_path) { $inputData.tool_input.file_path }
            else { $null }

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
