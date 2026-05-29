# Patch: version-control skill — PR Discipline Thresholds

> DRAFT — pending user approval. Do not promote to production.

**Target file:** `.agents/skills/version-control/SKILL.md`
**Session:** 2026-05-23 Topology Sync — Kabilan hire skill gaps
**Grounded by:** Peter (DORA 2024 AI Era findings, Peter's JD DORA AI-Era Responsibilities,
  `pyproject.toml` tooling config)
**Drafted by:** Harriet
**Gap addressed:** PR discipline thresholds — the current skill states "~400 changed lines"
  but lacks the DORA AI-era rationale, a pre-push size check command, and guidance on how
  to handle tasks that organically exceed the threshold.

---

## Changes

### 1. Replace the "PR Discipline" section

Replace the current "PR Discipline" section with the expanded version below.

---

**Current content:**

```markdown
## PR Discipline

- Every PR must be a single logical change. If a diff touches more than one bounded context or combines a refactor with a feature, split it.
- The founder reviews all code before it reaches origin. Do not push without explicit founder instruction.
- Aim for compact, reviewable diffs. As a guideline, keep PRs under ~400 changed lines. If a task requires more, break it into stacked commits or sequential PRs.
- Commit messages must explain intent, not just describe what changed. Good: "Extract Pandera schema for CPT data to enforce column constraints at ingestion boundary". Bad: "Add schema".
- Run static checks (`python-static-checks`) and relevant tests before requesting review.
```

**Replace with:**

```markdown
## PR Discipline

### Why small batches matter (especially with AI assistance)

DORA 2024 research identifies batch-size inflation as the primary risk when using AI
coding assistants. AI can generate 400 lines in the time a developer would write 40.
Without deliberate discipline, AI-assisted PRs drift to 1,000–2,000 lines — at which
point review becomes ineffective and defect detection drops sharply.

The mitigation is explicit batch size governance, not hope.

### The rules

- **One logical change per PR.** If a diff touches more than one bounded context, or
  combines a refactor with a feature, split it before pushing.
- **400-line soft threshold.** Aim to keep PRs under 400 changed lines (additions +
  deletions combined). This is a guideline, not a hard block — but exceeding it requires
  justification in the PR description.
- **Founder reviews all code before it reaches origin.** Do not push to origin without
  an explicit, same-session instruction from the founder.
- **Commit messages explain intent, not mechanics.**
  - Good: `"Extract Pandera schema for CPT data to enforce column constraints at ingestion boundary"`
  - Bad: `"Add schema"`

### Pre-push size check

Before pushing, check the size of your diff against the base branch:

```powershell
# Check diff size against the default branch (from repo root)
git diff --stat origin/master

# Count total changed lines (additions + deletions combined)
(git diff origin/master | Where-Object { $_ -match '^[+\-]' -and $_ -notmatch '^(\+\+\+|---)' } | Measure-Object).Count
```

If the output exceeds 400 lines, apply the stacking strategy below before pushing.

### Stacking strategy for large tasks

When a task organically exceeds 400 lines, split it into stacked sequential commits or PRs:

1. Identify the natural seam in the work (e.g., schema definition vs. reader implementation vs. tests).
2. Commit and request review at each seam.
3. In the second commit's message, reference the first: `"Add CPT reader (builds on schema from <commit-hash>)"`.
4. Never combine the seams into a single commit to "save time" — this defeats the purpose.

### Author-side AI feedback (before review)

Run static checks at authoring time, not only at PR review time:

```powershell
uv run prek run --all-files   # full hook suite
uv run ruff check .                 # fast lint pass
uv run mypy src/                    # type check
```

Catching issues before the founder review session is better than catching them during it.
Peter monitors macro-level trends (SonarQube, Copilot PR comment volume) — individual
findings are Kabilan's responsibility to resolve before requesting review.

### What Peter configures (not Kabilan's concern)

Peter sets SonarQube quality gate thresholds and Copilot PR comment rules. Kabilan does
not modify these. If a quality gate fires unexpectedly, check with Peter before bypassing it.
```
