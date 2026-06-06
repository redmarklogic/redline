"""CLI script: generate a GIR report skeleton .docx file."""

import datetime
import sys
from pathlib import Path

from marker.domain.models import ProjectMetadata, ReportStructure, SectionHeading
from marker.functions.builders import build_skeleton

_DEFAULT_SECTIONS = [
    "Introduction",
    "Site Description",
    "Desk Study",
    "Field Investigation",
    "Laboratory Testing",
    "Results and Discussion",
    "Conclusions and Recommendations",
    "References",
]

_OUTPUT_PATH = Path("output/skeleton.docx")
_PROJECT_NUMBER = "GIR-001"
_CLIENT = "Acme Corp"
_SITE = "123 Example Street"


def main() -> int:
    """Build a GIR report skeleton .docx from module-level constants."""
    output_path = _OUTPUT_PATH
    if output_path.suffix.lower() != ".docx":
        print(
            f"Error: output path must end in .docx, got: {output_path}", file=sys.stderr
        )
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)

    structure = ReportStructure.model_validate(
        {
            "Sections": tuple(
                SectionHeading.model_validate({"Heading": s}) for s in _DEFAULT_SECTIONS
            )
        }
    )
    metadata = ProjectMetadata.model_validate(
        {
            "Project Number": _PROJECT_NUMBER,
            "Client Name": _CLIENT,
            "Site Address": _SITE,
            "Date": datetime.date.today(),
        }
    )

    build_skeleton(structure, metadata, output_path)
    print(f"Skeleton written to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
