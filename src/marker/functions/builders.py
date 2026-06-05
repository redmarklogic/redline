"""Builder functions that compose document engines into report skeletons."""

from pathlib import Path

from marker.domain.models import ProjectMetadata, ReportStructure
from marker.functions.engines import PythonDocxFacade


def build_skeleton(
    structure: ReportStructure,
    metadata: ProjectMetadata,
    output_path: Path,
) -> None:
    """Write a .docx skeleton populated with section headings.

    Args:
        structure: Ordered report sections to render as headings.
        metadata: Project identifiers (reserved for future header population).
        output_path: Destination path for the generated .docx file.
    """
    doc = PythonDocxFacade()
    for section in structure.sections:
        doc.add_heading(section.heading, level=1)
    doc.save(str(output_path))
