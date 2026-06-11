You are executing the `make-pr` pipeline. Announce: "Running make-pr: pre-flight → code review → push → PR."

## Step 1 — Pre-flight: detect branch and work state

```powershell
$branch = git branch --show-current
$dirty = git status --porcelain
$onRemote = git ls-remote --exit-code origin $branch 2>$null
```

**If on `master` or `main`:**
Read `.specify/feature.json` → `feature_directory` → `<dir>/spec.md` → `**Feature Branch**` field.
Run `git switch -c <branch-name>`, then continue. Never commit to master.

**Evaluate work state after branch check:**

| State | Action |
|---|---|
| No uncommitted changes AND branch already on remote | Abort. Output: "Nothing to push — branch is clean and already on remote. If PR is missing, run `gh pr create` directly." Stop. |
| No uncommitted changes AND branch NOT on remote | Skip Step 3. Jump to Step 4. |
| Uncommitted changes present | Full pipeline. Continue to Step 2. |

## Step 2 — Code review gate

Load and apply `.claude/commands/perform-code-review.md`.

All phases must exit clean before proceeding. If any phase fails and cannot be fixed, abort and report which gate failed. Do not proceed to Step 3.

## Step 3 — Push (skip if branch already clean and pushed)

Load and apply `.claude/commands/git-push-batched.md`.

Branch must be on remote before proceeding to Step 4.

## Step 4 — Generate PR title and body

```powershell
$commits = git log origin/master..HEAD --oneline
$branch = git branch --show-current
```

- **Title:** derive from branch name — strip type prefix and issue number, slugify.
  Examples: `feature/67-add-auth` → `Add auth`, `fix/42-null-pointer` → `Fix null pointer`
- **Body:**

```
## Summary
- <one bullet per logical commit, condensed to what changed>

## Test Plan
- [ ] prek exits 0
- [ ] pytest exits 0
- [ ] SonarQube exits 0 (or skipped — no scannable files changed)
```

## Step 5 — Create PR

```powershell
gh pr create --base master --title "<title>" --body @'
<body>
'@
```

Base branch is always `master`. No draft mode.

If `gh pr create` fails with "already exists", output the existing PR URL and stop — do not error.

Output the PR URL on success.
