"""
Test-Driven Development: Extraction Prompt Format Validation

RED: Write test showing that extraction responses must be unwrapped JSON.
This test will fail with current prompt (due to code fence wrapping in Batch 3).
"""

import json
import re
from typing import Any


def validate_extraction_response_format(response_text: str) -> tuple[bool, str]:
    """
    Validate that extraction response is raw JSON with no markdown wrapping.

    Args:
        response_text: Raw text from NotebookLM extraction query

    Returns:
        (is_valid, error_message)
    """
    # RULE 1: Must NOT start with markdown code fence
    if response_text.strip().startswith("```"):
        return (False, "❌ FAIL: Response starts with ``` (markdown code fence)")

    # RULE 2: Must NOT end with markdown code fence
    if response_text.strip().endswith("```"):
        return (False, "❌ FAIL: Response ends with ``` (markdown code fence)")

    # RULE 3: Must NOT contain markdown json/yaml/text language marker
    if re.search(r"^```\w+", response_text.strip()):
        return (False, "❌ FAIL: Response contains markdown language marker (```json, ```text, etc)")

    # RULE 4: Must be parseable as JSON
    try:
        json.loads(response_text.strip())
    except json.JSONDecodeError as e:
        return (False, f"❌ FAIL: Not valid JSON - {e}")

    # RULE 5: Must start with { (left brace)
    if not response_text.strip().startswith("{"):
        return (False, f"❌ FAIL: Does not start with {{ (starts with: {response_text.strip()[:20]}...)")

    # RULE 6: Must end with } (right brace)
    if not response_text.strip().endswith("}"):
        return (False, f"❌ FAIL: Does not end with }} (ends with: ...{response_text.strip()[-20:]})")

    return (True, "✓ PASS: Valid raw JSON, no wrapping")


def test_extraction_response_must_be_unwrapped_json() -> None:
    """Test: Response must be raw JSON without markdown code fences."""

    # GOOD: Raw JSON
    good_response = """{
        "standard_code": "AS/NZS 1170.2:2021",
        "title": "Wind actions",
        "year_published": 2021,
        "document_status": "published"
    }"""
    is_valid, msg = validate_extraction_response_format(good_response)
    assert is_valid, f"Expected valid response: {msg}"
    print(msg)

    # BAD: Wrapped in code fences (Batch 3 bug)
    bad_response_1 = """```json
{
    "standard_code": "AS/NZS 1170.2:2021",
    "title": "Wind actions",
    "year_published": 2021,
    "document_status": "published"
}
```"""
    is_valid, msg = validate_extraction_response_format(bad_response_1)
    assert not is_valid, "Expected to reject code-fence wrapped response"
    print(msg)

    # BAD: Only starts with code fence
    bad_response_2 = """```json
{
    "standard_code": "AS/NZS 1170.2:2021"
}"""
    is_valid, msg = validate_extraction_response_format(bad_response_2)
    assert not is_valid, "Expected to reject response with code fence start"
    print(msg)

    # BAD: Only ends with code fence
    bad_response_3 = """{
    "standard_code": "AS/NZS 1170.2:2021"
}
```"""
    is_valid, msg = validate_extraction_response_format(bad_response_3)
    assert not is_valid, "Expected to reject response with code fence end"
    print(msg)


if __name__ == "__main__":
    test_extraction_response_must_be_unwrapped_json()
    print("\n✓ All format validation tests passed")
