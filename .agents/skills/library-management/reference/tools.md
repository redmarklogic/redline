# Tools Reference

All tools live in `.agents/tools/library/`. Run from the repo root:

```powershell
.\.venv\Scripts\python.exe .agents\tools\library\<script>.py
```

| Script | Purpose |
|---|---|
| `workbook_utils.py` | Shared helpers: worksheet name constants (`DOMAIN_WORKSHEETS`, `ENHANCED_WORKSHEETS`), `WorkbookLock` (creates `library-index.xlsx.lock`), atomic save, path-based resume, domain-note sync |
| `metadata_extractor.py` | Incremental add: `MetadataExtractionRequest` + `BookMetadataExtractor` — API lookup, digital PDF text, OCR fallback, SHA-256, returns `BookMetadata` |
| `dedup_index.py` | Flags duplicate `sha256` hashes in `notes`; syncs notes to domain worksheets by `path` |
| `verify_index.py` | Preflight/post-run verification: worksheets, row counts, source file count (PDF + EPUB), `NEEDS_REVIEW`, duplicates, missing years |
| `export_needs_review.py` | Exports `NEEDS_REVIEW` rows to a single flat CSV |
| `export_review_pack.py` | Exports the full review-queue pack (5 CSVs): all, standards, non-standards, missing-year, duplicates |
| `enrich_safe_metadata.py` | Safe mechanical enrichment: fill years from filenames, normalise status vocabulary, sync years to domain worksheets |
| `merge_chapters.py` | Merges chapter PDFs into one file before indexing; verifies output before deleting source chapters |

## Workbook Lock

Writer tools acquire `WorkbookLock`, which creates `library-index.xlsx.lock` beside the workbook. A second writer must fail fast. Remove the lock only after confirming no Python indexer is still running:

```powershell
Get-CimInstance Win32_Process |
    Where-Object { $_.CommandLine -match "\.agents\\tools\\library" } |
    Select-Object ProcessId, CommandLine
```

## Common openpyxl Pitfalls

- PDF extraction can return control characters (`\x00–\x1f`, `\x7f–\x9f`) that openpyxl rejects with `IllegalCharacterError`. Keep raw text in `BookMetadata.text_sample`; sanitise strings before any workbook write.
- Always save under `WorkbookLock`; unsaved changes are lost on session exit.
- `verify_index.py` counts source files with `source_file_count` (both PDF and EPUB). The old `source_pdf_count` name is retired.
- `verify_index.py` defaults to `LIBRARY_ROOT`; pass `source_folder=` to narrow scope to a specific subfolder.
