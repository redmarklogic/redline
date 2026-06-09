"""Skeleton service — orchestrates domain construction and document building."""

from marker.api.schemas import CreateSkeletonRequest
from marker.domain.models import ProjectMetadata, ReportStructure
from marker.functions.builders import build_skeleton_bytes


def create_skeleton_document(body: CreateSkeletonRequest) -> bytes:
    """Build a .docx skeleton from a validated request and return raw bytes.

    Args:
        body: Validated skeleton request DTO.

    Returns:
        Raw .docx bytes.
    """
    structure = ReportStructure.model_validate(
        {"Sections": [{"Heading": s} for s in body.sections]}
    )
    metadata = ProjectMetadata.model_validate(
        {
            "Project Number": body.project_number,
            "Client Name": body.client_name,
            "Site Address": body.site_address,
            "Date": body.date,
        }
    )
    return build_skeleton_bytes(structure, metadata)
