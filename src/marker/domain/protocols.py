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

    def add_table(self, rows: int, cols: int) -> None:
        """Insert an empty table with the given dimensions.

        Args:
            rows: Number of rows.
            cols: Number of columns.
        """
        ...

    def save(self, path: str) -> None:
        """Write the document to disk.

        Args:
            path: Destination file path.
        """
        ...
