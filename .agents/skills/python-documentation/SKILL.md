---
name: python-documentation
description: Standards and guidelines for writing Python documentation, ensuring Google Style adherence and proper type hint integration.
---

# Python Documentation Standards

This skill defines the standards for documenting Python code, following the Google Python Style Guide with specific adaptations for type-annotated code.

## Boundary Contract

### Applies To
- Docstrings in all Python modules, classes, and functions under `src/` and `tests/`

### Produces
- Google Style docstrings that complement type annotations without redundancy

### Does Not Cover
- Type hint standards (`python-typing`)
- Lint rule enforcement (`python-linting`)
- README and architecture docs (`doc-updater`)

## Core Rules

1. **Mandatory Documentation**: Public functions, classes, and methods must have docstrings.
2. **Parameters**: Document all function parameters.
3. **Returns**: Document return values.
4. **Exceptions**: Document exceptions raised.
5. **Maintainability**: Keep comments up-to-date with code changes.
6. **Examples**: Include examples for complex functions.

### Formatting

- Keep the first line as a short summary sentence.
- Include a blank line between the summary and the rest of the docstring.
- Wrap docstring lines at logical breakpoints to keep them readable.
- Write `Examples:` sections in standard **doctest** format (`>>> call(...)` followed
  by the expected output). This makes examples verifiable by `pytest --doctest-modules`.
  Do not use ad-hoc notations like `->`, `=>`, or `-->`.

## Docstring Structure and Section Order

According to the Google Python Style Guide, docstring fields should appear in a specific order.

The docstring must start with a summary line, followed by a blank line, and then the extended description (optional) and specific sections.

### 1. One-Line Summary

The first line should be a concise summary of the object's purpose. It should not reiterate the function name or signature but rather state what the function does (for example, "Fetches rows from a Bigtable.").

### 2. Extended Description (Optional)

If necessary, provide a more detailed description of the function or class's behavior. This paragraph follows the summary line, separated by a blank line.

### 3. Argument/Attribute Sections

The specific fields follow the description. They should be formatted with a section header followed by a colon (for example, `Args:`), and the items should be indented below.

**For Functions & Methods:**

1. **Args:** (or `Arguments:`, though `Args:` is preferred)
   Lists each parameter by name and then a description. If type information is not present in the function signature, it may appear in parentheses; if the signature is type-annotated, omit types to avoid redundancy.
2. **Returns:** (or `Yields:` for generators)
   Describes the semantics of the return value. If the function returns `None`, this section may be omitted.
3. **Raises:**
   Lists all exceptions that are relevant to the interface, followed by a description of when they are raised.

**For Classes:**

1. **Attributes:**
   Lists the public attributes of the class. Note: `__init__` arguments should be documented in the `Args` section of the `__init__` method docstring, not in the class docstring (some teams diverge on this).

### Example Structure

```python
def fetch_smalltable_rows(
    table_handle: "smalltable.Table",
    keys: "Sequence[str]",
    require_all_keys: bool,
) -> dict[str, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle. String keys will be UTF-8 encoded.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table row
            to fetch.
        require_all_keys: If True, only rows with values set for all keys will be
            returned.

    Returns:
        A dict mapping keys to the corresponding table row data fetched. Each row
        is represented as a tuple of strings.

    Raises:
        IOError: An error occurred accessing the smalltable.
    """
    raise NotImplementedError
```

## Type Hint Integration

Since the codebase uses Python 3.12+ with type hints, documentation should obey the following rules to avoid redundancy:

- **Do not** include type information in the docstring (args or returns) if it is already present in the function signature.
- **Do** describe the _purpose_ of the argument or return value.

If a function raises an exception as part of its normal contract, document it in a `Raises:`
section.

## Styling

- Follow the **Google Python Style Guide**.

## Procedure

1. Add or update docstrings for public functions, classes, and methods.
2. Ensure docstring sections follow Google order (`Args`, `Returns`, `Raises`).
3. Remove redundant type annotations from docstrings when signatures already provide types.
4. Verify examples remain accurate after code changes.

## Examples

### ✅ Correct (with Type Hints)

The types are defined in the signature, so the docstring only describes what the argument is.

```python
def repeat_message(msg: str, count: int) -> list[str]:
    """Repeats a message a specific number of times.

    Args:
        msg: The message to repeat.
        count: How many times to repeat the message.

    Returns:
        A list containing the repeated messages.
    """
    return [msg] * count
```

### ❌ Incorrect (Redundant Types)

Do not include the type inside parentheses in `Args` or at the start of `Returns` if they are already in the signature.

```python
def repeat_message(msg: str, count: int) -> list[str]:
    """Repeats a message a specific number of times.

    Args:
        msg (str): The message to repeat.  <-- REDUNDANT
        count (int): How many times...     <-- REDUNDANT

    Returns:
        list[str]: A list containing...    <-- REDUNDANT
    """
    return [msg] * count
```

### ✅ Correct (Doctest Examples)

When a function has behaviour worth illustrating, use standard `doctest` format
so examples are machine-verifiable.

```python
def zero_pad_id(raw: str) -> str:
    """Lowercase and zero-pad single-digit site IDs.

    Examples:
        >>> zero_pad_id("ox1")
        'ox01'
        >>> zero_pad_id("OX01")
        'ox01'
        >>> zero_pad_id("m10")
        'm10'
    """
    ...
```

### ❌ Incorrect (Ad-hoc Examples)

Do not use arrow notation or other non-standard formats in `Examples:` sections.
These are not verifiable by `pytest --doctest-modules`.

```python
def zero_pad_id(raw: str) -> str:
    """Lowercase and zero-pad single-digit site IDs.

    Examples:
        "ox1"  -> "ox01"   <-- NOT DOCTEST FORMAT
        "OX01" -> "ox01"   <-- NOT DOCTEST FORMAT
        "m10"  -> "m10"    <-- NOT DOCTEST FORMAT
    """
    ...
```
