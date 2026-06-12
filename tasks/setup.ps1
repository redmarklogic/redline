# setup.ps1 - First-time repo setup
# Run once after cloning: .\tasks\setup.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$root = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }

function Write-Banner { param([string]$msg) Write-Host "`n===  $msg  ===" -ForegroundColor Yellow }

Write-Host "Redline - dev environment setup" -ForegroundColor White

# Install Python deps
Write-Banner "Python dependencies"
uv sync
Write-Host "   OK  uv sync complete" -ForegroundColor Green

# speckit (Spec Kit / specify CLI + Claude Code integration)
Write-Banner "Spec Kit"
& "$root\setup-speckit.ps1"

# Superpowers overrides (remove vendor skills that conflict with Spec-Kit pipeline)
Write-Banner "Superpowers overrides"
& "$root\setup-superpowers.ps1"

# CCE (Code Context Engine MCP server)
Write-Banner "Code Context Engine"
& "$root\setup-cce.ps1"

# GPU embedding offload (optional - skips on machines without NVIDIA GPU)
Write-Banner "GPU embedding (Ollama)"
& "$root\setup-gpu-embedding.ps1"

Write-Host "`nAll done. Restart Claude Code to activate the CCE MCP server.`n" -ForegroundColor Yellow
