# Fixed ports — project convention (never 8000; that port is reserved by common tools).
# marker (FastAPI): 8765   web (Django): 8766
# If either port is occupied by any process, the script fails. Free it manually.
$MarkerPort = 8765
$DjangoPort  = 8766
$Host_       = "127.0.0.1"

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot   = Split-Path -Parent $ScriptRoot

# --- Port guard: fail hard if occupied -------------------------------------------
function Assert-PortFree {
    param([int]$Port, [string]$AppName)
    $occupied = Get-NetTCPConnection -LocalAddress $Host_ -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($occupied) {
        Write-Error "Port $Port (reserved for $AppName) is already in use by PID $($occupied.OwningProcess). Free it manually and retry."
        exit 1
    }
}

Assert-PortFree -Port $MarkerPort -AppName "marker (FastAPI)"
Assert-PortFree -Port $DjangoPort  -AppName "web (Django)"

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
