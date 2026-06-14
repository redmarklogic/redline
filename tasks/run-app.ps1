$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot   = Split-Path -Parent $ScriptRoot

# --- Endpoints: single source of truth -------------------------------------------
# All ports/URLs for every surface live in config/dev-endpoints.json (committed,
# non-secret). This launcher is the ONLY component that reads it; app source reads
# process env only (ADR-021). The #191 Word manifest build reads the same file, so
# the addin URL can never drift from what the server binds.
# Convention: never 8000 (reserved by common tools).
$EndpointsFile = Join-Path $RepoRoot "config\dev-endpoints.json"
if (-not (Test-Path $EndpointsFile)) {
    Write-Error "Endpoints config not found at $EndpointsFile. Cannot resolve service ports."
    exit 1
}
$Endpoints  = Get-Content $EndpointsFile -Raw | ConvertFrom-Json
$Host_      = $Endpoints.host
$MarkerPort = $Endpoints.surfaces.marker.port
$DjangoPort = $Endpoints.surfaces.web.port
$AddinPort  = $Endpoints.surfaces.addin.port

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
Assert-PortFree -Port $AddinPort   -AppName "addin (Flask HTTPS)"

# --- Settings-module guard ---------------------------------------------------------
# pytest/manage.py give an inherited DJANGO_SETTINGS_MODULE precedence over repo
# config; a foreign value silently boots the wrong settings (RT-159 finding F-005).
if ($env:DJANGO_SETTINGS_MODULE -and $env:DJANGO_SETTINGS_MODULE -ne 'web.settings') {
    Write-Error "DJANGO_SETTINGS_MODULE is set to '$($env:DJANGO_SETTINGS_MODULE)' (expected unset or 'web.settings'). Unset it and retry."
    exit 1
}

# --- Load .env into process environment (ADR-021 / research.md D4) ---------------
# Application source must never load .env files (ADR-021). The launcher does it
# here so that manage.py check (below) has the required vars in the process env
# before Django's settings module is imported for the first time.
#
# Parse rules: split on the FIRST '=' only (secret values may contain '=' padding);
# skip blank lines and '#' comments; do not override vars already set in the shell.
$EnvFile = Join-Path $RepoRoot ".env"
if (Test-Path $EnvFile) {
    Write-Host "Loading .env into process environment..."
    Get-Content $EnvFile | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith('#')) {
            $idx = $line.IndexOf('=')
            if ($idx -gt 0) {
                $key   = $line.Substring(0, $idx).Trim()
                $value = $line.Substring($idx + 1)
                if (-not [System.Environment]::GetEnvironmentVariable($key)) {
                    [System.Environment]::SetEnvironmentVariable($key, $value)
                    Set-Item "Env:$key" $value
                }
            }
        }
    }
} else {
    Write-Warning ".env not found at $EnvFile. Required vars must already be in the shell environment. Copy .env.example to .env and fill in secret values."
}

# --- Database pre-flight: fail fast if Postgres is unreachable --------------------
# Connects with psycopg using the same env-var defaults as web/settings.py. A dead
# database otherwise surfaces late (mid-migrate) with a raw traceback.
Write-Host "Checking database availability..."
$dbCheck = @'
import os, sys
import psycopg
# No dev-default fallbacks: all vars are required (ADR-021 / #161 FR-006).
# The .env loader above must have supplied them before this point.
missing = [v for v in ("POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD") if not os.environ.get(v)]
if missing:
    print(f"Missing required env vars: {', '.join(missing)}. Set them in .env and retry.", file=sys.stderr)
    sys.exit(1)
try:
    psycopg.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
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
$AddinCommand   = "& { Set-Location '$RepoRoot'; `$env:ADDIN_PORT='$AddinPort'; .\.venv\Scripts\python -m addin.server }"

Start-Process pwsh -ArgumentList @("-NoExit", "-Command", $MarkerCommand) -WindowStyle Normal
Start-Process pwsh -ArgumentList @("-NoExit", "-Command", $DjangoCommand)  -WindowStyle Normal
Start-Process pwsh -ArgumentList @("-NoExit", "-Command", $AddinCommand)   -WindowStyle Normal

# --- Liveness polling ------------------------------------------------------------
function Wait-ForHealth {
    param([string]$Url, [string]$AppName, [switch]$SkipCertCheck)
    Write-Host "Waiting for $AppName at $Url ..." -NoNewline
    for ($i = 0; $i -lt 30; $i++) {
        try {
            $opts = @{ Uri = $Url; UseBasicParsing = $true; Method = 'Get'; TimeoutSec = 2; SkipHttpErrorCheck = $true }
            if ($SkipCertCheck) { $opts['SkipCertificateCheck'] = $true }
            $r = Invoke-WebRequest @opts
            if ($r.StatusCode -eq 200) { Write-Host " ready!"; return $true }
        } catch {}
        Write-Host "." -NoNewline
        Start-Sleep -Seconds 1
    }
    Write-Host ""
    Write-Warning "$AppName did not become ready after 30 seconds. Check the terminal window for errors."
    return $false
}

# URLs derived from the single-source endpoints config (scheme + health/path).
$MarkerUrl = "$($Endpoints.surfaces.marker.scheme)://${Host_}:${MarkerPort}$($Endpoints.surfaces.marker.health)"
$DjangoUrl = "$($Endpoints.surfaces.web.scheme)://${Host_}:${DjangoPort}$($Endpoints.surfaces.web.health)"
$AddinUrl  = "$($Endpoints.surfaces.addin.scheme)://${Host_}:${AddinPort}$($Endpoints.surfaces.addin.path)"

$markerReady = Wait-ForHealth -Url $MarkerUrl -AppName "marker (FastAPI)"
$djangoReady  = Wait-ForHealth -Url $DjangoUrl -AppName "web (Django)"
$addinReady   = Wait-ForHealth -Url $AddinUrl  -AppName "addin (Flask HTTPS)" -SkipCertCheck

if ($markerReady) { Start-Process "$($Endpoints.surfaces.marker.scheme)://${Host_}:${MarkerPort}/docs" }
if ($djangoReady)  { Start-Process "$($Endpoints.surfaces.web.scheme)://${Host_}:${DjangoPort}/" }
if ($addinReady)   { Start-Process $AddinUrl }

# Fail closed: callers (CI, other scripts) read the exit code (RT-159 finding F-002).
if (-not ($markerReady -and $djangoReady -and $addinReady)) { exit 1 }
