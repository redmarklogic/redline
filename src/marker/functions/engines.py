"""Concrete document engine implementations."""

from pathlib import Path

from docx import Document as DocxDocument


class PythonDocxFacade:
    """python-docx backed implementation of DocumentFacade."""

    def __init__(self, template: Path | None = None) -> None:
        """Initialise a new document, optionally from a template.

        Args:
            template: Path to an existing .docx template file. When omitted,
                a blank document is created.
        """
        if template is not None:
            self._doc = DocxDocument(str(template))
        else:
            self._doc = DocxDocument()

    def add_heading(self, text: str, level: int) -> None:
        """Add a heading paragraph to the document.

        Args:
            text: Heading text content.
            level: Heading level (1 = top-level).
        """
        self._doc.add_heading(text, level=level)

    def add_table(self, rows: int, cols: int) -> None:
        """Insert an empty table with the given dimensions.

        Args:
            rows: Number of rows.
            cols: Number of columns.
        """
        self._doc.add_table(rows=rows, cols=cols)

    def save(self, path: str) -> None:
        """Write the document to disk.

        Args:
            path: Destination file path.
        """
        self._doc.save(path)
