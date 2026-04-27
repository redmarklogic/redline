"""Tests for library PDF metadata extraction."""

import importlib.util
from collections.abc import Mapping
from pathlib import Path
from types import ModuleType

import pytest
from pydantic import ValidationError
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

JsonPayload = Mapping[str, object]


def load_library_tool(tools_dir: Path, module_name: str) -> ModuleType:
    """Load a library tool module from the tools directory."""
    module_path = tools_dir / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        message = f"Could not load tool module: {module_name}"
        raise RuntimeError(message)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(name="metadata_extractor")
def metadata_extractor_fixture(tools_dir: Path) -> ModuleType:
    """Return the metadata extractor module."""
    return load_library_tool(tools_dir, "metadata_extractor")


@pytest.fixture(name="synthetic_text_pdf")
def synthetic_text_pdf_fixture(tmp_path: Path, pdf_assets_dir: Path) -> Path:
    """Create a synthetic text PDF from a test title-page extract."""
    text = (pdf_assets_dir / "synthetic_geotechnical_handbook_extract.txt").read_text(
        encoding="utf-8"
    )
    pdf_path = tmp_path / "Engineering" / "Ebooks" / "geotechnical-handbook.pdf"
    pdf_path.parent.mkdir(parents=True)
    _write_text_pdf(pdf_path, text)
    return pdf_path


def test_metadata_extraction_request_rejects_non_pdf_paths(
    tmp_path: Path, metadata_extractor: ModuleType
) -> None:
    text_path = tmp_path / "book.txt"
    text_path.write_text("not a PDF", encoding="utf-8")

    with pytest.raises(ValidationError, match="PDF"):
        metadata_extractor.MetadataExtractionRequest(pdf_path=text_path)


def test_classify_document_uses_library_path_segments(
    metadata_extractor: ModuleType,
) -> None:
    extractor = metadata_extractor.BookMetadataExtractor()

    assert (
        extractor.classify_document(Path("Engineering/Standards/BS-5930.pdf"))
        == "Standard"
    )
    assert (
        extractor.classify_document(Path("Engineering/Magazines/ge-2026.pdf"))
        == "Magazine"
    )
    assert (
        extractor.classify_document(Path("Engineering/Ebooks/soil-mechanics.pdf"))
        == "Book"
    )
    assert extractor.classify_document(Path("Unsorted/file.pdf")) == "Misc"


def test_fetch_by_title_returns_google_books_metadata(
    metadata_extractor: ModuleType,
) -> None:
    extractor = metadata_extractor.BookMetadataExtractor(
        http_get_json=_fake_google_books_response
    )

    result = extractor.fetch_by_title("Geotechnical Engineering Handbook")

    assert result is not None
    assert result.title == "Geotechnical Engineering Handbook"
    assert result.subtitle == "Second Edition"
    assert result.authors == ["Robert Day"]
    assert result.publisher == "Redline Test Press"
    assert result.published_year == 2020
    assert result.isbn_13 == ["9781234567890"]
    assert result.api_source == "google_books"
    assert result.source_urls == ["https://books.google.example/handbook"]


def test_fetch_by_title_falls_back_to_open_library(
    metadata_extractor: ModuleType,
) -> None:
    extractor = metadata_extractor.BookMetadataExtractor(
        http_get_json=_fake_open_library_response
    )

    result = extractor.fetch_by_title("Foundation Design Field Manual")

    assert result is not None
    assert result.title == "Foundation Design Field Manual"
    assert result.authors == ["Alice Morgan", "Ben Stone"]
    assert result.publisher == "FieldWorks Publishing"
    assert result.published_year == 2018
    assert result.isbn_10 == ["1234567890"]
    assert result.api_source == "open_library"
    assert result.source_urls == ["https://openlibrary.org/works/OL123W"]


def test_extract_metadata_reads_text_pdf_and_combines_api_metadata(
    metadata_extractor: ModuleType,
    synthetic_text_pdf: Path,
    tmp_path: Path,
) -> None:
    request = metadata_extractor.MetadataExtractionRequest(pdf_path=synthetic_text_pdf)
    extractor = metadata_extractor.BookMetadataExtractor(
        http_get_json=_fake_google_books_response,
        library_root=tmp_path,
    )

    result = extractor.extract_metadata(request)

    assert result.pdf_path == synthetic_text_pdf
    assert result.relative_path == "Engineering/Ebooks/geotechnical-handbook.pdf"
    assert result.file_name == "geotechnical-handbook.pdf"
    assert result.category == "Book"
    assert result.title == "Geotechnical Engineering Handbook"
    assert result.authors == ["Robert Day"]
    assert result.publisher == "Redline Test Press"
    assert result.published_year == 2020
    assert result.isbn_13 == ["9781234567890"]
    assert result.extraction_source == "pdf_text"
    assert result.api_source == "google_books"
    assert len(result.sha256) == 64


