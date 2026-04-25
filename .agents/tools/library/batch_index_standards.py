"""Automated batch indexer for G:\\My Drive\\Library\\Engineering\\Standards.

Unlike the generic batch_index.py (which requires interactive metadata entry),
this script auto-populates metadata by leveraging the known folder structure:
  - Each subdirectory is named after the issuing body (ASTM, NZS, ISO, etc.)
  - Filenames already encode the standard code
  - PDF text is extracted to recover title and year

Run from the repo root:
    .venv\\Scripts\\python.exe .agents\\tools\\library\\batch_index_standards.py

Phases covered by this script: Phase 1 (batch index) only.
Run dedup_index.py separately after this completes (Phase 3).
"""

import pathlib
import re
import sys
from datetime import date

import openpyxl

# --- CONFIG ---
FOLDER = pathlib.Path(r"G:\My Drive\Library\Engineering\Standards")
DOMAIN_WS = "Standards"
TEXT_SIZE_LIMIT_MB = 50
BATCH_SIZE = 8
# --------------

INDEX_PATH = r"G:\My Drive\Library\library-index.xlsx"
TODAY = date.today().isoformat()

# Issuing body → (canonical issuing_body_name, jurisdiction)
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

# GRI standards are geotechnical (Geosynthetics Research Institute)
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

# openpyxl's full set of illegal characters (matches openpyxl.cell.cell)
_ILLEGAL_CHARS = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f"
    r"\x7f-\x84\x86-\x9f"
    r"\ud800-\udfff\ufffe\uffff]"
)


def _sanitize(value: str | None) -> str | None:
    if value is None:
        return None
    return _ILLEGAL_CHARS.sub("", value).strip() or None


ocr_reader = make_ocr_reader()

wb = openpyxl.load_workbook(INDEX_PATH)
ws_master = wb["Master"]
ws_domain = wb[DOMAIN_WS]

already_done = {
    str(row[0].value).upper() for row in ws_master.iter_rows(min_row=2) if row[0].value
}

files = sorted(
    [f for f in FOLDER.rglob("*.pdf") if f.name != "desktop.ini"],
    key=lambda f: f.stat().st_size,
)
print(f"Found {len(files)} PDFs. Already indexed: {len(already_done)} hashes.")


def _parse_year_from_stem(stem: str) -> int | None:
    """Extract a 4-digit year from a filename stem."""
    matches = re.findall(r"\b(19[5-9]\d|20[0-2]\d)\b", stem)
    return int(matches[-1]) if matches else None


def _parse_standard_code(stem: str, folder_name: str) -> str:
    """Best-effort standard code from the filename stem.

    The filename stem is usually already a good standard code.
    Strip trailing '-YYYY' patterns that are redundant with the year column.
    """
    # Strip trailing year: "AS 1012.14-2018" -> "AS 1012.14"
    code = re.sub(r"[-\s]*(19[5-9]\d|20[0-2]\d)$", "", stem).strip()
    return code or stem


def _extract_title_from_text(text: str) -> str | None:
    """Heuristically extract the document title from the first ~500 chars."""
    if not text:
        return None
    # Take the first non-empty line that is longer than 10 chars
    clean = _ILLEGAL_CHARS.sub("", text)
    for line in clean[:1000].splitlines():
        line = line.strip()
        if len(line) > 10:
            return line[:200]
    return None


def _default_status(folder_name: str) -> str:
    return "superseded" if folder_name == "_archive" else "NEEDS_REVIEW"


batch_num = 0
for i in range(0, len(files), BATCH_SIZE):
    batch = files[i : i + BATCH_SIZE]
    batch_num += 1
    print(
        f"\n=== Batch {batch_num} ({i + 1}-{min(i + BATCH_SIZE, len(files))} of {len(files)}) ==="
    )

    new_rows: list[list] = []
    for f in batch:
        h = sha256(str(f))
        size_mb = round(f.stat().st_size / 1_000_000, 2)

        if h in already_done:
            print(f"  SKIP (already indexed): {f.name}")
            continue

        print(f"  {f.name}  ({size_mb} MB)")

        folder_name = f.parent.name
        issuing_body, jurisdiction = ISSUER_MAP.get(folder_name, ("", ""))
        subdomain = SUBDOMAIN_MAP.get(folder_name, "")
        status = _default_status(folder_name)
        standard_code = _parse_standard_code(f.stem, folder_name)
        year = _parse_year_from_stem(f.stem)

        # Text extraction
        notes_parts: list[str] = []
        if size_mb > TEXT_SIZE_LIMIT_MB:
            text = ""
            notes_parts.append(
                f"NEEDS_REVIEW: large file ({size_mb} MB) — verify metadata manually"
            )
        else:
            text = extract_text(f)
            if not text and ocr_reader:
                print("    -> No digital text; trying OCR...")
                text = ocr_extract_text(f, ocr_reader)
            if not text:
                notes_parts.append(
                    "NEEDS_REVIEW: no extractable text — digital and OCR both returned nothing"
                )

        # Title: try PDF text, fall back to stem
        title = _extract_title_from_text(text) or f.stem

        # Year: try PDF text if not found in filename
        if year is None and text:
            year_match = re.search(r"\b(19[5-9]\d|20[0-2]\d)\b", text[:2000])
            if year_match:
                year = int(year_match.group(1))

        if not subdomain:
            notes_parts.append(
                "NEEDS_REVIEW: subdomain not assigned — classify manually"
            )

        if status == "NEEDS_REVIEW":
            notes_parts.append(
                "NEEDS_REVIEW: status not confirmed — current/superseded/withdrawn/draft"
            )

        if not issuing_body:
            notes_parts.append("NEEDS_REVIEW: issuing body unknown")

        notes = "; ".join(notes_parts) if notes_parts else None

        relative_path = str(f.relative_to(r"G:\My Drive\Library"))
        canonical_filename = f.name  # Phase 2 will rename if needed

        row = [
            h,
            _sanitize(title),
            _sanitize(issuing_body),  # author = issuing body for standards
            _sanitize(issuing_body),  # publisher = issuing body for standards
            year,
            None,  # edition — standards use standard_code
            "PDF",
            _sanitize(relative_path),
            _sanitize(canonical_filename),
            "Engineering",
            _sanitize(subdomain),
            "Standard",
            "Standard",
            "",  # topics — NEEDS_REVIEW
            "",  # frameworks
            "",  # market_context
            "practitioner",
            "",  # skill_refs — auto-generated only
            _sanitize(notes),
            TODAY,
            # Engineering extra columns
            _sanitize(standard_code),
            _sanitize(status),
            _sanitize(jurisdiction),
            _sanitize(issuing_body),
            None,  # superseded_by — Phase 4
        ]

        new_rows.append(
            row
        )  # 25 cols: first 20 go to Master, all 25 to domain worksheet
        print(
            f"    code={standard_code!r}  year={year}  issuer={issuing_body!r}  status={status!r}"
        )
        already_done.add(h.upper())

    for row in new_rows:
        ws_master.append(row[:20])
        ws_domain.append(row)
    wb.save(INDEX_PATH)
    print(f"  -> Saved batch {batch_num} ({len(new_rows)} new rows).")

print("\nPhase 1 complete.")
print("Next: run dedup_index.py (Phase 3), then review NEEDS_REVIEW rows (Phase 4).")
