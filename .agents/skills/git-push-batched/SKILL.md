---
name: git-push-batched
description: Use when pushing changes to git -- organises dirty files into thematically cohesive commits before pushing
disable-model-invocation: true
model: haiku
---

# Git Push — Batched Commits

<!-- Manual-only: stages and commits files — must not auto-invoke. -->

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

If prek fails with a blocking error (not an auto-fix), apply the **Pre-commit Failure Triage** protocol below before escalating.

## Pre-commit Failure Triage

### Test cases (expected behaviour — the spec)

| # | Failure | Expected outcome |
|---|---|---|
| T1 | `ruff` unused import — single file | Auto-fix: remove import, re-stage, retry |
| T2 | `ruff` line-too-long — single file | Auto-fix: reformat, re-stage, retry |
| T3 | `ruff` import order wrong — single file | Auto-fix: reorder, re-stage, retry |
| T4 | Trailing whitespace — single file | Auto-fix: strip, re-stage, retry |
| T5 | `mypy` type mismatch | **Escalate** — semantic change, intent unclear |
| T6 | `prek` detects secret/credential | **Escalate** — security domain, never auto-fix |
| T7 | Lint violation spans 3+ files in batch | **Escalate** — blast radius too wide |
| T8 | Test file assertion fails | **Escalate** — test expectations encode intent |
| T9 | Missing type annotation, unambiguous inference | Auto-fix: add annotation, re-stage, retry |
| T10 | Two valid fixes exist for one error | **Escalate** — ambiguous, ask user to choose |
| T11 | Auto-fix applied, prek still fails second run | **Escalate** — do not loop; report both errors |

### Blast-radius assessment

Evaluate every failing dimension. One **red** → escalate immediately; skip remaining checks.

| Dimension | Green → auto-fix | Red → escalate |
|---|---|---|
| **Change domain** | Style, formatting, imports, whitespace | Logic, types, tests, security, auth, data contracts |
| **Scope** | Single file needs change | 2+ files need changes to resolve one error |
| **Ambiguity** | One unambiguous fix | Multiple valid fixes, or correct fix unclear |
| **Fix mechanism** | Rule-based rewrite (formatter rewrites deterministically) | Judgement-based (semantic understanding required) |
| **Risk area** | No security/auth/crypto code touched | Secret, credential, permission, or encryption code |

### Protocol

1. Classify the failure against the table above.
2. **All green** → apply fix, re-stage affected files, re-run `rtk uv run prek run --files <files>`, retry commit.
   - Second failure for any reason: escalate — do not loop.
3. **Any red** → stop. Report: (a) error message, (b) which red dimension triggered escalation, (c) what a fix would require. Ask how to proceed.
4. Never modify test assertions, type signatures, or security-related code without explicit user instruction.

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

<!-- rtk:skip -->
```
# NEVER do this
git add .
git commit -m "updates"
```


See `procedures/git-push-batched.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Creating a single commit for all changes regardless of theme | Group changes by theme (feat, fix, chore, docs) into separate commits for a clean history |
| Using vague commit messages like "updates" or "fixes" | Write conventional commit messages: eat(scope): what changed — be specific |
| Including generated or build artefacts in the commit | Add generated paths to .gitignore before committing; never commit .pyc, dist/, or lock files modified unintentionally |