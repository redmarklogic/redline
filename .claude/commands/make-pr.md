You are executing the `make-pr` pipeline. Announce: "Running make-pr: pre-flight → conflict check → code review → push → PR."

## Step 1 — Pre-flight: detect branch and work state

```powershell
$branch = git branch --show-current
$dirty = git status --porcelain
$onRemote = git ls-remote --exit-code origin $branch 2>$null
$existingPrUrl = gh pr view --json url --jq .url 2>$null
```

**If on `master` or `main`:**
Read `.specify/feature.json` → `feature_directory` → `<dir>/spec.md` → `**Feature Branch**` field.
Run `git switch -c <branch-name>`, then continue. Never commit to master.

**Evaluate work state after branch check:**

| State | Action |
|---|---|
| No uncommitted changes AND branch already on remote AND PR exists | Continue full pipeline. Step 6 will skip creation and output existing PR URL instead. |
| No uncommitted changes AND branch already on remote AND no PR | Abort. Output: "Nothing to push — branch is clean and already on remote. If PR is missing, run `gh pr create` directly." Stop. |
| No uncommitted changes AND branch NOT on remote | Skip Step 3. Jump to Step 4. |
| Uncommitted changes present | Full pipeline. Continue to Step 2. |

## Step 2 — Conflict check: merge master into branch

```bash
git fetch origin master
git log HEAD..origin/master --oneline
```

**If no new commits on `origin/master`:** skip the rest of this step, continue to Step 3.

**If new commits exist:** attempt a no-commit merge to detect conflicts.

```bash
git merge origin/master --no-commit --no-ff
```

- **Exit 0 (clean merge):** stage the merge and commit.

  ```bash
  git commit -m "chore: merge master into <branch-name>"
  ```

  Continue to Step 3.

- **Exit non-0 (conflicts):** attempt auto-resolution before giving up.

  **Auto-resolvable files (always use ours):** `.specify/feature.json`

  For each conflicting file in the auto-resolvable list:

  ```bash
  git checkout --ours -- <file>
  git add <file>
  ```

  After auto-resolution, check for remaining conflicts:

  ```bash
  git diff --name-only --diff-filter=U
  ```

  - **No remaining conflicts:** commit the merge.

    ```bash
    git commit -m "chore: merge master into <branch-name>"
    ```

    Continue to Step 3.

  - **Remaining conflicts exist:** abort the merge, list the unresolved files, then stop.

    ```bash
    git merge --abort
    ```

    Output the list of conflicting files, then print: "Merge conflicts detected. Resolve conflicts in the listed files, stage the resolutions, then re-run `/make-pr`." Do not proceed to Step 3.

## Step 3 — Code review gate

Load and apply `.claude/commands/perform-code-review.md`.

All phases must exit clean before proceeding. If any phase fails and cannot be fixed, abort and report which gate failed. Do not proceed to Step 4.

## Step 4 — Push (skip if branch already clean and pushed)

Load and apply `.claude/commands/git-push-batched.md`.

Branch must be on remote before proceeding to Step 5.

## Step 5 — Generate PR title and body

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

## Step 6 — Create or surface PR

**If `$existingPrUrl` is set (PR already exists):**
Output: "PR already exists: `$existingPrUrl` — skipping creation." Continue to Step 7.

**Otherwise:**

```powershell
gh pr create --base master --title "<title>" --body @'
<body>
'@
```

Base branch is always `master`. No draft mode.

If `gh pr create` fails with "already exists", output the existing PR URL and stop — do not error.

Output the PR URL on success.

## Step 7 — Quality gate summary

After the PR URL, output a table summarising every check run during this pipeline.

| Check | Violations | Details | Fixed |
|---|---|---|---|
| prek | Yes / No | List each hook that failed, or — | Yes / No / N/A |
| pytest | Yes / No | Number of failures, or — | Yes / No / N/A |
| SonarQube | Yes / No / Skipped | Each issue (rule, file:line), or — | Yes / No / N/A |

Rules:

- Include a row for every check that ran, even if clean.
- If a check was skipped (e.g. SonarQube predicate not met), set Violations to `Skipped` and Details/Fixed to `—`.
- Details for prek: list each failing hook by name (e.g. `ruff-format`, `fix-doc-sync`).
- Details for pytest: `N failed, M passed` or `all passed`.
- Details for SonarQube: each finding as `rule @ file:line`, or `—`.
- Fixed = `Yes` when the pipeline resolved it before pushing; `No` if it was suppressed or deferred; `N/A` if no violations.
