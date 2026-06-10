# setup-cce.ps1 - Install Code Context Engine (CCE) MCP server
# Called by setup.ps1 or run standalone after cloning: .\tasks\setup-cce.ps1
# Source: https://github.com/elara-labs/code-context-engine
#
# What this does:
#   - Installs the `cce` CLI via uv tool
#   - Runs `cce init --agent claude` to generate .mcp.json (gitignored, machine-specific)
#   - Index builds automatically when the editor/Claude Code starts the MCP server

param([switch]$Quiet)

function Write-Step { param([string]$msg) if (-not $Quiet) { Write-Host "`n>> $msg" -ForegroundColor Cyan } }
function Write-OK   { param([string]$msg) Write-Host "   OK  $msg" -ForegroundColor Green }
function Write-Skip { param([string]$msg) if (-not $Quiet) { Write-Host "   --  $msg" -ForegroundColor DarkGray } }
function Write-Fail { param([string]$msg) Write-Host "   ERR $msg" -ForegroundColor Red; exit 1 }

# 1. Verify uv is available
Write-Step "Checking uv"
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Fail "uv not found. Install from https://docs.astral.sh/uv/getting-started/installation/"
}
Write-Skip "uv $(uv --version)"

# 2. Ensure uv tool bin dir is on PATH (uv uses ~/.local/bin on Windows)
Write-Step "Checking uv tool bin dir on PATH"
$uvToolBin = Join-Path $env:USERPROFILE ".local\bin"
$userPath = [System.Environment]::GetEnvironmentVariable("PATH", "User") ?? ""
if ($userPath -notlike "*$uvToolBin*") {
    [System.Environment]::SetEnvironmentVariable(
        "PATH", "$uvToolBin;$userPath", "User")
    $env:PATH = "$uvToolBin;$env:PATH"
    Write-OK "Added $uvToolBin to User PATH (restart shell to inherit)"
} else {
    # Make sure it's visible in the current session even if inherited PATH is stale
    if ($env:PATH -notlike "*$uvToolBin*") { $env:PATH = "$uvToolBin;$env:PATH" }
    Write-Skip "$uvToolBin already in User PATH"
}

# 3. Install cce CLI
Write-Step "Installing code-context-engine"
$cceCmd = Get-Command cce -ErrorAction SilentlyContinue
if ($cceCmd) {
    Write-Skip "cce already installed at $($cceCmd.Source)"
} else {
    uv tool install "code-context-engine[local]"
    # Refresh PATH in current session after install
    $env:PATH = "$uvToolBin;$env:PATH"
    if (-not (Get-Command cce -ErrorAction SilentlyContinue)) {
        Write-Fail "cce installed but still not found. Open a new terminal and re-run."
    }
    Write-OK "cce installed"
}

# 4. Run cce init to generate .mcp.json (machine-specific, gitignored)
Write-Step "Initializing CCE for Claude Code"
if (Test-Path ".mcp.json") {
    Write-Skip ".mcp.json already exists - skipping init (delete it and re-run to regenerate)"
} else {
    cce init --agent claude 2>&1 | ForEach-Object { Write-Host "   $_" }
    if (Test-Path ".mcp.json") {
        Write-OK ".mcp.json generated"
    } else {
        Write-Fail "cce init did not produce .mcp.json - check output above"
    }
}

Write-OK "CCE ready. Index builds automatically when Claude Code starts the MCP server."
Write-Host "   Tip: run 'cce savings' to track token savings." -ForegroundColor DarkGray
Write-Host "   Note: CCE is always-on. PATH must include $uvToolBin for 'cce' to be found by Claude Code." -ForegroundColor DarkGray
Write-Host "   Test: cd $(Split-Path $PSScriptRoot); uv run pytest tasks/tests/ (config tests, ~2s)" -ForegroundColor DarkGray
