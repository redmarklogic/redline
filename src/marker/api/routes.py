"""Route handlers for the Marker API."""

import re
from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from marker.api.dependencies.auth import require_bearer
from marker.api.schemas import CreateSkeletonRequest
from marker.api.services.skeletons import create_skeleton_document

DOCX_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)

_SAFE_FILENAME_PATTERN = re.compile(r"[^A-Za-z0-9._-]")

router = APIRouter()


def _safe_filename(project_number: str) -> str:
    """Sanitise project_number to a header-safe filename stem.

    Strips any character outside [A-Za-z0-9._-]. Falls back to "skeleton"
    when the result is empty.

    Args:
        project_number: Raw project number string from the request.

    Returns:
        Safe filename stem (without .docx extension).
    """
    safe = _SAFE_FILENAME_PATTERN.sub("", project_number)
    return safe or "skeleton"


@router.post("/skeletons", status_code=status.HTTP_200_OK)
def create_skeleton(
    body: CreateSkeletonRequest,
    _token: Annotated[str, Depends(require_bearer)],
) -> StreamingResponse:
    """Build a .docx report skeleton and return it as a binary download.

    Args:
        body: Validated request body containing sections and project metadata.
        _token: Bearer token (presence-only placeholder; verification pending #50/#73/#48b).

    Returns:
        StreamingResponse with DOCX bytes and appropriate headers.
    """
    docx_bytes = create_skeleton_document(body)
    filename = _safe_filename(body.project_number)
    return StreamingResponse(
        BytesIO(docx_bytes),
        media_type=DOCX_MEDIA_TYPE,
        headers={"Content-Disposition": f'attachment; filename="{filename}.docx"'},
    )
