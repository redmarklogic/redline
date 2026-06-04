---
name: python-performance
description: Use when profiling or optimising Python code -- choosing a profiling tool, diagnosing bottlenecks, or applying algorithmic fixes
paths: "src/**/*.py,tests/**/*.py"
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


See `procedures/python-performance.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Optimising before profiling | Profile first with cProfile or py-spy; never guess the bottleneck |
| Using a list comprehension to build a set | Use a set comprehension {x for x in ...} — O(n) vs O(n log n) for membership checks |
| Repeated DataFrame .apply() for element-wise operations | Prefer vectorised pandas/numpy operations; .apply() with Python lambdas is slow |