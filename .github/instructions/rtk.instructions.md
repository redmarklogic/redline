---
applyTo: "**"
---

<!-- rtk-instructions v2 -->
# RTK — Token-Optimized CLI

**rtk** is a CLI proxy that filters and compresses command outputs, saving 60-90% tokens.

## Rule

Always prefix shell commands with `rtk`:

<!-- rtk:skip -->
```bash
# Instead of:              Use:
git status                 rtk git status
git log -10                rtk git log -10
pytest                     rtk pytest
ruff check                 rtk ruff check
docker ps                  rtk docker ps
```

## Meta commands (use directly)

```bash
rtk gain              # Token savings dashboard
rtk gain --history    # Per-command savings history
rtk discover          # Find missed rtk opportunities
rtk proxy <cmd>       # Run raw (no filtering) but track usage
```
<!-- /rtk-instructions -->
