"""DTO contract tests for CreateSkeletonRequest."""

import datetime

import pytest


class TestCreateSkeletonRequest:
    def test_valid_body_accepted(self) -> None:
        from marker.api.schemas import CreateSkeletonRequest

        request = CreateSkeletonRequest(
            sections=["Introduction", "Conclusions"],
            project_number="P-001",
            client_name="Acme Corp",
            site_address="123 Main St",
            date=datetime.date(2026, 6, 9),
        )

        assert request.sections == ["Introduction", "Conclusions"]
        assert request.project_number == "P-001"

    def test_missing_field_rejected(self) -> None:
        from pydantic import ValidationError

        from marker.api.schemas import CreateSkeletonRequest

        with pytest.raises(ValidationError):
            CreateSkeletonRequest(
                sections=["Introduction"],
                client_name="Acme",
                site_address="123 St",
                date=datetime.date(2026, 6, 9),
            )  # type: ignore[call-arg]

    def test_extra_field_rejected(self) -> None:
        from pydantic import ValidationError

        from marker.api.schemas import CreateSkeletonRequest

        with pytest.raises(ValidationError):
            CreateSkeletonRequest(
                sections=["Introduction"],
                project_number="P-001",
                client_name="Acme",
                site_address="123 St",
                date=datetime.date(2026, 6, 9),
                unexpected="oops",  # type: ignore[call-arg]
            )
