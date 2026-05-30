---
name: git-hooks-create
description: Use when implementing, registering, or testing project-specific git hooks in hooks/
---

# Bespoke Git Hooks

This skill covers how to create project-specific git hooks that live inside the
repository under `hooks/`.

## Boundary Contract


See `procedures/git-hooks-create.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Writing a hook that fails silently | Hooks must exit with a non-zero code and print an actionable error message when they block a commit |
| Putting hook logic directly in the .git/hooks/ directory | Store hooks in hooks/ and register them via prek.toml; .git/hooks/ is not version-controlled |
| Making a hook too slow for daily use | Hooks exceeding 3 seconds in normal usage will be bypassed with --no-verify; profile and optimise |