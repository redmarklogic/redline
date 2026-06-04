"""Phase 4 board enforcement checks.

Checks:
  1. blocked-without-reason  — Status=Blocked but Blocked by field is empty
  2. spec-link               — Source field does not point to an existing repo path
  3. done-without-open-issue — Status=Done but the linked GitHub issue is still OPEN

Exits 1 if any violations are found. Prints a summary table.

Project config is read from .agents/tools/github_projects/project_config.json
(committed to the repo). No CLI args needed for normal use.

Triggered by: daily schedule (weekdays 08:00 NZST) + workflow_dispatch.
Note: projects_v2_item is a webhook-only event (GitHub Apps), not a GitHub Actions trigger.

Usage:
    python .github/scripts/enforce_board.py
    python .github/scripts/enforce_board.py --repo redmarklogic/redline  # override repo
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_CONFIG_PATH = (
    _REPO_ROOT / ".agents" / "tools" / "github_projects" / "project_config.json"
)


def _read_project_config() -> tuple[int, str]:
    """Read project_number and owner from the committed project_config.json."""
    if not _CONFIG_PATH.exists():
        print(f"project_config.json not found at {_CONFIG_PATH}", file=sys.stderr)
        print(
            "Run resolve_project_config() first and commit the result.", file=sys.stderr
        )
        sys.exit(1)
    raw = json.loads(_CONFIG_PATH.read_text())
    return raw["project_number"], raw["owner"]


def _gh(*args: str) -> dict:
    r = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if r.returncode != 0:
        print(f"gh error: {r.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    return json.loads(r.stdout) if r.stdout.strip() else {}


def _issue_state(repo: str, issue_number: int) -> str:
    data = _gh("issue", "view", str(issue_number), "--repo", repo, "--json", "state")
    return data.get("state", "UNKNOWN")


def main() -> None:
    project_number, owner = _read_project_config()
    default_repo = f"{owner}/redline"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        default=default_repo,
        help=f"GitHub repo slug (default: {default_repo})",
    )
    args = parser.parse_args()

    sys.path.insert(0, str(_REPO_ROOT / ".agents" / "tools"))
    from github_projects import list_tasks, resolve_project_config

    config = resolve_project_config(project_number, owner)
    items = list_tasks(config)

    violations: list[tuple[str, str, str]] = []  # (check, title, detail)

    for item in items:
        url = item.issue_url
        title = item.title[:60]

        # 1. Blocked-without-reason
        if item.status == "Blocked" and not item.blocked_by:
            violations.append(("blocked-without-reason", title, url))

        # 2. Spec-link validation
        if item.source and item.source != "none":
            source_path = _REPO_ROOT / item.source.rstrip("/")
            if not source_path.exists():
                violations.append(
                    ("invalid-spec-link", title, f"{item.source!r} not found — {url}")
                )

        # 3. Done-without-open-issue
        if item.status == "Done" and url:
            issue_num = int(url.rstrip("/").split("/")[-1])
            state = _issue_state(args.repo, issue_num)
            if state == "OPEN":
                violations.append(
                    (
                        "done-with-open-issue",
                        title,
                        f"issue #{issue_num} is still OPEN — {url}",
                    )
                )

    if not violations:
        print(f"[board-enforcement] All {len(items)} items pass. No violations.")
        sys.exit(0)

    print(f"\n[board-enforcement] {len(violations)} violation(s) found:\n")
    print(f"{'CHECK':<28} {'TITLE':<45} DETAIL")
    print("-" * 110)
    for check, title, detail in violations:
        print(f"{check:<28} {title:<45} {detail}")
    print()

    # Add 'missing-block-reason' label to blocked items missing a reason
    for check, title, detail in violations:
        if check == "blocked-without-reason" and detail.startswith("http"):
            issue_num = int(detail.rstrip("/").split("/")[-1])
            subprocess.run(
                [
                    "gh",
                    "issue",
                    "edit",
                    str(issue_num),
                    "--repo",
                    args.repo,
                    "--add-label",
                    "missing-block-reason",
                ],
                capture_output=True,
            )
        elif check == "invalid-spec-link" and "github.com" in detail:
            url_part = [p for p in detail.split() if p.startswith("http")]
            if url_part:
                issue_num = int(url_part[0].rstrip("/").split("/")[-1])
                subprocess.run(
                    [
                        "gh",
                        "issue",
                        "edit",
                        str(issue_num),
                        "--repo",
                        args.repo,
                        "--add-label",
                        "missing-spec-link",
                    ],
                    capture_output=True,
                )

    sys.exit(1)


if __name__ == "__main__":
    main()