def test_extract_metadata_uses_ocr_when_digital_text_is_empty(
    metadata_extractor: ModuleType,
    pdf_assets_dir: Path,
) -> None:
    scan_path = pdf_assets_dir / "synthetic_blank_scan.pdf"
    scan_text = (
        pdf_assets_dir / "synthetic_scanned_foundations_extract.txt"
    ).read_text(encoding="utf-8")
    request = metadata_extractor.MetadataExtractionRequest(
        pdf_path=scan_path,
        category_hint="Book",
    )
    extractor = metadata_extractor.BookMetadataExtractor(
        http_get_json=_fake_open_library_response,
        text_reader=lambda _request: "",
        ocr_text_reader=lambda _request: scan_text,
        library_root=pdf_assets_dir,
    )

    result = extractor.extract_metadata(request)

    assert result.category == "Book"
    assert result.title == "Foundation Design Field Manual"
    assert result.authors == ["Alice Morgan", "Ben Stone"]
    assert result.extraction_source == "ocr"
    assert result.api_source == "open_library"


def _fake_google_books_response(url: str) -> JsonPayload | None:
    if "googleapis" not in url:
        message = f"Unexpected URL: {url}"
        raise AssertionError(message)
    return {
        "totalItems": 1,
        "items": [
            {
                "volumeInfo": {
                    "title": "Geotechnical Engineering Handbook",
                    "subtitle": "Second Edition",
                    "authors": ["Robert Day"],
                    "publisher": "Redline Test Press",
                    "publishedDate": "2020-03-15",
                    "description": "A practical guide for geotechnical engineering.",
                    "industryIdentifiers": [
                        {"type": "ISBN_13", "identifier": "9781234567890"},
                    ],
                    "pageCount": 512,
                    "categories": ["Technology & Engineering / Civil"],
                    "language": "en",
                    "canonicalVolumeLink": "https://books.google.example/handbook",
                }
            }
        ],
    }


def _fake_open_library_response(url: str) -> JsonPayload | None:
    if "googleapis" in url:
        return {"totalItems": 0, "items": []}
    if "openlibrary" not in url:
        message = f"Unexpected URL: {url}"
        raise AssertionError(message)
    return {
        "numFound": 1,
        "docs": [
            {
                "title": "Foundation Design Field Manual",
                "author_name": ["Alice Morgan", "Ben Stone"],
                "publisher": ["FieldWorks Publishing"],
                "first_publish_year": 2018,
                "isbn": ["1234567890"],
                "language": ["eng"],
                "number_of_pages_median": 240,
                "subject": ["Foundation engineering", "Soil mechanics"],
                "key": "/works/OL123W",
            }
        ],
    }


def _write_text_pdf(path: Path, text: str) -> None:
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    stream = DecodedStreamObject()
    stream.set_data(_compose_pdf_text_stream(text))
    page[NameObject("/Contents")] = stream
    page[NameObject("/Resources")] = _compose_pdf_resources()
    with path.open("wb") as pdf_file:
        writer.write(pdf_file)
    with path.open("rb") as pdf_file:
        page = PdfReader(pdf_file).pages[0]
        extracted_text = getattr(page, "extract_text")()
        assert extracted_text.strip()


def _compose_pdf_text_stream(text: str) -> bytes:
    escaped_lines = [
        _escape_pdf_text(line) for line in text.splitlines() if line.strip()
    ]
    operations = ["BT", "/F1 14 Tf", "72 720 Td"]
    for index, line in enumerate(escaped_lines):
        if index > 0:
            operations.append("0 -24 Td")
        operations.append(f"({line}) Tj")
    operations.append("ET")
    return "\n".join(operations).encode("utf-8")


def _compose_pdf_resources() -> DictionaryObject:
    font = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        }
    )
    return DictionaryObject(
        {NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})}
    )


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
