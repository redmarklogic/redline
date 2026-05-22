# Resolve PR Comments — Step-by-Step

**See:** `resolving-pr-issues/SKILL.md` for triage schema, non-negotiable rules, and the automation priority order.

---

## Step 1 — Fetch all comments

```powershell
gh pr view --json number,title,headRefName
gh api repos/<owner>/<repo>/pulls/<number>/comments
gh api repos/<owner>/<repo>/pulls/<number>/reviews
```

If the GitHub API returns 404 (private repo / limited token), fall back to local diff:

```powershell
git diff origin/HEAD..HEAD --stat
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

Before editing any file:

1. Demonstrate the issue exists in the current codebase (run the code path, write a scratch test, or show the failing output).
2. If you cannot reproduce it: reclassify the comment as `disagree` and route to Step 4.

This step cannot be skipped. "We trust the reviewer" is not evidence.

---

## Step 4 — Disagreed comments: Context analysis

Answer both questions:

1. What context did the reviewer not have? (domain knowledge, intent, non-obvious invariant, established pattern)
2. Would a short code or doc comment make that context visible next time?

Then:

- If yes: improve code/docs **and** reply with that context.
- If no: reply with technical evidence only.

After replying, **request PTAL** and mark the thread as pending re-consent.

---

## Step 5 — Critical/behavioral defects: Postmortem-lite + 5 Whys (pre-fix)

Run this step **before implementation** so the broken state is still visible:

1. **Postmortem-lite**: lock the facts — what failed, when, what the observable symptom was, what evidence you have.
2. **5 Whys**: trace the top failure path to its root cause. Stop at the causal layer you can prevent, not the symptom.

Record findings in `docs/lessons/` using `lesson_template.md`. For `standard` and `low` tier issues, defer to a biweekly batch retrospective.

---

## Step 6 — Fail-first test for behavioral defects

When triage is `behavioral-defect` (any impact tier):

1. Write a failing automated test that makes the defect observable in CI.
2. Run the test. Confirm it fails for the right reason.
3. Only then implement the fix.

Exemption: `style-docs` comments with no behavioral component may skip this step. Record why in the thread reply.

---

## Step 7 — Implement the fix

- Minimal change that satisfies the comment.
- Do not refactor unrelated code.
- Run `get_errors` after each logical group of changes.

---

## Step 8 — Fast local gate

```powershell
.\.venv\Scripts\activate; uv run pre-commit run -a
.\.venv\Scripts\activate; python -m pytest <impacted test files> -x
```

If either fails: fix and re-run before pushing. Do not push a failing local gate.

---

## Step 9 — Push and request PTAL

```powershell
git push origin <branch>
gh pr comment <number> --body "Addressed <N> comments. Please take another look — PTAL."
```

For each changed thread: mark as resolved or leave a reply explaining what changed.

---

## Step 10 — CI presubmit (parallel, not blocking)

CI runs lint + full test suite + SonarQube in parallel automatically. Context-switch to other work while it runs. CI reporting back is the authoritative quality decision.

If CI fails: return to Step 7 and address failures.

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
