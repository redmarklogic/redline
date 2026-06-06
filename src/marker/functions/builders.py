"""Builder functions that compose document engines into report skeletons."""

import datetime
from pathlib import Path

from marker.domain.models import ProjectMetadata, ReportStructure
from marker.domain.protocols import DocumentFacade
from marker.functions.engines import PythonDocxFacade

_METADATA_ROWS: tuple[tuple[str, str], ...] = (
    ("Project Number", "project_number"),
    ("Client Name", "client_name"),
    ("Site Address", "site_address"),
    ("Date", "date"),
)


def build_sections(structure: ReportStructure, doc: DocumentFacade) -> None:
    """Add a level-1 heading to doc for each section in structure.

    Args:
        structure: Report structure whose sections drive heading generation.
        doc: Document facade to which headings are written.
    """
    for section in structure.sections:
        doc.add_heading(section.heading, level=1)


def build_metadata(metadata: ProjectMetadata, doc: DocumentFacade) -> None:
    """Write a two-column metadata table (label | value) to doc.

    Args:
        metadata: Project metadata supplying field values.
        doc: Document facade to which the table is written.
    """
    table_index = doc.add_table(rows=len(_METADATA_ROWS), cols=2)
    for row_idx, (label, field) in enumerate(_METADATA_ROWS):
        value = getattr(metadata, field)
        doc.write_table_cell(table_index, row_idx, 0, label)
        if isinstance(value, datetime.date):
            doc.write_table_cell(table_index, row_idx, 1, value.isoformat())
        else:
            doc.write_table_cell(table_index, row_idx, 1, str(value))


def build_skeleton(
    structure: ReportStructure,
    metadata: ProjectMetadata,
    output_path: Path,
) -> None:
    """Build and save a .docx report skeleton from structure to output_path.

    Args:
        structure: Report structure whose sections populate the skeleton.
        metadata: Project metadata written as a table before the sections.
        output_path: Destination path where the .docx file is saved.
    """
    doc = PythonDocxFacade()
    build_metadata(metadata, doc)
    build_sections(structure, doc)
    doc.save(str(output_path))
