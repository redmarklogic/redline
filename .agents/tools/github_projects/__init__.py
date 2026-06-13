"""GitHub Projects CLI tool — Pydantic-typed wrappers around `gh project` commands."""

from .functions import (
    count_tasks,
    create_task,
    delete_task,
    get_task,
    list_tasks,
    move_task,
    resolve_project_config,
    update_task,
)
from .schema import (
    ProjectConfig,
    StatusValue,
    TaskCreate,
    TaskRecord,
    TaskResult,
    TaskType,
    TaskUpdate,
)

__all__ = [
    # Schema
    "ProjectConfig",
    "StatusValue",
    "TaskCreate",
    "TaskRecord",
    "TaskResult",
    "TaskType",
    "TaskUpdate",
    # Functions
    "count_tasks",
    "create_task",
    "delete_task",
    "get_task",
    "list_tasks",
    "move_task",
    "resolve_project_config",
    "update_task",
]
