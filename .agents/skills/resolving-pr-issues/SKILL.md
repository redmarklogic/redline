---
name: resolving-pr-issues
description: Use when resolving PR code-review comments, addressing reviewer feedback, or closing a PR review cycle after comments are received
---

## Boundary Contract

### Applies To
- Resolving incoming PR code-review comments
- Addressing agreed or disagreed reviewer feedback
- Closing a PR review cycle (reviewer re-consent + CI + threads)

### Produces
- Fixed code with fail-first tests for behavioral defects
- Reviewer re-consent (LGTM or explicit approval) for all changed threads
- CI presubmit green (lint + full tests + SonarQube)
- Prevention actions captured for critical/repeat defects

### Does Not Cover
- Conducting a PR review from scratch (use `pr-review`)
- Merging or branching decisions (use `finishing-a-development-branch`)
- Root-cause logging format (use `python-error-handling`)


See `procedures/resolve-cycle.md` for the numbered step-by-step procedure.

## Non-Negotiable Rules

These rules apply regardless of time pressure, sunk cost, or authority:

1. **Reproducibility before files** — for agreed comments, confirm the issue exists in the current codebase before editing anything.
2. **Fail-first test for behavioral defects** — write a failing automated test that captures the defect before implementing the fix.
3. **PTAL after every response** — after replying to any thread (agreed change or disagreed reasoning), post PTAL to request re-review. Treat the thread as open until the reviewer explicitly approves or re-consents.
4. **Two-stage quality gate** — fast local gate first, then CI presubmit. Not one, not three.
5. **Completion requires reviewer re-consent + CI green + threads resolved** — pushing the branch is not completion.
6. **Disagree path requires evidence and closure** — for disagree comments: (1) reply with concrete evidence (spec reference, benchmark, or code example), (2) post PTAL, (3) if disagreement persists escalate to tech lead or team convention, and (4) record the final decision in the thread.
7. **Never resolve threads before CI is green** — thread resolution is the final act, after fixes are committed + pushed + CI green + reviewer LGTM. Resolving threads with unflushed local fixes is a false signal to reviewers.

## Triage Schema

Every comment gets all three tags before any file is touched:

| Tag | Values |
|---|---|
| **Decision** | `agree` / `disagree` |
| **Impact tier** | `critical` · `standard` · `low` |
| **Type** | `behavioral-defect` · `maintainability` · `style-docs` · `tooling` |

Impact tier controls mandatory steps; Decision controls whether you reproduce-and-fix or evidence-and-escalate:

| Tier | Mandatory extras |
|---|---|
| `critical` | Reproducibility gate · Fail-first test (behavioral) · Postmortem-lite + 5 Whys · Immediate lesson capture |
| `standard` | Reproducibility gate · Fail-first test (behavioral) |
| `low` | None — minimal fix path |

## Control Flow

```mermaid
graph TD
    Entry(Entry) --> CI0["Step 0: Check CI/CD pipeline status"]
    CI0 -->|CI failing| Fix["Step 7: Implement minimal fix"]
    CI0 -->|CI green| Fetch["Step 1: Fetch all PR comments"]
    Fetch --> Triage["Step 2: Triage ALL comments\nDecision · Impact tier · Type"]
    Triage --> Dec1{agree or disagree?}
    Dec1 -->|agree| Repro["Step 3: Reproducibility gate"]
    Dec1 -->|disagree| Ctx["Step 4: Context analysis"]
    Repro -->|cannot reproduce| Ctx
    Repro -->|reproduced| Dec2{critical tier?}
    Dec2 -->|yes| PM["Step 5: Postmortem-lite + 5 Whys"]
    Dec2 -->|no| Dec3{behavioral defect?}
    PM --> Dec3
    Dec3 -->|yes| FFT["Step 6: Write fail-first test"]
    Dec3 -->|no| Fix
    FFT --> Fix
    Ctx --> Reply["Reply with evidence, post PTAL"]
    Fix --> Gate["Step 8: Fast local gate\npre-commit + pytest"]
    Reply --> Gate
    Gate -->|fails| Fix
    Gate -->|passes| Push["Step 9: Commit + push"]
    Push --> PTAL["Post PTAL comment on PR"]
    PTAL --> CI10["Step 10: Wait for CI\nlint · tests · SonarQube"]
    CI10 -->|CI fails| Fix
    CI10 -->|CI green| Dec4{reviewer LGTM?}
    Dec4 -->|changes requested| Fix
    Dec4 -->|LGTM| Resolve["Step 11: Resolve all threads\n(final act)"]
    Resolve --> Prevent["Step 12: Capture prevention actions"]
    Prevent --> Done(Complete)
```

## Automation Capture Priority

When a comment reveals a gap that automation could prevent, record it as a follow-up task. Do not implement automation as part of the current review cycle unless it is critical and can be implemented in under 15 minutes without modifying application code. Priority order when you do implement:

1. **Enable a ruff rule** — check `ruff rule <CODE>`; add to `extend-select` in `pyproject.toml`
2. **Add a community pre-commit hook** — search [pre-commit hook catalog](https://pre-commit.com/hooks.html)
3. **Extend an existing `hooks/` script** — add a case to an existing domain-specific hook
4. **Write a new local hook** — last resort; follow `pre-commit-hooks-create` skill

## Common Mistakes (Baseline Failures)

| Mistake | Correct behaviour |
|---|---|
| Starting with PR comments when CI is already red | Stop. Run Step 0 (CI status check) first — CI failures block closure regardless of review state |
| Implementing a fix without reproducing the issue | Stop. Run the reproduction check first, even under time pressure |
| Skipping the failing test because "the fix is obvious" | Obvious fixes still need a test — obvious is when rationalization is highest |
| Adding a code comment on a disagreed thread and closing it | Reply with evidence, then request PTAL and wait for re-consent |
| Running pre-commit only | Run fast local gate (pre-commit + impacted tests), then push and let CI run in parallel |
| Treating "push branch" as done | Done = reviewer re-consent + CI green + all threads resolved |
| Applying postmortem/lessons to every comment | Batch reflection for `low`-tier items; immediate for `critical`/`behavioral-defect` |
| Resolving threads before pushing or before CI green | Thread resolution is the final act — commit, push, CI green, reviewer LGTM, then resolve |
