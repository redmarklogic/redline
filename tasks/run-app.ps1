# Fixed ports — project convention (never 8000; that port is reserved by common tools).
# marker (FastAPI): 8765   web (Django): 8766
# If either port is occupied by any process, the script fails. Free it manually.
$MarkerPort = 8765
$DjangoPort  = 8766
$Host_       = "127.0.0.1"

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot   = Split-Path -Parent $ScriptRoot

# --- Port guard: fail hard if occupied -------------------------------------------
# No -LocalAddress filter: a wildcard bind (0.0.0.0 / ::) occupies the port just as
# hard as a loopback bind and must trip the guard (RT-159 finding F-002).
function Assert-PortFree {
    param([int]$Port, [string]$AppName)
    $occupied = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($occupied) {
        $pids = ($occupied.OwningProcess | Select-Object -Unique) -join ', '
        Write-Error "Port $Port (reserved for $AppName) is already in use by PID $pids. Free it manually and retry."
        exit 1
    }
}

Assert-PortFree -Port $MarkerPort -AppName "marker (FastAPI)"
Assert-PortFree -Port $DjangoPort  -AppName "web (Django)"

# --- Settings-module guard ---------------------------------------------------------
# pytest/manage.py give an inherited DJANGO_SETTINGS_MODULE precedence over repo
# config; a foreign value silently boots the wrong settings (RT-159 finding F-005).
if ($env:DJANGO_SETTINGS_MODULE -and $env:DJANGO_SETTINGS_MODULE -ne 'web.settings') {
    Write-Error "DJANGO_SETTINGS_MODULE is set to '$($env:DJANGO_SETTINGS_MODULE)' (expected unset or 'web.settings'). Unset it and retry."
    exit 1
}

# --- Database pre-flight: fail fast if Postgres is unreachable --------------------
# Connects with psycopg using the same env-var defaults as web/settings.py. A dead
# database otherwise surfaces late (mid-migrate) with a raw traceback.
Write-Host "Checking database availability..."
$dbCheck = @'
import os, sys
import psycopg
try:
    psycopg.connect(
        host=os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        port=os.environ.get("POSTGRES_PORT", "5433"),
        dbname=os.environ.get("POSTGRES_DB", "redline"),
        user=os.environ.get("POSTGRES_USER", "redline"),
        password=os.environ.get("POSTGRES_PASSWORD", "redline"),
        connect_timeout=3,
    ).close()
except psycopg.OperationalError as exc:
    print(f"Database unreachable: {exc}", file=sys.stderr)
    sys.exit(1)
'@
& "$RepoRoot\.venv\Scripts\python" -c $dbCheck
if ($LASTEXITCODE -ne 0) {
    Write-Error @"
PostgreSQL is not available. The Django app cannot start without its database.
Spin it up with:

    docker compose up -d db

then wait a few seconds for the container healthcheck and re-run this script.
"@
    exit 1
}
Write-Host "Database reachable."

# --- Django pre-flight: log-analysis gate ----------------------------------------
# manage.py check runs synchronously and validates all installed apps, URL patterns,
# and settings before any socket opens. Non-zero exit = abort before touching ports.
Write-Host "Running Django system check..."
$checkOutput = & "$RepoRoot\.venv\Scripts\python" "$RepoRoot\manage.py" check 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Django system check failed. Fix the errors below, then retry."
    Write-Host ($checkOutput | Out-String)
    exit 1
}
Write-Host ($checkOutput | Out-String)

# --- Database migrations -----------------------------------------------------------
# Postgres runs in docker-compose (`db` service); a fresh clone has an empty
# database. migrate is idempotent: creates schema on first run, no-ops after.
Write-Host "Applying database migrations..."
$migrateOutput = & "$RepoRoot\.venv\Scripts\python" "$RepoRoot\manage.py" migrate --no-input 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Database migration failed. Is the Postgres container running? Start it with: docker compose up -d db"
    Write-Host ($migrateOutput | Out-String)
    exit 1
}
Write-Host ($migrateOutput | Out-String)

# --- Start both servers -----------------------------------------------------------
$MarkerCommand = "& { Set-Location '$RepoRoot'; .\.venv\Scripts\python -m uvicorn marker.api.main:create_app --factory --host $Host_ --port $MarkerPort --reload }"
$DjangoCommand  = "& { Set-Location '$RepoRoot'; .\.venv\Scripts\python manage.py runserver ${Host_}:${DjangoPort} }"

Start-Process pwsh -ArgumentList @("-NoExit", "-Command", $MarkerCommand) -WindowStyle Normal
Start-Process pwsh -ArgumentList @("-NoExit", "-Command", $DjangoCommand)  -WindowStyle Normal

# --- Liveness polling ------------------------------------------------------------
function Wait-ForHealth {
    param([string]$Url, [string]$AppName)
    Write-Host "Waiting for $AppName at $Url ..." -NoNewline
    for ($i = 0; $i -lt 30; $i++) {
        try {
            $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -Method Get -TimeoutSec 2 -SkipHttpErrorCheck
            if ($r.StatusCode -eq 200) { Write-Host " ready!"; return $true }
        } catch {}
        Write-Host "." -NoNewline
        Start-Sleep -Seconds 1
    }
    Write-Host ""
    Write-Warning "$AppName did not become ready after 30 seconds. Check the terminal window for errors."
    return $false
}

$markerReady = Wait-ForHealth -Url "http://${Host_}:${MarkerPort}/health"  -AppName "marker (FastAPI)"
$djangoReady  = Wait-ForHealth -Url "http://${Host_}:${DjangoPort}/health/" -AppName "web (Django)"

if ($markerReady) { Start-Process "http://${Host_}:${MarkerPort}/docs" }
if ($djangoReady)  { Start-Process "http://${Host_}:${DjangoPort}/" }

# Fail closed: callers (CI, other scripts) read the exit code (RT-159 finding F-002).
if (-not ($markerReady -and $djangoReady)) { exit 1 }
