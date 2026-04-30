# Library Classification Reference

Two systems. Never mix them.

---

## Ebooks — Library of Congress Classification (LCC)

Folder structure: `G:\My Drive\Library\<LCC root>\<LCC subclass>\<filename>`  
Index columns: `lcc_class` (root) and `lcc_subclass` (subclass).

| LCC Root | LCC Subclass | Source domains / subdomains |
|---|---|---|
| B - Philosophy, Psychology, Religion | B - Philosophy (General) | Personal Development/philosophy; Intellectual |
| B - Philosophy, Psychology, Religion | BF - Psychology and Self-Improvement | Personal Development/psychology, self improvement, miscellaneous |
| B - Philosophy, Psychology, Religion | BL - Religion and Spirituality | Spiritual |
| G - Geography, Anthropology, Recreation | GV - Recreation and Games | Misc/Game Design |
| H - Social Sciences | HD - Management, Business and Leadership | Agile; Process Improvement; Stakeholder Engagement; Business Development (general); Professional Development; Design/Organisational Design |
| H - Social Sciences | HF - Commerce, Marketing and Sales | Business Development/B2B Sales, Product Pricing, RFP; Marketing; Job Interview |
| H - Social Sciences | HG - Finance | Personal Development/finance |
| Q - Science | QA - Mathematics and Statistics | Mathematics; Statistics |
| Q - Science | QA75-76 - Computer Science and Software Engineering | Software Craftsmanship; Data Engineering; AI Engineering; Data Science (general) |
| Q - Science | QA76.9 - User-Computer Interface (UI-UX) | Design/UI UX |
| T - Technology | T11 - Technical Writing and Communication | Writing |
| T - Technology | TA - Engineering Management and Professional Practice | Engineering/Business Professional Practice |
| T - Technology | TA1-348 - Civil Engineering (General) | Engineering/Civil Engineering, Reference, Engineering Reference |
| T - Technology | TA630-695 - Structural Engineering | Engineering/Structural Engineering |
| T - Technology | TA700-712 - Foundation and Geotechnical Engineering | Engineering/Geotechnical Engineering |
| T - Technology | TA715-787 - Earthwork, Excavations and Tunnelling | Engineering/Tunnelling |
| T - Technology | TC - Hydraulic and Ocean Engineering | Engineering/Water Resources, Water and Wastewater, Coastal & Marine |
| T - Technology | TD - Environmental Technology and Sanitary Engineering | Engineering/Environmental |
| Z - General Reference | Z - Bibliography, Library Science, Information Resources | 000 (catch-all); Knowledge Architecture; Dashboards; Data Science/Communication and Visualisation; Misc |

**Catch-all rule:** When no subclass clearly fits, use `Z - General Reference` / `Z - Bibliography, Library Science, Information Resources`.

---

## Standards — Issuing Body

Root: `G:\My Drive\Library\Engineering Standards\`  
Folder structure: `<Folder>\<official filename>`

| Folder | Issuing body in index | Notes |
|---|---|---|
| `ASTM` | ASTM International | |
| `AS-NZS` | Standards Australia/SNZ | Joint AU/NZ standards |
| `SNZ` | SNZ | New Zealand-only |
| `Standards Australia` | Standards Australia | Australia-only |
| `ISO` | ISO | |
| `BSI-CEN` | BSI · BSI/CEN | Merged: BS and BSEN folders combined |
| `DIN` | DIN | |
| `Local Authorities\Christchurch City Council` | Christchurch City Council | |
| `Local Authorities\Austroads` | Austroads | |
| `Local Authorities\Waka Kotahi NZTA` | Waka Kotahi NZTA | |
| `Local Authorities\Ministry of Health NZ` | Ministry of Health NZ | |
| `Local Authorities\Eco Choice Aotearoa` | Eco Choice Aotearoa | |
| `Local Authorities\ACENZ` | ACENZ | |
| `Industry Institutes\GRI` | GRI | |
| `Industry Institutes\DVS` | DVS | |
| `Industry Institutes\ACI` | ACI | |
| `Industry Institutes\ASCE` | ASCE | |
| `Industry Institutes\JSA` | JSA | Japanese Standards Association |
| `Industry Institutes\IEC` | IEC | |
| `Industry Institutes\VDI` | VDI | |
| `Industry Institutes\AWWA` | AWWA | |
| `Industry Institutes\AASHTO` | AASHTO | |
| `Industry Institutes\IEEE` | IEEE | |
| `Industry Institutes\ANSI` | ANSI | |
| `Industry Institutes\AACE International` | AACE International | |
| `Industry Institutes\API` | API | |
| `Industry Institutes\AFNOR` | AFNOR | |
| `Industry Institutes\ASME` | ASME | |
| `Industry Institutes\NFPA` | NFPA | |
| `Industry Institutes\Standard Norge` | Standard Norge | |
| `UNKNOWN` | None / unresolvable | Flag `NEEDS_REVIEW`; route to Graeme |

**Filename rule:** Never rename a standard to its title. Use the official code as the filename (e.g. `NZS 4402-1986.pdf`, `ASTM D4437.pdf`). Engineers search and cite by code, not title; audits require the specific code and year revision.

---

## Magazines — Periodicals (under subject class)

Root: `G:\My Drive\Library\T - Technology\TA700-712 - Foundation and Geotechnical Engineering\Serials & Periodicals\`

| Publication | Folder |
|---|---|
| Ground Engineering Magazine | `Serials & Periodicals\Ground Engineering Magazine\` |

Files are flat within the publication folder — no year subfolders needed. Files named `YYYY-MM.pdf` sort chronologically by OS without additional structure.

**Adding a new periodical:** Create a subfolder under `Serials & Periodicals\` using the publication's full name. Place all issues flat inside it. Add rows to the `Magazines` worksheet and `Master` with `path` pointing to the flat file location.
