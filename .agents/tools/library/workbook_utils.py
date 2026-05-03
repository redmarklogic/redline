"""Shared helpers for maintaining the digital-library workbook."""

from pathlib import Path
from types import TracebackType
from typing import Protocol, Self, TextIO
from uuid import uuid4

import openpyxl

LIBRARY_ROOT = Path(r"G:\My Drive\Library")
INDEX_PATH = LIBRARY_ROOT / "library-index.xlsx"

STANDARD_HEADERS = [
    "sha256",
    "title",
    "author",
    "publisher",
    "year",
    "edition",
    "format",
    "path",
    "canonical_filename",
    "domain",
    "subdomain",
    "lcc_class",
    "lcc_subclass",
    "category",
    "document_type",
    "topics",
    "frameworks",
    "market_context",
    "audience",
    "skill_refs",
    "notes",
    "last_updated",
]

ENGINEERING_EXTRA_HEADERS = [
    "standard_code",
    "status",
    "jurisdiction",
    "issuing_body",
    "superseded_by",
]

DOMAIN_WORKSHEETS = ["Ebooks", "Standards", "Magazines", "Misc"]
ENHANCED_WORKSHEETS = ["Standards"]


class WorkbookSaver(Protocol):
    """Object that can save itself to an XLSX file path."""

    def save(self, filename: str | Path) -> None:
        """Save the workbook to filename."""


class WorkbookLock:
    """Exclusive lock file for one-writer workbook updates."""

    def __init__(self, index_path: Path) -> None:
        self.index_path = Path(index_path)
        self.lock_path = self.index_path.with_name(f"{self.index_path.name}.lock")
        self._handle: TextIO | None = None

    def __enter__(self) -> Self:
        try:
            self._handle = self.lock_path.open("x", encoding="utf-8")
        except FileExistsError as exc:
            message = (
                "Another library index writer is active. "
                f"Remove the lock only after confirming no writer is running: {self.lock_path}"
            )
            raise RuntimeError(message) from exc
        self._handle.write("locked\n")
        self._handle.flush()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._handle is not None:
            self._handle.close()
        self.lock_path.unlink(missing_ok=True)


def save_workbook_atomically(workbook: WorkbookSaver, target_path: Path) -> None:
    """Save a workbook through a temporary file before replacing the target."""
    target_path = Path(target_path)
    temp_path = target_path.with_name(f".{target_path.name}.{uuid4().hex}.tmp.xlsx")
    try:
        workbook.save(temp_path)
        temp_path.replace(target_path)
    finally:
        temp_path.unlink(missing_ok=True)


def append_index_row(
    workbook: openpyxl.Workbook,
    domain_worksheet: str,
    row: list[object],
) -> None:
    """Append one physical file row to Master and the matching domain worksheet."""
    workbook["Master"].append(row[: len(STANDARD_HEADERS)])
    workbook[domain_worksheet].append(row)


def get_indexed_paths(workbook: openpyxl.Workbook) -> set[str]:
    """Return relative paths already present in the Master worksheet."""
    worksheet = workbook["Master"]
    header_indexes = get_header_indexes(worksheet, ["path"])
    path_idx = header_indexes["path"]
    return {
        str(row[path_idx].value)
        for row in worksheet.iter_rows(min_row=2)
        if row[path_idx].value
    }


def sync_domain_notes_by_path(
    workbook: openpyxl.Workbook,
    notes_by_path: dict[str, str],
) -> int:
    """Copy notes from Master-derived rows into domain worksheets using path as key."""
    synced = 0
    for worksheet in workbook.worksheets:
        if worksheet.title == "Master":
            continue
        try:
            header_indexes = get_header_indexes(worksheet, ["path", "notes"])
        except ValueError:
            continue
        path_idx = header_indexes["path"]
        notes_idx = header_indexes["notes"]
        for row in worksheet.iter_rows(min_row=2):
            row_path = str(row[path_idx].value) if row[path_idx].value else ""
            new_note = notes_by_path.get(row_path)
            if new_note and row[notes_idx].value != new_note:
                row[notes_idx].value = new_note
                synced += 1
    return synced


def get_header_indexes(
    worksheet: openpyxl.worksheet.worksheet.Worksheet,
    required_headers: list[str],
) -> dict[str, int]:
    """Return zero-based header indexes for required worksheet columns."""
    headers = [cell.value for cell in worksheet[1]]
    missing_headers = sorted(set(required_headers) - set(headers))
    if missing_headers:
        message = f"Worksheet {worksheet.title} is missing headers: {', '.join(missing_headers)}"
        raise ValueError(message)
    return {header: headers.index(header) for header in required_headers}
