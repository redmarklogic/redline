import json
from github_projects.functions import resolve_project_config, list_tasks

cfg = resolve_project_config(project_number=1, owner="redmarklogic")
tasks = list_tasks(cfg, sprint="Sprint 2 - Jun 8-14")
out = [t.__dict__ for t in tasks]
print(json.dumps(out, default=str, indent=1))
