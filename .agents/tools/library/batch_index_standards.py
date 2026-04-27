r"""Automated manifest-first indexer for Engineering standards PDFs.

Unlike the generic batch_index.py, this script derives metadata from the known
standards folder structure:
  - Each subdirectory is named after the issuing body (ASTM, NZS, ISO, etc.).
  - Filenames usually encode the standard code and sometimes the year.
  - PDF text extraction and OCR are optional enrichment, not default indexing.

Run from the repo root:
    .venv\Scripts\python.exe .agents\tools\library\batch_index_standards.py

Phases covered by this script: Phase 1 (batch index) only.
Run dedup_index.py separately after this completes (Phase 3).
"""

import os
import pathlib
import re
import sys
from datetime import date

import openpyxl

FOLDER = pathlib.Path(r"G:\My Drive\Library\Engineering\Standards")
DOMAIN_WS = "Standards"
TEXT_SIZE_LIMIT_MB = 50
BATCH_SIZE = 8
USE_TEXT_EXTRACTION = os.environ.get("LIBRARY_INDEX_EXTRACT_TEXT") == "1"
USE_OCR = os.environ.get("LIBRARY_INDEX_USE_OCR") == "1"

INDEX_PATH = pathlib.Path(r"G:\My Drive\Library\library-index.xlsx")
TODAY = date.today().isoformat()

ISSUER_MAP: dict[str, tuple[str, str]] = {
    "_archive": ("", ""),
    "AACE": ("AACE International", "International"),
    "AASHTO": ("AASHTO", "US"),
    "ACENZ": ("ACENZ", "NZ"),
    "ACI": ("ACI", "US"),
    "ANSI": ("ANSI", "US"),
    "API": ("API", "US"),
    "AS": ("Standards Australia", "AU"),
    "ASCE": ("ASCE", "US"),
    "ASME": ("ASME", "US"),
    "ASNZS": ("Standards Australia/SNZ", "AU/NZ"),
    "ASTM": ("ASTM International", "US"),
    "Austroads": ("Austroads", "AU"),
    "AWWA": ("AWWA", "US"),
    "BS": ("BSI", "UK"),
    "BSEN": ("BSI/CEN", "UK/EU"),
    "Christchurch": ("Christchurch City Council", "NZ"),
    "DIN": ("DIN", "DE"),
    "DVS": ("DVS", "DE"),
    "Eco Choice Aotearoa": ("Eco Choice Aotearoa", "NZ"),
    "GRI": ("GRI", "US"),
    "IEC": ("IEC", "International"),
    "IEEE": ("IEEE", "International"),
    "ISO": ("ISO", "International"),
    "JIS": ("JSA", "JP"),
    "NF": ("AFNOR", "FR"),
    "NFPA": ("NFPA", "US"),
    "NS": ("Standard Norge", "NO"),
    "NZ Drinking Water": ("Ministry of Health NZ", "NZ"),
    "NZS": ("SNZ", "NZ"),
    "NZTA": ("Waka Kotahi NZTA", "NZ"),
    "UNKNOWN": ("", ""),
    "VDI": ("VDI", "DE"),
}

SUBDOMAIN_MAP: dict[str, str] = {
    "GRI": "Geotechnical Engineering",
}

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from extract_text import (  # noqa: E402
    extract_text,
    make_ocr_reader,
    ocr_extract_text,
    sha256,
)
from workbook_utils import (  # noqa: E402
    LIBRARY_ROOT,
    WorkbookLock,
    append_index_row,
    get_indexed_paths,
    save_workbook_atomically,
)

_ILLEGAL_CHARS = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f"
    r"\x7f-\x84\x86-\x9f"
    r"\ud800-\udfff\ufffe\uffff]"
)


def index_standards() -> None:
    """Index one row per physical standards PDF using path-based resume."""
    with WorkbookLock(INDEX_PATH):
        workbook = openpyxl.load_workbook(INDEX_PATH)
        already_done = get_indexed_paths(workbook)
        ocr_reader = make_ocr_reader() if USE_OCR else None
        files = _get_source_files()
        print(f"Found {len(files)} PDFs. Already indexed: {len(already_done)} paths.")
        _index_batches(workbook, files, already_done, ocr_reader)

    print("\nPhase 1 complete.")
    print(
        "Next: run dedup_index.py (Phase 3), then review NEEDS_REVIEW rows (Phase 4)."
    )


def _get_source_files() -> list[pathlib.Path]:
    return sorted(
        [
            file_path
            for file_path in FOLDER.rglob("*.pdf")
            if file_path.name != "desktop.ini"
        ],
        key=lambda file_path: file_path.stat().st_size,
    )


def _index_batches(
    workbook: openpyxl.Workbook,
    files: list[pathlib.Path],
    already_done: set[str],
    ocr_reader: object | None,
) -> None:
    for batch_num, batch_start in enumerate(range(0, len(files), BATCH_SIZE), start=1):
        batch = files[batch_start : batch_start + BATCH_SIZE]
        print(
            f"\n=== Batch {batch_num} "
            f"({batch_start + 1}-{min(batch_start + BATCH_SIZE, len(files))} of {len(files)}) ==="
        )
        new_rows = _compose_batch_rows(batch, already_done, ocr_reader)
        for row in new_rows:
            append_index_row(workbook, DOMAIN_WS, row)
        save_workbook_atomically(workbook, INDEX_PATH)
        print(f"  -> Saved batch {batch_num} ({len(new_rows)} new rows).")


