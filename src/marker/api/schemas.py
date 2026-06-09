"""Transport DTOs for the Marker API."""

import datetime

from pydantic import BaseModel, Field, field_validator

model_config_extra_forbid = {"extra": "forbid"}


class CreateSkeletonRequest(BaseModel):
    """Request body for POST /skeletons.

    All domain constraints are mirrored here so validation failures are
    caught as RequestValidationError (→ 422) at the boundary, not as
    pydantic.ValidationError inside the route (which would → 500).
    """

    model_config = {"extra": "forbid"}

    sections: list[str] = Field(
        description="Ordered list of section headings. Must be non-empty, "
        "each heading non-blank, with no duplicates.",
    )
    project_number: str = Field(
        min_length=1,
        description="Client-assigned project number.",
    )
    client_name: str = Field(
        min_length=1,
        description="Name of the client organisation.",
    )
    site_address: str = Field(
        min_length=1,
        description="Physical address of the site.",
    )
    date: datetime.date = Field(
        description="Date the report was prepared (ISO-8601).",
    )

    @field_validator("sections")
    @classmethod
    def validate_sections(cls, v: list[str]) -> list[str]:
        """Enforce non-empty, non-blank, duplicate-free section list.

        Args:
            v: Raw sections value from input.

        Returns:
            The validated sections list.

        Raises:
            ValueError: If sections is empty, contains blank entries, or has
                duplicate headings.
        """
        if not v:
            raise ValueError("sections must contain at least one item")
        for heading in v:
            if not heading.strip():
                raise ValueError("each section heading must be non-blank")
        if len(v) != len(set(v)):
            raise ValueError("sections must not contain duplicate headings")
        return v
