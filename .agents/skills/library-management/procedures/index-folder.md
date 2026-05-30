# Procedure: Index a Folder

Bulk initial-index tools have been retired. To index a folder of new files, run preflight once, then repeat [add-single-book.md](add-single-book.md) for each PDF. Phase 4 requires approval when rows remain `NEEDS_REVIEW`.

---

## Phase 0 — Pre-scan

**0a. Confirm no workbook writer is active.** Only one process may write `library-index.xlsx`. Writer tools create `library-index.xlsx.lock` beside the workbook. If that lock exists, stop and confirm there is no active Python indexer before removing it:

```powershell
Get-CimInstance Win32_Process |
    Where-Object { $_.CommandLine -match "\.agents\\tools\\library" } |
    Select-Object ProcessId, CommandLine
```

**0b. List all PDFs with exact names and sizes — never assume filenames from session notes:**

```powershell
Get-ChildItem -Recurse -Path "G:\My Drive\Library\<folder>" -Filter "*.pdf" |
  Where-Object { $_.Name -ne "desktop.ini" } |
  Sort-Object Length |
  Select-Object FullName, Length |
  Format-Table -AutoSize
```

This reveals exact filenames (often longer than remembered) and shows large files that will be slow to OCR.

**0c. Handle chapter subfolders** before indexing. See [chapter-subfolders.md](chapter-subfolders.md).

**0d. Already-indexed paths** are the resume key. Before appending a row, check the `path` column in `Master`. Never use `sha256` as the resume key because duplicate physical files still need rows.

**0e. Verify the index file is readable before proceeding.** A corrupted index means all Phase 1 work is lost on first write:

```python
import openpyxl
wb = openpyxl.load_workbook(r"G:\My Drive\Library\library-index.xlsx", read_only=True)
print("Worksheets:", wb.sheetnames)  # must include "Master" and the target domain worksheet
wb.close()
```

If this raises `BadZipFile` or `InvalidFileException`, stop and ask the user how to recover the workbook. Do not recreate the initial index automatically.

**0f. Run the verification summary before indexing:**

```powershell
.\.venv\Scripts\python.exe .agents\tools\library\verify_index.py
```

Record the starting worksheet row counts and `NEEDS_REVIEW` counts.

---

## Phase 1 — Extract and Append Each New PDF

For each PDF in the folder, run [add-single-book.md](add-single-book.md). The canonical extraction path is `MetadataExtractionRequest` plus `BookMetadataExtractor.extract_metadata()` from `.agents/tools/library/metadata_extractor.py`.

Do not block the folder on missing OCR/API metadata. Append the physical-file row with the known fields and mark missing metadata with `NEEDS_REVIEW` in `notes`. <!-- hook: allow -->

---

## Phase 2 — Rename Files

After all new files are indexed, rename files to the canonical convention (see naming rules in SKILL.md). Run renaming as a separate step — the index must be consistent before files move.

For standards, preserve official filenames unless the user explicitly requests canonical renaming. If skipped, report Phase 2 as `skipped`, not complete.

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

This flags duplicate hashes in `Master` and syncs duplicate notes to domain worksheets by `path`.

Run verification immediately after dedup:

```powershell
.\.venv\Scripts\python.exe .agents\tools\library\verify_index.py
```

Report:

- source file count (PDF + EPUB)
- `Master` row count
- target domain worksheet row count
- duplicate note counts in `Master` and the domain worksheet
- missing-year counts
- `NEEDS_REVIEW` counts

---

## Phase 3.5 -- Safe Enrichment

Run safe mechanical enrichment that requires no domain judgment:

```powershell
.\.venv\Scripts\python.exe .agents\tools\library\enrich_safe_metadata.py
```

This tool performs three operations:

1. **Fill missing years** from unambiguous trailing filename tokens (e.g. `BS-EN-1997-1-2004.pdf` -> year 2004)
2. **Normalize status values** across all worksheets (`NEEDS_REVIEW` -> `needs_review`, etc.)
3. **Sync years to domain worksheets** by path key

Run verification immediately after enrichment to confirm counts changed as expected.

---

## Phase 4 — Web Search (requires user approval)

After Phases 1–3, export all `NEEDS_REVIEW` rows and present the review queue:

```powershell
.\.venv\Scripts\python.exe .agents\tools\library\export_needs_review.py
```

For ad hoc inspection, collect rows directly:

```python
import openpyxl
wb = openpyxl.load_workbook(r"G:\My Drive\Library\library-index.xlsx")
ws = wb["Master"]
headers = [cell.value for cell in ws[1]]
filename_idx = headers.index("canonical_filename")
notes_idx = headers.index("notes")
needs_review = [
    (row[filename_idx].value, row[notes_idx].value)
    for row in ws.iter_rows(min_row=2)
    if row[notes_idx].value and "NEEDS_REVIEW" in str(row[notes_idx].value)
]
print(f"{len(needs_review)} rows need review:")
for filename, note in needs_review:
    print(f"  {filename}: {note}")
```

**Request permission before browsing any URL.** Route standards currentness decisions to the Domain Expert. After resolving each item, update `status`, update `superseded_by` where relevant, and remove the corresponding `NEEDS_REVIEW` flag. Save after each update.

### Structured the Domain Expert Review Request

Before invoking the Domain Expert for standards review, prepare a structured handoff using the following template. Do not send free-text descriptions.

```markdown
## Library Review Request for the Domain Expert

### Current State
- Master rows: <count>
- Standards rows: <count>
- Missing year rows: <count>
- Duplicate rows: <count>
- Status breakdown: current=<n>, superseded=<n>, needs_review=<n>

### Review Queue Files
- `review-queues/needs-review-standards.csv` (<n> rows)
- `review-queues/duplicates.csv` (<n> rows)

### Decision Points (yes/no required)
1. **Safe enrichment already applied:** years filled from filenames (<n>), statuses normalized (<n>). Any corrections needed?
2. **Duplicates:** <n> rows flagged. Which copy to keep for each group?
3. **Standards currentness:** <n> standards have `status=needs_review`. Which require official metadata lookup vs. can be resolved from filename/issuer alone?
4. **Red lines:** Any rows that must NOT be modified without the Domain Expert's explicit approval?

### Expected Response Format
For each decision point, respond with:
- APPROVED / REJECTED / NEEDS_MORE_INFO
- For duplicates: path of the copy to keep
- For standards: status assignment (current/superseded/withdrawn) and superseded_by if applicable
```

Generate this template by running `verify_index.py` and `export_review_pack.py` first, then populating the counts from their output.
