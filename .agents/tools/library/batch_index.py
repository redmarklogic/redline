r"""Batch indexer — Phase 1 of the folder indexing workflow.

Usage
-----
1. Set the constants in the CONFIG block below.
2. Run from the repo root:
       .venv\Scripts\python.exe .agents\tools\library\batch_index.py

The script:
  - Sorts files by size ascending (small digital PDFs first; large scanned PDFs last).
  - Skips paths already present in the Master worksheet (safe to re-run after interruption).
  - Tries pypdf digital extraction, then falls back to EasyOCR for scanned pages.
  - Skips text extraction entirely for files > TEXT_SIZE_LIMIT_MB (marks NEEDS_REVIEW).
  - Pauses at the <<< FILL IN METADATA >>> marker — build the row tuple there.
  - Saves through a temporary workbook after every batch of 8 files.
"""

import pathlib
import sys
from datetime import date

import openpyxl

FOLDER = pathlib.Path(r"G:\My Drive\Library\<subfolder>")
DOMAIN_WS = "<domain worksheet>"
TEXT_SIZE_LIMIT_MB = 100

BATCH_SIZE = 8
INDEX_PATH = pathlib.Path(r"G:\My Drive\Library\library-index.xlsx")
TODAY = date.today().isoformat()

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


def index_folder() -> None:
    """Index one row per physical file in the configured folder."""
    with WorkbookLock(INDEX_PATH):
        workbook = openpyxl.load_workbook(INDEX_PATH)
        already_done = get_indexed_paths(workbook)
        ocr_reader = make_ocr_reader()
        files = _get_source_files()
        print(f"Found {len(files)} PDFs. Already indexed: {len(already_done)} paths.")
        _index_batches(workbook, files, already_done, ocr_reader)

    print("\nPhase 1 complete. Proceed to Phase 2 (rename) then Phase 3 (dedup).")


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
        already_done.update(str(row[7]) for row in new_rows if row[7])
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

        file_hash = sha256(file_path)
        size_mb = round(file_path.stat().st_size / 1_000_000, 2)
        print(f"  {file_path.name}  ({size_mb} MB)  {file_hash[:12]}...")
        text, _notes = _extract_review_text(file_path, size_mb, ocr_reader)
        print(f"    TEXT SNIPPET: {text[:300] if text else '(none)'}")

        # <<< FILL IN METADATA from text snippet above, then build the row >>>
        # title = "..."
        # author = "..."
        # publisher = "..."
        # year = None
        # edition = None
        # canonical_filename = "..."
        # domain = "Engineering"
        # subdomain = "Geotechnical Engineering"
        # category = "Book"
        # document_type = "Textbook"
        # topics = ""
        # frameworks = ""
        # market_context = ""
        # audience = "practitioner"
        #
        # new_rows.append([
        #     file_hash, title, author, publisher, year, edition, "PDF",
        #     relative_path, canonical_filename,
        #     domain, subdomain, category, document_type,
        #     topics, frameworks, market_context, audience,
        #     "", notes, TODAY,
        # ])
    return new_rows


def _extract_review_text(
    file_path: pathlib.Path,
    size_mb: float,
    ocr_reader: object | None,
) -> tuple[str, str | None]:
    if size_mb > TEXT_SIZE_LIMIT_MB:
        return (
            "",
            f"NEEDS_REVIEW: large file ({size_mb} MB), likely scanned — verify metadata manually",
        )
    text = extract_text(file_path)
    if not text and ocr_reader:
        print("    -> No digital text; trying OCR...")
        text = ocr_extract_text(file_path, ocr_reader)
    if not text:
        return (
            "",
            "NEEDS_REVIEW: no extractable text — digital and OCR both returned nothing",
        )
    return text, None


if __name__ == "__main__":
    index_folder()
