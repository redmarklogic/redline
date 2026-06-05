import datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class SectionHeading(BaseModel, frozen=True):
    heading: str = Field(description="Section heading text.", alias="Heading")

    @field_validator("heading")
    @classmethod
    def heading_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("heading must not be empty or whitespace")
        return v


class ReportStructure(BaseModel, frozen=True):
    sections: tuple[SectionHeading, ...] = Field(
        description="Ordered list of report sections.", alias="Sections"
    )

    @model_validator(mode="after")
    def validate_sections(self) -> ReportStructure:
        if not self.sections:
            raise ValueError("sections must not be empty")
        headings = [s.heading for s in self.sections]
        if len(headings) != len(set(headings)):
            raise ValueError("sections must not contain duplicate headings")
        return self


class ProjectMetadata(BaseModel, frozen=True):
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
