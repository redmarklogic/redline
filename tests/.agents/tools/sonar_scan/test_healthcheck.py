"""Tests for sonar_scan.healthcheck (the pre-flight availability probe)."""

from unittest.mock import patch

from sonar_scan import SonarQubeUnavailableError
from sonar_scan.healthcheck import main


class TestHealthcheckMain:
    def test_returns_zero_when_up(self) -> None:
        with patch.dict("os.environ", {"SONARQUBE_URL": "http://localhost:9000"}):
            with patch("sonar_scan.healthcheck.ensure_available", return_value="UP"):
                assert main() == 0

    def test_prefers_sonarqube_url_then_host_url(self) -> None:
        env = {"SONAR_HOST_URL": "http://host.docker.internal:9000"}
        with patch.dict("os.environ", env, clear=True):
            with patch(
                "sonar_scan.healthcheck.ensure_available", return_value="UP"
            ) as probe:
                assert main() == 0
        probe.assert_called_once_with("http://host.docker.internal:9000")

    def test_returns_one_when_unavailable(self) -> None:
        err = SonarQubeUnavailableError("http://localhost:9000", reason="refused")
        with patch.dict("os.environ", {"SONARQUBE_URL": "http://localhost:9000"}):
            with patch("sonar_scan.healthcheck.ensure_available", side_effect=err):
                assert main() == 1

    def test_returns_one_when_no_url_configured(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            assert main() == 1
