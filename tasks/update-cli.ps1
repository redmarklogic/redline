# update-cli.ps1 - Install or update project CLI tools
# Run: .\tasks\update-cli.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "SilentlyContinue"

$results = @()

function Test-CommandExists([string]$cmd) {
    return $null -ne (Get-Command $cmd -ErrorAction SilentlyContinue)
}

function Test-Auth([string]$name, [scriptblock]$check, [string]$hint) {
    try {
        $out = & $check 2>&1
        if ($LASTEXITCODE -ne 0) { throw $out }
        Write-Host "  Auth OK  $name" -ForegroundColor Green
    } catch {
        Write-Host "  NOT AUTHENTICATED  $name" -ForegroundColor Red
        Write-Host "  -> $hint" -ForegroundColor Yellow
    }
}

# ── CLI definitions ──────────────────────────────────────────────────────────
$cliTools = @(
    @{
        Name      = "GitHub CLI"
        Cmd       = "gh"
        Update    = { gh upgrade --all 2>&1 }
        Install   = { winget install --id GitHub.cli --silent --accept-package-agreements --accept-source-agreements 2>&1 }
        AuthCheck = { gh auth status 2>&1; $LASTEXITCODE }
        AuthHint  = "Run: gh auth login"
    }
    @{
        Name    = "Google Workspace CLI"
        Cmd     = "gws"
        Install = {
            $tmp = "$env:TEMP\gws-install"
            New-Item -ItemType Directory -Force $tmp | Out-Null
            $url = "https://github.com/googleworkspace/cli/releases/latest/download/google-workspace-cli-x86_64-pc-windows-msvc.zip"
            $zip = "$tmp\gws.zip"
            Invoke-WebRequest -Uri $url -OutFile $zip -ErrorAction Stop
            Expand-Archive -Path $zip -DestinationPath $tmp -Force
            $dest = "$env:USERPROFILE\.local\bin"
            New-Item -ItemType Directory -Force $dest | Out-Null
            Copy-Item "$tmp\gws.exe" "$dest\gws.exe" -Force
            $env:PATH = "$dest;$env:PATH"
            "Installed to $dest\gws.exe"
        }
        Update  = {
            $tmp = "$env:TEMP\gws-install"
            New-Item -ItemType Directory -Force $tmp | Out-Null
            $url = "https://github.com/googleworkspace/cli/releases/latest/download/google-workspace-cli-x86_64-pc-windows-msvc.zip"
            $zip = "$tmp\gws.zip"
            Invoke-WebRequest -Uri $url -OutFile $zip -ErrorAction Stop
            Expand-Archive -Path $zip -DestinationPath $tmp -Force
            $dest = Split-Path (Get-Command gws).Source
            Copy-Item "$tmp\gws.exe" "$dest\gws.exe" -Force
            "Updated in $dest"
        }
        AuthCheck = { gws auth status 2>&1; $LASTEXITCODE }
        AuthHint  = "Run: gws auth login"
    }
    @{
        Name      = "GCP CLI (gcloud)"
        Cmd       = "gcloud"
        Update    = { gcloud components update --quiet 2>&1 }
        AuthCheck = { gcloud auth list 2>&1; $LASTEXITCODE }
        AuthHint  = "Run: gcloud auth login (add --update-adc for Application Default Credentials)"
        Install   = {
            $tmp = "$env:TEMP\gcloud-install"
            New-Item -ItemType Directory -Force $tmp | Out-Null
            $url = "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-windows-x86_64.zip"
            $zip = "$tmp\gcloud.zip"
            Invoke-WebRequest -Uri $url -OutFile $zip -ErrorAction Stop
            Expand-Archive -Path $zip -DestinationPath "$env:USERPROFILE\google-cloud-sdk" -Force
            & "$env:USERPROFILE\google-cloud-sdk\google-cloud-sdk\install.bat" --quiet 2>&1
            "Installed. Restart shell for PATH changes to take effect."
        }
    }
)

# ── Loop ─────────────────────────────────────────────────────────────────────
foreach ($tool in $cliTools) {
    $name = $tool.Name
    $cmd  = $tool.Cmd
    Write-Host "`n[$name]" -ForegroundColor Cyan

    if (Test-CommandExists $cmd) {
        # Installed — try to update
        $updateFn = if ($tool.Update) { $tool.Update } elseif ($tool.CheckUpdate) { $tool.CheckUpdate } else { $null }

        if ($null -ne $updateFn) {
            try {
                $out = & $updateFn
                Write-Host "  Updated $name" -ForegroundColor Green
                $results += "  Updated       $name"
            } catch {
                Write-Host "  Skipped $name (update check failed: $_)" -ForegroundColor Yellow
                $results += "  Skipped       $name"
            }
        } else {
            Write-Host "  Skipped $name (no update mechanism defined)" -ForegroundColor Yellow
            $results += "  Skipped       $name"
        }
    } else {
        # Not installed — install
        try {
            $out = & $tool.Install
            if (Test-CommandExists $cmd) {
                Write-Host "  Installed $name" -ForegroundColor Green
                $results += "  Installed     $name"
            } else {
                Write-Host "  Installed $name (binary may require a new shell to be on PATH)" -ForegroundColor Green
                $results += "  Installed     $name  (restart shell to use)"
            }
        } catch {
            Write-Host "  Failed to install $name : $_" -ForegroundColor Red
            $results += "  Failed        $name"
        }
    }

    # Auth check (runs regardless of install/update outcome, skipped if binary still absent)
    if ($tool.AuthCheck -and (Test-CommandExists $cmd)) {
        Test-Auth $name $tool.AuthCheck $tool.AuthHint
    }
}

# ── Summary ───────────────────────────────────────────────────────────────────
Write-Host "`n════════════════════════════════" -ForegroundColor White
Write-Host " Summary" -ForegroundColor White
Write-Host "════════════════════════════════" -ForegroundColor White
$results | ForEach-Object { Write-Host $_ }
Write-Host ""
