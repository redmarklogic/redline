---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

## Boundary Contract


See `procedures/verification-before-completion.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Claiming "done" based on the code looking correct | Run the verification commands first; assertion must follow evidence, not precede it |
| Running only the relevant test file instead of the full suite | Run the full suite; changes can break distant tests through shared fixtures or side effects |
| Skipping verification when the task was "just a small edit" | Every edit requires verification — the size of the change does not predict the scope of breakage |