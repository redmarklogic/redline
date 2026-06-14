# Quickstart: Edit-to-Refresh Development Cycle

Spike notes for the Python-served Word taskpane dev loop (issue #192). Interim
home for the refresh-cycle runbook; #198 consolidates this into the durable
taskpane skill.

## Refresh cycle

How to change the taskpane and see the edit in desktop Microsoft Word without
restarting Word or re-sideloading the add-in.

### Prerequisites

- Add-in sideloaded once via the trusted catalog (issue #191 runbook).
- Dev certificate present: `rtk python -m addin.make_cert` (only if `src/addin/certs/` is empty).

### Steps

1. **Start the server via the launcher** (not bare `python -m addin.server`):

   ```powershell
   tasks/run-app.ps1
   ```

   The launcher sets `ADDIN_PORT=8767` and rebuilds the catalog manifest so the
   pane URL matches the bound port (`run-app.ps1:140,155`). Bare
   `python -m addin.server` binds port 3000 and the sideloaded pane — which
   loads `https://localhost:8767` — will fail to connect.

2. Open the taskpane in desktop Word (Insert > My Add-ins, per the #191 runbook).

3. Edit a visible string in `src/addin/static/taskpane.html` (e.g. the
   `Hello, world` heading) and **save**.

4. Reload the pane: **right-click inside the pane > Reload**.

5. Confirm the new string appears — no Word restart, no re-sideload.

The server never serves a stale page: `taskpane()` reads `taskpane.html` fresh
per request and sends `Cache-Control: no-store` + `Pragma: no-cache`
(`server.py`), so any staleness is the WebView2 cache, busted by the reload
above.

### Observed (fill in during verification — T007–T009)

- **Reload action that worked:** _<right-click Reload | close + reopen pane>_
- **Rough loop time (save -> visible change):** _<seconds>_
- **Fallback needed?** _<no | yes: which action>_

### Page loop vs server-code loop

Two distinct loops — do not confuse them:

- **Page edit** (`taskpane.html`, CSS, client JS): reload the pane (steps 3–5
  above). No server restart needed.
- **Server code** (`server.py` and other Python): the dev server runs with
  `use_reloader=True`, so it auto-restarts on save; then reload the pane to
  pick up the restarted server.
