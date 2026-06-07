# ---------------------------------------------------------------------------
# RedMark SonarQube -- branch scan (PowerShell)
# ---------------------------------------------------------------------------
# Analyses the currently checked-out redline branch against the local SonarQube
# instance (http://localhost:9000). Runs directly on the dev machine -- no CI.
#
#   1. Load secrets/config from .env (untracked).
#   2. Derive the current git branch.
#   3. Generate sonar-project.properties from [tool.usethis] (the SSOT).
#   4. Produce best-effort ruff + coverage reports (absence does not fail).
#   5. Run the sonar-scanner-cli container against the local instance.
#
# Prereq: the local stack is up (redmark-sonarqube: ../services/redmark-sonarqube).
# Usage:  ./scan.ps1
# ---------------------------------------------------------------------------

$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {

# Pinned scanner image (FR/Plan: pin a specific tag).
$SCANNER_IMAGE = 'sonarsource/sonar-scanner-cli:11'
$USETHIS_VERSION = 'usethis@0.22.0'

# -- 1. Load .env -----------------------------------------------------------
$envPath = Join-Path $PSScriptRoot '.env'
if (-not (Test-Path $envPath)) {
    throw ".env not found at $envPath. Copy .env.example to .env and set SONAR_TOKEN " +
          "(generate one at http://localhost:9000 -> My Account -> Security)."
}
Get-Content $envPath | ForEach-Object {
    $line = $_.Trim()
    if ($line -and -not $line.StartsWith('#') -and $line.Contains('=')) {
        $k, $v = $line.Split('=', 2)
        Set-Item -Path "Env:$($k.Trim())" -Value $v.Trim()
    }
}

$SONAR_HOST_URL    = if ($env:SONAR_HOST_URL) { $env:SONAR_HOST_URL } else { 'http://host.docker.internal:9000' }
$SONAR_PROJECT_KEY = if ($env:SONAR_PROJECT_KEY) { $env:SONAR_PROJECT_KEY } else { 'redline' }
if (-not $env:SONAR_TOKEN) {
    throw "SONAR_TOKEN is empty in .env. Generate a token at http://localhost:9000 " +
          "(My Account -> Security -> Generate Tokens) and set SONAR_TOKEN in .env."
}

# -- Availability check: single source of truth (sonar_scan.ensure_available) --
# Delegates to the Python tool so the scan and review gates share one definition
# of "available". SONARQUBE_URL is loaded from .env above; the tool normalises
# host.docker.internal -> localhost for this host-side call.
$env:PYTHONPATH = Join-Path $PSScriptRoot '.agents/tools'
uv run python -m sonar_scan.healthcheck
if ($LASTEXITCODE -ne 0) {
    throw "SonarQube availability check failed (see message above). Start the local stack and retry."
}

# -- 2. Current branch ------------------------------------------------------
$BRANCH = (git rev-parse --abbrev-ref HEAD).Trim()
if (-not $BRANCH) { throw 'Could not determine the current git branch.' }
Write-Host "-- Scanning branch: $BRANCH --" -ForegroundColor Cyan

# -- 3. Generate properties from the SSOT -----------------------------------
Write-Host '-- Generating .cache/sonarqube/sonar-project.properties from [tool.usethis] --' -ForegroundColor Cyan
$null = New-Item -ItemType Directory -Force -Path '.cache/sonarqube'
$env:SONAR_PROJECT_KEY = $SONAR_PROJECT_KEY
uvx $USETHIS_VERSION show sonarqube --output-file=.cache/sonarqube/sonar-project.properties
if ($LASTEXITCODE -ne 0) { throw 'Failed to generate .cache/sonarqube/sonar-project.properties from [tool.usethis].' }

# -- 4. Best-effort reports (absence must not fail the scan) -----------------
Write-Host '-- Producing ruff report (best-effort) --' -ForegroundColor Cyan
# ruff exits non-zero when it finds issues; that is expected, not a scan failure.
try { uv run ruff check . --output-format=json -o .cache/sonarqube/ruff-report.json 2>$null } catch {}
if (-not (Test-Path '.cache/sonarqube/ruff-report.json')) { '[]' | Set-Content -Path '.cache/sonarqube/ruff-report.json' -Encoding ascii }
# Rewrite Windows absolute paths to repo-relative forward-slash paths so the
# Linux scanner container can resolve them (e.g. src/marker/foo.py not C:\...\foo.py).
# PS 5.1: ConvertFrom-Json returns the whole array as ONE pipeline object; do NOT
# wrap in @() or foreach sees a single nested array instead of per-issue objects.
$ruffIssues = Get-Content '.cache/sonarqube/ruff-report.json' -Raw | ConvertFrom-Json
if ($ruffIssues.Count -gt 0) {
    foreach ($issue in $ruffIssues) {
        if ($issue.filename -and $issue.filename.StartsWith($PSScriptRoot)) {
            $issue.filename = ($issue.filename.Substring($PSScriptRoot.Length + 1)) -replace '\\', '/'
        }
    }
    # @() forces a JSON array even when exactly one issue remains.
    ConvertTo-Json -InputObject @($ruffIssues) -Depth 10 | Set-Content '.cache/sonarqube/ruff-report.json' -Encoding ascii
}

Write-Host '-- Producing coverage report if data exists (best-effort) --' -ForegroundColor Cyan
if (Test-Path '.coverage') {
    try { uv run coverage xml -o coverage.xml 2>$null } catch { Write-Host '  coverage xml failed -- continuing without coverage.' -ForegroundColor Yellow }
} else {
    Write-Host '  No .coverage data found -- skipping coverage (run tests with coverage first to include it).' -ForegroundColor Yellow
}

# -- 5. Run the scanner container against the local instance ----------------
$repo = ($PSScriptRoot -replace '\\', '/')
Write-Host "-- Running $SCANNER_IMAGE --" -ForegroundColor Cyan
$tempLog = [System.IO.Path]::GetTempFileName()
docker run --rm `
    -e "SONAR_HOST_URL=$SONAR_HOST_URL" `
    -e "SONAR_TOKEN=$env:SONAR_TOKEN" `
    -v "${repo}:/usr/src" `
    $SCANNER_IMAGE `
    "-Dproject.settings=/usr/src/.cache/sonarqube/sonar-project.properties" `
    "-Dsonar.branch.name=$BRANCH" | Tee-Object -FilePath $tempLog
if ($LASTEXITCODE -ne 0) {
    Remove-Item $tempLog -Force -ErrorAction SilentlyContinue
    throw "sonar-scanner failed (exit $LASTEXITCODE)."
}

# -- 6. Poll compute-engine task (bounded wait, max 60 s) --------------------
$ceTaskUrl = ([regex]::Match((Get-Content $tempLog -Raw), 'https?://\S+api/ce/task\?id=\S+').Value) `
    -replace 'host\.docker\.internal', 'localhost'
Remove-Item $tempLog -Force -ErrorAction SilentlyContinue
if (-not $ceTaskUrl) { throw 'Could not extract CE task URL from scanner output.' }

Write-Host "-- Polling CE task (max 60 s): $ceTaskUrl --" -ForegroundColor Cyan
$ceHeaders = @{ Authorization = "Bearer $env:SONAR_TOKEN" }
$ceStatus  = $null
for ($i = 0; $i -lt 12; $i++) {
    $ceResult = Invoke-RestMethod -Uri $ceTaskUrl -Headers $ceHeaders -TimeoutSec 10 -ErrorAction Stop
    $ceStatus = $ceResult.task.status
    if ($ceStatus -in @('SUCCESS', 'FAILED', 'CANCELED')) { break }
    Write-Host "  status: $ceStatus - waiting 5 s..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
}
if ($ceStatus -ne 'SUCCESS') {
    throw "CE task did not reach SUCCESS (status=$ceStatus). Task: $ceTaskUrl"
}
Write-Host "  CE task: SUCCESS" -ForegroundColor Green

Write-Host ''
Write-Host '======================================================' -ForegroundColor Green
Write-Host "  Scan complete for branch: $BRANCH"                    -ForegroundColor Green
Write-Host "  Project: $SONAR_PROJECT_KEY"
Write-Host "  View:    http://localhost:9000/dashboard?id=$SONAR_PROJECT_KEY&branch=$BRANCH"
Write-Host '======================================================' -ForegroundColor Green

} finally {
    Pop-Location
}
