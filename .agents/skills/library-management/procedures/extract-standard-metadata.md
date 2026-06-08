# Extract Standard Metadata from NotebookLM

Procedure for extracting structured metadata from engineering standards uploaded to a NotebookLM notebook. Uses `nlm notebook query` scoped to individual sources — not `nlm source describe`.

## Prerequisites

- NotebookLM notebook ID containing uploaded standards
- Source list retrieved via `nlm source list` (need source IDs)
- **Skills required:** `rag-prompting` (structured extraction), `notebooklm-mcp` (CLI access)

## Why `nlm notebook query`, not `nlm source describe`

`nlm source describe` is a summarisation tool — it conflates drafts with published editions, uses wrong titles, and misses precise metadata (committee IDs, DR prefixes, exact years). `nlm notebook query` with a structured extraction prompt gets the precise fields we need by asking the model to quote verbatim from the title page.

## Extraction Prompt

Use this prompt verbatim with `nlm notebook query`, scoped to one source at a time via `--source-ids <source-id>`.

```
Explain for the uninitiated. Define any specialist term the first time
it appears. Keep citations. Avoid ambiguity.

You are examining a single uploaded document (an engineering standard or
draft standard). Extract metadata from the TITLE PAGE, FOREWORD, and
PREFACE of this document only. Do not infer metadata from other
documents referenced in the body text.

CRITICAL DISTINCTION: Report what this document IS, not what it
references. If this is a draft (DR, DPC), report the draft designation
— not the target standard it proposes to become.

AMENDMENT DETECTION: If the filename, title page, or document header
contains "Amendment", "Amdt", "Amd", or "A1"/"A2"/etc., check
whether this is a STANDALONE amendment or a CONSOLIDATED reissue:

- STANDALONE AMENDMENT: A short change-sheet or errata document that
  modifies specific clauses of a base standard. The title page will
  say "Amendment No. 1" without "Incorporating". Set
  `document_status` to "amendment" and populate `amends`.
- CONSOLIDATED REISSUE: The full base standard republished with
  amendments folded into the text. The title page will say
  "Incorporating Amendment No. 1", "Reissued incorporating
  Amendment", or similar. This is NOT an amendment — it is the base
  standard. Set `document_status` to "published", leave `amends` as
  "N/A", and record the incorporated amendment in
  `incorporated_amendments`.

Do NOT report the base standard's metadata as if this were an
amendment. Only set `document_status` to "amendment" for standalone
amendment documents.

CURRENTNESS: Do NOT attempt to determine whether a standard is
"current" or "superseded". Report `document_status` as what the
document itself states: "draft" for drafts, "amendment" for
amendments, "published" for published standards. Supersession is
determined post-extraction, not by the model.

HANDBOOK DESIGNATION: Distinguish published Handbooks (HB prefix)
from drafts. If `standard_code` is "HB <number>:<year>" or the
document starts with "HB" (e.g., "HB 89:2011"), this is a published
Handbook — NOT a draft. Handbooks have "DRAFT ONLY" or "NOT
NORMATIVE" in their footer as a formatting convention (they are
guidance, not requirements). This does NOT mean they are
pre-publication drafts. Only mark `document_status` as "draft" if: <!-- hook: allow -->
(1) `standard_code` starts with "DR" (e.g., "DR 05564"), OR
(2) the document explicitly says "Draft for Public Comment" with a
comment deadline. If `standard_code` is "HB" or "AS/NZS" (no "DR"
prefix), set `document_status` to "published" regardless of footer
text.

OUTPUT FORMAT (CRITICAL — TDD refined):
Your response MUST be raw JSON with NO wrapping.

**WHAT TO DO:**
- Response starts with { (left brace)
- Response ends with } (right brace)
- Response is valid JSON
- Nothing before the {. Nothing after the }.

**WHAT NOT TO DO (DO NOT violate):**
- DO NOT wrap in markdown code fences (```)
- DO NOT start with ```json or ```
- DO NOT end with ```
- DO NOT include explanations or preamble
- DO NOT write any text after closing }

**EXAMPLES:**
- RIGHT: { "standard_code": "AS/NZS 1170.2:2021", ... }
- WRONG: ```json { ... } ```
- WRONG: Here is the JSON: { ... }

SCHEMA:
- "standard_code":    [String]  The full designation printed on the
                      title page, including any DR/DPC/amendment prefix
                      and year suffix. E.g. "DR 05564", "AS/NZS 2865:2009",
                      "BS EN 1997-1:2004+A1:2013".
- "title":            [String]  The full title as printed on the title
                      page of THIS document. Do not use a different
                      edition's title.
- "year_published":   [Integer] The year this document was published or
                      issued. For drafts, use the year of the commenting
                      period. Do not use the year the target standard
                      was eventually published.
- "committee":        [String]  The technical committee identifier and
                      name, e.g. "Committee SF-037 — Work in Confined
                      Spaces". Quote exactly as printed.
- "issuing_body":     [String]  The standards body or bodies that
                      authored this document. Semicolon-separated if
                      joint. E.g. "Standards Australia; Standards
                      New Zealand". Never list a distributor like
                      SAI Global.
- "jurisdiction":     [Enum]    Exactly one or more of: "AU", "NZ",
                      "UK", "EU", "US", "International".
                      Semicolon-separated if joint. E.g. "AU; NZ".
- "document_status":  [Enum]    Exactly one of: "published", "draft",
                      "amendment".
                      Use "published" for any published standard.
                      Use "draft" for DR/DPC documents.
                      Use "amendment" for amendment documents.
                      Do NOT use "current" or "superseded" — those
                      are determined post-extraction.
- "amends":           [String]  Only for standalone amendments: the
                      base standard code this amendment modifies.
                      E.g. "AS/NZS 1170.2:2021". Use "N/A" if not
                      a standalone amendment.
- "incorporated_amendments": [String]  Only for consolidated reissues:
                      list of amendment numbers incorporated. E.g.
                      "Amdt 1 (2020)". Use "N/A" if no amendments
                      incorporated.
- "supersedes":       [String]  The standard this document replaces, if
                      stated in the foreword. E.g. "AS/NZS 2865:2001".
- "scope_summary":    [String]  One-sentence summary of the document's
                      scope section.
- "discipline":       [Enum]    Exactly one of the following. Choose
                      based on the DEFINITIONS below, not by
                      inferring from what the material is used for:
                      "geotechnical" — ground investigation,
                        foundation design, earthworks, retaining
                      "structural" — design of structural elements
                        (beams, columns, slabs, connections)
                      "materials" — material product specifications
                        (steel, concrete, timber grades/properties)
                      "materials testing" — test methods for
                        materials (tensile, compressive, chemical)
                      "loading" — actions on structures (dead, live,
                        wind, snow, combinations)
                      "seismic" — earthquake design and actions
                      "environmental" — environmental management,
                        contamination, noise, air quality
                      "plumbing" — water services, drainage,
                        sanitary plumbing, gas fitting
                      "electrical" — electrical installations,
                        wiring rules, hazardous areas
                      "fire" — fire resistance, fire safety systems,
                        fire testing
                      "occupational health and safety" — workplace
                        safety, confined spaces, PPE, hazardous
                        substances
                      "quality" — quality management systems,
                        auditing, risk management
                      "general" — does not fit any above category.
- "topics":           [String]  3-8 key terms a practitioner would
                      search for, semicolon-separated.
- "verbatim_evidence": [String] Quote the exact text from the title
                      page or foreword that contains the standard
                      designation, year, and committee. This is for
                      audit — quote verbatim, do not paraphrase.

MISSING VALUES: Use "N/A" for strings, null for integers.

EXAMPLE (draft):
{"standard_code": "DR 05564", "title": "Confined spaces", "year_published": 2005, "committee": "Committee SF-037 — Work in Confined Spaces", "issuing_body": "Standards Australia; Standards New Zealand", "jurisdiction": "AU; NZ", "document_status": "draft", "amends": "N/A", "incorporated_amendments": "N/A", "supersedes": "AS/NZS 2865:2001", "scope_summary": "Safety requirements for identifying, entering, and working in confined spaces.", "discipline": "occupational health and safety", "topics": "confined spaces; entry permit; atmospheric testing; gas detection; ventilation; rescue procedures; isolation", "verbatim_evidence": "COMMITTEE SF-037 DR 05564 (Project ID: 6248) Draft for Public Comment"}

EXAMPLE (standalone amendment — a short change-sheet, NOT the full standard):
{"standard_code": "AS/NZS 1170.2:2021/Amdt 1:2023", "title": "Structural design actions Part 2: Wind actions — Amendment 1", "year_published": 2023, "committee": "Joint Technical Committee BD-006", "issuing_body": "Standards Australia; Standards New Zealand", "jurisdiction": "AU; NZ", "document_status": "amendment", "amends": "AS/NZS 1170.2:2021", "incorporated_amendments": "N/A", "supersedes": "N/A", "scope_summary": "Amendment to wind action provisions in AS/NZS 1170.2:2021.", "discipline": "loading", "topics": "wind actions; amendment; structural design", "verbatim_evidence": "Amendment 1 to AS/NZS 1170.2:2021"}

EXAMPLE (consolidated reissue — full standard republished with amendments folded in):
{"standard_code": "AS/NZS 3000:2018", "title": "Electrical installations", "year_published": 2018, "committee": "Joint Technical Committee EL-001, Wiring Rules", "issuing_body": "Standards Australia; Standards New Zealand", "jurisdiction": "AU; NZ", "document_status": "published", "amends": "N/A", "incorporated_amendments": "Amdt 1 (2020)", "supersedes": "AS/NZS 3000:2007", "scope_summary": "Requirements for design, construction and verification of electrical installations.", "discipline": "electrical", "topics": "electrical installations; wiring rules; earthing; overcurrent protection", "verbatim_evidence": "AS/NZS 3000:2018 Reissued incorporating Amendment No. 1 (January 2020)"}

Answer only using information found in this source document.
If a field cannot be determined from the title page, foreword, or
preface, use the missing-value sentinel. Do not guess.
```

