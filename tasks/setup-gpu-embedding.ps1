# setup-gpu-embedding.ps1 - Offload CCE embeddings to the NVIDIA GPU via Ollama
# Called by setup.ps1 or run standalone: .\tasks\setup-gpu-embedding.ps1
#
# What this does (idempotent, skips gracefully on machines without NVIDIA GPU):
#   - Detects NVIDIA GPU + modern driver (nvidia-smi in System32)
#   - Installs Ollama via winget if missing, starts it, pulls nomic-embed-text
#   - Sets user env var CCE_EMBED_BACKEND=ollama (consumed by context_engine/config.py)
#
# Why: CCE's default fastembed backend embeds in-process on CPU (~3 cores during
# indexing, one model copy per `cce serve` instance). The Ollama backend moves
# embedding to one shared GPU service (~500 MB VRAM, nomic-embed-text).
#
# After first enabling on a machine: run `cce index --full` in each project
# (vector dimensions change 384 -> 768) and restart Claude Code sessions so
# `cce serve` picks up the env var.

param([switch]$Quiet)

function Write-Step { param([string]$msg) if (-not $Quiet) { Write-Host "`n>> $msg" -ForegroundColor Cyan } }
function Write-OK   { param([string]$msg) Write-Host "   OK  $msg" -ForegroundColor Green }
function Write-Skip { param([string]$msg) if (-not $Quiet) { Write-Host "   --  $msg" -ForegroundColor DarkGray } }
function Write-Warn { param([string]$msg) Write-Host "   !!  $msg" -ForegroundColor Yellow }

# 1. NVIDIA GPU present?
Write-Step "Checking for NVIDIA GPU"
$gpu = Get-CimInstance Win32_VideoController -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match 'NVIDIA' } | Select-Object -First 1
if (-not $gpu) {
    Write-Skip "No NVIDIA GPU - keeping CPU (fastembed) backend. Nothing to do."
    return
}
Write-Skip "$($gpu.Name)"

# 2. Modern driver? (modern drivers install nvidia-smi into System32; the 2018-era
#    391.xx driver only has the legacy NVSMI copy and supports CUDA 9 at most)
Write-Step "Checking NVIDIA driver"
$smi = "$env:SystemRoot\System32\nvidia-smi.exe"
if (-not (Test-Path $smi)) {
    Write-Warn "Driver too old for CUDA workloads (no System32\nvidia-smi.exe)."
    Write-Warn "Update first: https://www.nvidia.com/Download/index.aspx (DCH driver for your GPU)."
    Write-Warn "If NVIDIA setup.exe refuses silently (exit 0xE4000008), extract with"
    Write-Warn "  tar -xf <installer>.exe -C <dir> Display.Driver"
    Write-Warn "and install the matching OEM INF via: pnputil /add-driver <inf> /install"
    Write-Warn "Then re-run this script."
    return
}
$drv = (& $smi --query-gpu=driver_version --format=csv,noheader) 2>$null
Write-Skip "driver $drv"

# 3. Ollama installed?
Write-Step "Checking Ollama"
$ollama = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
if (-not (Test-Path $ollama)) {
    $cmd = Get-Command ollama -ErrorAction SilentlyContinue
    if ($cmd) { $ollama = $cmd.Source }
}
if (-not (Test-Path $ollama)) {
    winget install --id Ollama.Ollama --accept-source-agreements --accept-package-agreements --silent | Out-Null
    if (-not (Test-Path "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe")) {
        Write-Warn "winget install failed - install manually from https://ollama.com/download"
        return
    }
    $ollama = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
    Write-OK "Ollama installed"
} else {
    Write-Skip "Ollama at $ollama"
}

# 4. Server running + embedding model present
Write-Step "Checking Ollama server + nomic-embed-text"
try {
    Invoke-RestMethod 'http://localhost:11434/api/tags' -TimeoutSec 2 | Out-Null
} catch {
    Start-Process $ollama -ArgumentList 'serve' -WindowStyle Hidden
    Start-Sleep -Seconds 4
}
$models = (& $ollama list) 2>$null
if ($models -match 'nomic-embed-text') {
    Write-Skip "nomic-embed-text already pulled"
} else {
    & $ollama pull nomic-embed-text
    Write-OK "nomic-embed-text pulled (~274 MB)"
}

# 5. CCE backend switch (user-level env var; new shells/sessions inherit it)
Write-Step "Setting CCE_EMBED_BACKEND=ollama"
$current = [System.Environment]::GetEnvironmentVariable('CCE_EMBED_BACKEND', 'User')
if ($current -eq 'ollama') {
    Write-Skip "already set"
} else {
    [System.Environment]::SetEnvironmentVariable('CCE_EMBED_BACKEND', 'ollama', 'User')
    Write-OK "set (new terminals/sessions inherit it)"
    Write-Warn "Run 'cce index --full' in each project (vector dims change 384 -> 768)"
    Write-Warn "and restart Claude Code sessions so cce serve picks up the new backend."
}

Write-OK "GPU embedding ready. Verify with: ollama ps  (PROCESSOR column should say GPU)"
