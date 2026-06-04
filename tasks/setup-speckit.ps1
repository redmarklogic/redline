# setup-speckit.ps1 - Install specify CLI and activate Claude Code integration
# Called by setup.ps1 or run standalone: .\tasks\setup-speckit.ps1
#
# Skills land in .agents/skills/speckit-* (project convention).
# speckit hardcodes .claude/skills/ as install target; this script moves them after install.

param([switch]$Quiet)

$SPECKIT_VERSION = "v0.9.3"
$SPECKIT_SOURCE  = "git+https://github.com/github/spec-kit.git@$SPECKIT_VERSION"

function Write-Step { param([string]$msg) if (-not $Quiet) { Write-Host "`n>> $msg" -ForegroundColor Cyan } }
function Write-OK   { param([string]$msg) Write-Host "   OK  $msg" -ForegroundColor Green }
function Write-Skip { param([string]$msg) if (-not $Quiet) { Write-Host "   --  $msg" -ForegroundColor DarkGray } }
function Write-Fail { param([string]$msg) Write-Host "   ERR $msg" -ForegroundColor Red; exit 1 }

$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

# 1. Verify uv is available
Write-Step "Checking uv"
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Fail "uv not found. Install from https://docs.astral.sh/uv/getting-started/installation/"
}
Write-Skip "uv $(uv --version)"

# 2. Install or upgrade specify CLI from git
Write-Step "Installing specify CLI ($SPECKIT_VERSION from git)"
$specifyCmd = Get-Command specify -ErrorAction SilentlyContinue
$needsInstall = $true
if ($specifyCmd) {
    $currentSource = uv tool list 2>&1 | Select-String "specify-cli"
    if ($currentSource -match [regex]::Escape($SPECKIT_VERSION)) {
        Write-Skip "specify $SPECKIT_VERSION already installed"
        $needsInstall = $false
    } else {
        Write-Skip "specify found but not $SPECKIT_VERSION - upgrading"
    }
}
if ($needsInstall) {
    uv tool install "specify-cli" --from $SPECKIT_SOURCE --force 2>&1 | ForEach-Object { Write-Host "   $_" }
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "User") + ";" + $env:PATH
    if (-not (Get-Command specify -ErrorAction SilentlyContinue)) {
        Write-Fail "specify installed but not in PATH. Add uv tool bin dir to your PATH and re-run."
    }
    Write-OK "specify $SPECKIT_VERSION installed"
}

# 3. Install/upgrade Claude Code integration (speckit installs to .claude/skills/ internally)
Write-Step "Installing Claude Code integration"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$integrationStatus = specify integration list 2>&1 | Select-String "claude"
if ($integrationStatus -match "installed") {
    specify integration upgrade claude 2>&1 | Select-String "upgraded|already|Error" | ForEach-Object { Write-Host "   $_" }
} else {
    specify integration install claude --force 2>&1 | Select-String "installed|Error" | ForEach-Object { Write-Host "   $_" }
}

# 4. Move skills from .claude/skills/speckit-* to .agents/skills/speckit-*
Write-Step "Moving speckit skills to .agents/skills/"
$claudeSkillsDir = ".claude\skills"
$agentsSkillsDir = ".agents\skills"
if (-not (Test-Path $agentsSkillsDir)) { New-Item -ItemType Directory -Path $agentsSkillsDir | Out-Null }

$moved = 0
$claudeSpeckit = Get-ChildItem $claudeSkillsDir -Filter "speckit-*" -Directory -ErrorAction SilentlyContinue
foreach ($dir in $claudeSpeckit) {
    $target = Join-Path $agentsSkillsDir $dir.Name
    if (Test-Path $target) { Remove-Item $target -Recurse -Force }
    Move-Item $dir.FullName $target
    $moved++
}

# Clean up empty .claude/skills dir
$remaining = Get-ChildItem $claudeSkillsDir -ErrorAction SilentlyContinue
if ($claudeSpeckit.Count -gt 0 -and -not $remaining) {
    Remove-Item $claudeSkillsDir -Force -ErrorAction SilentlyContinue
}

if ($moved -gt 0) { Write-OK "$moved skill(s) moved to $agentsSkillsDir" }
else { Write-Skip "no new skills to move" }

# 5. Verify
Write-Step "Verifying speckit skills"
$skills = Get-ChildItem $agentsSkillsDir -Filter "speckit-*" -Directory -ErrorAction SilentlyContinue
if ($skills.Count -ge 1) {
    Write-OK "$($skills.Count) speckit skills in $agentsSkillsDir"
} else {
    Write-Fail "No speckit skills found in $agentsSkillsDir"
}
