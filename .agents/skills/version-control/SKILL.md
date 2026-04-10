---
name: version-control
description: Version control conventions (commits, hygiene, pre-commit, and pre-push checks).
---

# Version Control

This skill defines version control conventions for this repo.

## Context & Guidelines

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

## Checklist

- No hardcoded credentials.
- Public functions/classes have docstrings and type hints (where applicable).
- Pre-commit passes.
- Tests pass.
