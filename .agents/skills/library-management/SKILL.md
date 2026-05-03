---
name: library-management
description: Use when indexing, renaming, or adding books to the digital library at G:\My Drive\Library — covers scanning folders, extracting metadata from PDFs, updating the Excel index, and renaming files to the canonical convention.
---

# Library Management

## Overview

The canonical digital library lives at `G:\My Drive\Library`. All books are indexed in `G:\My Drive\Library\library-index.xlsx` — this file is the single source of truth. Every operation must leave the index consistent before finishing.

## Boundary Contract

### Inputs
- A folder path inside `G:\My Drive\Library\` to scan, or a file to add
- Instructions to rename, deduplicate, or update entries

### Outputs
- Updated `library-index.xlsx` (both `Master` and domain worksheet)
- Files renamed on disk to the canonical convention
- Verification summary proving workbook integrity, row counts, duplicate sync, and review queues
- A summary of what changed

### Out of Scope
- Domain judgments (which notebook to add a book to — route to the domain agent)
- Deciding whether to keep superseded editions — flag in `notes`, route to Graeme for engineering books
- Converting EPUB to PDF (flag, do not act without user confirmation)
- Deciding which duplicate copy to keep — flag, do not delete

---

## Index Schema

File: `G:\My Drive\Library\library-index.xlsx`
Worksheets: `Master` (all entries) + four domain worksheets: `Ebooks`, `Standards`, `Magazines`, `Misc`. Only `Standards` includes extra engineering columns — see **Engineering Worksheets** section below.

| Worksheet | Content | Headers |
|---|---|---|
| `Master` | Every physical file in the library | Standard (20 columns) |
| `Ebooks` | PDF and EPUB ebooks | Standard (20 columns) |
| `Standards` | Engineering standards | Enhanced (20 standard + 5 engineering) |
| `Magazines` | Magazine PDFs and EPUBs | Standard (20 columns) |
| `Misc` | Everything that does not fit Ebooks, Standards, or Magazines | Standard (20 columns) |

**One row per physical file.** Two rows may share a `sha256` — that signals a duplicate.

| Column | Description |
|---|---|
| `sha256` | SHA-256 hash — used to detect duplicates |
| `title` | Full title including meaningful subtitle |
| `author` | All authors, semicolon-separated. Format: `Surname, Firstname` |
| `publisher` | Publisher or national distributor |
| `year` | Year of publication (integer) |
| `edition` | Edition number only (e.g. `3rd`). Official reference codes for standards go in `standard_code` on the Engineering worksheet. |
| `format` | `PDF` or `EPUB` |
| `path` | Path relative to `G:\My Drive\Library\` (no drive letter) |
| `canonical_filename` | Filename only, in canonical convention |
| `domain` | Top-level folder name |
| `subdomain` | Sub-folder name |
| `category` | Origin type (see vocabulary below) |
| `document_type` | Semantic character (see vocabulary below) |
| `topics` | 3-8 thematic tags, semicolon-separated |
| `frameworks` | Named methodologies or models, semicolon-separated |
| `market_context` | Industries or segments the book addresses, semicolon-separated |
| `audience` | Primary intended reader (see vocabulary below) |
| `skill_refs` | Auto-generated — never populate manually |
| `notes` | Administrative flags only: `DUPLICATE of <path>`, `SUPERSEDED`, `NEEDS_REVIEW`, licensing |
| `last_updated` | ISO date (`YYYY-MM-DD`) |

**Resume/idempotency key:** use relative `path`, never `sha256`. Every physical file gets a row.

**Duplicate flagging:** Add `DUPLICATE of <path>` in `notes` on the second row. Never delete files — flag only. `sha256` is only for duplicate grouping after indexing.

---

### Domain vocabulary — Library of Congress Classification (LCC)

The physical folder structure uses **LCC**. `domain` = the LCC root folder name; `subdomain` = the LCC subclass folder name. Folder format: `<LCC Root>\<LCC Subclass>\filename`.

Example: a geotechnical engineering textbook goes in `T - Technology\TA700-712 - Foundation and Geotechnical Engineering\`.

**Determining the correct LCC class:**
1. Look up the book's LCC number via the [Library of Congress catalogue](https://catalog.loc.gov) or WorldCat.
2. Use the first two characters of the LCC number to identify the subclass (e.g. `HD` → `HD - Industries. Land use. Labor`).
3. The root folder is the single-letter prefix (e.g. `H` → `H - Social Sciences`).
4. If no LCC number is available, use the most specific subclass from the reference table below.

**Commonly used LCC classes in this library:**

| `domain` (LCC root folder) | `subdomain` (LCC subclass folder) | Typical content |
|---|---|---|
| `H - Social Sciences` | `HD - Industries. Land use. Labor` | Business strategy, innovation, creativity (HD53), management, entrepreneurship — "Land use" is one narrow section; HD covers industries and business broadly |
| `H - Social Sciences` | `HF - Commerce` | Marketing, sales, branding |
| `H - Social Sciences` | `HM - Sociology` | Organisational behaviour, leadership |
| `Q - Science` | `QA - Mathematics` | Statistics, data science, machine learning |
| `T - Technology` | `TA - Engineering (General). Civil engineering` | Civil/geotechnical engineering, professional practice |
| `T - Technology` | `TC - Hydraulic engineering` | Hydraulics, dams, flood management |
| `T - Technology` | `TH - Building construction` | Structural, building |
| `B - Philosophy. Psychology. Religion` | `BF - Psychology` | Cognitive science, decision-making, behavioural economics |

---

### Category vocabulary

Origin type — what kind of physical object this file is:

`Book` · `Handbook` · `Framework Guide` · `Academic Paper` · `Conference Paper` · `Magazine Issue` · `Chapter` · `Standard` · `Guidance Note` · `Technical Report` · `Code of Practice`

---

### Document type vocabulary

Semantic character — how to use it, independent of origin:

`Textbook` · `Practical Guide` · `Reference Manual` · `Case Studies` · `Theory` · `Standard` · `Code of Practice` · `Guidance Note` · `Technical Report` · `Magazine Issue` · `Chapter` · `Academic Paper` · `Workbook`

**Note:** `category` and `document_type` serve different purposes. A file can be `category = Guidance Note` and `document_type = Practical Guide` simultaneously.

---

### Audience vocabulary

`practitioner` · `executive` · `academic` · `consultant` · `general`

---

## Standards Worksheet (within `library-index.xlsx`)

The `Standards` worksheet is the only domain worksheet with enhanced headers. It holds engineering standards with additional engineering-specific columns beyond the standard 20. The `Master` sheet holds all rows with standard headers only.

When indexing an engineering standard, populate the extra columns below in addition to the standard Master columns.

| Column | Description | Example |
|---|---|---|
| `standard_code` | Official reference designation engineers cite | `BS EN 1997-1:2004`, `NZS 4402:1986` |
| `status` | `current` · `superseded` · `withdrawn` · `draft` · `needs_review` | |
| `jurisdiction` | `UK` · `EU` · `NZ` · `AU` · `US` · `International` | |
| `issuing_body` | Standards body that authored the document (distinct from national distributor) | `CEN`, `CIRIA`, `BSI` |
| `superseded_by` | Reference code of the replacing document; populate when `status = superseded` | `BS EN 1997-1:2013` |

**Rules:** Never leave `status` blank for any engineering standard. Use `needs_review` when currentness is unknown; do not default to `current` unless confirmed. When `status = needs_review`, add a `NEEDS_REVIEW` note and route currentness resolution to Graeme. When `status = superseded`, always populate `superseded_by` if known — flag to Graeme if unknown. Non-standard engineering books (textbooks, guidance notes) leave `standard_code`, `status`, `jurisdiction`, `issuing_body`, and `superseded_by` blank.

---

## Canonical Filename Convention

Format: `Full-Title-Without-Marketing-Subtitle_FirstAuthorSurname_Year.pdf`

**Rules:**
1. Title Case with hyphens instead of spaces. Only `_` separates the three components.
2. Drop the subtitle only if it is marketing padding (adds no meaning).
3. Keep the subtitle if it disambiguates from sibling books with the same main title.
4. Replace colons with hyphens. Strip publisher names, edition tags, licensing notes.
5. First author surname only in filename; full list in `author` column.
6. 4-digit publication year.

```
Continuous-Delivery_Humble_2010.pdf
Geotechnical-Baseline-Reports-Suggested-Guidelines_Essex_2022.pdf
Geotechnical-Baseline-Reports-Guide-to-Good-Practice_Davis_2023.pdf
```

---

## Incremental Add Workflow

The initial full-library index is complete. The default workflow is now incremental: add one new file, extract metadata, update the workbook, deduplicate, verify.

For a single new PDF, see [procedures/add-single-book.md](procedures/add-single-book.md). For a folder of new PDFs, repeat the single-book procedure for each file; do not recreate the initial index.

Sequential phases — Phases 0-3 run without user interaction. Phase 4 requires user approval when rows remain `NEEDS_REVIEW`.
See [procedures/index-folder.md](procedures/index-folder.md) for step-by-step detail.

| Phase | Purpose | Tool |
|---|---|---|
| 0 — Preflight | Exact filenames, workbook readability, expected worksheets, no active writer | PowerShell + `.agents/tools/library/verify_index.py` |
| 1 — Extract metadata | Build a Pydantic `BookMetadata` record from path, PDF/OCR text, and catalogue APIs | `.agents/tools/library/metadata_extractor.py` |
| 2 — Workbook update | Append one row to `Master` and the matching domain worksheet; use `path` as the idempotency key | `.agents/tools/library/workbook_utils.py` |
| 3 — Rename | Apply canonical filenames when appropriate; update `path` and `canonical_filename` together | Inline snippet in `index-folder.md` |
| 4 — Dedup | Flag duplicate hashes in `notes`; sync duplicate notes to domain worksheets by `path` | `.agents/tools/library/dedup_index.py` |
| 5 — Review/enrichment | Resolve `NEEDS_REVIEW` rows and standards currentness | Browser/Graeme approval required |

**Workbook lock:** writer tools use `workbook_utils.WorkbookLock`, which creates `library-index.xlsx.lock` beside the workbook. A second writer must fail fast. Remove the lock only after confirming no Python indexer process is still running.

For chapter subfolders, see [procedures/chapter-subfolders.md](procedures/chapter-subfolders.md).

---

## Adding a Single New Book

See [procedures/add-single-book.md](procedures/add-single-book.md).

---

## Tools Reference

All tools live in `.agents/tools/library/`. Script-style tools run from the repo root:

```powershell
.\.venv\Scripts\python.exe .agents\tools\library\<script>.py
```

| Script | Purpose |
|---|---|
| `workbook_utils.py` | Importable helpers: shared headers, worksheet name constants (`DOMAIN_WORKSHEETS`, `ENHANCED_WORKSHEETS`), `WorkbookLock` (`library-index.xlsx.lock`), atomic save, path-based resume, domain-note sync |
| `metadata_extractor.py` | Incremental add helper: `MetadataExtractionRequest`, `BookMetadataExtractor`, API lookup, digital PDF text, OCR fallback, SHA-256, and final `BookMetadata` output |
| `dedup_index.py` | Phase 3 — flags duplicate hashes in `notes` and syncs domain worksheets by `path`; no configuration needed |
| `verify_index.py` | Preflight/post-run verification summary: worksheets, row counts, source PDF count, `NEEDS_REVIEW`, duplicates, missing years |
| `export_needs_review.py` | Exports `NEEDS_REVIEW` rows to a single flat CSV review queue |
| `export_review_pack.py` | Exports the full review-queue pack (5 CSVs): all, standards, non-standards, missing-year, duplicates |
| `enrich_safe_metadata.py` | Safe mechanical enrichment: fill years from filenames, normalize status vocabulary, sync years to domain worksheets |
| `merge_chapters.py` | Phase 0 helper — merges chapter PDFs into one file; takes CLI args |

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Dropping a subtitle that disambiguates | Check: sibling books with the same main title? If yes, keep the subtitle. |
| Using full author list in filename | First author surname only; full list in `author` column. |
| Updating `path` but not `canonical_filename` | Always update both columns together. |
| Forgetting `last_updated` after a rename | Set it every time a row is touched. |
| Skipping a duplicate row | Every file gets a row. Add `DUPLICATE of <path>` — never silently skip. |
| Deleting duplicate files without user instruction | Flag in `notes`. The user decides. |
| Deleting chapters before confirming merge succeeded | `merge_chapters.py` verifies output before deleting — use the tool. |
| Acting on EPUB-to-PDF conversion without confirmation | Flag it. Never convert without user approval. |
| Writing throwaway Python for metadata extraction | Use the documented `metadata_extractor.py` and `workbook_utils.py` imports in [procedures/add-single-book.md](procedures/add-single-book.md). |
| Assuming filenames from session notes | Always run `Get-ChildItem` — actual names are often longer than remembered. |
| Not saving after each workbook mutation | Save atomically before moving to the next file. Unsaved index changes are lost on session exit. |
| Running retired initial-index scripts for a single file | Use `metadata_extractor.py`, then append one workbook row under `WorkbookLock`. |
| Using `sha256` as the resume key | Use relative `path` to skip already-indexed rows; use `sha256` only in the dedup pass. |
| Running multiple workbook writers | Stop. All writer tools must acquire the workbook lock; if a lock exists, confirm no writer is active before removing it. |
| Running dedup checks during Phase 1 | Dedup is Phase 3 only — inline checking slows the batch loop. |
| Blocking on web search mid-run | Mark NEEDS_REVIEW, continue, batch all web searches in Phase 4. |
| Using `C:\Temp` as temp directory | Use `$env:TEMP` — `C:\Temp` may not exist. |
| Instantiating OCR repeatedly | Reuse one `BookMetadataExtractor`; it caches the OCR reader lazily. |
| Leaving `status` blank for engineering standards | Use `needs_review` until currentness is confirmed. Never default to `current`. |
| Not verifying the index before extraction | Run preflight — open `library-index.xlsx` in Python and confirm expected worksheets exist before scanning any files. |
| Skipping post-run verification | Run `verify_index.py`; report source PDF count, `Master`/domain row counts, duplicate note counts, missing-year counts, and `NEEDS_REVIEW` counts. |
| Writing raw PDF-extracted text directly to openpyxl cells | PDF extraction can return control characters (`\x00–\x1f`, `\x7f–\x9f`) that openpyxl rejects with `IllegalCharacterError`. Keep raw text in `BookMetadata.text_sample`; sanitize any string before workbook writes if openpyxl rejects it. |
| Invoking a persona agent (Linda, Graeme, etc.) for execution | Persona agents are advisory — they do not run shell commands or scripts. Apply the persona's skills directly and execute the work in the main agent. |
| Writing throwaway `tmp_*.py` scripts for repeatable operations | Promote to a permanent tool in `.agents/tools/library/` after first use. If no tool exists, create one before proceeding. |
| Using `source_pdf_count` in verify output | Renamed to `source_file_count` — counts both PDF and EPUB. |
| Hardcoding `verify_index.py` source folder to Standards only | Default is now `LIBRARY_ROOT`; pass `source_folder=` to narrow scope. |