## Workflow

1. **List sources** — call `nlm source list` to get all source IDs and filenames.
2. **Loop per source** — for each source, run `nlm notebook query <notebook-id> "<prompt>" --source-ids <source-id>` to scope the query to that one source.
3. **Parse JSON** — extract the JSON object from the response.
4. **Preserve raw response** — store the full `nlm notebook query` response alongside the parsed fields for audit.
5. **Map to worksheet columns** — align extracted fields to the Standards worksheet schema:

   | Extracted field | Worksheet column |
   |---|---|
   | `standard_code` | `standard_code` |
   | `title` | `title` (standard 20) |
   | `year_published` | `year_published` AND `year` (standard 20) |
   | `committee` | `author` (standard 20) |
   | `issuing_body` | `issuing_body` AND `publisher` (standard 20) |
   | `jurisdiction` | `jurisdiction` |
   | `document_status` | `status` (map: `"published"` -> `"needs_review"`, `"draft"` -> `"draft"`, `"amendment"` -> `"current"` with note). Supersession derived post-extraction |
   | `amends` | *(informational — links amendment to base standard)* |
   | `supersedes` | *(informational — the reverse of `superseded_by`)* |
   | `scope_summary` | *(used to populate `topics` if extraction incomplete)* |
   | `discipline` | `discipline` |
   | `topics` | `topics` (standard 20) |
   | `verbatim_evidence` | *(audit trail — not stored in worksheet)* |

6. **Flag unknowns** — any field with `"N/A"` or `null` gets `NEEDS_REVIEW` in `notes` and is routed to the Domain Expert.
7. **Copyright defaults** — apply the copyright lookup table decision flow. Most purchased standards: `copyright = proprietary`, `reproduction_permitted = clause-reference`, `licence_verified = FALSE`.
8. **the Domain Expert review** — send the full batch output to the Domain Expert for domain review before writing to the worksheet.

## Pilot Protocol

Before scaling to all sources:

1. Select 5-10 sources spanning different types (published standard, draft, amendment, different disciplines).
2. Run the extraction prompt on each.
3. Present results to the Domain Expert in a comparison table.
4. Calibrate the prompt based on error patterns.
5. Scale to full batch only after the Domain Expert approves.
