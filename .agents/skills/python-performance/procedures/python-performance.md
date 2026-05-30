# Python Performance — Detailed Reference

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
