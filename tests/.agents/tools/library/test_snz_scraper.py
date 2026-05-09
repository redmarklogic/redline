"""Tests for the Standards NZ scraper (.agents/tools/library/snz_scraper.py)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[4] / ".agents" / "tools" / "library"))

import snz_scraper
from snz_scraper import (
    AmbiguousStandardError,
    StandardNotFoundError,
    StandardRecord,
    get_snz_metadata,
)

_ASSETS = Path(__file__).parents[3] / "assets" / "html"
_DETAIL_FIXTURE = _ASSETS / "snz_asnzs_1158_5_2014.html"


def test_get_snz_metadata_returns_full_record(monkeypatch: pytest.MonkeyPatch) -> None:
    search_html = (_ASSETS / "snz_search_asnzs_1158.html").read_text(encoding="utf-8")
    detail_html = _DETAIL_FIXTURE.read_text(encoding="utf-8")
    responses = iter([search_html, detail_html])
    monkeypatch.setattr(snz_scraper, "_fetch", lambda _url: next(responses))

    record = get_snz_metadata("AS/NZS 1158.5:2014")

    assert isinstance(record, StandardRecord)
    assert record.standard_number == "AS/NZS 1158.5:2014"
    assert "Tunnels and underpasses" in record.title
    assert record.status == "Current"
    assert record.date_published == "14/11/14"
    assert record.publisher == "Standards New Zealand"
    assert record.pages == 60
    assert len(record.previous_versions) >= 1
    assert len(record.similar_standards) >= 1


def test_get_snz_metadata_raises_not_found_when_no_results(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    html = (_ASSETS / "snz_search_not_found.html").read_text(encoding="utf-8")
    monkeypatch.setattr(snz_scraper, "_fetch", lambda _url: html)

    with pytest.raises(StandardNotFoundError, match="AS/NZS 11586"):
        get_snz_metadata("ASNZS 11586")


def test_get_snz_metadata_raises_ambiguous_when_no_results_match_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    html = (_ASSETS / "snz_search_asnzs_115.html").read_text(encoding="utf-8")
    monkeypatch.setattr(snz_scraper, "_fetch", lambda _url: html)

    with pytest.raises(AmbiguousStandardError) as exc_info:
        get_snz_metadata("ASNZS 115")

    msg = str(exc_info.value)
    assert "AS/NZS 115" in msg
    assert "60335.2.115" in msg


def test_get_snz_metadata_raises_ambiguous_when_multiple_standards_match(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    html = (_ASSETS / "snz_search_asnzs_1158.html").read_text(encoding="utf-8")
    monkeypatch.setattr(snz_scraper, "_fetch", lambda _url: html)

    with pytest.raises(AmbiguousStandardError) as exc_info:
        get_snz_metadata("ASNZS 1158")

    msg = str(exc_info.value)
    assert "AS/NZS 1158" in msg
    assert "AS/NZS 1158.5:2014" in msg
    assert "AS/NZS 1158.4:2024" in msg


def test_get_snz_metadata_raises_ambiguous_when_multiple_editions_match(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    html = (_ASSETS / "snz_search_asnzs_1158_0.html").read_text(encoding="utf-8")
    monkeypatch.setattr(snz_scraper, "_fetch", lambda _url: html)

    with pytest.raises(AmbiguousStandardError) as exc_info:
        get_snz_metadata("AS/NZS 1158.0")

    msg = str(exc_info.value)
    assert "AS/NZS 1158.0" in msg
    assert "AS/NZS 1158.0:2005" in msg
    assert "AS/NZS 1158.0:1997" in msg
    assert "1158.1.1" not in msg


def test_get_snz_metadata_resolves_exact_standard_number_to_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    search_html = (_ASSETS / "snz_search_asnzs_1158_0.html").read_text(encoding="utf-8")
    detail_html = _DETAIL_FIXTURE.read_text(encoding="utf-8")
    responses = iter([search_html, detail_html])
    monkeypatch.setattr(snz_scraper, "_fetch", lambda _url: next(responses))

    record = get_snz_metadata("AS/NZS 1158.0:2005")

    assert record.url == "https://www.standards.govt.nz/shop/ASNZS-1158-02005"


# --- Bug 1: parenthetical amendment qualifiers in search result text ---


def test_get_snz_metadata_resolves_when_result_has_parenthetical_qualifier(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # SNZ appends e.g. "(Excludes Amdt 1)" to the display text; should not block resolution
    search_html = (_ASSETS / "snz_search_nzs_1170_5_2004.html").read_text(
        encoding="utf-8"
    )
    detail_html = _DETAIL_FIXTURE.read_text(encoding="utf-8")
    responses = iter([search_html, detail_html])
    monkeypatch.setattr(snz_scraper, "_fetch", lambda _url: next(responses))

    record = get_snz_metadata("NZS 1170.5:2004")

    assert "NZS-1170-52004" in record.url
    assert "SUPP" not in record.url  # must not resolve to the supplement


# --- Bug 2: "Amd N:YEAR" suffix in query should be stripped before searching ---


def test_get_snz_metadata_strips_amendment_suffix_and_resolves_base_standard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Library index codes sometimes include "Amd 1:2005"; SNZ only sells the base standard
    search_html = (_ASSETS / "snz_search_asnzs_1269_1_2005.html").read_text(
        encoding="utf-8"
    )
    detail_html = _DETAIL_FIXTURE.read_text(encoding="utf-8")
    responses = iter([search_html, detail_html])
    monkeypatch.setattr(snz_scraper, "_fetch", lambda _url: next(responses))

    record = get_snz_metadata("AS/NZS 1269.1:2005 Amd 1:2005")

    assert record.url == "https://www.standards.govt.nz/shop/ASNZS-1269-12005"


# --- Bug 3: "Supp N" abbreviation vs "Supplement N" on the SNZ site ---


def test_get_snz_metadata_expands_supp_abbreviation_to_supplement(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Library index and common usage write "Supp 1"; SNZ site uses full word "Supplement 1"
    search_html = (_ASSETS / "snz_search_asnzs_3725_supp1.html").read_text(
        encoding="utf-8"
    )
    detail_html = _DETAIL_FIXTURE.read_text(encoding="utf-8")
    responses = iter([search_html, detail_html])
    monkeypatch.setattr(snz_scraper, "_fetch", lambda _url: next(responses))

    record = get_snz_metadata("AS/NZS 3725 Supp 1:2007")

    assert "3725" in record.url
    assert "SUPPLEMENT" in record.url.upper()
