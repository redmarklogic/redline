---
name: python-testing-unit
description: Standards for writing unit tests in this repo.
---

# Python Unit Testing

This skill defines conventions for unit testing in this repo.

## Context & Guidelines

### Scope

Apply these rules when writing or updating tests under `tests/`.

### Core Philosophy

**Test behavior, not implementation.** Tests should verify that code works correctly, not how it achieves that. If you refactor internal logic while preserving external behavior, tests should still pass.

This approach prevents the **Fragile Test Problem**, where tests break every time code is refactored, turning the test suite from an asset into a burden. By focusing on observable behavior (outputs, state changes, exceptions) rather than internal mechanics (which private methods are called, in what order), you ensure tests enable refactoring rather than hinder it.

### Testing Styles

**State-based testing (Classicist approach)**: Assert on return values, object state, and observable side effects. This is the preferred style because it decouples tests from implementation details.

**Interaction-based testing (Mockist approach)**: Verify that specific methods were called with specific arguments. Use this sparingly and only for external boundaries (APIs, databases, file I/O). Overusing this style couples tests to implementation and makes refactoring painful.

### Core Rules

- Use pytest.
- Prefer the arrange / act / assert structure.
- Keep assertions at the end of the test; split tests if needed.
- **Test essential functionality only** — one test per function/method is often sufficient.
- **Avoid over-testing parameter variations** — don't test every possible input combination unless they represent distinct behavioral paths.
- **Mock only external dependencies** — APIs, file I/O, databases, third-party services. Follow the principle: **"Don't mock what you don't own."** Don't mock internal functions unless necessary.
- **Verify outcomes, not method calls** — prefer state-based testing (assert on return values and state changes) over interaction-based testing (verifying which internal methods were called).
- **Use clear, concise test function names** in preference to docstrings or comments. Always avoid "block" comments e.g. `# ---------` to separate sections to preface before a function. Using `# Arrange`, `# Act`, `# Assert` is good practice within functions.

## What to Test

### DO Test

- **Core functionality works** — the function/method produces expected outputs
- **State changes correctly** — objects are modified as expected
- **Error handling works** — exceptions are raised when appropriate
- **Integration points work** — external dependencies are called (via mocks)

### DON'T Test

- **Domain value objects directly** — never create a `test_<value_object>.py` file. Value objects (Pydantic `BaseModel` subclasses in `domain/value_objects/`) are exercised indirectly through the service or function that uses them. See `python-domain-modeling` skill.
- **Every parameter permutation** — use **equivalence classes** and **boundary values** instead. If a function handles all positive integers the same way, test one representative value and the boundaries (0, -1, maxint).
- **Private functions** (prefixed with `_`) — these are implementation details, not public contracts. Testing them couples your test suite to refactoring decisions and breaks when you optimize internal logic. Always test through the public API.
- **Internal implementation details** — which private methods are called, in what order
- **Framework internals** — trust that third-party libraries work correctly
- **Trivial getters/setters** — if a property just returns a value, skip it

## Procedure

1. Select a concise test function name, avoiding verbose docstrings and comments unless absolutely needed for clarity.
2. Arrange inputs and fixtures.
3. Act by calling the function under test.
4. Assert results at the end.

## Examples

### Good Example: Behavior-Focused

```python
def test_build_report_works() -> None:
    """Test that build_report creates a report with expected data."""
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
    """Test that fetch_user_data retrieves data from API."""
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

✅ **Good candidates for mocking:**

- HTTP clients (requests, httpx)
- Database connections (SQLAlchemy sessions)
- File system operations (Path.open, Path.exists)
- External APIs (Stripe, SendGrid, AWS SDK)
- Time/random functions (time.time, random.randint)

❌ **Bad candidates for mocking:**

- Your own internal functions
- Domain model methods
- Business logic

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

# Bad: using block comments to separate sections before a function
# ---------
# Test that calculate_discount applies the percentage correctly.
# ---------
def test_calculate_discount_applies_percentage() -> None:
    ...
```
