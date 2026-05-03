"""Upsert a NotebookLM notebook into index-notebooklm.xlsx.

Usage (one-shot, called by Linda):
    python .agents/tools/library/upsert_notebooklm_index.py
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

INDEX_PATH = Path(r"G:\My Drive\Library\index-notebooklm.xlsx")
HEADER_FONT = Font(bold=True, color="FFFFFF")
HEADER_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
DATA_ALIGN = Alignment(wrap_text=True, vertical="top")


def _apply_row_style(ws, row_idx: int) -> None:
    for cell in ws[row_idx]:
        cell.alignment = DATA_ALIGN


def upsert(notebook: dict, sources: list[dict]) -> str:
    wb = openpyxl.load_workbook(INDEX_PATH)
    ws_nb = wb["notebooks"]
    ws_src = wb["sources"]

    nid = notebook["notebook_id"]
    today = date.today().isoformat()

    # --- notebooks: find existing row ---
    existing_row = None
    for row in ws_nb.iter_rows(min_row=2, max_row=ws_nb.max_row, min_col=1, max_col=1):
        if row[0].value == nid:
            existing_row = row[0].row
            break

    nb_values = [
        nid,
        notebook["title"],
        notebook["url"],
        notebook["source_count"],
        notebook.get("summary", ""),
        notebook.get("suggested_topics", ""),
        today,
        "active",
    ]

    if existing_row:
        for col_idx, val in enumerate(nb_values, start=1):
            ws_nb.cell(row=existing_row, column=col_idx, value=val)
        _apply_row_style(ws_nb, existing_row)
        operation = "upsert (existing row overwritten)"
    else:
        ws_nb.append(nb_values)
        _apply_row_style(ws_nb, ws_nb.max_row)
        operation = "insert (new row appended)"

    # --- sources: delete existing rows for this notebook_id ---
    rows_to_delete = []
    for row in ws_src.iter_rows(
        min_row=2, max_row=ws_src.max_row, min_col=1, max_col=1
    ):
        if row[0].value == nid:
            rows_to_delete.append(row[0].row)

    for row_idx in reversed(rows_to_delete):
        ws_src.delete_rows(row_idx)

    # --- sources: insert current sources ---
    for src in sources:
        ws_src.append(
            [
                nid,
                notebook["title"],
                src["source_id"],
                src["source_title"],
                src.get("source_summary", ""),
                src.get("source_keywords", ""),
            ]
        )
        _apply_row_style(ws_src, ws_src.max_row)

    wb.save(INDEX_PATH)

    # Verify
    wb2 = openpyxl.load_workbook(INDEX_PATH)
    nb_count = wb2["notebooks"].max_row - 1
    src_count = wb2["sources"].max_row - 1
    wb2.close()

    return (
        f"{operation}\n"
        f"notebooks worksheet: {nb_count} rows (excl. header)\n"
        f"sources worksheet: {src_count} rows (excl. header)\n"
        f"deleted {len(rows_to_delete)} old source rows, inserted {len(sources)} new"
    )


if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    result = upsert(data["notebook"], data["sources"])
    print(result)
