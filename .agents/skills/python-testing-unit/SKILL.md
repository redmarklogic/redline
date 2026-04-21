---
name: python-testing-unit
description: Standards for writing unit tests in this repo.
---

# Python Unit Testing

This skill defines conventions for unit testing in this repo.

## Boundary Contract

### Applies To
- Unit tests under `tests/` using pytest

### Produces
- Tests following Arrange/Act/Assert, equivalence classes, and parametrize conventions

### Does Not Cover
- API endpoint testing (`python-testing-api`)
- TDD workflow (`test-driven-development`)
- General style (`python-style`)

## Context & Guidelines

### Scope

Apply these rules when writing or updating tests under `tests/`.

### Core Philosophy

**Test behavior, not implementation.** Tests should verify that code works correctly, not how it achieves that. If you refactor internal logic while preserving external behavior, tests should still pass.

This approach prevents the **Fragile Test Problem** (also called "change detector tests"), where tests break every time code is refactored, turning the test suite from an asset into a burden. By focusing on observable behavior (outputs, state changes, exceptions) rather than internal mechanics (which private methods are called, in what order), you ensure tests enable refactoring rather than hinder it.

### Testing Styles

**State-based testing (Classicist approach)**: Assert on return values, object state, and observable side effects. This is the preferred style because it decouples tests from implementation details.

**Interaction-based testing (Mockist approach)**: Verify that specific methods were called with specific arguments. Use this sparingly and only for external boundaries (APIs, databases, file I/O). Overusing this style couples tests to implementation and makes refactoring painful.

**Mixed-layer testing**: Execute the real system where possible and verify end state through the public API rather than mocking internal layers. This tests true behavior, is less fragile, and can run faster than mock-heavy tests.

### Core Rules

- Use pytest.
- Prefer the arrange / act / assert structure (equivalent to given / when / then from BDD).
- Keep assertions at the end of the test; split tests if needed.
- Never interleave actions and assertions (e.g. arrange-assert-act-assert). Each test validates exactly one behavior.
- **Test essential functionality only** — one test per function/method is often sufficient.
- **Avoid over-testing parameter variations** — don't test every possible input combination unless they represent distinct behavioral paths.
- **Mock only external dependencies** — APIs, file I/O, databases, third-party services. Follow the principle: **"Don't mock what you don't own."** Don't mock internal functions unless necessary.
- **Verify outcomes, not method calls** — prefer state-based testing (assert on return values and state changes) over interaction-based testing (verifying which internal methods were called).
- **Use clear, concise test function names** in preference to docstrings or comments. Always avoid "block" comments e.g. `# ---------` to separate sections to preface before a function. Using `# Arrange`, `# Act`, `# Assert` is good practice within functions.
- **Tests must be independent and deterministic** — no test should depend on the run order or state left behind by another test. Consider using `pytest-randomly` to detect hidden dependencies.

## Test Strategy

Prioritize what to test using this framework:

- **Recent**: Newly added, repaired, or refactored code
- **Core**: The application's essential functions (unique selling propositions)
- **Risk**: Important areas relying on third-party code or rarely exercised by the team
- **Problematic**: Code that frequently breaks or generates defect reports
- **Expertise**: Features understood by only a limited subset of people

Avoid writing tests merely to achieve 100% code coverage — this wastes development time and masks unused code.

## What to Test

### DO Test

- **Core functionality works** — the function/method produces expected outputs
- **State changes correctly** — objects are modified as expected
- **Error handling works** — exceptions are raised when appropriate (use `pytest.raises()` with `match` for error message validation)
- **Different starting states** — e.g. empty vs. populated inputs, default vs. custom config
- **All possible error states** — not just the happy path
- **Integration points work** — external dependencies produce the expected result when called (mock the boundary, assert on the returned outcome)

### DON'T Test

- **Domain value objects directly** — never create a `test_<value_object>.py` file. Value objects (Pydantic `BaseModel` subclasses in `domain/value_objects/`) are exercised indirectly through the service or function that uses them. See `python-domain-modeling` skill.
- **Every parameter permutation** — use **equivalence classes** and **boundary values** instead. If a function handles all positive integers the same way, test one representative value and the boundaries (0, -1, maxint).
- **Private functions** (prefixed with `_`) — these are implementation details, not public contracts. Testing them couples your test suite to refactoring decisions and breaks when you optimize internal logic. Always test through the public API.
- **Internal implementation details** — which private methods are called, in what order
- **Framework internals** — trust that third-party libraries work correctly
- **Trivial getters/setters** — if a property just returns a value, skip it

