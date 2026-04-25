"""Batch indexer — Phase 1 of the folder indexing workflow.

Usage
-----
1. Set the three constants in the CONFIG block below.
2. Run from the repo root:
       .venv\\Scripts\\python.exe .agents\\tools\\library\\batch_index.py

The script:
  - Sorts files by size ascending (small digital PDFs first; large scanned PDFs last).
  - Skips hashes already present in the Master worksheet (safe to re-run after interruption).
  - Tries pypdf digital extraction, then falls back to EasyOCR for scanned pages.
  - Skips text extraction entirely for files > TEXT_SIZE_LIMIT_MB (marks NEEDS_REVIEW).
  - Pauses at the <<< FILL IN METADATA >>> marker — build the row tuple there.
  - Saves after every batch of 8 files.
"""

import pathlib
import sys
from datetime import date

import openpyxl

# --- CONFIG: set these before running ---
FOLDER = pathlib.Path(r"G:\My Drive\Library\<subfolder>")
DOMAIN_WS = "<domain worksheet>"  # e.g. "Engineering" or "Management"
TEXT_SIZE_LIMIT_MB = 100
# ----------------------------------------

BATCH_SIZE = 8
INDEX_PATH = r"G:\My Drive\Library\library-index.xlsx"
TODAY = date.today().isoformat()

# Import helpers from the same tools/library/ directory
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from extract_text import (  # noqa: E402
    extract_text,
    make_ocr_reader,
    ocr_extract_text,
    sha256,
)

ocr_reader = make_ocr_reader()

wb = openpyxl.load_workbook(INDEX_PATH)
ws_master = wb["Master"]
ws_domain = wb[DOMAIN_WS]
already_done = {
    str(row[0].value).upper()
    for row in ws_master.iter_rows(min_row=2)
    if row[0].value
}

files = sorted(
    [f for f in FOLDER.rglob("*.pdf") if f.name != "desktop.ini"],
    key=lambda f: f.stat().st_size,
)
print(f"Found {len(files)} PDFs. Already indexed: {len(already_done)} hashes.")

batch_num = 0
for i in range(0, len(files), BATCH_SIZE):
    batch = files[i : i + BATCH_SIZE]
    batch_num += 1
    print(f"\n=== Batch {batch_num} ({i + 1}–{min(i + BATCH_SIZE, len(files))} of {len(files)}) ===")

    new_rows = []
    for f in batch:
        h = sha256(str(f))
        size_mb = round(f.stat().st_size / 1_000_000, 2)
        print(f"  {f.name}  ({size_mb} MB)  {h[:12]}...")

        if h in already_done:
            print("    -> SKIP (already indexed)")
            continue

        if size_mb > TEXT_SIZE_LIMIT_MB:
            text = ""
            notes = f"NEEDS_REVIEW: large file ({size_mb} MB), likely scanned — verify metadata manually"
        else:
            text = extract_text(f)
            if not text and ocr_reader:
                print("    -> No digital text; trying OCR...")
                text = ocr_extract_text(f, ocr_reader)
            notes = "NEEDS_REVIEW: no extractable text — digital and OCR both returned nothing" if not text else None

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
        # relative_path = str(f.relative_to(r"G:\My Drive\Library"))
        #
        # new_rows.append([
        #     h, title, author, publisher, year, edition, "PDF",
        #     relative_path, canonical_filename,
        #     domain, subdomain, category, document_type,
        #     topics, frameworks, market_context, audience,
        #     "", notes, TODAY,
        # ])

    for row in new_rows:
        ws_master.append(row)
        ws_domain.append(row)
    wb.save(INDEX_PATH)
    print(f"  -> Saved batch {batch_num}.")

print("\nPhase 1 complete. Proceed to Phase 2 (rename) then Phase 3 (dedup).")
