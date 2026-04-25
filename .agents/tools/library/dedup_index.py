"""Deduplication pass — Phase 3 of the folder indexing workflow.

Run after all files are indexed and renamed:

    .\.venv\Scripts\python.exe .agents\tools\library\dedup_index.py

Groups all rows in the Master worksheet by sha256. Flags the second+ occurrence
of each hash with "DUPLICATE of <path>" in the notes column. Does not delete files.
"""

from collections import defaultdict

import openpyxl

INDEX_PATH = r"G:\My Drive\Library\library-index.xlsx"

wb = openpyxl.load_workbook(INDEX_PATH)
ws = wb["Master"]

headers = [cell.value for cell in ws[1]]
path_idx = headers.index("path")
filename_idx = headers.index("canonical_filename")
notes_idx = headers.index("notes")

hash_to_rows: dict[str, list] = defaultdict(list)
for row in ws.iter_rows(min_row=2):
    h = str(row[0].value).upper() if row[0].value else None
    if h:
        hash_to_rows[h].append(row)

flagged = 0
for h, rows in hash_to_rows.items():
    if len(rows) > 1:
        primary_path = rows[0][path_idx].value
        for dup_row in rows[1:]:
            existing = dup_row[notes_idx].value or ""
            if "DUPLICATE of" not in existing:
                dup_row[
                    notes_idx
                ].value = f"DUPLICATE of {primary_path}; {existing}".strip("; ")
                print(f"Flagged: {dup_row[filename_idx].value}")
                flagged += 1

wb.save(INDEX_PATH)
print(f"\nDedup pass complete. {flagged} row(s) flagged.")
