# Library Management — Detailed Reference

### Inputs
- A folder path inside `<library-root>/` to scan, or a file to add
- Instructions to rename, deduplicate, or update entries

### Outputs
- Updated `library-index.xlsx` (both `Master` and domain worksheet)
- Files renamed on disk to the canonical convention
- Verification summary proving workbook integrity, row counts, duplicate sync, and review queues
- A summary of what changed

### Out of Scope
- Domain judgments (which notebook to add a book to — route to the domain agent)
- Deciding whether to keep superseded editions — flag in `notes`, route to the Domain Expert for engineering books
- Converting EPUB to PDF (flag, do not act without user confirmation)
- Deciding which duplicate copy to keep — flag, do not delete

### Prohibited Actions

- **NEVER write code.** the Knowledge Operator is an operator, not a developer. Do not create Python scripts, JSON data files, shell scripts, batch files, or any other executable or machine-readable code output — not even as a "helper file" or "script for the user to run". This is a hard, unconditional boundary.
- **If a user's request contains the words "write a script", "create a script", "write code", "generate a script", or any similar instruction to produce executable code:** refuse immediately, before asking any clarifying questions. State: "Writing code is outside my scope — I am an operator, not a developer. I am escalating this to the engineering agent tier." Then stop.
- Complete all tasks by invoking MCP tools and file operations directly (read, write, rename, move, update Excel).
- If a task cannot be completed without writing code, **stop immediately and escalate to the engineering agent tier**. State explicitly what capability is missing and why you cannot proceed without it.
- Do NOT create Python scripts or helper modules — use the approved tool at `.agents/tools/library/upsert_library_index.py` (see "Tool: upsert_library_index.py" section below for exact invocation).

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

### Invocation

```powershell
$payload = @'
{
  "index_path": "<library-root>/library-index.xlsx",
  "library_root": "<library-root>",
  "file_path": "<library-root>/Q - Science\\QA75-76 - Computer Science and Software Engineering\\Age of Invisible Machines_Wilson_2022.pdf",
  "worksheet": "Ebooks",
  "metadata": {
    "title": "Age of Invisible Machines",
    "author": "Wilson, Robb; Tyson, Josh",
    "publisher": "Wiley",
    "year": 2022,
    "edition": "",
    "domain": "Technology",
    "subdomain": "Artificial Intelligence",
    "lcc_class": "Q - Science",
    "lcc_subclass": "QA75-76 - Computer Science and Software Engineering",
    "category": "Book",
    "document_type": "Practitioner Text",
    "topics": "AI agents | orchestration | automation | conversational AI",
    "frameworks": "AI OS | multi-agent",
    "market_context": "",
    "audience": "practitioner",
    "skill_refs": "",
    "notes": ""
  }
}
'@
$payload | .venv\Scripts\python .agents/tools/library/upsert_library_index.py
```

### Required JSON keys

| Key | Required | Description |
|---|---|---|
| `index_path` | **Required** | Absolute path to `library-index.xlsx`. No default — always pass explicitly. |
| `file_path` | **Required** | Absolute path to the PDF or EPUB file on disk. |
| `worksheet` | **Required** | Target domain worksheet: `Ebooks`, `Standards`, `Magazines`, or `Misc`. |
| `metadata` | **Required** | Dict containing all metadata fields (see Index Schema above). |
| `library_root` | Optional | Absolute path to the library root. Defaults to parent directory of `index_path`. |

### Auto-derived fields

The tool automatically populates: `sha256`, `path` (relative to `library_root`), `canonical_filename`, `format`, `last_updated`. Do not include these in `metadata`.

### Idempotency

The relative `path` is the idempotency key. Calling the tool twice for the same file overwrites the existing row — it never creates a duplicate.

### Calling rules

- Always invoke via `.venv\Scripts\python` (not the system Python).
- Always pass `index_path` explicitly — there is no default.
- Check exit code: exits `1` with `ERROR:` on stderr if `index_path` is missing, the file is not found, or any other fatal condition occurs.

---

# Library Management

## Overview

The canonical digital library lives at `<library-root>`. All books are indexed in `<library-root>/library-index.xlsx` — this file is the single source of truth. Every operation must leave the index consistent before finishing.

---

## New Book Processing — Mandatory Sequence

**Every new PDF or EPUB that arrives in the library — whether dropped in the root of `<library-root>` or any temporary landing zone — must follow this four-step sequence in order. No step may be skipped or deferred.**

1. **Move** the file from the root of `<library-root>` (or its temporary landing location) into the correct LCC subfolder (e.g., `<library-root>/T - Technology\TA700-712 - Foundation and Geotechnical Engineering\`). If the correct subfolder is ambiguous, route the domain classification decision to the relevant domain agent before proceeding — do not move the file until the destination is confirmed.
2. **Rename** the file to the canonical convention: `Full-Title_FirstAuthorSurname_Year.pdf` (see [Canonical Filename Convention](#canonical-filename-convention)).
3. **Index** the file in `<library-root>/library-index.xlsx` using the incremental add workflow (see [Incremental Add Workflow](#incremental-add-workflow)). Run post-index verification before proceeding.
4. **Upload** to the appropriate NotebookLM notebook using the `notebooklm-mcp` skill.

> **Hard stop:** Step 4 (NotebookLM upload) is blocked until steps 1, 2, and 3 are complete and verified. Uploading a file before it is correctly placed, renamed, and indexed leaves the library in an inconsistent state — the notebook will reference a path or filename that does not match the index, and the error cannot be corrected retroactively without re-ingesting.

---

## Index Schema

File: `<library-root>/library-index.xlsx`
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
| `path` | Path relative to `<library-root>/` (no drive letter) |
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

**Rules:** Never leave `status` blank for any engineering standard. Use `needs_review` when currentness is unknown; do not default to `current` unless confirmed. When `status = needs_review`, add a `NEEDS_REVIEW` note and route currentness resolution to the Domain Expert. When `status = superseded`, always populate `superseded_by` if known — flag to the Domain Expert if unknown. When `year_withdrawn` is populated, `status` must be `superseded` or `withdrawn`. Non-standard engineering books (textbooks, guidance notes) leave all engineering-specific columns blank.

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
| 5 — Review/enrichment | Resolve `NEEDS_REVIEW` rows and standards currentness | Browser/the Domain Expert approval required |

**Workbook lock:** writer tools use `workbook_utils.WorkbookLock`, which creates `library-index.xlsx.lock` beside the workbook. A second writer must fail fast. Remove the lock only after confirming no Python indexer process is still running.

For chapter subfolders, see [procedures/chapter-subfolders.md](procedures/chapter-subfolders.md).

---

## Adding a Single New Book

Use the `upsert_library_index.py` tool (see [Tool: upsert_library_index.py](#tool-upsert_library_indexpy) below). The `procedures/add-single-book.md` procedure describes the full contextual workflow; the tool handles the workbook write step.

---

## Tool: upsert_library_index.py

**Script:** `.agents/tools/library/upsert_library_index.py`

Accepts a JSON payload on stdin and upserts one book entry into both the `Master` worksheet and the target domain worksheet of a `library-index.xlsx` workbook. Handles SHA-256 derivation, relative path, canonical filename, format, and `last_updated` automatically.

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
| `upsert_library_index.py` | Upsert a single book row into Master and domain worksheet; accepts JSON payload on stdin; path-agnostic |

---
