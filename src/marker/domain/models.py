"""Pydantic domain models for report structure and project metadata."""

import datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class SectionHeading(BaseModel, frozen=True):
    """A single section heading within a report."""

    heading: str = Field(description="Section heading text.", alias="Heading")

    @field_validator("heading")
    @classmethod
    def heading_not_blank(cls, v: str) -> str:
        """Reject blank or whitespace-only headings.

        Args:
            v: Raw heading value from input.

        Returns:
            The validated heading string.

        Raises:
            ValueError: If the heading is empty or whitespace-only.
        """
        if not v.strip():
            raise ValueError("heading must not be empty or whitespace")
        return v


class ReportStructure(BaseModel, frozen=True):
    """Ordered collection of section headings defining a report layout."""

    sections: tuple[SectionHeading, ...] = Field(
        description="Ordered list of report sections.", alias="Sections"
    )

    @model_validator(mode="after")
    def validate_sections(self) -> ReportStructure:
        """Ensure sections are non-empty and contain no duplicate headings.

        Returns:
            The validated ReportStructure instance.

        Raises:
            ValueError: If sections is empty or contains duplicate headings.
        """
        if not self.sections:
            raise ValueError("sections must not be empty")
        headings = [s.heading for s in self.sections]
        if len(headings) != len(set(headings)):
            raise ValueError("sections must not contain duplicate headings")
        return self


class ProjectMetadata(BaseModel, frozen=True):
    """Client and project identifiers attached to a report."""

    project_number: str = Field(
        description="Client-assigned project number.", alias="Project Number"
    )
    client_name: str = Field(
        description="Name of the client organization.", alias="Client Name"
    )
    site_address: str = Field(
        description="Physical address of the site.", alias="Site Address"
    )
    date: datetime.date = Field(
        description="Date the report was prepared.", alias="Date"
    )
