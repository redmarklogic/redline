from pathlib import Path

from marker.domain.models import ProjectMetadata, ReportStructure
from marker.functions.engines import PythonDocxFacade


def build_skeleton(
    structure: ReportStructure,
    metadata: ProjectMetadata,
    output_path: Path,
) -> None:
    doc = PythonDocxFacade()
    for section in structure.sections:
        doc.add_heading(section.heading, level=1)
    doc.save(str(output_path))
