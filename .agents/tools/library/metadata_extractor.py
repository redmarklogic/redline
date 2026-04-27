"""Extract and enrich metadata for one library PDF."""

import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Literal, Self, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
    validate_call,
)
from pypdf import PdfReader
from pypdf.errors import PdfReadError

type ApiSource = Literal["google_books", "open_library"]
type ExtractionSource = Literal["pdf_text", "ocr", "none"]
type JsonObject = Mapping[str, object]
type HttpJsonGetter = Callable[[str], Mapping[str, object] | None]
type LibraryCategory = Literal["Book", "Standard", "Magazine", "Misc"]

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"
OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"
OPEN_LIBRARY_WORKS_URL = "https://openlibrary.org"
USER_AGENT = "RedlineLibraryIndexer/1.0"
DEFAULT_LIBRARY_ROOT = Path(r"G:\My Drive\Library")
VALIDATE_CONFIG = ConfigDict(arbitrary_types_allowed=True)


class MetadataExtractionRequest(BaseModel):
    """Validated input for extracting metadata from one PDF path."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    pdf_path: Path
    category_hint: LibraryCategory | None = None
    title_hint: str | None = None
    author_hint: str | None = None
    max_text_pages: int = Field(default=5, ge=1, le=20)
    max_ocr_pages: int = Field(default=3, ge=1, le=10)

    @field_validator("pdf_path")
    @classmethod
    def validate_pdf_path(cls, value: Path) -> Path:
        """Require an existing PDF path."""
        if value.suffix.lower() != ".pdf":
            message = "PDF metadata extraction requires a PDF path"
            raise ValueError(message)
        if not value.exists():
            message = f"PDF path does not exist: {value}"
            raise ValueError(message)
        return value


type TextReader = Callable[[MetadataExtractionRequest], str]
type OcrReadText = Callable[..., list[str]]


class ApiBookMetadata(BaseModel):
    """Book metadata returned by an external catalogue API."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    title: str
    subtitle: str | None = None
    authors: list[str] = Field(default_factory=list)
    publisher: str | None = None
    published_date: str | None = None
    published_year: int | None = Field(default=None, ge=1000, le=2100)
    description: str | None = None
    isbn_10: list[str] = Field(default_factory=list)
    isbn_13: list[str] = Field(default_factory=list)
    language: str | None = None
    page_count: int | None = Field(default=None, ge=1)
    categories: list[str] = Field(default_factory=list)
    subjects: list[str] = Field(default_factory=list)
    source_urls: list[str] = Field(default_factory=list)
    api_source: ApiSource

    @model_validator(mode="after")
    def require_title(self) -> Self:
        """Reject catalogue results without a usable title."""
        if not self.title.strip():
            message = "API metadata must include a title"
            raise ValueError(message)
        return self


class PdfTitlePageMetadata(BaseModel):
    """Metadata inferred from PDF title-page text or OCR text."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    title: str | None = None
    authors: list[str] = Field(default_factory=list)
    publisher: str | None = None
    published_year: int | None = Field(default=None, ge=1000, le=2100)
    document_type: str | None = None
    topics: list[str] = Field(default_factory=list)
    raw_text: str = ""
    extraction_source: ExtractionSource = "none"


class BookMetadata(BaseModel):
    """Combined filesystem, PDF, OCR, and catalogue metadata for one PDF."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    pdf_path: Path
    relative_path: str
    file_name: str
    sha256: str = Field(min_length=64, max_length=64)
    category: LibraryCategory
    title: str | None = None
    subtitle: str | None = None
    authors: list[str] = Field(default_factory=list)
    publisher: str | None = None
    published_date: str | None = None
    published_year: int | None = Field(default=None, ge=1000, le=2100)
    description: str | None = None
    isbn_10: list[str] = Field(default_factory=list)
    isbn_13: list[str] = Field(default_factory=list)
    language: str | None = None
    page_count: int | None = Field(default=None, ge=1)
    categories: list[str] = Field(default_factory=list)
    subjects: list[str] = Field(default_factory=list)
    document_type: str | None = None
    topics: list[str] = Field(default_factory=list)
    market_context: list[str] = Field(default_factory=list)
    source_urls: list[str] = Field(default_factory=list)
    extraction_source: ExtractionSource = "none"
    api_source: ApiSource | None = None
    text_sample: str | None = None


