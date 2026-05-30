---
name: python-patterns
description: Use when writing idiomatic Python -- control-flow, iteration, resource management, composition, or concurrency patterns in this repo
---

# Python Patterns

This skill captures Pythonic _patterns_ (not lint rules) that help keep code readable and robust.
It intentionally avoids redefining rules that already exist in other skills.

For related topics, defer to these canonical skills:

- Style and repo conventions: use the `python-style` skill.
- Typing rules: use the `python-typing` skill.
- Error handling and logging: use the `python-error-handling` skill.
- Function design: use the `python-function-design` skill.
- Class design: use the `python-class-design` skill.
- Domain/value objects: use the `python-domain-modeling` skill.
- Linting and suppressions: use the `python-linting` skill.

## Boundary Contract

### Applies To
- Control-flow, iteration, resource management, and composition patterns in Python code

### Produces
- Idiomatic Python code following established patterns for readability and robustness

### Does Not Cover
- Style and formatting (`python-style`)
- Typing rules (`python-typing`)
- Error handling and logging (`python-error-handling`)
- Class design (`python-class-design`)
- Domain modeling (`python-domain-modeling`)

## Patterns

# In src/faultless/processor.py
class DataProcessor:
    def process(self) -> ProcessResult:
        # ... processing logic ...
        return ProcessResult(findings=findings, stats=stats)
```

Good (script handles display):

```python
# In src/scripts/process_data.py
from ruru import cli

result = processor.process()
cli.bullets(result.stats)  # Script owns display
```

Bad (library prints):

```python
# In src/faultless/processor.py - BAD
class DataProcessor:
    def process(self) -> ProcessResult:
        result = self._compute()
        print(f"Processed {len(result.findings)} items")  # Don't do this!
        return result
```

This pattern ensures:

- Library code is testable without capturing stdout
- Library code is reusable in non-CLI contexts (web APIs, notebooks)
- Clear separation of concerns: logic vs presentation

# Caller picks the strategy
result = calculate_pressure(_rankine, depth=5.0)
```

# Core (pure)
def classify_soil(plasticity_index: float, liquid_limit: float) -> str:
    if plasticity_index > 7 and liquid_limit > 50:
        return "CH"
    return "CL"

# Shell (I/O)
def run_classification(input_path: Path, output_path: Path) -> None:
    data = pd.read_csv(input_path)
    data["classification"] = data.apply(
        lambda row: classify_soil(row["pi"], row["ll"]), axis=1
    )
    data.to_csv(output_path, index=False)
```

# Bad — Unicode subscripts render as empty boxes in default font
ax.set_ylabel("Emission Rate (kg N₂O/d)")

# Good — mathtext rendered by matplotlib's internal engine
ax.set_ylabel(r"Emission Rate (kg $\mathrm{N_2O}$/d)")
```

If a module uses the same label for both plot and non-plot output, declare two
separate constants:

```python
GAS_LABELS = {"ch4": "CH₄", "n2o": "N₂O"}                          # prose / tables
GAS_LABELS_PLOT = {"ch4": r"$\mathrm{CH_4}$", "n2o": r"$\mathrm{N_2O}$"}  # matplotlib
```


See `procedures/python-patterns.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using a while True loop with a manual counter | Use enumerate or itertools.islice to make termination explicit |
| Opening a file with open() without a context manager | Always use with open(...) as f: to guarantee the file is closed on error |
| Using a bare except: to handle cleanup in a resource pattern | Use 	ry/finally or a context manager; bare except swallows KeyboardInterrupt |