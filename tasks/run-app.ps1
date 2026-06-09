$Port = 8765
$Host_ = "127.0.0.1"

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptRoot

$AppCommand = "& { Set-Location '$RepoRoot'; .\.venv\Scripts\python -m uvicorn marker.api.main:create_app --factory --host $Host_ --port $Port --reload }"

$existing = Get-NetTCPConnection -LocalAddress $Host_ -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($existing) {
    $pid_ = $existing.OwningProcess
    Write-Host "Port $Port in use by PID $pid_. Terminating..."
    Stop-Process -Id $pid_ -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

Start-Process pwsh -ArgumentList @("-NoExit", "-Command", $AppCommand) -WindowStyle Normal

$Url = "http://${Host_}:$Port"

Write-Host "Waiting for app at $Url ..." -NoNewline
$MaxAttempts = 30
$Ready = $false
for ($Attempt = 0; $Attempt -lt $MaxAttempts; $Attempt++) {
    try {
        $response = Invoke-WebRequest -Uri "$Url/health" -UseBasicParsing -Method Get -TimeoutSec 2 -SkipHttpErrorCheck
        if ($response) {
            $Ready = $true
            break
        }
    } catch {
        # connection refused — server not up yet
    }
    Write-Host "." -NoNewline
    Start-Sleep -Seconds 1
}

if ($Ready) {
    Write-Host " ready! Opening browser."
    Start-Process "$Url/docs"
} else {
    Write-Host ""
    Write-Warning "App did not become ready after $MaxAttempts seconds. Check the uvicorn terminal window for errors."
}
