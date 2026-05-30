---
name: version-control
description: Use when applying version control conventions -- commit hygiene, prek hooks, or pre-push checks in this repo
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

## PR Discipline

# Check diff size against the default branch (from repo root)
rtk git diff --stat origin/master

# Count total changed lines (additions + deletions combined)
(git diff origin/master | Where-Object { $_ -match '^[+\-]' -and $_ -notmatch '^(\+\+\+|---)' } | Measure-Object).Count
```

If the output exceeds 400 lines, apply the stacking strategy below before pushing.

## Checklist

- No hardcoded credentials.
- Public functions/classes have docstrings and type hints (where applicable).
- prek hooks pass.
- Tests pass.


See `procedures/version-control.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Committing directly to main/master for feature work | Use a feature branch; main is a protected branch in this repo |
| Writing a commit message in past tense ("Added feature") | Use imperative mood ("Add feature"); conventional commits follow this convention |
| Bypassing prek hooks with --no-verify | Fix the hook failure instead; --no-verify commits may introduce violations that fail CI |