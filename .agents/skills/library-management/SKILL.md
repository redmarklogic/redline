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
- A summary of what changed

### Out of Scope
- Domain judgments (which notebook to add a book to — route to the domain agent)
- Deciding whether to keep superseded editions — flag in `notes`, route to Graeme for engineering books
- Converting EPUB to PDF (flag, do not act without user confirmation)
- Deciding which duplicate copy to keep — flag, do not delete

---

## Index Schema

File: `G:\My Drive\Library\library-index.xlsx`
Worksheets: `Master` (all entries) + one per top-level domain folder (e.g. `Engineering`, `Management`). Engineering worksheets include extra columns — see **Engineering Worksheets** section below.

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

**Duplicate flagging:** Add `DUPLICATE of <path>` in `notes` on the second row. Never delete files — flag only.

---

### Domain vocabulary

| `domain` | `subdomain` examples |
|---|---|
| `Engineering` | `Geotechnical Engineering`, `Structural Engineering`, `Civil Engineering` |
| `Management` | `Organisational Design`, `People Operations`, `Leadership` |
| `Product` | `Product Management`, `Product Strategy`, `UX & Design` |
| `Marketing` | `Content Marketing`, `SEO`, `Social Selling`, `Brand Strategy`, `Demand Generation` |
| `Business Strategy` | `GTM Strategy`, `Competitive Positioning`, `Pricing`, `Platform Strategy` |
| `Artificial Intelligence` | `AI Systems`, `Machine Learning`, `AI Strategy` |
| `Learning & Development` | `Skills Development`, `Coaching`, `Learning Design` |

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

## Engineering Worksheets (within `library-index.xlsx`)

Engineering documents live in one or more worksheets inside `library-index.xlsx` — there is no separate engineering index file. The `Master` sheet holds all rows; the `Engineering` worksheet (and any subdomain worksheets, e.g. `Geotechnical Engineering`) hold the same rows plus additional engineering-specific columns.

Applies to `domain = Engineering` only. When indexing an engineering document, populate the extra columns below in addition to the standard Master columns.

| Column | Description | Example |
|---|---|---|
| `standard_code` | Official reference designation engineers cite | `BS EN 1997-1:2004`, `NZS 4402:1986` |
| `status` | `current` · `superseded` · `withdrawn` · `draft` | |
| `jurisdiction` | `UK` · `EU` · `NZ` · `AU` · `US` · `International` | |
| `issuing_body` | Standards body that authored the document (distinct from national distributor) | `CEN`, `CIRIA`, `BSI` |
| `superseded_by` | Reference code of the replacing document; populate when `status = superseded` | `BS EN 1997-1:2013` |

**Rules:** Never leave `status` blank for any engineering standard. When `status = superseded`, always populate `superseded_by` if known — flag to Graeme if unknown. Non-standard engineering books (textbooks, guidance notes) leave `standard_code`, `status`, `jurisdiction`, `issuing_body`, and `superseded_by` blank.

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

## Folder Indexing Workflow

Four sequential phases — Phases 1-3 run without user interaction. Phase 4 requires user approval.
See [procedures/index-folder.md](procedures/index-folder.md) for step-by-step detail.

| Phase | Purpose | Tool |
|---|---|---|
| 0 — Pre-scan | Exact filenames via `Get-ChildItem`; **index integrity check**; chapter subfolder cleanup | PowerShell + Python |
| 1 — Batch index | Extract text/OCR; build rows; save every 8 files | `.agents/tools/library/batch_index.py` |
| 2 — Rename | Apply canonical filenames; update index | Inline snippet in `index-folder.md` |
| 3 — Dedup | Flag duplicate hashes in `notes` | `.agents/tools/library/dedup_index.py` |
| 4 — Web search | Resolve NEEDS_REVIEW rows | Browser (approval required) |

For chapter subfolders, see [procedures/chapter-subfolders.md](procedures/chapter-subfolders.md).

---

## Adding a Single New Book

See [procedures/add-single-book.md](procedures/add-single-book.md).

---

## Tools Reference

All tools live in `.agents/tools/library/`. Run from the repo root:

```powershell
.\.venv\Scripts\python.exe .agents\tools\library\<script>.py
```

| Script | Purpose |
|---|---|
| `extract_text.py` | Importable helpers: `sha256`, `extract_text`, `make_ocr_reader`, `ocr_extract_text` |
| `batch_index.py` | Phase 1 — batch loop; set `FOLDER` and `DOMAIN_WS` constants before running |
| `batch_index_standards.py` | Phase 1 — automated Standards variant; derives metadata from folder name (issuer) and filename (code, year); no interactive metadata entry |
| `dedup_index.py` | Phase 3 — flags duplicate hashes in `notes`; no configuration needed |
| `merge_chapters.py` | Phase 0 helper — merges chapter PDFs into one file; takes CLI args |
| `create_fresh_index.py` | Emergency tool — creates a new `library-index.xlsx` with correct worksheets and headers; overwrites existing file |

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
| Using inline Python in PowerShell (`-c "..."`) | Use the tools in `.agents/tools/library/` — run them as files. |
| Assuming filenames from session notes | Always run `Get-ChildItem` — actual names are often longer than remembered. |
| Not saving after each batch | Save after every batch. Unsaved index is lost on session exit. |
| Hardcoding already-indexed hashes | `batch_index.py` loads them dynamically — do not hardcode. |
| Running dedup checks during Phase 1 | Dedup is Phase 3 only — inline checking slows the batch loop. |
| Blocking on web search mid-run | Mark NEEDS_REVIEW, continue, batch all web searches in Phase 4. |
| Processing large files (> 100 MB) first | Sort by size ascending — `batch_index.py` does this automatically. |
| Using `C:\Temp` as temp directory | Use `$env:TEMP` — `C:\Temp` may not exist. |
| Instantiating `easyocr.Reader` per file | `make_ocr_reader()` is called once in `batch_index.py` — do not move it inside the loop. |
| Leaving `status` blank for engineering standards | Default to `current` only when confirmed. Never blank. |
| Not verifying the index before Phase 1 | Run Phase 0d — open `library-index.xlsx` in Python and confirm expected worksheets exist before scanning any files. |
| Writing PDF-extracted text directly to openpyxl cells | PDF extraction returns control characters (`\x00–\x1f`, `\x7f–\x9f`) that openpyxl rejects with `IllegalCharacterError`. Sanitize every string field — see `batch_index_standards.py` for the `_sanitize()` pattern. |
| Invoking a persona agent (Linda, Graeme, etc.) for execution | Persona agents are advisory — they do not run shell commands or scripts. Apply the persona's skills directly and execute the work in the main agent. |
