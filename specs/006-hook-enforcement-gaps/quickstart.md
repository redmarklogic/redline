# Quickstart: Hook-First Enforcement Gaps

**Feature**: 006-hook-enforcement-gaps

---

## Run a single hook manually

```powershell
# Activate the virtual environment
.\.venv\Scripts\activate

# Run any hook against all files
pre-commit run <hook-id> --all-files

# Examples
pre-commit run check-skills-persona-names --all-files
pre-commit run check-no-argparse --all-files
pre-commit run check-hook-adr-reference --all-files
pre-commit run detect-secrets --all-files
```

---

## Run the full pre-commit suite

```powershell
pre-commit run --all-files
```

---

## Run tests for a specific hook (TDD verification)

```powershell
# Token-optimised (preferred)
rtk pytest tests/hooks/test_check_no_argparse.py -v

# Full test suite for all hooks
rtk pytest tests/hooks/ -v
```

---

## Lint a hook script

```powershell
rtk ruff check hooks/check-no-argparse.py
```

---

## Call a hook directly (without pre-commit)

```powershell
rtk uv run --frozen --offline hooks/check-no-argparse.py --dirs=src --dirs=scripts
```

Exit code `0` = clean, `1` = violations found.

---

## Regenerate the detect-secrets baseline (Phase 10 setup)

Run once on a clean repository before activating the `detect-secrets` hook:

```powershell
rtk uv run detect-secrets scan > .secrets.baseline
rtk git add .secrets.baseline
```

---

## Suppress a false positive

For Python source files, append `# hook: allow` to the flagged line:

```python
api_key = os.environ["LEGACY_KEY"]  # hook: allow
```

For Markdown skill files, append `<!-- hook: allow -->`:

```markdown
See the Kabilan handoff guide for examples. <!-- hook: allow -->
```