class BookMetadataExtractor:
    """Extract title-page metadata and enrich it with book catalogue APIs."""

    def __init__(
        self,
        *,
        http_get_json: HttpJsonGetter | None = None,
        text_reader: TextReader | None = None,
        ocr_text_reader: TextReader | None = None,
        library_root: Path = DEFAULT_LIBRARY_ROOT,
    ) -> None:
        """Initialize the extractor with optional testable boundaries.

        Args:
            http_get_json: Optional HTTP JSON reader for catalogue lookups.
            text_reader: Optional digital PDF text reader.
            ocr_text_reader: Optional OCR text reader for scanned PDFs.
            library_root: Root folder used to compute relative library paths.
        """
        self._http_get_json = http_get_json or _get_json
        self._text_reader = text_reader or read_pdf_text
        self._ocr_text_reader = ocr_text_reader or self._read_ocr_text
        self._library_root = Path(library_root)
        self._ocr_readtext: OcrReadText | None = None

    @validate_call(config=VALIDATE_CONFIG)
    def extract_metadata(self, request: MetadataExtractionRequest) -> BookMetadata:
        """Return combined metadata for the PDF in the request.

        Args:
            request: Validated PDF metadata extraction request.

        Returns:
            Combined metadata for the PDF and any matching catalogue result.
        """
        pdf_metadata = self.extract_from_text_pdf(request)
        if pdf_metadata.extraction_source == "none":
            pdf_metadata = self.extract_from_scan(request)

        title = request.title_hint or pdf_metadata.title
        author = request.author_hint or _first_or_none(pdf_metadata.authors)
        api_metadata = self.fetch_by_title(title, author=author) if title else None
        category = request.category_hint or self.classify_document(request.pdf_path)
        return self._compose_book_metadata(
            request=request,
            pdf_metadata=pdf_metadata,
            api_metadata=api_metadata,
            category=category,
        )

    @validate_call(config=VALIDATE_CONFIG)
    def extract_from_text_pdf(
        self, request: MetadataExtractionRequest
    ) -> PdfTitlePageMetadata:
        """Extract metadata from digital PDF text.

        Args:
            request: Validated PDF metadata extraction request.

        Returns:
            Metadata parsed from digital text, or an empty result if no text exists.
        """
        text = self._text_reader(request).strip()
        if not text:
            return PdfTitlePageMetadata()
        return _parse_title_page_text(text, extraction_source="pdf_text")

    @validate_call(config=VALIDATE_CONFIG)
    def extract_from_scan(
        self, request: MetadataExtractionRequest
    ) -> PdfTitlePageMetadata:
        """Extract metadata from OCR text for scanned PDFs.

        Args:
            request: Validated PDF metadata extraction request.

        Returns:
            Metadata parsed from OCR text, or an empty result if OCR finds no text.
        """
        text = self._ocr_text_reader(request).strip()
        if not text:
            return PdfTitlePageMetadata()
        return _parse_title_page_text(text, extraction_source="ocr")

    @validate_call(config=VALIDATE_CONFIG)
    def fetch_by_title(
        self, title: str, *, author: str | None = None
    ) -> ApiBookMetadata | None:
        """Fetch book metadata from Google Books, then Open Library.

        Args:
            title: Title or title hint to search for.
            author: Optional author hint used to improve matching.

        Returns:
            API metadata from the best matching source, or None when both APIs miss.
        """
        search_title = clean_title_for_search(title)
        if not search_title:
            return None
        google_match = self._fetch_google_books(search_title, author=author)
        if google_match is not None:
            return google_match
        return self._fetch_open_library(search_title, author=author)

    @validate_call(config=VALIDATE_CONFIG)
    def classify_document(self, path: Path) -> LibraryCategory:
        """Classify a library path as Book, Standard, Magazine, or Misc.

        Args:
            path: PDF path or relative library path.

        Returns:
            The inferred library category.
        """
        normalized_parts = {part.casefold() for part in path.parts}
        if normalized_parts & {"standard", "standards"}:
            return "Standard"
        if normalized_parts & {"magazine", "magazines"}:
            return "Magazine"
        if normalized_parts & {"book", "books", "ebook", "ebooks", "textbooks"}:
            return "Book"
        return "Misc"

    def _compose_book_metadata(
        self,
        *,
        request: MetadataExtractionRequest,
        pdf_metadata: PdfTitlePageMetadata,
        api_metadata: ApiBookMetadata | None,
        category: LibraryCategory,
    ) -> BookMetadata:
        title = _first_available(
            api_metadata.title if api_metadata else None,
            request.title_hint,
            pdf_metadata.title,
            request.pdf_path.stem,
        )
        categories = api_metadata.categories if api_metadata else []
        subjects = api_metadata.subjects if api_metadata else []
        topics = _unique_strings([*categories, *subjects, *pdf_metadata.topics])
        values = {
            "pdf_path": request.pdf_path,
            "relative_path": self._relative_path(request.pdf_path),
            "file_name": request.pdf_path.name,
            "sha256": _sha256(request.pdf_path),
            "category": category,
            "title": title,
            "authors": _choose_list(
                api_metadata.authors if api_metadata else [], pdf_metadata.authors
            ),
            "publisher": _first_available(
                api_metadata.publisher if api_metadata else None, pdf_metadata.publisher
            ),
            "published_year": _first_available_int(
                api_metadata.published_year if api_metadata else None,
                pdf_metadata.published_year,
            ),
            "categories": categories,
            "subjects": subjects,
            "document_type": pdf_metadata.document_type
            or _infer_document_type(topics, ""),
            "topics": topics,
            "market_context": _infer_market_context(topics),
            "extraction_source": pdf_metadata.extraction_source,
            "text_sample": pdf_metadata.raw_text[:1000]
            if pdf_metadata.raw_text
            else None,
        }
        values.update(_api_book_fields(api_metadata))
        return BookMetadata.model_validate(values)

    def _relative_path(self, pdf_path: Path) -> str:
        try:
            return pdf_path.relative_to(self._library_root).as_posix()
        except ValueError:
            return pdf_path.as_posix()

    def _fetch_google_books(
        self, title: str, *, author: str | None
    ) -> ApiBookMetadata | None:
        query = f"intitle:{title}"
        if author:
            query = f"{query} inauthor:{author}"
        params = urllib.parse.urlencode({"q": query, "maxResults": "5"})
        payload = self._http_get_json(f"{GOOGLE_BOOKS_URL}?{params}")
        if not payload or (_optional_int(payload.get("totalItems")) or 0) == 0:
            return None
        for item in _as_mappings(payload.get("items")):
            info = _as_mapping(item.get("volumeInfo"))
            candidate_title = str(info.get("title") or "")
            if _titles_match(title, candidate_title):
                return _google_books_metadata(info)
        first_item = _first_or_none(_as_mappings(payload.get("items")))
        if first_item is None:
            return None
        return _google_books_metadata(_as_mapping(first_item.get("volumeInfo")))

    def _fetch_open_library(
        self, title: str, *, author: str | None
    ) -> ApiBookMetadata | None:
        params = {"title": title, "limit": "5"}
        if author:
            params["author"] = author
        payload = self._http_get_json(
            f"{OPEN_LIBRARY_URL}?{urllib.parse.urlencode(params)}"
        )
        if not payload or (_optional_int(payload.get("numFound")) or 0) == 0:
            return None
        for doc in _as_mappings(payload.get("docs")):
            candidate_title = str(doc.get("title") or "")
            if _titles_match(title, candidate_title):
                return _open_library_metadata(doc)
        first_doc = _first_or_none(_as_mappings(payload.get("docs")))
        return _open_library_metadata(first_doc) if first_doc else None

    def _read_ocr_text(self, request: MetadataExtractionRequest) -> str:
        try:
            import easyocr
            import numpy as np
            import pypdfium2 as pdfium
        except ImportError:
            return ""

        if self._ocr_readtext is None:
            self._ocr_readtext = cast(
                OcrReadText, easyocr.Reader(["en"], verbose=False).readtext
            )
        pdf = pdfium.PdfDocument(str(request.pdf_path))
        for page_index in range(min(request.max_ocr_pages, len(pdf))):
            bitmap = pdf[page_index].render(scale=2)
            text_data = self._ocr_readtext(
                np.array(bitmap.to_pil()),
                detail=0,
            )
            text = "\n".join(text_data)
            if text.strip():
                return text[:5000]
        return ""


