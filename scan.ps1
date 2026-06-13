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
    try { uv run coverage xml -o .cache/sonarqube/coverage.xml 2>$null } catch { Write-Host '  coverage xml failed -- continuing without coverage.' -ForegroundColor Yellow }
} else {
    Write-Host '  No .coverage data found -- skipping coverage (run tests with coverage first to include it).' -ForegroundColor Yellow
}

# -- 5. Run the scanner container against the local instance ----------------
# PERFORMANCE: the repo lives on Windows NTFS (C:\). Bind-mounting it into the
# Linux scanner (-v ${repo}:/usr/src) routes every file stat/read through the
# Docker Desktop 9p/virtiofs WSL2 boundary. Measured: a Python-only scan took
# ~9 min, dominated by Cobertura (159s), PythonXUnit (152s) and SCM blame (108s)
# -- all per-small-file work across that boundary. Flags alone got it to ~8 min.
# Fix: stage the source into a Linux-NATIVE named volume (overlayfs) via a tar
# stream, then scan THAT. The scanner never touches NTFS, so sensor I/O collapses.
$repo = ($PSScriptRoot -replace '\\', '/')
$SRC_VOLUME = 'redmark-sonar-src'
Write-Host "-- Staging source into native volume '$SRC_VOLUME' (avoids NTFS bind-mount tax) --" -ForegroundColor Cyan

# Fresh volume each run (source is a point-in-time snapshot of the working tree).
docker volume rm $SRC_VOLUME 2>$null | Out-Null
docker volume create $SRC_VOLUME | Out-Null

# Stream a filtered tar of the working tree into the volume. Excludes heavy dirs
# the scanner ignores anyway (.git is safe to drop -- sonar.scm.disabled below) so
# the copy stays small and fast. tar over stdin is one boundary crossing total
# instead of tens of thousands of per-file stats.
$stageSw = [System.Diagnostics.Stopwatch]::StartNew()
tar -C $PSScriptRoot `
    --exclude='./.git' --exclude='./.venv' --exclude='./node_modules' `
    --exclude='./.hypothesis' --exclude='./dist' --exclude='./build' `
    --exclude='./**/__pycache__' --exclude='./.mypy_cache' --exclude='./.ruff_cache' `
    --exclude='./**/.terraform' `
    -cf - . | docker run --rm -i -v "${SRC_VOLUME}:/usr/src" busybox sh -c 'tar -C /usr/src -xf -'
if ($LASTEXITCODE -ne 0) { throw 'Failed to stage source into the native volume.' }
$stageSw.Stop()
Write-Host ("   staged in {0:N1}s" -f $stageSw.Elapsed.TotalSeconds) -ForegroundColor DarkGray

Write-Host "-- Running $SCANNER_IMAGE (against native volume) --" -ForegroundColor Cyan
$tempLog = [System.IO.Path]::GetTempFileName()
# Named volume persists the scanner cache (JRE/engine/plugins, ~150 MB) across
# the --rm containers. skipJreProvisioning uses the image's bundled JRE 17.
# scm.disabled: blame only feeds new-code attribution, useless for a local scan.
# xunit.skipDetails: skips per-testcase drill-down (coverage signal unaffected).
docker run --rm `
    -e "SONAR_HOST_URL=$SONAR_HOST_URL" `
    -e "SONAR_TOKEN=$env:SONAR_TOKEN" `
    -v "${SRC_VOLUME}:/usr/src" `
    -v "redmark-sonar-scanner-cache:/opt/sonar-scanner/.sonar" `
    $SCANNER_IMAGE `
    "-Dproject.settings=/usr/src/.cache/sonarqube/sonar-project.properties" `
    "-Dsonar.branch.name=$BRANCH" `
    "-Dsonar.scanner.skipJreProvisioning=true" `
    "-Dsonar.scm.disabled=true" `
    "-Dsonar.python.xunit.skipDetails=true" | Tee-Object -FilePath $tempLog
$scanExit = $LASTEXITCODE
docker volume rm $SRC_VOLUME 2>$null | Out-Null   # drop the snapshot
if ($scanExit -ne 0) {
    Remove-Item $tempLog -Force -ErrorAction SilentlyContinue
    throw "sonar-scanner failed (exit $scanExit)."
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
