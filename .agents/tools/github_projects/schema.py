"""Pydantic v2 schemas for GitHub Projects task management.

Design decisions:
- `TaskCreate` and `TaskUpdate` are input models (frozen, strict).
- `TaskResult` is the mutation envelope; `TaskRecord` is the read model.
- `ProjectConfig` caches resolved GitHub node IDs — persisted to project_config.json.
- `start_date` and `target_date` are mandatory on TaskCreate (no default, no Optional).
- `blocked_by` is mandatory when status == "Blocked" — enforced by model_validator.
- All fields carry `alias` (GitHub Projects field name / JSON key), `title`, `description`,
  `examples`, and relevant constraints. `populate_by_name=True` allows both the Python
  attribute name and the alias at construction time.

Agent assignment design:
  Agents are not GitHub users and cannot appear in the native GitHub assignees field.
  The solution uses two complementary mechanisms:
  1. `agents: frozenset[AgentName]` — validated, closed-set field on the Pydantic model.
     Mandatory on TaskCreate (min_length=1 on the frozenset); optional on TaskUpdate/TaskRecord.
  2. `primary_agent` property — returns the single agent name written to the 'Agent'
     single-select custom field on the GitHub Project board (first name alphabetically
     when multiple agents are set). The board field is single-select by GitHub design;
     the full set is preserved in the '## Agents' section of the issue body.
  AgentName is a Literal type alias listing every valid agent; validation rejects any
  name not in the closed set at construction time.
"""

from datetime import date, datetime
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

type TaskType = Literal["Feature", "Design", "Content", "Ops", "Research"]
type StatusValue = Literal["Backlog", "In Progress", "Blocked", "To Review", "Done"]

# Closed set of valid agent names — must match the options configured on the
# GitHub Projects 'Agent' custom field and the agent register in docs/people/.
type AgentName = Literal[
    "Kabilan",
    "Mark",
    "Matt",
    "John",
    "Peter",
    "Ron",
    "Graeme",
    "Linda",
    "Harriet",
    "Founder",
]


# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class TaskCreate(BaseModel):
    """Input schema for creating a new task (GitHub issue + project item).

    `start_date` and `target_date` are unconditionally required — no defaults,
    no Optional. A task without dates cannot be sprint-planned or roadmap-rendered.

    All fields carry an `alias` matching the GitHub Projects custom field name or
    the GitHub Issues API JSON key so callers can use either the Python name or the
    wire name. `populate_by_name=True` permits both.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
        populate_by_name=True,  # accept both Python name and alias at construction
    )

    title: Annotated[
        str,
        Field(
            alias="title",
            title="Issue title",
            description="Short, imperative summary of the task. Displayed as the GitHub issue title.",
            min_length=1,
            max_length=256,
            examples=["Implement skeleton-generator PDF export"],
        ),
    ]
    task_type: Annotated[
        TaskType,
        Field(
            alias="Task Type",
            title="Task type",
            description=(
                "Discriminates the task category and determines which body template is used. "
                "Maps to the 'Task Type' single-select custom field on the GitHub Project board. "
                "(GitHub reserves the name 'Type' — field was created as 'Task Type'.)"
            ),
            examples=["Feature"],
        ),
    ]
    start_date: Annotated[
        date,
        Field(
            alias="Start date",
            title="Sprint start date",
            description=(
                "Planned start date for this task. Mandatory — a task without a start date "
                "cannot appear as a bar on the roadmap timeline. Set by Mark on sprint assignment. "
                "Format: ISO 8601 (YYYY-MM-DD)."
            ),
            examples=["2026-06-09"],
        ),
    ]
    target_date: Annotated[
        date,
        Field(
            alias="Target date",
            title="Target completion date",
            description=(
                "Planned end date for this task. Mandatory — defaults to the sprint end date. "
                "Must be >= start_date (enforced by model_validator). "
                "Format: ISO 8601 (YYYY-MM-DD)."
            ),
            examples=["2026-06-22"],
        ),
    ]
    purpose: Annotated[
        str,
        Field(
            alias="purpose",
            title="Purpose",
            description=(
                "One sentence stating the outcome this task unlocks and the strategic bet it serves. "
                "Appears as the ## Purpose section in the issue body. "
                "Pattern: 'Enables X by Y — serves *bet-name*'."
            ),
            min_length=1,
            max_length=512,
            examples=[
                "Enables PDF export of skeleton reports — serves *free-tier-signal* bet."
            ],
        ),
    ]
    done_when: Annotated[
        str,
        Field(
            alias="done_when",
            title="Done when",
            description=(
                "Observable Done condition the founder can verify in under 30 seconds. "
                "Not 'when it looks good' — must name a specific file, URL, or system state. "
                "Appears as the ## Done when section in the issue body."
            ),
            min_length=1,
            max_length=512,
            examples=[
                "PR merged and spec task 001-T4 checked off in specs/001-skeleton-generator/tasks.md."
            ],
        ),
    ]
    source: Annotated[
        str,
        Field(
            alias="Source",
            title="SSOT source pointer",
            description=(
                "Single authoritative document reference for this task. "
                "Maps to the 'Source' text custom field on the GitHub Project board. "
                "Feature: 'specs/NNN/'. "
                "Design: 'docs/product/design/[file].md'. "
                "Content: 'docs/product/marketing/content-calendar.md#[id]'. "
                "Ops: 'docs/ops/runbooks/[file].md' or 'none'. "
                "Research: 'docs/research/YYYYMMDD-[topic].md'."
            ),
            min_length=1,
            max_length=512,
            examples=["specs/001-skeleton-generator/"],
        ),
    ]
    status: Annotated[
        StatusValue,
        Field(
            alias="Status",
            title="Board column",
            description=(
                "Current column on the GitHub Project board. "
                "New tasks default to 'Backlog'. "
                "'Done' is write-protected — only a merged PR or founder action may set it."
            ),
            examples=["Backlog"],
        ),
    ] = "Backlog"
    agents: Annotated[
        frozenset[AgentName],
        Field(
            alias="agents",
            title="Responsible agents",
            description=(
                "Non-empty set of agent names responsible for this task. "
                "Agents are not GitHub users and cannot be set via the native GitHub assignees field. "
                "Instead this value is stored in two places: "
                "(1) the 'Agent' single-select custom field on the board receives the primary agent "
                "(first alphabetically when multiple agents are listed), and "
                "(2) all agent names are written to a '## Agents' section in the issue body for full traceability. "
                "Must be non-empty — a task with no agent owner will stall. "
                "Each name must be a value in the AgentName Literal type alias."
            ),
            min_length=1,
            examples=[["Kabilan"], ["Kabilan", "Peter"]],
        ),
    ]
    sprint: Annotated[
        str | None,
        Field(
            default=None,
            alias="Sprint",
            title="Sprint iteration title",
            description=(
                "Human-readable sprint title matching an iteration option on the board "
                "(e.g. 'Sprint 1 - Jun 1-14'). Mark resolves this to an iteration node ID "
                "via ProjectConfig.option_ids['Sprint']. "
                "Leave None if the task is not yet sprint-assigned."
            ),
            examples=["Sprint 1 - Jun 1-14"],
        ),
    ]
    blocked_by: Annotated[
        str | None,
        Field(
            default=None,
            alias="Blocked by",
            title="Blocking dependency",
            description=(
                "Free-text description of the external dependency that blocks forward progress. "
                "Required when status == 'Blocked'; must name the specific unblock condition. "
                "Maps to the 'Blocked by' text custom field. "
                "Example: 'Waiting for client to return signed NDA — unblocks on receipt.'"
            ),
            max_length=512,
            examples=["Waiting for client to return signed NDA — unblocks on receipt."],
        ),
    ]
    depends_on: Annotated[
        frozenset[int] | None,
        Field(
            default=None,
            alias="Depends on",
            title="Predecessor issue numbers",
            description=(
                "Set of GitHub issue numbers this task depends on. "
                "Used to render predecessor bars on the Gantt roadmap: "
                "this task's start_date should be >= the target_date of all predecessors. "
                "Stored in two places: (1) a 'Depends on' text custom field on the board "
                "(comma-separated numbers, e.g. '#42, #17'), and (2) a '## Depends on' section "
                "in the issue body where each number auto-links to the referenced issue. "
                "None means no predecessors. Provide at least one number if the field is set."
            ),
            min_length=1,
            examples=[[42], [17, 42]],
        ),
    ]
    labels: Annotated[
        list[str],
        Field(
            default_factory=list,
            alias="labels",
            title="GitHub issue labels",
            description=(
                "Labels applied to the GitHub issue. Must be from the approved taxonomy: "
                "surface:web, surface:mobile, surface:pdf, "
                "bet:free-tier-signal, bet:qualified-conversations, bet:paid-conversions, "
                "missing-spec-link. "
                "Do not use labels to duplicate information already in custom fields (Type, Agent)."
            ),
            examples=[["bet:free-tier-signal", "surface:web"]],
        ),
    ]
    body: Annotated[
        str | None,
        Field(
            default=None,
            alias="body",
            title="Issue body (Markdown)",
            description=(
                "Full Markdown body for the GitHub issue. "
                "If None, `_build_body()` in functions.py generates it from purpose, source, "
                "and done_when. Provide an explicit body only when using a full template "
                "(e.g., from the per-type templates in the task knowledge architecture doc)."
            ),
        ),
    ]

    @model_validator(mode="after")
    def dates_ordered(self) -> Self:
        if self.start_date > self.target_date:
            raise ValueError("start_date must be <= target_date")
        return self

    @model_validator(mode="after")
    def blocked_requires_reason(self) -> Self:
        if self.status == "Blocked" and not self.blocked_by:
            raise ValueError("blocked_by must be set when status is 'Blocked'")
        return self

    @property
    def primary_agent(self) -> AgentName:
        """The single agent name written to the 'Agent' board field.

        GitHub Projects single-select fields hold one value only. When multiple
        agents are assigned, the primary agent is the first name alphabetically.
        The full set is preserved in the '## Agents' section of the issue body.
        """
        return min(self.agents)  # type: ignore[return-value]


class TaskUpdate(BaseModel):
    """Input schema for updating fields on an existing project item.

    `item_id` is the only required field — all task fields are optional.

    Note on partial-date validation: if only `start_date` or only `target_date`
    is updated (not both), cross-field ordering cannot be enforced without fetching
    the current task. Callers must ensure consistency when updating a single date.
    The validator fires only when both fields are present in this update payload.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    item_id: Annotated[
        str,
        Field(
            alias="id",
            title="Project item node ID",
            description=(
                "GitHub Projects item node ID (GraphQL node ID, e.g. 'PVTI_lAD...'). "
                "Returned as item_id in TaskResult and TaskRecord. "
                "Required — identifies which board item to update."
            ),
            min_length=1,
            examples=["PVTI_lADOANN5s84ACbL0zgBVd94"],
        ),
    ]
    title: Annotated[
        str | None,
        Field(
            default=None,
            alias="title",
            title="Issue title",
            description="Updated issue title. If None, the existing title is unchanged.",
            min_length=1,
            max_length=256,
            examples=["Implement skeleton-generator PDF export (revised scope)"],
        ),
    ]
    task_type: Annotated[
        TaskType | None,
        Field(
            default=None,
            alias="Task Type",
            title="Task type",
            description="Updated task type. If None, the existing Task Type field is unchanged.",
            examples=["Design"],
        ),
    ]
    status: Annotated[
        StatusValue | None,
        Field(
            default=None,
            alias="Status",
            title="Board column",
            description=(
                "Updated board status. If None, the existing Status is unchanged. "
                "'Done' is write-protected — agents may not set it via TaskUpdate; "
                "use a merged PR or founder action."
            ),
            examples=["In Progress"],
        ),
    ]
    start_date: Annotated[
        date | None,
        Field(
            default=None,
            alias="Start date",
            title="Sprint start date",
            description=(
                "Updated start date. If None, the existing date is unchanged. "
                "When updating only this field (not target_date), the caller must ensure "
                "start_date remains <= the existing target_date."
            ),
            examples=["2026-06-16"],
        ),
    ]
    target_date: Annotated[
        date | None,
        Field(
            default=None,
            alias="Target date",
            title="Target completion date",
            description=(
                "Updated target date. If None, the existing date is unchanged. "
                "When updating only this field (not start_date), the caller must ensure "
                "target_date remains >= the existing start_date."
            ),
            examples=["2026-06-28"],
        ),
    ]
    purpose: Annotated[
        str | None,
        Field(
            default=None,
            alias="purpose",
            title="Purpose",
            description="Updated purpose sentence. If None, the issue body is not modified.",
            max_length=512,
        ),
    ]
    done_when: Annotated[
        str | None,
        Field(
            default=None,
            alias="done_when",
            title="Done when",
            description="Updated Done condition. If None, the issue body is not modified.",
            max_length=512,
        ),
    ]
    source: Annotated[
        str | None,
        Field(
            default=None,
            alias="Source",
            title="SSOT source pointer",
            description="Updated Source field. If None, the existing Source is unchanged.",
            max_length=512,
            examples=["specs/002-mobile-bridge/"],
        ),
    ]
    agents: Annotated[
        frozenset[AgentName] | None,
        Field(
            default=None,
            alias="agents",
            title="Responsible agents",
            description=(
                "Replacement agent set. If None, the existing agents are unchanged. "
                "When provided, replaces the full agent set: include all agents you want to keep. "
                "The primary agent (first alphabetically) is written to the 'Agent' board field; "
                "all agents are written to the issue body."
            ),
            min_length=1,
            examples=[["Matt"], ["Kabilan", "Peter"]],
        ),
    ]
    sprint: Annotated[
        str | None,
        Field(
            default=None,
            alias="Sprint",
            title="Sprint iteration title",
            description=(
                "Updated sprint assignment. If None, the existing Sprint field is unchanged. "
                "Only Mark may change sprint assignment per governance rules."
            ),
            examples=["Sprint 2 - Jun 15-28"],
        ),
    ]
    blocked_by: Annotated[
        str | None,
        Field(
            default=None,
            alias="Blocked by",
            title="Blocking dependency",
            description=(
                "Updated or cleared blocking reason. "
                "Required (non-empty) when status is being set to 'Blocked' in this update. "
                "Pass an empty string to clear the field when unblocking."
            ),
            max_length=512,
        ),
    ]
    depends_on: Annotated[
        frozenset[int] | None,
        Field(
            default=None,
            alias="Depends on",
            title="Predecessor issue numbers",
            description=(
                "Updated set of predecessor issue numbers. If None, the existing value is unchanged. "
                "When provided, replaces the full set — include all predecessors you want to keep. "
                "Pass an empty frozenset to clear all dependencies."
            ),
            examples=[[42]],
        ),
    ]
    labels: Annotated[
        list[str] | None,
        Field(
            default=None,
            alias="labels",
            title="GitHub issue labels",
            description=(
                "Replacement label set. If None, labels are unchanged. "
                "Replaces all existing labels — include any labels you want to keep."
            ),
        ),
    ]
    body: Annotated[
        str | None,
        Field(
            default=None,
            alias="body",
            title="Issue body (Markdown)",
            description="Replacement issue body. If None, the issue body is not modified.",
        ),
    ]

    @model_validator(mode="after")
    def dates_ordered_if_both_present(self) -> Self:
        if (
            self.start_date is not None
            and self.target_date is not None
            and self.start_date > self.target_date
        ):
            raise ValueError("start_date must be <= target_date")
        return self

    @model_validator(mode="after")
    def blocked_requires_reason(self) -> Self:
        if self.status == "Blocked" and not self.blocked_by:
            raise ValueError("blocked_by must be set when updating status to 'Blocked'")
        return self