## Procedure

1. Start with a non-trivial "happy path" test case — a scenario where the user does everything right and no errors occur.
2. Select a concise test function name; avoid verbose docstrings and comments unless absolutely needed for clarity.
3. Arrange inputs and fixtures (push complex setup into fixtures, keep the test body minimal).
4. Act by calling the function under test.
5. Assert results at the end (all assertions grouped together, never interleaved with further actions).
6. Add additional test cases for: interesting starting states, boundary values, and all possible error states.

## Test Case Generation Strategy

When creating tests for a feature, follow this sequence:

1. **Happy path first**: A non-trivial success scenario with representative inputs.
2. **Different starting states**: e.g. empty vs. populated, default config vs. custom flags enabled.
3. **Boundary values**: Edges where behavior changes (0, -1, empty list, max values).
4. **Error states**: All exception paths, invalid inputs, missing data.
5. **Interesting end states**: e.g. verifying a deletion leaves an empty result, or a conditional toggle changes output structure.

## Fixture Best Practices

- **Define shared fixtures in `conftest.py`** — pytest auto-discovers them; never explicitly import `conftest.py`.
- **Prefer a single top-level `conftest.py`** — only add subdirectory `conftest.py` files when fixtures are genuinely specific to a sub-package.
- **Fixtures local to one test file** may be defined directly in that test module.
- **Use `yield` for teardown** — code before `yield` is setup; code after is guaranteed cleanup (runs even if the test fails).
- **Use fixture scope wisely** — default `function` scope is safest for isolation. Only widen to `module`/`session` for expensive setup (e.g. database connections). Combine with a narrow-scope fixture that resets state per test to maintain isolation.
- **Avoid `autouse=True`** unless the fixture must run for every test in scope (e.g. timing hooks). Prefer explicit fixture injection.
- **Use `@pytest.mark.usefixtures` for side-effect-only fixtures** — fixtures that patch or configure but return no value the test body references. Never inject them as function parameters (triggers ARG001/ARG002).

## Markers

- **`@pytest.mark.skip(reason="...")`** — bypass a test entirely; always provide a `reason`.
- **`@pytest.mark.skipif(condition, reason="...")`** — skip conditionally (e.g. platform-specific).
- **`@pytest.mark.xfail(reason="...", strict=True)`** — mark a test as expected to fail. Use `strict=True` so unexpected passes are reported as failures.
- **When to use `xfail`**: TDD (mark unimplemented features), tracking known defects.
- **When NOT to use `skip`/`xfail`**: Do not use for brainstorming future behaviors — this violates YAGNI.
- **Register custom markers** in `pyproject.toml` under `[tool.pytest.ini_options]` and use `--strict-markers` to catch typos.

## Examples

### Good Example: Behavior-Focused

```python
def test_build_report_works() -> None:
    data = {"metric": 42}

    result = build_report(data)

    assert result.metric == 42
    assert result.timestamp is not None
```

### Bad Example: Over-Testing Implementation

```python
# Don't test every parameter variation
def test_build_report_with_default_format() -> None: ...
def test_build_report_with_json_format() -> None: ...
def test_build_report_with_xml_format() -> None: ...
def test_build_report_with_csv_format() -> None: ...

# Instead, test once with a representative case
def test_build_report_works() -> None:
    result = build_report(data, format="json")
    assert result.format == "json"
```

### Bad Example: Testing Internal Calls

```python
# Don't verify which internal functions were called
def test_process_data_calls_validator(mocker) -> None:
    mock_validator = mocker.patch("module._validate_data")
    process_data({"key": "value"})
    mock_validator.assert_called_once()  # Too coupled to implementation

# Instead, test the outcome
def test_process_data_works() -> None:
    result = process_data({"key": "value"})
    assert result.is_valid is True
```

### Good Example: Minimal Mocking

```python
# Mock only external dependencies
def test_fetch_user_data_works(mocker) -> None:
    mock_http = mocker.patch("module.requests.get")
    mock_http.return_value.json.return_value = {"name": "Alice"}

    result = fetch_user_data(user_id=123)

    assert result["name"] == "Alice"
```

## When to Write Multiple Tests

