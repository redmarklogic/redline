# Index Schema Reference

File: `G:\My Drive\Library\library-index.xlsx`

Worksheets: `Master` (all entries) + four domain worksheets: `Ebooks`, `Standards`, `Magazines`, `Misc`.  
Only `Standards` has extra engineering columns.

---

## Standard Columns (all worksheets)

| Column | Description |
|---|---|
| `sha256` | SHA-256 hash — used to detect duplicates only |
| `title` | Full title including meaningful subtitle |
| `author` | All authors, semicolon-separated. Format: `Surname, Firstname` |
| `publisher` | Publisher or national distributor |
| `year` | Year of publication (integer) |
| `edition` | Edition number only (e.g. `3rd`). Standards codes go in `standard_code`. |
| `format` | `PDF` or `EPUB` |
| `path` | Path relative to `G:\My Drive\Library\` (no drive letter) — **resume key** |
| `canonical_filename` | Filename only, in canonical convention |
| `domain` | Top-level folder name |
| `subdomain` | Sub-folder name |
| `lcc_class` | LCC root letter group (ebooks only) |
| `lcc_subclass` | LCC number-range subclass (ebooks only) |
| `category` | Origin type (see vocabulary below) |
| `document_type` | Semantic character (see vocabulary below) |
| `topics` | 3–8 thematic tags, semicolon-separated |
| `frameworks` | Named methodologies or models, semicolon-separated |
| `market_context` | Industries or segments the book addresses, semicolon-separated |
| `audience` | Primary intended reader (see vocabulary below) |
| `skill_refs` | Auto-generated — never populate manually |
| `notes` | Administrative flags only: `DUPLICATE of <path>`, `SUPERSEDED`, `NEEDS_REVIEW`, licensing |
| `last_updated` | ISO date (`YYYY-MM-DD`) |

---

## Standards Extra Columns (`Standards` worksheet only)

| Column | Description | Example |
|---|---|---|
| `standard_code` | Official reference designation engineers cite | `BS EN 1997-1:2004`, `NZS 4402:1986` |
| `status` | `current` · `superseded` · `withdrawn` · `draft` · `needs_review` | |
| `jurisdiction` | `UK` · `EU` · `NZ` · `AU` · `US` · `International` | |
| `issuing_body` | Standards body that authored the document (not the national distributor) | `CEN`, `BSI`, `CIRIA` |
| `superseded_by` | Reference code of the replacing document; populate when `status = superseded` | `BS EN 1997-1:2013` |

**Rules:**
- Never leave `status` blank. Use `needs_review` when currentness is unknown.
- Never default to `current` unless confirmed.
- When `status = superseded`, populate `superseded_by` if known; flag to Graeme if unknown.
- Non-standard engineering books leave all five columns blank.

---

## Vocabulary

### `domain` and `subdomain`

`domain` = LCC root folder name. `subdomain` = LCC subclass folder name. The physical folder structure on disk is `<domain>\<subdomain>\<filename>`.

Refer to `.agents/skills/library-management/reference/classification.md` for the authoritative LCC class table.

| `domain` example | `subdomain` example | Typical content |
|---|---|---|
| `H - Social Sciences` | `HD - Management, Business and Leadership` | Strategy, management, entrepreneurship |
| `H - Social Sciences` | `HF - Commerce, Marketing and Sales` | Marketing, branding, sales |
| `Q - Science` | `QA75-76 - Computer Science and Software Engineering` | AI, software, data science |
| `T - Technology` | `TA700-712 - Foundation and Geotechnical Engineering` | Geotechnical engineering |
| `T - Technology` | `TA - Engineering Management and Professional Practice` | Professional practice |

### `category` (origin type)

`Book` · `Handbook` · `Framework Guide` · `Academic Paper` · `Conference Paper` · `Magazine` · `Chapter` · `Standard` · `Guidance Note` · `Technical Report` · `Code of Practice`

### `document_type` (semantic character)

`Textbook` · `Practical Guide` · `Reference Manual` · `Case Studies` · `Theory` · `Standard` · `Code of Practice` · `Guidance Note` · `Technical Report` · `Magazine Issue` · `Chapter` · `Academic Paper` · `Workbook`

`category` and `document_type` serve different purposes. A file can have `category = Guidance Note` and `document_type = Practical Guide` simultaneously.

### `audience`

`practitioner` · `executive` · `academic` · `consultant` · `general`
