---
name: git-push-batched
description: Use when pushing changes to git -- organises dirty files into thematically cohesive commits before pushing
---

# Git Push — Batched Commits

This skill is applied whenever the user says anything like:
"push changes", "commit and push", "push to git", or "push my work".

**Do not apply this skill proactively.** Completing a task does not trigger a commit.
Wait for an explicit user instruction before staging or committing anything.

It prevents the anti-pattern of a single giant commit ("WIP", "save", "misc changes")
by grouping related changes before anything is staged.

**Default mode — auto-commit**: Display the proposed batch plan, then immediately execute
it without waiting for a reply. Only pause for confirmation if the user explicitly says
something like "show me the batches first", "let me review", or "don't commit yet".

For general commit hygiene, prek hooks, and push checklist, see the `version-control` skill.

## Boundary Contract

## Helper Functions

# Stage only the files in this batch
rtk git add <file1> <file2> ...

# Run prek on staged files only
rtk uv run prek run --files <file1> <file2> ...

# If prek auto-fixes files, re-stage them
rtk git add <file1> <file2> ...

# Commit
rtk git commit -m "<type>(<scope>): <summary>"
```

If prek fails with a blocking error (not an auto-fix), stop, report the error,
and ask the user how to proceed before continuing to the next batch.

## Thematic Grouping Heuristics

| File pattern | Likely commit type |
|---|---|
| `src/<pkg>/**/*.py` (new feature logic) | `feat` or `refactor` |
| `src/<pkg>/**/*.py` (bug fix) | `fix` |
| `tests/**/*.py` | `test` (or bundle with source) |
| `docs/**`, `*.md` (not skills) | `docs` |
| `.agents/skills/**` | `docs` |
| `pyproject.toml`, `uv.lock`, `prek.toml` | `chore` |
| `*.css`, `*.qmd` (style only) | `style` |
| `src/scripts/**` | `feat` or `chore` depending on purpose |
| `data/**` | `chore` (data updates) |
| `hooks/**` | `chore` |

# NEVER do this
git add .
git commit -m "updates"
```


See `procedures/git-push-batched.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Creating a single commit for all changes regardless of theme | Group changes by theme (feat, fix, chore, docs) into separate commits for a clean history |
| Using vague commit messages like "updates" or "fixes" | Write conventional commit messages: eat(scope): what changed � be specific |
| Including generated or build artefacts in the commit | Add generated paths to .gitignore before committing; never commit .pyc, dist/, or lock files modified unintentionally |