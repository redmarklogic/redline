"""
Test refined extraction prompt against Batch 3 source that had code fence issues.

This script:
1. Loads the refined prompt
2. Queries a known Batch 3 source (AS/NZS 1170.2:2021 Amd 1:2023)
3. Validates response format
4. Compares with previous results to show improvement
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from rl.functions.extraction import validate_extraction_response_format


def test_refined_prompt_against_batch3_source() -> None:
    """Query Batch 3 source with refined prompt and validate output."""

    # Load the refined prompt
    refined_prompt_path = Path("extraction_prompt_refined.txt")
    with open(refined_prompt_path) as f:
        refined_prompt = f.read()

    print("=" * 70)
    print("GREEN PHASE: Testing refined extraction prompt")
    print("=" * 70)
    print(f"\n✓ Loaded refined prompt ({len(refined_prompt)} chars)")
    print(
        "✓ Ready to query: AS/NZS 1170.2:2021 Amd 1:2023 (Batch 3 source that had code fence issue)"
    )

    # Prepare for query
    notebook_id = "dfd5b22d-4b26-4919-a5b0-3d21385ec745"
    source_code = "AS/NZS 1170.2:2021 Amd 1:2023"

    print("\n" + "=" * 70)
    print("NEXT: Run manual extraction query using refined prompt:")
    print("=" * 70)
    print(f"""
From NotebookLM notebook ({notebook_id}):

1. Open the notebook
2. Query: "Extract metadata for the document titled '{source_code}'"
3. Use the refined prompt from: extraction_prompt_refined.txt
4. Paste the response into: batch3_test_response.txt
5. Run this script again to validate

Or run automated: mcp_notebooklm_notebook_query with extracted source_id from batch3_results.json
    """)

    # Check if test response exists
    test_response_path = Path("batch3_test_response.txt")
    if test_response_path.exists():
        with open(test_response_path) as f:
            response = f.read()

        print("=" * 70)
        print("VALIDATING RESPONSE")
        print("=" * 70)
        is_valid, msg = validate_extraction_response_format(response)
        print(f"\nResponse format: {msg}")

        if is_valid:
            data = json.loads(response.strip())
            print("\n✓ Valid JSON parsed successfully")
            print(f"  Standard Code: {data.get('standard_code')}")
            print(f"  Document Status: {data.get('document_status')}")
            print(f"  Amends: {data.get('amends')}")
        else:
            print("\n❌ Format validation failed")
            print(f"Response preview: {response[:200]}")
            sys.exit(1)
    else:
        print("\n⏳ Awaiting test response...")
        print(f"   Save query response to: {test_response_path}")


if __name__ == "__main__":
    test_refined_prompt_against_batch3_source()