Write multiple tests for the same function only when:

1. **Distinct behavioral paths exist** — success vs. error cases
2. **Edge cases are critical** — empty inputs, boundary values, special states
3. **Multiple integration points** — different external dependencies
4. **Different starting states** — e.g. empty database vs. populated database produce fundamentally different behavior

### Example: Multiple Tests Justified

```python
def test_parse_config_with_valid_yaml() -> None:
    result = parse_config("valid.yaml")
    assert result.database_url is not None

def test_parse_config_raises_on_invalid_yaml() -> None:
    with pytest.raises(ConfigError):
        parse_config("invalid.yaml")

def test_parse_config_with_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        parse_config("nonexistent.yaml")
```

## Parametrize Wisely

Use `@pytest.mark.parametrize` only when:

- Testing the same logic with different representative inputs
- Verifying boundary conditions
- NOT when testing implementation details

**Important: Parameter names must be a tuple, not a string.**

```python
# Correct: Use a tuple for parameter names
@pytest.mark.parametrize(
    ("prefix", "expected_count"),
    [("H", 12), ("S", 8), ("A", 5)],
    ids=["filter_H_rules", "filter_S_rules", "filter_A_rules"],
)
def test_filter_rules_by_prefix(prefix: str, expected_count: int) -> None:
    result = filter_rules(rulebank, prefix=prefix)
    assert len(result) == expected_count

# Incorrect: Don't use a comma-separated string
# @pytest.mark.parametrize(
#     "prefix,expected_count",  # Wrong! This triggers PT006
```

## Equivalence Classes and Boundary Values

Instead of exhaustive testing, use **equivalence partitioning** and **boundary value analysis**:

- **Equivalence class**: A set of inputs that are handled the same way by the code. Test one representative from each class.
- **Boundary value**: The edges where behavior changes (0, -1, empty string, null, max values). These are where bugs hide.

### Example: Testing Age Validation

```python
# Function validates: 0 <= age <= 120
# Equivalence classes: negative, valid (0-120), excessive (>120)
# Boundaries: -1, 0, 120, 121

@pytest.mark.parametrize(
    ("age", "is_valid"),
    [
        (-1, False),      # Boundary: just below valid range
        (0, True),        # Boundary: minimum valid
        (25, True),       # Representative: middle of valid range
        (120, True),      # Boundary: maximum valid
        (121, False),     # Boundary: just above valid range
    ],
    ids=["below_min", "min_valid", "mid_valid", "max_valid", "above_max"],
)
def test_validate_age(age: int, is_valid: bool) -> None:
    assert validate_age(age) == is_valid
```

## Side-Effect-Only Fixtures

Some fixtures exist only to patch external I/O (e.g. `mocker.patch(...)` calls). They produce no value that the test body uses directly. **Never inject them as function or method parameters**; doing so triggers `ARG001` (standalone functions) or `ARG002` (class methods) for unused arguments. Prefixing with `_` to silence the linter triggers `PT019` (fixture without value injected as parameter).

**Quick check before writing any test:** ask "does the test body reference this fixture by name?" If no — use `@pytest.mark.usefixtures` instead of a parameter.

Instead, apply them at the class or function level via `@pytest.mark.usefixtures`:

```python
# Bad: standalone async function — triggers ARG001
@pytest.mark.asyncio
async def test_something(mock_llm_flow) -> None:  # ARG001: mock_llm_flow never used in body
    result = await my_service()
    assert isinstance(result, MyResult)

# Bad: class method — triggers ARG002
async def test_something(self, mock_pipeline_boundaries, mock_rulebank_repo): ...

# Also bad: underscore prefix "fixes" ARG001/ARG002 but triggers PT019
async def test_something(_mock_llm_flow) -> None: ...

# Good (standalone): apply decorator directly on the function
@pytest.mark.asyncio
@pytest.mark.usefixtures("mock_llm_flow")
async def test_something() -> None:
    result = await my_service()
    assert isinstance(result, MyResult)

# Good (class): declare at the class level; pytest applies the fixture automatically
@pytest.mark.usefixtures("mock_pipeline_boundaries")
class TestSomething:
    async def test_something(self, mock_rulebank_repo): ...
```

If every test in a class needs the same side-effect fixture, put `@pytest.mark.usefixtures` on the class. If only some tests need it, put it on those individual test methods. For standalone test functions, apply `@pytest.mark.usefixtures` directly on each function that needs it.

