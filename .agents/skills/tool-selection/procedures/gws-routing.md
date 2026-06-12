# Google Workspace Operations (`gws`) — Command Reference

Loaded from `SKILL.md` when the routing rule resolves to `gws`.

Command pattern: `gws <service> <resource> <method> [flags]`
Helper shortcuts use `+` prefix: `gws gmail +send`, `gws drive +upload`

## Pre-flight (run before first `gws` use in a session)

```sh
gws auth status   # verify authenticated account and scopes
```

Remediation (auth failures — per SKILL.md Auth-Failure Protocol):

- Not set up → `gws auth setup` (automated, requires gcloud installed) or `gws auth login` (manual OAuth fallback) — **both require user browser interaction**; ask the user to complete consent, then re-check.
- Scope-limited / silent failures → unverified apps hit ~25-scope limit; user must add themselves as test user in the OAuth consent screen, then re-run `gws auth setup`.

> **Shell requirement:** `gws --params` uses single-quoted JSON. Use Bash, not PowerShell — PS5.1 mangles curly-brace quoting and the command fails with "key must be a string".

| Operation | Command |
|---|---|
| Unread inbox summary | `gws gmail +triage` |
| List Gmail inbox | `gws gmail users messages list --params '{"labelIds":["INBOX"],"maxResults":20}'` |
| Read a message (extract body/headers) | `gws gmail +read --message-id <id>` |
| Send email | `gws gmail +send --to user@example.com --subject "Subject" --body "Body"` |
| Reply to email | `gws gmail +reply --message-id <id> --body "..."` |
| Reply-all | `gws gmail +reply-all --message-id <id> --body "..."` |
| Forward a message | `gws gmail +forward --message-id <id> --to user@example.com` |
| Watch inbox (streaming) | `gws gmail +watch` |
| List Drive files | `gws drive files list --params '{"pageSize":20}'` |
| Upload a file | `gws drive +upload --file path/to/file.pdf` |
| Share a file | `gws drive permissions create --params '{"fileId":"...","role":"reader","type":"user"}'` |
| List calendar events | `gws calendar events list --params '{"calendarId":"primary","timeMin":"..."}'` |
| Create calendar event | `gws calendar +insert --summary "Meeting" --start "2026-06-10T10:00:00Z" --end "..."` |
| Read a Sheet | `gws sheets +read --spreadsheet <id> --range "Sheet1!A1:D10"` |
| Append to a Sheet | `gws sheets +append --spreadsheet <id> --values "row data"` |
| Read a Doc | `gws docs documents get --params '{"documentId":"..."}'` |
| Write to a Doc | `gws docs +write --document <id> --content "..."` |
| Send Chat message | `gws chat +send --space <space-id> --text "..."` |
| List Workspace users (Admin) | `gws admin directory users list --params '{"domain":"example.com"}'` |

**Output format flag:** append `--format json` (or `table`, `yaml`, `csv`) to any command.
**Paginate all results:** append `--page-all` for automatic pagination as NDJSON.
**Dry run:** append `--dry-run` to preview without executing.
