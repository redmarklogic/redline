---
name: library-management
description: Use when indexing, renaming, or adding books to the digital library at G:\My Drive\Library — covers scanning folders, extracting metadata from PDFs, using the SNZ scraper for NZ/AU standard metadata (title, status, canonical code), updating the Excel index, and renaming files to the canonical convention.
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
| `Master` | Every physical file in the library | Standard (22 columns) |
| `Ebooks` | PDF and EPUB ebooks | Standard (22 columns) |
| `Standards` | Engineering standards | Enhanced (22 standard + 5 engineering; additional columns are planned — see below) |
| `Magazines` | Magazine PDFs and EPUBs | Standard (22 columns) |
| `Misc` | Everything that does not fit Ebooks, Standards, or Magazines | Standard (22 columns) |

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
| `T - Technology` | `TA - Engineering (General). Civil engineering` | Civil engineering (general), professional practice |
| `T - Technology` | `TA700-712 - Foundation and Geotechnical Engineering` | Geotechnical engineering, foundation engineering |
| `T - Technology` | `TC - Hydraulic engineering` | Hydraulics, dams, flood management |
| `T - Technology` | `TH - Building construction` | Structural, building |
| `B - Philosophy. Psychology. Religion` | `BF - Psychology` | Cognitive science, decision-making, behavioural economics |

---

### Category vocabulary

Origin type — what kind of physical object this file is:

`Book` · `Handbook` · `Framework Guide` · `Academic Paper` · `Conference Paper` · `Magazine Issue` · `Chapter` · `Standard` · `Draft for Public Comment` · `Guidance Note` · `Technical Report` · `Code of Practice`

---

### Document type vocabulary

Semantic character — how to use it, independent of origin:

`Textbook` · `Practical Guide` · `Reference Manual` · `Case Studies` · `Theory` · `Standard` · `Draft for Public Comment` · `Code of Practice` · `Guidance Note` · `Technical Report` · `Magazine Issue` · `Chapter` · `Academic Paper` · `Workbook`

**Note:** `category` and `document_type` serve different purposes. A file can be `category = Guidance Note` and `document_type = Practical Guide` simultaneously.

---

### Audience vocabulary

`practitioner` · `executive` · `academic` · `consultant` · `general`

---

## Standards Worksheet (within `library-index.xlsx`)

The `Standards` worksheet is the only domain worksheet with enhanced headers. It holds engineering standards with additional engineering-specific columns beyond the standard 22. The `Master` sheet holds all rows with standard headers only.

**Implemented engineering columns (5):** `standard_code`, `status`, `jurisdiction`, `issuing_body`, `superseded_by` — these are defined in `workbook_utils.ENGINEERING_EXTRA_HEADERS` and present in every Standards row.

**Planned engineering columns (8):** `discipline`, `year_published`, `year_withdrawn`, `copyright`, `reproduction_permitted`, `citation_permitted`, `licence_verified`, `licence_notes` — not yet in `workbook_utils.py`. Add these to `ENGINEERING_EXTRA_HEADERS` before writing them to the workbook.

When indexing an engineering standard, populate the extra columns below in addition to the standard Master columns. Columns are grouped thematically.

**Identity**

| Column | Description | Example |
|---|---|---|
| `standard_code` | The designation printed on the document. For published standards: `AS/NZS 2865:2009`. For drafts: `DR 05564`. Never use the target standard code for a draft — index what the document *is*, not what it aspires to become | `DR 05564`, `AS/NZS 2865:2009`, `BS EN 1997-1:2004` |
| `issuing_body` | Standards body that authored the document (distinct from national distributor like SAI Global). For joint standards: semicolon-separated | `Standards Australia; Standards New Zealand`, `CEN`, `BSI` |
| `jurisdiction` | `UK` · `EU` · `NZ` · `AU` · `US` · `International`. Semicolon-separated when joint | `AU; NZ` |

**Identity — planned columns** *(not yet in workbook_utils.py)*

| Column | Description | Example |
|---|---|---|
| `discipline` | Engineering discipline. Controlled vocabulary: `geotechnical` · `structural` · `materials` · `materials testing` · `loading` · `seismic` · `environmental` · `plumbing` · `electrical` · `fire` · `occupational health and safety` · `quality` · `general`. See [reference/discipline-taxonomy.md](reference/discipline-taxonomy.md) for definitions | `occupational health and safety` |

**Temporal (validity window)** *(planned — not yet in workbook_utils.py)*

| Column | Description | Example |
|---|---|---|
| `year_published` | Year the standard came into force (integer). Do not parse from `standard_code` — populate explicitly | `2009` |
| `year_withdrawn` | Year the standard ceased being authoritative (integer, nullable). Blank = still current | `2023` |

**Currency chain**

| Column | Description | Example |
|---|---|---|
| `status` | `current` · `superseded` · `withdrawn` · `draft` · `needs_review` | `superseded` |
| `superseded_by` | Reference code of the replacing document; populate when `status = superseded` | `AS/NZS 2865:2023` |

**Copyright and licensing** *(planned — not yet in workbook_utils.py)*

| Column | Description | Example |
|---|---|---|
| `copyright` | Copyright classification. Controlled vocabulary — see [reference/copyright-lookup.md](reference/copyright-lookup.md) for definitions and decision rules | `proprietary` |
| `reproduction_permitted` | What can be done with the text. `none` · `clause-reference` · `partial-quote` · `full-with-licence` | `clause-reference` |
| `citation_permitted` | Whether the standard may be referenced by number and title. Boolean, default `TRUE` — referencing is always legally safe | `TRUE` |
| `licence_verified` | Has someone actually checked the licence terms? Boolean, default `FALSE`. Prevents assumptions becoming commitments | `FALSE` |
| `licence_notes` | Free text (nullable). Licence number, expiry, subscription tier, specific restrictions | `Single-user licence, purchased SAI Global 2024` |

