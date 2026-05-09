"""Normalise and compare standard code strings for library indexing and SNZ querying."""

import re


def normalise_standard_code(code: str) -> str:
    """Convert a library-filename-derived standard code to a canonical SNZ query string.

    Applies a deterministic chain of regex transformations to undo the encoding
    artefacts introduced when standard designations were derived from filenames:

    - ``ASNZS XXXX``  →  ``AS/NZS XXXX``  (missing slash / space)
    - ``[Amdt N]``    →  ``Amd N``         (bracketed amendment)
    - ``/Amdt N``     →  ``Amd N``         (slash amendment)
    - ``+AN``         →  ``Amd N``         (plus amendment, e.g. ``+A2``)
    - ``.YY.AN``      →  ``:YEAR Amd N``   (two-digit year before amendment)
    - ``.AN``         →  ``Amd N``         (dot amendment suffix)
    - ``-YYYY``       →  ``:YYYY``         (hyphen year → colon year)
    - ``[Source ...]`` / ``[Extract ...]`` → stripped entirely

    Already-canonical codes are returned unchanged.

    Args:
        code: A standard code as stored in the library index, e.g. ``'NZS 3104.A2'``.

    Returns:
        A canonical query string suitable for passing to ``get_snz_metadata``,
        e.g. ``'NZS 3104 Amd 2'``.
    """
    s = code.strip()

    # 1. Extract [Amdt N] bracket before stripping all brackets
    amdt_bracket = re.search(r"\[Amdt\s+(\d+)\]", s, re.IGNORECASE)
    amdt_from_bracket = int(amdt_bracket.group(1)) if amdt_bracket else None

    # 2. Strip all [...] annotations (Source N NNpp, Extract Npp, AS NZS ..., etc.)
    s = re.sub(r"\s*\[[^\]]*\]", "", s).strip()

    # 3. Normalise ASNZS prefix → AS/NZS (handles missing slash and optional space)
    s = re.sub(r"^ASNZS\s*", "AS/NZS ", s, flags=re.IGNORECASE).strip()

    # 4. Convert hyphen-year to colon-year: -YYYY → :YYYY
    s = re.sub(r"-(\d{4})\b", r":\1", s)

    # 5. Slash amendment: /Amdt N → Amd N
    s = re.sub(r"/Amdt\s*(\d+)", r" Amd \1", s, flags=re.IGNORECASE).strip()

    # 6. Plus amendment: +AN → Amd N  (e.g. +A2 → Amd 2)
    s = re.sub(r"\+A(\d+)$", r" Amd \1", s, flags=re.IGNORECASE).strip()

    # 7. Two-digit year before dot-amendment: .YY.AN → :YEAR Amd N
    #    Only fires when YY ≥ 10 (two digits), preventing false matches on
    #    sub-section numbers like .4.2.3 where .4 is only one digit.
    def _year_and_amdt(m: re.Match[str]) -> str:
        yy = int(m.group(1))
        year = 1900 + yy if yy >= 30 else 2000 + yy
        return f":{year} Amd {m.group(2)}"

    s = re.sub(r"\.(\d{2})\.A(\d+)$", _year_and_amdt, s)

    # 8. Dot-amendment suffix: .AN → Amd N  (e.g. .A2 → Amd 2)
    s = re.sub(r"\.A(\d+)$", r" Amd \1", s).strip()

    # 9. Append bracket-extracted amendment if none was introduced by steps 5-8
    if amdt_from_bracket is not None and "Amd" not in s:
        s = f"{s} Amd {amdt_from_bracket}"

    return s.strip()


def strip_amendment_suffix(query: str) -> str:
    """Remove trailing amendment specifiers such as ``Amd 1:2005`` or ``Amd 2``.

    SNZ does not sell amendments as separate products, so the amendment suffix
    must be stripped before submitting a search query.

    Args:
        query: A canonical standard code, e.g. ``'AS/NZS 1269.1:2005 Amd 1:2005'``.

    Returns:
        The code with any trailing amendment specifier removed,
        e.g. ``'AS/NZS 1269.1:2005'``.
    """
    return re.sub(
        r"\s+Amd\s+\d+[:\d]*\s*$", "", query.strip(), flags=re.IGNORECASE
    ).strip()


def normalise_snz_query(query: str) -> str:
    """Strip the AS/NZS family prefix and expand abbreviations for result comparison.

    Used to produce a normalised form that can be compared against the standard
    numbers returned by the SNZ search results page.

    Args:
        query: A standard code with or without a prefix,
               e.g. ``'AS/NZS 1158.5:2014'`` or ``'NZS 3725 Supp 1:2007'``.

    Returns:
        A prefix-free, abbreviation-expanded string, e.g. ``'1158.5:2014'``
        or ``'3725 Supplement 1:2007'``.
    """
    stripped = re.sub(
        r"^(AS/NZS|ASNZS|AS|NZS)\s*", "", query.strip(), flags=re.IGNORECASE
    ).strip()
    stripped = re.sub(r"^ISO(?:/IEC)?\s+", "", stripped, flags=re.IGNORECASE).strip()
    return re.sub(r"\bSupp\b", "Supplement", stripped, flags=re.IGNORECASE)


def snz_query_matches(query_norm: str, result_number: str) -> bool:
    """Return ``True`` if *result_number* matches the normalised query at a word boundary.

    Handles parenthetical display annotations appended by SNZ
    (e.g. ``"(Excludes Amdt 1)"``), and enforces that a partial match only
    succeeds when followed by a recognised separator (``.`` or ``:``) rather
    than a digit.

    Args:
        query_norm: A normalised query string produced by :func:`normalise_snz_query`.
        result_number: A standard number as displayed on the SNZ search results page.

    Returns:
        ``True`` if *result_number* corresponds to the queried standard.
    """
    clean = re.sub(r"\s*\([^)]*\)\s*$", "", result_number).strip()
    result_norm = normalise_snz_query(clean)
    if result_norm == query_norm:
        return True
    if result_norm.startswith(query_norm):
        tail = result_norm[len(query_norm) :]
        return tail[:1] in (".", ":")
    return False