# ---------------------------------------------------------------------------
# Output models
# ---------------------------------------------------------------------------


class TaskResult(BaseModel):
    """Envelope returned by every mutating operation: create, update, move, delete.

    HTTP-style status codes:
        200  Success
        207  Partial success (task created/updated but some field writes failed)
        400  Bad input (Pydantic ValidationError before reaching gh)
        401  Authentication error (gh auth not configured or missing project scope)
        403  Forbidden (e.g., agent attempted to set status to 'Done')
        404  Item not found
        422  GitHub API rejected the request (validation, constraint, duplicate)
        500  Unexpected error (JSON parse failure, subprocess crash)
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    ok: Annotated[
        bool,
        Field(
            alias="ok",
            title="Success flag",
            description="True when the operation completed without errors (status_code 200 or 207).",
            examples=[True],
        ),
    ]
    status_code: Annotated[
        int,
        Field(
            alias="status_code",
            title="HTTP-style status code",
            description=(
                "Numeric status code following HTTP semantics. "
                "200=OK, 207=partial success, 400=bad input, 401=auth error, "
                "403=forbidden, 404=not found, 422=API rejection, 500=unexpected error."
            ),
            ge=100,
            le=599,
            examples=[200],
        ),
    ]
    message: Annotated[
        str,
        Field(
            alias="message",
            title="Human-readable result message",
            description="Summary of the operation outcome. Contains field-level error details on 207.",
            examples=["OK"],
        ),
    ]
    issue_url: Annotated[
        str | None,
        Field(
            default=None,
            alias="issue_url",
            title="GitHub issue URL",
            description="Full URL of the created or updated GitHub issue. Populated on success; None on failure.",
            examples=["https://github.com/redmarklogic/redline/issues/42"],
        ),
    ]
    item_id: Annotated[
        str | None,
        Field(
            default=None,
            alias="item_id",
            title="Project item node ID",
            description="GitHub Projects item node ID. Populated on success; None on failure.",
            examples=["PVTI_lADOANN5s84ACbL0zgBVd94"],
        ),
    ]
    raw: Annotated[
        dict[str, object] | None,
        Field(
            default=None,
            alias="raw",
            title="Raw gh JSON payload",
            description="Raw JSON response from the gh CLI for debugging purposes. Never logged in production.",
        ),
    ]


class TaskRecord(BaseModel):
    """Read model returned by get_task() and list_tasks()."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    item_id: Annotated[
        str,
        Field(
            alias="id",
            title="Project item node ID",
            description="GitHub Projects item node ID (GraphQL). Used as the key for update/move/delete operations.",
            examples=["PVTI_lADOANN5s84ACbL0zgBVd94"],
        ),
    ]
    issue_url: Annotated[
        str,
        Field(
            alias="url",
            title="GitHub issue URL",
            description="Full URL of the linked GitHub issue.",
            examples=["https://github.com/redmarklogic/redline/issues/42"],
        ),
    ]
    title: Annotated[
        str,
        Field(
            alias="title",
            title="Issue title",
            description="Current title of the GitHub issue.",
            min_length=1,
            max_length=256,
        ),
    ]
    status: Annotated[
        StatusValue,
        Field(
            alias="Status",
            title="Board column",
            description="Current column on the GitHub Project board.",
            examples=["In Progress"],
        ),
    ]
    task_type: Annotated[
        TaskType | None,
        Field(
            default=None,
            alias="Task Type",
            title="Task type",
            description="Value of the 'Task Type' custom field. None if not set on the board item.",
        ),
    ]
    start_date: Annotated[
        date | None,
        Field(
            default=None,
            alias="Start date",
            title="Sprint start date",
            description="Value of the 'Start date' custom field. None if not yet set.",
            examples=["2026-06-09"],
        ),
    ]
    target_date: Annotated[
        date | None,
        Field(
            default=None,
            alias="Target date",
            title="Target completion date",
            description="Value of the 'Target date' custom field. None if not yet set.",
            examples=["2026-06-22"],
        ),
    ]
    source: Annotated[
        str | None,
        Field(
            default=None,
            alias="Source",
            title="SSOT source pointer",
            description="Value of the 'Source' custom field. None if not set.",
            examples=["specs/001-skeleton-generator/"],
        ),
    ]
    agents: Annotated[
        frozenset[AgentName] | None,
        Field(
            default=None,
            alias="agents",
            title="Responsible agents",
            description=(
                "Set of agent names responsible for this task, as read from the issue body '## Agents' section. "
                "None if the section is absent or the task was created before this field was introduced. "
                "The 'Agent' board field holds only the primary agent (first alphabetically)."
            ),
        ),
    ]
    sprint: Annotated[
        str | None,
        Field(
            default=None,
            alias="Sprint",
            title="Sprint iteration title",
            description="Human-readable sprint title from the 'Sprint' iteration field. None if not sprint-assigned.",
            examples=["Sprint 1 - Jun 1-14"],
        ),
    ]
    blocked_by: Annotated[
        str | None,
        Field(
            default=None,
            alias="Blocked by",
            title="Blocking dependency",
            description="Value of the 'Blocked by' custom field. None when the task is not blocked.",
        ),
    ]
    depends_on: Annotated[
        frozenset[int] | None,
        Field(
            default=None,
            alias="Depends on",
            title="Predecessor issue numbers",
            description=(
                "Set of predecessor issue numbers parsed from the 'Depends on' board field or "
                "the '## Depends on' issue body section. None if no dependencies are recorded."
            ),
        ),
    ]
    labels: Annotated[
        list[str],
        Field(
            default_factory=list,
            alias="labels",
            title="GitHub issue labels",
            description="Labels currently applied to the linked GitHub issue.",
            examples=[["bet:free-tier-signal"]],
        ),
    ]

    @property
    def primary_agent(self) -> AgentName | None:
        """The primary agent name (first alphabetically) or None if agents is not set."""
        if not self.agents:
            return None
        return min(self.agents)  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Project configuration cache
