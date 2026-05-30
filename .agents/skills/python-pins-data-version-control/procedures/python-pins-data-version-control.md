# Python Pins Data Version Control — Detailed Reference

## Context & Guidelines

### Scope

Apply whenever code reads or writes datasets that are too large, too volatile, or too
numerous to track in git. Pins is the default mechanism for sharing pipeline outputs
and analysis results.

### Board Layout

Boards live on the `T:` network drive under a project-level `pins/` directory.
The main board is always at a named subdirectory — never at the bare `pins/` root:

```
T:/path/to/project/pins/
    main/              <- general-purpose board
    site_readings/     <- dedicated board for parameterized datasets
    model_outputs/     <- another dedicated board
```

The bare `pins/` directory is a namespace that holds multiple boards. Each board
is a subdirectory.

### Board Setup

Always use `pins.board("file", ...)`. Never use `pins.board_folder()`.

```python
import pins

board = pins.board("file", "T:/path/to/project/pins/main")
```

### Reading and Writing

```python
### Pin Naming Rules

- Always use `snake_case`.
- Never embed IDs, parameters, or dynamic values in the pin name.

If a dataset is parameterized (e.g., one table per site), create a **dedicated board**
for that dataset family and use the bare identifier as the pin name:

```python
### Preferred Format

Use `type="parquet"` for DataFrames. Parquet preserves types, is compact, and is
fast to read.

### Relationship to `data/`

Pins replaces the pattern of writing pipeline outputs to `data/processed/`.
Git-tracked data under `data/` remains as a fallback for tiny, stable reference
tables only.

## Procedure

1. Determine whether the dataset should be git-tracked or pinned (see decision
   table above).
2. If pinned, identify whether it belongs on the main board or needs a dedicated
   board (parameterized data always gets a dedicated board).
3. Set up the board with `pins.board("file", "T:/.../pins/<board_name>")`.
4. Write with `board.pin_write(df, "pin_name", type="parquet")`.
5. Read with `board.pin_read("pin_name")`.
6. Never hardcode the full `T:` path in library code; define board paths as
   constants in scripts or configuration.
