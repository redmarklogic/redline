"""GitHub Projects CLI wrappers.

All GitHub interaction is performed by shelling out to the `gh` CLI.
No REST/GraphQL client is imported — `gh` handles authentication and
translates to the GraphQL API.

Security rules:
- `shell=False` always (prevents shell injection).
- Arguments are passed as a list, never interpolated into a string.
- `check=False` — non-zero exit codes are mapped to TaskResult, not raised.

Conventions:
- Public functions return typed Pydantic models.
- Private helpers are prefixed with `_`.
- `_run_gh` is the single subprocess call-site — all gh invocations go through it.
- `project_config.json` is persisted after `resolve_project_config` runs.
  It is the only persistent state this module owns.
"""

import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, NamedTuple

from .schema import (
    ProjectConfig,
    StatusValue,
    TaskCreate,
    TaskRecord,
    TaskResult,
    TaskUpdate,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_CONFIG_PATH: Path = Path(__file__).parent / "project_config.json"
_CACHE_TTL: timedelta = timedelta(hours=24)

# gh project item-list truncates at --limit (default 30). The board passed 100
# items during Sprint-3 planning and the old hardcoded limit silently hid new
# issues. Fetch generously; _fetch_items refetches if totalCount exceeds this.
_ITEM_LIST_LIMIT = 500

# Custom field name constants — defined once to avoid duplicated string literals.
_FIELD_STATUS = "Status"
_FIELD_TYPE = "Task Type"
_FIELD_AGENT = "Agent"
_FIELD_SPRINT = "Sprint"
_FIELD_START_DATE = "Start date"
_FIELD_TARGET_DATE = "Target date"
_FIELD_BLOCKED_BY = "Blocked by"
_FIELD_SOURCE = "Source"

_MUTATION_SELECT = """
mutation {{
  updateProjectV2ItemFieldValue(input: {{
    projectId: "{project_id}"
    itemId: "{item_id}"
    fieldId: "{field_id}"
    value: {{ {value_key}: "{value}" }}
  }}) {{ projectV2Item {{ id }} }}
}}
"""

_MUTATION_TEXT = """
mutation {{
  updateProjectV2ItemFieldValue(input: {{
    projectId: "{project_id}"
    itemId: "{item_id}"
    fieldId: "{field_id}"
    value: {{ text: "{value}" }}
  }}) {{ projectV2Item {{ id }} }}
}}
"""

_MUTATION_DATE = """
mutation {{
  updateProjectV2ItemFieldValue(input: {{
    projectId: "{project_id}"
    itemId: "{item_id}"
    fieldId: "{field_id}"
    value: {{ date: "{value}" }}
  }}) {{ projectV2Item {{ id }} }}
}}
"""

_VALID_STATUSES: frozenset[str] = frozenset(
    {"Backlog", "In Progress", "Blocked", "To Review", "Done"}
)


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------


def _run_gh(*args: str) -> tuple[int, Any, str]:
    """Shell out to gh. Returns (returncode, parsed_json_or_None, stderr).

    encoding is pinned to UTF-8: on Windows, text=True alone decodes with
    cp1252 and crashes (UnicodeDecodeError) on emoji/en-dash in issue bodies.
    """
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        return result.returncode, None, result.stderr.strip()
    if not result.stdout.strip():
        return 0, None, ""
    try:
        return 0, json.loads(result.stdout), ""
    except json.JSONDecodeError:
        return 500, None, f"gh returned non-JSON output: {result.stdout[:200]}"


def _graphql(query: str) -> tuple[int, Any, str]:
    return _run_gh("api", "graphql", "-f", f"query={query}")


def _map_gh_error(stderr: str) -> int:
    lower = stderr.lower()
    if "authentication" in lower or "credentials" in lower or "auth" in lower:
        return 401
    if "not found" in lower or "could not resolve" in lower:
        return 404
    return 422


def _ok(
    issue_url: str | None = None, item_id: str | None = None, raw: Any = None
) -> TaskResult:
    return TaskResult(
        ok=True,
        status_code=200,
        message="OK",
        issue_url=issue_url,
        item_id=item_id,
        raw=raw,
    )


def _err(*, status_code: int, message: str) -> TaskResult:
    return TaskResult(ok=False, status_code=status_code, message=message)


# ---------------------------------------------------------------------------
# Field mutation helpers
# ---------------------------------------------------------------------------


class _WriteCtx(NamedTuple):
    """Shared context passed to all field-write helpers."""

    item_id: str
    pid: str
    config: ProjectConfig


@dataclass(frozen=True, slots=True)
class _FieldValues:
    """Container for task field values to pass to _write_all_fields.

    Reduces function signature from 10 parameters to 3.
    """

    status: str | None
    task_type: str | None
    agent: str | None
    start_date: Any
    target_date: Any
    source: str | None
    blocked_by: str | None
    sprint: str | None


def _set_select(
    item_id: str, project_id: str, field_id: str, option_id: str
) -> TaskResult:
    query = _MUTATION_SELECT.format(
        project_id=project_id,
        item_id=item_id,
        field_id=field_id,
        value_key="singleSelectOptionId",
        value=option_id,
    )
    rc, data, stderr = _graphql(query)
    if rc == 0:
        return _ok(item_id=item_id, raw=data)
    return _err(status_code=_map_gh_error(stderr), message=stderr)


def _set_iteration(
    item_id: str, project_id: str, field_id: str, iteration_id: str
) -> TaskResult:
    query = _MUTATION_SELECT.format(
        project_id=project_id,
        item_id=item_id,
        field_id=field_id,
        value_key="iterationId",
        value=iteration_id,
    )
    rc, data, stderr = _graphql(query)
    if rc == 0:
        return _ok(item_id=item_id, raw=data)
    return _err(status_code=_map_gh_error(stderr), message=stderr)


def _set_text(item_id: str, project_id: str, field_id: str, value: str) -> TaskResult:
    query = _MUTATION_TEXT.format(
        project_id=project_id,
        item_id=item_id,
        field_id=field_id,
        value=value.replace('"', '\\"'),
    )
    rc, data, stderr = _graphql(query)
    if rc == 0:
        return _ok(item_id=item_id, raw=data)
    return _err(status_code=_map_gh_error(stderr), message=stderr)


def _set_date(item_id: str, project_id: str, field_id: str, value: str) -> TaskResult:
    query = _MUTATION_DATE.format(
        project_id=project_id,
        item_id=item_id,
        field_id=field_id,
        value=value,
    )
    rc, data, stderr = _graphql(query)
    if rc == 0:
        return _ok(item_id=item_id, raw=data)
    return _err(status_code=_map_gh_error(stderr), message=stderr)


def _option_id(config: ProjectConfig, field: str, value: str) -> str | None:
    return config.option_ids.get(field, {}).get(value)


# ---------------------------------------------------------------------------
# Bulk field writer — shared between create and update
# ---------------------------------------------------------------------------


def _write_select(
    ctx: _WriteCtx, field: str, value: str | None, errors: list[str]
) -> None:
    if value is None or field not in ctx.config.field_ids:
        return
    oid = _option_id(ctx.config, field, value)
    if not oid:
        errors.append(f"{field} option '{value}' not found in project config")
        return
    r = _set_select(ctx.item_id, ctx.pid, ctx.config.field_ids[field], oid)
    if not r.ok:
        errors.append(f"{field}: {r.message}")


def _write_date(ctx: _WriteCtx, field: str, value: Any, errors: list[str]) -> None:
    if value is None or field not in ctx.config.field_ids:
        return
    r = _set_date(ctx.item_id, ctx.pid, ctx.config.field_ids[field], value.isoformat())
    if not r.ok:
        errors.append(f"{field}: {r.message}")


def _write_text(
    ctx: _WriteCtx, field: str, value: str | None, errors: list[str]
) -> None:
    if not value or field not in ctx.config.field_ids:
        return
    r = _set_text(ctx.item_id, ctx.pid, ctx.config.field_ids[field], value)
    if not r.ok:
        errors.append(f"{field}: {r.message}")


def _write_sprint(ctx: _WriteCtx, sprint: str | None, errors: list[str]) -> None:
    if not sprint or _FIELD_SPRINT not in ctx.config.field_ids:
        return
    sid = _option_id(ctx.config, _FIELD_SPRINT, sprint)
    if sid:
        r = _set_iteration(
            ctx.item_id, ctx.pid, ctx.config.field_ids[_FIELD_SPRINT], sid
        )
        if not r.ok:
            errors.append(f"Sprint: {r.message}")
    else:
        errors.append(
            f"Sprint '{sprint}' not found — run resolve_project_config(force_refresh=True)"
        )


def _write_all_fields(
    ctx: _WriteCtx,
    errors: list[str],
    fields: _FieldValues,
) -> None:
    _write_select(ctx, _FIELD_STATUS, fields.status, errors)
    _write_select(ctx, _FIELD_TYPE, fields.task_type, errors)
    _write_select(ctx, _FIELD_AGENT, fields.agent, errors)
    _write_date(ctx, _FIELD_START_DATE, fields.start_date, errors)
    _write_date(ctx, _FIELD_TARGET_DATE, fields.target_date, errors)
    _write_text(ctx, _FIELD_SOURCE, fields.source, errors)
    _write_text(ctx, _FIELD_BLOCKED_BY, fields.blocked_by, errors)
    _write_sprint(ctx, fields.sprint, errors)


# ---------------------------------------------------------------------------
# Config cache helpers
# ---------------------------------------------------------------------------


def _load_cached_config() -> ProjectConfig | None:
    if not _CONFIG_PATH.exists():
        return None
    try:
        cached = ProjectConfig.model_validate_json(_CONFIG_PATH.read_text())
        if datetime.now(tz=UTC) - cached.resolved_at < _CACHE_TTL:
            return cached
    except ValueError:
        pass
    return None


def _resolve_fields_from_api(
    project_number: int,
    owner: str,
) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    rc, data, stderr = _run_gh(
        "project",
        "field-list",
        str(project_number),
        "--owner",
        owner,
        "--format",
        "json",
    )
    if rc != 0:
        raise RuntimeError(f"gh project field-list failed: {stderr}")
    field_ids: dict[str, str] = {}
    option_ids: dict[str, dict[str, str]] = {}
    for field in (data or {}).get("fields", []):
        name: str = field.get("name", "")
        fid: str = field.get("id", "")
        if not name or not fid:
            continue
        field_ids[name] = fid
        options = field.get("options", [])
        if options:
            option_ids[name] = {opt["name"]: opt["id"] for opt in options}

    # Fetch iteration IDs for ITERATION fields via GraphQL (gh field-list omits them)
    iteration_ids = _resolve_iteration_ids(project_number, owner)
    option_ids.update(iteration_ids)
    return field_ids, option_ids


def _resolve_iteration_ids(
    project_number: int,
    owner: str,
) -> dict[str, dict[str, str]]:
    """Return {field_name: {iteration_title: iteration_id}} for all iteration fields."""
    query = (
        "query($login: String!, $num: Int!) {"
        "  organization(login: $login) {"
        "    projectV2(number: $num) {"
        "      fields(first: 30) {"
        "        nodes {"
        "          ... on ProjectV2IterationField {"
        "            name"
        "            configuration {"
        "              iterations { id title }"
        "              completedIterations { id title }"
        "            }"
        "          }"
        "        }"
        "      }"
        "    }"
        "  }"
        "}"
    )
    import json as _json

    body = _json.dumps(
        {"query": query, "variables": {"login": owner, "num": project_number}}
    )
    import subprocess as _sub

    result = _sub.run(
        ["gh", "api", "graphql", "--input", "-"],
        input=body,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        return {}
    try:
        data = _json.loads(result.stdout)
    except Exception:
        return {}
    fields = (
        data.get("data", {})
        .get("organization", {})
        .get("projectV2", {})
        .get("fields", {})
        .get("nodes", [])
    )
    result_map: dict[str, dict[str, str]] = {}
    for field in fields:
        fname = field.get("name")
        if not fname:
            continue
        config = field.get("configuration") or {}
        iterations = config.get("iterations", []) + config.get(
            "completedIterations", []
        )
        if iterations:
            result_map[fname] = {it["title"]: it["id"] for it in iterations}
    return result_map


# ---------------------------------------------------------------------------
# Issue body builder
# ---------------------------------------------------------------------------


def _build_body(task: TaskCreate) -> str:
    parts: list[str] = []
    if task.purpose:
        parts.append(f"## Purpose\n{task.purpose}")
    parts.append(f"## Source\n`{task.source}`")
    if task.done_when:
        parts.append(f"## Done when\n{task.done_when}")
    parts.append(f"## Agents\n{', '.join(sorted(task.agents))}")
    if task.depends_on:
        parts.append(
            f"## Depends on\n{', '.join(f'#{n}' for n in sorted(task.depends_on))}"
        )
    if task.body:
        parts.append(task.body)
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def resolve_project_config(
    project_number: int,
    owner: str,
    *,
    force_refresh: bool = False,
) -> ProjectConfig:
    """Discover and cache field/option node IDs for a GitHub Project.

    Reads from project_config.json if it exists and is within the 24-hour TTL.
    Set force_refresh=True to bypass the cache (e.g., after adding a new field).

    The config file is committed to the repo — node IDs are not secrets.
    """
    if not force_refresh:
        cached = _load_cached_config()
        if cached is not None:
            return cached

    rc, data, stderr = _run_gh("project", "list", "--owner", owner, "--format", "json")
    if rc != 0:
        raise RuntimeError(f"gh project list failed: {stderr}")

    project_node_id = next(
        (
            p["id"]
            for p in (data or {}).get("projects", [])
            if p.get("number") == project_number
        ),
        None,
    )
    if project_node_id is None:
        raise ValueError(f"Project #{project_number} not found for owner {owner!r}")

    field_ids, option_ids = _resolve_fields_from_api(project_number, owner)

    config = ProjectConfig(
        project_number=project_number,
        project_node_id=project_node_id,
        owner=owner,
        field_ids=field_ids,
        option_ids=option_ids,
        resolved_at=datetime.now(tz=UTC),
    )
    _CONFIG_PATH.write_text(config.model_dump_json(indent=2))
    return config


def create_task(task: TaskCreate, config: ProjectConfig) -> TaskResult:
    """Create a GitHub issue and add it to the project board.

    Returns TaskResult with issue_url and item_id on success.
    status_code 207 means the issue was created but some fields failed to set;
    ok is False in that case — the item exists, so repair the named fields via
    update_task rather than recreating (consistent with update_task's 207).
    """
    # Use REST API — gh issue create dropped --json support in v2.x
    api_args = [
        "api",
        f"repos/{config.owner}/redline/issues",
        "--method",
        "POST",
        "--field",
        f"title={task.title}",
        "--field",
        f"body={_build_body(task)}",
    ]
    for label in task.labels:
        api_args += ["--field", f"labels[]={label}"]

    rc, data, stderr = _run_gh(*api_args)
    if rc != 0:
        return _err(
            status_code=_map_gh_error(stderr),
            message=f"Failed to create issue: {stderr}",
        )
    issue_url: str = (data or {}).get("html_url", "")
    if not issue_url:
        return _err(status_code=500, message="Issue created but URL not returned")

    item_id, add_err = _add_issue_to_project(issue_url, config)
    if add_err:
        return _err(
            status_code=422,
            message=f"Issue created ({issue_url}) but failed to add to project: {add_err}",
        )

    ctx = _WriteCtx(item_id=item_id, pid=config.project_node_id, config=config)
    errors: list[str] = []
    fields = _FieldValues(
        status=task.status,
        task_type=task.task_type,
        agent=task.primary_agent,
        start_date=task.start_date,
        target_date=task.target_date,
        source=task.source,
        blocked_by=task.blocked_by,
        sprint=task.sprint,
    )
    _write_all_fields(ctx, errors, fields)
    if errors:
        return TaskResult(
            ok=False,
            status_code=207,
            message=f"Task created ({issue_url}) but some fields failed: {'; '.join(errors)}",
            issue_url=issue_url,
            item_id=item_id,
        )
    return _ok(issue_url=issue_url, item_id=item_id)


def update_task(update: TaskUpdate, config: ProjectConfig) -> TaskResult:
    """Update one or more fields on an existing project item.

    Only non-None fields in the TaskUpdate payload are written.
    Partial date updates (one date only) cannot be cross-validated here;
    callers must ensure date ordering when updating a single date field.
    """
    item_id = update.item_id
    pid = config.project_node_id
    ctx = _WriteCtx(item_id=item_id, pid=pid, config=config)
    errors: list[str] = []

    if update.title is not None:
        rc, _, stderr = _run_gh(
            "project",
            "item-edit",
            "--id",
            item_id,
            "--title",
            update.title,
            "--project-id",
            pid,
        )
        if rc != 0:
            errors.append(f"Title: {stderr}")

    fields = _FieldValues(
        status=update.status,
        task_type=update.task_type,
        agent=min(update.agents) if update.agents else None,
        start_date=update.start_date,
        target_date=update.target_date,
        source=update.source,
        blocked_by=update.blocked_by,
        sprint=update.sprint,
    )
    _write_all_fields(ctx, errors, fields)
    if errors:
        return TaskResult(
            ok=False,
            status_code=207,
            message=f"Partial update on {item_id}: {'; '.join(errors)}",
            item_id=item_id,
        )
    return _ok(item_id=item_id)


def move_task(
    item_id: str,
    status: StatusValue,
    config: ProjectConfig,
    *,
    blocked_by: str | None = None,
) -> TaskResult:
    """Move a project item to a new column (status field).

    `blocked_by` is keyword-only and required when status == "Blocked".
    Done is write-protected: only GitHub automation or the founder may set it.
    """
    if status == "Done":
        return _err(
            status_code=403,
            message="Agents may not set status to 'Done'. Only a merged PR or founder action can.",
        )
    if status == "Blocked" and not blocked_by:
        return _err(
            status_code=400,
            message="blocked_by is required when moving status to 'Blocked'",
        )

    oid = _option_id(config, _FIELD_STATUS, status)
    if not oid:
        return _err(
            status_code=422,
            message=f"Status option '{status}' not found in project config",
        )

    result = _set_select(
        item_id, config.project_node_id, config.field_ids[_FIELD_STATUS], oid
    )
    if not result.ok:
        return result

    if blocked_by and _FIELD_BLOCKED_BY in config.field_ids:
        r = _set_text(
            item_id,
            config.project_node_id,
            config.field_ids[_FIELD_BLOCKED_BY],
            blocked_by,
        )
        if not r.ok:
            return TaskResult(
                ok=True,
                status_code=207,
                message=f"Status → '{status}' but failed to set '{_FIELD_BLOCKED_BY}': {r.message}",
                item_id=item_id,
            )
    return _ok(item_id=item_id)


def delete_task(item_id: str, config: ProjectConfig) -> TaskResult:
    """Archive (remove from project view) a project item.

    Does NOT close or delete the underlying GitHub Issue.
    To also close the issue, call `gh issue close <number>` separately.
    Only the founder should call this function.
    """
    rc, data, stderr = _run_gh(
        "project",
        "item-archive",
        "--id",
        item_id,
        "--project-id",
        config.project_node_id,
        "--format",
        "json",
    )
    if rc == 0:
        return _ok(item_id=item_id, raw=data)
    return _err(
        status_code=_map_gh_error(stderr),
        message=f"Failed to archive {item_id}: {stderr}",
    )


def _fetch_items_with_total(config: ProjectConfig) -> tuple[list[dict[str, Any]], int]:
    """Fetch ALL board items plus the authoritative totalCount.

    gh project item-list silently truncates at --limit; the JSON payload's
    totalCount reveals the true board size, so a single refetch at that size
    guarantees completeness. Returns ``(items, total)`` where ``total`` is the
    board's reported totalCount after any refetch.
    """

    def _page(limit: int) -> tuple[list[dict[str, Any]], int]:
        rc, data, stderr = _run_gh(
            "project",
            "item-list",
            str(config.project_number),
            "--owner",
            config.owner,
            "--format",
            "json",
            "--limit",
            str(limit),
        )
        if rc != 0:
            raise RuntimeError(f"gh project item-list failed: {stderr}")
        payload = data or {}
        return payload.get("items", []), int(payload.get("totalCount", 0))

    items, total = _page(_ITEM_LIST_LIMIT)
    if total > len(items):
        items, total = _page(total)
    return items, total


def _fetch_items(config: ProjectConfig) -> list[dict[str, Any]]:
    """Fetch ALL board items, refetching if the first page was truncated."""
    return _fetch_items_with_total(config)[0]


def count_tasks(config: ProjectConfig) -> int:
    """Return the authoritative total number of items on the board.

    Use this for the standup completeness assert instead of hand-rolling a
    `gh api graphql` query: in PowerShell the GraphQL ``$variable`` syntax
    collides with shell interpolation (``query($id: ID!)`` fails to parse).
    `_fetch_items` already guarantees a complete fetch, so
    ``len(list_tasks(config)) == count_tasks(config)`` by construction.
    """
    return _fetch_items_with_total(config)[1]


def get_task(item_id: str, config: ProjectConfig) -> TaskRecord | None:
    """Fetch a single project item by its node ID. Returns None if not found."""
    for item in _fetch_items(config):
        if item.get("id") == item_id:
            return _item_to_record(item)
    return None


def list_tasks(
    config: ProjectConfig,
    *,
    status: StatusValue | None = None,
    agent: str | None = None,
    sprint: str | None = None,
) -> list[TaskRecord]:
    """List project items, optionally filtered by status, agent, or sprint."""
    records = [_item_to_record(item) for item in _fetch_items(config)]
    if status is not None:
        records = [r for r in records if r.status == status]
    if agent is not None:
        records = [r for r in records if r.primary_agent == agent]
    if sprint is not None:
        records = [r for r in records if r.sprint == sprint]
    return records


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _add_issue_to_project(issue_url: str, config: ProjectConfig) -> tuple[str, str]:
    """Add a GitHub issue URL to the project. Returns (item_id, error_or_empty)."""
    rc, data, stderr = _run_gh(
        "project",
        "item-add",
        str(config.project_number),
        "--owner",
        config.owner,
        "--url",
        issue_url,
        "--format",
        "json",
    )
    if rc != 0:
        return "", stderr
    item_id = (data or {}).get("id", "")
    return item_id, ("" if item_id else "item ID not returned after add")


def _item_to_record(item: dict[str, Any]) -> TaskRecord:
    """Convert a raw gh project item dict to a TaskRecord.

    gh v2.x returns a flat dict with lowercase field names rather than the
    nested fieldValues structure used by older versions. Build a case-insensitive
    lookup over the flat item to handle both formats.
    """
    from datetime import date as Date

    # Build case-insensitive lookup from the flat item (gh v2.x format).
    flat: dict[str, Any] = {
        k.lower(): v
        for k, v in item.items()
        if k not in ("id", "title", "content", "repository")
    }

    def _get(field_name: str) -> Any:
        """Lookup field by exact name then by lowercase."""
        return item.get(field_name) or flat.get(field_name.lower())

    def _parse_date(field_name: str) -> Date | None:
        raw = _get(field_name)
        if not raw:
            return None
        try:
            return Date.fromisoformat(str(raw)[:10])
        except ValueError:
            return None

    raw_status = _get(_FIELD_STATUS) or "Backlog"
    status: StatusValue = raw_status if raw_status in _VALID_STATUSES else "Backlog"  # type: ignore[assignment]

    raw_agent = _get(_FIELD_AGENT)

    return TaskRecord(
        item_id=str(item.get("id", "")),
        issue_url=str(item.get("content", {}).get("url", "")),
        title=str(item.get("title") or item.get("content", {}).get("title", "")),
        status=status,
        task_type=_get(_FIELD_TYPE),  # type: ignore[arg-type]
        start_date=_parse_date(_FIELD_START_DATE),
        target_date=_parse_date(_FIELD_TARGET_DATE),
        source=_get(_FIELD_SOURCE),  # type: ignore[arg-type]
        agents=frozenset({raw_agent}) if raw_agent else None,  # type: ignore[arg-type]
        sprint=(_get(_FIELD_SPRINT) or {}).get("title")
        if isinstance(_get(_FIELD_SPRINT), dict)
        else _get(_FIELD_SPRINT),  # type: ignore[arg-type]
        blocked_by=_get(_FIELD_BLOCKED_BY),  # type: ignore[arg-type]
    )