@validate_call(config=VALIDATE_CONFIG)
def clean_title_for_search(raw_title: str) -> str:
    """Strip edition and file-name noise from a title for catalogue search.

    Args:
        raw_title: Raw title, stem, or title hint.

    Returns:
        A normalized title suitable for API search.
    """
    title = re.sub(r"\(\d{4}\)$", "", raw_title).strip()
    title = re.sub(r"\b\d+(st|nd|rd|th)\s+[Ee]dition\b", "", title)
    title = re.sub(r"\bEdition\b", "", title, flags=re.IGNORECASE)
    title = re.sub(r"\s*[-_]\s*", " ", title)
    return re.sub(r"\s+", " ", title).strip()


@validate_call(config=VALIDATE_CONFIG)
def read_pdf_text(request: MetadataExtractionRequest) -> str:
    """Read digital text from the first pages of a PDF.

    Args:
        request: Validated PDF metadata extraction request.

    Returns:
        Concatenated text from the first pages, truncated for metadata parsing.
    """
    try:
        with request.pdf_path.open("rb") as pdf_file:
            reader = PdfReader(pdf_file)
            pages = reader.pages[: request.max_text_pages]
            text = "\n".join(page.extract_text() or "" for page in pages)
    except (OSError, PdfReadError, KeyError, TypeError):
        return ""
    return text[:5000]


