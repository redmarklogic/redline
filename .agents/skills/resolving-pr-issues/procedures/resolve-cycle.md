# Resolve PR Comments — Step-by-Step

**See:** `resolving-pr-issues/SKILL.md` for the triage schema, non-negotiable rules, automation priority order, and the control flow diagram.

---

## Step 0 — Check CI/CD pipeline status

Before fetching comments, check whether CI is already failing on the current branch.
Failing CI must be resolved before any review cycle can close.

```powershell
# Latest runs on the current branch (show name, conclusion, run ID)
gh api repos/<owner>/<repo>/actions/runs --jq '.workflow_runs[:10] | .[] | select(.head_branch=="<branch>") | {id, name, status, conclusion}'
```

For each failed run, fetch the failure detail:

```powershell
gh run view <run-id> --log-failed
```

Triage each failure as a CI issue using the same **Decision / Impact tier / Type** schema used for review comments. Treat CI failures as `agree` + the appropriate tier. Proceed to fix them using Steps 3–9 before addressing review comments.

If CI is green on all workflows: skip to Step 1.

---

## Step 1 — Fetch all comments

```powershell
gh pr view --json number,title,headRefName
gh api repos/<owner>/<repo>/pulls/<number>/comments
gh api repos/<owner>/<repo>/pulls/<number>/reviews
```

If the GitHub API returns 404 (private repo / limited token), fall back to local diff:

```powershell
rtk git diff origin/HEAD..HEAD --stat
```

---

## Step 2 — Triage every comment

For each comment, assign all three tags before touching any file:

- **Decision**: agree / disagree
- **Impact tier**: critical · standard · low
- **Type**: behavioral-defect · maintainability · style-docs · tooling

Build a triage table and present it to the user. Do not proceed until every comment has all three tags.

---

## Step 3 — Agreed comments: Reproducibility gate

Demonstrate the issue exists in the current codebase. If unreproducible: reclassify as `disagree` → Step 4.

---

## Step 4 — Disagreed comments: Context analysis

Identify missing reviewer context. Improve code/docs if a comment would help. Reply with evidence. Post PTAL on the thread.

---

## Step 5 — Critical/behavioral defects: Postmortem-lite + 5 Whys (pre-fix)

Record in `docs/lessons/` using `lesson_template.md` before implementing the fix.

---

## Step 6 — Fail-first test for behavioral defects

Write a failing test. Confirm it fails for the right reason. Then implement the fix.

Exemption: `style-docs` comments with no behavioral component may skip. Record why in the thread reply.

---

## Step 7 — Implement the fix

Minimal change. No unrelated refactors.

---

## Step 8 — Fast local gate

```powershell
.\.venv\Scripts\activate; rtk uv run prek run -a
.\.venv\Scripts\activate; rtk pytest <impacted test files> -x
```

If either fails: fix and re-run before pushing. Do not push a failing local gate.

---

## Step 9 — Commit + push and request PTAL

```powershell
rtk git push origin <branch>
gh pr comment <number> --body "Addressed <N> comments. Please take another look — PTAL."
```

**Do not resolve threads at this step. Threads are resolved only in Step 11 after CI green and reviewer LGTM.**

---

## Step 10 — CI presubmit

CI runs automatically. Context-switch to other work while it runs. If CI fails: return to Step 7.

---

## Step 11 — Closure criteria (all must be true)

- [ ] Reviewer has replied LGTM on all changed threads
- [ ] CI presubmit is green (lint + tests + SonarQube)
- [ ] All review threads are resolved
- [ ] Prevention actions (lessons, automation candidates) captured as follow-up tasks

Only when all four are true is the review cycle complete.

---

## Step 12 — Prevention actions (post-closure)

After LGTM + CI green:

- Update `docs/lessons/` for critical/repeat defects.
- Record automation candidates as prioritised backlog tasks (use automation priority order in SKILL.md).
- Capture skill/checklist updates with owner and replay validation date.
