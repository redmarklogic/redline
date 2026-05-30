# Python Script Numbering — Detailed Reference

### Filenames

- Use descriptive, action-oriented names: `extract_survey_data.py`, `calculate_plant_emissions.py`.
- Do **not** add numeric prefixes (`s01_`, `001_`, `step1_`, etc.).

### README execution order

Document the pipeline execution order as a **flat numbered Markdown list**
in `src/scripts/README.md` (or in a dedicated `src/scripts/.order.md` if the
README is already large).

Each entry is a relative hyperlink followed by a description:

```markdown
### Pre-commit hook enforcement

Two pre-commit hooks enforce the naming and documentation conventions:

1. **`no-numeric-script-prefix`** (`tasks/hooks/no_numeric_script_prefix.py`) --
   Scans `src/scripts/` for `.py` files matching `s\d\d_*` and rejects
   them. Rename offending files with `git mv` (preserves history).

2. **`scripts-in-readme`** (`tasks/hooks/scripts_in_readme.py`) --
   Recursively scans for `.py` files under the README's parent directory tree
   and fails if any script filename is missing from the README content. This
   guarantees every script is documented.

## Procedure

### When adding a new script

1. Create the `.py` file in the appropriate subfolder.
2. Add a numbered or bulleted entry in `src/scripts/README.md`.
3. Run `uv run prek run scripts-in-readme` to verify.

### Applying to a new codebase

1. Remove numeric prefixes from existing script filenames (use `git mv` to preserve history).
2. Create or update the scripts README with a numbered execution-order list.
3. Update any references (docs, docstrings, configs) that used the old prefixed names.
4. Add or fix the `scripts_in_readme.py` pre-commit hook to use `rglob("*.py")`
   so it scans subdirectories recursively.
5. Run `git diff --stat` to verify git recognises renames (not delete + add).