def _parse_title_page_text(
    text: str, *, extraction_source: ExtractionSource
) -> PdfTitlePageMetadata:
    lines = _clean_lines(text)
    title = _extract_title(lines)
    authors = _extract_authors(lines)
    publisher = _extract_publisher(text)
    year = _extract_year(text)
    topics = _infer_topics(text, title or "")
    return PdfTitlePageMetadata(
        title=title,
        authors=authors,
        publisher=publisher,
        published_year=year,
        document_type=_infer_document_type(topics, text),
        topics=topics,
        raw_text=text[:5000],
        extraction_source=extraction_source,
    )


def _get_json(url: str) -> JsonObject | None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    return cast(JsonObject, payload) if isinstance(payload, Mapping) else None


def _google_books_metadata(info: JsonObject) -> ApiBookMetadata:
    identifiers = _as_mappings(info.get("industryIdentifiers"))
    categories = _as_strings(info.get("categories"))
    source_urls = _unique_strings(
        [
            str(info.get("canonicalVolumeLink") or ""),
            str(info.get("infoLink") or ""),
        ]
    )
    return ApiBookMetadata(
        title=str(info.get("title") or ""),
        subtitle=_optional_string(info.get("subtitle")),
        authors=_as_strings(info.get("authors")),
        publisher=_optional_string(info.get("publisher")),
        published_date=_optional_string(info.get("publishedDate")),
        published_year=_extract_year(str(info.get("publishedDate") or "")),
        description=_optional_string(info.get("description")),
        isbn_10=_isbn_values(identifiers, "ISBN_10"),
        isbn_13=_isbn_values(identifiers, "ISBN_13"),
        language=_optional_string(info.get("language")),
        page_count=_optional_int(info.get("pageCount")),
        categories=categories,
        subjects=[],
        source_urls=source_urls,
        api_source="google_books",
    )


def _open_library_metadata(doc: JsonObject) -> ApiBookMetadata:
    isbn_values = _as_strings(doc.get("isbn"))
    key = _optional_string(doc.get("key"))
    return ApiBookMetadata(
        title=str(doc.get("title") or ""),
        authors=_as_strings(doc.get("author_name")),
        publisher=_first_or_none(_as_strings(doc.get("publisher"))),
        published_year=_optional_int(doc.get("first_publish_year")),
        isbn_10=[value for value in isbn_values if len(value) == 10],
        isbn_13=[value for value in isbn_values if len(value) == 13],
        language=_first_or_none(_as_strings(doc.get("language"))),
        page_count=_optional_int(doc.get("number_of_pages_median")),
        subjects=_as_strings(doc.get("subject"))[:12],
        source_urls=[f"{OPEN_LIBRARY_WORKS_URL}{key}"] if key else [],
        api_source="open_library",
    )


def _api_book_fields(api_metadata: ApiBookMetadata | None) -> dict[str, object]:
    if api_metadata is None:
        return {
            "subtitle": None,
            "published_date": None,
            "description": None,
            "isbn_10": [],
            "isbn_13": [],
            "language": None,
            "page_count": None,
            "source_urls": [],
            "api_source": None,
        }
    return {
        "subtitle": api_metadata.subtitle,
        "published_date": api_metadata.published_date,
        "description": api_metadata.description,
        "isbn_10": api_metadata.isbn_10,
        "isbn_13": api_metadata.isbn_13,
        "language": api_metadata.language,
        "page_count": api_metadata.page_count,
        "source_urls": api_metadata.source_urls,
        "api_source": api_metadata.api_source,
    }


