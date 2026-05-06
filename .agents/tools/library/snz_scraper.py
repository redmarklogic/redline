"""Scrape a standard record from Standards New Zealand (standards.govt.nz)."""

import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser

from naming_conventions import (
    normalise_snz_query,
    normalise_standard_code,
    snz_query_matches,
    strip_amendment_suffix,
)
from pydantic import BaseModel, ConfigDict, Field, validate_call

SNZ_BASE_URL = "https://www.standards.govt.nz"
SNZ_SEARCH_URL = f"{SNZ_BASE_URL}/search/doSearch"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-NZ,en;q=0.9",
}


class StandardNotFoundError(Exception):
    """Raised when no standard matching the query exists on standards.govt.nz."""


class AmbiguousStandardError(Exception):
    """Raised when a query matches zero or multiple standards on standards.govt.nz."""


class StandardRecord(BaseModel):
    """A standard record scraped from Standards New Zealand."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    standard_number: str = Field(
        description="Designation of the standard, e.g. 'AS/NZS 1158.5:2014'.",
        alias="standard_number",
    )
    title: str = Field(
        description="Full descriptive title of the standard.",
        alias="title",
    )
    status: str = Field(
        description="Publication lifecycle status, e.g. 'Current', 'Superseded', 'Withdrawn'.",
        alias="status",
    )
    date_published: str = Field(
        description="Publication date as displayed on the SNZ site (DD/MM/YY).",
        alias="date_published",
    )
    publisher: str = Field(
        description="Publishing body. Always 'Standards New Zealand' for this scraper.",
        alias="publisher",
    )
    abstract: str = Field(
        description="Short scope-and-purpose summary taken from the product page.",
        alias="abstract",
    )
    pages: int | None = Field(
        default=None,
        ge=1,
        description="Total page count of the document. None if not stated on the page.",
        alias="pages",
    )
    url: str = Field(
        description="Canonical URL of the standard's detail page on standards.govt.nz.",
        alias="url",
    )
    previous_versions: list[str] = Field(
        default_factory=list,
        description="Designations of earlier editions listed on the detail page.",
        alias="previous_versions",
    )
    similar_standards: list[str] = Field(
        default_factory=list,
        description="Designations of related standards suggested by the SNZ site.",
        alias="similar_standards",
    )


@validate_call
def get_snz_metadata(query: str) -> StandardRecord:
    """Search for a standard on Standards NZ and return its full record.

    Makes two HTTP requests: one to the search page to locate the standard,
    then one to the detail page to extract the full record.

    Args:
        query: Free-text search term, e.g. ``"AS/NZS 1158.5:2014"``.

    Returns:
        A populated :class:`StandardRecord` for the first matching result.

    Raises:
        :exc:`StandardNotFoundError`: When no standard matches ``query``.
        :exc:`AmbiguousStandardError`: When ``query`` matches zero or multiple standards.
    """
    canonical_query = strip_amendment_suffix(normalise_standard_code(query))
    params = {
        "Search": canonical_query,
        "start": 0,
        "filterby": "standards",
        "ICSCode": "*",
    }
    search_url = f"{SNZ_SEARCH_URL}?{urllib.parse.urlencode(params)}"
    search_html = _fetch(search_url)
    detail_url = _parse_search(search_html, canonical_query)
    detail_html = _fetch(detail_url)
    return _parse(detail_html, detail_url)


def _parse_search(html: str, query: str) -> str:
    """Return the detail page URL for the single standard matching *query*.

    Parses all search results, filters to those whose standard number starts
    with the normalised query, then enforces uniqueness:

    - 0 total results → :exc:`StandardNotFoundError`
    - results exist but none match the normalised query →
      :exc:`AmbiguousStandardError` listing what was found
    - >1 results match → :exc:`AmbiguousStandardError` listing the matches
    - exactly 1 result matches → returns its absolute detail URL

    Args:
        html: Raw HTML of the SNZ search results page.
        query: The original search term, e.g. ``"AS/NZS 1158.0:2005"``.

    Returns:
        Absolute URL of the matching standard's detail page.

    Raises:
        :exc:`StandardNotFoundError`: When the search page has no results at all.
        :exc:`AmbiguousStandardError`: When zero or multiple results match *query*.
    """
    parser = _SearchPageParser()
    parser.feed(html)

    all_results = parser.results  # list of (standard_number, url)

    if not all_results:
        raise StandardNotFoundError(
            f"No standard found matching {query!r} on standards.govt.nz"
        )

    query_norm = normalise_snz_query(query)
    matches = [
        (num, url) for num, url in all_results if snz_query_matches(query_norm, num)
    ]

    if not matches:
        found = ", ".join(num for num, _ in all_results)
        raise AmbiguousStandardError(
            f"No result matches {query!r}. Search returned: {found}. "
            f"Check the standard number and try again."
        )

    if len(matches) > 1:
        options = ", ".join(num for num, _ in matches)
        raise AmbiguousStandardError(
            f"Query {query!r} matches multiple standards: {options}. "
            f"Provide a more specific identifier, e.g. including the year."
        )

    return f"{SNZ_BASE_URL}{matches[0][1]}"


def _fetch(url: str) -> str:
    """Fetch *url* and return its decoded content as a string."""
    req = urllib.request.Request(url, headers=_HEADERS)
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _parse(html: str, url: str) -> StandardRecord:
    """Parse a SNZ standard detail page into a :class:`StandardRecord`."""
    parser = _DetailPageParser()
    parser.feed(html)
    return StandardRecord(
        standard_number=parser.standard_number,
        title=parser.title,
        status=parser.status,
        date_published=parser.date_published,
        publisher="Standards New Zealand",
        abstract=parser.abstract,
        pages=parser.pages,
        url=url,
        previous_versions=parser.previous_versions,
        similar_standards=parser.similar_standards,
    )


class _SearchPageParser(HTMLParser):
    """Collects all (standard_number, shop_href) pairs from a SNZ search results page."""

    def __init__(self) -> None:
        super().__init__()
        self.results: list[tuple[str, str]] = []
        self._in_item = False
        self._in_h5 = False
        self._in_link = False
        self._href = ""
        self._text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = (dict(attrs).get("class") or "").split()
        href = dict(attrs).get("href") or ""

        if tag == "li" and "search-result__list-item" in classes:
            self._in_item = True
        if self._in_item and tag == "h5":
            self._in_h5 = True
        if self._in_h5 and tag == "a" and "/shop/" in href:
            self._in_link = True
            self._href = href
            self._text = ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._in_link:
            self.results.append((self._text.strip(), self._href))
            self._in_link = False
        if tag == "h5":
            self._in_h5 = False
        if tag == "li":
            self._in_item = False

    def handle_data(self, data: str) -> None:
        if self._in_link:
            self._text += data


_DETAIL_APPEND_FIELDS: frozenset[str] = frozenset(
    {"abstract", "standard_number", "title"}
)
_DETAIL_ASSIGN_FIELDS: frozenset[str] = frozenset({"date_published", "status"})


class _DetailPageParser(HTMLParser):
    """Minimal state-machine HTML parser for SNZ standard detail pages."""

    def __init__(self) -> None:
        super().__init__()
        self.standard_number = ""
        self.title = ""
        self.status = ""
        self.date_published = ""
        self.abstract = ""
        self.pages: int | None = None
        self.previous_versions: list[str] = []
        self.similar_standards: list[str] = []

        self._capture: str | None = None  # which field is being captured
        self._in_prev_section = False
        self._in_similar_section = False
        self._link_is_shop = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = (dict(attrs).get("class") or "").split()
        href = dict(attrs).get("href") or ""

        if tag == "h1" and "product__standard-number" in classes:
            self._capture = "standard_number"
        elif tag == "h2" and "product__title" in classes:
            self._capture = "title"
        elif tag == "span" and any(c.startswith("product__state") for c in classes):
            self._capture = "status"
        elif tag == "time":
            self._capture = "date_published"
        elif tag == "p" and "product__abstract" in classes:
            self._capture = "abstract"
        elif tag == "span" and "product__pages__title" in classes:
            self._capture = "_pages_label"
        elif tag == "span" and self._capture == "_pages_label":
            self._capture = "_pages_value"
        elif tag == "a" and "/shop/" in href and not href.endswith(("#", "/subscribe")):
            self._link_is_shop = True
            self._capture = "_link"
        elif tag != "span":
            self._link_is_shop = False

    def handle_endtag(self, tag: str) -> None:
        if tag in {"h1", "h2", "span", "time", "p", "a"}:
            if self._capture in {
                "standard_number",
                "title",
                "status",
                "date_published",
                "abstract",
            }:
                self._capture = None
            elif self._capture == "_link":
                self._capture = None
                self._link_is_shop = False

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if not text:
            return

        if self._capture in _DETAIL_APPEND_FIELDS:
            setattr(self, self._capture, getattr(self, self._capture) + text)
        elif self._capture in _DETAIL_ASSIGN_FIELDS:
            setattr(self, self._capture, text)
        elif self._capture == "_pages_value":
            m = re.search(r"\d+", text)
            if m:
                self.pages = int(m.group())
            self._capture = None
        elif self._capture == "_link" and self._link_is_shop:
            if self._in_prev_section:
                self.previous_versions.append(text)
            elif self._in_similar_section:
                self.similar_standards.append(text)
        elif text == "Previous versions":
            self._in_prev_section = True
            self._in_similar_section = False
        elif text == "Similar Standards":
            self._in_similar_section = True
            self._in_prev_section = False
