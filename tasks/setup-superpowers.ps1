# setup-superpowers.ps1 - Install or upgrade obra/superpowers skills, then apply Redline overrides
# Called by setup.ps1 or run standalone: .\tasks\setup-superpowers.ps1
#
# On each run:
#   1. Download the pinned release from GitHub if not already at that version
#   2. Remove writing-plans and executing-plans (conflict with Spec-Kit pipeline)
#
# Run again after bumping SUPERPOWERS_VERSION to upgrade.

param([switch]$Quiet)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$SUPERPOWERS_REPO    = "obra/superpowers"

$agentsSkillsDir  = ".agents\skills"
$skillsLockFile   = "skills-lock.json"

# Read pinned version dynamically from skills-lock.json
$skillsLock          = Get-Content $skillsLockFile -Raw | ConvertFrom-Json
$SUPERPOWERS_VERSION = $skillsLock.superpowersVersion
if (-not $SUPERPOWERS_VERSION) { Write-Fail "superpowersVersion not found in $skillsLockFile" }

function Write-Step { param([string]$msg) if (-not $Quiet) { Write-Host "`n>> $msg" -ForegroundColor Cyan } }
function Write-OK   { param([string]$msg) Write-Host "   OK  $msg" -ForegroundColor Green }
function Write-Skip { param([string]$msg) if (-not $Quiet) { Write-Host "   --  $msg" -ForegroundColor DarkGray } }
function Write-Fail { param([string]$msg) Write-Host "   ERR $msg" -ForegroundColor Red; exit 1 }

# ── 1. Check current version ──────────────────────────────────────────────────

Write-Step "Checking Superpowers version"

$installedVersion = $skillsLock.PSObject.Properties['installedSuperpowersVersion']?.Value

if ($installedVersion -eq $SUPERPOWERS_VERSION) {
    Write-Skip "Superpowers $SUPERPOWERS_VERSION already installed"
} else {
    if ($installedVersion) {
        Write-Host "   Upgrading $installedVersion → $SUPERPOWERS_VERSION" -ForegroundColor Yellow
    } else {
        Write-Host "   Installing Superpowers $SUPERPOWERS_VERSION" -ForegroundColor Yellow
    }

    # ── 2. Download source archive ────────────────────────────────────────────

    Write-Step "Downloading obra/superpowers $SUPERPOWERS_VERSION"

    $versionNum  = $SUPERPOWERS_VERSION -replace '^v', ''
    $tmpDir      = Join-Path $env:TEMP "superpowers-install-$versionNum"
    $zipFile     = Join-Path $tmpDir "superpowers.zip"
    $archiveName = "superpowers-$versionNum"          # GitHub strips the 'v'
    $extractRoot = Join-Path $tmpDir $archiveName
    $skillsSource = Join-Path $extractRoot "skills"

    if (Test-Path $tmpDir) { Remove-Item $tmpDir -Recurse -Force }
    New-Item -ItemType Directory -Force $tmpDir | Out-Null

    $downloadUrl = "https://codeload.github.com/$SUPERPOWERS_REPO/zip/refs/tags/$SUPERPOWERS_VERSION"
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $zipFile -UseBasicParsing
    } catch {
        Write-Fail "Download failed: $_"
    }

    Expand-Archive -Path $zipFile -DestinationPath $tmpDir -Force

    if (-not (Test-Path $skillsSource)) {
        Write-Fail "Expected skills/ at $skillsSource — archive structure may have changed"
    }

    # ── 3. Copy skills to .agents/skills/ ────────────────────────────────────

    Write-Step "Installing skills"

    $installed = 0
    Get-ChildItem $skillsSource -Directory | ForEach-Object {
        $dest = Join-Path $agentsSkillsDir $_.Name
        if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
        Copy-Item $_.FullName $dest -Recurse
        $installed++
    }

    Write-OK "$installed skill(s) installed from $SUPERPOWERS_REPO $SUPERPOWERS_VERSION"

    # ── 4. Record installed version in skills-lock.json ──────────────────────

    $skillsLock | Add-Member -MemberType NoteProperty -Name installedSuperpowersVersion -Value $SUPERPOWERS_VERSION -Force
    $skillsLock | ConvertTo-Json -Depth 10 | Set-Content $skillsLockFile -Encoding UTF8
    Write-OK "installedSuperpowersVersion updated in $skillsLockFile"

    # Cleanup temp
    Remove-Item $tmpDir -Recurse -Force
}

# ── 5. Remove skills that conflict with the Spec-Kit pipeline ─────────────────
#
# writing-plans  → use /speckit.plan + /speckit.tasks instead
# executing-plans → use subagent-driven-development with specs/NNN/tasks.md instead

Write-Step "Removing Spec-Kit-conflicting Superpowers skills"

$skillsToRemove = @("writing-plans", "executing-plans")
foreach ($skill in $skillsToRemove) {
    $path = Join-Path $agentsSkillsDir $skill
    if (Test-Path $path) {
        Remove-Item $path -Recurse -Force
        Write-OK "Removed $skill"
    } else {
        Write-Skip "$skill already absent"
    }
}
