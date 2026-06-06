import pytest


class RecordingFacade:
    """Protocol-conforming fake that records facade calls without touching disk."""

    def __init__(self) -> None:
        """Initialise with empty recording state."""
        self.headings: list[tuple[str, int]] = []
        self.tables: list[tuple[int, int]] = []
        self.cell_writes: dict[tuple[int, int, int], str] = {}
        self.saved_to: str | None = None

    def add_heading(self, text: str, level: int) -> None:
        """Record a heading call.

        Args:
            text: Heading text.
            level: Heading level.
        """
        self.headings.append((text, level))

    def add_table(self, rows: int, cols: int) -> int:
        """Record a table creation and return its zero-based index.

        Args:
            rows: Number of rows.
            cols: Number of columns.

        Returns:
            Zero-based index of the newly added table.
        """
        self.tables.append((rows, cols))
        return len(self.tables) - 1

    def write_table_cell(self, table_index: int, row: int, col: int, text: str) -> None:
        """Record a cell write.

        Args:
            table_index: Zero-based table index.
            row: Zero-based row index.
            col: Zero-based column index.
            text: Cell content.
        """
        self.cell_writes[(table_index, row, col)] = text

    def save(self, path: str) -> None:
        """Record the save path.

        Args:
            path: Destination file path.
        """
        self.saved_to = path


@pytest.fixture
def recording_facade() -> RecordingFacade:
    """Return a fresh RecordingFacade instance."""
    return RecordingFacade()
