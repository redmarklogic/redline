r"""Deduplication pass — Phase 3 of the folder indexing workflow.

Run after all files are indexed and renamed:

    .\.venv\Scripts\python.exe .agents\tools\library\dedup_index.py

Groups all rows in the Master worksheet by sha256. Flags the second+ occurrence
of each hash with "DUPLICATE of <path>" in the notes column. Does not delete files.
"""

import pathlib
import sys
from collections import defaultdict

import openpyxl

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from workbook_utils import (  # noqa: E402
    INDEX_PATH,
    WorkbookLock,
    get_header_indexes,
    save_workbook_atomically,
    sync_domain_notes_by_path,
)


def deduplicate_index() -> None:
    """Flag duplicate physical files by hash and sync notes to domain sheets."""
    with WorkbookLock(INDEX_PATH):
        workbook = openpyxl.load_workbook(INDEX_PATH)
        worksheet = workbook["Master"]
        header_indexes = get_header_indexes(
            worksheet,
            ["sha256", "path", "canonical_filename", "notes"],
        )
        duplicate_notes_by_path, flagged = _flag_duplicate_master_rows(
            worksheet,
            header_indexes,
        )
        synced = sync_domain_notes_by_path(workbook, duplicate_notes_by_path)
        save_workbook_atomically(workbook, INDEX_PATH)

    print(f"\nDedup pass complete. {flagged} row(s) flagged.")
    print(f"Synced duplicate notes to {synced} domain row(s).")


def _flag_duplicate_master_rows(
    worksheet: openpyxl.worksheet.worksheet.Worksheet,
    header_indexes: dict[str, int],
) -> tuple[dict[str, str], int]:
    hash_to_rows = _group_rows_by_hash(worksheet, header_indexes["sha256"])
    flagged = 0
    duplicate_notes_by_path: dict[str, str] = {}
    for rows in hash_to_rows.values():
        if len(rows) <= 1:
            continue
        primary_path = rows[0][header_indexes["path"]].value
        for duplicate_row in rows[1:]:
            if _flag_duplicate_row(duplicate_row, primary_path, header_indexes):
                flagged += 1
            duplicate_path = str(duplicate_row[header_indexes["path"]].value)
            duplicate_note = str(duplicate_row[header_indexes["notes"]].value)
            duplicate_notes_by_path[duplicate_path] = duplicate_note
    return duplicate_notes_by_path, flagged


def _group_rows_by_hash(
    worksheet: openpyxl.worksheet.worksheet.Worksheet,
    hash_idx: int,
) -> dict[str, list[tuple[openpyxl.cell.cell.Cell, ...]]]:
    hash_to_rows: dict[str, list[tuple[openpyxl.cell.cell.Cell, ...]]] = defaultdict(
        list
    )
    for row in worksheet.iter_rows(min_row=2):
        file_hash = str(row[hash_idx].value).upper() if row[hash_idx].value else None
        if file_hash:
            hash_to_rows[file_hash].append(row)
    return hash_to_rows


def _flag_duplicate_row(
    row: tuple[openpyxl.cell.cell.Cell, ...],
    primary_path: object,
    header_indexes: dict[str, int],
) -> bool:
    existing_notes = row[header_indexes["notes"]].value or ""
    if "DUPLICATE of" in str(existing_notes):
        return False
    row[
        header_indexes["notes"]
    ].value = f"DUPLICATE of {primary_path}; {existing_notes}".strip("; ")
    print(f"Flagged: {row[header_indexes['canonical_filename']].value}")
    return True


if __name__ == "__main__":
    deduplicate_index()
