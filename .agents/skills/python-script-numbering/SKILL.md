---
name: python-script-numbering
description: Convention for naming pipeline scripts and documenting execution order via README rather than filename prefixes.
---

# Script Naming & Ordering

Never encode execution order in script filenames using numeric prefixes
(e.g. `s01_`, `s02_`, `001_`, `step1_`). Instead, document the execution
order in the scripts directory README using a numbered Markdown list with
relative hyperlinks.

## Boundary Contract

### Applies To
- Script file naming and execution order documentation under `src/scripts/`

### Produces
- Descriptive script names with execution order documented in README

### Does Not Cover
- Script internal structure (`python-script`)
- Function design (`python-function-design`)
- General style (`python-style`)

## Rationale

Numeric-prefix filenames suffer from two chronic problems in version-controlled projects:

1. **Merge-conflict churn** -- renaming files triggers conflicts in every branch that touches
   those paths, their imports, or any documentation that references them.
2. **Tedious mass-renames** -- inserting a step between existing ones (e.g. between `s02` and
   `s03`) forces renumbering all subsequent files and updating every reference site.

Encoding order in a Markdown list inside the README avoids both problems: reordering is a
single-file text edit, and filenames remain stable across branches.

## Convention

### Filenames

- Use descriptive, action-oriented names: `extract_survey_data.py`, `calculate_plant_emissions.py`.
- Do **not** add numeric prefixes (`s01_`, `001_`, `step1_`, etc.).

### README execution order

Document the pipeline execution order as a **flat numbered Markdown list**
in `src/scripts/README.md` (or in a dedicated `src/scripts/.order.md` if the
README is already large).

Each entry is a relative hyperlink followed by a description:

```markdown
## Execution order

1. [extract_survey_data.py](extract/extract_survey_data.py) -- Extract discrete GHG flux data ...
2. [build_jul2022_recovered_temps.py](extract/build_jul2022_recovered_temps.py) -- Recover Jul 2022 ...
3. [extract_field_temperatures.py](extract/extract_field_temperatures.py) -- Extract co-located ...
4. [calculate_plant_emissions.py](analyse/calculate_plant_emissions.py) -- Calculate plant-wide ...
```

- Use **relative paths** from the README location (e.g. `extract/foo.py`, not `src/scripts/extract/foo.py`).
- One-off or verification scripts that have no ordering requirement go in an
  **unnumbered** bullet list in a separate section.

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
3. Run `uv run pre-commit run scripts-in-readme` to verify.

### Applying to a new codebase

1. Remove numeric prefixes from existing script filenames (use `git mv` to preserve history).
2. Create or update the scripts README with a numbered execution-order list.
3. Update any references (docs, docstrings, configs) that used the old prefixed names.
4. Add or fix the `scripts_in_readme.py` pre-commit hook to use `rglob("*.py")`
   so it scans subdirectories recursively.
5. Run `git diff --stat` to verify git recognises renames (not delete + add).
