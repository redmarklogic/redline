"""Tests for the chapter-merge tool (.agents/tools/library/merge_chapters.py)."""

import pathlib

import pypdf
import pytest


def _make_chapter_pdf(path: pathlib.Path, n_pages: int = 1) -> None:
    """Create a minimal PDF with n_pages blank pages."""
    writer = pypdf.PdfWriter()
    for _ in range(n_pages):
        writer.add_blank_page(width=612, height=792)
    with open(path, "wb") as f:
        writer.write(f)


@pytest.fixture
def chapter_folder(tmp_path: pathlib.Path) -> pathlib.Path:
    """Create a temp folder with 3 chapter PDFs."""
    folder = tmp_path / "chapters"
    folder.mkdir()
    _make_chapter_pdf(folder / "ch01.pdf", n_pages=2)
    _make_chapter_pdf(folder / "ch02.pdf", n_pages=3)
    _make_chapter_pdf(folder / "ch03.pdf", n_pages=1)
    return folder


class TestMergeChapters:
    """Tests for merge_chapters function."""

    def test_merges_all_pages(
        self, chapter_folder: pathlib.Path, tmp_path: pathlib.Path
    ) -> None:
        """Merged PDF should contain sum of all chapter pages."""
        import sys

        sys.path.insert(
            0,
            str(pathlib.Path(__file__).parent.parent / ".agents" / "tools" / "library"),
        )
        from merge_chapters import merge_chapters

        output = tmp_path / "merged.pdf"
        merge_chapters(chapter_folder, output)

        reader = pypdf.PdfReader(str(output))
        assert len(reader.pages) == 6  # 2 + 3 + 1

    def test_deletes_chapter_folder_after_merge(
        self, chapter_folder: pathlib.Path, tmp_path: pathlib.Path
    ) -> None:
        """Chapter folder should be removed after successful merge."""
        import sys

        sys.path.insert(
            0,
            str(pathlib.Path(__file__).parent.parent / ".agents" / "tools" / "library"),
        )
        from merge_chapters import merge_chapters

        output = tmp_path / "merged.pdf"
        merge_chapters(chapter_folder, output)

        assert not chapter_folder.exists()

    def test_sorts_chapters_alphabetically(self, tmp_path: pathlib.Path) -> None:
        """Chapters should be merged in sorted filename order."""
        import sys

        sys.path.insert(
            0,
            str(pathlib.Path(__file__).parent.parent / ".agents" / "tools" / "library"),
        )
        from merge_chapters import merge_chapters

        folder = tmp_path / "sorted_chapters"
        folder.mkdir()
        # Create with non-alphabetical filesystem order
        _make_chapter_pdf(folder / "C5.pdf", n_pages=5)
        _make_chapter_pdf(folder / "C1.pdf", n_pages=1)
        _make_chapter_pdf(folder / "C3.pdf", n_pages=3)

        output = tmp_path / "sorted_merged.pdf"
        merge_chapters(folder, output)

        reader = pypdf.PdfReader(str(output))
        # Total pages = 1 + 3 + 5 = 9
        assert len(reader.pages) == 9

    def test_aborts_if_output_exists(
        self, chapter_folder: pathlib.Path, tmp_path: pathlib.Path
    ) -> None:
        """Should exit with error if output path already exists."""
        import sys

        sys.path.insert(
            0,
            str(pathlib.Path(__file__).parent.parent / ".agents" / "tools" / "library"),
        )
        from merge_chapters import merge_chapters

        output = tmp_path / "existing.pdf"
        output.write_bytes(b"dummy")

        with pytest.raises(SystemExit):
            merge_chapters(chapter_folder, output)

    def test_aborts_if_no_pdfs(self, tmp_path: pathlib.Path) -> None:
        """Should exit with error if chapter folder has no PDFs."""
        import sys

        sys.path.insert(
            0,
            str(pathlib.Path(__file__).parent.parent / ".agents" / "tools" / "library"),
        )
        from merge_chapters import merge_chapters

        empty_folder = tmp_path / "empty"
        empty_folder.mkdir()
        output = tmp_path / "output.pdf"

        with pytest.raises(SystemExit):
            merge_chapters(empty_folder, output)
