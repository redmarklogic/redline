from pathlib import Path

from marker.domain.models import ProjectMetadata, ReportStructure


def build_skeleton(
    structure: ReportStructure,
    metadata: ProjectMetadata,
    output_path: Path,
) -> None:
    raise NotImplementedError
