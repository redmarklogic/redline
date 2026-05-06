"""Tests for standard-code normalisation (.agents/tools/library/naming_conventions.py)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[4] / ".agents" / "tools" / "library"))

from naming_conventions import normalise_snz_query, normalise_standard_code


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        # Already canonical — must be identity
        ("NZS 6807", "NZS 6807"),
        ("AS/NZS 1158.5:2014", "AS/NZS 1158.5:2014"),
        ("NZS 4402.4.2.3", "NZS 4402.4.2.3"),  # sub-section, not year
        ("AS/NZS 1269.1:2005 Amd 1:2005", "AS/NZS 1269.1:2005 Amd 1:2005"),
        # Prefix normalisation: ASNZS → AS/NZS
        ("ASNZS 4911", "AS/NZS 4911"),
        ("ASNZS2041.2", "AS/NZS 2041.2"),  # missing space after prefix
        # Dot-amendment suffix: .AN → Amd N
        ("NZS 3104.A2", "NZS 3104 Amd 2"),
        ("ASNZS 4671.A1", "AS/NZS 4671 Amd 1"),
        # Two-digit year before amendment: .YY.AN → :YEAR Amd N (YY >= 30 → 1900s)
        ("NZS 3112.2.86.A1", "NZS 3112.2:1986 Amd 1"),
        ("NZS 3112.2.86.A2", "NZS 3112.2:1986 Amd 2"),
        # Bracketed amendment: [Amdt N] → Amd N
        ("ASNZS 9001-2008 [Amdt 1]", "AS/NZS 9001:2008 Amd 1"),
        ("ASNZS 1170.0-2002 [Amdt 5]", "AS/NZS 1170.0:2002 Amd 5"),
        ("ASNZS 1170.0-2002 [Amdt 3]", "AS/NZS 1170.0:2002 Amd 3"),
        # Slash amendment: /Amdt N → Amd N
        ("AS/NZS 3500.3/Amdt 3", "AS/NZS 3500.3 Amd 3"),
        ("AS/NZS 3500.1/Amdt 2", "AS/NZS 3500.1 Amd 2"),
        # Source / extract bracket stripping (no amendment)
        ("NZS 3605-2001 [Source 2 26pp]", "NZS 3605:2001"),
        ("NZS 7646-1978 [Source 2 30pp]", "NZS 7646:1978"),
        ("ASNZS 4130-2018 [Source 2 34pp]", "AS/NZS 4130:2018"),
        # Extract bracket stripping
        ("ASNZS 1170.0 [Extract 11pp]", "AS/NZS 1170.0"),
        # Plus-amendment: +AN → Amd N
        ("ASNZS2033-2008+A2", "AS/NZS 2033:2008 Amd 2"),
        # Hyphen year alone (no amendment): -YYYY → :YYYY
        ("ASNZS 4130-2003", "AS/NZS 4130:2003"),
    ],
)
def test_normalise_standard_code(code: str, expected: str) -> None:
    assert normalise_standard_code(code) == expected


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        # Standard prefix stripping
        ("AS/NZS 1158.5:2014", "1158.5:2014"),
        ("ASNZS 1158.5:2014", "1158.5:2014"),
        ("AS 1158.5:2014", "1158.5:2014"),
        ("NZS 6807:1994", "6807:1994"),
        # Supp expansion
        ("NZS 3725 Supp 1:2007", "3725 Supplement 1:2007"),
        ("AS/NZS 1170.1 Supp 1:2002", "1170.1 Supplement 1:2002"),
        # Bug 4: ISO infix must be stripped after AS/NZS prefix
        ("AS/NZS ISO 9001:2008", "9001:2008"),
        ("AS/NZS ISO/IEC 38500:2015", "38500:2015"),
        # ISO infix alone (result side, no AS/NZS prefix)
        ("ISO 9001:2008", "9001:2008"),
        ("ISO/IEC 38500:2015", "38500:2015"),
    ],
)
def test_normalise_snz_query(query: str, expected: str) -> None:
    assert normalise_snz_query(query) == expected
