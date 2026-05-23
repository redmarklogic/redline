---
name: version-control
description: Version control conventions (commits, hygiene, pre-commit, and pre-push checks).
---

# Version Control

This skill defines version control conventions for this repo.

## Boundary Contract

### Applies To
- Git commits, branch hygiene, pre-commit, and pre-push checks

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

- Run pre-commit checks (use the `dev-environment` skill).
- Run the relevant tests for the changed area.

## Procedure

1. Review staged changes for accidental debug code, secrets, and unrelated edits.
2. Run pre-commit checks and targeted tests for the modified area.
3. Create a clear commit message that explains intent and scope.
4. Push only after checks pass and the working tree is clean.

## PR Discipline

- Every PR must be a single logical change. If a diff touches more than one bounded context or combines a refactor with a feature, split it.
- The founder reviews all code before it reaches origin. Do not push without explicit founder instruction.
- Aim for compact, reviewable diffs. As a guideline, keep PRs under ~400 changed lines. If a task requires more, break it into stacked commits or sequential PRs.
- Commit messages must explain intent, not just describe what changed. Good: "Extract Pandera schema for CPT data to enforce column constraints at ingestion boundary". Bad: "Add schema".
- Run static checks (`python-static-checks`) and relevant tests before requesting review.

## Checklist

- No hardcoded credentials.
- Public functions/classes have docstrings and type hints (where applicable).
- Pre-commit passes.
- Tests pass.
