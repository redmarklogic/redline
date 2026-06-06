import datetime

import pytest

from marker.domain.models import ProjectMetadata, ReportStructure, SectionHeading


def _heading(text: str) -> SectionHeading:
    return SectionHeading.model_validate({"Heading": text})


def _structure(*headings: str) -> ReportStructure:
    return ReportStructure.model_validate(
        {"Sections": [{"Heading": h} for h in headings]}
    )


def _metadata(**overrides: object) -> ProjectMetadata:
    data: dict[str, object] = {
        "Project Number": "P-001",
        "Client Name": "Acme Corp",
        "Site Address": "123 Main St, Auckland",
        "Date": "2026-06-05",
        **overrides,
    }
    return ProjectMetadata.model_validate(data)


class TestSectionHeading:
    def test_valid_heading(self) -> None:
        h = _heading("Introduction")
        assert h.heading == "Introduction"

    def test_rejects_empty_string(self) -> None:
        with pytest.raises(Exception, match="empty or whitespace"):
            _heading("")

    def test_rejects_whitespace_only(self) -> None:
        with pytest.raises(Exception, match="empty or whitespace"):
            _heading("   ")

    def test_is_frozen(self) -> None:
        h = _heading("Introduction")
        with pytest.raises(Exception, match="frozen"):
            h.heading = "Changed"  # type: ignore[misc]


class TestReportStructure:
    def test_valid_structure(self) -> None:
        s = _structure("Introduction", "Methodology", "Conclusion")
        assert len(s.sections) == 3

    def test_sections_ordered(self) -> None:
        s = _structure("A", "B", "C")
        assert [sec.heading for sec in s.sections] == ["A", "B", "C"]

    def test_rejects_empty_sections(self) -> None:
        with pytest.raises(Exception, match="empty"):
            _structure()

    def test_rejects_duplicate_headings(self) -> None:
        with pytest.raises(Exception, match="duplicate"):
            _structure("Introduction", "Introduction")

    def test_is_frozen(self) -> None:
        s = _structure("Introduction")
        with pytest.raises(Exception, match="frozen"):
            s.sections = ()  # type: ignore[misc]


class TestProjectMetadata:
    def test_valid_metadata(self) -> None:
        m = _metadata()
        assert m.project_number == "P-001"
        assert m.client_name == "Acme Corp"
        assert m.site_address == "123 Main St, Auckland"

    def test_date_field_is_date_type(self) -> None:
        m = _metadata()
        assert isinstance(m.date, datetime.date)

    def test_rejects_missing_required_field(self) -> None:
        with pytest.raises(Exception, match="Field required"):
            ProjectMetadata.model_validate(
                {
                    "Client Name": "Acme",
                    "Site Address": "123 Main St",
                    "Date": "2026-06-05",
                }
            )

    def test_is_frozen(self) -> None:
        m = _metadata()
        with pytest.raises(Exception, match="frozen"):
            m.project_number = "P-999"  # type: ignore[misc]
