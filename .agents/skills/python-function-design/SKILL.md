---
name: python-function-design
description: Standards for designing readable, testable Python functions (decomposition, signatures, and side effects).
---

# Python Function Design

This skill covers function design in this repo: decomposition, naming, signatures, and
minimizing side effects.

For related topics:

- Typing: use the `python-typing` skill.
- Docstrings: use the `python-documentation` skill.
- Exceptions/logging: use the `python-error-handling` skill.
- Module-level function ordering and step-down rule: use the `python-module-structure` skill.

## Context & Guidelines

### Scope

Apply these rules whenever you add or refactor Python functions/methods in `src/`.

### Mindset

- Assume the happy path by default. Do not bloat code to accommodate extreme edge cases—alert
  the users and ask for feedback if they want to support an edge case, rather than
  implementing it preemptively.
- Prefer linear, readable code over clever decomposition.
- Do not use `print` unless the user explicitly requests execution-time feedback.

### Do One Thing (One Level of Abstraction)

"Do one thing" is about abstraction level, not line count.

- A function is doing one thing when its body consists of steps one level below the function
  name.
- If you can extract a helper with a name that is not merely a restatement of the
  implementation, the function is likely doing more than one thing.
- Do not force a function to be smaller if it hurts readability or testability.

See: [discussion](https://news.ycombinator.com/item?id=37517329)

### Naming

- Use descriptive names.
- Start function names with a verb in imperative form (except predicate functions).
- Use a noun after the verb.
- Follow `snake_case` naming.
- Common action verbs: `get`, `set`, `reset`, `fetch`, `remove`, `delete`, `compose`, `handle`.
- Common predicate prefixes: `is`, `has`, `can`, `should`.

Examples: `update_user_account`, `calculate_gdp`, `is_testing`.

### Function Shape

- Limit parameters to 5 or fewer (excluding `self` / `cls`).
- Return early (guard clauses) to reduce nesting.
- Never return multiple DataFrames from a single function (e.g., as a tuple). Split into separate
  functions, each returning one DataFrame.
- Apply Pandera `@pa.check_types` only on public methods; never on private methods or classes.

### Input Validation with `@validate_call`

Use Pydantic's `@validate_call` (V2+) as the standard input-validation strategy for public
functions and methods. Do **not** add manual defensive checks (`isinstance`, `assert`,
`if x is None: raise ...`) — that bloats code without meaningful benefit.

**Rules:**

- Apply `@validate_call` to every **public** function/method whose inputs are not already
  guaranteed by the type system at the call site.
- **Never** apply it to private functions/methods (prefixed `_`) — they are internal and
  validated through their public callers.
- **Never** apply it to class definitions or `__init__`; use a Pydantic `BaseModel` or
  `dataclass` instead when the class needs validation.
- Assume Pydantic V2 or higher is always available; no version guards.

```python
from pydantic import validate_call

@validate_call
def calculate_discount(price: float, rate: float) -> float:
    """Return the discounted price."""
    return price * (1 - rate)
```

### Function Arguments

#### Data Comes First

In functions that operate on a DataFrame, pass the data through the first argument.

#### Avoid Flag Arguments (Boolean)

- Avoid boolean flag arguments.
- Instead, split into separate functions for each behavior, or accept a strategy/callback.
- If you need a cross-cutting toggle (e.g., quiet/verbose), use a module-level configuration
  value.
- Do not use `None` as a pseudo-boolean.

#### Avoid Pass-Through Variables for Same-Module Constants

Do not accept a module-level constant as a function parameter when the function lives in the
**same module** as the constant. Access the constant directly.

Pass-through parameters are justified only when the value originates from a **different module**
and the caller genuinely owns the decision of which value to provide.

**Symptoms of the anti-pattern:**

- Every call site passes the same module-level constant.
- The parameter flows unchanged through intermediate functions to a leaf function.
- No test or external caller ever provides a different value.

Bad (pass-through for a same-module constant):

```python
SURVEYS_DIR = DATA_DIR / "ghg_emissions" / "discrete_surveys"

def read_survey_raw(config: SurveyConfig, surveys_dir: Path) -> pd.DataFrame:
    return pd.read_excel(surveys_dir / config.file_name, ...)

def build_tidy_survey(config: SurveyConfig, surveys_dir: Path) -> pd.DataFrame:
    raw = read_survey_raw(config, surveys_dir)  # just forwarding
    ...
```

Good (access the constant directly):

```python
SURVEYS_DIR = DATA_DIR / "ghg_emissions" / "discrete_surveys"

def read_survey_raw(config: SurveyConfig) -> pd.DataFrame:
    return pd.read_excel(SURVEYS_DIR / config.file_name, ...)

def build_tidy_survey(config: SurveyConfig) -> pd.DataFrame:
    raw = read_survey_raw(config)
    ...
```

### Cognitive Complexity

SonarQube enforces a **maximum cognitive complexity of 15** per function. Violations
block the quality gate and must be resolved before merging.

**What inflates cognitive complexity:**

- Each `if` / `elif` / `else` branch adds 1.
- Each `for` / `while` loop adds 1.
- Each `and` / `or` operator in a condition adds 1.
- Nesting multiplies the cost — a branch inside a loop inside another branch adds
  more than the same branch at the top level.
- Duplicate structural branches (two `if`/`elif` arms that do the same thing on
  different inputs) count independently.

**How to reduce complexity:**

1. **Extract a named helper for repeated branch logic.** If two or more branches in a
   loop body perform the same conceptual operation on slightly different inputs, extract
   a helper whose name communicates the intent. Collapsing two `if`/`elif` arms into a
   single call to `_detect_temp_col(row)` removes both the branch penalty and its
   nested checks.
2. **Return early (guard clauses).** Flip `if condition: long body` into
   `if not condition: continue` (or `return`) at the top. This flattens nesting and
   eliminates the need for a corresponding `else`.
3. **Avoid deeply nested conditions.** A guard clause at the start of a loop body is
   cheaper than an `if/elif/else` tree three levels deep.
4. **Do not duplicate structural branches.** If two `elif` arms share the same shape,
   make the differing part a parameter and unify them into one branch.

**Pattern — before (complexity > 15, duplicate branches):**

```python
for row in ws.iter_rows(values_only=True):
    if _cell(row, 8) == "Temp":          # +1 branch
        temp_col = 8
        raw = _cell(row, 0)
        if isinstance(raw, dt.date):     # +1 nested
            current_date = pd.Timestamp(raw)
    elif _cell(row, 7) == "Temp":        # +1 branch (duplicate shape)
        temp_col = 7
        raw = _cell(row, 0)
        if isinstance(raw, dt.date):     # +1 nested (again)
            current_date = pd.Timestamp(raw)
    elif temp_col is not None:           # ...
        ...
```

**Pattern — after (extracted helper, complexity <= 15):**

```python
def _parse_daily_pond_sheet(ws: object) -> list[dict[str, object]]:
    for row in ws.iter_rows(values_only=True):
        detected = _detect_temp_col(row)      # single call, no duplicate branch
        if detected is not None:              # +1
            temp_col = detected
            raw = _cell(row, 0)
            if isinstance(raw, dt.date):      # +1 nested (only once)
                current_date = pd.Timestamp(raw)
        elif temp_col is not None:            # +1
            ...

def _detect_temp_col(row: tuple) -> int | None:   # placed BELOW its caller
    if _cell(row, 8) == "Temp":               # +1
        return 8
    if _cell(row, 7) == "Temp":               # +1
        return 7
    return None
```

### Step-Down Rule

For helper placement rules after extraction, and the step-down ordering that applies
to every module in `src/`, see the `python-module-structure` skill.

### Have No Side Effects

Prefer functions with no side effects (pure functions). When side effects are necessary,
minimize them and document them.

Common side effects include:

- Modifying a mutable object passed in (e.g., list/dict mutation).
- Printing output.
- Writing to files or databases.
- Modifying global/module-level state.
- Making network requests.

### Library vs Script Responsibilities

Library code (under `src/<package>/`) and script code (under `src/scripts/`) have distinct responsibilities:

**Library code provides composable tools:**

- `load_data(path)` - loads from a given path
- `filter_data(data, predicate)` - filters based on a condition
- `transform_data(data, config)` - transforms data
- `format_output(data, format_type)` - formats for display

**Script code orchestrates and makes decisions:**

- Which file to process (path selection)
- Which subset of data to use (prefix filter, date range)
- Which processing steps to apply (compose library functions)
- How to present output (CLI formatting, file writing)

**Anti-pattern: "Convenience" functions that hide business decisions**

Bad (library function hardcodes business logic):

```python
# In library code - BAD
def build_copyeditor_rules_prompt() -> str:
    """Load the rulebank and format the copyeditor rule prompt."""
    rulebank = load_rulebank()
    copy_rules = select_rulebank_rules(rulebank=rulebank, prefix="H")  # Hardcoded!
    return build_rules_prompt(rules=copy_rules)
```

Good (library provides primitives, script composes):

```python
# In library code - GOOD
from faultless.domain.repository import RulebankRepository
from faultless.functions.rulebank import build_rules_prompt

# In script code - GOOD
def build_copyeditor_prompt() -> str:
    repo = RulebankRepository(path=RULEBANK_PATH)
    prompts = repo.get_prompts(prefix="H")  # Script decides "H"
    return build_rules_prompt(prompts_df=prompts)
```

This separation enables:

- Library code stays reusable (no hardcoded business rules)
- Scripts compose primitives to express intent
- Easy to add new scripts with different selections without changing library code

### Anonymous Functions

Only use anonymous functions (e.g., `lambda`) when it improves readability.

- The function does not already exist.
- The function is only used once.
- The function is not tested directly.

### Magic Numbers

- Avoid "magic numbers" in code. Nearly all numbers should have variable names (or a short
  explanation) so intent is clear.
- Some values like `0` can be acceptable when they serve a functional (not numerical) purpose.

### Don't Repeat Yourself (DRY)

- Avoid copy/paste logic. Prefer a single implementation and reuse it.
- Functionalize repeated code where it improves readability and testability.
- Use the "Zero, One, Infinity" rule as a heuristic:
  - Support zero occurrences.
  - Handle one occurrence simply.
  - If you have many occurrences, extract a function/data structure.

Avoid over-functionalization: do not hard-code things as identical when they may diverge in
the future. Domain-driven design can help prevent over-DRY abstractions.

## Procedure

0. **Trace call sites first.** Before designing any new function or module, identify every
   place it will be called. If multiple call sites contain the same multi-step sequence
   (e.g., A → B → C always appear together), wrap them in a single higher-level function at
   the design stage — not as a follow-up refactor.
1. Name the function based on intent (verb + noun; `snake_case`).
2. Design the signature:
   - Keep it small (<= 5 parameters).
   - Prefer keyword-only for arguments that reduce readability when passed positionally.
   - If it operates on a DataFrame, put the DataFrame first.
   - Avoid boolean flags.
3. Apply `@validate_call` if the function is public and its inputs are not statically
   guaranteed — do not add manual defensive checks instead.
4. Write the happy path first, as linear code at one abstraction level.
5. Add guard clauses for **business-logic** conditions only (not type checks).
6. Isolate side effects (prefer pure core logic + thin boundary wrapper).
7. Add tests when the logic is non-trivial.

## Examples

### Good Example (returns new data; no side effects)

```python
def append_and_sort_list(lst: list[int], element: int) -> list[int]:
    """Return a new list with the element appended and sorted."""

    new_lst = lst + [element]
    return sorted(new_lst)
```

### Good Example (data-driven over repeated structure)

```python
_QUANTITIES = [
    "plate_rl",
    "rod_length",
    "first_easting",
]


def make_values_by_name(*, identity: str) -> dict[str, list[object]]:
    return {f"{quantity}_{identity}": [] for quantity in _QUANTITIES}
```
