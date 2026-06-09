"""Protocols defining the document facade interface."""

from typing import Protocol


class DocumentFacade(Protocol):
    """Structural interface for document engines used by builder functions."""

    def add_heading(self, text: str, level: int) -> None:
        """Add a heading paragraph to the document.

        Args:
            text: Heading text content.
            level: Heading level (1 = top-level).
        """
        ...

    def add_table(self, rows: int, cols: int) -> int:
        """Insert an empty table and return its zero-based index.

        Args:
            rows: Number of rows.
            cols: Number of columns.

        Returns:
            Zero-based index of the newly added table.
        """
        ...

    def write_table_cell(self, table_index: int, row: int, col: int, text: str) -> None:
        """Write text into a specific table cell.

        Args:
            table_index: Zero-based index of the table (returned by add_table).
            row: Zero-based row index.
            col: Zero-based column index.
            text: Cell content.
        """
        ...

    def save(self, path: str) -> None:
        """Write the document to disk.

        Args:
            path: Destination file path.
        """
        ...

    def to_bytes(self) -> bytes:
        r"""Render the document to bytes without touching disk.

        Returns:
            Raw .docx bytes (ZIP/OOXML, starts with PK\x03\x04).
        """
        ...
