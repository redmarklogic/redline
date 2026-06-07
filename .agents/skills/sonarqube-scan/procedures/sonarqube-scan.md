# Procedure: sonarqube-scan

Trigger a static analysis scan on the current branch and confirm the
compute-engine task succeeds. `scan.ps1` / `scan.sh` handle availability
checking, branch derivation, properties generation, and CE polling internally —
surface any failure verbatim, never swallow it.

## Step 1 — Run the scanner

```powershell
./scan.ps1   # Windows
```

```sh
./scan.sh    # Linux / macOS
```

The script:

1. Checks `.env` for `SONAR_TOKEN` — throws if missing.
2. Checks SonarQube is `UP` at `localhost:9000` — throws if not.
3. Detects the current branch — throws on detached `HEAD`.
4. Generates `.cache/sonarqube/sonar-project.properties` from `pyproject.toml`
   `[tool.usethis]` (SSOT — do not edit the properties file directly).
5. Produces best-effort ruff + coverage reports; rewrites ruff paths to
   repo-relative so the Linux container can resolve them.
6. Runs `sonarsource/sonar-scanner-cli:11` in Docker.
7. Polls the compute-engine task (bounded, max 60 s) until `SUCCESS`.

A non-zero exit or a thrown error means the scan or CE task failed. Surface the
message and stop — do not retry blindly.

## Step 2 — Confirm SUCCESS

The script exits 0 only when the CE task reaches `SUCCESS`. On exit 0, proceed
to `sonarqube-review`. Any other outcome is a hard stop.
