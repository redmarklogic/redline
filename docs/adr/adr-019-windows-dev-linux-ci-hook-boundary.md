# ADR-019: Windows-dev / Linux Deployment Platform Boundary

## Summary

Development happens on Windows; CI and production run on Ubuntu Linux. This ADR
records the platform matrix for every artifact category in this project — which
artifacts must be Linux-compatible, which must be cross-platform, and which are
legitimately Windows-only — and the implementation rules that follow from each
classification (accepted 2026-06-09).

**Deciders**: Peter (architecture)

## Status

Accepted — 2026-06-09

## Decision

Every artifact in this project has a deployment context. The platform obligation
follows from that context, not from where the artifact was authored. Three classes
exist:

| Artifact class | Dev (Windows) | CI / Production (Linux) | Platform obligation |
|---|---|---|---|
| Application code | authored | executes | Linux-compatible (Python stdlib only, POSIX paths, LF line endings) |
| Enforcement hooks | executes | executes | Cross-platform (Python — runs on both) |
| Claude Code hooks | executes | never executes | Windows-only (PowerShell `.ps1`) |
| Dev convenience scripts | executes | never executes | Windows-only |

The failure mode this ADR prevents: confusing *where an artifact is authored* with
*where it must run*. Application code runs on Linux — it must be Linux-compatible
regardless of the author's workstation. Claude Code hooks run only on a Windows
developer's machine — they carry no Linux portability obligation.

## Context

This project develops on Windows and runs CI and production on Ubuntu Linux. Two
incidents surfaced the need for an explicit platform policy:

1. A module (`rl.greeting`) was deleted on Windows but its import statement in the
   package initialiser was not removed. CI caught it on a fresh Linux checkout; the
   local Windows environment did not, because a stale virtual environment masked the
   missing module. Application code cannot rely on Windows-local state; it must be
   clean on a fresh Linux checkout.

2. The CCE health-gate hook test created a `.bat` fake binary. On Linux CI, PowerShell
   does not recognise `.bat` files, causing the hook to crash with an unset
   `USERPROFILE` environment variable. The root cause: the test and hook were written
   against a Windows runtime that CI does not provide. CCE (Code Context Engine) is a
   developer tool — it is never installed in CI or production.

Both failures stem from the same gap: no documented policy for which artifacts must
run on Linux, which must run on both, and which are Windows-only.

## Principles

### P0 — Platform obligation is set by deployment context, not authoring context

The platform an artifact is *authored on* is irrelevant to its compatibility
requirement. Only *where it executes* determines the obligation:

- Executes on Linux (in CI or production) → must be Linux-compatible.
- Executes on both → must be cross-platform.
- Executes only on Windows (dev-session guards) → Windows-only is correct and
  intentional; no portability obligation.

### P1 — Application code is Linux-compatible

All application code under the project source directory deploys to and executes on
Linux. Authors on Windows must ensure compatibility:

- Use `pathlib.Path` for all file-system operations; never construct paths with
  backslash literals.
- Use only Python standard library or explicitly cross-platform third-party packages.
- Do not reference Windows-only environment variables (`USERPROFILE`, `APPDATA`,
  `LOCALAPPDATA`) without a `HOME`/`XDG_*` fallback.
- Line endings: LF only in committed source files (enforced by `.gitattributes`).

CI is the authoritative compatibility gate. A test that passes locally on Windows
but fails on Linux CI is a Windows-local defect — fix the code, not the CI config.

### P2 — Enforcement hooks are cross-platform

Pre-commit hooks run on both developer machines (Windows) and CI (Linux). They are
Python scripts; Python's cross-platform behaviour applies. Authors must not use
Windows path separators, `os.sep` assumptions, or subprocess calls to Windows-only
binaries inside these hooks.

### P3 — Claude Code hooks are Windows PowerShell by design

Claude Code hooks gate agent actions. Claude Code on this project runs on Windows.
`.ps1` is the correct and only hook language. This is a deliberate scope boundary,
not a portability gap.

Do not add shell (`#!/bin/sh`) counterparts or CI compatibility shims for hooks
that are exclusively dev-session guards.

### P4 — Dev-only hook tests skip on non-Windows

Hook tests that exercise Windows-specific dev tooling (CCE, Windows-only env vars,
`.bat` fake binaries) must use:

```python
pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="<hook name> is a Windows-dev hook; <tool> is not a CI/Linux concern",
)
```

The legacy pattern (`shutil.which("powershell") is None and shutil.which("pwsh") is
None`) must not be used for dev-only hooks — `pwsh` is present on Ubuntu runners and
causes the test to run in an unsupported environment.

Hook tests that exercise platform-neutral PowerShell logic (no Windows env vars, no
`.bat` binaries) may retain the `pwsh`-presence guard if CI coverage is genuinely
valuable.

### P5 — Hook scripts must guard Windows-only env vars

When a `.ps1` hook references `USERPROFILE` (Windows-only), it must provide a
`HOME` fallback so the script does not crash on Linux if it ever runs there
incidentally:

```powershell
$userHome = if ($env:USERPROFILE) { $env:USERPROFILE } `
            elseif ($env:HOME)     { $env:HOME }        `
            else                   { $null }
if ($userHome) { $cce = Join-Path $userHome ".local/bin/cce" }
```

Additionally, `Write-Error` inside a `catch` block must use `-ErrorAction Continue`
to prevent re-throwing when `$ErrorActionPreference = 'Stop'` is active:

```powershell
catch {
    Write-Error "hook error: $_" -ErrorAction Continue
    exit 0  # fail open
}
```

## Options Considered

- **Option A — Single platform (Linux everywhere).** Develop on Linux or WSL; align
  dev and CI environments. Rejected: the project toolchain (Claude Code, local Windows
  scripts) is Windows-native. Forcing WSL adds friction with no deployment benefit.

- **Option B — Full cross-platform for all artifacts.** Port Claude Code hooks to
  Python or POSIX shell. Rejected: Claude Code hooks run in a Claude Code session on
  Windows; the runtime is PowerShell. Porting introduces maintenance overhead with no
  production benefit — these hooks never run in production or CI.

- **Option C — Explicit platform matrix per artifact class (chosen).** Application
  code must be Linux-compatible (it deploys there). Enforcement hooks must be
  cross-platform (they run on both). Claude Code hooks are Windows-only (they never
  reach CI or production). Each class has a clear, minimal obligation. No one class
  borrows the other's constraints.

## Decision Rationale

Option C matches actual deployment reality. The platform obligation is a consequence
of where an artifact runs — imposing Linux compatibility on dev-session tools that
never leave a Windows machine is waste; failing to impose it on application code that
runs on Linux is a defect. The platform matrix makes both explicit.

## Consequences

- All application code must use `pathlib.Path`, avoid Windows-only env vars, and pass
  CI on a fresh Linux checkout. Windows-local state (stale virtual environment,
  locally-installed packages) is not a valid reason for a test to pass locally but
  fail on CI.
- Pre-commit enforcement hooks must remain cross-platform Python.
- New Claude Code hook tests for dev-only tools must use `sys.platform != "win32"`.
- Hook authors must guard `USERPROFILE` with a `HOME` fallback per P5.
- `Write-Error` inside `catch` blocks must specify `-ErrorAction Continue`.
- The CCE health-gate hook retains its Windows-only behaviour; no cross-platform
  changes are required to the hook itself.

## References

- [ADR-011](adr-011-hook-first-enforcement.md) — Hook-first Enforcement (parent; this
  ADR extends the hook boundary definition with dev/CI scoping rules)
