"""PDF text extraction helpers for the library indexing workflow.

Importable module — used by batch_index.py and add_single_book.py.

Functions
---------
sha256(path)
    Compute SHA-256 hex digest of a file.
extract_text(path, max_pages=5)
    Extract digital text from a PDF via pypdf.
make_ocr_reader()
    Initialize an EasyOCR reader (models auto-download ~30 s on first run).
ocr_extract_text(path, ocr_reader, max_pages=3)
    Extract text from a scanned PDF page-by-page via EasyOCR.
"""

import hashlib
import pathlib

import pypdf


def sha256(path: str | pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def extract_text(path: str | pathlib.Path, max_pages: int = 5) -> str:
    """Return up to 2000 chars of digital text from the first non-empty page."""
    try:
        reader = pypdf.PdfReader(str(path))
        for i in range(min(max_pages, len(reader.pages))):
            text = reader.pages[i].extract_text()
            if text and text.strip():
                return text[:2000]
    except Exception as e:
        return f"ERROR: {e}"
    return ""


def make_ocr_reader():
    """Initialize EasyOCR reader (English). Returns None if easyocr is not installed."""
    try:
        import easyocr
        reader = easyocr.Reader(["en"], verbose=False)
        print("EasyOCR ready.")
        return reader
    except ImportError:
        print("easyocr not installed — scanned PDFs will be marked NEEDS_REVIEW")
        return None


def ocr_extract_text(path: str | pathlib.Path, ocr_reader, max_pages: int = 3) -> str:
    """OCR-extract text from a scanned PDF. Stops on first page that yields text."""
    try:
        import numpy as np
        import pypdfium2 as pdfium

        pdf = pdfium.PdfDocument(str(path))
        for i in range(min(max_pages, len(pdf))):
            bitmap = pdf[i].render(scale=2)
            text_data = ocr_reader.readtext(np.array(bitmap.to_pil()), detail=0)
            text = "\n".join(text_data)
            if text.strip():
                return text[:2000]
    except Exception as e:
        return f"ERROR: {e}"
    return ""
