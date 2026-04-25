# Procedure: Add a Single New Book

1. **Copy** the file to the correct folder under `G:\My Drive\Library\`.

2. **Hash and check for duplicates:**
   ```python
   import sys, pathlib
   sys.path.insert(0, ".agents/tools/library")
   from extract_text import sha256
   import openpyxl

   path = pathlib.Path(r"G:\My Drive\Library\...\filename.pdf")
   h = sha256(path)
   wb = openpyxl.load_workbook(r"G:\My Drive\Library\library-index.xlsx")
   existing = {str(row[0].value).upper() for row in wb["Master"].iter_rows(min_row=2) if row[0].value}
   print("DUPLICATE" if h in existing else "NEW", h)
   ```

3. If the hash already exists, add a row anyway with `DUPLICATE of <existing path>` in `notes`.

4. **Extract text:**
   ```python
   from extract_text import extract_text, make_ocr_reader, ocr_extract_text
   text = extract_text(path)
   if not text:
       reader = make_ocr_reader()
       if reader:
           text = ocr_extract_text(path, reader)
       else:
           text = ""  # easyocr not installed — will be marked NEEDS_REVIEW
   print(text[:500] or "(no text)")
   ```
   Files > 100 MB: skip extraction and mark `NEEDS_REVIEW: large file`.

5. **Determine canonical filename** using the naming rules in SKILL.md.

6. **Rename** the file on disk. Update both `path` and `canonical_filename` in the index row. Set `last_updated`.

7. **Append a row** to `Master` and the domain worksheet. Save immediately.

8. **Run dedup:**
   ```powershell
   .\.venv\Scripts\python.exe .agents\tools\library\dedup_index.py
   ```

9. **Flag to the domain agent** if the book is domain-relevant (e.g. Graeme for geotechnical engineering).
