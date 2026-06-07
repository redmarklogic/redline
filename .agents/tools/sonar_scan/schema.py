"""Pydantic v2 schema for SonarQube issue retrieval (spec 014, Phase 4).

`SonarIssue` is the read model for one issue returned by the SonarQube Web API
(`/api/issues/search`) or the official `mcp/sonarqube` MCP server. It carries the
fields the triage loop groups and presents: rule, severity, file, line, message,
and status. The model is frozen — issues are immutable records, not mutable state.
"""

from pydantic import BaseModel, ConfigDict, Field


class SonarIssue(BaseModel):
    """One SonarQube issue, normalised for triage grouping and display."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    key: str = Field(description="SonarQube issue key (stable identifier).")
    rule: str = Field(description="Rule key that raised the issue, e.g. python:S1192.")
    severity: str = Field(description="INFO | MINOR | MAJOR | CRITICAL | BLOCKER.")
    component: str = Field(
        description="Component key, e.g. 'redline:src/rl/foo.py'.",
    )
    line: int | None = Field(
        default=None,
        description="1-based line number, or None for file-level issues.",
    )
    message: str = Field(description="Human-readable issue message.")
    status: str = Field(description="OPEN | CONFIRMED | REOPENED | RESOLVED | CLOSED.")

    @property
    def file_path(self) -> str:
        """Repo-relative file path parsed from the component key.

        Component keys are '<projectKey>:<path>'. Falls back to the raw component
        when no project-key prefix is present.
        """
        _, _, path = self.component.partition(":")
        return path or self.component