def _clean_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def _extract_title(lines: list[str]) -> str | None:
    for line in lines:
        lower_line = line.casefold()
        if lower_line.startswith(("by ", "copyright", "published by")):
            continue
        if lower_line == "edition" or lower_line.endswith(" edition"):
            continue
        if len(line) >= 4:
            return line[:200]
    return None


def _extract_authors(lines: list[str]) -> list[str]:
    for line in lines[:12]:
        match = re.match(
            r"(?:by|authors?|edited by|written by)[:\s]+(.+)", line, re.IGNORECASE
        )
        if match:
            return _split_author_names(match.group(1))
    return []


def _extract_publisher(text: str) -> str | None:
    patterns = [
        r"(?:published\s+by|publisher[:\s])\s*(.+?)(?:\n|$)",
        r"(?:©|copyright)\s+\d{4}\s+(.+?)(?:\n|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            publisher = match.group(1).strip().rstrip(".,;:")
            if 3 <= len(publisher) <= 120:
                return publisher
    return None


def _extract_year(text: str) -> int | None:
    match = re.search(r"\b(19\d\d|20[0-4]\d)\b", text)
    return int(match.group(1)) if match else None


def _infer_document_type(topics: list[str], text: str) -> str:
    combined = " ".join([*topics, text[:1000]]).casefold()
    if any(word in combined for word in ["handbook", "manual"]):
        return "Reference Manual"
    if any(word in combined for word in ["textbook", "course", "learning objectives"]):
        return "Textbook"
    if "case stud" in combined:
        return "Case Studies"
    return "Practical Guide"


def _infer_topics(text: str, title: str) -> list[str]:
    combined = f"{title} {text[:1500]}".casefold()
    keyword_map = {
        "bearing capacity": "Bearing Capacity",
        "foundation": "Foundation Engineering",
        "geotechnical": "Geotechnical Engineering",
        "groundwater": "Groundwater",
        "pile": "Pile Foundations",
        "retaining wall": "Retaining Walls",
        "settlement": "Settlement Analysis",
        "site investigation": "Site Investigation",
        "soil mechanic": "Soil Mechanics",
    }
    return [topic for keyword, topic in keyword_map.items() if keyword in combined]


def _infer_market_context(topics: list[str]) -> list[str]:
    combined = " ".join(topics).casefold()
    contexts = []
    if any(word in combined for word in ["geotechnical", "soil", "foundation"]):
        contexts.append("Geotechnical Engineering")
    if any(word in combined for word in ["civil", "retaining", "settlement"]):
        contexts.append("Civil Engineering")
    return contexts


def _split_author_names(raw_authors: str) -> list[str]:
    cleaned = raw_authors.replace(" & ", " and ")
    parts = re.split(r"\s*(?:,|\band\b)\s*", cleaned)
    return [part.strip() for part in parts if part.strip()]


def _titles_match(query: str, candidate: str) -> bool:
    query_words = set(re.findall(r"\w+", query.casefold()))
    candidate_words = set(re.findall(r"\w+", candidate.casefold()))
    if not query_words:
        return False
    return len(query_words & candidate_words) / len(query_words) >= 0.6


def _isbn_values(identifiers: list[JsonObject], isbn_type: str) -> list[str]:
    return [
        str(identifier.get("identifier"))
        for identifier in identifiers
        if identifier.get("type") == isbn_type and identifier.get("identifier")
    ]


def _as_mappings(value: object) -> list[JsonObject]:
    if not isinstance(value, list):
        return []
    return [cast(JsonObject, item) for item in value if isinstance(item, Mapping)]


def _as_mapping(value: object) -> JsonObject:
    return cast(JsonObject, value) if isinstance(value, Mapping) else {}


def _as_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def _choose_list(preferred: list[str], fallback: list[str]) -> list[str]:
    return preferred or fallback


def _first_available(*values: str | None) -> str | None:
    for value in values:
        if value:
            return value
    return None


def _first_available_int(*values: int | None) -> int | None:
    for value in values:
        if value is not None:
            return value
    return None


def _first_or_none[T](items: list[T]) -> T | None:
    return items[0] if items else None


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if not isinstance(value, str):
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _unique_strings(values: list[str]) -> list[str]:
    seen = set()
    unique = []
    for value in values:
        cleaned = value.strip()
        if cleaned and cleaned.casefold() not in seen:
            seen.add(cleaned.casefold())
            unique.append(cleaned)
    return unique


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest().upper()
