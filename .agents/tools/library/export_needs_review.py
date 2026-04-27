"""Export NEEDS_REVIEW workbook rows to a CSV review queue."""

import csv
import pathlib
import sys

import openpyxl

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from workbook_utils import INDEX_PATH, LIBRARY_ROOT, get_header_indexes  # noqa: E402

REVIEW_QUEUE_PATH = LIBRARY_ROOT / "needs-review.csv"
EXPORT_HEADERS = ["path", "canonical_filename", "title", "year", "notes"]


def export_needs_review(
    *,
    index_path: pathlib.Path = INDEX_PATH,
    output_path: pathlib.Path = REVIEW_QUEUE_PATH,
    worksheet_name: str = "Master",
) -> int:
    """Write all NEEDS_REVIEW rows from a worksheet to CSV."""
    workbook = openpyxl.load_workbook(index_path, read_only=True, data_only=True)
    try:
        worksheet = workbook[worksheet_name]
        header_indexes = get_header_indexes(worksheet, EXPORT_HEADERS)
        rows = [
            _compose_export_row(row, header_indexes)
            for row in worksheet.iter_rows(min_row=2)
            if _row_needs_review(row, header_indexes)
        ]
    finally:
        workbook.close()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXPORT_HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def _compose_export_row(
    row: tuple[openpyxl.cell.cell.Cell, ...],
    header_indexes: dict[str, int],
) -> dict[str, object]:
    return {header: row[header_indexes[header]].value for header in EXPORT_HEADERS}


def _row_needs_review(
    row: tuple[openpyxl.cell.cell.Cell, ...],
    header_indexes: dict[str, int],
) -> bool:
    notes = row[header_indexes["notes"]].value
    return bool(notes and "NEEDS_REVIEW" in str(notes))


if __name__ == "__main__":
    exported = export_needs_review()
    print(f"Exported {exported} NEEDS_REVIEW rows to {REVIEW_QUEUE_PATH}")
