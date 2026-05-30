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


See `procedures/resolving-pr-issues.md` for detailed rules, examples, and extended reference.

## Common Mistakes (Baseline Failures)

| Mistake | Correct behaviour |
|---|---|
| Implementing a fix without reproducing the issue | Stop. Run the reproduction check first, even under time pressure |
| Skipping the failing test because "the fix is obvious" | Obvious fixes still need a test — obvious is when rationalization is highest |
| Adding a code comment on a disagreed thread and closing it | Reply with evidence, then request PTAL and wait for re-consent |
| Running pre-commit only | Run fast local gate (pre-commit + impacted tests), then push and let CI run in parallel |
| Treating "push branch" as done | Done = reviewer re-consent + CI green + all threads resolved |
| Applying postmortem/lessons to every comment | Batch reflection for `low`-tier items; immediate for `critical`/`behavioral-defect` |
| Resolving threads before pushing or before CI green | Thread resolution is the final act — commit, push, CI green, reviewer LGTM, then resolve |
