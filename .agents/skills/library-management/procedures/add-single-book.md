# Procedure: Add a Single New Book

1. **Copy** the file to the correct folder under `G:\My Drive\Library\`.

2. **Extract metadata with the canonical incremental extractor:**

   ```python
   import pathlib
   import sys

   sys.path.insert(0, ".agents/tools/library")
   from metadata_extractor import BookMetadataExtractor, MetadataExtractionRequest

   path = pathlib.Path(r"G:\My Drive\Library\...\filename.pdf")
   request = MetadataExtractionRequest(pdf_path=path)
   metadata = BookMetadataExtractor().extract_metadata(request)
   print(metadata.model_dump_json(indent=2))
   ```

   The returned `BookMetadata` is the source for `sha256`, `title`, `authors`, `publisher`, `year`, `format`, `path`, `category`, `document_type`, `topics`, `market_context`, API source, and PDF/OCR provenance. If OCR dependencies are unavailable, the extractor returns no OCR text and the row must retain `NEEDS_REVIEW` for missing metadata.

3. **Check for existing path and duplicate hash:** use `path` as the resume/idempotency key. If the `sha256` already exists on another row, add the new physical file anyway and put `DUPLICATE of <existing path>` in `notes`.

4. **Translate `BookMetadata` to workbook vocabulary:**

   | Workbook column | Source |
   | --- | --- |
   | `sha256` | `metadata.sha256` |
   | `title` | `metadata.title` |
   | `author` | `"; ".join(metadata.authors)` |
   | `publisher` | `metadata.publisher` |
   | `year` | `metadata.published_year` |
   | `format` | `PDF` |
   | `path` | `metadata.relative_path` |
   | `canonical_filename` | `metadata.file_name` after any rename |
   | `category` | `metadata.category` |
   | `document_type` | `metadata.document_type` |
   | `topics` | `"; ".join(metadata.topics)` |
   | `market_context` | `"; ".join(metadata.market_context)` |
   | `notes` | `NEEDS_REVIEW` flags, duplicate note, extraction/API provenance |

5. **Append the row under the workbook lock:** reuse the `metadata` object from step 2 when building `row`.

   ```python
   import openpyxl
   import pathlib
   import sys
   from datetime import date

   sys.path.insert(0, ".agents/tools/library")
   from workbook_utils import INDEX_PATH, WorkbookLock, append_index_row, save_workbook_atomically

   CATEGORY_TO_WORKSHEET = {
       "Book": "Ebooks",
       "Standard": "Standards",
       "Magazine": "Magazines",
       "Misc": "Misc",
   }

   # Build `row` from the table above. Standards rows need the 5 extra
   # engineering columns; use status="needs_review" unless Graeme confirms currentness.
   with WorkbookLock(INDEX_PATH):
       workbook = openpyxl.load_workbook(INDEX_PATH)
       append_index_row(workbook, CATEGORY_TO_WORKSHEET[metadata.category], row)
       save_workbook_atomically(workbook, INDEX_PATH)
   ```

6. **Determine canonical filename** using the naming rules in SKILL.md.

7. **Rename** the file on disk when appropriate. Update both `path` and `canonical_filename` in the index row. Set `last_updated`.

8. **Run dedup:**

   ```powershell
   .\.venv\Scripts\python.exe .agents\tools\library\dedup_index.py
   ```

9. **Flag to the domain agent** if the book is domain-relevant (e.g. Graeme for geotechnical engineering).
