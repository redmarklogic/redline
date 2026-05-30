# RTK Rewrite Hook Validation

Procedure to confirm the `.github/hooks/rtk-rewrite.json` PreToolUse hook fires and rewrites Copilot terminal commands.

## Prerequisites

- RTK installed and on PATH (`rtk --version`)
- `.github/hooks/rtk-rewrite.json` present in repo root
- VS Code with GitHub Copilot extension active

## Validation Steps

### Step 1: Confirm hook file exists

```
ls .github/hooks/rtk-rewrite.json
```

Expected: file exists with `PreToolUse` hook configuration pointing to `rtk hook copilot`.

### Step 2: Trigger a terminal command via Copilot

In Copilot Chat, ask it to run a bare command such as:

> Run `git status` in the terminal

Observe the actual command executed in the terminal. If the hook is active, the command will be rewritten to `rtk git status`.

### Step 3: Check rtk gain history

<!-- rtk:skip -->
```bash
rtk gain --history
```

Expected output: at least one entry showing a rewritten command with token savings.

### Step 4: Verify token savings dashboard

<!-- rtk:skip -->
```bash
rtk gain
```

Expected: summary showing cumulative token savings across sessions.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Hook does not fire | `.github/hooks/` not in Copilot hook search path | Verify VS Code setting `github.copilot.chat.hooks.path` points to `.github/hooks/` |
| `rtk` command not found | RTK not installed | Run `uv tool install rtk` |
| `rtk gain --history` shows no entries | No commands have been proxied | Run any `rtk <cmd>` manually, then check again |
| Hook fires but command fails | RTK version mismatch | Update RTK: `uv tool upgrade rtk` |

## Validation Cadence

Run this procedure:
- After VS Code major updates
- After RTK version upgrades
- Monthly as part of tooling health check