**Rules:** Never leave `status` blank for any engineering standard. Use `needs_review` when currentness is unknown; do not default to `current` unless confirmed. When `status = needs_review`, add a `NEEDS_REVIEW` note and route currentness resolution to Graeme. When `status = superseded`, always populate `superseded_by` if known — flag to Graeme if unknown. When `year_withdrawn` is populated, `status` must be `superseded` or `withdrawn`. Non-standard engineering books (textbooks, guidance notes) leave all engineering-specific columns blank.

**Draft-handling rules (binding):**

1. **`standard_code`** = the designation printed on the document (e.g. `DR 05564`), never the target standard it proposes to become.
2. **`title`** = the title on *this* document, not a related published edition's title. Drafts and published editions often have different titles.
3. **`year`** and **`year_published`** = the year *this* document was issued (e.g. the commenting-period year), not the year the target standard was eventually published.
4. **`document_type`** = `Draft for Public Comment` (not `Standard`). `category` remains `Standard` (it is in the standards domain).
5. **`author`** = the technical committee (e.g. `Committee SF-037 — Work in Confined Spaces`), not the issuing body. The issuing body is already captured in `issuing_body`. For published standards, `author` is also the technical committee when identifiable; fall back to the issuing body only when the committee is unknown.
6. **`publisher`** = the national standards body (e.g. `Standards Australia; Standards New Zealand`), never a distributor/retailer (e.g. SAI Global).
7. **`notes`** must link the draft to its target standard and any related editions in the library (e.g. "Draft proposing revision of AS/NZS 2865:2001. See also source #120.").

---

## Metadata Enrichment for NZ/AU Standards

For standards issued by Standards Australia, Standards New Zealand, or jointly (AS, NZS, AS/NZS prefix), the SNZ catalogue scraper is the **primary metadata source**. PDF text extraction alone is unreliable for scanned standards and will miss canonical title and currentness.

**Required skill:** `python-testing-unit` (`.agents/skills/python-testing-unit/SKILL.md`) — follow TDD when extending the scraper or normaliser.

### Step-by-step workflow

1. **Normalise the code** from the filename using `normalise_standard_code` (`.agents/tools/library/naming_conventions.py`) to convert filename artefacts to a canonical query:
   ```python
   from naming_conventions import normalise_standard_code, strip_amendment_suffix
   canonical = strip_amendment_suffix(normalise_standard_code(raw_code))
   # e.g. "ASNZS 5667.4-1998" → "AS/NZS 5667.4:1998"
   # e.g. "ASNZS 9001-2008 [Amdt 1]" → "AS/NZS 9001:2008" (amendment stripped for query)
   ```

2. **Query the SNZ catalogue**:
   ```python
   from snz_scraper import get_snz_metadata, StandardNotFoundError, AmbiguousStandardError
   result = get_snz_metadata(canonical)
   # Populate: title = result.title, status = result.status.lower()
   ```

3. **If `StandardNotFoundError` or `AmbiguousStandardError`**: read the **first page** of the PDF to find the real standard code printed on the cover. Common causes and fixes:

   | Symptom | Likely cause | Fix |
   |---|---|---|
   | Digits run together (`56674`) | Missing decimal point (`5667.4`) | Add the dot |
   | Year before the dot (`5667.4-1998`) | Already canonical — check normaliser | Recheck input |
   | No SNZ entry at all | Non-SNZ standard (ISO, IEC, BS) | Fall back to manual |
   | Multiple editions returned | Year missing from filename | Find year on cover page |

   Correct the code and retry step 2.

4. **If still unresolvable** after reading the cover page: flag `NEEDS_REVIEW: SNZ lookup failed — verify code manually` in `notes` and proceed with whatever is printed on the cover.

5. **Rectify the filename** if the original filename did not match the resolved standard code: rename the file and update `path` and `canonical_filename` together. See [Canonical Filename Convention](#canonical-filename-convention).

### What the scraper populates

| Field | How to populate |
|---|---|
| `title` | `result.title` — always prefer over filename-derived title |
| `status` | `result.status.lower()` — `current` / `superseded` / `withdrawn` / `sponsored` |
| `standard_code` | Output of `normalise_standard_code` after confirmation |
| `issuing_body` | Inferred from prefix: `AS/NZS` → `Standards Australia; Standards New Zealand` |
| `jurisdiction` | Inferred from prefix: `AS/NZS` → `AU; NZ`; `NZS` only → `NZ`; `AS` only → `AU` |

### Scraper coverage

The SNZ scraper covers `standards.govt.nz` only (NZS, AS/NZS, AS prefixes). For ISO, IEC, BS EN, ASTM, or other non-SNZ standards, fall back to PDF text extraction and manual lookup. Future tools for other publishers will follow the same pattern and will be registered in `.agents/tools/library/`.

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
| Using filename as `title` for NZ/AU standards | Call `get_snz_metadata` first; filename is never the canonical title. |
| Leaving `status = needs_review` after a successful SNZ lookup | Populate `status` from `result.status.lower()` — the scraper resolves this. |
| Not renaming the file after a code correction | When the resolved code differs from the filename, rename and update `path` + `canonical_filename` together. |
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
