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

## Case B — No full book, only chapters in a subfolder

Merge the chapters into a single PDF, then delete the originals:

```powershell
.\.venv\Scripts\python.exe .agents\tools\library\merge_chapters.py `
    "G:\My Drive\Library\...\chapter-subfolder" `
    "G:\My Drive\Library\...\Merged-Title_Author_Year.pdf"
```

`merge_chapters.py` verifies the output is readable before removing the chapter files. If the merged PDF has 0 pages, the chapters are left intact.

---

## Case C — Chapters scattered in parent folder (no subfolder)

When chapter PDFs are downloaded directly into a parent folder alongside other books:

1. Create a temporary subfolder and move the chapter files into it:

```powershell
$base = "G:\My Drive\Library\...\<lcc-subfolder>"
$chapDir = "$base\<Title>-Chapters"
New-Item -ItemType Directory -Path $chapDir -Force | Out-Null
Get-ChildItem $base -Filter "<title-prefix>*.pdf" | Move-Item -Destination $chapDir
```

2. Run `merge_chapters.py` as in Case B:

```powershell
.\.venv\Scripts\python.exe .agents\tools\library\merge_chapters.py `
    "$chapDir" `
    "$base\<Canonical-Title_Author_Year>.pdf"
```

The chapter subfolder is automatically deleted after a successful merge.

---

## Chapter-only entries

If a single extracted chapter exists with no parent book and cannot be merged (no siblings), index it with `category = Chapter`.

---

After either case, proceed to Phase 1 indexing with the resulting file.
