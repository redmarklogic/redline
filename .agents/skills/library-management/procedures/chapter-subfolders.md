# Procedure: Chapter Subfolder Handling

When a folder contains both a compiled full-book PDF **and** a subfolder of individual chapter PDFs, resolve the redundancy before indexing.

---

## Case A — Full book exists, chapters are redundant

Delete the chapter subfolder entirely:

```python
import shutil, pathlib
shutil.rmtree(pathlib.Path(r"G:\My Drive\Library\...\chapter-subfolder"))
```

---

## Case B — No full book, only chapters

Merge the chapters into a single PDF, then delete the originals:

```powershell
c:\Users\harel\Documents\products\redline\.venv\Scripts\python.exe .agents\tools\library\merge_chapters.py `
    "G:\My Drive\Library\...\chapter-subfolder" `
    "G:\My Drive\Library\...\Merged-Title_Author_Year.pdf"
```

`merge_chapters.py` verifies the output is readable before removing the chapter files. If the merged PDF has 0 pages, the chapters are left intact.

---

## Chapter-only entries

If a single extracted chapter exists with no parent book and cannot be merged (no siblings), index it with `category = Chapter`.

---

After either case, proceed to Phase 1 indexing with the resulting file.
