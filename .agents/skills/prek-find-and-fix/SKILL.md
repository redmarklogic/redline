---
name: prek-find-and-fix
description: Use when running the end-to-end prek triage-and-fix cycle for the current branch — from initial run through violation triage, fix, suppression with rationale, and re-run verification.
---

# prek Find and Fix

Orchestrates the full prek quality-gate sequence. Wraps violation triage in a
triage-first loop: tag every finding before editing any file, apply the
correct fix strategy per hook category, verify clean exit.

**Boundary contract:**

- **Input**: checked-out branch; working `.venv` (dev-environment prerequisite met).
- **Output**: `rtk uv run prek run -a` exits 0; every suppression carries inline
  rationale; no formatter violation fixed manually.
- **Out of scope**: running individual hooks in isolation (`python-static-checks`);
  SonarQube scan; test execution.

## Hook Categories (from `prek.toml` priority groups)

| Priority | Category | Behaviour | Fix strategy |
|---|---|---|---|
| 0 | Instant blockers | `language=fail`; file-existence checks | Delete or rename the offending file. No suppression possible for `language=fail` hooks. |
| 10 | Fast read-only validators | Logic, structure, doc checks — no mutations | Fix the code/doc/structure issue. Suppression only when genuinely inapplicable — requires inline rationale. |
| 20 | Formatters / fixers | Mutate files (`ruff-check --fix`, `ruff-format`, `pyproject-fmt`) | Re-run the formatter. Never hand-edit formatter output. Investigate only if formatter itself cannot fix. |
| 30 | Post-format validators | Read formatter output (`uv-sync`, `uv-export`, `ruff-format`) | Re-run prek after P20 pass; fix remaining structural issues. |
| 40 | Slow deep analysis | `pydoclint`, `deptry`, `import-linter`, `codespell` | Fix the root cause. For genuine false positives, add targeted suppression with rationale. |

## Triage Schema

Tag every violation before editing any file. Tags determine fix strategy.

| Tag | Values |
|---|---|
| **Decision** | `fix` · `suppress` (justified false positive / won't fix with documented rationale) |
| **Priority** | `blocker` (P0) · `standard` (P10/P30/P40) · `auto` (P20 — formatter, usually self-healing) |
| **Type** | `structural` (file existence, encoding) · `style` (format/lint) · `semantic` (import-linter, deptry, pydoclint) · `security` (detect-secrets) |

## Procedure

### Step 1 — Run prek

```bash
rtk uv run prek run -a
```

Capture all violations. Do not edit any file yet.

### Step 2 — Triage

For each violation, assign Decision / Priority / Type using the schema above.
List every finding in a triage table before proceeding.

Triage rules:
- P0 (`language=fail`): always `fix` + `structural`. No suppress path exists.
- P20 (`auto`): always `fix` by re-running the formatter — never by hand-editing.
- `security` type: verify the flagged string is not a real secret before tagging
  `suppress`. If real, rotate the secret; do not commit it.
- Whole-class exclusions (generated files, third-party assets, test fixtures):
  add a pattern to `prek.toml` `exclude`, not per-file `# noqa`.

### Step 3 — Fix in priority order

Apply fixes low-priority-number first (P0 → P10 → P20 → P30 → P40).

**P0 — Instant blockers:**
Delete or rename the offending file. Examples: `.rej` files, `test.py` files
inside `tests/`, `.ipynb` notebooks, `.github/copilot-instructions.md`.

**P10 — Validators:**
Fix the underlying code, documentation, or structure issue. If the finding is
genuinely inapplicable, add an inline suppression comment with rationale:

```python
# prek: suppress check-no-dataclass-in-domain — generated DTO, not domain model
```

**P20 — Formatters:**
Re-run the formatter that owns the file type:

```bash
rtk uv run prek run -a   # re-run full suite; P20 formatters self-heal
```

Never hand-edit a file to satisfy a formatter. If the formatter cannot fix it,
investigate why the formatter is failing — do not work around it.

**P30 — Post-format validators:**
Re-run after P20 is clean. Fix remaining issues (e.g., lock file out of sync
after `uv-lock`).

**P40 — Deep analysis:**
Fix the root cause:
- `pydoclint`: add or correct the docstring.
- `deptry`: add the missing dep to `pyproject.toml` or remove the unused import.
- `import-linter`: restructure the import to comply with the layer contract.
- `codespell`: correct the spelling; add to `[tool.codespell] ignore-words-list`
  only for domain terms that are not misspellings.

For genuine false positives, add a targeted suppression with rationale.

### Step 4 — Re-run to verify

```bash
rtk uv run prek run -a
```

Must exit 0. If new violations surface, repeat triage from Step 2.

### Step 5 — Suppression discipline

Every `suppress` decision must carry a rationale. Acceptable forms:

Inline (preferred for one-off findings):
```python
# noqa: <CODE>  -- <rationale: rule ref + why inapplicable>
```

`prek.toml` exclusion (required for a whole class):
```toml
exclude = "tests/assets/|generated/"
```

Never suppress without rationale. A bare `# noqa` or `# type: ignore` is a
violation of this skill.

## Common Mistakes

| Mistake | Correct behaviour |
|---|---|
| Suppressing a finding with no rationale | Add `# noqa: <CODE>  -- <rule ref + why inapplicable>` before committing. Bare suppression is not acceptable. |
| Hand-editing a P20 formatter violation | Re-run the formatter. Never manually reformat lines — hand edits will be overwritten and may introduce drift. |
| Not re-running prek after fixes | Re-run `rtk uv run prek run -a` after every fix batch. Fixes can unmask downstream violations. |
| Adding per-file `# noqa` across many files for the same class of finding | Add a single `exclude` pattern to `prek.toml`. Per-file suppression recurs on new files and clutters code. |
| Treating a `detect-secrets` finding as an obvious false positive | Verify the string is not a real secret before suppressing. If real: rotate first, then remove. Never commit a real secret. |
| Fixing P40 violations before P0/P10 are clean | Fix in priority order. P0 blockers must be resolved first — they cost nothing and their presence invalidates the run. |
| Running individual hooks to check a single file | `python-static-checks` covers isolated hook runs. This skill drives the full `--all` cycle only. |
