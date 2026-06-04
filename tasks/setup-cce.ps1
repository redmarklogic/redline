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

# 2. Install cce CLI
Write-Step "Installing code-context-engine"
$cceCmd = Get-Command cce -ErrorAction SilentlyContinue
if ($cceCmd) {
    Write-Skip "cce already installed at $($cceCmd.Source)"
} else {
    uv tool install "code-context-engine[local]"
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";" + $env:PATH
    if (-not (Get-Command cce -ErrorAction SilentlyContinue)) {
        Write-Fail "cce installed but not in PATH. Add uv tool bin dir to your PATH and re-run."
    }
    Write-OK "cce installed"
}

# 3. Run cce init to generate .mcp.json (machine-specific, gitignored)
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
Write-Host "   Tip: use 'cce savings' to track token savings." -ForegroundColor DarkGray
