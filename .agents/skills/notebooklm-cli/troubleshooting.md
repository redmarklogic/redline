# NotebookLM CLI Troubleshooting

Known failure modes for the `nlm` CLI on Windows.
Organised by symptom for fast lookup.

## Chrome / Edge detection

| Symptom | Cause | Fix |
|---------|-------|-----|
| `nlm doctor` reports `Chrome: not found` | Chrome installed at user level (`%LOCALAPPDATA%\...`); `nlm` only scans system-level paths | `nlm config set auth.browser edge` |
| `nlm login` fails with browser not found | Same as above | Same as above |

Edge is always present on Windows at
`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`.

## Authentication

| Symptom | Cause | Fix |
| --- | --- | --- |
| Command returns `"No authentication found"` | `nlm login` not completed | Run `nlm login` in a terminal |
| Command returns `status: error`, `error_reason: "expired"` | Auth cookies fully expired | Re-run `nlm login` |
| Command returns `status: error`, `error_reason: "stale_heuristic"` | Cookies likely expired based on age heuristic | Re-run `nlm login` |
| Command returns `status: error`, `error_reason: "no_tokens"` | No credentials stored at all | Run `nlm login` (first-time setup) |
| Queries fail after weeks of working | Auth cookies expired (2-4 week lifetime) | Re-run `nlm login` |

Cookies are stored locally at `~/.notebooklm-mcp-cli/`. Never commit them.
Re-running `nlm login` takes effect immediately for the next command.

## CLI

| Symptom | Cause | Fix |
|---------|-------|-----|
| `nlm` not found | CLI not installed | `rtk uv tool install notebooklm-mcp-cli` |
| Unknown flag / command | Published docs lag the installed binary | Confirm with `nlm <command> --help` |
| General diagnostics needed | -- | Run `nlm doctor` |