## Mocking Guidelines

### "Don't Mock What You Don't Own"

Mock only code at the boundaries of your system:

**Good candidates for mocking:**

- HTTP clients (requests, httpx)
- Database connections (SQLAlchemy sessions)
- File system operations (Path.open, Path.exists)
- External APIs (Stripe, SendGrid, AWS SDK)
- Time/random functions (time.time, random.randint)

**Bad candidates for mocking:**

- Your own internal functions (but protocol-based architectural boundaries like `DocumentFacade` are NOT internal functions — they are deliberate abstraction seams suitable for recording fakes)
- Domain model methods
- Business logic

### Always Use `autospec=True`

When creating mocks, always use `autospec=True` to bind the mock to the real object's specification. Without it, mocks silently accept misspelled method names or invalid parameters (mock drift). The only exception is objects that dynamically add attributes at runtime.

```python
# Good: autospec catches interface mismatches
mock_service = mocker.patch("module.MyService", autospec=True)

# Bad: silent acceptance of any method name or argument
mock_service = mocker.patch("module.MyService")
```

### Prefer `monkeypatch` for Simple Substitutions

Use the built-in `monkeypatch` fixture for environment variables (`monkeypatch.setenv`), simple attribute replacement (`monkeypatch.setattr`), and dictionary patching (`monkeypatch.setitem`). Reserve `mocker.patch` for when you need return value configuration or call tracking.

### Test Doubles for Protocol-Based Design

When testing code that depends on a protocol (e.g. `DocumentFacade`), prefer a purpose-built recording fake over generic mocking. A recording fake (sometimes called a "spy" or "fake") implements the protocol and captures calls for later assertion. This approach tests behavior without coupling to mock library internals.

```python
class RecordingFacade:
    """Captures all facade method calls for assertion."""
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple, dict]] = []

    def add_heading(self, text: str, *, level: int) -> None:
        self.calls.append(("add_heading", (text,), {"level": level}))
    # ... other protocol methods
```

### Example: Proper Mocking Boundary

```python
# Good: Mock the external HTTP library
def test_get_user_profile_works(mocker) -> None:
    mock_get = mocker.patch("myapp.services.requests.get")
    mock_get.return_value.json.return_value = {"name": "Alice"}

    profile = get_user_profile(user_id=123)

    assert profile.name == "Alice"

# Bad: Mock internal business logic
def test_process_order_calls_validator(mocker) -> None:
    mock_validate = mocker.patch("myapp.orders._validate_order")
    process_order(order_data)
    mock_validate.assert_called_once()  # Fragile! Breaks on refactor
```

### Example: Good naming of test functions

```python
# Good: Clear, concise test function names
class TestCalculateDiscount:
    def test_applies_percentage() -> None: ...

# Bad: Redundant naming from parent class
class TestCalculateDiscount:
    def test_calculate_discount_applies_percentage() -> None: ...

# Bad: Using a docstring when it adds no value beyond the function name
def test_calculate_discount_applies_percentage() -> None:
    """Test that calculate_discount applies the percentage correctly."""
    ...
```

## Built-in Fixtures

Use these before reaching for third-party tools:

- **`tmp_path`** (function scope): fresh temporary directory as `pathlib.Path`. Use for any test that writes files.
- **`tmp_path_factory`** (session scope): call `.mktemp("name")` to create directories shared across tests.
- **`capsys`**: capture `stdout`/`stderr`. Call `capsys.readouterr()` to get `.out` and `.err` strings.
- **`monkeypatch`**: dynamic runtime substitution (environment variables, attributes, dict items). Automatically undone after the test.

## Anti-Patterns

| Anti-Pattern | Why It Hurts |
| --- | --- |
| **Change detector tests** | Over-mocking tests implementation, not behavior. Breaks on valid refactors. |
| **Mock drift** | Forgetting `autospec=True` lets mocks accept invalid calls silently. |
| **Coverage-driven tests** | Adding meaningless tests for 100% coverage masks unused code. |
| **Duplicate test names** | Python silently ignores the first function — hidden gaps in the suite. |
| **Interleaved assertions** | Arrange-Assert-Act-Assert obscures intent and makes failures hard to diagnose. |
| **Testing only happy paths** | Ignoring error states, empty inputs, and boundary values leaves bugs hiding at the edges. |
