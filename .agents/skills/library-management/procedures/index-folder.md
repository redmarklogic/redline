# Procedure: Index a Folder

Four sequential phases. Run in order. Phases 1–3 require no user interaction. Phase 4 requires approval.

---

## Phase 0 — Pre-scan

**0a. List all PDFs with exact names and sizes — never assume filenames from session notes:**

```powershell
Get-ChildItem -Recurse -Path "G:\My Drive\Library\<folder>" -Filter "*.pdf" |
  Where-Object { $_.Name -ne "desktop.ini" } |
  Sort-Object Length |
  Select-Object FullName, Length |
  Format-Table -AutoSize
```

This reveals exact filenames (often longer than remembered) and shows large files that will be slow to OCR.

**0b. Handle chapter subfolders** before indexing. See [chapter-subfolders.md](chapter-subfolders.md).

**0c. Already-indexed hashes** are loaded automatically by `batch_index.py` — no manual action needed.

**0d. Verify the index file is readable before proceeding.** A corrupted index means all Phase 1 work is lost on first write:

```python
import openpyxl
wb = openpyxl.load_workbook(r"G:\My Drive\Library\library-index.xlsx", read_only=True)
print("Worksheets:", wb.sheetnames)  # must include "Master" and the target domain worksheet
wb.close()
```

If this raises `BadZipFile` or `InvalidFileException`, stop. Use `create_fresh_index.py` to recreate the file (this is destructive — confirm with the user first if the file might contain unrecovered data).

---

## Phase 1 — Batch Index

1. Open `.agents/tools/library/batch_index.py`.
2. Set `FOLDER` and `DOMAIN_WS` at the top.
3. Run from the repo root:
   ```powershell
   .\.venv\Scripts\python.exe .agents\tools\library\batch_index.py
   ```
4. For each file the script prints a **TEXT SNIPPET**. At the `<<< FILL IN METADATA >>>` block, uncomment and populate the metadata fields, then re-run the batch to write the rows.
5. The script saves after every 8 files. If the session exits, re-run from step 3 — already-indexed hashes are skipped.

**Required packages** (install once): `pypdf`, `openpyxl`, `easyocr`, `pypdfium2`.

---

## Phase 2 — Rename Files

After all batches are indexed, rename files to the canonical convention (see naming rules in SKILL.md). Run renaming as a separate step — the index must be consistent before files move.

```python
import openpyxl, pathlib
from datetime import date

INDEX_PATH = r"G:\My Drive\Library\library-index.xlsx"
TODAY = date.today().isoformat()

# Build from the metadata collected in Phase 1
renames = [
    (r"G:\My Drive\Library\...\old-name.pdf", "New-Canonical-Name_Author_Year.pdf"),
    # one tuple per file
]

wb = openpyxl.load_workbook(INDEX_PATH)
ws_master = wb["Master"]

for old_path_str, new_name in renames:
    old_path = pathlib.Path(old_path_str)
    new_path = old_path.parent / new_name
    if not old_path.exists():
        print("NOT FOUND:", old_path.name); continue
    if new_path.exists() and old_path != new_path:
        print("TARGET EXISTS:", new_name); continue
    old_path.rename(new_path)
    relative_new = str(new_path.relative_to(r"G:\My Drive\Library"))
    for row in ws_master.iter_rows(min_row=2):
        if row[8].value == old_path.name:
            row[7].value = relative_new
            row[8].value = new_name
            row[19].value = TODAY
    wb.save(INDEX_PATH)
    print("Renamed:", new_name)
```

Always update **both** `path` (col 8) and `canonical_filename` (col 9) together. Save after each rename.

---

## Phase 3 — Deduplication

```powershell
.\.venv\Scripts\python.exe .agents\tools\library\dedup_index.py
```

---

## Phase 4 — Web Search (requires user approval)

After Phases 1–3, collect all NEEDS_REVIEW rows and present them:

```python
import openpyxl
wb = openpyxl.load_workbook(r"G:\My Drive\Library\library-index.xlsx")
ws = wb["Master"]
needs_review = [
    (row[8].value, row[12].value)
    for row in ws.iter_rows(min_row=2)
    if row[12].value and "NEEDS_REVIEW" in str(row[12].value)
]
print(f"{len(needs_review)} rows need review:")
for filename, note in needs_review:
    print(f"  {filename}: {note}")
```

**Request permission before browsing any URL.** After resolving each item, update the row and remove the `NEEDS_REVIEW` flag. Save after each update.
