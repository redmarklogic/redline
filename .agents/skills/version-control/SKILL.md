---
name: version-control
description: Version control conventions (commits, hygiene, prek hooks, and pre-push checks).
---

# Version Control

This skill defines version control conventions for this repo.

## Boundary Contract

### Applies To
- Git commits, branch hygiene, prek hooks, and pre-push checks

### Produces
- Clean commit history following repo conventions

### Does Not Cover
- Batched push workflow (`git-push-batched`)
- Branch finishing (`finishing-a-development-branch`)
- Code review (`requesting-code-review`)

## Context & Guidelines

### Commit and Push Authorisation

**Never commit or push unless the user explicitly instructs you to.**
Completing a file edit, finishing a task, or reaching a natural stopping point does NOT
automatically justify a commit. Wait for an explicit instruction such as "commit",
"push", "save to git", or similar.

This applies even when:
- A task is fully complete and working
- The changes are small and low-risk
- You have previously committed during the same session

The only exception is when the user has given a standing instruction for the current
task (e.g. "commit after each file"). Absent that, wait.

### Commits

- Write clear, descriptive commit messages.
- Do not commit commented-out code; delete it.
- Do not commit debug print statements or breakpoints.
- Never commit credentials or sensitive data.

### Before Pushing

- Run prek hooks (use the `dev-environment` skill).
- Run the relevant tests for the changed area.

## Procedure

1. Review staged changes for accidental debug code, secrets, and unrelated edits.
2. Run prek hooks and targeted tests for the modified area.
3. Create a clear commit message that explains intent and scope.
4. Push only after checks pass and the working tree is clean.

## PR Discipline

### Why small batches matter (especially with AI assistance)

DORA 2024 research identifies batch-size inflation as the primary risk when using AI
coding assistants. AI can generate 400 lines in the time a developer would write 40.
Without deliberate discipline, AI-assisted PRs drift to 1,000–2,000 lines — at which
point review becomes ineffective and defect detection drops sharply.

The mitigation is explicit batch size governance, not hope.

### The rules

- **One logical change per PR.** If a diff touches more than one bounded context, or
  combines a refactor with a feature, split it before pushing.
- **400-line soft threshold.** Aim to keep PRs under 400 changed lines (additions +
  deletions combined). Exceeding it requires a justification comment in the PR description.
- **Founder reviews all code before it reaches origin.** Do not push to origin without
  an explicit, same-session instruction from the founder.
- **Commit messages explain intent, not mechanics.**
  - Good: `"Extract Pandera schema for CPT data to enforce column constraints at ingestion boundary"`
  - Bad: `"Add schema"`

### Pre-push size check

Before pushing, check the size of your diff against the base branch:

```powershell
# Check diff size against the default branch (from repo root)
rtk git diff --stat origin/master

# Count total changed lines (additions + deletions combined)
(git diff origin/master | Where-Object { $_ -match '^[+\-]' -and $_ -notmatch '^(\+\+\+|---)' } | Measure-Object).Count
```

If the output exceeds 400 lines, apply the stacking strategy below before pushing.

### Stacking strategy for large tasks

When a task organically exceeds 400 lines, split it into sequential commits or PRs:

1. Identify the natural seam in the work (e.g., schema definition vs. reader vs. tests).
2. Commit and request review at each seam.
3. In the second commit's message, reference the first: `"Add CPT reader (builds on schema from <commit-hash>)"`.
4. Never combine the seams into one commit to "save time" — this defeats the purpose.

### Author-side AI feedback (before review)

Catch issues before the founder review session, not during it:

```powershell
rtk uv run prek run --all-files   # full hook suite
rtk uv run ruff check .                 # fast lint pass
rtk uv run mypy src/                    # type check
```

the Principal Engineer monitors macro-level trends (SonarQube quality gate, Copilot PR comment volume).
Individual findings are the Python Developer's responsibility to resolve before requesting review.
Do not modify SonarQube quality gate thresholds or Copilot PR rules — those are set by the Principal Engineer.

## Checklist

- No hardcoded credentials.
- Public functions/classes have docstrings and type hints (where applicable).
- prek hooks pass.
- Tests pass.
