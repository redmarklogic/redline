---
name: python-module-structure
description: Use when ordering functions within a Python module -- step-down rule, public-before-private ordering, or separating executable code from implementation
---

# Python Module Structure

This skill governs the internal organisation of Python modules: how functions are
ordered, when to extract helpers, and what code may appear at module level.

For related topics:

- Function design (signatures, parameters, side effects): use the `python-function-design` skill.
- Script cell structure and Spyder conventions: use the `python-script` skill.
- Cognitive complexity reduction through helper extraction: use the `python-function-design` skill.

## Boundary Contract

### Applies To
- Function and definition ordering within any Python module under `src/` and `tests/`

### Produces
- Modules following the step-down rule with public-before-private ordering

### Does Not Cover
- Function design and signatures (`python-function-design`)
- Script cell structure (`python-script`)
- General style (`python-style`)

# src/ghgmod/functions/loaders.py
def load_daily_pond_readings(path: Path) -> pd.DataFrame:
    ...
```

**Not acceptable** (execution in a package module):

```python
# src/ghgmod/functions/loaders.py  ← WRONG
df = load_daily_pond_readings(Path("data/..."))  # runs on import
print(df.head())
```

**Acceptable** (execution lives in a script):

```python
# src/scripts/build_pond_dataset.py
from ghgmod.functions.loaders import load_daily_pond_readings

df = load_daily_pond_readings(DATA_DIR / "wastewater_process/daily_pond_readings/...")
```

---

# Public function to add a task
def add_task(task: str) -> None:
    if _validate_task(task):
        tasks.append(task)
        _log_action(f"Task added: {task}")
    else:
        print("Task validation failed.")


# Public function to complete a task
def complete_task(task: str) -> None:
    if task in tasks:
        tasks.remove(task)
        completed_tasks.append(task)
        _log_action(f"Task completed: {task}")
    else:
        print("Task not found.")


# Private helper: validate a task (follows the public functions it supports)
def _validate_task(task: str) -> bool:
    return isinstance(task, str) and bool(task.strip())


# Private helper: log an action
def _log_action(action: str) -> None:
    print(f"Action: {action}")
```

# Private function to validate a task  ← helper defined before its caller
def _validate_task(task):
    return isinstance(task, str) and bool(task.strip())


# Private function to log actions      ← helper defined before its caller
def _log_action(action):
    print(f"Action: {action}")


# Public function to add a task        ← caller buried below its helpers
def add_task(task):
    if _validate_task(task):
        tasks.append(task)
        _log_action(f"Task added: {task}")
```


See `procedures/python-module-structure.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Defining private helpers before the public functions that call them | Public functions first; private helpers immediately below their single caller |
| Mixing executable script code with importable functions at module level | Guard executable code with if __name__ == '__main__' or move to a separate script |
| Grouping functions by type (all helpers together) instead of by call order | Order by step-down rule: each function calls only functions defined below it |