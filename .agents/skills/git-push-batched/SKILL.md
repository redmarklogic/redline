---
name: git-push-batched
description: When asked to push changes to git, inspect all dirty files and organise them into thematically cohesive commits, then stage and commit each batch before pushing. By default, proceeds automatically; pauses for confirmation only when the user explicitly asks to review first.
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

### Inputs
- Dirty working tree with uncommitted changes

### Outputs
- Thematically grouped commits pushed to remote

### Out of Scope
- Branch management (`version-control`)
- PR creation (`finishing-a-development-branch`)
- Code review (`requesting-code-review`)

## Context & Guidelines

- **Scope**: Any time the user wants to push uncommitted changes to a remote branch.
- **Protected branches — hard stop**: Before doing anything, check the current branch.
  If it is `master` or `main`, **stop immediately**. Do not stage, do not commit, do not push.
  Tell the developer they are on a protected branch and ask them to check out a feature branch.
- **Auto-commit by default**: Show the batch plan, then execute immediately. Only wait
  for confirmation when the user explicitly requests a review step.
- **Never amend published commits**: Only create new commits on the current branch.
- **Commit message style**: Use conventional commits — `type(scope): short imperative summary`.
  Permitted types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`, `perf`.
- **Batch size**: Aim for 1–5 files per commit; split large features into logical sub-batches.
  Never put unrelated files in the same commit.
- **Tests travel with their subject**: If a source file and its test file both changed, they
  belong in the same `feat`/`fix`/`refactor` commit unless the test change is purely
  structural (then a separate `test:` commit is fine).
- **Config/tooling changes** (pyproject.toml, .pre-commit-config.yaml, mkdocs.yml, etc.)
  form their own `chore:` commit unless they are mechanically caused by the same feature,
  in which case they may be grouped with it.
- **Docs and skills** always form a separate `docs:` commit.

## Helper Functions

### Get-LocalBranch

Always call this helper to obtain the **local** branch name. Never infer the branch
from attachment metadata, repository context objects, or any other source — those
reflect the remote default branch, not the checked-out local branch.

<!-- rtk:skip -->
```powershell
function Get-LocalBranch {
    git branch --show-current
}
```

Usage: `$branch = Get-LocalBranch`

---

## Procedure

### 0. Check Branch (Hard Stop)

Call the helper to get the actual local branch:

```powershell
$branch = Get-LocalBranch   # calls: git branch --show-current
```

If `$branch` is `master` or `main`, **stop here**. Do not proceed.
Tell the developer:

> "You are on `<branch>`, which is a protected branch. I cannot commit or push here.
> Please check out a feature branch and try again."

**Important**: Do NOT use the branch name from attachment metadata or repository context.
Those show the remote default branch. Always use `Get-LocalBranch`.

### 1. Discover Changes

Run the following to get the full picture of dirty files:

```powershell
rtk git status --short
rtk git diff --stat HEAD
```

Also run to capture untracked files:

```powershell
rtk git ls-files --others --exclude-standard
```

### 2. Read the Diffs

For each changed file, read `git diff HEAD -- <file>` (or the full file content for
untracked files) to understand *what* changed, not just *that* it changed.

### 3. Display Plan and Execute

Print the batch plan **before touching the index**. Format:

```
Proposed commits
================

Batch 1  feat(readers): add timber-pole wall reader
  src/rl/functions/readers/timber_pole.py   (new)
  tests/functions/readers/test_timber_pole.py  (new)

Batch 2  test(calculators): add edge-case tests for timber pole
  tests/calculators/test_timber_pole.py   (modified)

Batch 3  docs: update functions codebook and codemap
  docs/CODEMAPS/functions.md   (modified)
  docs/codebooks/retaining_walls/timber_pole.md  (new)

Batch 4  chore: update pyproject.toml dependencies
  pyproject.toml   (modified)

Push to: origin/<current-branch>
```

**Default (auto-commit)**: Proceed immediately to Step 4 without waiting.

**Confirmation mode** (only when user explicitly requested a review step): Ask:
> "Does this grouping look right? You can rename commit messages, merge batches, or
> exclude files. Reply with adjustments or 'go' to proceed."

### 4. Execute

For each confirmed batch in order:

```powershell
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

### 5. Push

Call `Get-LocalBranch` again to confirm the branch hasn't changed mid-session.
If it is `master` or `main`, stop and report.

After all batches are committed:

```powershell
$branch = Get-LocalBranch
rtk git push origin $branch
```

Report the push output to the user.

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

## Examples

### Good — tight, themed batches

```
feat(readers): parse timber-pole wall schedule from Excel
  src/rl/functions/readers/timber_pole.py
  tests/functions/readers/test_timber_pole.py

docs: add timber-pole codebook and update functions codemap
  docs/codebooks/retaining_walls/timber_pole.md
  docs/CODEMAPS/functions.md

chore: add openpyxl to dependencies
  pyproject.toml
  uv.lock
```

### Bad — single monolithic commit

<!-- rtk:skip -->
```
# NEVER do this
git add .
git commit -m "updates"
```
