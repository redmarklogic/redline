---
name: python-performance
description: Profiling and optimisation patterns for Python code in this repo — when to profile, which tools to use, and common algorithmic fixes.
---

# Python Performance

This skill covers how to identify, measure, and fix performance bottlenecks in Python code.

Apply it when a script, hook, or function is noticeably slow and the cause is not obvious.
Do not guess — always measure first.

## Boundary Contract

### Applies To
- Python code with suspected performance bottlenecks in scripts, hooks, or functions

### Produces
- Profiled and optimised code with measured improvements

### Does Not Cover
- General style (`python-style`)
- Function design (`python-function-design`)
- Algorithmic design decisions (`spec-kit`)

## Context & Guidelines

### Scope

Apply whenever:

- A script or hook is slower than expected for its input size.
- A change is proposed that involves an inner loop, pairwise comparison, or repeated regex
  compilation.
- A performance fix is being reviewed and its impact needs to be verified.

### Constraints

- **Measure before changing.** Use `cProfile` or `timeit` to identify the bottleneck
  before writing any optimisation code. Gut feelings about hotspots are frequently wrong.
- **Verify after changing.** Re-run the profiler or timer to confirm the fix had the
  expected impact.
- **Preserve correctness.** Run the test suite and the relevant pre-commit hook after any
  optimisation to confirm behaviour is unchanged.
- **No third-party profiling libraries** unless one is already in `pyproject.toml`. The
  stdlib `cProfile`, `timeit`, and `time` are sufficient for most cases.

## Procedure

### 1. Profile

```powershell
python -m cProfile -s cumulative <script.py> 2>&1 | Select-Object -First 30
```

Read the `cumtime` column. The highest-cumtime non-built-in entry is the primary
bottleneck. Look for functions called far more times than expected — this reveals
algorithmic issues (e.g. O(n²) loops).

### 2. Measure baseline

```powershell
Measure-Command { python <script.py> } | Select-Object TotalSeconds
```

Record this as your baseline to compare against after optimisation.

### 3. Fix the bottleneck

Common patterns:

#### Cascade cheap upper bounds before expensive similarity checks

`SequenceMatcher.ratio()` is O(n·m). Always guard it with the two built-in O(1)/O(n+m)
upper-bound methods before calling it:

```python
sm = difflib.SequenceMatcher(None, text_a, text_b)
if sm.real_quick_ratio() < threshold:   # O(1)  — length arithmetic
    continue
if sm.quick_ratio() < threshold:        # O(n+m) — character frequency
    continue
ratio = sm.ratio()                      # O(n·m) — only reached if necessary
```

#### Compile regex patterns once

Move `re.compile()` calls to module level, not inside loops.

```python
# Good — compiled once
_PATTERN = re.compile(r"\b(always|must)\b\s+(.*)", flags=re.IGNORECASE)

for line in lines:
    match = _PATTERN.search(line)

# Bad — compiled on every iteration
for line in lines:
    match = re.compile(r"\b(always|must)\b\s+(.*)").search(line)
```

#### Replace O(n²) membership tests with sets

If checking `item in list` inside a loop, convert the list to a `set` first.

```python
# Good — O(1) lookups
existing = {doc.skill_dir.name for doc in documents}
if name not in existing: ...

# Bad — O(n) per lookup
existing = [doc.skill_dir.name for doc in documents]
if name not in existing: ...
```

### 4. Verify

```powershell
Measure-Command { python <script.py> } | Select-Object TotalSeconds
```

Confirm the speedup is meaningful relative to the baseline. Then run:

```powershell
rtk uv run prek run <hook-id>
rtk uv run pytest tests/
```

## Examples

### Good: Cascaded SequenceMatcher guards

```python
threshold = 0.94
sm = difflib.SequenceMatcher(None, left_text, right_text)
if sm.real_quick_ratio() < threshold:
    continue
if sm.quick_ratio() < threshold:
    continue
if sm.ratio() >= threshold:
    report_near_duplicate(left_path, right_path, sm.ratio())
```

### Bad: Unconditional ratio() call

```python
ratio = difflib.SequenceMatcher(None, left_text, right_text).ratio()
if ratio >= 0.94:
    report_near_duplicate(left_path, right_path, ratio)
```
