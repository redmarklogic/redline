"""Chapter merger — Phase 0 helper when no full-book PDF exists.

Usage
-----
    .venv\\Scripts\\python.exe .agents\\tools\\library\\merge_chapters.py <chapter_folder> <output_pdf>

Example
-------
    .venv\\Scripts\\python.exe .agents\\tools\\library\\merge_chapters.py \
        "G:\\My Drive\\Library\\Engineering\\Geotechnical Engineering\\Foundations\\Correlations for Soil Properties" \\
        "G:\\My Drive\\Library\\Engineering\\Geotechnical Engineering\\Foundations\\Correlations-for-Soil-Properties_Bowles_1984.pdf"

The script:
  - Merges all *.pdf files in <chapter_folder> in sorted name order.
  - Verifies the merged PDF is readable (non-zero page count) before deleting sources.
  - Removes the chapter folder after a successful merge.
  - Exits with an error message (no deletion) if the output PDF is unreadable.
"""

import pathlib
import shutil
import sys

import pypdf


def merge_chapters(chapter_folder: pathlib.Path, output_path: pathlib.Path) -> None:
    """Merge all chapter PDFs in a folder into a single output PDF.

    Verifies the merged PDF is readable before deleting source files
    and the chapter folder.

    Args:
        chapter_folder: Directory containing chapter PDF files.
        output_path: Destination path for the merged PDF.
    """
    if output_path.exists():
        print(
            f"ERROR: output path already exists — aborting to prevent overwrite: {output_path}"
        )
        sys.exit(1)

    chapters = sorted(chapter_folder.glob("*.pdf"))
    if not chapters:
        print(f"ERROR: no PDFs found in {chapter_folder}")
        sys.exit(1)

    writer = pypdf.PdfWriter()
    for chapter in chapters:
        reader = pypdf.PdfReader(str(chapter))
        for page in reader.pages:
            writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"Merged {len(chapters)} chapters -> {output_path.name}")

    # Verify before deleting sources
    check = pypdf.PdfReader(str(output_path))
    if len(check.pages) == 0:
        print("ERROR: merged PDF has 0 pages — chapter files NOT deleted")
        sys.exit(1)

    shutil.rmtree(chapter_folder)
    print(f"Deleted chapter folder: {chapter_folder.name}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: merge_chapters.py <chapter_folder> <output_pdf>")
        sys.exit(1)
    merge_chapters(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))
