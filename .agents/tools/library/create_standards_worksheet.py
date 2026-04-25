"""One-off script: create the Standards worksheet in library-index.xlsx.

Run once from the repo root:
    .venv\\Scripts\\python.exe .agents\\tools\\library\\create_standards_worksheet.py
"""

import openpyxl

INDEX_PATH = r"G:\My Drive\Library\library-index.xlsx"

STANDARD_COLS = [
    "sha256",
    "title",
    "author",
    "publisher",
    "year",
    "edition",
    "format",
    "path",
    "canonical_filename",
    "domain",
    "subdomain",
    "category",
    "document_type",
    "topics",
    "frameworks",
    "market_context",
    "audience",
    "skill_refs",
    "notes",
    "last_updated",
]
ENGINEERING_EXTRA_COLS = [
    "standard_code",
    "status",
    "jurisdiction",
    "issuing_body",
    "superseded_by",
]

wb = openpyxl.load_workbook(INDEX_PATH)

if "Standards" in wb.sheetnames:
    print("'Standards' worksheet already exists — no changes made.")
else:
    ws = wb.create_sheet("Standards")
    headers = STANDARD_COLS + ENGINEERING_EXTRA_COLS
    ws.append(headers)
    wb.save(INDEX_PATH)
    print(f"Created 'Standards' worksheet with {len(headers)} columns:")
    print("  " + ", ".join(headers))
