"""Export the full review-queue pack from the digital-library workbook."""

import csv
import pathlib
import sys

import openpyxl

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from workbook_utils import INDEX_PATH, LIBRARY_ROOT, get_header_indexes  # noqa: E402

REVIEW_QUEUE_DIR = LIBRARY_ROOT / "review-queues"
EXPORT_HEADERS = ["path", "canonical_filename", "title", "year", "notes"]


def export_review_pack(
    *,
    index_path: pathlib.Path = INDEX_PATH,
    output_dir: pathlib.Path = REVIEW_QUEUE_DIR,
) -> dict[str, int]:
    """Export the full review-queue pack as multiple CSV files."""
    workbook = openpyxl.load_workbook(index_path, read_only=True, data_only=True)
    try:
        master = workbook["Master"]
        header_indexes = get_header_indexes(master, [*EXPORT_HEADERS, "sha256"])
        all_rows = list(master.iter_rows(min_row=2))

        needs_review_all = [r for r in all_rows if _has_needs_review(r, header_indexes)]
        standards = [r for r in needs_review_all if _is_standard(r, header_indexes)]
        non_standards = [
            r for r in needs_review_all if not _is_standard(r, header_indexes)
        ]
        missing_year = [r for r in all_rows if _is_missing_year(r, header_indexes)]
        duplicates = [r for r in all_rows if _is_duplicate(r, header_indexes)]
    finally:
        workbook.close()

    output_dir.mkdir(parents=True, exist_ok=True)

    counts = {
        "needs-review-all": _write_csv(
            output_dir / "needs-review-all.csv", needs_review_all, header_indexes
        ),
        "needs-review-standards": _write_csv(
            output_dir / "needs-review-standards.csv", standards, header_indexes
        ),
        "needs-review-non-standards": _write_csv(
            output_dir / "needs-review-non-standards.csv", non_standards, header_indexes
        ),
        "needs-review-missing-year": _write_csv(
            output_dir / "needs-review-missing-year.csv", missing_year, header_indexes
        ),
        "duplicates": _write_csv(
            output_dir / "duplicates.csv", duplicates, header_indexes
        ),
    }
    return counts


def _write_csv(
    path: pathlib.Path,
    rows: list[tuple[openpyxl.cell.cell.Cell, ...]],
    header_indexes: dict[str, int],
) -> int:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXPORT_HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row[header_indexes[h]].value for h in EXPORT_HEADERS})
    return len(rows)


def _has_needs_review(
    row: tuple[openpyxl.cell.cell.Cell, ...],
    header_indexes: dict[str, int],
) -> bool:
    notes = row[header_indexes["notes"]].value
    return bool(notes and "NEEDS_REVIEW" in str(notes))


def _is_standard(
    row: tuple[openpyxl.cell.cell.Cell, ...],
    header_indexes: dict[str, int],
) -> bool:
    path = str(row[header_indexes["path"]].value or "")
    return "Engineering/Standards/" in path


def _is_missing_year(
    row: tuple[openpyxl.cell.cell.Cell, ...],
    header_indexes: dict[str, int],
) -> bool:
    return row[header_indexes["year"]].value in (None, "")


def _is_duplicate(
    row: tuple[openpyxl.cell.cell.Cell, ...],
    header_indexes: dict[str, int],
) -> bool:
    notes = row[header_indexes["notes"]].value
    return bool(notes and "DUPLICATE of" in str(notes))


if __name__ == "__main__":
    result = export_review_pack()
    for name, count in result.items():
        print(f"{name}: {count}")
