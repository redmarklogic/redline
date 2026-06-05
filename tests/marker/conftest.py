import pytest


class RecordingFacade:
    """Protocol-conforming fake that records facade calls without touching disk."""

    def __init__(self) -> None:
        self.headings: list[tuple[str, int]] = []
        self.tables: list[tuple[int, int]] = []
        self.saved_to: str | None = None

    def add_heading(self, text: str, level: int) -> None:
        self.headings.append((text, level))

    def add_table(self, rows: int, cols: int) -> None:
        self.tables.append((rows, cols))

    def save(self, path: str) -> None:
        self.saved_to = path


@pytest.fixture
def recording_facade() -> RecordingFacade:
    return RecordingFacade()
