# setup-superpowers.ps1 - Apply Redline overrides after Superpowers install or update
# Called by setup.ps1 or run standalone: .\tasks\setup-superpowers.ps1
#
# Superpowers ships writing-plans and executing-plans, which conflict with Redline's
# Spec-Kit planning pipeline. This script removes them after every install or update
# so they can never be invoked accidentally.
#
# Run this again after any `obra/superpowers` update.

param([switch]$Quiet)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Step { param([string]$msg) if (-not $Quiet) { Write-Host "`n>> $msg" -ForegroundColor Cyan } }
function Write-OK   { param([string]$msg) Write-Host "   OK  $msg" -ForegroundColor Green }
function Write-Skip { param([string]$msg) if (-not $Quiet) { Write-Host "   --  $msg" -ForegroundColor DarkGray } }

$agentsSkillsDir = ".agents\skills"

# These Superpowers skills conflict with Redline's Spec-Kit pipeline.
# writing-plans  → use speckit.plan + speckit.tasks instead
# executing-plans → use subagent-driven-development with specs/NNN/tasks.md instead
$skillsToRemove = @("writing-plans", "executing-plans")

Write-Step "Removing superseded Superpowers skills"
foreach ($skill in $skillsToRemove) {
    $path = Join-Path $agentsSkillsDir $skill
    if (Test-Path $path) {
        Remove-Item $path -Recurse -Force
        Write-OK "Removed $skill"
    } else {
        Write-Skip "$skill already absent"
    }
}
