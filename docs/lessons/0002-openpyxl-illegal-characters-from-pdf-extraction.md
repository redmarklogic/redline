# 0002 — openpyxl rejects control characters extracted from PDFs

**Date**: 2026-04-25

**Skill**: `library-management` ([.agents/skills/library-management/SKILL.md](.agents/skills/library-management/SKILL.md))

**Context**: Batch-indexing 1473 PDF standards into `library-index.xlsx`. PDF text extraction via `pypdf` returns raw bytes that can include control characters (`\x00–\x1f`, `\x7f–\x9f`). When appending rows to a worksheet, openpyxl raises `IllegalCharacterError: <value> cannot be used in worksheets.` halting the entire batch without saving the completed rows.

**Root Cause**: The initial sanitization regex `[\x00-\x08\x0b\x0c\x0e-\x1f]` was too narrow — it missed the `\x7f–\x9f` range that openpyxl also rejects. The root error was not consulting openpyxl's actual illegal character definition before writing the regex.

**Principle**: Any string extracted from a PDF (via `pypdf`, `pdfminer`, OCR, etc.) must be sanitized against openpyxl's full illegal character set before writing to a worksheet. Use a regex that covers both ASCII control characters *and* the `\x7f–\x9f` range:

```python
import re
_ILLEGAL = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f\ud800-\udfff\uffff\ufffe]"
)

def sanitize(value: str | None) -> str | None:
    if value is None:
        return None
    return _ILLEGAL.sub("", value).strip() or None
```

Apply `sanitize()` to **every** string field in the row — not just the title — because illegal chars can appear in file paths, standard codes extracted from OCR, and notes fields.

**Source**: Session conversation, 2026-04-25 — batch_index_standards.py, batch 28 error
