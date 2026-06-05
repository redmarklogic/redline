"""Builder functions that compose document engines into report skeletons."""

from pathlib import Path

from marker.domain.models import ProjectMetadata, ReportStructure
from marker.domain.protocols import DocumentFacade
from marker.functions.engines import PythonDocxFacade


def build_sections(structure: ReportStructure, doc: DocumentFacade) -> None:
    for section in structure.sections:
        doc.add_heading(section.heading, level=1)


def build_skeleton(
    structure: ReportStructure,
    metadata: ProjectMetadata,
    output_path: Path,
) -> None:
    doc = PythonDocxFacade()
    build_sections(structure, doc)
    doc.save(str(output_path))
