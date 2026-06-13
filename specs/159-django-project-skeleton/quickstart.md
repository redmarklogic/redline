# Quickstart: Django Project Skeleton (#159)

Verifies the three done-when criteria from issue #159 on a fresh clone.

## 1. Install (resolves Django from the manifest)

```powershell
rtk uv sync
```

## 2. Configuration check — must report zero issues (done-when 2)

```powershell
rtk uv run python manage.py check
```

Expected output: `System check identified no issues (0 silenced).`
Runs headless: no database, no network. Exit code 0.

## 3. Boot and hit the root page (done-when 1)

```powershell
rtk uv run python manage.py runserver 127.0.0.1:8766
```

Then `GET http://127.0.0.1:8766/` (browser or `curl -i`) — expect `HTTP 200` and a
minimal placeholder page. Port 8766 is the project convention for the Django web app
(8765 = marker/FastAPI; 8000 is avoided — reserved by common tooling).

## 4. Smoke tests (executable form of done-when 1 + 2)

```powershell
rtk uv run pytest tests/web/
```

## Expected oddities (do not "fix")

- **`runserver` warns about unapplied migrations** — expected and harmless. No
  database exists in this slice by design; #164 owns DATABASES + migrate.
- **`/admin/` renders a login form but cannot log anyone in** — admin is enabled at
  launch per ADR-024 yet has no database (#164) or users (#165) behind it.
- **Port 8766 is the project convention** for the Django web app. The marker (FastAPI)
  app uses 8765. Neither uses 8000 — that port is avoided project-wide. Use
  `tasks/run-app.ps1` to start both together; the script enforces these ports and
  fails hard if either is occupied by a foreign process.
- **Dev-only settings** — `SECRET_KEY` (dev-insecure prefix) and `DEBUG=True` are
  the generated baseline; environment-only boot is #161's done-when, next task in
  the dependency chain.
