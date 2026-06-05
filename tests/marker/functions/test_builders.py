import pytest

from marker.domain.models import ProjectMetadata, ReportStructure
from marker.functions.builders import build_skeleton


def _make_structure(*headings: str) -> ReportStructure:
    return ReportStructure.model_validate(
        {"Sections": [{"Heading": h} for h in headings]}
    )


def _make_metadata() -> ProjectMetadata:
    return ProjectMetadata.model_validate(
        {
            "Project Number": "P-001",
            "Client Name": "Acme Corp",
            "Site Address": "123 Main St, Auckland",
            "Date": "2026-06-05",
        }
    )


class TestBuildSkeleton:
    def test_writes_docx_file(self, tmp_path) -> None:
        structure = _make_structure("Introduction", "Methodology", "Conclusion")
        metadata = _make_metadata()
        output = tmp_path / "report.docx"

        build_skeleton(structure, metadata, output)

        assert output.exists()

    def test_single_section(self, tmp_path) -> None:
        structure = _make_structure("Executive Summary")
        metadata = _make_metadata()
        output = tmp_path / "report.docx"

        build_skeleton(structure, metadata, output)

        assert output.exists()

    def test_raises_on_empty_structure(self) -> None:
        with pytest.raises(Exception, match="empty"):
            ReportStructure.model_validate({"Sections": []})

    def test_sections_with_special_characters(self, tmp_path) -> None:
        structure = _make_structure("Site & Location", "Results (Preliminary)")
        metadata = _make_metadata()
        output = tmp_path / "report.docx"

        build_skeleton(structure, metadata, output)

        assert output.exists()