def _compose_batch_rows(
    batch: list[pathlib.Path],
    already_done: set[str],
    ocr_reader: object | None,
) -> list[list[object]]:
    new_rows: list[list[object]] = []
    for file_path in batch:
        relative_path = str(file_path.relative_to(LIBRARY_ROOT))
        if relative_path in already_done:
            print(f"  SKIP (already indexed): {file_path.name}")
            continue
        row = _compose_standard_row(file_path, relative_path, ocr_reader)
        new_rows.append(row)
        already_done.add(relative_path)
    return new_rows


def _compose_standard_row(
    file_path: pathlib.Path,
    relative_path: str,
    ocr_reader: object | None,
) -> list[object]:
    file_hash = sha256(file_path)
    size_mb = round(file_path.stat().st_size / 1_000_000, 2)
    print(f"  {file_path.name}  ({size_mb} MB)")

    parent_folder_name = file_path.parent.name
    issuing_body, jurisdiction = ISSUER_MAP.get(parent_folder_name, ("", ""))
    subdomain = SUBDOMAIN_MAP.get(parent_folder_name, "")
    status = _default_status(parent_folder_name)
    standard_code = _parse_standard_code(file_path.stem)
    year = _parse_year_from_stem(file_path.stem)
    text, notes_parts = _extract_metadata_text(file_path, size_mb, ocr_reader)
    title = _extract_title_from_text(text) or file_path.stem
    year = _year_from_text(text, year)
    _append_review_notes(
        notes_parts=notes_parts,
        subdomain=subdomain,
        status=status,
        issuing_body=issuing_body,
    )
    notes = "; ".join(notes_parts) if notes_parts else None
    print(
        f"    code={standard_code!r}  year={year}  issuer={issuing_body!r}  status={status!r}"
    )

    return [
        file_hash,
        _sanitize(title),
        _sanitize(issuing_body),
        _sanitize(issuing_body),
        year,
        None,
        "PDF",
        _sanitize(relative_path),
        _sanitize(file_path.name),
        "Engineering",
        _sanitize(subdomain),
        "Standard",
        "Standard",
        "",
        "",
        "",
        "practitioner",
        "",
        _sanitize(notes),
        TODAY,
        _sanitize(standard_code),
        _sanitize(status),
        _sanitize(jurisdiction),
        _sanitize(issuing_body),
        None,
    ]


def _extract_metadata_text(
    file_path: pathlib.Path,
    size_mb: float,
    ocr_reader: object | None,
) -> tuple[str, list[str]]:
    notes_parts: list[str] = []
    if not USE_TEXT_EXTRACTION:
        notes_parts.append(
            "NEEDS_REVIEW: text extraction skipped — verify title/year manually"
        )
        return "", notes_parts
    if size_mb > TEXT_SIZE_LIMIT_MB:
        notes_parts.append(
            f"NEEDS_REVIEW: large file ({size_mb} MB) — verify metadata manually"
        )
        return "", notes_parts

    text = extract_text(file_path)
    if not text and ocr_reader:
        print("    -> No digital text; trying OCR...")
        text = ocr_extract_text(file_path, ocr_reader)
    if not text:
        review_reason = "digital text extraction returned nothing"
        if USE_OCR:
            review_reason = "digital and OCR extraction both returned nothing"
        notes_parts.append(f"NEEDS_REVIEW: no extractable text — {review_reason}")
    return text, notes_parts


def _append_review_notes(
    *,
    notes_parts: list[str],
    subdomain: str,
    status: str,
    issuing_body: str,
) -> None:
    if not subdomain:
        notes_parts.append("NEEDS_REVIEW: subdomain not assigned — classify manually")
    if status == "needs_review":
        notes_parts.append(
            "NEEDS_REVIEW: status not confirmed — current/superseded/withdrawn/draft"
        )
    if not issuing_body:
        notes_parts.append("NEEDS_REVIEW: issuing body unknown")


def _year_from_text(text: str, year: int | None) -> int | None:
    if year is not None or not text:
        return year
    year_match = re.search(r"\b(19[5-9]\d|20[0-2]\d)\b", text[:2000])
    if year_match:
        return int(year_match.group(1))
    return None


def _sanitize(value: str | None) -> str | None:
    if value is None:
        return None
    return _ILLEGAL_CHARS.sub("", value).strip() or None


def _parse_year_from_stem(stem: str) -> int | None:
    matches = re.findall(r"\b(19[5-9]\d|20[0-2]\d)\b", stem)
    return int(matches[-1]) if matches else None


def _parse_standard_code(stem: str) -> str:
    code = re.sub(r"[-\s]*(19[5-9]\d|20[0-2]\d)$", "", stem).strip()
    return code or stem


def _extract_title_from_text(extracted_text: str) -> str | None:
    if not extracted_text:
        return None
    clean = _ILLEGAL_CHARS.sub("", extracted_text)
    for line in clean[:1000].splitlines():
        stripped_line = line.strip()
        if len(stripped_line) > 10:
            return stripped_line[:200]
    return None


def _default_status(folder_name: str) -> str:
    return "superseded" if folder_name == "_archive" else "needs_review"


if __name__ == "__main__":
    index_standards()