# ---------------------------------------------------------------------------


class ProjectConfig(BaseModel):
    """Cached GitHub Projects field and option node IDs.

    Persisted to .agents/tools/github_projects/project_config.json after
    first resolution. TTL = 24 hours. Commit to repo — node IDs are not secrets.

    field_ids  : {"Status": "PVTSSF_abc...", "Type": "PVTSSF_xyz...", ...}
    option_ids : {"Status": {"Backlog": "opt_001", "In Progress": "opt_002", ...}, ...}
    """

    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)

    project_number: Annotated[
        int,
        Field(
            alias="number",
            title="GitHub Project number",
            description=(
                "Numeric project identifier visible in the GitHub Projects URL. "
                "Example: 1 for https://github.com/users/harell/projects/1."
            ),
            gt=0,
            examples=[1],
        ),
    ]
    project_node_id: Annotated[
        str,
        Field(
            alias="id",
            title="Project GraphQL node ID",
            description=(
                "GitHub Projects v2 node ID (GraphQL). "
                "Required for all field mutation GraphQL calls. "
                "Example prefix: 'PVT_kwDOA...'."
            ),
            min_length=1,
            examples=["PVT_kwDOANN5s84ACbL0zgBVd94"],
        ),
    ]
    owner: Annotated[
        str,
        Field(
            alias="owner",
            title="GitHub owner login",
            description=(
                "GitHub username or organisation login that owns the project. "
                "Pass '@me' to refer to the authenticated user. "
                "Example: 'harell' or 'redmarklogic'."
            ),
            min_length=1,
            examples=["harell"],
        ),
    ]
    field_ids: Annotated[
        dict[str, str],
        Field(
            alias="field_ids",
            title="Custom field node IDs",
            description=(
                "Mapping of custom field name → GraphQL node ID. "
                "Keys are exact field names as configured on the board "
                "(e.g. 'Status', 'Type', 'Start date'). "
                "Values are node IDs with prefix 'PVTSSF_', 'PVTIF_', or 'PVTF_'."
            ),
            examples=[
                {
                    "Status": "PVTSSF_lADOANN5s84ACbL0zgBZrZg",
                    "Sprint": "PVTIF_lADOANN5s84ACbL0zgBah28",
                }
            ],
        ),
    ]
    option_ids: Annotated[
        dict[str, dict[str, str]],
        Field(
            alias="option_ids",
            title="Field option and iteration node IDs",
            description=(
                "Nested mapping of field name → option/iteration name → node ID. "
                "Single-select fields (Status, Type, Agent) and iteration fields (Sprint) "
                "require the option node ID for GraphQL mutations. "
                "Date and text fields are not present here."
            ),
            examples=[
                {
                    "Status": {
                        "Backlog": "f75ad846",
                        "In Progress": "47fc9ee4",
                        "Done": "98236657",
                    }
                }
            ],
        ),
    ]
    resolved_at: Annotated[
        datetime,
        Field(
            alias="resolved_at",
            title="Cache resolution timestamp",
            description=(
                "UTC datetime when the project config was last resolved from the GitHub API. "
                "The tool refreshes the cache when this value is more than 24 hours old."
            ),
            examples=["2026-06-03T10:00:00+00:00"],
        ),
    ]
