# ADR-019: Windows-dev / Linux-CI Hook Boundary

## Summary

Claude Code hooks under `.claude/hooks/` are Windows PowerShell (`.ps1`) by design.
CI runs on Ubuntu Linux. This ADR records the boundary, its rationale, and the three
rules every hook author must follow to keep tests passing on CI without compromising
the dev-time contract (accepted 2026-06-09).

**Status**: Accepted
**Date**: 2026-06-09
**Deciders**: Peter (architecture), Harel Lustiger (founder)

---

## Decision

Claude Code hooks are Windows-only PowerShell scripts. They are development-session
tools — they gate the agent's actions on a developer's machine. They are not deployed
to production and must not be expected to run on Linux CI as a hard requirement.

Hook tests that verify Windows-specific dev-time behaviour must skip on non-Windows
platforms. When a hook depends on a Windows-only environment variable, the hook must
guard the fallback path rather than crash — but CI portability is a convenience, not
a first-class obligation for hooks that are inherently Windows-scoped.

---

## Context

This project develops on Windows and runs CI on Ubuntu Linux. The CCE health-gate
hook (`.claude/hooks/cce-health-gate.ps1`) tests revealed two failure modes:

1. `$env:USERPROFILE` is unset on Linux; `Join-Path $env:USERPROFILE ...` throws a
   terminating error, which the catch block then re-throws because `$ErrorActionPreference`
   is still `'Stop'` inside the handler — producing a non-zero exit with empty stdout
   instead of the intended `ask` decision.

2. The hook test (`tests/.agents/hooks/test_cce_health_gate.py`) created a `cce.bat`
   fake binary. On Linux, `pwsh` does not recognise `.bat` files, so the fake was
   invisible and the hook followed a crash path instead of the test's intended one.

The root cause in both cases is the same: the hook and its test assumed a Windows
runtime that CI does not provide. CCE (Code Context Engine) is a developer tool — it
is never installed in CI or production. There is no value in running CCE hook tests
on Linux CI beyond incidental coverage of platform-neutral scripting patterns.

---

## Principles

### P1 — `.claude/hooks/` scripts are Windows PowerShell by design

Hooks under `.claude/hooks/` gate Claude Code agent actions. Claude Code on this
project runs on Windows. `.ps1` is the correct and only hook language. This is a
deliberate scope boundary, not a portability gap.

Do not add shell (`#!/bin/sh`) counterparts or CI compatibility shims for hooks
that are exclusively dev-session guards.

### P2 — Dev-only hook tests skip on non-Windows

Hook tests under `tests/.agents/hooks/` that exercise Windows-specific dev tooling
(CCE, Windows-only env vars, `.bat` fake binaries) must use:

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

### P3 — Hook scripts must guard Windows-only env vars

When a `.ps1` hook references `$env:USERPROFILE` (Windows-only), it must provide a
`$HOME` fallback so the script fails gracefully on Linux if it ever runs there
incidentally (e.g., in a local Linux dev environment):

```powershell
$userHome = if ($env:USERPROFILE) { $env:USERPROFILE } `
            elseif ($env:HOME)     { $env:HOME }        `
            else                   { $null }
if ($userHome) { $cce = Join-Path $userHome ".local/bin/cce" }
```

Additionally, `Write-Error` inside a `catch` block must use `-ErrorAction Continue`
or an equivalent to prevent re-throwing when `$ErrorActionPreference = 'Stop'` is
active in the outer scope:

```powershell
catch {
    Write-Error "hook error: $_" -ErrorAction Continue
    exit 0  # fail open
}
```

---

## Options Considered

- **Option A — Make all hooks cross-platform.** Port hooks to POSIX shell or Python.
  Rejected: Claude Code hooks run in a Claude Code session on Windows; the runtime is
  PowerShell. Porting introduces maintenance overhead with zero production benefit.

- **Option B — Skip all hook tests on Linux CI.** Apply `sys.platform != "win32"` to
  every hook test regardless of content. Rejected: hooks that exercise platform-neutral
  logic (JSON parsing, exit-code routing) can run on Linux CI and provide useful
  coverage. Blanket skipping loses that signal.

- **Option C — Skip only dev-tool-specific hook tests on Linux (chosen).** Tests that
  depend on Windows-only infrastructure (CCE, `USERPROFILE`, `.bat` binaries) skip on
  non-Windows. Tests with platform-neutral logic retain the `pwsh`-presence guard.
  This preserves CI signal where it is valid and eliminates false failures where it
  is not.

---

## Decision Rationale

Option C matches the actual boundary: CCE is a developer tool, not a CI tool. Its
hook tests have no valid Linux CI meaning. Skipping them on Linux is not a coverage
loss — it is an accurate statement of scope. Platform-neutral hook logic retains CI
coverage through the existing `pwsh` guard.

---

## Consequences

- All new hook tests for dev-only tools (CCE, Windows-specific session guards) must
  use `sys.platform != "win32"` as the skip condition.
- Hook authors must guard `$env:USERPROFILE` with a `$HOME` fallback per P3.
- `Write-Error` inside `catch` blocks must specify `-ErrorAction Continue` to prevent
  re-throws under `$ErrorActionPreference = 'Stop'`.
- The `cce-health-gate.ps1` hook retains its current behaviour on Windows; no
  cross-platform changes are required to the hook itself.

---

## References

- [ADR-011](adr-011-hook-first-enforcement.md) — Hook-first Enforcement (parent; this
  ADR extends the hook boundary definition with dev/CI scoping rules)
