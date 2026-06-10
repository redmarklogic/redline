#Requires -Version 7
<#
.SYNOPSIS
    Reclaim RAM from stale Claude Code (VS Code extension) sessions.

.DESCRIPTION
    Each Claude Code tab keeps a full process tree alive even when idle:
        claude.exe  (~200-400 MB)
        + 2x CCE python MCP servers   (0.3 - 1.8 GB!)
        + 2x context7 node MCP procs  (~80 MB)
        + cmd/conhost shells
    This script lists every session tree with age and RAM, then (with -Apply)
    kills trees older than -MaxAgeHours. The session running this script is
    always protected. Killed sessions are recoverable via /resume in VS Code
    (transcripts live on disk).

.EXAMPLE
    pwsh -File Optimize-ClaudeRAM.ps1                  # dry run: report only
    pwsh -File Optimize-ClaudeRAM.ps1 -Apply           # kill sessions idle > 2h
    pwsh -File Optimize-ClaudeRAM.ps1 -Apply -All      # kill all except current
    pwsh -File Optimize-ClaudeRAM.ps1 -Apply -MaxAgeHours 0.5
#>
param(
    [switch]$Apply,                    # actually kill (default: dry run)
    [double]$MaxAgeHours = 2,          # sessions older than this are targets
    [switch]$All,                      # ignore age: target every unprotected session
    [double]$IdleSampleSeconds = 5,    # CPU sampling window for the idle guard
    [double]$CpuBusyThreshold = 0.5,   # tree CPU-seconds within window that counts as "active"
    [switch]$SkipIdleCheck             # kill by age alone (not recommended unattended)
)

$ErrorActionPreference = 'Stop'

# --- snapshot all processes once ---
$procs = Get-CimInstance Win32_Process
$byId = @{}
$children = @{}
foreach ($p in $procs) {
    $byId[$p.ProcessId] = $p
    if (-not $children.ContainsKey($p.ParentProcessId)) {
        $children[$p.ParentProcessId] = [System.Collections.Generic.List[object]]::new()
    }
    $children[$p.ParentProcessId].Add($p)
}

function Get-Subtree([uint32]$ProcId) {
    $seen = [System.Collections.Generic.HashSet[uint32]]::new()
    $result = [System.Collections.Generic.List[object]]::new()
    $queue = [System.Collections.Generic.Queue[uint32]]::new()
    $queue.Enqueue($ProcId)
    while ($queue.Count) {
        $id = $queue.Dequeue()
        if (-not $seen.Add($id)) { continue }
        if ($byId.ContainsKey($id)) { $result.Add($byId[$id]) }
        if ($children.ContainsKey($id)) {
            foreach ($c in $children[$id]) { $queue.Enqueue($c.ProcessId) }
        }
    }
    return $result
}

# --- protect the session this script runs inside (if any) ---
$protected = [System.Collections.Generic.HashSet[uint32]]::new()
$cur = $byId[[uint32]$PID]
$hops = 0
while ($cur -and $hops++ -lt 50) {
    if ($cur.Name -eq 'claude.exe') {
        foreach ($p in (Get-Subtree $cur.ProcessId)) { [void]$protected.Add($p.ProcessId) }
        break
    }
    $cur = $byId[$cur.ParentProcessId]
}

# --- evaluate each claude.exe session tree ---
$now = Get-Date
$report = foreach ($s in ($procs | Where-Object Name -eq 'claude.exe')) {
    $tree = Get-Subtree $s.ProcessId
    $ramMB = [math]::Round((($tree | Measure-Object WorkingSetSize -Sum).Sum) / 1MB)
    $age = if ($s.CreationDate) { ($now - $s.CreationDate).TotalHours } else { 999 }
    $isProt = $protected.Contains($s.ProcessId)
    [PSCustomObject]@{
        PID      = $s.ProcessId
        AgeHours = [math]::Round($age, 1)
        Procs    = $tree.Count
        RAM_MB   = $ramMB
        Status   = if ($isProt) { 'CURRENT (protected)' }
                   elseif ($All -or $age -gt $MaxAgeHours) { 'KILL' }
                   else { 'keep (young)' }
        Tree     = $tree
    }
}

$report | Sort-Object RAM_MB -Descending |
    Format-Table PID, AgeHours, Procs, RAM_MB, Status -AutoSize

$targets = @($report | Where-Object Status -eq 'KILL')

# --- idle guard: never kill a tree that is actively burning CPU ---
if ($targets -and -not $SkipIdleCheck) {
    $allIds = @($targets.Tree.ProcessId | ForEach-Object { [int]$_ })
    $s0 = @{}; Get-Process -Id $allIds -ErrorAction SilentlyContinue | ForEach-Object { $s0[$_.Id] = $_.CPU }
    Start-Sleep -Seconds $IdleSampleSeconds
    $s1 = @{}; Get-Process -Id $allIds -ErrorAction SilentlyContinue | ForEach-Object { $s1[$_.Id] = $_.CPU }
    foreach ($t in $targets) {
        $delta = 0.0
        foreach ($p in $t.Tree) {
            $id = [int]$p.ProcessId
            if ($s1.ContainsKey($id) -and $s0.ContainsKey($id)) { $delta += ($s1[$id] - $s0[$id]) }
        }
        if ($delta -gt $CpuBusyThreshold) {
            $t.Status = "skip (active: {0:N1}s CPU/{1}s)" -f $delta, $IdleSampleSeconds
        }
    }
    $targets = @($targets | Where-Object Status -eq 'KILL')
}

$totalMB = [int](($targets | Measure-Object RAM_MB -Sum).Sum)
"{0} session(s) targeted, ~{1:N0} MB reclaimable" -f $targets.Count, $totalMB

if (-not $Apply) {
    "`nDRY RUN - nothing killed. Re-run with -Apply to reclaim."
    return
}

foreach ($t in $targets) {
    # children first, claude.exe last
    foreach ($p in ($t.Tree | Sort-Object { $_.ProcessId -eq $t.PID })) {
        try { Stop-Process -Id $p.ProcessId -Force -ErrorAction Stop } catch {}
    }
    "Killed session $($t.PID) (~$($t.RAM_MB) MB, $($t.Procs) procs)"
}

Start-Sleep -Seconds 2
$os = Get-CimInstance Win32_OperatingSystem
"Free RAM now: {0:N1} GB (was target ~{1:N1} GB reclaimed)" -f ($os.FreePhysicalMemory / 1MB), ($totalMB / 1024)
