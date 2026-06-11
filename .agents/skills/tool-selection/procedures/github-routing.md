# GitHub Operations (`gh`) — Command Reference

Loaded from `SKILL.md` when the routing rule resolves to `gh`.

| Operation | Command |
|---|---|
| List open PRs | `gh pr list --state open --repo <owner>/<repo>` |
| View a PR | `gh pr view <number>` |
| Create a PR | `gh pr create --title "..." --body "..."` |
| Merge a PR | `gh pr merge <number> --squash` |
| Check PR CI status | `gh pr checks <number>` |
| Create an issue | `gh issue create --title "..." --body "..."` |
| List issues | `gh issue list --state open` |
| View an issue | `gh issue view <number>` |
| Close an issue | `gh issue close <number>` |
| Clone a repo | `gh repo clone <owner>/<repo>` |
| View repo | `gh repo view <owner>/<repo>` |
| List Actions runs | `gh run list` |
| View a run | `gh run view <run-id>` |
| Watch a run live | `gh run watch <run-id>` |
| Re-run failed jobs | `gh run rerun <run-id> --failed` |
| List releases | `gh release list` |
| Create a release | `gh release create <tag> --notes "..."` |
| Check auth status | `gh auth status` |

## GitHub Projects (board operations)

**Critical:** GitHub Projects requires the `project` OAuth scope, which is NOT included in the default `gh auth login`. Always verify before any board write.

```sh
gh auth status          # check if 'project' appears in scopes
gh auth refresh -s project   # add project scope if missing
```

| Operation | Command |
|---|---|
| List project items | `gh project item-list <project-number> --owner <org>` |
| Add issue to project | `gh project item-add <project-number> --owner <org> --url <issue-url>` |
| Update a project field | `gh project item-edit --id <item-id> --field-id <field-id> --project-id <proj-id> --text "..."` |
| List project fields | `gh project field-list <project-number> --owner <org>` |
| Archive a project item | `gh project item-archive <project-number> --owner <org> --id <item-id>` |

> For complex field updates (custom single-select, iteration fields), prefer the Python tool at `.agents/tools/github_projects/` — it wraps the GraphQL API and handles field type resolution. See `github-projects` skill.
