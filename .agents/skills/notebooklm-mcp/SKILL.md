---
name: notebooklm-mcp

description: Setup and usage of the NotebookLM MCP server in VS Code, enabling GitHub Copilot Agent to query Google NotebookLM notebooks for citation-backed answers without leaving the editor.
---

# NotebookLM MCP

This skill covers how to connect GitHub Copilot (Agent mode) to Google NotebookLM via the

[`notebooklm-mcp`](https://github.com/PleasePrompto/notebooklm-mcp) MCP server. Once configured,

Copilot can query notebooks and return citation-backed answers directly inside VS Code.

## Context & Guidelines

- **Scope**: Apply this skill when you need to reference NotebookLM notebooks from within VS Code

  (e.g., querying project research, source documents, or literature notes during coding tasks).

- **Prerequisite**: A Google account with one or more notebooks in [NotebookLM](https://notebooklm.google/).
- **MCP server**: community-maintained; uses browser automation (Puppeteer/Chrome) to interact

  with NotebookLM. Authentication is handled entirely through MCP tools — no separate CLI auth

  command exists.

## Procedure

Before querying NotebookLM, complete the following steps in order:

### Step 1 — Is the MCP configured?

Check whether `.vscode/mcp.json` exists in the project root. If `.vscode/mcp.json` does not exist, create the file:

```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "npx",

      "args": ["-y", "notebooklm-mcp@latest"]
    }
  }
}
```

Then run the following in the terminal once to install the package:

```powershell

npx notebooklm-mcp@latest

```

Reload the VS Code window (**Developer: Reload Window**) so VS Code picks up the new config.

### Step 2 — Is the session authenticated?

Call the `get_health` MCP tool (or check using `mcp_notebooklm_setup_auth`) to verify the

authentication state. If the session is not authenticated (or this is a first install):

1. Call `mcp_notebooklm_setup_auth` — this opens a Chrome browser window.
2. The user signs in to their Google account in the popup.
3. The server saves the session locally. Credentials never leave the machine and must not be

   committed to version control.

4. Confirm success: the tool returns `"authenticated": true`.

If the session has expired or the user needs to switch accounts, call `mcp_notebooklm_re_auth`

instead.

### Step 3 — Query notebooks

Once authenticated, notebooks can be queried immediately using `mcp_notebooklm_ask_question`.

Optionally add notebooks to the managed library first using `mcp_notebooklm_add_notebook` so

notebooks can be referenced by name in future sessions.

### Step 4 — Plain-language tone

- **MUST** prepend the following prefix to every `ask_question` call unless the
  user has already specified an audience:

  ```
  Explain for the uninitiated. Define any specialist term or acronym the
  first time it appears. Keep citations. Avoid ambiguity.
  ```

- **MUST** write self-contained questions: use explicit noun phrases instead of
  pronouns (`"the CH4 flux model"`, not `"it"`; `"the kriging variance"`, not
  `"that value"`). Every question must be unambiguous when read in isolation.
- **MUST** scan the NotebookLM response for unexplained jargon or ambiguity. If any remains,
  append a short glossary at the end of the answer.
- **NEVER** rewrite the body of a NotebookLM response to simplify the response.
- **NEVER** remove or paraphrase citations returned by NotebookLM.

#### Correct

```
Explain for the uninitiated. Define any specialist term or acronym the
first time it appears. Keep citations.

What kriging model was selected for the CH4 flux interpolation and why
was that model preferred over ordinary kriging?
```

#### Incorrect

```
What model was selected and why was it preferred?
```

(Pronouns "it" and "model" are ambiguous without context; plain-language prefix is missing.)

## Usage Examples

Add a notebook to the library:

```

Add [notebooklm-share-link] to library tagged 'my-project, research'

```

Query a notebook:

```

Search my 'Project Phoenix' notebook for the authentication flow

```

List saved notebooks:

```

Show our notebooks

```

## Tips

- Notebook names are case-sensitive; match notebook names exactly when querying.
- The server spawns a headless Chrome instance; the first query per session may take a few

  seconds while the browser initialises.

- Say "Show me the browser" to watch the live NotebookLM interaction for debugging.
- Use a dedicated Google account rather than your primary account (browser automation caveat

  per upstream docs).

- Tool profiles: default is `standard` (10 tools). Run

  `npx notebooklm-mcp config set profile minimal` to load only 5 query tools and reduce token

  overhead.

## Troubleshooting

| Symptom | Fix |

| -------------------------------- | ------------------------------------------------------- |

| Server not listed in Copilot | Check `mcp.json` exists (see MCP Config Location below); reload VS Code window. |

|`npx` not found | Confirm Node.js >= 18 is installed and on the PATH. |

| Auth popup does not open | Call `mcp_notebooklm_setup_auth` directly. |

| Stale credentials / auth expired | Call `mcp_notebooklm_re_auth`. |

| Need a clean restart | See **Chrome exit code 21** procedure below. |

### MCP Config Location

The MCP config is **not** in `.vscode/mcp.json` for user-level installs — it lives at:

- **Windows**: `%APPDATA%\Code\User\mcp.json`
- **macOS/Linux**: `~/.config/Code/User/mcp.json`

Environment variables set in a terminal (e.g. PowerShell `$env:VAR=...`) have **no effect** on

the MCP server — the server is a child process of VS Code, not the shell. All env overrides

must be placed in the `mcp.json` `"env"` block, e.g.:

```json
{
  "servers": {
    "notebooklm": {
      "command": "npx",

      "args": ["-y", "notebooklm-mcp@latest"],

      "env": {
        "NOTEBOOK_PROFILE_STRATEGY": "isolated"
      }
    }
  }
}
```

After editing `mcp.json`, kill the old server processes (see below) so VS Code restarts them

with the new config.

### Chrome exit code 21 on Windows (known issue)

**Symptom**: Every `ask_question` call fails with

`browserType.launchPersistentContext: Target page, context or browser has been closed`

and Chrome exits immediately with `exitCode=21`. `cleanup_data` also partially fails because

the `chrome_profile` directory is locked.

**Root cause**: The persistent Chrome profile is corrupted (often from a previous force-kill).

`cleanup_data` cannot remove it while any `notebooklm-mcp` process is alive. This is a known

open issue ([#19](https://github.com/PleasePrompto/notebooklm-mcp/issues/19)).

**Fix** (run in PowerShell):

```powershell

# Step 1 — kill all notebooklm-mcp node processes

$pids = (Get-WmiObject Win32_Process |

    Where-Object { $_.Name -eq "node.exe" -and $_.CommandLine -like "*notebooklm*" }

).ProcessId

$pids | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }

Write-Host "Killed $($pids.Count) processes"

# Step 2 — delete the corrupted Chrome profile

Remove-Item -Recurse -Force "$env:LOCALAPPDATA\notebooklm-mcp\Data\chrome_profile" -ErrorAction SilentlyContinue

# Step 3 — re-authenticate via MCP tool (opens browser window)

# Call mcp_notebooklm_setup_auth from Copilot chat

```

After `setup_auth` returns `"authenticated": true`, the server creates a fresh profile and

subsequent `ask_question` calls work normally.

### Zombie process accumulation

Multiple `notebooklm-mcp` node processes can accumulate over time (known issue

[#29](https://github.com/PleasePrompto/notebooklm-mcp/issues/29)), consuming high CPU.

Diagnose with:

```powershell

Get-WmiObject Win32_Process |

    Where-Object { $_.Name -eq "node.exe" -and $_.CommandLine -like "*notebooklm*" } |

    Select-Object ProcessId, CommandLine | Format-List

```

Kill all matching processes using the Step 1 command above, then allow VS Code to restart the

`notebooklm-mcp` server automatically on the next tool call.

### Parallel notebook queries

Do not fire two `ask_question` calls to different notebooks simultaneously — both will attempt

to open the same persistent Chrome profile and one will fail with exit code 21. Query

notebooks **sequentially** instead.

## References

- [notebooklm-mcp GitHub repo](https://github.com/PleasePrompto/notebooklm-mcp)
- [notebooklm-mcp troubleshooting guide](https://github.com/PleasePrompto/notebooklm-mcp/blob/main/docs/troubleshooting.md)
- [notebooklm-mcp configuration reference](https://github.com/PleasePrompto/notebooklm-mcp/blob/main/docs/configuration.md)
- [VS Code MCP server configuration docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
